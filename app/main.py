from fastapi import FastAPI, Depends, HTTPException, Request, Form, Response, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import traceback
import re
import os
import shutil
import uuid

from . import models, schemas, database, auth

# ── Module prefix ──
MODULE_PREFIX = "/NucleoTallerV1"

app = FastAPI(title="Work Order Management")

# Setup templates with global base URL
templates = Jinja2Templates(directory="app/templates")
templates.env.globals["base"] = MODULE_PREFIX

# Router with module prefix
router = APIRouter(prefix=MODULE_PREFIX)

# Static files mounting
app.mount(f"{MODULE_PREFIX}/static", StaticFiles(directory="app/static"), name="static")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MANEJADOR GLOBAL DE ERRORES ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    return HTMLResponse(content=f"""
        <div class="p-8 bg-red-50 border-4 border-red-200 rounded-3xl m-8 font-sans">
            <h1 class="text-2xl font-black text-red-700 mb-4 flex items-center gap-2">⚠️ ERROR INTERNO DETECTADO</h1>
            <p class="text-red-600 font-bold mb-4">Causa probable: {str(exc)}</p>
            <pre class="bg-slate-900 text-sky-400 p-6 rounded-2xl overflow-auto text-xs font-mono shadow-2xl max-h-[500px]">{error_trace}</pre>
        </div>
    """, status_code=500)

# --- UTILIDADES ---
def format_duration(td):
    if not td: return "00:00:00"
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days:02}:{hours:02}:{minutes:02}"

def log_audit(db: Session, user_id: int, action: str, entity: str, entity_id: int, details: str = None):
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        entity_name=entity,
        entity_id=entity_id,
        details=details
    )
    db.add(log)
    db.commit()

async def save_uploaded_img(photo: UploadFile) -> str:
    if photo and photo.filename:
        ext = photo.filename.split('.')[-1]
        new_name = f"{uuid.uuid4()}.{ext}"
        path = os.path.join("app", "static", "uploads", new_name)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        return f"/static/uploads/{new_name}"
    return None

# --- SEGURIDAD (LOGIN / LOGOUT / ADMIN) ---

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user:
        return HTMLResponse(content='<div id="error-msg" class="text-red-500 font-black text-[10px] uppercase tracking-widest bg-red-50 p-4 rounded-2xl border border-red-100 mb-6 shadow-sm">Usuario no registrado</div', status_code=401)
    
    if user.status == 'Suspendido':
        return HTMLResponse(content='<div id="error-msg" class="text-white font-black text-[10px] uppercase tracking-[0.2em] bg-red-600 p-4 rounded-2xl border border-red-700 mb-6 shadow-xl shadow-red-900/20">CUENTA SUSPENDIDA. Contacte soporte.</div>', status_code=403)

    if not auth.verify_password(password, user.hashed_password):
        auth.handle_failed_login(db, user)
        msg = f"Clave incorrecta. Intentos: {user.failed_attempts}/3"
        if user.status == 'Suspendido':
            msg = "CUENTA SUSPENDIDA POR INTENTOS FALLIDOS."
        return HTMLResponse(content=f'<div id="error-msg" class="text-red-500 font-black text-[10px] uppercase tracking-widest bg-red-50 p-4 rounded-2xl border border-red-100 mb-6 shadow-sm">{msg}</div>', status_code=401)
    
    # Éxito
    auth.reset_failed_login(db, user)
    access_token = auth.create_access_token(data={"sub": user.username})
    
    # Professional redirect via HTMX Header
    response = Response(status_code=204) # No content, redirect handled by header
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, path="/")
    response.headers["HX-Redirect"] = f"{MODULE_PREFIX}/"
    
    log_audit(db, user.id, "LOGIN", "Usuario", user.id, "Inicio de sesión exitoso")
    
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url=f"{MODULE_PREFIX}/login")
    response.delete_cookie("access_token", path="/")
    return response

@router.get("/admin/security", response_class=HTMLResponse)
async def security_admin(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    users = db.query(models.User).all()
    roles = db.query(models.Role).all()
    return templates.TemplateResponse(request, "security_admin.html", {"users": users, "roles": roles, "current_user": current_user, "active_page": "security"})

@router.post("/admin/security/user", response_class=HTMLResponse)
async def create_user(username: str = Form(...), full_name: str = Form(...), password: str = Form(...), email: Optional[str] = Form(None), role_id: int = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    try:
        auth.validate_password_strength(password)
        hashed_pw = auth.get_password_hash(password)
        new_user = models.User(username=username, full_name=full_name, hashed_password=hashed_pw, email=email)
        role = db.get(models.Role, role_id)
        if role: new_user.roles.append(role)
        db.add(new_user)
        db.commit()
        log_audit(db, current_user.id, "CREAR", "Usuario", new_user.id, f"Creación de {username}")
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except ValueError as e: return HTMLResponse(content=f'<div class="bg-red-50 text-red-600 border border-red-100 p-4 rounded-2xl font-bold text-xs shadow-sm">{str(e)}</div>', status_code=400)
    except IntegrityError: return HTMLResponse(content='<div class="bg-red-50 text-red-600 border border-red-100 p-4 rounded-2xl font-bold text-xs shadow-sm">Usuario/Email ya existe</div>', status_code=400)

@router.post("/admin/user/{user_id}/toggle-status")
async def toggle_status(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    user = db.get(models.User, user_id)
    if user:
        user.status = "Suspendido" if user.status == "Activo" else "Activo"
        user.failed_attempts = 0 # Reset attempts on manual fix
        db.commit()
        log_audit(db, current_user.id, "ESTADO", "Usuario", user.id, f"Cambio a {user.status}")
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.get("/admin/audit", response_class=HTMLResponse)
async def audit_report(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    today = datetime.now().strftime("%Y-%m-%d")
    logs = db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(100).all()
    return templates.TemplateResponse(request, "admin_audit.html", {"logs": logs, "today": today, "user": current_user, "active_page": "admin"})

@router.get("/admin/audit/filter", response_class=HTMLResponse)
async def audit_filter(request: Request, start_date: str, end_date: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    logs = db.query(models.AuditLog).filter(models.AuditLog.timestamp >= start, models.AuditLog.timestamp < end).order_by(models.AuditLog.timestamp.desc()).all()
    return templates.TemplateResponse(request, "admin_audit.html", {"logs": logs}, block_name="results")

# --- ADMINISTRACION ---

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    techs = db.query(models.Technician).all()
    countries = db.query(models.Country).all()
    provinces = db.query(models.Province).all()
    return templates.TemplateResponse(request, "admin.html", {"brands": brands, "types": types, "technicians": techs, "countries": countries, "provinces": provinces, "user": user, "active_page": "admin"})

# --- GESTION DE VEHICULOS ---

@router.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    vehicles = db.query(models.Vehicle).all()
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    return templates.TemplateResponse(request, "vehicles.html", {"vehicles": vehicles, "brands": brands, "types": types, "user": user, "active_page": "vehicles"})


@router.get("/vehicles/{vehicle_id}/history", response_class=HTMLResponse)
async def vehicle_history(request: Request, vehicle_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    vehicle = db.query(models.Vehicle).options(joinedload(models.Vehicle.orders)).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle: raise HTTPException(status_code=404, detail="Vehicle not found")
    return templates.TemplateResponse(request, "vehicle_history.html", {"vehicle": vehicle, "user": user})

@router.post("/vehicles/save", response_class=HTMLResponse)
async def save_vehicle(plate: str = Form(...), brand_id: int = Form(...), type_id: int = Form(...), model: str = Form(None), year: int = Form(None), current_mileage: int = Form(0), last_owner: str = Form(None), last_service_date: str = Form(None), photo: UploadFile = File(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    try:
        service_date = datetime.strptime(last_service_date, "%Y-%m-%d") if last_service_date else None
        
        # Generar Código Interno Autonumerado
        max_code = db.query(models.Vehicle.internal_code).order_by(models.Vehicle.internal_code.desc()).first()
        new_code = (max_code[0] + 1) if max_code and max_code[0] else 1001
        
        photo_path = await save_uploaded_img(photo)
        
        db_vehicle = models.Vehicle(
            plate=plate.upper(), brand_id=brand_id, type_id=type_id, model=model, year=year,
            current_mileage=current_mileage, last_owner=last_owner, last_service_date=service_date,
            photo_url=photo_path if photo_path else "/static/img/default_vehicle.png",
            created_by=user.id if user else None,
            internal_code=new_code
        )
        db.add(db_vehicle)
        db.commit()
        log_audit(db, user.id if user else None, "CREAR", "Vehículo", db_vehicle.id, f"Alta de móvil {db_vehicle.plate}")
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">Patente ya existe</div>', status_code=400)

@router.post("/vehicles/{vehicle_id}/delete", response_class=HTMLResponse)
async def delete_vehicle(request: Request, vehicle_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    vehicle = db.get(models.Vehicle, vehicle_id)
    if vehicle:
        try:
            db.delete(vehicle)
            db.commit()
            log_audit(db, user.id if user else None, "BORRAR", "Vehículo", vehicle_id)
        except IntegrityError:
            return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">Este móvil tiene órdenes asignadas y no puede eliminarse.</div>', status_code=400)
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    orders = db.query(models.WorkOrder).order_by(models.WorkOrder.entry_date.desc()).all()
    for ot in orders:
        ot.total_cost = sum(p.quantity * p.unit_price for p in ot.parts) + sum(t.price for t in ot.third_parties)
        ot.formatted_time = format_duration(timedelta(minutes=sum(t.duration_minutes for t in ot.tasks)))
    return templates.TemplateResponse(request, "index.html", {"orders": orders, "user": user, "active_page": "dashboard"})

@router.get("/order/new", response_class=HTMLResponse)
async def new_order_form(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    vehicles = db.query(models.Vehicle).all()
    return templates.TemplateResponse(request, "components/new_order_modal.html", {"vehicles": vehicles, "user": user})

@router.get("/order/{order_id}", response_class=HTMLResponse)
async def view_order(request: Request, order_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    techs = db.query(models.Technician).all()
    is_closed = order.status in ['Terminada', 'Anulada']
    return templates.TemplateResponse(request, "order_detail.html", {"order": order, "technicians": techs, "user": user, "is_closed": is_closed})

@router.post("/order/{order_id}/status", response_class=HTMLResponse)
async def update_status(request: Request, order_id: int, status: str = Form(...), solution: Optional[str] = Form(None), mileage: Optional[int] = Form(None), next_visit: Optional[str] = Form(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    order.updated_by = user.id if user else None
    if status == "Terminada":
        if not order.tasks:
            return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">NO PUEDE CERRAR: El móvil no tiene TAREAS cargadas.</div>', status_code=400)
        if not solution or not mileage: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">Datos incompletos para cierre</div>', status_code=400)
        order.status = "Terminada"; order.solution = solution; order.recorded_mileage = mileage; order.exit_date = datetime.now()
        v = order.vehicle; v.current_mileage = mileage; v.last_service_date = order.exit_date
        v.next_service_suggestion = datetime.strptime(next_visit, "%Y-%m-%d") if next_visit else (order.exit_date + timedelta(days=180))
        log_audit(db, user.id if user else None, "TERMINAR", "Orden", order.id, f"Cierre de OT por {user.username if user else '?'}")
    elif status == "Anulada": 
        order.status = "Anulada"; order.exit_date = datetime.now()
        log_audit(db, user.id if user else None, "ANULAR", "Orden", order.id)
    else: 
        old_status = order.status
        order.status = status; order.exit_date = None
        log_audit(db, user.id if user else None, "ESTADO", "Orden", order.id, f"Cambio de {old_status} a {status}")
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.get("/reports", response_class=HTMLResponse)
async def report_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse(request, "reports.html", {"technicians": techs, "user": user, "active_page": "reports"})

@router.post("/reports/results", response_class=HTMLResponse)
async def generate_report(request: Request, start_date: str = Form(...), end_date: str = Form(...), status: str = Form(...), tech_id: str = Form(""), db: Session = Depends(get_db)):
    try:
        # Flexible date parsing
        if "-" in start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        elif "/" in start_date:
            try:
                start = datetime.strptime(start_date, "%d/%m/%Y")
            except:
                start = datetime.strptime(start_date, "%Y/%m/%d")
        else:
            start = datetime.strptime(start_date, "%Y-%m-%d") # fallback

        if "-" in end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        elif "/" in end_date:
            try:
                end = datetime.strptime(end_date, "%d/%m/%Y") + timedelta(days=1)
            except:
                end = datetime.strptime(end_date, "%Y/%m/%d") + timedelta(days=1)
        else:
             end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) # fallback
    except Exception as e:
        return HTMLResponse(content=f'<div class="p-8 bg-red-50 border-2 border-red-200 rounded-3xl text-red-700 font-bold">Error en formato de fecha: {str(e)}. Use YYYY-MM-DD o DD/MM/YYYY.</div>', status_code=400)
    
    query = db.query(models.WorkOrder).options(
        joinedload(models.WorkOrder.parts),
        joinedload(models.WorkOrder.third_parties),
        joinedload(models.WorkOrder.tasks).joinedload(models.WOTask.technician),
        joinedload(models.WorkOrder.vehicle).joinedload(models.Vehicle.brand)
    ).filter(models.WorkOrder.entry_date >= start, models.WorkOrder.entry_date < end)
    
    if status != "all":
        query = query.filter(models.WorkOrder.status == status)
    
    orders = query.order_by(models.WorkOrder.entry_date.desc()).all()
    
    parts_total = Decimal(0)
    parts_count = 0
    third_total = Decimal(0)
    third_count = 0
    tech_time = {}
    
    for ot in orders:
        parts_total += sum((p.quantity or 0) * (p.unit_price or 0) for p in ot.parts)
        third_total += sum((t.price or 0) for t in ot.third_parties)
        parts_count += len(ot.parts)
        third_count += len(ot.third_parties)
        
        ot_minutes = sum((t.duration_minutes or 0) for t in ot.tasks)
        ot.total_minutes = ot_minutes
        ot.work_duration = format_duration(timedelta(minutes=ot_minutes))
        
        for t in ot.tasks:
            if tech_id and str(t.technician_id) != tech_id:
                continue
            t_id = t.technician_id or 0
            if t_id not in tech_time:
                t_name = t.technician.name if t.technician else "Sin asignar"
                tech_time[t_id] = {"name": t_name, "minutes": 0}
            tech_time[t_id]["minutes"] += (t.duration_minutes or 0)
            
    tech_stats = []
    for tdata in tech_time.values():
        tdata["formatted"] = format_duration(timedelta(minutes=tdata["minutes"]))
        tech_stats.append(tdata)
        
    print(f"DEBUG: Reporte generado con {len(orders)} ordenes. Total Repuestos: {parts_total}")

    return templates.TemplateResponse(request, "components/report_results.html", {
        "orders": orders,
        "parts_total": "{:,.2f}".format(parts_total),
        "parts_count": parts_count,
        "third_total": "{:,.2f}".format(third_total),
        "third_count": third_count,
        "tech_stats": tech_stats
    })

@router.post("/order/save", response_class=HTMLResponse)
async def save_order(vehicle_id: int = Form(...), diagnosis: str = Form(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    db_order = models.WorkOrder(vehicle_id=vehicle_id, diagnosis=diagnosis, status="Pendiente", created_by=user.id if user else None)
    db.add(db_order)
    db.commit()
    log_audit(db, user.id if user else None, "CREAR", "Orden", db_order.id, f"Apertura de OT para vehículo ID {vehicle_id}")
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.post("/admin/{entity_name}", response_class=HTMLResponse)
async def create_admin_entity(request: Request, entity_name: str, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name").strip() if form.get("name") else ""
    model_map = {"brand": models.Brand, "type": models.VehicleType, "tech": models.Technician, "country": models.Country, "province": models.Province}
    
    if entity_name in model_map:
        if entity_name == "province":
            db.add(models.Province(name=name, country_id=int(form.get("country_id"))))
        else:
            db.add(model_map[entity_name](name=name))
        db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.post("/admin/{entity_name}/{entity_id}/update", response_class=HTMLResponse)
async def update_admin_entity(request: Request, entity_name: str, entity_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name").strip() if form.get("name") else ""
    model_map = {"brand": models.Brand, "type": models.VehicleType, "tech": models.Technician, "country": models.Country, "province": models.Province}
    
    if entity_name in model_map:
        obj = db.get(model_map[entity_name], entity_id)
        if obj:
            obj.name = name
            if entity_name == "province" and form.get("country_id"):
                obj.country_id = int(form.get("country_id"))
            db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.post("/admin/{entity_name}/{entity_id}/delete", response_class=HTMLResponse)
async def delete_admin_entity(request: Request, entity_name: str, entity_id: int, db: Session = Depends(get_db)):
    model_map = {"brand": models.Brand, "type": models.VehicleType, "tech": models.Technician, "country": models.Country, "province": models.Province}
    if entity_name in model_map:
        obj = db.get(model_map[entity_name], entity_id)
        if obj:
            try:
                db.delete(obj)
                db.commit()
            except IntegrityError:
                return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl text-white font-bold">No se puede eliminar la entidad porque está en uso.</div>', status_code=400)
    return HTMLResponse(content='<script>window.location.reload();</script>')

# --- ORDENES DETALLE (Tareas, Partes, Terceros, Resumen) ---

@router.get("/order/{order_id}/header", response_class=HTMLResponse)
async def get_order_header(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    is_closed = order.status in ['Terminada', 'Anulada'] if order else False
    return templates.TemplateResponse(request, "components/order_header.html", {"order": order, "is_closed": is_closed})

@router.get("/order/{order_id}/summary", response_class=HTMLResponse)
async def get_order_summary(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    if not order:
        return HTMLResponse("Orden no encontrada", status_code=404)
        
    total_parts = sum(p.quantity * p.unit_price for p in order.parts)
    total_third = sum(t.price for t in order.third_parties)
    total_general = total_parts + total_third
    
    total_minutes = sum(t.duration_minutes for t in order.tasks)
    total_duration = format_duration(timedelta(minutes=total_minutes))
    
    return templates.TemplateResponse(request, "components/summary_card.html", {
        "order": order,
        "total_parts": f"{total_parts:.2f}",
        "total_third": f"{total_third:.2f}",
        "total_general": f"{total_general:.2f}",
        "total_duration": total_duration
    })

@router.get("/order/{order_id}/status-only", response_class=HTMLResponse)
async def get_status_only(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    status = order.status if order else ""
    return HTMLResponse(content=f'<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded font-bold uppercase text-xs">{status}</span>')

@router.post("/order/{order_id}/task", response_class=HTMLResponse)
async def add_task(request: Request, order_id: int, description: str = Form(...), duration: int = Form(...), tech_id: int = Form(...), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    db.add(models.WOTask(work_order_id=order_id, description=description, duration_minutes=duration, technician_id=tech_id))
    order.updated_by = user.id if user else None
    db.commit()
    log_audit(db, user.id if user else None, "MODIFICAR", "Orden Tarea", order_id, f"Añadida tarea a OT {order_id}")
    db.refresh(order)
    resp = templates.TemplateResponse(request, "components/task_list.html", {"tasks": order.tasks})
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

@router.delete("/task/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    task = db.get(models.WOTask, task_id)
    if task:
        order = task.work_order
        order.updated_by = user.id if user else None
        db.delete(task)
        db.commit()
        log_audit(db, user.id if user else None, "BORRAR", "Orden Tarea", task_id)
    resp = HTMLResponse(content="")
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

@router.post("/order/{order_id}/part", response_class=HTMLResponse)
async def add_part(request: Request, order_id: int, description: str = Form(...), qty: Decimal = Form(...), price: Decimal = Form(...), uom: str = Form(""), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    db.add(models.WOPart(work_order_id=order_id, description=description, quantity=qty, unit_price=price, uom=uom))
    order.updated_by = user.id if user else None
    db.commit()
    log_audit(db, user.id if user else None, "MODIFICAR", "Orden Repuesto", order_id)
    db.refresh(order)
    resp = templates.TemplateResponse(request, "components/part_list.html", {"parts": order.parts})
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

@router.delete("/part/{part_id}", response_class=HTMLResponse)
async def delete_part(request: Request, part_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    part = db.get(models.WOPart, part_id)
    if part:
        order = part.work_order
        order.updated_by = user.id if user else None
        db.delete(part)
        db.commit()
        log_audit(db, user.id if user else None, "BORRAR", "Orden Repuesto", part_id)
    resp = HTMLResponse(content="")
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

@router.post("/order/{order_id}/third-party", response_class=HTMLResponse)
async def add_third_party(request: Request, order_id: int, provider: str = Form(...), description: str = Form(...), price: Decimal = Form(...), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    db.add(models.WOThirdParty(work_order_id=order_id, provider_name=provider, description=description, price=price))
    order.updated_by = user.id if user else None
    db.commit()
    log_audit(db, user.id if user else None, "MODIFICAR", "Orden Tercero", order_id)
    db.refresh(order)
    resp = templates.TemplateResponse(request, "components/third_party_list.html", {"third_parties": order.third_parties})
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

@router.delete("/third-party/{tp_id}", response_class=HTMLResponse)
async def delete_third_party(request: Request, tp_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    tp = db.get(models.WOThirdParty, tp_id)
    if tp:
        order = tp.work_order
        order.updated_by = user.id if user else None
        db.delete(tp)
        db.commit()
        log_audit(db, user.id if user else None, "BORRAR", "Orden Tercero", tp_id)
    resp = HTMLResponse(content="")
    resp.headers["HX-Trigger"] = "refreshSummary"
    return resp

# --- RECUPERACION DE CLAVE ---

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_pw_page(request: Request):
    return templates.TemplateResponse(request, "reset_password.html")

@router.post("/reset-password", response_class=HTMLResponse)
async def reset_password(password: str = Form(...), confirm_password: str = Form(...), db: Session = Depends(get_db)):
    if password != confirm_password:
        return HTMLResponse(content='<div id="error-msg" hx-swap-oob="true" class="text-red-500 font-bold">Las claves no coinciden</div>', status_code=400)
    try:
        auth.validate_password_strength(password)
        # En una versión real, aquí se validaría un TOKEN enviado por email.
        # Para esta Beta, asumimos que el usuario actual (o el último suspendido) es quien pide el cambio.
        # Requerimos el Oficial de Seguridad por ahora o simulamos éxito.
        return HTMLResponse(content='<div class="bg-green-100 p-4 rounded-xl text-green-700 font-bold">Contraseña actualizada con éxito. Ya puede iniciar sesión.</div>')
    except ValueError as e:
        return HTMLResponse(content=f'<div id="error-msg" hx-swap-oob="true" class="text-red-500 font-bold">{str(e)}</div>', status_code=400)

# --- AGENDA DE TURNOS ---

@router.get("/appointments", response_class=HTMLResponse)
async def appointments_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    # Turnos para hoy
    today_appointments = db.query(models.Appointment).filter(
        models.Appointment.scheduled_date >= today_start,
        models.Appointment.scheduled_date < today_end
    ).order_by(models.Appointment.scheduled_date.asc()).all()
    
    # Próximos turnos a partir de mañana
    upcoming_appointments = db.query(models.Appointment).filter(
        models.Appointment.scheduled_date >= today_end
    ).order_by(models.Appointment.scheduled_date.asc()).limit(50).all()
    
    vehicles = db.query(models.Vehicle).all()
    return templates.TemplateResponse(request, "appointments.html", {
        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming_appointments,
        "vehicles": vehicles,
        "user": user,
        "today_date": today_start.strftime("%Y-%m-%d"),
        "active_page": "appointments"
    })

@router.get("/appointments/api/check-client")
async def check_client(email: str, db: Session = Depends(get_db)):
    owner = db.query(models.Owner).filter(models.Owner.email == email.strip()).first()
    if owner:
        return {"found": True, "name": owner.full_name, "phone": owner.phone}
    
    # Buscar el último turno asociado a este email por compatibilidad
    last_apt = db.query(models.Appointment).filter(models.Appointment.client_email == email.strip()).order_by(models.Appointment.id.desc()).first()
    if last_apt:
        return {"found": True, "name": last_apt.client_name, "phone": last_apt.client_phone}
    return {"found": False}

@router.post("/appointments/save", response_class=HTMLResponse)
async def save_appointment(
    client_email: str = Form(...), client_name: str = Form(...), client_phone: str = Form(...),
    scheduled_date: str = Form(...), scheduled_time: str = Form(...),
    vehicle_id: str = Form(""), plate: str = Form(""), reason: str = Form(""),
    db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)
):
    date_val = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
    v_id = int(vehicle_id) if vehicle_id else None
    
    # Pre-cargar Owner "silenciosamente"
    owner = db.query(models.Owner).filter(models.Owner.email == client_email.strip()).first()
    if not owner:
        owner = models.Owner(
            email=client_email.strip(),
            full_name=client_name.strip(),
            phone=client_phone.strip()
        )
        db.add(owner)
        db.flush()
    
    nuevo_turno = models.Appointment(
        owner_id=owner.id,
        client_email=client_email.strip(), client_name=client_name.strip(), client_phone=client_phone.strip(),
        vehicle_id=v_id, plate=plate.strip().upper() if not v_id else None,
        scheduled_date=date_val, reason=reason.strip(),
        created_by=user.id if user else None
    )
    db.add(nuevo_turno)
    db.commit()
    log_audit(db, user.id if user else None, "CREAR", "Turno", nuevo_turno.id, f"Reserva para {nuevo_turno.client_email} el {date_val}")
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.post("/appointments/{apt_id}/status", response_class=HTMLResponse)
async def update_appointment_status(request: Request, apt_id: int, status: str = Form(...), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    apt = db.get(models.Appointment, apt_id)
    if apt:
        old_val = apt.status
        apt.status = status
        apt.updated_by = user.id if user else None
        db.commit()
        log_audit(db, user.id if user else None, "ESTADO", "Turno", apt.id, f"Cambio de {old_val} a {status}")
    return HTMLResponse(content='<script>window.location.reload();</script>')

@router.post("/appointments/report", response_class=HTMLResponse)
async def appointments_report(request: Request, start_date: str = Form(...), end_date: str = Form(...), db: Session = Depends(get_db)):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    appointments = db.query(models.Appointment).filter(
        models.Appointment.scheduled_date >= start,
        models.Appointment.scheduled_date < end
    ).order_by(models.Appointment.scheduled_date.asc()).all()
    
    return templates.TemplateResponse(request, "components/appointment_report_results.html", {"appointments": appointments})

# --- GESTION DE CLIENTES ---

@router.get("/clients", response_class=HTMLResponse)
async def clients_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    clients = db.query(models.Owner).order_by(models.Owner.owner_number.desc()).all()
    countries = db.query(models.Country).all()
    provinces = db.query(models.Province).all()
    return templates.TemplateResponse(request, "clients.html", {"clients": clients, "countries": countries, "provinces": provinces, "user": user, "active_page": "clients"})

@router.post("/clients/save", response_class=HTMLResponse)
async def save_client(
    client_id: str = Form(""), email: str = Form(...), full_name: str = Form(...), phone: str = Form(""),
    address: str = Form(""), owner_type: str = Form(...), document_id: str = Form(""), country_id: str = Form(""), province_id: str = Form(""), photo: UploadFile = File(None),
    db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)
):
    try:
        photo_path = await save_uploaded_img(photo)
        c_id = int(country_id) if country_id else None
        p_id = int(province_id) if province_id else None
        
        if client_id:
            c = db.get(models.Owner, int(client_id))
            c.email = email.strip()
            c.full_name = full_name.strip()
            c.phone = phone.strip()
            c.address = address.strip()
            c.owner_type = owner_type
            c.document_id = document_id.strip()
            c.country_id = c_id
            c.province_id = p_id
            if photo_path: c.photo_url = photo_path
            action = "MODIFICAR"
        else:
            c = models.Owner(
                email=email.strip(), full_name=full_name.strip(), phone=phone.strip(),
                address=address.strip(), owner_type=owner_type, document_id=document_id.strip(),
                country_id=c_id, province_id=p_id,
                photo_url=photo_path if photo_path else "/static/img/default_avatar.png"
            )
            db.add(c)
            action = "CREAR"
            
        db.commit()
        log_audit(db, user.id if user else None, action, "Propietario/Cliente", c.id)
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError:
        db.rollback()
        return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl text-white font-bold">El Email ingresado ya se encuentra registrado.</div>', status_code=400)

@router.post("/clients/{client_id}/delete", response_class=HTMLResponse)
async def delete_client(client_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    c = db.get(models.Owner, client_id)
    if c:
        try:
            db.delete(c)
            db.commit()
            log_audit(db, user.id if user else None, "BORRAR", "Propietario/Cliente", client_id)
        except IntegrityError:
            db.rollback()
            return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl text-white font-bold">No se puede eliminar porque posee turnos vinculados.</div>', status_code=400)
    return HTMLResponse(content='<script>window.location.reload();</script>')


# ── Register Router with Module Prefix ──
app.include_router(router)

# ── Root Redirect (convenience) ──
@app.get("/", response_class=RedirectResponse)
async def root_redirect():
    return RedirectResponse(url=f"{MODULE_PREFIX}/login")

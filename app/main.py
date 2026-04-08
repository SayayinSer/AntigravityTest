from fastapi import FastAPI, Depends, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import traceback

from . import models, schemas, database, auth

app = FastAPI(title="Work Order Management")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

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

# --- SEGURIDAD (LOGIN / LOGOUT / ADMIN) ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return HTMLResponse(content='<div id="error-msg" class="text-red-500 font-bold text-sm bg-red-50 p-3 rounded-lg border border-red-100 mb-4">Credenciales inválidas</div>', status_code=401)
    
    access_token = auth.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

@app.get("/admin/security", response_class=HTMLResponse)
async def security_admin(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    users = db.query(models.User).all()
    roles = db.query(models.Role).all()
    return templates.TemplateResponse("security_admin.html", {"request": request, "users": users, "roles": roles, "current_user": current_user})

@app.post("/admin/security/user", response_class=HTMLResponse)
async def create_user(username: str = Form(...), full_name: str = Form(...), password: str = Form(...), role_id: int = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_role(["OficialSeguridad"]))):
    try:
        hashed_pw = auth.get_password_hash(password)
        new_user = models.User(username=username, full_name=full_name, hashed_password=hashed_pw)
        role = db.get(models.Role, role_id)
        if role: new_user.roles.append(role)
        db.add(new_user)
        db.commit()
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div class="bg-red-500 text-white p-2">Usuario ya existe</div>', status_code=400)

# --- ADMINISTRACION ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("admin.html", {"request": request, "brands": brands, "types": types, "technicians": techs, "user": user})

# --- GESTION DE VEHICULOS ---

@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    vehicles = db.query(models.Vehicle).all()
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    return templates.TemplateResponse("vehicles.html", {"request": request, "vehicles": vehicles, "brands": brands, "types": types, "user": user})

@app.post("/vehicles/save", response_class=HTMLResponse)
async def save_vehicle(plate: str = Form(...), brand_id: int = Form(...), type_id: int = Form(...), model: str = Form(None), year: int = Form(None), current_mileage: int = Form(0), last_owner: str = Form(None), last_service_date: str = Form(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    try:
        service_date = datetime.strptime(last_service_date, "%Y-%m-%d") if last_service_date else None
        db_vehicle = models.Vehicle(plate=plate.upper(), brand_id=brand_id, type_id=type_id, model=model, year=year, current_mileage=current_mileage, last_owner=last_owner, last_service_date=service_date, created_by=user.id if user else None)
        db.add(db_vehicle)
        db.commit()
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl">Patente ya existe</div>', status_code=400)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    orders = db.query(models.WorkOrder).order_by(models.WorkOrder.entry_date.desc()).all()
    for ot in orders:
        ot.total_cost = sum(p.quantity * p.unit_price for p in ot.parts) + sum(t.price for t in ot.third_parties)
        ot.formatted_time = format_duration(timedelta(minutes=sum(t.duration_minutes for t in ot.tasks)))
    return templates.TemplateResponse("index.html", {"request": request, "orders": orders, "user": user})

@app.get("/order/{order_id}", response_class=HTMLResponse)
async def view_order(request: Request, order_id: int, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("order_detail.html", {"request": request, "order": order, "technicians": techs, "user": user})

# ... resto de rutas (simplificadas para brevedad en esta actualización crítica) ...
@app.post("/order/{order_id}/status", response_class=HTMLResponse)
async def update_status(request: Request, order_id: int, status: str = Form(...), solution: Optional[str] = Form(None), mileage: Optional[int] = Form(None), next_visit: Optional[str] = Form(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    order = db.get(models.WorkOrder, order_id)
    order.updated_by = user.id if user else None
    if status == "Terminada":
        if not solution or not mileage: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl">Datos incompletos</div>', status_code=400)
        order.status = "Terminada"; order.solution = solution; order.recorded_mileage = mileage; order.exit_date = datetime.now()
        v = order.vehicle; v.current_mileage = mileage; v.last_service_date = order.exit_date
        v.next_service_suggestion = datetime.strptime(next_visit, "%Y-%m-%d") if next_visit else (order.exit_date + timedelta(days=180))
    elif status == "Anulada": order.status = "Anulada"; order.exit_date = datetime.now()
    else: order.status = status; order.exit_date = None
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

# Endpoints CRUD (se mantienen igual, solo pasando 'user' si es necesario para UI)
@app.get("/reports", response_class=HTMLResponse)
async def report_page(request: Request, db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("reports.html", {"request": request, "technicians": techs, "user": user})

@app.post("/order/save", response_class=HTMLResponse)
async def save_order(vehicle_id: int = Form(...), diagnosis: str = Form(None), db: Session = Depends(get_db), user: Optional[models.User] = Depends(auth.get_current_user)):
    db_order = models.WorkOrder(vehicle_id=vehicle_id, diagnosis=diagnosis, status="Pendiente", created_by=user.id if user else None)
    db.add(db_order)
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@app.post("/admin/brand", response_class=HTMLResponse)
async def create_brand_route(name: str = Form(...), db: Session = Depends(get_db)):
    db.add(models.Brand(name=name.strip()))
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

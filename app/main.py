from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import traceback

from . import models, schemas, database

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

# --- ADMINISTRACION ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("admin.html", {"request": request, "brands": brands, "types": types, "technicians": techs})

@app.post("/admin/brand", response_class=HTMLResponse)
async def create_brand(name: str = Form(...), db: Session = Depends(get_db)):
    try:
        brand = models.Brand(name=name.strip())
        db.add(brand)
        db.commit()
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-amber-600 p-4 rounded-xl">Ya existe</div>', status_code=400)

# --- GESTION DE VEHICULOS (MÓVILES) ---

@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request, db: Session = Depends(get_db)):
    vehicles = db.query(models.Vehicle).all()
    brands = db.query(models.Brand).all()
    types = db.query(models.VehicleType).all()
    return templates.TemplateResponse("vehicles.html", {"request": request, "vehicles": vehicles, "brands": brands, "types": types})

@app.post("/vehicles/save", response_class=HTMLResponse)
async def save_vehicle(
    plate: str = Form(...), brand_id: int = Form(...), type_id: int = Form(...), 
    model: str = Form(None), year: int = Form(None),
    current_mileage: int = Form(0), last_owner: str = Form(None),
    last_service_date: str = Form(None), db: Session = Depends(get_db)
):
    try:
        service_date = datetime.strptime(last_service_date, "%Y-%m-%d") if last_service_date else None
        db_vehicle = models.Vehicle(
            plate=plate.upper(), brand_id=brand_id, type_id=type_id, model=model, year=year,
            current_mileage=current_mileage, last_owner=last_owner, last_service_date=service_date
        )
        db.add(db_vehicle)
        db.commit()
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl">Patente ya existe</div>', status_code=400)

@app.get("/vehicles/{id}/history", response_class=HTMLResponse)
async def vehicle_history(id: int, request: Request, db: Session = Depends(get_db)):
    vehicle = db.get(models.Vehicle, id)
    if not vehicle: raise HTTPException(status_code=404)
    return templates.TemplateResponse("vehicle_history.html", {"request": request, "vehicle": vehicle})

@app.post("/vehicles/{id}/delete", response_class=HTMLResponse)
async def delete_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = db.get(models.Vehicle, id)
    if vehicle:
        try:
            db.delete(vehicle)
            db.commit()
            return HTMLResponse(content='<script>window.location.reload();</script>')
        except IntegrityError: return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 p-4 rounded-xl">Vehículo con órdenes asociadas</div>', status_code=400)
    return HTMLResponse(status_code=404)

# --- DASHBOARD Y ORDENES (LOGICA DE CIERRE) ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.WorkOrder).order_by(models.WorkOrder.entry_date.desc()).all()
    for ot in orders:
        ot.total_cost = sum(p.quantity * p.unit_price for p in ot.parts) + sum(t.price for t in ot.third_parties)
        ot.formatted_time = format_duration(timedelta(minutes=sum(t.duration_minutes for t in ot.tasks)))
    return templates.TemplateResponse("index.html", {"request": request, "orders": orders})

@app.get("/order/new", response_class=HTMLResponse)
async def new_order_form(request: Request, db: Session = Depends(get_db)):
    vehicles = db.query(models.Vehicle).all()
    return templates.TemplateResponse("components/order_form.html", {"request": request, "vehicles": vehicles})

@app.post("/order/save", response_class=HTMLResponse)
async def save_order(vehicle_id: int = Form(...), diagnosis: str = Form(None), db: Session = Depends(get_db)):
    db_order = models.WorkOrder(vehicle_id=vehicle_id, diagnosis=diagnosis, status="Pendiente")
    db.add(db_order)
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@app.get("/order/{order_id}", response_class=HTMLResponse)
async def view_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    if not order: raise HTTPException(status_code=404)
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("order_detail.html", {"request": request, "order": order, "technicians": techs})

@app.post("/order/{order_id}/status", response_class=HTMLResponse)
async def update_status(
    request: Request, order_id: int, status: str = Form(...),
    solution: Optional[str] = Form(None), mileage: Optional[int] = Form(None),
    next_visit: Optional[str] = Form(None), db: Session = Depends(get_db)
):
    order = db.get(models.WorkOrder, order_id)
    if status == "Terminada":
        if not solution or not mileage:
            return HTMLResponse(content='<div id="notification-area" hx-swap-oob="true" class="bg-red-600 text-white p-4 rounded-xl">Datos de cierre incompletos (Solución/KM)</div>', status_code=400)
        
        # Actualizar Orden
        order.status = "Terminada"
        order.solution = solution
        order.recorded_mileage = mileage
        order.exit_date = datetime.now()
        
        # Actualizar Ficha del Vehículo
        vehicle = order.vehicle
        vehicle.current_mileage = mileage
        vehicle.last_service_date = order.exit_date
        if next_visit:
            vehicle.next_service_suggestion = datetime.strptime(next_visit, "%Y-%m-%d")
        else:
            vehicle.next_service_suggestion = order.exit_date + timedelta(days=180) # +6 meses sugerencia
            
    elif status == "Anulada":
        order.status = "Anulada"
        order.exit_date = datetime.now()
    else:
        order.status = status
        order.exit_date = None
        
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

@app.get("/order/{order_id}/summary", response_class=HTMLResponse)
async def get_order_summary(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    p_total = sum(p.quantity * p.unit_price for p in order.parts)
    t_total = sum(t.price for t in order.third_parties)
    total_mins = sum(t.duration_minutes for t in order.tasks)
    return templates.TemplateResponse("components/summary_card.html", {
        "request": request, "order": order, "total_parts": p_total, "total_third": t_total, 
        "total_general": p_total + t_total, "total_duration": format_duration(timedelta(minutes=total_mins))
    })

# --- REPORTES Y AUXILIARES ---

@app.get("/reports", response_class=HTMLResponse)
async def report_page(request: Request, db: Session = Depends(get_db)):
    techs = db.query(models.Technician).all()
    return templates.TemplateResponse("reports.html", {"request": request, "technicians": techs})

@app.post("/reports/results", response_class=HTMLResponse)
async def report_results(request: Request, start_date: str = Form(...), end_date: str = Form(...), status: str = Form("all"), tech_id: Optional[str] = Form(None), db: Session = Depends(get_db)):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d"), datetime.max.time())
    query = db.query(models.WorkOrder).filter(models.WorkOrder.entry_date >= start, models.WorkOrder.entry_date <= end)
    if status != "all": query = query.filter(models.WorkOrder.status == status)
    orders = query.all()
    
    tech_stats = []
    t_query = db.query(models.Technician)
    if tech_id and tech_id.strip(): t_query = t_query.filter(models.Technician.id == int(tech_id))
    for t in t_query.all():
        total_min = sum(task.duration_minutes for task in t.tasks if task.work_order.entry_date >= start and task.work_order.entry_date <= end)
        tech_stats.append({"name": t.name, "minutes": total_min, "formatted": format_duration(timedelta(minutes=total_min))})

    return templates.TemplateResponse("components/report_results.html", {
        "request": request, "orders": orders, "tech_stats": tech_stats,
        "parts_total": sum(p.quantity * p.unit_price for p in db.query(models.WOPart).join(models.WorkOrder).filter(models.WorkOrder.entry_date >= start, models.WorkOrder.entry_date <= end).all()),
        "third_total": sum(t.price for t in db.query(models.WOThirdParty).join(models.WorkOrder).filter(models.WorkOrder.entry_date >= start, models.WorkOrder.entry_date <= end).all())
    })

# Endpoints CRUD técnicos y tipos
@app.post("/admin/type", response_class=HTMLResponse)
async def create_type(name: str = Form(...), db: Session = Depends(get_db)):
    try:
        vtype = models.VehicleType(name=name.strip())
        db.add(vtype)
        db.commit()
        return HTMLResponse(content='<script>window.location.reload();</script>')
    except IntegrityError: return HTMLResponse(content='<div class="bg-red-500 p-2 text-white">Error</div>', status_code=400)

@app.post("/admin/tech", response_class=HTMLResponse)
async def create_tech(name: str = Form(...), db: Session = Depends(get_db)):
    db.add(models.Technician(name=name.strip()))
    db.commit()
    return HTMLResponse(content='<script>window.location.reload();</script>')

# Auxiliares de Orden
@app.post("/order/{order_id}/task", response_class=HTMLResponse)
async def add_task(request: Request, order_id: int, description: str = Form(...), duration: int = Form(...), tech_id: int = Form(...), db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    if order.status == "Pendiente": order.status = "En Ejecución"
    db.add(models.WOTask(work_order_id=order_id, description=description, duration_minutes=duration, technician_id=tech_id))
    db.commit()
    return templates.TemplateResponse("components/task_list.html", {"request": request, "tasks": order.tasks}, headers={"HX-Trigger": "refreshSummary, refresh-status"})

@app.delete("/task/{task_id}", response_class=HTMLResponse)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.WOTask, task_id)
    if task:
        db.delete(task)
        db.commit()
    return HTMLResponse(content="", headers={"HX-Trigger": "refreshSummary"})

@app.post("/order/{order_id}/part", response_class=HTMLResponse)
async def add_part(request: Request, order_id: int, description: str = Form(...), qty: Decimal = Form(...), price: Decimal = Form(...), uom: str = Form(None), db: Session = Depends(get_db)):
    db.add(models.WOPart(work_order_id=order_id, description=description, quantity=qty, unit_price=price, uom=uom))
    db.commit()
    return templates.TemplateResponse("components/part_list.html", {"request": request, "parts": db.get(models.WorkOrder, order_id).parts}, headers={"HX-Trigger": "refreshSummary"})

@app.delete("/part/{part_id}", response_class=HTMLResponse)
async def delete_part(part_id: int, db: Session = Depends(get_db)):
    part = db.get(models.WOPart, part_id)
    if part:
        db.delete(part)
        db.commit()
    return HTMLResponse(content="", headers={"HX-Trigger": "refreshSummary"})

@app.post("/order/{order_id}/third-party", response_class=HTMLResponse)
async def add_third_party(request: Request, order_id: int, provider: str = Form(...), description: str = Form(...), price: Decimal = Form(...), db: Session = Depends(get_db)):
    db.add(models.WOThirdParty(work_order_id=order_id, provider_name=provider, description=description, price=price))
    db.commit()
    return templates.TemplateResponse("components/third_party_list.html", {"request": request, "third_parties": db.get(models.WorkOrder, order_id).third_parties}, headers={"HX-Trigger": "refreshSummary"})

@app.delete("/third-party/{id}", response_class=HTMLResponse)
async def delete_third_party(id: int, db: Session = Depends(get_db)):
    third = db.get(models.WOThirdParty, id)
    if third:
        db.delete(third)
        db.commit()
    return HTMLResponse(content="", headers={"HX-Trigger": "refreshSummary"})

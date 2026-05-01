from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Numeric, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Tabla intermedia para Roles de Usuario (Muchos a Muchos)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    status = Column(Enum('Activo', 'Suspendido', name='user_status_enum', native_enum=False), default='Activo')
    failed_attempts = Column(Integer, default=0)
    is_active = Column(Integer, default=1) # 1=Active, 0=Inactive
    
    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255))
    
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    provinces = relationship("Province", back_populates="country")

class Province(Base):
    __tablename__ = "provinces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"))
    country = relationship("Country", back_populates="provinces")

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    vehicles = relationship("Vehicle", back_populates="brand")

class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    vehicles = relationship("Vehicle", back_populates="vehicle_type")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    internal_code = Column(Integer, unique=True, index=True, autoincrement=True)
    plate = Column(String(20), unique=True, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="RESTRICT"))
    type_id = Column(Integer, ForeignKey("vehicle_types.id", ondelete="RESTRICT"))
    model = Column(String(100))
    year = Column(Integer)
    current_mileage = Column(Integer, default=0)
    last_owner = Column(String(150))
    last_service_date = Column(DateTime)
    next_service_suggestion = Column(DateTime)
    photo_url = Column(String(255), default="/static/img/default_vehicle.png")
    owner_id = Column(Integer, ForeignKey("owners.id", ondelete="SET NULL"))

    # Auditoria
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    brand = relationship("Brand", back_populates="vehicles")
    vehicle_type = relationship("VehicleType", back_populates="vehicles")
    owner = relationship("Owner", back_populates="vehicles")
    orders = relationship("WorkOrder", back_populates="vehicle")

class Technician(Base):
    __tablename__ = "technicians"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tasks = relationship("WOTask", back_populates="technician")

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="RESTRICT"))
    status = Column(Enum('Pendiente', 'En Ejecución', 'Terminada', 'Anulada', name='order_status_enum', native_enum=False), default='Pendiente')
    diagnosis = Column(Text)
    solution = Column(Text)
    recommendation = Column(Text)
    entry_date = Column(DateTime, server_default=func.now())
    exit_date = Column(DateTime)
    recorded_mileage = Column(Integer)

    # Auditoria
    updated_at = Column(DateTime, onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    vehicle = relationship("Vehicle", back_populates="orders")
    tasks = relationship("WOTask", back_populates="work_order", cascade="all, delete-orphan")
    parts = relationship("WOPart", back_populates="work_order", cascade="all, delete-orphan")
    third_parties = relationship("WOThirdParty", back_populates="work_order", cascade="all, delete-orphan")

    @property
    def total_parts_price(self):
        return sum((p.quantity or 0) * (p.unit_price or 0) for p in self.parts)

    @property
    def total_third_party_price(self):
        return sum((t.price or 0) for t in self.third_parties)

class WOTask(Base):
    __tablename__ = "wo_tasks"
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"))
    description = Column(Text)
    duration_minutes = Column(Integer)
    technician_id = Column(Integer, ForeignKey("technicians.id", ondelete="RESTRICT"))

    work_order = relationship("WorkOrder", back_populates="tasks")
    technician = relationship("Technician", back_populates="tasks")

class WOPart(Base):
    __tablename__ = "wo_parts"
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"))
    description = Column(String(255))
    quantity = Column(Numeric(10, 2))
    unit_price = Column(Numeric(12, 2))
    uom = Column(String(20))

    work_order = relationship("WorkOrder", back_populates="parts")
    
    @property
    def total_price(self):
        return (self.quantity or 0) * (self.unit_price or 0)

class WOThirdParty(Base):
    __tablename__ = "wo_third_parties"
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"))
    provider_name = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(12, 2))

    work_order = relationship("WorkOrder", back_populates="third_parties")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(50)) # CREAR, MODIFICAR, BORRAR
    entity_name = Column(String(50)) # Vehículo, Orden
    entity_id = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
    details = Column(Text) # JSON o descripción de cambios

    user = relationship("User")

class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    owner_number = Column(Integer, unique=True, index=True, autoincrement=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(50))
    address = Column(String(255))
    owner_type = Column(Enum('Persona Física', 'Persona Jurídica', name='owner_type_enum', native_enum=False), default='Persona Física')
    document_id = Column(String(50)) # DNI o CUIT
    photo_url = Column(String(255), default="/static/img/default_avatar.png")
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="SET NULL"), nullable=True)
    province_id = Column(Integer, ForeignKey("provinces.id", ondelete="SET NULL"), nullable=True)
    
    country = relationship("Country")
    province = relationship("Province")
    vehicles = relationship("Vehicle", back_populates="owner")
    
    # Auditoria
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id", ondelete="RESTRICT"), nullable=True) # Ligado al Propietario "Silenciosamente"
    client_email = Column(String(150), index=True) # Histórico
    client_name = Column(String(150), nullable=False) # Histórico
    client_phone = Column(String(50)) # Histórico
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)
    plate = Column(String(20))
    scheduled_date = Column(DateTime, nullable=False, index=True)
    reason = Column(Text)
    status = Column(Enum('Pendiente', 'Confirmado', 'Atendido', 'Cancelado', name='appointment_status_enum', native_enum=False), default='Pendiente')
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    vehicle = relationship("Vehicle")
    owner = relationship("Owner")


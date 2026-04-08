from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Base Schemas
class BrandBase(BaseModel):
    name: str

class Brand(BrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class VehicleTypeBase(BaseModel):
    name: str

class VehicleType(VehicleTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TechnicianBase(BaseModel):
    name: str

class Technician(TechnicianBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Vehicle Schemas
class VehicleBase(BaseModel):
    internal_code: str
    plate: str = Field(..., max_length=20)
    brand_id: int
    type_id: int
    model: Optional[str] = None
    year: Optional[int] = None

class Vehicle(VehicleBase):
    id: int
    brand: Brand
    vehicle_type: VehicleType
    model_config = ConfigDict(from_attributes=True)

# Work Order Sub-items
class WOTaskBase(BaseModel):
    description: str
    duration_minutes: int
    technician_id: int

class WOTask(WOTaskBase):
    id: int
    technician: Technician
    model_config = ConfigDict(from_attributes=True)

class WOPartBase(BaseModel):
    description: str
    quantity: Decimal
    unit_price: Decimal
    uom: str

class WOPart(WOPartBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WOThirdPartyBase(BaseModel):
    provider_name: str
    description: str
    price: Decimal

class WOThirdParty(WOThirdPartyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Work Order Schemas
class WorkOrderBase(BaseModel):
    vehicle_id: int
    status: str = "Pendiente"
    diagnosis: Optional[str] = None
    solution: Optional[str] = None
    recommendation: Optional[str] = None

class WorkOrderCreate(WorkOrderBase):
    pass

class WorkOrder(WorkOrderBase):
    id: int
    entry_date: datetime
    exit_date: Optional[datetime] = None
    vehicle: Vehicle
    tasks: List[WOTask] = []
    parts: List[WOPart] = []
    third_parties: List[WOThirdParty] = []
    model_config = ConfigDict(from_attributes=True)

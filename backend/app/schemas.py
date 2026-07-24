from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Equipment
# =====================================================

class EquipmentCreate(BaseModel):
    # Договор
    contract_number: str
    client_name: str

    # Оборудование
    vendor: str
    model: str
    serial_number: str
    size_u: int
    placement_type: Optional[str] = None

    # Размещение
    room_id: int
    rack_id: int
    top_unit: int


class EquipmentUpdate(BaseModel):
    vendor: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    size_u: Optional[int] = None
    placement_type: Optional[str] = None


class EquipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    contract_number: str
    client_name: str

    vendor: str
    model: str
    serial_number: str

    size_u: Optional[int]
    placement_type: Optional[str]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# =====================================================
# Placement
# =====================================================

class PlacementCreate(BaseModel):
    rack_id: int
    bottom_unit: int
    top_unit: int


class PlacementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int

    rack_id: int

    bottom_unit: int
    top_unit: int

    placed_at: Optional[datetime]
    removed_at: Optional[datetime]


# =====================================================
# Clients
# =====================================================

class ClientCreate(BaseModel):
    name: str
    comment: Optional[str] = None


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    comment: Optional[str]
    created_at: Optional[datetime]


# =====================================================
# Contracts
# =====================================================

class ContractCreate(BaseModel):
    client_id: int
    contract_number: str
    comment: Optional[str] = None


class ContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    client_id: int
    client_name: Optional[str] = None

    contract_number: str
    comment: Optional[str]

    created_at: Optional[datetime]


# =====================================================
# Rooms
# =====================================================

class RoomCreate(BaseModel):
    name: str
    comment: Optional[str] = None


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    comment: Optional[str]


# =====================================================
# Racks
# =====================================================

class RackCreate(BaseModel):
    room_id: int
    rack_number: int
    height_u: int
    comment: Optional[str] = None


class RackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int

    rack_number: int
    height_u: int

    comment: Optional[str]


# =====================================================
# History
# =====================================================

class HistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int

    operation: str
    description: Optional[str]

    created_at: Optional[datetime]


# =====================================================
# Rack layout
# =====================================================

class RackUnit(BaseModel):
    unit: int

    equipment_id: Optional[int] = None

    contract_number: Optional[str] = None

    vendor: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None


class RackLayoutResponse(BaseModel):
    rack_id: int
    units: list[RackUnit]

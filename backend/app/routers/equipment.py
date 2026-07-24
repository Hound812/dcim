from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(
    prefix="/api/equipment",
    tags=["Equipment"]
)


# =====================================================
# Получить список оборудования
# =====================================================

@router.get(
    "",
    response_model=list[schemas.EquipmentResponse]
)
def get_equipment_list(
    db: Session = Depends(get_db)
):
    return crud.get_all_equipment(db)


# =====================================================
# Получить оборудование по ID
# =====================================================

@router.get(
    "/{equipment_id}",
    response_model=schemas.EquipmentResponse
)
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    equipment = crud.get_equipment(db, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return equipment


# =====================================================
# Создать оборудование
# =====================================================

@router.post(
    "",
    response_model=schemas.EquipmentResponse,
    status_code=201
)
def create_equipment(
    item: schemas.EquipmentCreate,
    db: Session = Depends(get_db)
):
    existing = crud.get_equipment_by_serial(
        db,
        item.serial_number
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Equipment with this serial number already exists"
        )

    try:
        return crud.create_equipment(db, item)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# =====================================================
# Обновить оборудование
# =====================================================

@router.put(
    "/{equipment_id}",
    response_model=schemas.EquipmentResponse
)
def update_equipment(
    equipment_id: int,
    item: schemas.EquipmentUpdate,
    db: Session = Depends(get_db)
):
    equipment = crud.update_equipment(
        db,
        equipment_id,
        item
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return equipment


# =====================================================
# Удалить оборудование
# =====================================================

@router.delete(
    "/{equipment_id}"
)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_equipment(
        db,
        equipment_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return {
        "status": "ok"
    }


# =====================================================
# Разместить оборудование
# =====================================================

@router.post(
    "/{equipment_id}/place",
    response_model=schemas.PlacementResponse
)
def place_equipment(
    equipment_id: int,
    placement: schemas.PlacementCreate,
    db: Session = Depends(get_db)
):
    equipment = crud.get_equipment(
        db,
        equipment_id
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return crud.place_equipment(
        db,
        equipment_id,
        placement
    )

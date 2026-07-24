from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Rack
import app.crud as crud
from app.schemas import (
    RackCreate,
    RackResponse,
    RackLayoutResponse
)

router = APIRouter(
    prefix="/api/racks",
    tags=["Racks"]
)


@router.get("/", response_model=list[RackResponse])
def get_racks(db: Session = Depends(get_db)):
    return db.query(Rack).order_by(Rack.room_id, Rack.rack_number).all()

@router.get("/{rack_id}", response_model=RackResponse)
def get_rack(rack_id: int, db: Session = Depends(get_db)):
    rack = db.query(Rack).filter(Rack.id == rack_id).first()

    if rack is None:
        raise HTTPException(status_code=404, detail="Rack not found")

    return rack


@router.post("/", response_model=RackResponse, status_code=201)
def create_rack(rack_data: RackCreate, db: Session = Depends(get_db)):
    rack = Rack(
        room_id=rack_data.room_id,
        rack_number=rack_data.rack_number,
        height_u=rack_data.height_u,
        comment=rack_data.comment
    )

    db.add(rack)
    db.commit()
    db.refresh(rack)

    return rack


@router.put("/{rack_id}", response_model=RackResponse)
def update_rack(
    rack_id: int,
    rack_data: RackCreate,
    db: Session = Depends(get_db)
):
    rack = db.query(Rack).filter(Rack.id == rack_id).first()

    if rack is None:
        raise HTTPException(status_code=404, detail="Rack not found")

    rack.room_id = rack_data.room_id
    rack.rack_number = rack_data.rack_number
    rack.height_u = rack_data.height_u
    rack.comment = rack_data.comment

    db.commit()
    db.refresh(rack)

    return rack


@router.delete("/{rack_id}")
def delete_rack(rack_id: int, db: Session = Depends(get_db)):
    rack = db.query(Rack).filter(Rack.id == rack_id).first()

    if rack is None:
        raise HTTPException(status_code=404, detail="Rack not found")

    db.delete(rack)
    db.commit()

    return {
        "status": "success",
        "message": f"Rack {rack_id} deleted"
    }
@router.get("/{rack_id}/layout", response_model=RackLayoutResponse)
def get_rack_layout_endpoint(
    rack_id: int,
    db: Session = Depends(get_db)
):
    layout = crud.get_rack_layout(db, rack_id)

    if layout is None:
        raise HTTPException(
            status_code=404,
            detail="Rack not found"
        )

    return layout

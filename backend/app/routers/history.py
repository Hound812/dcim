from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EquipmentHistory
from app.schemas import HistoryResponse

router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)


@router.get("/", response_model=list[HistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return (
        db.query(EquipmentHistory)
        .order_by(EquipmentHistory.created_at.desc())
        .all()
    )


@router.get("/{equipment_id}", response_model=list[HistoryResponse])
def get_equipment_history(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    history = (
        db.query(EquipmentHistory)
        .filter(EquipmentHistory.equipment_id == equipment_id)
        .order_by(EquipmentHistory.created_at.desc())
        .all()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="History not found"
        )

    return history

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PlacementCreate, PlacementResponse
from app.crud import place_equipment

router = APIRouter(
    prefix="/api/placement",
    tags=["Placement"]
)


@router.post(
    "/{equipment_id}",
    response_model=PlacementResponse,
    status_code=201
)
def place(
    equipment_id: int,
    placement: PlacementCreate,
    db: Session = Depends(get_db)
):
    return place_equipment(
        db=db,
        equipment_id=equipment_id,
        placement=placement
    )

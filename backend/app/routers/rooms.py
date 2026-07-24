from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Room
from app.schemas import RoomCreate, RoomResponse

router = APIRouter(
    prefix="/api/rooms",
    tags=["Rooms"]
)


@router.get("/", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).order_by(Room.name).all()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return room


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(room_data: RoomCreate, db: Session = Depends(get_db)):
    room = Room(
        name=room_data.name,
        comment=room_data.comment
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_data: RoomCreate,
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    room.name = room_data.name
    room.comment = room_data.comment

    db.commit()
    db.refresh(room)

    return room


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()

    return {
        "status": "success",
        "message": f"Room {room_id} deleted"
    }

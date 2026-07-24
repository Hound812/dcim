from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate, ClientResponse

router = APIRouter(
    prefix="/api/clients",
    tags=["Clients"]
)


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.name).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    client = Client(
        name=client_data.name,
        comment=client_data.comment
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientCreate,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client.name = client_data.name
    client.comment = client_data.comment

    db.commit()
    db.refresh(client)

    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {
        "status": "success",
        "message": f"Client {client_id} deleted"
    }

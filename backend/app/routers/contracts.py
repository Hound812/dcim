from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate, ContractResponse

router = APIRouter(
    prefix="/api/contracts",
    tags=["Contracts"]
)


@router.get("/", response_model=list[ContractResponse])
def get_contracts(db: Session = Depends(get_db)):
    return db.query(Contract).order_by(Contract.contract_number).all()


@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract


@router.post("/", response_model=ContractResponse, status_code=201)
def create_contract(contract_data: ContractCreate, db: Session = Depends(get_db)):
    contract = Contract(
        client_id=contract_data.client_id,
        contract_number=contract_data.contract_number,
        comment=contract_data.comment
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return contract


@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(
    contract_id: int,
    contract_data: ContractCreate,
    db: Session = Depends(get_db)
):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract.client_id = contract_data.client_id
    contract.contract_number = contract_data.contract_number
    contract.comment = contract_data.comment

    db.commit()
    db.refresh(contract)

    return contract


@router.delete("/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    db.delete(contract)
    db.commit()

    return {
        "status": "success",
        "message": f"Contract {contract_id} deleted"
    }

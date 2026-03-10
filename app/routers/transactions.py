from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import Sessiondep
from models import Customer, Transaction, TransactionCreate

router = APIRouter(tags=["transactions"])


@router.post("/transactions")
async def create_transaction(transaction_data: TransactionCreate, session: Sessiondep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="customer doesn´t exist"
        )

    transaction_db = Transaction.moddel_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("transactions")
async def list_transaction(session: Sessiondep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions

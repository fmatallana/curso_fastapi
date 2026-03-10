from typing import Optional

from db import Sessiondep
from fastapi import APIRouter, HTTPException, Query, status
from models import (
    Customer,
    CustomerCreate,
    CustomerPlan,
    CustomerUpdate,
    Plan,
    StatusEnum,
)
from sqlmodel import select

router = APIRouter(tags=["customers"])


@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: Sessiondep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/customers", response_model=list[Customer])
async def list_customer(session: Sessiondep):
    return session.exec(select(Customer)).all()


@router.get("/customers/{customer_id}", response_model=Customer)
async def show_customer(customer_id: int, session: Sessiondep):
    # RECORDATORIO: 'select' crea la consulta, 'session.exec' la ejecuta.
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(
            status_code=404, detail=f"No hay cliente con el id {customer_id}"
        )
    return customer


@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_200_OK,
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: Sessiondep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exist"
        )
    # RECORDATORIO: exclude_unset=True evita sobrescribir con valores Nulos lo que el usuario no envió.
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exist"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@router.post("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: Sessiondep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or plan doesnt exist",
        )
    customer_plan_db = CustomerPlan(
        plan_id=plan_db.id, customer_id=plan_db.id, status=plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get("/customers/{customer_id}/plans")
async def list_subscribe_customer_to_plan(
    customer_id: int,
    session: Sessiondep,
    plan_status: Optional[StatusEnum] = Query(default=None),
):
    if plan_status is None:
        customer_db = session.get(Customer, customer_id)
        return customer_db
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or plan doesnt exist",
        )
    stmt = (
        select(Plan)
        .join(CustomerPlan, CustomerPlan.plan_id == Plan.id)
        .where(CustomerPlan.customer_id == customer_id, CustomerPlan.status == status)
    )
    return session.exec(
        stmt
    ).all()  # customers puede acceder a plans ya que tiene una relacion  plans list[Plan] = Relationship(back_populates="customers", link_model=CustomerPlan)

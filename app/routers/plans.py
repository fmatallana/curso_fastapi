from db import Sessiondep
from fastapi import APIRouter, HTTPException, status
from models import Customer, CustomerPlan, Plan
from sqlmodel import select

router = APIRouter(tags=["plans"])


@router.post("/plans")
async def create_plan(plan_data: Plan, session: Sessiondep):
    plan_db = Plan.model_validate(
        plan_data.model_dump()
    )  # esto valida que la data que pase el usuario sea valida y con el model_dump convierte esta data en un diccionario
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get("/plans", response_model=list[Plan])
async def list_plan(session: Sessiondep):
    plans = session.exec(select(Plan)).all()
    return plans


@router.get("/plans/active", response_model=list[CustomerPlan])
async def show_active_plans(session: Sessiondep):
    # RECORDATORIO: Puedes pasar múltiples condiciones al .where() separadas por coma (es un AND lógico).
    statement = select(CustomerPlan).where(CustomerPlan.is_active)
    product = session.exec(statement).all()
    if not product:
        return []
    return product


@router.patch("/customers/{customer_id}/plans/{plan_id}")
async def cancel_suscription(customer_id: int, plan_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Customer, plan_id)
    statement = select(CustomerPlan).where(
        CustomerPlan.customer_id == customer_id, CustomerPlan.plan_id == plan_id
    )
    sub = session.exec(statement).first()
    if not customer_db or not plan_db or not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or plan doesnt exist",
        )
    if not sub.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La suscripción ya está cancelada",
        )
    sub.is_active = False
    session.add(sub)
    session.commit()
    session.refresh(sub)
    return sub

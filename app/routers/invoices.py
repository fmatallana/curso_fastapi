from fastapi import APIRouter

from models import Invoice

router = APIRouter(tags=["invoices"])


@router.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data

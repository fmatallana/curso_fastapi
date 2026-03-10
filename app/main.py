import time
from typing import Annotated

from db import create_all_tables
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .routers import customers, fechas, invoices, orders, plans, products

app = FastAPI(lifespan=create_all_tables)  # type: ignore
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(fechas.router)
app.include_router(invoices.router)
app.include_router(plans.router)


@app.middleware("http")  # asi se define un middleware
async def log_request(
    request: Request, call_next
):  # un middleware recibe el request que se esta haciendo, de tipo request (que se importa desde fast api), la funcion call_next que lo que hace es llamar la funcionalidad por defecto que ya venia llamando
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"request: {request.url} completed in:{process_time:.4f} seconds")
    return response


@app.middleware("http")
async def log_request_headers(request: Request, call_next) -> Request:
    """
    Middleware para registrar los encabezados de la solicitud.
    Parámetros:
    - request: La solicitud entrante.
    """
    print(f"Request headers: {request.headers}")
    response = await call_next(request)
    return response


security = HTTPBasic()


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):  # noqa: F821
    print(credentials)
    if credentials.username == "lcmartinez" and credentials.password == "4234":
        return {"mensaje": f"hola {credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

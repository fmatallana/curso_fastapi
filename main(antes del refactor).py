import zoneinfo
from datetime import datetime

from db import Sessiondep, create_all_tables
from fastapi import FastAPI, HTTPException, status
from models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    Invoice,
    Order,
    OrderCreate,
    OrderItem,
    OrderStatus,
    Product,
    ProductCreate,
    ProductUpdate,
    Transaction,
)
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"mensaje": "hola mundo"}


country_timezones = {
    "CO": "America/Bogota",  # Colombia
    "MX": "America/Mexico_City",  # México
    "AR": "America/Argentina/Buenos_Aires",  # Argentina
    "PE": "America/Lima",  # Perú
    "BR": "America/Sao_Paulo",  # Brasil
}


@app.get("/fecha/{iso_code}")
async def get_date(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if not timezone_str:
        return {"error": "Código de país no encontrado"}

    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"hora": datetime.now(tz)}


# --- SECCIÓN DE CLIENTES ---


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: Sessiondep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customer(session: Sessiondep):
    return session.exec(select(Customer)).all()


@app.get("/customers/{customer_id}", response_model=Customer)
async def show_customer(customer_id: int, session: Sessiondep):
    # RECORDATORIO: 'select' crea la consulta, 'session.exec' la ejecuta.
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(
            status_code=404, detail=f"No hay cliente con el id {customer_id}"
        )
    return customer


@app.patch(
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


@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exist"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


# --- SECCIÓN DE PRODUCTOS ---


@app.post("/products", response_model=Product, status_code=201)
async def create_products(product_data: ProductCreate, session: Sessiondep):
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products", response_model=list[Product])
async def list_products(session: Sessiondep, offset: int = 0, limit: int = 100):
    query = select(Product).offset(offset).limit(limit)
    return session.exec(query).all()


@app.get("/product/{product_id}", response_model=Product)
async def show_product(product_id: int, session: Sessiondep):
    # RECORDATORIO: session.get es más directo que select().where() cuando buscas por ID (Primary Key).
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"No hay productos con el id {product_id}"
        )
    return product


@app.patch(
    "/product/{product_id}", response_model=Product, status_code=status.HTTP_200_OK
)
async def update_product(
    product_id: int, product_data: ProductUpdate, session: Sessiondep
):
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product_data_dict = product_data.model_dump(exclude_unset=True)
    product_db.sqlmodel_update(product_data_dict)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


@app.get("/product/avaliable", response_model=list[Product])
async def show_avaliable_product(session: Sessiondep):
    # RECORDATORIO: Puedes pasar múltiples condiciones al .where() separadas por coma (es un AND lógico).
    statement = select(Product).where(Product.stock > 0, Product.is_active)
    product = session.exec(statement).all()
    if not product:
        return []
    return product


# --- SECCIÓN DE ÓRDENES ---


@app.post("/orders", response_model=Order, status_code=201)
async def create_orders(product_data: OrderCreate, session: Sessiondep):
    customer_db = session.get(
        Customer, product_data.customer_id
    )  # se toma el id de ordercreate
    if not customer_db:  # si este id no existe, lanza este error
        raise HTTPException(status_code=404, detail="cliente no encontrado")

    db_order = Order(
        customer_id=product_data.customer_id,
        total=0,
        created_at=datetime.now().isoformat(),
    )  # se crea una nueva orden
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    # se actualiza con estos 3 sessions
    total_acumulado = 0  # vatiable que se usara desúes en el fpr
    for item in product_data.items:
        # Recuperamos la información oficial (precio y estado) desde la base de datos
        disponibilidad = session.get(
            Product, item.product_id
        )  # se hace un get dentro de la lista items con la clase product
        if (
            disponibilidad and disponibilidad.is_active
        ):  # Verificamos que el producto exista y esté habilitado para la venta
            if (
                item.quantity <= disponibilidad.stock
            ):  # si la cantidad de lo que pide el usuario es menor a lo qye hay disponible entra a la validacion
                disponibilidad.stock -= item.quantity  # Actualizamos el inventario y calculamos el subtotal con el precio vigente
                subtotal = (
                    item.quantity * disponibilidad.price
                )  # multiplica la cantidad de items que pidio el usuario por el precio que hay de este en la creacion del producto
                total_acumulado += subtotal  # aca se actualiza la cariable total acumulado con la multiplicacion anterior

                nuevo_item = OrderItem(
                    order_id=db_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=disponibilidad.price,  # Congelamos el precio de venta actual
                )  # Vinculamos el producto a la orden usando el ID generado previamente
                session.add(nuevo_item)  # se actualiza la session
            else:
                raise HTTPException(
                    status_code=400, detail="No hay suficiente stock"
                )  # si no se cumple el primer if salta este raise
        else:
            raise HTTPException(
                status_code=400, detail="El producto no es valido o no existe"
            )  # si no existe el id del product se lanza este raise

    db_order.total = total_acumulado  # el total de la primera orden ahora vale lo del total acumulado del total de la orden del bucle
    session.commit()
    session.refresh(db_order)
    return db_order  # se retorna el db_order


@app.get("/orders", response_model=list[Order])
async def list_order(session: Sessiondep, offset: int = 0, limit: int = 100):
    query = select(Order).offset(offset).limit(limit)
    return session.exec(query).all()


@app.get("/order/{order_id}")
async def show_order_details(order_id: int, session: Sessiondep):
    # RECORDATORIO: Aquí hacemos una respuesta personalizada uniendo datos de dos tablas manualmente.
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="No hay ordenes")

    # RECORDATORIO: Filtramos OrderItem usando el 'order_id' como llave foránea.
    statement = select(OrderItem).where(OrderItem.order_id == order_id)
    items_list = session.exec(statement).all()

    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "total": db_order.total,
        "created_at": db_order.created_at,
        "items": items_list,
    }


@app.patch("/orders/{order_id}/status")
async def change_order_status(
    order_id: int, product_data: OrderStatus, session: Sessiondep
):
    # RECORDATORIO: Buscamos por el ID de la URL, no por el contenido del body.
    order_db = session.get(Order, order_id)
    if not order_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order doesn´t exist"
        )

    # RECORDATORIO: Aquí actualizamos el objeto 'trackeado' por la sesión y luego comiteamos.
    order_db.status = product_data.status
    session.commit()
    session.refresh(order_db)
    return order_db


# --- OTROS ENDPOINTS ---


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data

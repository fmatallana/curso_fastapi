from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import Sessiondep
from models import Customer, Order, OrderCreate, OrderItem, OrderStatus, Product

router = APIRouter(tags=["orders"])
# --- SECCIÓN DE ÓRDENES ---


@router.post("/orders", response_model=Order, status_code=201)
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


@router.get("/orders", response_model=list[Order])
async def list_order(session: Sessiondep, offset: int = 0, limit: int = 100):
    query = select(Order).offset(offset).limit(limit)
    return session.exec(query).all()


@router.get("/order/{order_id}")
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


@router.patch("/orders/{order_id}/status")
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

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import Sessiondep
from models import Product, ProductCreate, ProductUpdate

router = APIRouter(tags=["products"])


@router.post("/products", response_model=Product, status_code=201)
async def create_products(product_data: ProductCreate, session: Sessiondep):
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.get("/products", response_model=list[Product])
async def list_products(session: Sessiondep, offset: int = 0, limit: int = 100):
    query = select(Product).offset(offset).limit(limit)
    return session.exec(query).all()


@router.get("/product/{product_id}", response_model=Product)
async def show_product(product_id: int, session: Sessiondep):
    # RECORDATORIO: session.get es más directo que select().where() cuando buscas por ID (Primary Key).
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"No hay productos con el id {product_id}"
        )
    return product


@router.patch(
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


@router.get("/product/avaliable", response_model=list[Product])
async def show_avaliable_product(session: Sessiondep):
    # RECORDATORIO: Puedes pasar múltiples condiciones al .where() separadas por coma (es un AND lógico).
    statement = select(Product).where(Product.stock > 0, Product.is_active)
    product = session.exec(statement).all()
    if not product:
        return []
    return product

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import Field, Relationship, Session, SQLModel, select

from db import engine


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    plan_id: int = Field(
        foreign_key="plan.id"
    )  # con plan.id se se referencia el id del modelo plan
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)
    customer: "Customer" = Relationship()
    plan: "Plan" = Relationship()


class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )  # esta relacion lo que hace es usar la variable o el campo plans que esta en la otra tabla y se linkea con el modelo CustomerPlan


# relacion de plan y customer mediante otra tabla intermedia y foreign keys


class CustomerBase(SQLModel):
    name: str
    description: str | None = Field(default=None)
    email: EmailStr
    age: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("this email is already registered")
        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class ProductBase(SQLModel):
    name: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    is_active: bool = Field(default=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(gt=0)
    stock: int | None = Field(ge=0)
    is_active: bool = Field(default=True)


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class OrderBase(SQLModel):
    customer_id: int = Field(foreign_key="customer.id")
    status: str = Field(default="pending")
    total: float = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderStatus(BaseModel):
    status: str


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]


class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderItem(OrderItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TransacctionBase(SQLModel):
    ammount: int
    description: str


class Transaction(TransacctionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class TransactionCreate(TransacctionBase):
    customer_id: int = Field(foreign_key="customer.id")


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)

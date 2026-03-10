import pytest
from db import get_session
from fastapi.testclient import TestClient
from models import Customer
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel

from app.main import app

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_overwrite():
        return session

    app.dependency_overrides[get_session] = get_session_overwrite
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="customer")
def customer_fixture(session: Session):
    customer = Customer(
        name="Test Customer",
        email="test@example.com",
        age=30,
        description="A test customer",
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    yield customer

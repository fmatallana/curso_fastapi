"""
configuracion de entorno local


1. crear un archivo de conftest.py(aca se hacen todas las configuraciones que se necesiten)
importar pytest, testclient


se debe configurar una base de datos para los testing

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

a esta configuracion se le debe pasar un diccionario por medio de connect_args, check_same_thread:false

el poolclass=StaticPool (importar desde sqlalchemy.pool) sera uno que cree la DB de manera temporal y en memoria


se debe hacer la siguiente configuracion de tablas

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)      # Crea las tablas antes del test
    with Session(engine) as session:
        yield session                          # Le pasa la sesión al test
    SQLModel.metadata.drop_all(engine)         # Limpia las tablas después del test

EXPLICACIÓN CORTA:
- create_all(): Prepara BD limpia antes de cada test
- yield session: Proporciona sesión para usar en el test
- drop_all(): Limpia BD después del test para aislamiento


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_overwrite():           # Función que retorna la sesión del test
        return session

    app.dependency_overrides[get_session] = get_session_overwrite  # Reemplaza get_session de la app
    client = TestClient(app)               # Crea cliente HTTP para hacer peticiones al servidor
    yield client                           # Le pasa el cliente al test
    app.dependency_overrides.clear()       # Limpia las overrides después del test

EXPLICACIÓN CORTA:
- dependency_overrides: Intercepta las dependencias de FastAPI
- TestClient: Cliente HTTP para simular peticiones sin levantar servidor real
- yield client: Proporciona cliente para hacer requests en el test
- clear(): Limpia las sobreescrituras para no afectar otros tests


#PRUEBA DEL CLIENT

from fastapi.testclient import TestClient

def test_client(client):
    assert type(client) == TestClient

assert permite validar que 2 cosas son iguales
"""

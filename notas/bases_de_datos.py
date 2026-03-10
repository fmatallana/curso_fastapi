"""
para poder asignar una primary key a una variable o parametro primero se importa field desde sqlmodel

luego se escribe la siguiente linea


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True) lo que hace es agregar el primary key y que sea umente de a 1 automaticamente

CREACION DE TABLAS


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine) el metodo create_all() requiere el motor de base de datos que se va a usar y ese motor esta en la variable engine
    yield


app = FastAPI(lifespan=create_all_tables)

FastAPI(): Crea la aplicación web
lifespan=create_all_tables: Asocia una función que se ejecutará durante eventos del ciclo de vida de la aplicación

El parámetro lifespan espera una función asíncrona de contexto (async context manager) que se ejecuta:

Al inicio: cuando la aplicación arranca (startup)
Al final: cuando la aplicación se cierra (shutdown)


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: Sessiondep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

customer_data.model_dump() convierte el objeto Pydantic a un diccionario
Customer.model_validate() crea una instancia del modelo Customer (el modelo de la base de datos) a partir de ese diccionario

Añade el nuevo objeto customer a la sesión de la base de datos (lo prepara para ser guardado)
session.commit()

Confirma la transacción y guarda permanentemente el cliente en la base de dato

session.refresh(customer)

Actualiza el objeto customer con los datos que la base de datos pudo haber generado (como un ID auto-incremental, timestamps, etc.)

return customer

Devuelve el cliente creado, que FastAPI serializará automáticamente a JSON según el response_model

@app.get("/customers", response_model=list[Customer])
async def list_customer(session: Sessiondep):
    return session.exec(select(Customer)).all()

lo que esto hace es retornar todas las entidades del tipo customer, se debe importar select de sqlmodel
"""

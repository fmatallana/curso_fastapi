"""
MÓDULO DE GESTIÓN DE CLIENTES
Este módulo implementa un CRUD básico utilizando FastAPI y Pydantic.

MODELOS DE DATOS (Esquemas):
    - CustomerBase: Define los campos comunes (nombre, descripción, email, edad).
    - CustomerCreate: Modelo para la entrada de datos (sin ID).
    - Customer: Modelo para la salida y almacenamiento (incluye ID).


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):

    Crea un nuevo cliente en el sistema.

    Proceso:
    1. Convierte 'customer_data' (CustomerCreate) a diccionario con .model_dump().
    2. Valida y transforma ese diccionario al modelo 'Customer' con .model_validate().
    3. Asigna un ID único basado en la longitud actual de la lista 'db_customers'.
    4. Almacena el objeto en la base de datos volátil (lista).

    Returns:
    - El objeto Customer creado, incluyendo su nuevo ID asignado.

    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customer():

    Obtiene la lista completa de clientes.

    Returns:
    - Una lista de objetos Customer. FastAPI serializa automáticamente
      la lista basándose en el 'response_model'.
    return db_customers


@app.get("/customers/{customer_id}", response_model=Customer)
async def show_customer(customer_id: int):

    Busca un cliente específico por su ID.

    Args:
        customer_id (int): El identificador único del cliente a buscar.

    Raises:
        HTTPException: Error 404 si el ID no existe en la lista.

    Returns:
        Customer: Los datos del cliente encontrado.

    for customer in db_customers:
        if customer.id == customer_id:
            return customer
    raise HTTPException(
        status_code=404, detail=f"No hay cliente con el id {customer_id}"
    ): El identificador único del cliente

"""

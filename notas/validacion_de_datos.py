"""
class Customer(BaseModel):
    name: str
    description: str | None
    email: str
    age: int

esto es una clase pero en fast api se le llama un Modelo y es una representación de la estructura de los datos. No es solo una clase común que tiene métodos y lógica; su función principal es definir cómo debe lucir la información (qué campos tiene, de qué tipo son y si son obligatorios).
Al heredar de BaseModel, le estás diciendo a Python: "Esta clase no es solo un objeto, es un estándar o molde para validar datos que vienen de fuera (como un formulario web o una base de datos)".

para la creacion las apirest deben usar post
@app.post("/customers")
async def create_customer(customer_data: Customer):
    return customer_data
"""

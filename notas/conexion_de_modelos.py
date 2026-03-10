"""
por buena praactica se pasan todos los modelos a un archivo nuedo (modelos.py)

class Customer(BaseModel):
    id: int
    name: str
    description: str | None
    email: EmailStr
    age: int


class Transaction(BaseModel):
    id: int
    ammount: int
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)

en este caso se crean 2 modelos customer y transaction en envoy se crean 4 parametros , 2 de la clase invoice y 2 que se tipan de los modelos creados, asi se hace la conexion

@property en Python permite usar un método como si fuera un atributo de clase

se crea una funcion que retorne la suma de ransaction.ammount y se hace un for dentro de la lista transactions previamente tipada en la clase envoice
"""

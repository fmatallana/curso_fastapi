"""
table = true permite crear tablas dentro de la DB
importante ponerle el primary key a los id de la siguente manera = Field(default= none, primary_key = True)

para crear la foreing key se hace lo siguiente, dentro del modelo que se va a relacionar se crea la foreing key de otro campo, si voy a relacionar una transaccion con un cliente, la logica es la siguiente

un cliente puede crear muchas tranasacciones

entonces dentro del modelo de transacciones que tiene el id y hereda de transaccionBase
se crea un campo customer id que es de tipo int y para declarar su foreing key se hace lo siguiente  Field(foreing_key = "cliente.id")
esto lo que quiere decir es que se accede al id del cliente

si el modelo de cliente esta asi

class cliente(clienteBase, table=True):
id:int = Field(default = none, primary_key = True)

pues se accede al campo id para hacer la relacion

campo que hace una relacion, no se crea un nuevo campo directamente en la tabla pero este campo nos permite obtener datos

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")

lo que hace list["Transaction"] es darle el mismo tipado al campo transactions que tiene el modelo Transaction

Relationship(back_populates="customer"), lo que hace es llenar la lista transactions con un campo llamado customer que esta en el modelo Transaction

el campo customer en el modelo de transactions esta de la siguiente manera

customer: Customer = Relationship(back_populates="transactions")

y lo que hacen es practicamente lo mismo, el campo transactions del modelo customer se llena con informacion del campo customer de transactions y el customer se llena con las transactions

si se crea un nuevo modelo, se deben crear los routers de dicho modelo
"""

"""
1. creacion y activacion de un venv
2. instalacion de fastapi pip install "fastapi[standard]"

3.  desarrollar api en main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "Hola, Mundo"}

La función root define un endpoint básico que devuelve un mensaje JSON. Utiliza el decorador @app.get("/") para indicar que este endpoint responde a solicitudes GET en la ruta raíz (/).


¿Cómo ejecutar y probar la API en desarrollo?
Iniciar el servidor:

Usa Uvicorn para ejecutar la aplicación:
uvicorn main:app --reload
El parámetro --reload activa el modo de desarrollo, permitiendo recargar la API automáticamente cada vez que guardes cambios en el código.

si se crea otra funcion async def para enrar al puerto y ver lo que retorna se hace asi http://localhost:8000/nombre_del_app.get


en mi caso http://localhost:8000/fecha
"""

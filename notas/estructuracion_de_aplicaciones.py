"""
ESTRUCTURA DEL PROYECTO (FastAPI Standard Layout)

/ (Root)
├── db.py              # Configuración y conexión a la Base de Datos.
├── models.py          # Definición de modelos de datos (SQLAlchemy/Pydantic).
│                        Nota: Si superan los 3 modelos, mover a una carpeta /models.
├── requirements.txt   # Dependencias del proyecto.
│
└── app/               # Paquete principal que encapsula la lógica de la API.
    ├── __init__.py    # Convierte la carpeta app en un módulo importable.
    ├── main.py        # Punto de entrada: instancia FastAPI e incluye los routers.
    ├── dependencies.py # Lógica de inyección de dependencias (Auth, DB session, etc).
    │
    └── routers/       # Submódulo para la división de endpoints (Mini-apps).
        ├── __init__.py
        ├── customers.py    # Endpoints de Clientes.
        ├── invoices.py     # Endpoints de Facturas.
        └── transactions.py # Endpoints de Transacciones.

DESCRIPCIÓN DE COMPONENTES:
- APIRouter: Utilizado en la carpeta /routers para agrupar y organizar rutas
             por dominio lógico, manteniendo el main.py limpio.
- __init__.py: Archivos clave para permitir imports relativos entre módulos.
"""

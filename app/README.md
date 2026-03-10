# 🚀 FastAPI E-Commerce API

Una API REST completa y robusta construida con **FastAPI** para gestionar un sistema de comercio electrónico. Este proyecto implementa mejores prácticas de desarrollo, incluyendo autenticación, validación de datos, testing y una arquitectura modular y escalable.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Arquitectura](#arquitectura)
- [Contribuir](#contribuir)

## ✨ Características

### Core Features
- ✅ **Autenticación HTTP Basic** para endpoints protegidos
- ✅ **CRUD Completo** para múltiples recursos (clientes, productos, pedidos, etc.)
- ✅ **Relaciones Entre Modelos** (One-to-Many, Many-to-Many)
- ✅ **Sistema de Planes** para asignar planes a clientes
- ✅ **Gestión de Pedidos** con items, estado y seguimiento
- ✅ **Sistema de Transacciones** y facturas
- ✅ **Validación de Datos** con Pydantic y EmailStr
- ✅ **Middleware de Logging** para rastrear requests y tiempos de respuesta
- ✅ **Base de Datos SQLite** con SQLModel (ORM moderno)
- ✅ **Testing Unitario** con Pytest y fixtures configuradas
- ✅ **Documentación Automática** con Swagger UI y ReDoc

## 📁 Estructura del Proyecto

```
app/
├── __init__.py                 # Inicializador del package
├── conftest.py                 # Configuración de fixtures para pytest
├── main.py                     # Aplicación principal de FastAPI
├── routers/                    # Endpoints organizados por módulos
│   ├── __init__.py
│   ├── customers.py           # CRUD de clientes y relación con planes
│   ├── products.py            # CRUD de productos
│   ├── orders.py              # Gestión de pedidos y items
│   ├── plans.py               # CRUD de planes
│   ├── fechas.py              # Endpoints de fechas (utility)
│   ├── invoices.py            # Gestión de facturas
│   └── transactions.py        # Gestión de transacciones
├── tests/                      # Suite de testing
│   ├── __init__.py
│   ├── test.py               # Tests básicos
│   └── tests_customers.py    # Tests específicos de clientes
├── db.sqlite3                 # Base de datos (generada automáticamente)
└── README.md                  # Este archivo

models.py                       # Definición de modelos SQLModel
db.py                          # Configuración de base de datos
requirements.txt               # Dependencias del proyecto
```

## 🔧 Requisitos Previos

- **Python 3.10+**
- **pip** (gestor de paquetes de Python)
- **Git** (para versionado)

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/curso-fastapi-project.git
cd curso-fastapi-project
```

### 2. Crear entorno virtual
```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Verificar instalación
```bash
python -c "import fastapi; print(fastapi.__version__)"
```

## ⚙️ Configuración

### Estructura de Base de Datos

La base de datos se crea automáticamente al iniciar la aplicación. Los modelos incluyen:

- **Customer**: Clientes con email, nombre, edad y descripción
- **Product**: Productos con precio, stock y estado
- **Plan**: Planes de suscripción con precio y descripción
- **CustomerPlan**: Relación Many-to-Many entre clientes y planes
- **Order**: Pedidos con fecha de creación y total
- **OrderItem**: Items dentro de un pedido
- **Invoice**: Facturas generadas
- **Transaction**: Transacciones de pago

### Autenticación

La API implementa **HTTP Basic Authentication**. Por defecto:
- **Usuario**: `lcmartinez`
- **Contraseña**: `4234`

⚠️ **Importante**: Cambiar estas credenciales en `main.py` antes de usar en producción.

### Variables de Entorno

Actualmente, la base de datos usa SQLite local. Para usar otra BD:

```python
# En db.py, modificar:
sqlite_url = "sqlite:///db.sqlite3"  # Local
# O para Production:
# database_url = "postgresql://user:password@localhost/dbname"
```

## 🏃 Uso

### Iniciar el Servidor

```bash
# Opción 1: Directamente con Python
cd app
python -m uvicorn main:app --reload

# Opción 2: Desde la raíz del proyecto
uvicorn app.main:app --reload
```

El servidor estará disponible en:
- 🌐 **API**: http://localhost:8000
- 📚 **Swagger UI**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

### Ejemplo de Request con cURL

```bash
# Obtener lista de clientes (requiere autenticación)
curl -u lcmartinez:4234 http://localhost:8000/customers

# Crear un nuevo cliente
curl -u lcmartinez:4234 -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "age": 30,
    "description": "Cliente VIP"
  }'

# Obtener cliente específico
curl -u lcmartinez:4234 http://localhost:8000/customers/1
```

## 📡 API Endpoints

### 👤 Clientes (Customers)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/customers` | Crear nuevo cliente |
| `GET` | `/customers` | Listar todos los clientes |
| `GET` | `/customers/{customer_id}` | Obtener cliente específico |
| `PATCH` | `/customers/{customer_id}` | Actualizar cliente |
| `DELETE` | `/customer/{customer_id}` | Eliminar cliente |
| `POST` | `/customers/{customer_id}/plans/{plan_id}` | Asignar plan a cliente |
| `GET` | `/customers/{customer_id}/plans` | Obtener planes del cliente |

### 📦 Productos (Products)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/products` | Crear nuevo producto |
| `GET` | `/products` | Listar productos (con paginación) |
| `GET` | `/product/{product_id}` | Obtener producto específico |
| `PATCH` | `/product/{product_id}` | Actualizar producto |
| `GET` | `/product/avaliable` | Listar productos disponibles |

### 📋 Pedidos (Orders)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/orders` | Crear nuevo pedido |
| `GET` | `/orders` | Listar todos los pedidos |
| `GET` | `/order/{order_id}` | Obtener pedido específico |
| `PATCH` | `/orders/{order_id}/status` | Actualizar estado del pedido |

### 💳 Planes (Plans)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/plans` | Crear nuevo plan |
| `GET` | `/plans` | Listar todos los planes |
| `GET` | `/plans/active` | Listar planes activos |
| `PATCH` | `/customers/{customer_id}/plans/{plan_id}` | Actualizar estado del plan |

### 📊 Otros Endpoints

- **Transacciones**: `POST /transactions`, `GET /transactions`
- **Facturas**: `POST /invoices`
- **Fechas**: `GET /fecha/{iso_code}`

## 🧪 Testing

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Con salida detallada
pytest -v

# Tests específicos
pytest app/tests/tests_customers.py -v

# Con cobertura
pytest --cov=app --cov-report=html
```

### Estructura de Tests

```
tests/
├── test.py              # Tests básicos (validar client)
└── tests_customers.py  # Tests específicos de clientes
```

### Fixtures Disponibles

Defined in `conftest.py`:
- **`session`**: Sesión de BD para tests
- **`client`**: Cliente TestClient de FastAPI
- **`customer`**: Fixture de cliente de prueba

### Ejemplo de Test

```python
def test_create_customer(client):
    response = client.post("/customers", json={
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "description": "Test"
    })
    assert response.status_code == 201
```

## 🏗️ Arquitectura

### Patrón de Proyecto

El proyecto sigue una arquitectura **modular y escalable**:

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│  (main.py - Inicialización y Routers)   │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┬─────────────┐
       │                │             │
   ┌───▼──┐    ┌────────▼──┐   ┌────▼────────┐
   │Routers   │  Models    │   │ Database    │
   │(CRUD)    │  (SQLModel)│   │ (SQLModel)  │
   └────┬─────┘  └──────────┘   └─────┬──────┘
        │                              │
        └──────────────┬───────────────┘
                       │
              ┌────────▼────────┐
              │  SQLite / DB    │
              └─────────────────┘
```

### Stack Tecnológico

- **Framework**: FastAPI 0.128.0
- **ORM**: SQLModel 0.0.31 (hybrid de SQLAlchemy + Pydantic)
- **Base de Datos**: SQLite (fácilmente migrable a PostgreSQL)
- **Testing**: Pytest
- **Validación**: Pydantic con EmailStr
- **Servidor**: Uvicorn

## 🔐 Características de Seguridad

- HTTP Basic Authentication implementada
- Validación de datos con Pydantic
- Validación de emails con EmailStr
- Manejo de excepciones HTTPException
- Middleware de logging para auditoría

## 📝 Middleware

### Request Logging
```python
@app.middleware("http")
async def log_request(request: Request, call_next):
    # Registra URL y tiempo de procesamiento
```

### Header Logging
```python
@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    # Registra headers de cada request
```

## 🚀 Despliegue

### Opciones de Producción

#### 1. **Heroku**
```bash
echo "web: gunicorn app.main:app" > Procfile
heroku login
heroku create mi-app
git push heroku main
```

#### 2. **Docker**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 3. **Railway / Render**
- Conectar repositorio Git
- Configurar comando: `uvicorn app.main:app --host 0.0.0.0`
- Variable BD: Cambiar a PostgreSQL

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación SQLModel](https://sqlmodel.tiangolo.com/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Checklist para PRs

- [ ] Código formateado con Black/Pylint
- [ ] Tests agregados y pasando
- [ ] Documentación actualizada
- [ ] Sin credenciales en el código
- [ ] Compatible con Python 3.10+

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Luis C. Martínez**

---

## 📞 Soporte

Para reportar issues o sugerencias:
- 🐛 Crear un Issue en Github
- 💬 Discusiones en el repositorio
- 📧 Email: contacto@example.com

---

**Última actualización**: Marzo 2026
**Versión**: 1.0.0

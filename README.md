# 📚 Curso FastAPI - Proyecto Completo

Un proyecto educativo completo que demuestra las mejores prácticas y patrones de desarrollo en **FastAPI**. Desarrollado como parte del curso de FastAPI.

## 🎯 Objetivo del Proyecto

Este proyecto sirve como referencia práctica para aprender:
- Construcción de APIs REST con FastAPI
- Autenticación y autorización
- ORM con SQLModel
- Testing unitario con Pytest
- Arquitectura modular y escalable
- Middlewares y validación de datos
- Documentación automática

## 📁 Estructura General

```
curso-fastapi-project/
├── app/                          # Aplicación principal
│   ├── main.py                  # Punto de entrada
│   ├── conftest.py              # Configuración de tests
│   ├── routers/                 # Endpoints por módulo
│   │   ├── customers.py         # Gestión de clientes
│   │   ├── products.py          # Gestión de productos
│   │   ├── orders.py            # Gestión de órdenes
│   │   ├── plans.py             # Gestión de planes
│   │   ├── invoices.py          # Gestión de facturas
│   │   ├── transactions.py      # Gestión de transacciones
│   │   └── fechas.py            # Funciones de fecha/hora
│   ├── tests/                   # Suite de pruebas
│   │   ├── test.py
│   │   └── tests_customers.py
│   ├── db.sqlite3               # Base de datos
│   └── README.md                # Documentación de la app (⭐ Ver este archivo)
│
├── notas/                        # Apuntes y ejemplos del curso
│   ├── autenticacion_de_http.py
│   ├── bases_de_datos.py
│   ├── conexion_de_modelos.py
│   ├── endpoints_dinamicos.py
│   ├── estructuracion_de_aplicaciones.py
│   ├── fastapi.py
│   ├── middlewares.py
│   ├── pruebas_unitarias_para_crud.py
│   ├── relacion_muchos_a_muchos.py
│   ├── relaciones_en_FASTAPI.py
│   ├── unit_testing.py
│   ├── validacion_de_datos.py
│   └── validacion de datos_y_modelos.py
│
├── models.py                     # Definición de modelos SQLModel
├── db.py                         # Configuración de BD
├── requirements.txt              # Dependencias
├── main(antes del refactor).py  # Código anterior (referencia)
├── db.sqlite3                    # BD raíz
└── README.md                     # Este archivo
```

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar o navegar al proyecto
cd curso-fastapi-project

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
# Desde la carpeta app/
cd app
python -m uvicorn main:app --reload

# O desde la raíz
uvicorn app.main:app --reload
```

### 3. Acceder a la Documentación
- 📚 **Swagger UI**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

### 4. Probar Endpoints
```bash
# Auth: usuario=lcmartinez, contraseña=4234
curl -u lcmartinez:4234 http://localhost:8000/customers
```

## 📚 Documentación Detallada

➡️ **[Ver documentación completa de la API](app/README.md)**

En el archivo `app/README.md` encontrarás:
- Descripción detallada de endpoints
- Ejemplos de requests/responses
- Instrucciones de testing
- Guía de despliegue
- Arquitectura del proyecto

## 🧪 Testing

```bash
# Ejecutar todos los tests
cd app
pytest -v

# Tests específicos
pytest tests/tests_customers.py -v

# Con cobertura
pytest --cov=app --cov-report=html
```

## 📖 Contenido Educativo

La carpeta `notas/` contiene ejemplos y explicaciones sobre:

| Archivo | Tema |
|---------|------|
| `fastapi.py` | Fundamentos de FastAPI |
| `autenticacion_de_http.py` | HTTP Basic Authentication |
| `validacion_de_datos.py` | Validación con Pydantic |
| `bases_de_datos.py` | Configuración de BD |
| `relaciones_en_FASTAPI.py` | ORM y relaciones |
| `middlewares.py` | Implementación de middlewares |
| `endpoints_dinamicos.py` | Rutas y parámetros |
| `pruebas_unitarias_para_crud.py` | Testing |
| `relacion_muchos_a_muchos.py` | Many-to-Many con SQLModel |
| `estructuracion_de_aplicaciones.py` | Arquitectura modular |

## 🔑 Credenciales por Defecto

```
Usuario: lcmartinez
Contraseña: 4234
```

⚠️ **Cambiar antes de producción**

## 📦 Dependencias Principales

```
fastapi[standard]==0.128.0    # Framework web
sqlmodel==0.0.31              # ORM hybrid (SQLAlchemy + Pydantic)
pytest                         # Testing (instalado implícitamente)
```

## 🎓 Temas Cubiertos

- ✅ Creación de APIs REST
- ✅ CRUD operations
- ✅ Validación de datos
- ✅ Autenticación HTTP Basic
- ✅ Manejo de relaciones (1-to-many, many-to-many)
- ✅ Middlewares personalizados
- ✅ Testing unitario
- ✅ Documentación automática (Swagger/ReDoc)
- ✅ Logging y auditoría
- ✅ Manejo de excepciones

## 🚀 Próximos Pasos

### Para Mejorar el Proyecto

- [ ] Implementar JWT en lugar de HTTP Basic
- [ ] Agregar más tests (cobertura >80%)
- [ ] Implementar paginación avanzada
- [ ] Agregar caché (Redis)
- [ ] Logging centralizado
- [ ] Rate limiting
- [ ] CORS configuración
- [ ] Validación de permisos (RBAC)
- [ ] API versioning
- [ ] CI/CD con GitHub Actions

### Para Aprender Más

- [ ] Agregar WebSockets
- [ ] Implementar Background Tasks
- [ ] Usar Alembic para migraciones
- [ ] Dockerizar la aplicación
- [ ] Deploying en producción
- [ ] Monitoreo con Prometheus

## 📝 Notas de Desarrollo

### Patrón de Routers
```python
# app/routers/ejemplo.py
from fastapi import APIRouter
from db import Sessiondep

router = APIRouter(prefix="/ejemplo", tags=["ejemplo"])

@router.get("/")
async def get_items(session: Sessiondep):
    # Implementación
    pass
```

### Patrón de Modelos
```python
# models.py
from sqlmodel import SQLModel, Field, Relationship

class Ejemplo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

### Patrón de Testing
```python
# tests.py
def test_endpoint(client, session):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

## 🤝 Contributing

1. Crea una rama: `git checkout -b feature/nueva-feature`
2. Commit cambios: `git commit -am 'Add nueva-feature'`
3. Push: `git push origin feature/nueva-feature`
4. Pull request

## 📄 Licencia

MIT License - Libre para uso educativo y comercial

## 👨‍💻 Información

- **Profesor/Autor**: Luis C. Martínez
- **Año**: 2026
- **Versión**: 1.0.0
- **Estado**: Completo y funcional

## 📞 Preguntas / Issues

Si tienes preguntas o encuentras problemas:
1. Revisa la [documentación de la API](app/README.md)
2. Consulta los archivos en `notas/`
3. Ejecuta los tests para validar

---

**Made with ❤️ for FastAPI learners**

# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! Este documento proporciona directrices para ayudarte a colaborar efectivamente.

## 📋 Tabla de Contenidos

- [Cómo Contribuir](#cómo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)
- [Guías de Estilo](#guías-de-estilo)
- [Proceso de Revisión](#proceso-de-revisión)

## 🚀 Cómo Contribuir

Hay varias maneras de contribuir al proyecto:

### 1. Reportar Bugs
Si encuentras un bug, abre una issue describiendo:
- Qué esperabas que sucediera
- Qué sucedió en realidad
- Pasos para reproducir el problema
- Información del sistema (SO, versión Python, etc.)

### 2. Sugerir Mejoras
- Documentación mejorada
- Nuevos endpoints
- Mejor manejo de errores
- Optimización de código
- Nuevos tests

### 3. Código
- Corregir bugs existentes
- Agregar nuevas características
- Mejorar tests
- Refactorización

### 4. Documentación
- Mejorar READMEs
- Agregar ejemplos
- Documentar arquitectura
- Traducir a otros idiomas

## 🐛 Reportar Bugs

### Antes de Reportar
1. Actualiza a la última versión
2. Verifica [las issues existentes](../../issues)
3. Revisa la documentación en [app/README.md](app/README.md)

### Cómo Reportar
```
Título: [BUG] Descripción breve del problema

Descripción:
- Comportamiento esperado
- Comportamiento actual
- Cómo reproducir
- Screenshots/logs si aplica

Información del Sistema:
- SO: [ej. Ubuntu 22.04]
- Python: [ej. 3.10]
- FastAPI: [ej. 0.128.0]
```

## 💡 Sugerir Mejoras

Si tienes una idea para mejorar el proyecto:

```
Título: [ENHANCEMENT] Descripción de la mejora

Descripción:
- Motivación: ¿Por qué sería útil?
- Ejemplo de uso
- Alternativas consideradas
- Contexto adicional
```

## 📝 Pull Requests

### Proceso

1. **Fork del repositorio**
   ```bash
   git clone https://github.com/tu-usuario/curso-fastapi-project.git
   cd curso-fastapi-project
   ```

2. **Crear rama**
   ```bash
   git checkout -b feature/descripcion-feature
   # o
   git checkout -b fix/descripcion-bug
   ```

3. **Hacer cambios**
   - Edita los archivos necesarios
   - Agrega tests si es apropiado
   - Actualiza documentación

4. **Commit de cambios**
   ```bash
   git add .
   git commit -m "descripción clara del cambio"
   ```

5. **Push a tu fork**
   ```bash
   git push origin feature/descripcion-feature
   ```

6. **Abrir Pull Request**
   - Ir a GitHub
   - Clic en "New Pull Request"
   - Completar el template

### Template de PR

```markdown
## Descripción
Brief description of the changes.

## Tipo de Cambio
- [ ] Bug Fix
- [ ] Nueva Feature
- [ ] Cambio Breaking
- [ ] Documentación

## ¿Cómo fue probado?
Describe los tests realizados.

## Checklist
- [ ] Mi código sigue las guías de estilo
- [ ] He agregado tests
- [ ] He actualizado la documentación
- [ ] No hay cambios en dependencias innecesarias
- [ ] Los tests locales pasan
- [ ] No hay conflictos de merge

## Issues Relacionados
Cierra #(issue number)
```

## 🎯 Guías de Estilo

### Python

Seguimos [PEP 8](https://pep8.org/):

```python
# ✅ Bien
def crear_cliente(nombre: str, email: str) -> Cliente:
    """Crear un nuevo cliente."""
    cliente = Cliente(nombre=nombre, email=email)
    session.add(cliente)
    session.commit()
    return cliente

# ❌ Mal
def CrearCliente(nombre,email):
    c=Cliente(n=nombre,e=email)
    s.add(c);s.commit()
    return c
```

### Commits

Usar Conventional Commits:

```bash
git commit -m "feat: agregar endpoint de reportes"
git commit -m "fix: resolver error en validación de email"
git commit -m "docs: actualizar README con ejemplos"
git commit -m "test: agregar tests para customers"
git commit -m "refactor: mejorar estructura de routers"
git commit -m "style: formatear código con black"
```

### Tipos de Commits

- **feat**: Nueva característica
- **fix**: Corrección de bugs
- **docs**: Cambios en documentación
- **style**: Formateo, missing semicolons, etc.
- **refactor**: Cambios que no arreglan bugs ni agregan features
- **test**: Tests nuevos o mejorados
- **chore**: Cambios en build, CI/CD, etc.

### Docstrings

```python
def obtener_cliente(cliente_id: int, session: Sessiondep) -> Cliente:
    """
    Obtener un cliente específico por ID.

    Args:
        cliente_id: ID del cliente a obtener
        session: Sesión de base de datos

    Returns:
        Cliente encontrado

    Raises:
        HTTPException: Si el cliente no existe (404)
    """
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente {cliente_id} no encontrado"
        )
    return cliente
```

### Tests

```python
# Test naming
def test_crear_cliente_exitoso() -> None:
    """Verifica que se pueda crear un cliente correctamente."""
    ...

def test_crear_cliente_sin_email_falla() -> None:
    """Verifica que la creación falle sin email."""
    ...

# Assertion clarity
assert cliente.nombre == "Juan"  # ✅
assert c.n == "Juan"  # ❌
```

## 🔄 Proceso de Revisión

### Los mantenedores revisarán tu PR

1. **Validación**: ¿Sigue las guías?
2. **Funcionalidad**: ¿Funciona correctamente?
3. **Tests**: ¿Hay cobertura?
4. **Documentación**: ¿Está actualizada?
5. **Cambios Breaking**: ¿Son necesarios?

### Feedback

- Seremos constructivos y respetuosos
- Podemos solicitar cambios
- Discutiremos en los comentarios
- Una vez aprobado, será mergeado

## ✅ Checklists

### Antes de Hacer Push

- [ ] Tests pasan localmente (`pytest`)
- [ ] Código formateado (`black app/`)
- [ ] Imports organizados (`isort app/`)
- [ ] Sin errores lint (`pylint`)
- [ ] Doctests documentados
- [ ] README actualizado si es necesario
- [ ] Sin credenciales en el código
- [ ] Commits descriptivos

### Checklist de PR

- [ ] Rama tiene un nombre descriptivo
- [ ] PR tiene descripción clara
- [ ] Links a issues relacionados
- [ ] Código no tiene conflictos
- [ ] Cambios son mínimos y enfocados
- [ ] Accesibilidad considerada

## 🏆 Reconocimientos

- Todos los contribuidores son listados en [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Los aportes significativos se mencionan en el release notes

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Pytest Docs](https://docs.pytest.org/)
- [PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 🚫 Código de Conducta

- Sé respetuoso
- Incluye a todos
- No tolera acoso
- Reporta comportamiento inapropiado

## 📞 Preguntas

Si tienes preguntas:
1. Abre una Discussion
2. Comenta en una Issue
3. Envía un email

---

**¡Gracias por contribuir!** 🎉


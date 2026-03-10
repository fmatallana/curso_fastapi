"""
Resumen
Generar pruebas automatizadas utilizando PyTest para rutas FastAPI permite identificar rápidamente errores al hacer cambios en aplicaciones. Asegurar un correcto funcionamiento en operaciones críticas como creación, lectura, edición y eliminación de un recurso, como el Customer, reduce considerablemente el riesgo de dañar módulos relacionados.

¿Por qué son importantes las pruebas automáticas en el desarrollo?

Las pruebas automáticas son fundamentales al realizar modificaciones, dado que permiten detectar de inmediato efectos no deseados de cualquier cambio en nuestro código. Con ellas podemos:

Validar rápidamente distintas funcionalidades, como creación y edición.
Identificar errores provocados indirectamente al modificar dependencias compartidas.
Realizar chequeos continuos y constantes sin verificaciones manuales exhaustivas.
Al implementar estas pruebas en las rutas específicas, como en nuestro módulo Customers, aseguramos una cobertura completa para escenarios críticos.

Utilizaremos PyTest junto con FastAPI para escribir y ejecutar pruebas en nuestro módulo Customers.

¿Cómo organizamos las pruebas en un proyecto de FastAPI?

La organización clara de pruebas es esencial para proyectos escalables:

Crea una carpeta específica para pruebas dentro del proyecto (App).
Añade un archivo __init__.py para convertirla en módulo Python.
Agrupa prueba previamente creada aquí, usando claros nombres como test-customers.py para pruebas específicas.
¿Qué pasos seguir al escribir una prueba en PyTest para FastAPI?

Para escribir pruebas claras y efectivas:

Utiliza un cliente test client que realiza peticiones HTTP a rutas FastAPI.

Realiza la petición POST a la ruta con Json válido:


response = client.post('/Customers', json={"Name": "John Doe", "Email": "sample.com", "edad": 30})
Valida códigos HTTP con assert:


assert response.status_code == status.HTTP_201_CREATED

En caso de errores por falta de status code en rutas, recuerda añadir explícitamente el status_code deseado en el decorador de la ruta:


@app.post("/customers", status_code=status.HTTP_201_CREATED)
def crear_customer():
    pass

Tras definirlo correctamente, la prueba debería pasar exitosamente.

¿Cómo se realizan pruebas para obtener recursos específicos?

Al crear pruebas para obtener recursos como un Customer específico, debes:

Crear primero el recurso mediante una prueba previa (por ejemplo, con POST).
Obtener ID del recurso recién creado.
Realizar solicitud GET específica con el ID obtenido.
Validar respuesta y código de estado correspondiente (usualmente 200).
Ejemplo práctico:


response_read = client.get(f"/customers/{customer_id}")
assert response_read.json()["Name"] == "John Doe"
assert response_read.status_code == status.HTTP_200_OK
"""

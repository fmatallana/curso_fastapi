"""
Cuando desarrollas APIs con FastAPI, proteger los datos es fundamental para garantizar la seguridad y privacidad de la información. Una forma práctica y sencilla de lograr esta protección es implementando autenticación con usuario y contraseña mediante HTTP Basic Credentials, una funcionalidad fácil de incorporar en tus endpoints.

FastAPI ofrece diversos mecanismos que te permiten asegurar tus endpoints; uno de ellos es la autenticación básica, ampliamente utilizada por su eficiencia y sencillez. Este método consiste en requerir al usuario que ingrese su usuario y contraseña, validándose con información previamente almacenada.


¿Cómo implementar HTTP Basic Credentials en tus endpoints?

Para agregar autenticación básica mediante HTTP Basic Credentials, debes seguir estos pasos:

Añadir dependencia en el endpoint: En tu código, deberás incluir Credentials como una dependencia directa en la definición del endpoint:

def root(credentials: Annotate[HTTPBasicCredentials, Depends(security)]):

Registrar y validar credenciales: Asegúrate de importar y definir correctamente todas las dependencias necesarias como Depends, Annotate, y HTTPBasic. De esta forma, FastAPI sabrá gestionar automáticamente las credenciales de usuario.

Autenticación de usuario: Utiliza las credenciales obtenidas para realizar acciones como consultar una base de datos y verificar si el usuario y la contraseña son correctos. Por ejemplo:

if credentials.username == "LC Martínez" and credentials.password == "contraseña_ejemplo":
    return {"mensaje": f"Hola, {credentials.username}"}
else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
"""
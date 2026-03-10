"""
Un endpoint estático es poco común en aplicaciones que requieren personalización. FastAPI permite recibir variables directamente en la URL, por lo que podemos modificar el endpoint para que acepte un código de país y devuelva la hora correspondiente en ese huso horario.

@app.get("/fecha/{iso_code}") se crea un nuevo app.get con el nombre fecha y el parametro iso_code
async def get_date(iso_code: str): para que el parametro funcione se debe tipar
    iso = iso_code.upper() funcion para que cualquier parametro que le pasen se convierta en mayuscula (ejemplo si pasan co = CO | Co = CO)
    timezone_str = country_timezones.get(iso) en la variable timezone_str se guarda el valor que se obtiene del iso y se busca si esta en el diccionario country_timezones
    tz = zoneinfo.ZoneInfo(timezone_str) zoneinfo es un modulo para manejar las zonas horarias precisas
    entonces si timezone_str es co, da a la perfeccion la zona horaria
    return {"hora": datetime.now(tz)} se retorna la hora actual del timezone que se paso  y se obtuvo del diccionario

"""

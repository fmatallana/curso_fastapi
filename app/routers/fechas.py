import zoneinfo
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["fehas"])


country_timezones = {
    "CO": "America/Bogota",  # Colombia
    "MX": "America/Mexico_City",  # México
    "AR": "America/Argentina/Buenos_Aires",  # Argentina
    "PE": "America/Lima",  # Perú
    "BR": "America/Sao_Paulo",  # Brasil
}


@router.get("/fecha/{iso_code}")
async def get_date(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if not timezone_str:
        return {"error": "Código de país no encontrado"}

    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"hora": datetime.now(tz)}

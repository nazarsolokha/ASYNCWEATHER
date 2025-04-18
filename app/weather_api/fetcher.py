import time
from app.weather_api.providers.weather import get_weather

def fetch_weather_for_city(city: str):
    try:
        return get_weather("openweather",city)
    except:
        return get_weather("weatherstack",city)

def get_coords(city: str):
    data = fetch_weather_for_city(city)
    if not data:
        return None

    lat = data.get("latitude") or data.get("lat")
    lon = data.get("logtitude") or data.get("lon")

    if lat is None or lon is None:
        return None

    return city, lat, lon
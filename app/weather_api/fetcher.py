from app.weather_api.providers.openweather import get_weather_openweather
from app.weather_api.providers.weatherstack import get_weather_weatherstack

def fetch_weather_for_city(city: str):
    try:
        return get_weather_openweather(city)
    except:
        return get_weather_weatherstack(city)
    
    
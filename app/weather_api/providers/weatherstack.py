import requests
import os

API_KEY = os.getenv("WEATHERAPI_KEY", "82a6ef4580d64aa69bb134610251302")

def get_weather_weatherstack(city: str) -> dict:
    url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no"

    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    return {
        "provider": "weatherstack",
        "temperature": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "description": data["current"]["condition"]["text"],
        "city": data["location"]["name"],
        "country": data["location"]["country"]
    }

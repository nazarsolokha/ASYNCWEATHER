from .worker import celery_app
from .tasks import fetch_weather_data
from .utils import normalize, regions, validators
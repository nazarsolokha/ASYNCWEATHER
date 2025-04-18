from app.tasks import fetch_weather_data
from app.worker import celery_app

if __name__ == "__main__":
    celery_app.start()
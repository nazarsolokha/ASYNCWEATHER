from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.tasks import fetch_weather_data
from app.worker import celery_app
import uuid
import os, json, glob

router = APIRouter()

# Pydantic модель для запроса
class CityRequest(BaseModel):
    cities: list[str]

# Запуск асинхронной задачи Celery
@router.post("/weather")
def post_weather(request: CityRequest):
    task_id = str(uuid.uuid4())
    task = fetch_weather_data.apply_async(args=[task_id, request.cities])  # <--- ТАК правильно
    return {"task_id": task.id}

# Получение статуса задачи Celery
@router.get("/tasks/{task_id}")
def get_weather_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {"status": "PENDING"}
    elif result.state == "FAILURE":
        return {"status": "FAILURE", "result": str(result.result)}
    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}
    else:
        return {"status": result.state, "result": str(result.result)}

# Получение сохранённых погодных данных по региону
@router.get("/results/{region}")
def get_results(region: str):
    pattern = f"weather_data/{region}/*.json"
    files = glob.glob(pattern)
    result = []

    for file in files:
        try:
            with open(file, 'r') as f:
                result += json.load(f)
        except Exception as e:
            # Ошибки чтения файла не критичны, просто логируем
            print(f"Ошибка чтения {file}: {e}")

    return result

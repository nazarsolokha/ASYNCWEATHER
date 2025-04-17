from celery import Celery
from app.worker import celery_app
import os, json, logging
from app.weather_api.fetcher import fetch_weather_for_city
from app.utils.normalize import normalize_city_name
from app.utils.validators import is_valid_temperature
from app.utils.regions import get_region

celery = Celery("tasks", broker="redis://localhost:6379/0")

# @celery.task(bind=True)
# def fetch_weather_data(self, task_id, cities):
#     results = {}
#     for city in cities:
#         norm_city = normalize_city_name(city)
#         try:
#             data = fetch_weather_for_city(norm_city)
#             temp = data.get("temperature")
#             if not is_valid_temperature(temp):
#                 continue
#             region = get_region(norm_city)
#             results.setdefault(region, []).append({
#                 "city": norm_city,
#                 "temperature": temp,
#                 "description": data.get("description"),
#             })
#         except Exception as e:
#             logging.error(f"Error fetching {city}: {e}")
#             self.update_state(state='FAILURE', meta={'error': str(e)})
#             return {'status': 'failure', 'error': str(e)}
    
#     for region, items in results.items():
#         os.makedirs(f"weather_data/{region}", exist_ok=True)
#         with open(f"weather_data/{region}/{task_id}.json", "w") as f:
#             json.dump(items, f)

#     self.update_state(state='SUCCESS', meta={'result': results})
#     return {'status': 'success', 'result': results}

@celery_app.task(name="app.tasks.fetch_weather_data")
def fetch_weather_data(task_id: str, cities: list[str]):
    try:
        print(f"[DEBUG] fetch_weather_data started with task_id={task_id} and cities={cities}")

        for city in cities:
            print(f"[DEBUG] Processing city: {city}")

            # Временно подставь мок вместо реального вызова
            # city, lat, lon = get_coords(city)  ❌ ← тут скорее всего падает
            result = get_coords(city)  # 👈 проверь, что возвращает
            print(f"[DEBUG] get_coords({city}) = {result}")

            if not result or len(result) != 3:
                raise ValueError(f"[ERROR] get_coords вернул некорректное значение для {city}: {result}")

            city, lat, lon = result
            print(f"[DEBUG] Parsed: {city=}, {lat=}, {lon=}")

        return {"message": "test run completed"}

    except Exception as e:
        import traceback
        return f"Ошибка при выполнении задачи: {e}\n{traceback.format_exc()}"

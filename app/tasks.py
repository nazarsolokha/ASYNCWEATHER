import os
import json
import logging
import traceback

from app.worker import celery_app
from app.weather_api.fetcher import fetch_weather_for_city
from app.utils.normalize import normalize_city_name
from app.utils.validators import is_valid_temperature
from app.utils.regions import get_region

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
)

@celery_app.task(name="app.tasks.fetch_weather_data")
def fetch_weather_data(task_id: str, cities: list[str]):
    logger.info(f"[START] Задача началась: {task_id} | Города: {cities}")
    results = {}

    try:
        for city in cities:
            try:
                logger.info(f"[CITY] Обработка города: {city}")
                norm_city = normalize_city_name(city)
                logger.info(f"[NORMALIZED] {city} → {norm_city}")

                data = fetch_weather_for_city(norm_city)
                temp = data.get("temperature")

                if not is_valid_temperature(temp):
                    logger.warning(f"[SKIP] Невалидная температура для {norm_city}: {temp}")
                    continue

                region = get_region(norm_city)
                results.setdefault(region, []).append({
                    "city": norm_city,
                    "temperature": temp,
                    "description": data.get("description"),
                })

                logger.info(f"[OK] {norm_city} добавлен в регион {region}")

            except Exception as e:
                logger.error(f"[ERROR] Не удалось обработать {city}: {e}")
                logger.debug(traceback.format_exc())
                continue

        # Сохранение данных по регионам
        for region, items in results.items():
            os.makedirs(f"weather_data/{region}", exist_ok=True)
            filepath = f"weather_data/{region}/{task_id}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            logger.info(f"[SAVE] Сохранено: {filepath}")

        logger.info(f"[DONE] Задача {task_id} завершена успешно")
        return {"status": "success", "result": results}

    except Exception as e:
        logger.exception("[FAILURE] Ошибка выполнения задачи")
        return {
            "status": "failure",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
    
# from app.worker import celery_app
# import os, json, logging
# from app.weather_api.fetcher import fetch_weather_for_city
# from app.utils.normalize import normalize_city_name
# from app.utils.validators import is_valid_temperature
# from app.utils.regions import get_region

# # celery = Celery("tasks", broker="redis://localhost:6379/0")

# # @celery.task(bind=True)
# # def fetch_weather_data(self, task_id, cities):
# #     results = {}
# #     for city in cities:
# #         norm_city = normalize_city_name(city)
# #         try:
# #             data = fetch_weather_for_city(norm_city)
# #             temp = data.get("temperature")
# #             if not is_valid_temperature(temp):
# #                 continue
# #             region = get_region(norm_city)
# #             results.setdefault(region, []).append({
# #                 "city": norm_city,
# #                 "temperature": temp,
# #                 "description": data.get("description"),
# #             })
# #         except Exception as e:
# #             logging.error(f"Error fetching {city}: {e}")
# #             self.update_state(state='FAILURE', meta={'error': str(e)})
# #             return {'status': 'failure', 'error': str(e)}
    
# #     for region, items in results.items():
# #         os.makedirs(f"weather_data/{region}", exist_ok=True)
# #         with open(f"weather_data/{region}/{task_id}.json", "w") as f:
# #             json.dump(items, f)

# #     self.update_state(state='SUCCESS', meta={'result': results})
# #     return {'status': 'success', 'result': results}

# @celery_app.task(name="app.tasks.fetch_weather_data")
# def fetch_weather_data(task_id: str, cities: list[str]):
#     try:
#         print(f"[DEBUG] fetch_weather_data started with task_id={task_id} and cities={cities}")

#         for city in cities:
#             print(f"[DEBUG] Processing city: {city}")

#             # Временно подставь мок вместо реального вызова
#             # city, lat, lon = get_coords(city)  ❌ ← тут скорее всего падает
#             result = get_coords(city)  # 👈 проверь, что возвращает
#             print(f"[DEBUG] get_coords({city}) = {result}")

#             if not result or len(result) != 3:
#                 raise ValueError(f"[ERROR] get_coords вернул некорректное значение для {city}: {result}")

#             city, lat, lon = result
#             print(f"[DEBUG] Parsed: {city=}, {lat=}, {lon=}")

#         return {"message": "test run completed"}

#     except Exception as e:
#         import traceback
#         return f"Ошибка при выполнении задачи: {e}\n{traceback.format_exc()}"

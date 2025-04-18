import os
import json
import logging
import traceback

from app.worker import celery_app
from app.weather_api.fetcher import fetch_weather_for_city, get_coords
from app.utils.normalize import normalize_city_name
from app.utils.validators import is_valid_temperature
from app.utils.regions import get_region
from celery import shared_task

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
)

# @shared_task(name="app.tasks.fetch_weather_data")
# def fetch_weather_data(city: str):
#     from app.weather_api.fetcher import fetch_weather_for_city
#     return fetch_weather_for_city(city)

@celery_app.task(name="app.tasks.fetch_weather_data")
def fetch_weather_data(task_id: str, cities: list[str]):
    logger.info(f"[START] Задача fetch_weather_data начата | task_id={task_id}, cities={cities}")
    results = {}

    try:
        for city in cities:
            logger.info(f"[CITY] Обработка: {city}")

            # Получение координат
            result = get_coords(city)
            #logger.info(f"[DEBUG] get_coords({city}) => {result}")
            logger.debug(f"[BEFORE UNPACK] result={result}, type={type(result)}, len={len(result) if hasattr(result, '__len__') else 'N/A'}")

            if not result or not isinstance(result, (list, tuple)) or len(result) != 3:
                logger.warning(f"[SKIP] get_coords вернул некорректные данные для '{city}': {result}")
                continue

            city, lat, lon = result
            logger.info(f"[PARSED] Город: {city}, Широта: {lat}, Долгота: {lon}")

            # Нормализация
            norm_city = normalize_city_name(city)
            logger.info(f"[NORMALIZED] {city} → {norm_city}")

            try:
                data = fetch_weather_for_city(norm_city)
                temp = data.get("temperature")

                if not is_valid_temperature(temp):
                    logger.warning(f"[SKIP] Невалидная температура у {norm_city}: {temp}")
                    continue

                region = get_region(norm_city)
                results.setdefault(region, []).append({
                    "city": norm_city,
                    "temperature": temp,
                    "description": data.get("description"),
                })

                logger.info(f"[OK] Данные по {norm_city} добавлены в регион {region}")

            except Exception as e:
                logger.error(f"[ERROR] Не удалось получить погоду для {norm_city}: {e}")
                raise

        # Сохраняем по регионам
        for region, items in results.items():
            os.makedirs(f"weather_data/{region}", exist_ok=True)
            filepath = f"weather_data/{region}/{task_id}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            logger.info(f"[WRITE] Файл сохранён: {filepath}")

        logger.info("[DONE] Задача успешно завершена")
        return {"status": "success", "result": results}

    except Exception as e:
        logger.exception("[FAILURE] Произошла ошибка при выполнении задачи")
        return {
            "status": "failure",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }

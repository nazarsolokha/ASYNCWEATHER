import re

def is_valid_temperature(temp):
    try:
        temp = float(temp)
        return -50 <= temp <= 50
    except:
        return False

def validate_city_input(city: str) -> bool:
    return re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", city) is not None

#commit

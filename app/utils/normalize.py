from difflib import get_close_matches

KNOWN_CITIES = {
    "Kyiv": ["Киев", "Kiev"],
    "Tokyo": ["Токио", "Tokio"],
    "London": ["Londn"],
    "New York": ["New York"]
}

def normalize_city_name(name: str) -> str:
    for canonical, variants in KNOWN_CITIES.items():
        if name.lower() in [v.lower() for v in variants + [canonical]]:
            return canonical
    matches = get_close_matches(name, KNOWN_CITIES.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else name


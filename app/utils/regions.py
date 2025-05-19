CITY_REGIONS = {
    "Kyiv": "Europe",
    "London": "Europe",
    "New York": "America",
    "Tokyo": "Asia"
}

def get_region(city: str) -> str:
    """
    Get the region of a city based on predefined mappings.
    """
    return CITY_REGIONS.get(city, "Unknown")

def is_valid_temperature(temp: float, region: str) -> bool:
    region_limits = {
        "europe": (-30, 45),
        "asia": (-50, 50),
        "north_america": (-40, 50),
        "south_america": (0, 45),
        "africa": (10, 55),
        "australia": (0, 50),
        "antarctica": (-90, 0),
    }
    min_temp, max_temp = region_limits.get(region.lower(), (-100, 100))
    return min_temp <= temp <= max_temp


#commit
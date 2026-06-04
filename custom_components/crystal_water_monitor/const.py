import os

DOMAIN = "crystal_water_monitor"

IS_DEV_BUILD = os.getenv("HA_CRYSTAL_DEV") == "1"

CONF_API_KEY = "api_key"
CONF_ENVIRONMENT = "environment"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 20
MIN_SCAN_INTERVAL = 15

BASE_URLS = {
    "production": "https://connect.crystalwatermonitor.app",
    "development": "https://dev.connect.crystalwatermonitor.app",
}

WATER_STATUS_MAP = {
    "blue": "Balanced",
    "orange": "Needs Attention",
    "red": "Unsafe",
    "gray": "Unknown",
}

# (reading_type, friendly_name, unit, device_class, entity_category)
READING_SENSORS: list[tuple[str, str, str | None, str | None, str | None]] = [
    ("ph", "pH", "pH", None, None),
    ("orp", "ORP", "mV", None, None),
    ("waterTemp", "Water Temperature", "°C", "temperature", None),
    ("freeChlorine", "Free Chlorine", "ppm", None, None),
    ("totalChlorine", "Total Chlorine", "ppm", None, None),
    ("totalAlkalinity", "Total Alkalinity", "ppm", None, None),
    ("totalHardness", "Total Hardness", "ppm", None, None),
    ("cyanuricAcid", "Cyanuric Acid", "ppm", None, None),
    ("bromine", "Bromine", "ppm", None, None),
    ("salt", "Salt", "ppm", None, None),
    ("totalDissolvedSolids", "Total Dissolved Solids", "ppm", None, None),
    ("phosphates", "Phosphates", "ppb", None, None),
    ("lsi", "LSI", None, None, None),
    ("battery", "Battery", "mV", None, "diagnostic"),
    ("wifiRssi", "WiFi Signal", "dBm", "signal_strength", "diagnostic"),
]

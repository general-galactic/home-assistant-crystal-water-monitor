import os

DOMAIN = "crystal_water_monitor"

IS_DEV_BUILD = os.getenv("HA_CRYSTAL_DEV") == "1"

CONF_API_KEY = "api_key"
CONF_ENVIRONMENT = "environment"

DEFAULT_SCAN_INTERVAL = 20

BASE_URLS = {
    "production": "https://connect.crystalwatermonitor.app",
    "development": "https://dev.connect.crystalwatermonitor.app",
}

WATER_STATUS_MAP = {
    "blue": "Balanced",
    "orange": "Needs Attention",
    "red": "Needs Immediate Attention",
    "gray": "Unknown",
}

# (reading_type, friendly_name, unit, device_class, entity_category, icon)
READING_SENSORS: list[tuple[str, str, str | None, str | None, str | None, str | None]] = [
    ("ph", "pH", "pH", None, None, "mdi:ph"),
    ("orp", "ORP", "mV", None, None, "mdi:lightning-bolt"),
    ("waterTemp", "Water Temperature", "°C", "temperature", None, "mdi:thermometer-water"),
    ("freeChlorine", "Free Chlorine", "ppm", None, None, "mdi:flask"),
    ("totalChlorine", "Total Chlorine", "ppm", None, None, "mdi:flask-outline"),
    ("totalAlkalinity", "Total Alkalinity", "ppm", None, None, "mdi:test-tube"),
    ("totalHardness", "Total Hardness", "ppm", None, None, "mdi:water-opacity"),
    ("cyanuricAcid", "Cyanuric Acid", "ppm", None, None, "mdi:shield-sun"),
    ("bromine", "Bromine", "ppm", None, None, "mdi:atom"),
    ("salt", "Salt", "ppm", None, None, "mdi:shaker-outline"),
    ("totalDissolvedSolids", "Total Dissolved Solids", "ppm", None, None, "mdi:water-percent"),
    ("phosphates", "Phosphates", "ppb", None, None, "mdi:leaf"),
    ("lsi", "LSI", None, None, None, "mdi:scale-balance"),
    ("battery", "Battery", "mV", None, "diagnostic", "mdi:battery"),
    ("wifiRssi", "WiFi Signal", "dBm", "signal_strength", "diagnostic", None),
]

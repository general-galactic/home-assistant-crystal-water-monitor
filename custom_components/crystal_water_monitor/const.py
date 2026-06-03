import json
import os

DOMAIN = "crystal_water_monitor"

def _is_dev_build() -> bool:
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    with open(manifest_path) as f:
        version = json.load(f).get("version", "")
    return "-" in version

IS_DEV_BUILD = _is_dev_build()

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

# (reading_type, friendly_name, unit, device_class)
READING_SENSORS: list[tuple[str, str, str | None, str | None]] = [
    ("ph", "pH", "pH", None),
    ("orp", "ORP", "mV", None),
    ("waterTemp", "Water Temperature", "°C", "temperature"),
    ("freeChlorine", "Free Chlorine", "ppm", None),
    ("totalChlorine", "Total Chlorine", "ppm", None),
    ("totalAlkalinity", "Total Alkalinity", "ppm", None),
    ("totalHardness", "Total Hardness", "ppm", None),
    ("cyanuricAcid", "Cyanuric Acid", "ppm", None),
    ("bromine", "Bromine", "ppm", None),
    ("salt", "Salt", "ppm", None),
    ("totalDissolvedSolids", "Total Dissolved Solids", "ppm", None),
    ("phosphates", "Phosphates", "ppb", None),
    ("lsi", "LSI", None, None),
    ("battery", "Battery", "%", "battery"),
    ("wifiRssi", "WiFi Signal", "dBm", "signal_strength"),
]

"""Shared fixtures for Crystal Water Monitor tests."""
from __future__ import annotations

import sys
import os

# Ensure the generated connect-api package is importable
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "custom_components",
        "crystal_water_monitor",
        "connect-api",
    ),
)

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from connect_api.models.connect_api_account_vessel_v1 import ConnectApiAccountVesselV1
from connect_api.models.connect_api_account_vessel_disc_v1 import ConnectApiAccountVesselDiscV1
from connect_api.models.connect_api_readings_v1 import ConnectAPIReadingsV1
from connect_api.models.connect_api_reading_v1 import ConnectAPIReadingV1
from connect_api.models.water_status_color import WaterStatusColor
from connect_api.models.reading_statuses import ReadingStatuses
from connect_api.models.reading_sources_v1 import ReadingSourcesV1


def make_reading(
    value: float | None = 7.4,
    status: ReadingStatuses = ReadingStatuses.OK,
    source: ReadingSourcesV1 = ReadingSourcesV1.MONITOR,
    range_from: float | None = None,
    range_to: float | None = None,
) -> ConnectAPIReadingV1:
    range_obj = None
    if range_from is not None and range_to is not None:
        range_obj = MagicMock()
        range_obj.var_from = range_from
        range_obj.to = range_to

    r = MagicMock(spec=ConnectAPIReadingV1)
    r.value = value
    r.status = status
    r.source = source
    r.var_date = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    r.status_since_date = None
    r.range = range_obj
    return r


def make_vessel(
    vessel_id: int = 1,
    name: str = "My Pool",
    vessel_type: str = "Pool",
    water_status_color: WaterStatusColor = WaterStatusColor.BLUE,
    ph_value: float | None = 7.4,
    monitor_serial: str | None = "MON-001",
    sensor_serial: str | None = "SEN-001",
    num_actions: int = 0,
) -> ConnectApiAccountVesselV1:
    disc = MagicMock(spec=ConnectApiAccountVesselDiscV1)
    disc.name = name
    disc.text = "Water looks great"
    disc.temp_c = 28.0
    disc.water_status_color = water_status_color
    disc.last_updated_date = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

    readings = MagicMock(spec=ConnectAPIReadingsV1)
    readings.ph = make_reading(value=ph_value)
    readings.orp = make_reading(value=720.0)
    readings.water_temp = make_reading(value=28.0)
    readings.free_chlorine = make_reading(value=2.5)
    readings.total_chlorine = make_reading(value=3.0)
    readings.total_alkalinity = make_reading(value=100.0)
    readings.total_hardness = make_reading(value=250.0)
    readings.cyanuric_acid = make_reading(value=40.0)
    readings.bromine = None
    readings.salt = None
    readings.total_dissolved_solids = None
    readings.phosphates = None
    readings.wifi_rssi = make_reading(value=-65.0)
    readings.battery = make_reading(value=3700.0)
    readings.smart_chlor = None
    readings.lsi = make_reading(value=0.1)
    readings.model_fields = {
        "ph": None, "orp": None, "water_temp": None, "free_chlorine": None,
        "total_alkalinity": None, "total_hardness": None, "cyanuric_acid": None,
        "lsi": None,
    }

    vessel = MagicMock(spec=ConnectApiAccountVesselV1)
    vessel.vessel_id = vessel_id
    vessel.type = vessel_type
    vessel.monitor_serial_number = monitor_serial
    vessel.sensor_serial_number = sensor_serial
    vessel.disc = disc
    vessel.readings = readings
    vessel.actions = [MagicMock() for _ in range(num_actions)]
    for a in vessel.actions:
        a.to_dict.return_value = {"type": "add_chlorine", "amount": 1.0}

    return vessel


def make_client() -> MagicMock:
    with patch("custom_components.crystal_water_monitor.api.ApiClient"):
        with patch("custom_components.crystal_water_monitor.api.DefaultApi"):
            from custom_components.crystal_water_monitor.api import CrystalApiClient
            return CrystalApiClient("test-key", "production")

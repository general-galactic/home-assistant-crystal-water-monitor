"""Tests for Crystal Water Monitor sensor entities."""
from __future__ import annotations

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from connect_api.models.water_status_color import WaterStatusColor
from connect_api.models.reading_statuses import ReadingStatuses
from connect_api.models.reading_sources_v1 import ReadingSourcesV1

from custom_components.crystal_water_monitor.sensor import (
    WaterStatusSensor,
    ActionsPendingSensor,
    LastUpdatedSensor,
    LastSyncedSensor,
    MonitorSerialSensor,
    SensorSerialSensor,
    ReadingSensor,
)

from .conftest import make_vessel, make_reading


def make_coordinator(vessel=None, inactive=False):
    coord = MagicMock()
    coord.data = vessel
    coord.inactive = inactive
    coord.last_synced = None
    coord.vessel_id = vessel.vessel_id if vessel else 1
    return coord


# ---------------------------------------------------------------------------
# WaterStatusSensor
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("color,expected", [
    (WaterStatusColor.BLUE, "Balanced"),
    (WaterStatusColor.ORANGE, "Needs Attention"),
    (WaterStatusColor.RED, "Unsafe"),
    (WaterStatusColor.GRAY, "Unknown"),
])
def test_water_status_sensor_value(color, expected):
    vessel = make_vessel(water_status_color=color)
    coord = make_coordinator(vessel)
    sensor = WaterStatusSensor(coord, 1, vessel)
    assert sensor.native_value == expected


def test_water_status_sensor_extra_attributes():
    vessel = make_vessel(num_actions=2)
    coord = make_coordinator(vessel)
    sensor = WaterStatusSensor(coord, 1, vessel)
    attrs = sensor.extra_state_attributes
    assert attrs["waterStatusColor"] == "blue"
    assert len(attrs["actions"]) == 2
    assert "name" in attrs
    assert "lastUpdatedDate" in attrs


def test_water_status_sensor_missing_vessel():
    vessel = make_vessel()
    coord = make_coordinator(vessel=None)
    sensor = WaterStatusSensor(coord, 1, vessel)
    assert sensor.native_value == "Unknown"
    assert sensor.extra_state_attributes == {}


def test_water_status_sensor_unavailable_when_inactive():
    vessel = make_vessel()
    coord = make_coordinator(vessel, inactive=True)
    sensor = WaterStatusSensor(coord, 1, vessel)
    assert sensor.available is False


def test_water_status_sensor_available_when_active():
    vessel = make_vessel()
    coord = make_coordinator(vessel, inactive=False)
    sensor = WaterStatusSensor(coord, 1, vessel)
    assert sensor.available is True


# ---------------------------------------------------------------------------
# ActionsPendingSensor
# ---------------------------------------------------------------------------

def test_actions_pending_zero():
    vessel = make_vessel(num_actions=0)
    coord = make_coordinator(vessel)
    sensor = ActionsPendingSensor(coord, 1, vessel)
    assert sensor.native_value == 0


def test_actions_pending_count():
    vessel = make_vessel(num_actions=3)
    coord = make_coordinator(vessel)
    sensor = ActionsPendingSensor(coord, 1, vessel)
    assert sensor.native_value == 3
    assert len(sensor.extra_state_attributes["actions"]) == 3


def test_actions_pending_missing_vessel():
    vessel = make_vessel()
    coord = make_coordinator(vessel=None)
    sensor = ActionsPendingSensor(coord, 1, vessel)
    assert sensor.native_value == 0
    assert sensor.extra_state_attributes == {"actions": []}


# ---------------------------------------------------------------------------
# LastUpdatedSensor
# ---------------------------------------------------------------------------

def test_last_updated_from_disc():
    vessel = make_vessel()
    ts = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    vessel.disc.last_updated_date = ts
    coord = make_coordinator(vessel)
    sensor = LastUpdatedSensor(coord, 1, vessel)
    assert sensor.native_value == ts


def test_last_updated_naive_datetime_gets_utc():
    vessel = make_vessel()
    vessel.disc.last_updated_date = None
    naive_dt = datetime(2024, 6, 1, 10, 0, 0)

    import custom_components.crystal_water_monitor.sensor as sensor_module
    original = sensor_module._last_updated
    sensor_module._last_updated = lambda v: naive_dt.isoformat()

    coord = make_coordinator(vessel)
    sensor = LastUpdatedSensor(coord, 1, vessel)
    result = sensor.native_value

    sensor_module._last_updated = original

    assert result.tzinfo == timezone.utc


def test_last_updated_missing_vessel():
    vessel = make_vessel()
    coord = make_coordinator(vessel=None)
    sensor = LastUpdatedSensor(coord, 1, vessel)
    assert sensor.native_value is None


# ---------------------------------------------------------------------------
# LastSyncedSensor
# ---------------------------------------------------------------------------

def test_last_synced_none_initially():
    vessel = make_vessel()
    coord = make_coordinator(vessel)
    coord.last_synced = None
    sensor = LastSyncedSensor(coord, 1, vessel)
    assert sensor.native_value is None


def test_last_synced_returns_coordinator_value():
    vessel = make_vessel()
    ts = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    coord = make_coordinator(vessel)
    coord.last_synced = ts
    sensor = LastSyncedSensor(coord, 1, vessel)
    assert sensor.native_value == ts


# ---------------------------------------------------------------------------
# MonitorSerialSensor / SensorSerialSensor
# ---------------------------------------------------------------------------

def test_monitor_serial():
    vessel = make_vessel(monitor_serial="MON-ABC")
    coord = make_coordinator(vessel)
    sensor = MonitorSerialSensor(coord, 1, vessel)
    assert sensor.native_value == "MON-ABC"


def test_sensor_serial():
    vessel = make_vessel(sensor_serial="SEN-XYZ")
    coord = make_coordinator(vessel)
    sensor = SensorSerialSensor(coord, 1, vessel)
    assert sensor.native_value == "SEN-XYZ"


def test_monitor_serial_missing_vessel():
    vessel = make_vessel()
    coord = make_coordinator(vessel=None)
    sensor = MonitorSerialSensor(coord, 1, vessel)
    assert sensor.native_value is None


# ---------------------------------------------------------------------------
# ReadingSensor
# ---------------------------------------------------------------------------

def _make_reading_sensor(coord, vessel_id, vessel, reading_type="ph"):
    return ReadingSensor(
        coordinator=coord,
        vessel_id=vessel_id,
        vessel_data=vessel,
        reading_type=reading_type,
        friendly_name="pH",
        unit="pH",
        device_class=None,
        entity_category=None,
        icon="mdi:ph",
    )


def test_reading_sensor_value():
    vessel = make_vessel(ph_value=7.4)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.native_value == 7.4


def test_reading_sensor_rounds_to_2_decimal_places():
    vessel = make_vessel()
    vessel.readings.ph = make_reading(value=7.456789)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.native_value == 7.46


def test_reading_sensor_range_midpoint():
    vessel = make_vessel()
    vessel.readings.ph = make_reading(value=None, range_from=7.2, range_to=7.8)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.native_value == 7.5


def test_reading_sensor_none_when_no_value_or_range():
    vessel = make_vessel()
    r = make_reading(value=None)
    r.range = None
    vessel.readings.ph = r
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.native_value is None


def test_reading_sensor_unavailable_when_no_reading():
    vessel = make_vessel()
    vessel.readings.ph = None
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.available is False


def test_reading_sensor_unavailable_when_inactive():
    vessel = make_vessel()
    coord = make_coordinator(vessel, inactive=True)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.available is False


def test_reading_sensor_available_when_reading_present():
    vessel = make_vessel(ph_value=7.2)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.available is True


def test_reading_sensor_extra_attributes():
    vessel = make_vessel()
    r = make_reading(value=7.4, status=ReadingStatuses.OK, source=ReadingSourcesV1.MONITOR)
    r.status_since_date = None
    r.range = None
    vessel.readings.ph = r
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    attrs = sensor.extra_state_attributes
    assert attrs["status"] == "ok"
    assert attrs["source"] == "monitor"
    assert "date" in attrs


def test_reading_sensor_ranged_attribute_set():
    vessel = make_vessel()
    vessel.readings.ph = make_reading(value=None, range_from=7.0, range_to=7.6)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 1, vessel)
    attrs = sensor.extra_state_attributes
    assert attrs.get("is_ranged") is True
    assert attrs["range_low"] == 7.0
    assert attrs["range_high"] == 7.6


def test_reading_sensor_camelcase_to_snake():
    vessel = make_vessel()
    coord = make_coordinator(vessel)
    sensor = ReadingSensor(
        coordinator=coord,
        vessel_id=1,
        vessel_data=vessel,
        reading_type="waterTemp",
        friendly_name="Water Temperature",
        unit="°C",
        device_class="temperature",
        entity_category=None,
    )
    assert sensor.native_value == 28.0


def test_reading_sensor_unique_id():
    vessel = make_vessel(vessel_id=5)
    coord = make_coordinator(vessel)
    sensor = _make_reading_sensor(coord, 5, vessel, reading_type="orp")
    assert sensor._attr_unique_id == "5_orp"


def test_reading_sensor_missing_vessel_returns_none():
    vessel = make_vessel()
    coord = make_coordinator(vessel=None)
    sensor = _make_reading_sensor(coord, 1, vessel)
    assert sensor.native_value is None
    assert sensor.extra_state_attributes == {}

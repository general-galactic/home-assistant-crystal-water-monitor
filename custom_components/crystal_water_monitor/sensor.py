from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import ConnectApiAccountVesselV1, ConnectAPIReadingV1
from .const import DOMAIN, READING_SENSORS, WATER_STATUS_MAP
from .coordinator import CrystalDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CrystalDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for vessel_id, vessel_data in coordinator.vessel_data.items():
        entities.append(WaterStatusSensor(coordinator, vessel_id, vessel_data))
        entities.append(ActionsPendingSensor(coordinator, vessel_id, vessel_data))
        entities.append(LastUpdatedSensor(coordinator, vessel_id, vessel_data))
        entities.append(LastSyncedSensor(coordinator, vessel_id, vessel_data))
        for reading_type, name, unit, device_class, entity_category in READING_SENSORS:
            entities.append(
                ReadingSensor(coordinator, vessel_id, vessel_data, reading_type, name, unit, device_class, entity_category)
            )

    async_add_entities(entities)


def _last_updated(vessel: ConnectApiAccountVesselV1) -> str | None:
    if vessel.disc.last_updated_date:
        return vessel.disc.last_updated_date.isoformat()
    for field in vessel.readings.model_fields:
        r = getattr(vessel.readings, field, None)
        if r is not None and r.var_date:
            return r.var_date.isoformat()
    return None


_VESSEL_TYPE_ICON = {
    "Pool": "mdi:pool",
    "Hot Tub": "mdi:hot-tub",
    "Swim Spa": "mdi:pool",
}


def _vessel_icon(vessel_data: ConnectApiAccountVesselV1) -> str:
    return _VESSEL_TYPE_ICON.get(vessel_data.type, "mdi:pool")


def _device_info(vessel_data: ConnectApiAccountVesselV1) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, str(vessel_data.vessel_id))},
        name=vessel_data.disc.name,
        manufacturer="Crystal Water Monitor",
        model=vessel_data.type,
        configuration_url="https://www.crystalwatermonitor.com",
    )


class CrystalSensorBase(CoordinatorEntity[CrystalDataUpdateCoordinator], SensorEntity):
    def __init__(
        self,
        coordinator: CrystalDataUpdateCoordinator,
        vessel_id: int,
        vessel_data: ConnectApiAccountVesselV1,
    ) -> None:
        super().__init__(coordinator)
        self._vessel_id = vessel_id
        self._attr_device_info = _device_info(vessel_data)
        self._attr_icon = _vessel_icon(vessel_data)

    @property
    def _vessel(self) -> ConnectApiAccountVesselV1 | None:
        return self.coordinator.vessel_data.get(self._vessel_id)


class WaterStatusSensor(CrystalSensorBase):
    _attr_icon = "mdi:water-check"

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_water_status"
        self._attr_name = f"{vessel_data.disc.name} Water Status"

    @property
    def native_value(self) -> str:
        vessel = self._vessel
        color = vessel.disc.water_status_color.value if vessel else "gray"
        return WATER_STATUS_MAP.get(color, "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        vessel = self._vessel
        if not vessel:
            return {}
        disc = vessel.disc
        return {
            "name": disc.name,
            "text": disc.text,
            "tempC": disc.temp_c,
            "lastUpdatedDate": _last_updated(vessel),
            "monitorSerialNumber": disc.monitor_serial_number,
            "sensorSerialNumber": disc.sensor_serial_number,
            "waterStatusColor": disc.water_status_color.value,
            "actions": [a.to_dict() for a in vessel.actions],
        }


class ActionsPendingSensor(CrystalSensorBase):
    _attr_icon = "mdi:clipboard-list"
    _attr_native_unit_of_measurement = None

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_actions_pending"
        self._attr_name = f"{vessel_data.disc.name} Actions Pending"

    @property
    def native_value(self) -> int:
        vessel = self._vessel
        return len(vessel.actions) if vessel else 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        vessel = self._vessel
        return {"actions": [a.to_dict() for a in vessel.actions] if vessel else []}


class LastUpdatedSensor(CrystalSensorBase):
    _attr_icon = "mdi:clock-outline"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_last_updated"
        self._attr_name = f"{vessel_data.disc.name} Last Updated"

    @property
    def native_value(self):
        vessel = self._vessel
        if not vessel:
            return None
        iso = _last_updated(vessel)
        if not iso:
            return None
        dt = datetime.fromisoformat(iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt


class LastSyncedSensor(CrystalSensorBase):
    _attr_icon = "mdi:cloud-check-outline"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_last_synced"
        self._attr_name = f"{vessel_data.disc.name} Last Synced"

    @property
    def native_value(self) -> datetime | None:
        return self.coordinator.last_synced


class ReadingSensor(CrystalSensorBase):
    def __init__(
        self,
        coordinator: CrystalDataUpdateCoordinator,
        vessel_id: int,
        vessel_data: ConnectApiAccountVesselV1,
        reading_type: str,
        friendly_name: str,
        unit: str | None,
        device_class: str | None,
        entity_category: str | None,
    ) -> None:
        super().__init__(coordinator, vessel_id, vessel_data)
        self._reading_type = reading_type
        self._attr_unique_id = f"{vessel_id}_{reading_type}"
        self._attr_name = f"{vessel_data.disc.name} {friendly_name}"
        self._attr_native_unit_of_measurement = unit
        if device_class:
            try:
                self._attr_device_class = SensorDeviceClass(device_class)
            except ValueError:
                pass
        if entity_category:
            self._attr_entity_category = EntityCategory(entity_category)

    @property
    def _reading(self) -> ConnectAPIReadingV1 | None:
        vessel = self._vessel
        if not vessel:
            return None
        # pydantic converts camelCase aliases to snake_case attribute names
        attr = re.sub(r'(?<!^)(?=[A-Z])', '_', self._reading_type).lower()
        return getattr(vessel.readings, attr, None)

    @property
    def native_value(self) -> float | None:
        r = self._reading
        if r is None:
            return None
        if r.value is not None:
            return round(r.value, 2)
        if r.range is not None and r.range.var_from is not None and r.range.to is not None:
            return round((r.range.var_from + r.range.to) / 2, 2)
        return None

    @property
    def available(self) -> bool:
        return self._reading is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        r = self._reading
        if r is None:
            return {}
        attrs: dict[str, Any] = {
            "status": r.status.value if r.status else None,
            "source": r.source.value if r.source else None,
            "date": r.var_date.isoformat() if r.var_date else None,
            "status_since": r.status_since_date.isoformat() if r.status_since_date else None,
        }
        if r.range is not None:
            attrs["range_low"] = r.range.var_from
            attrs["range_high"] = r.range.to
        if r.value is None and r.range is not None:
            attrs["is_ranged"] = True
        return attrs

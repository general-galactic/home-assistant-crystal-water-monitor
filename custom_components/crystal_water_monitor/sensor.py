from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        for reading_type, name, unit, device_class in READING_SENSORS:
            entities.append(
                ReadingSensor(coordinator, vessel_id, vessel_data, reading_type, name, unit, device_class)
            )

    async_add_entities(entities)


_VESSEL_TYPE_ICON = {
    "Pool": "mdi:pool",
    "Hot Tub": "mdi:hot-tub",
    "Swim Spa": "mdi:pool",
}


def _vessel_icon(vessel_data: dict) -> str:
    return _VESSEL_TYPE_ICON.get(vessel_data.get("type", ""), "mdi:pool")


def _device_info(vessel_data: dict) -> DeviceInfo:
    vessel_id = vessel_data["vesselId"]
    return DeviceInfo(
        identifiers={(DOMAIN, str(vessel_id))},
        name=vessel_data.get("disc", {}).get("name", f"Vessel {vessel_id}"),
        manufacturer="Crystal Water Monitor",
        model=vessel_data.get("type", "Pool Monitor"),
    )


class CrystalSensorBase(CoordinatorEntity[CrystalDataUpdateCoordinator], SensorEntity):
    def __init__(
        self,
        coordinator: CrystalDataUpdateCoordinator,
        vessel_id: int,
        vessel_data: dict,
    ) -> None:
        super().__init__(coordinator)
        self._vessel_id = vessel_id
        self._attr_device_info = _device_info(vessel_data)
        self._attr_icon = _vessel_icon(vessel_data)

    @property
    def _vessel(self) -> dict:
        return self.coordinator.vessel_data.get(self._vessel_id, {})


class WaterStatusSensor(CrystalSensorBase):
    _attr_icon = "mdi:water-check"

    def __init__(self, coordinator, vessel_id, vessel_data):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_water_status"
        self._attr_name = f"{vessel_data.get('disc', {}).get('name', 'Vessel')} Water Status"

    @property
    def native_value(self) -> str:
        color = self._vessel.get("disc", {}).get("waterStatusColor", "gray")
        return WATER_STATUS_MAP.get(color, "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        disc = self._vessel.get("disc", {})
        return {
            "last_updated_text": disc.get("lastUpdatedText"),
            "status_text": disc.get("text"),
            "actions": self._vessel.get("actions", []),
        }


class ActionsPendingSensor(CrystalSensorBase):
    _attr_icon = "mdi:clipboard-list"
    _attr_native_unit_of_measurement = None

    def __init__(self, coordinator, vessel_id, vessel_data):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_actions_pending"
        name = vessel_data.get("disc", {}).get("name", "Vessel")
        self._attr_name = f"{name} Actions Pending"

    @property
    def native_value(self) -> int:
        return len(self._vessel.get("actions", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"actions": self._vessel.get("actions", [])}


class ReadingSensor(CrystalSensorBase):
    def __init__(
        self,
        coordinator: CrystalDataUpdateCoordinator,
        vessel_id: int,
        vessel_data: dict,
        reading_type: str,
        friendly_name: str,
        unit: str | None,
        device_class: str | None,
    ) -> None:
        super().__init__(coordinator, vessel_id, vessel_data)
        self._reading_type = reading_type
        self._attr_unique_id = f"{vessel_id}_{reading_type}"
        vessel_name = vessel_data.get("disc", {}).get("name", "Vessel")
        self._attr_name = f"{vessel_name} {friendly_name}"
        self._attr_native_unit_of_measurement = unit
        if device_class:
            try:
                self._attr_device_class = SensorDeviceClass(device_class)
            except ValueError:
                pass

    @property
    def _reading(self) -> dict:
        return self._vessel.get("readings", {}).get(self._reading_type, {})

    @property
    def native_value(self) -> float | None:
        r = self._reading
        if "value" in r:
            return r["value"]
        rng = r.get("range")
        if rng and "low" in rng and "high" in rng:
            return (rng["low"] + rng["high"]) / 2
        return None

    @property
    def available(self) -> bool:
        return bool(self._reading)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        r = self._reading
        if not r:
            return {}
        attrs: dict[str, Any] = {
            "status": r.get("status"),
            "source": r.get("source"),
            "date": r.get("date"),
            "status_since": r.get("statusSinceDate"),
        }
        if rng := r.get("range"):
            attrs["range_low"] = rng.get("low")
            attrs["range_high"] = rng.get("high")
        if "value" not in r and "range" in r:
            attrs["is_ranged"] = True
        vessel_actions = self._vessel.get("actions", [])
        if vessel_actions:
            attrs["actions"] = vessel_actions
        return attrs

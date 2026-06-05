from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import ConnectApiAccountVesselV1, ConnectAPIReadingV1
from .const import DOMAIN, READING_SENSORS, WATER_STATUS_MAP
from .coordinator import CrystalVesselCoordinator

_LOGGER = logging.getLogger(__name__)


def _entities_for_vessel(
    coordinator: CrystalVesselCoordinator,
    vessel_id: int,
    vessel_data,
) -> list[SensorEntity]:
    entities: list[SensorEntity] = [
        WaterStatusSensor(coordinator, vessel_id, vessel_data),
        ActionsPendingSensor(coordinator, vessel_id, vessel_data),
        LastUpdatedSensor(coordinator, vessel_id, vessel_data),
        LastSyncedSensor(coordinator, vessel_id, vessel_data),
        MonitorSerialSensor(coordinator, vessel_id, vessel_data),
        SensorSerialSensor(coordinator, vessel_id, vessel_data),
    ]
    for reading_type, name, unit, device_class, entity_category, icon in READING_SENSORS:
        entities.append(
            ReadingSensor(coordinator, vessel_id, vessel_data, reading_type, name, unit, device_class, entity_category, icon)
        )
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinators: dict[int, CrystalVesselCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    registry = er.async_get(hass)
    entities: list[SensorEntity] = []

    for vessel_id, coordinator in coordinators.items():
        if coordinator.data is not None:
            entities.extend(_entities_for_vessel(coordinator, vessel_id, coordinator.data))
            entry.async_on_unload(
                coordinator.async_add_listener(
                    lambda c=coordinator: _sync_vessel_disabled(registry, entry, c)
                )
            )

    async_add_entities(entities)


def _sync_vessel_disabled(
    registry: er.EntityRegistry,
    entry: ConfigEntry,
    coordinator: CrystalVesselCoordinator,
) -> None:
    for entity_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
        if _vessel_id_from_unique_id(entity_entry.unique_id) != coordinator.vessel_id:
            continue
        currently_disabled = entity_entry.disabled_by == er.RegistryEntryDisabler.INTEGRATION
        if coordinator.inactive and not currently_disabled:
            registry.async_update_entity(
                entity_entry.entity_id,
                disabled_by=er.RegistryEntryDisabler.INTEGRATION,
            )
        elif not coordinator.inactive and currently_disabled:
            registry.async_update_entity(
                entity_entry.entity_id,
                disabled_by=None,
            )


def _vessel_id_from_unique_id(unique_id: str | None) -> int | None:
    if not unique_id:
        return None
    try:
        return int(unique_id.split("_")[0])
    except (ValueError, IndexError):
        return None


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
    disc = vessel_data.disc
    return DeviceInfo(
        identifiers={(DOMAIN, str(vessel_data.vessel_id))},
        name=disc.name,
        manufacturer="Crystal Water Monitor",
        model=vessel_data.type,
        serial_number=vessel_data.monitor_serial_number,
        configuration_url="https://www.crystalwatermonitor.com",
    )


class CrystalSensorBase(CoordinatorEntity[CrystalVesselCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrystalVesselCoordinator,
        vessel_id: int,
        vessel_data: ConnectApiAccountVesselV1,
    ) -> None:
        super().__init__(coordinator)
        self._vessel_id = vessel_id
        self._initial_vessel_data = vessel_data
        if not self.__class__.__dict__.get("_attr_icon"):
            self._attr_icon = _vessel_icon(vessel_data)

    @property
    def device_info(self) -> DeviceInfo:
        vessel = self.coordinator.data or self._initial_vessel_data
        return _device_info(vessel)

    @property
    def _vessel(self) -> ConnectApiAccountVesselV1 | None:
        return self.coordinator.data

    @property
    def available(self) -> bool:
        return not self.coordinator.inactive and self.coordinator.data is not None


class WaterStatusSensor(CrystalSensorBase):
    _attr_icon = "mdi:water-check"

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_water_status"
        self._attr_name = "Water Status"

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
            "waterStatusColor": disc.water_status_color.value,
            "vesselId": self._vessel_id,
            "actions": [a.to_dict() for a in vessel.actions],
        }


class ActionsPendingSensor(CrystalSensorBase):
    _attr_icon = "mdi:clipboard-list"
    _attr_native_unit_of_measurement = None

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_actions_pending"
        self._attr_name = "Actions Pending"

    @property
    def native_value(self) -> int:
        vessel = self._vessel
        return len(vessel.actions) if vessel else 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        vessel = self._vessel
        return {"actions": [a.to_dict() for a in vessel.actions] if vessel else []}


class LastUpdatedSensor(CrystalSensorBase):
    _attr_icon = "mdi:history"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_last_updated"
        self._attr_name = "Last Updated"

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
    _attr_icon = "mdi:cloud-sync-outline"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_last_synced"
        self._attr_name = "Last Synced"

    @property
    def native_value(self) -> datetime | None:
        return self.coordinator.last_synced


class MonitorSerialSensor(CrystalSensorBase):
    _attr_icon = "mdi:barcode"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_monitor_serial"
        self._attr_name = "Monitor Serial"

    @property
    def native_value(self) -> str | None:
        vessel = self._vessel
        return vessel.monitor_serial_number if vessel else None


class SensorSerialSensor(CrystalSensorBase):
    _attr_icon = "mdi:barcode-scan"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, vessel_id, vessel_data: ConnectApiAccountVesselV1):
        super().__init__(coordinator, vessel_id, vessel_data)
        self._attr_unique_id = f"{vessel_id}_sensor_serial"
        self._attr_name = "Sensor Serial"

    @property
    def native_value(self) -> str | None:
        vessel = self._vessel
        return vessel.sensor_serial_number if vessel else None


class ReadingSensor(CrystalSensorBase):
    def __init__(
        self,
        coordinator: CrystalVesselCoordinator,
        vessel_id: int,
        vessel_data: ConnectApiAccountVesselV1,
        reading_type: str,
        friendly_name: str,
        unit: str | None,
        device_class: str | None,
        entity_category: str | None,
        icon: str | None = None,
    ) -> None:
        super().__init__(coordinator, vessel_id, vessel_data)
        self._reading_type = reading_type
        self._attr_unique_id = f"{vessel_id}_{reading_type}"
        self._attr_name = friendly_name
        self._attr_native_unit_of_measurement = unit
        if icon:
            self._attr_icon = icon
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
        return not self.coordinator.inactive and self._reading is not None

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

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import CrystalVesselCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinators: dict[int, CrystalVesselCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    entities = [
        ForcePollButton(coordinator)
        for coordinator in coordinators.values()
        if coordinator.data is not None
    ]
    async_add_entities(entities)


class ForcePollButton(ButtonEntity):
    def __init__(self, coordinator: CrystalVesselCoordinator) -> None:
        self._coordinator = coordinator
        vessel_id = coordinator.vessel_id
        vessel_name = coordinator.data.disc.name if coordinator.data else str(vessel_id)
        self._attr_unique_id = f"{DOMAIN}_{vessel_id}_force_poll"
        self._attr_name = f"{vessel_name} Force Poll"
        self._attr_icon = "mdi:refresh"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(vessel_id))},
        )

    async def async_press(self) -> None:
        await self._coordinator.async_request_refresh()

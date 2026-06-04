from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import ConnectApiAccountVesselV1
from .const import DOMAIN
from .coordinator import CrystalDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CrystalDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        ForcePollButton(coordinator, vessel_id, vessel_data)
        for vessel_id, vessel_data in coordinator.vessel_data.items()
    ]
    async_add_entities(entities)


class ForcePollButton(ButtonEntity):
    def __init__(
        self,
        coordinator: CrystalDataUpdateCoordinator,
        vessel_id: int,
        vessel_data: ConnectApiAccountVesselV1,
    ) -> None:
        self._coordinator = coordinator
        self._vessel_id = vessel_id
        vessel_name = vessel_data.disc.name
        self._attr_unique_id = f"{DOMAIN}_{vessel_id}_force_poll"
        self._attr_name = f"{vessel_name} Force Poll"
        self._attr_icon = "mdi:refresh"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(vessel_id))},
        )

    async def async_press(self) -> None:
        await self._coordinator.async_request_refresh()

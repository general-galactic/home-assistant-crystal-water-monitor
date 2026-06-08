from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_API_KEY, DOMAIN
from .coordinator import CrystalVesselCoordinator

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    coordinators: dict[int, CrystalVesselCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]

    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "entry_options": async_redact_data(dict(entry.options), TO_REDACT),
        "vessels": {
            str(vessel_id): {
                "inactive": coordinator.inactive,
                "last_synced": coordinator.last_synced.isoformat() if coordinator.last_synced else None,
                "data": coordinator.data.to_dict() if coordinator.data else None,
            }
            for vessel_id, coordinator in coordinators.items()
        },
    }

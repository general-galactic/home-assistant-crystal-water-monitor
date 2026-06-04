from __future__ import annotations

from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CrystalApiClient
from .const import (
    CONF_API_KEY,
    CONF_ENVIRONMENT,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    IS_DEV_BUILD,
)
from .coordinator import CrystalDataUpdateCoordinator

PLATFORMS = ["sensor", "button"] if IS_DEV_BUILD else ["sensor"]

_WWW_DIR = Path(__file__).parent / "www"
_LOVELACE_RESOURCE = "/crystal_water_monitor/crystal-disc-card.js"


def _get_config(entry: ConfigEntry) -> dict:
    """Merge entry data with options, options taking precedence."""
    return {**entry.data, **entry.options}


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.http.register_static_path(
        _LOVELACE_RESOURCE,
        str(_WWW_DIR / "crystal-disc-card.js"),
        cache_headers=False,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    config = _get_config(entry)
    session = async_get_clientsession(hass)
    client = CrystalApiClient(
        api_key=config[CONF_API_KEY],
        environment=config.get(CONF_ENVIRONMENT, "production"),
        session=session,
    )
    coordinator = CrystalDataUpdateCoordinator(
        hass=hass,
        client=client,
        scan_interval=config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry when options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

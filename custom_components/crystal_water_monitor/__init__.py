from __future__ import annotations

import logging
from pathlib import Path

_LOGGER = logging.getLogger(__name__)

from homeassistant.components.http import StaticPathConfig

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


async def _async_register_lovelace_resource(hass: HomeAssistant) -> None:
    try:
        from homeassistant.components.lovelace.const import LOVELACE_DATA  # noqa: PLC0415
        from homeassistant.components.lovelace.resources import ResourceStorageCollection  # noqa: PLC0415

        lovelace_data = hass.data.get(LOVELACE_DATA)
        if lovelace_data is None:
            _LOGGER.warning("Lovelace not loaded yet, skipping resource registration")
            return

        resource_collection = lovelace_data.resources
        if not isinstance(resource_collection, ResourceStorageCollection):
            _LOGGER.debug("Lovelace in YAML mode, skipping resource registration")
            return

        existing_urls = {r["url"] for r in resource_collection.async_items()}
        if _LOVELACE_RESOURCE not in existing_urls:
            await resource_collection.async_create_item(
                {"res_type": "module", "url": _LOVELACE_RESOURCE}
            )
            _LOGGER.info("Registered Lovelace resource: %s", _LOVELACE_RESOURCE)
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Could not register Lovelace resource: %s", err)


def _get_config(entry: ConfigEntry) -> dict:
    """Merge entry data with options, options taking precedence."""
    return {**entry.data, **entry.options}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if not hass.data.get(f"{DOMAIN}_www_registered"):
        await hass.http.async_register_static_paths([
            StaticPathConfig(
                _LOVELACE_RESOURCE,
                str(_WWW_DIR / "crystal-disc-card.js"),
                cache_headers=False,
            ),
            *[
                StaticPathConfig(
                    f"/crystal_water_monitor/{name}",
                    str(_WWW_DIR / name),
                    cache_headers=True,
                )
                for name in ["disc-blue.svg", "disc-orange.svg", "disc-red.svg", "disc-gray.svg", "CWM_icon_wordmark_white.svg", "CWM_icon_wordmark_color.svg"]
            ],
        ])
        await _async_register_lovelace_resource(hass)
        hass.data[f"{DOMAIN}_www_registered"] = True
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

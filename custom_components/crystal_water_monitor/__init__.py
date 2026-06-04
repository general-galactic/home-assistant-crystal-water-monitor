from __future__ import annotations

import json
import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import CrystalApiClient
from .const import (
    CONF_API_KEY,
    CONF_ENVIRONMENT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    IS_DEV_BUILD,
)
from .coordinator import CrystalDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "button"] if IS_DEV_BUILD else ["sensor"]

_WWW_DIR = Path(__file__).parent / "www"

try:
    _VERSION = json.loads((Path(__file__).parent / "manifest.json").read_text())["version"]
except Exception:  # noqa: BLE001
    _VERSION = "0"

_LOVELACE_URL = f"/crystal_water_monitor/crystal-custom-cards.js?v={_VERSION}"


async def _async_register_lovelace_resource(hass: HomeAssistant) -> None:
    try:
        import homeassistant.components.lovelace.const as _lovelace_const  # noqa: PLC0415
        from homeassistant.components.lovelace.resources import (
            ResourceStorageCollection,  # noqa: PLC0415
        )

        LOVELACE_DATA = getattr(_lovelace_const, "LOVELACE_DATA", None)
        if LOVELACE_DATA is None:
            _LOGGER.debug("LOVELACE_DATA not available, skipping resource registration")
            return
        lovelace_data = hass.data.get(LOVELACE_DATA)
        if lovelace_data is None:
            _LOGGER.warning("Lovelace not loaded yet, skipping resource registration")
            return

        resource_collection = lovelace_data.resources
        if not isinstance(resource_collection, ResourceStorageCollection):
            _LOGGER.debug("Lovelace in YAML mode, skipping resource registration")
            return

        await resource_collection.async_load()

        url = _LOVELACE_URL

        all_items = list(resource_collection.async_items())
        mine = [i for i in all_items if "crystal_water_monitor/crystal" in i["url"]]
        correct = [i for i in mine if i["url"] == url]

        if len(correct) == 1 and len(mine) == 1:
            return

        for item in mine:
            await resource_collection.async_delete_item(item["id"])

        await resource_collection.async_create_item({"res_type": "module", "url": url})
        _LOGGER.info("Registered Lovelace resource: %s", url)
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Could not register Lovelace resource: %s", err)


def _get_config(entry: ConfigEntry) -> dict:
    """Merge entry data with options, options taking precedence."""
    return {**entry.data, **entry.options}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    if not hass.data.get(f"{DOMAIN}_static_registered"):
        hass.data[f"{DOMAIN}_static_registered"] = True
        await hass.http.async_register_static_paths([
            StaticPathConfig(
                "/crystal_water_monitor/crystal-custom-cards.js",
                str(_WWW_DIR / "crystal-custom-cards.js"),
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
    config = _get_config(entry)
    client = await hass.async_add_executor_job(
        lambda: CrystalApiClient(
            api_key=config[CONF_API_KEY],
            environment=config.get(CONF_ENVIRONMENT, "production"),
            locale=hass.config.language,
        )
    )
    coordinator = CrystalDataUpdateCoordinator(
        hass=hass,
        client=client,
        scan_interval=DEFAULT_SCAN_INTERVAL,
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
        coordinator: CrystalDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.client.close()
    return unload_ok

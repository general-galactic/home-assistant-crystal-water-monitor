from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CrystalApiClient, CrystalApiError, CrystalAuthError, CrystalNotFoundError
from .const import (
    CONF_API_KEY,
    CONF_ENVIRONMENT,
    DOMAIN,
    IS_DEV_BUILD,
)

API_KEY_HELP_URL = "https://www.crystalwatermonitor.app/api-key"


def _user_schema(show_env: bool) -> vol.Schema:
    fields: dict = {
        vol.Required(CONF_API_KEY): str,
    }
    if show_env:
        fields[vol.Required(CONF_ENVIRONMENT, default="production")] = vol.In(
            ["production", "development"]
        )
    return vol.Schema(fields)


def _options_schema(current: dict, show_env: bool) -> vol.Schema:
    fields: dict = {
        vol.Required(CONF_API_KEY, default=current.get(CONF_API_KEY, "")): str,
    }
    if show_env:
        fields[vol.Required(CONF_ENVIRONMENT, default=current.get(CONF_ENVIRONMENT, "production"))] = vol.In(
            ["production", "development"]
        )
    return vol.Schema(fields)


async def _validate_api_key(hass, api_key: str, environment: str) -> str | None:
    """Returns an error key string on failure, None on success."""
    session = async_get_clientsession(hass)
    client = CrystalApiClient(api_key=api_key, environment=environment, session=session)
    try:
        await client.list_vessels()
    except CrystalAuthError:
        return "invalid_auth"
    except CrystalNotFoundError:
        return "no_subscription"
    except CrystalApiError:
        return "cannot_connect"
    except Exception:  # noqa: BLE001
        return "unknown"
    return None


class CrystalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            environment = user_input.get(CONF_ENVIRONMENT, "production")
            error = await _validate_api_key(self.hass, user_input[CONF_API_KEY], environment)
            if error:
                errors["base"] = error
            else:
                data = dict(user_input)
                data.setdefault(CONF_ENVIRONMENT, "production")
                await self.async_set_unique_id(user_input[CONF_API_KEY])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Crystal Water Monitor", data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=_user_schema(IS_DEV_BUILD),
            description_placeholders={"api_key_url": API_KEY_HELP_URL},
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return CrystalOptionsFlow(config_entry)


class CrystalOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        errors: dict[str, str] = {}
        current = {**self._entry.data, **self._entry.options}

        if user_input is not None:
            environment = user_input.get(CONF_ENVIRONMENT, current.get(CONF_ENVIRONMENT, "production"))
            error = await _validate_api_key(self.hass, user_input[CONF_API_KEY], environment)
            if error:
                errors["base"] = error
            else:
                options = dict(user_input)
                options.setdefault(CONF_ENVIRONMENT, current.get(CONF_ENVIRONMENT, "production"))
                return self.async_create_entry(title="", data=options)

        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(current, IS_DEV_BUILD),
            description_placeholders={"api_key_url": API_KEY_HELP_URL},
            errors=errors,
        )

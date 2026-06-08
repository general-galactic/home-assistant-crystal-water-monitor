from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    ConnectApiAccountVesselV1,
    CrystalApiClient,
    CrystalApiError,
    CrystalAuthError,
    CrystalMaintenanceError,
    CrystalNotFoundError,
    CrystalRateLimitError,
    CrystalSubscriptionError,
)

_LOGGER = logging.getLogger(__name__)


class CrystalVesselCoordinator(DataUpdateCoordinator[ConnectApiAccountVesselV1 | None]):
    """Fetches data for a single vessel."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: CrystalApiClient,
        vessel_id: int,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"Crystal Water Monitor vessel {vessel_id}",
            update_interval=timedelta(minutes=scan_interval),
        )
        self.client = client
        self.vessel_id = vessel_id
        self.inactive = False
        self.auth_failed = False
        self.last_synced: datetime | None = None

    async def _async_update_data(self) -> ConnectApiAccountVesselV1 | None:
        _LOGGER.debug(
            "Polling vessel %s (env=%s, key_prefix=%s...)",
            self.vessel_id,
            self.client.environment,
            self.client.key_prefix,
        )
        try:
            data = await self.client.get_vessel(self.vessel_id)
            _LOGGER.debug("Poll succeeded for vessel %s", self.vessel_id)
            self.inactive = False
            self.auth_failed = False
            self.last_synced = datetime.now(timezone.utc)
            return data
        except CrystalAuthError as err:
            _LOGGER.warning(
                "Auth error fetching vessel %s (env=%s, key_prefix=%s...): %s; triggering reauth",
                self.vessel_id,
                self.client.environment,
                self.client.key_prefix,
                err,
            )
            self.auth_failed = True
            raise ConfigEntryAuthFailed("Crystal API rejected the configured API key") from err
        except CrystalNotFoundError:
            _LOGGER.warning("Vessel %s not found; marking inactive", self.vessel_id)
            self.inactive = True
            return self.data
        except CrystalSubscriptionError:
            _LOGGER.debug("Vessel %s has no active subscription; marking inactive", self.vessel_id)
            self.inactive = True
            return self.data
        except CrystalRateLimitError:
            _LOGGER.warning("Rate limit hit fetching vessel %s; keeping cached value", self.vessel_id)
            return self.data
        except CrystalMaintenanceError:
            _LOGGER.warning("Maintenance mode fetching vessel %s; keeping cached value", self.vessel_id)
            return self.data
        except CrystalApiError as err:
            raise UpdateFailed(f"Crystal API error fetching vessel {self.vessel_id}: {err}") from err

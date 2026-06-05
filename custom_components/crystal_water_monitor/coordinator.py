from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
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
        self.last_synced: datetime | None = None

    async def _async_update_data(self) -> ConnectApiAccountVesselV1 | None:
        try:
            data = await self.client.get_vessel(self.vessel_id)
            self.inactive = False
            self.last_synced = datetime.now(timezone.utc)
            return data
        except CrystalAuthError:
            _LOGGER.warning("Auth error fetching vessel %s; triggering reauth", self.vessel_id)
            self.config_entry.async_start_reauth(self.hass)
            return self.data
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

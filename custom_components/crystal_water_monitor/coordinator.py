from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    CrystalApiClient,
    CrystalApiError,
    CrystalMaintenanceError,
    CrystalRateLimitError,
)

_LOGGER = logging.getLogger(__name__)


class CrystalDataUpdateCoordinator(DataUpdateCoordinator):
    """Fetches data for all vessels under one account."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: CrystalApiClient,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Crystal Water Monitor",
            update_interval=timedelta(minutes=scan_interval),
        )
        self.client = client
        # vessel_id -> detail dict
        self.vessel_data: dict[int, dict] = {}

    async def _async_update_data(self) -> dict[int, dict]:
        try:
            vessels = await self.client.list_vessels()
        except CrystalRateLimitError:
            _LOGGER.warning("Crystal API rate limit hit; using cached data")
            return self.vessel_data
        except CrystalMaintenanceError:
            _LOGGER.warning("Crystal API in maintenance mode; using cached data")
            return self.vessel_data
        except CrystalApiError as err:
            raise UpdateFailed(f"Crystal API error: {err}") from err

        results: dict[int, dict] = {}
        for vessel in vessels:
            vessel_id = vessel["vesselId"]
            try:
                detail = await self.client.get_vessel(vessel_id)
                results[vessel_id] = detail
            except CrystalRateLimitError:
                _LOGGER.warning(
                    "Rate limit hit fetching vessel %s; keeping cached value", vessel_id
                )
                if vessel_id in self.vessel_data:
                    results[vessel_id] = self.vessel_data[vessel_id]
            except CrystalMaintenanceError:
                _LOGGER.warning("Maintenance mode fetching vessel %s", vessel_id)
                if vessel_id in self.vessel_data:
                    results[vessel_id] = self.vessel_data[vessel_id]
            except CrystalApiError as err:
                _LOGGER.error("Error fetching vessel %s: %s", vessel_id, err)

        self.vessel_data = results
        return results

from __future__ import annotations

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "connect-api"))

from connect_api.api.default_api import DefaultApi
from connect_api.api_client import ApiClient
from connect_api.configuration import Configuration
from connect_api.exceptions import ApiException, ForbiddenException, NotFoundException, ServiceException, UnauthorizedException
from connect_api.models.connect_api_account_vessel_summary_v1 import ConnectApiAccountVesselSummaryV1
from connect_api.models.connect_api_account_vessel_v1 import ConnectApiAccountVesselV1
from connect_api.models.connect_api_reading_v1 import ConnectAPIReadingV1

from .const import BASE_URLS

# Re-export the generated models so the rest of the component imports from here
__all__ = [
    "ConnectApiAccountVesselSummaryV1",
    "ConnectApiAccountVesselV1",
    "ConnectAPIReadingV1",
    "CrystalApiError",
    "CrystalAuthError",
    "CrystalRateLimitError",
    "CrystalMaintenanceError",
    "CrystalNotFoundError",
    "CrystalSubscriptionError",
    "CrystalApiClient",
]


class CrystalApiError(Exception):
    pass


class CrystalAuthError(CrystalApiError):
    pass


class CrystalRateLimitError(CrystalApiError):
    pass


class CrystalMaintenanceError(CrystalApiError):
    pass


class CrystalNotFoundError(CrystalApiError):
    pass


class CrystalSubscriptionError(CrystalApiError):
    pass


class CrystalApiClient:
    def __init__(self, api_key: str, environment: str) -> None:
        config = Configuration(host=BASE_URLS[environment], api_key={"api_key": api_key})
        self._client = ApiClient(configuration=config)
        self._api = DefaultApi(api_client=self._client)

    async def close(self) -> None:
        await self._client.close()

    async def list_vessels(self) -> list[ConnectApiAccountVesselSummaryV1]:
        try:
            result = await self._api.connect_v1_vessels_get()
            return result.vessels
        except (UnauthorizedException, ForbiddenException) as err:
            raise CrystalAuthError(self._server_message(err)) from err
        except ApiException as err:
            raise self._map(err) from err

    async def get_vessel(self, vessel_id: int) -> ConnectApiAccountVesselV1:
        try:
            return await self._api.connect_v1_vessels_vessel_id_get(str(vessel_id))
        except (UnauthorizedException, ForbiddenException) as err:
            raise CrystalAuthError(self._server_message(err)) from err
        except ApiException as err:
            raise self._map(err) from err

    def _server_message(self, err: ApiException) -> str:
        try:
            return json.loads(err.body).get("message") or err.reason or str(err.status)
        except Exception:
            return err.reason or str(err.status)

    def _map(self, err: ApiException) -> CrystalApiError:
        msg = self._server_message(err)
        if err.status == 402:
            return CrystalSubscriptionError(msg)
        if err.status == 404:
            return CrystalNotFoundError(msg)
        if err.status == 429:
            return CrystalRateLimitError(msg)
        if err.status == 503:
            return CrystalMaintenanceError(msg)
        return CrystalApiError(msg)

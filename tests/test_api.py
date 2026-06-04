import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.crystal_water_monitor.api import (
    CrystalApiClient,
    CrystalAuthError,
    CrystalRateLimitError,
    CrystalMaintenanceError,
)
from connect_api.exceptions import ApiException, ForbiddenException, UnauthorizedException


def make_client():
    with patch("custom_components.crystal_water_monitor.api.ApiClient"):
        with patch("custom_components.crystal_water_monitor.api.DefaultApi"):
            return CrystalApiClient("test-key", "production")


@pytest.mark.asyncio
async def test_list_vessels_success():
    client = make_client()
    vessel = MagicMock()
    vessel.vessel_id = 1
    vessel.name = "My Pool"
    result = MagicMock()
    result.vessels = [vessel]
    client._api.connect_v1_vessels_get = AsyncMock(return_value=result)

    vessels = await client.list_vessels()

    assert len(vessels) == 1
    assert vessels[0].name == "My Pool"


@pytest.mark.asyncio
async def test_auth_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(
        side_effect=UnauthorizedException(status=401, reason="Unauthorized")
    )

    with pytest.raises(CrystalAuthError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_rate_limit_error():
    client = make_client()
    err = ApiException(status=429, reason="Too Many Requests")
    err.body = None
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=err)

    with pytest.raises(CrystalRateLimitError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_maintenance_error():
    client = make_client()
    err = ApiException(status=503, reason="Service Unavailable")
    err.body = None
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=err)

    with pytest.raises(CrystalMaintenanceError):
        await client.list_vessels()

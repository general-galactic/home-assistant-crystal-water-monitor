from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from connect_api.exceptions import ApiException

from custom_components.crystal_water_monitor.api import (
    CrystalApiClient,
    CrystalAuthError,
    CrystalMaintenanceError,
    CrystalNotFoundError,
    CrystalRateLimitError,
    CrystalSubscriptionError,
)


def make_client():
    with patch("custom_components.crystal_water_monitor.api.ApiClient"):
        with patch("custom_components.crystal_water_monitor.api.DefaultApi"):
            return CrystalApiClient("test-key", "production")


def make_api_exception(status: int) -> ApiException:
    err = ApiException(status=status, reason="test")
    err.body = None
    return err


# ---------------------------------------------------------------------------
# list_vessels
# ---------------------------------------------------------------------------

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
async def test_list_vessels_401_raises_auth_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=make_api_exception(401))
    with pytest.raises(CrystalAuthError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_list_vessels_403_raises_auth_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=make_api_exception(403))
    with pytest.raises(CrystalAuthError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_list_vessels_402_raises_subscription_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=make_api_exception(402))
    with pytest.raises(CrystalSubscriptionError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_list_vessels_429_raises_rate_limit_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=make_api_exception(429))
    with pytest.raises(CrystalRateLimitError):
        await client.list_vessels()


@pytest.mark.asyncio
async def test_list_vessels_503_raises_maintenance_error():
    client = make_client()
    client._api.connect_v1_vessels_get = AsyncMock(side_effect=make_api_exception(503))
    with pytest.raises(CrystalMaintenanceError):
        await client.list_vessels()


# ---------------------------------------------------------------------------
# get_vessel
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_vessel_success():
    client = make_client()
    vessel = MagicMock()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(return_value=vessel)
    result = await client.get_vessel(42)
    assert result is vessel


@pytest.mark.asyncio
async def test_get_vessel_401_raises_auth_error():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(401))
    with pytest.raises(CrystalAuthError):
        await client.get_vessel(1)


@pytest.mark.asyncio
async def test_get_vessel_403_raises_auth_error():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(403))
    with pytest.raises(CrystalAuthError):
        await client.get_vessel(1)


@pytest.mark.asyncio
async def test_get_vessel_402_raises_subscription_error():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(402))
    with pytest.raises(CrystalSubscriptionError):
        await client.get_vessel(1)


@pytest.mark.asyncio
async def test_get_vessel_404_raises_not_found():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(404))
    with pytest.raises(CrystalNotFoundError):
        await client.get_vessel(1)


@pytest.mark.asyncio
async def test_get_vessel_429_raises_rate_limit_error():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(429))
    with pytest.raises(CrystalRateLimitError):
        await client.get_vessel(1)


@pytest.mark.asyncio
async def test_get_vessel_503_raises_maintenance_error():
    client = make_client()
    client._api.connect_v1_vessels_vessel_id_get = AsyncMock(side_effect=make_api_exception(503))
    with pytest.raises(CrystalMaintenanceError):
        await client.get_vessel(1)

import pytest
import aiohttp
from aioresponses import aioresponses

from custom_components.crystal_water_monitor.api import (
    CrystalApiClient,
    CrystalAuthError,
    CrystalRateLimitError,
    CrystalMaintenanceError,
)


PROD_URL = "https://connect.crystalwatermonitor.app"


@pytest.fixture
def client(aiohttp_session):
    return CrystalApiClient("test-key", "production", aiohttp_session)


@pytest.mark.asyncio
async def test_list_vessels_success(aiohttp_client):
    async with aiohttp.ClientSession() as session:
        cli = CrystalApiClient("key", "production", session)
        with aioresponses() as m:
            m.get(
                f"{PROD_URL}/connect/v1/vessels",
                payload={"vessels": [{"vesselId": 1, "name": "My Pool", "type": "Pool", "volumeGallons": 15000}]},
            )
            vessels = await cli.list_vessels()
    assert len(vessels) == 1
    assert vessels[0]["vesselId"] == 1


@pytest.mark.asyncio
async def test_auth_error():
    async with aiohttp.ClientSession() as session:
        cli = CrystalApiClient("bad-key", "production", session)
        with aioresponses() as m:
            m.get(f"{PROD_URL}/connect/v1/vessels", status=403)
            with pytest.raises(CrystalAuthError):
                await cli.list_vessels()


@pytest.mark.asyncio
async def test_rate_limit_error():
    async with aiohttp.ClientSession() as session:
        cli = CrystalApiClient("key", "production", session)
        with aioresponses() as m:
            m.get(f"{PROD_URL}/connect/v1/vessels", status=429)
            with pytest.raises(CrystalRateLimitError):
                await cli.list_vessels()


@pytest.mark.asyncio
async def test_maintenance_error():
    async with aiohttp.ClientSession() as session:
        cli = CrystalApiClient("key", "production", session)
        with aioresponses() as m:
            m.get(f"{PROD_URL}/connect/v1/vessels", status=503)
            with pytest.raises(CrystalMaintenanceError):
                await cli.list_vessels()

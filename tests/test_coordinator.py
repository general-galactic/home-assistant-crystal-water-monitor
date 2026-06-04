"""Tests for CrystalDataUpdateCoordinator."""
from __future__ import annotations

import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.crystal_water_monitor.coordinator import CrystalDataUpdateCoordinator
from custom_components.crystal_water_monitor.api import (
    CrystalAuthError,
    CrystalSubscriptionError,
    CrystalRateLimitError,
    CrystalMaintenanceError,
    CrystalApiError,
    CrystalNotFoundError,
)

from .conftest import make_vessel


@pytest.fixture
def hass(hass):
    return hass


def make_coordinator(hass, client):
    coord = CrystalDataUpdateCoordinator(hass=hass, client=client, scan_interval=20)
    return coord


@pytest.mark.asyncio
async def test_successful_update(hass):
    vessel = make_vessel(vessel_id=42, name="Backyard Pool")
    summary = MagicMock()
    summary.vessel_id = 42

    client = MagicMock()
    client.list_vessels = AsyncMock(return_value=[summary])
    client.get_vessel = AsyncMock(return_value=vessel)

    coord = make_coordinator(hass, client)
    result = await coord._async_update_data()

    assert 42 in result
    assert result[42] is vessel
    assert coord.last_synced is not None


@pytest.mark.asyncio
async def test_multiple_vessels(hass):
    summaries = [MagicMock(vessel_id=1), MagicMock(vessel_id=2)]
    vessels = {1: make_vessel(vessel_id=1), 2: make_vessel(vessel_id=2)}

    client = MagicMock()
    client.list_vessels = AsyncMock(return_value=summaries)
    client.get_vessel = AsyncMock(side_effect=lambda vid: vessels[int(vid)])

    coord = make_coordinator(hass, client)
    result = await coord._async_update_data()

    assert set(result.keys()) == {1, 2}


@pytest.mark.asyncio
async def test_auth_error_raises_config_entry_error(hass):
    client = MagicMock()
    client.list_vessels = AsyncMock(side_effect=CrystalAuthError("bad key"))

    coord = make_coordinator(hass, client)
    with pytest.raises(ConfigEntryError):
        await coord._async_update_data()


@pytest.mark.asyncio
async def test_subscription_error_raises_config_entry_error(hass):
    client = MagicMock()
    client.list_vessels = AsyncMock(side_effect=CrystalSubscriptionError("no sub"))

    coord = make_coordinator(hass, client)
    with pytest.raises(ConfigEntryError):
        await coord._async_update_data()


@pytest.mark.asyncio
async def test_rate_limit_returns_cached_data(hass):
    cached_vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.list_vessels = AsyncMock(side_effect=CrystalRateLimitError("429"))

    coord = make_coordinator(hass, client)
    coord.vessel_data = {1: cached_vessel}

    result = await coord._async_update_data()

    assert result == {1: cached_vessel}
    # last_synced should not be updated on cached return
    assert coord.last_synced is None


@pytest.mark.asyncio
async def test_maintenance_returns_cached_data(hass):
    cached_vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.list_vessels = AsyncMock(side_effect=CrystalMaintenanceError("503"))

    coord = make_coordinator(hass, client)
    coord.vessel_data = {1: cached_vessel}

    result = await coord._async_update_data()

    assert result == {1: cached_vessel}


@pytest.mark.asyncio
async def test_generic_api_error_raises_update_failed(hass):
    client = MagicMock()
    client.list_vessels = AsyncMock(side_effect=CrystalApiError("oops"))

    coord = make_coordinator(hass, client)
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()


@pytest.mark.asyncio
async def test_vessel_rate_limit_keeps_cached(hass):
    """Rate limit on individual vessel fetch falls back to cached value."""
    summary = MagicMock(vessel_id=1)
    cached_vessel = make_vessel(vessel_id=1)

    client = MagicMock()
    client.list_vessels = AsyncMock(return_value=[summary])
    client.get_vessel = AsyncMock(side_effect=CrystalRateLimitError("429"))

    coord = make_coordinator(hass, client)
    coord.vessel_data = {1: cached_vessel}

    result = await coord._async_update_data()

    assert result[1] is cached_vessel


@pytest.mark.asyncio
async def test_vessel_not_found_raises_config_entry_error(hass):
    summary = MagicMock(vessel_id=99)
    client = MagicMock()
    client.list_vessels = AsyncMock(return_value=[summary])
    client.get_vessel = AsyncMock(side_effect=CrystalNotFoundError("not found"))

    coord = make_coordinator(hass, client)
    with pytest.raises(ConfigEntryError):
        await coord._async_update_data()


@pytest.mark.asyncio
async def test_scan_interval_set_correctly(hass):
    client = MagicMock()
    coord = CrystalDataUpdateCoordinator(hass=hass, client=client, scan_interval=30)
    assert coord.update_interval == timedelta(minutes=30)


@pytest.mark.asyncio
async def test_last_synced_updated_after_success(hass):
    summary = MagicMock(vessel_id=1)
    vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.list_vessels = AsyncMock(return_value=[summary])
    client.get_vessel = AsyncMock(return_value=vessel)

    coord = make_coordinator(hass, client)
    assert coord.last_synced is None

    await coord._async_update_data()

    assert coord.last_synced is not None
    from datetime import timezone
    assert coord.last_synced.tzinfo == timezone.utc

"""Tests for CrystalVesselCoordinator."""
from __future__ import annotations

import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.crystal_water_monitor.coordinator import CrystalVesselCoordinator
from custom_components.crystal_water_monitor.api import (
    CrystalAuthError,
    CrystalSubscriptionError,
    CrystalRateLimitError,
    CrystalMaintenanceError,
    CrystalApiError,
    CrystalNotFoundError,
)

from .conftest import make_vessel


def make_coordinator(hass, client, vessel_id=1, scan_interval=20):
    coord = CrystalVesselCoordinator(
        hass=hass,
        client=client,
        vessel_id=vessel_id,
        scan_interval=scan_interval,
    )
    # Provide a fake config_entry so async_start_reauth can be called
    coord.config_entry = MagicMock()
    coord.config_entry.async_start_reauth = MagicMock()
    return coord


# ---------------------------------------------------------------------------
# Success
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_successful_update(hass):
    vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(return_value=vessel)

    coord = make_coordinator(hass, client, vessel_id=1)
    result = await coord._async_update_data()

    assert result is vessel
    assert coord.inactive is False
    assert coord.last_synced is not None


@pytest.mark.asyncio
async def test_last_synced_updated_after_success(hass):
    vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(return_value=vessel)

    coord = make_coordinator(hass, client)
    assert coord.last_synced is None

    await coord._async_update_data()

    assert coord.last_synced is not None
    from datetime import timezone
    assert coord.last_synced.tzinfo == timezone.utc


@pytest.mark.asyncio
async def test_scan_interval_set_correctly(hass):
    client = MagicMock()
    coord = CrystalVesselCoordinator(hass=hass, client=client, vessel_id=1, scan_interval=30)
    assert coord.update_interval == timedelta(minutes=30)


# ---------------------------------------------------------------------------
# Auth errors → reauth, return cached
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_auth_error_triggers_reauth_and_returns_cached(hass):
    cached = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalAuthError("bad key"))

    coord = make_coordinator(hass, client)
    coord.data = cached

    result = await coord._async_update_data()

    coord.config_entry.async_start_reauth.assert_called_once_with(hass)
    assert result is cached


@pytest.mark.asyncio
async def test_auth_error_returns_none_when_no_cache(hass):
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalAuthError("bad key"))

    coord = make_coordinator(hass, client)
    coord.data = None

    result = await coord._async_update_data()

    coord.config_entry.async_start_reauth.assert_called_once()
    assert result is None


# ---------------------------------------------------------------------------
# Inactive states (402, 404) → mark inactive, no reauth
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_not_found_marks_inactive(hass):
    cached = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalNotFoundError("not found"))

    coord = make_coordinator(hass, client)
    coord.data = cached

    result = await coord._async_update_data()

    assert coord.inactive is True
    assert result is cached
    coord.config_entry.async_start_reauth.assert_not_called()


@pytest.mark.asyncio
async def test_subscription_error_marks_inactive(hass):
    cached = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalSubscriptionError("no sub"))

    coord = make_coordinator(hass, client)
    coord.data = cached

    result = await coord._async_update_data()

    assert coord.inactive is True
    assert result is cached
    coord.config_entry.async_start_reauth.assert_not_called()


@pytest.mark.asyncio
async def test_inactive_cleared_on_recovery(hass):
    vessel = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(return_value=vessel)

    coord = make_coordinator(hass, client)
    coord.inactive = True

    await coord._async_update_data()

    assert coord.inactive is False


# ---------------------------------------------------------------------------
# Rate limit / maintenance → return cached, no inactive
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_rate_limit_returns_cached(hass):
    cached = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalRateLimitError("429"))

    coord = make_coordinator(hass, client)
    coord.data = cached

    result = await coord._async_update_data()

    assert result is cached
    assert coord.inactive is False
    assert coord.last_synced is None


@pytest.mark.asyncio
async def test_maintenance_returns_cached(hass):
    cached = make_vessel(vessel_id=1)
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalMaintenanceError("503"))

    coord = make_coordinator(hass, client)
    coord.data = cached

    result = await coord._async_update_data()

    assert result is cached
    assert coord.inactive is False


# ---------------------------------------------------------------------------
# Generic API error → UpdateFailed
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_generic_api_error_raises_update_failed(hass):
    client = MagicMock()
    client.get_vessel = AsyncMock(side_effect=CrystalApiError("oops"))

    coord = make_coordinator(hass, client)
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()

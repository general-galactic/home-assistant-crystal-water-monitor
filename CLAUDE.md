# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Home Assistant custom component (integration) for the **Crystal Water Monitor** — an IoT device that measures pool/hot tub/swim spa water chemistry (pH, ORP, temperature, chlorine, etc.) every 10 minutes and uploads readings every 20 minutes.

The integration connects to the **Crystal Connect API**, a REST proxy in front of the Crystal platform.

## API

- **Production base URL**: `https://connect.crystalwatermonitor.app`
- **Dev base URL**: `https://dev.connect.crystalwatermonitor.app`
- **Auth**: `x-api-key` header — one key per account, scoped to that account only
- **Rate limit**: 1 request per 15 minutes per key (AWS API Gateway); 10 req / 5-min window per IP (WAF → 429)
- **Poll interval**: minimum 15 min; default 20 min (monitor only uploads every 20 min anyway)

### Key endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/connect/v1/vessels` | List all vessels for the account |
| GET | `/connect/v1/vessels/{vesselId}` | Full detail + readings + actions for one vessel |

The vessel detail response is the core data structure. `readings` is a map of reading type → reading object; keys are optional and must be handled gracefully. All temperature values (`disc.tempC`, `waterTemp.value`) are in °C.

### Reading object fields

`readingType`, `value`, `range {low, high}`, `unit`, `unitTitle`, `date` (ISO8601), `source` (`monitor` | `report` | `computed`), `status` (`really_low` | `low` | `ok` | `high` | `really_high` | `invalid` | `unknown`), `statusSinceDate`, `abbreviation`, `title`

### Water status color

`disc.waterStatusColor`: `blue` = balanced, `orange` = needs attention, `red` = unsafe, `gray` = unknown

## Integration Architecture

Standard HA custom component layout under `custom_components/crystal_water_monitor/`:

- **`__init__.py`** — sets up the `DataUpdateCoordinator` (one per account), registers vessels as config entries, fetches `/vessels` then `/vessels/{id}` for each on every poll cycle
- **`config_flow.py`** — UI flow asking for `api_key`, `environment` (Production/Development), and `scan_interval` (minutes, default 20, min 15)
- **`coordinator.py`** — `CrystalDataUpdateCoordinator` wraps the API client; handles 429 (back off, do not raise) and 503 (surface as sensor state, not an error)
- **`api.py`** — thin async HTTP client using `aiohttp`; raises typed exceptions for auth failure, rate limit, maintenance
- **`sensor.py`** — one `SensorEntity` per reading type per vessel, plus a Water Status sensor and an Actions Pending count sensor
- **`const.py`** — reading type definitions, unit mappings, status → HA state mappings

### Entity model (per vessel)

| Entity | Source field | Unit |
|--------|-------------|------|
| Water Status | `disc.waterStatusColor` | — (Balanced / Needs Attention / Unsafe / Unknown) |
| pH | `readings.ph.value` | pH |
| ORP | `readings.orp.value` | mV |
| Water Temperature | `readings.waterTemp.value` | °C or °F |
| Free Chlorine | `readings.freeChlorine.value` | ppm |
| Total Alkalinity | `readings.totalAlkalinity.value` | ppm |
| Total Hardness | `readings.totalHardness.value` | ppm |
| Cyanuric Acid | `readings.cyanuricAcid.value` | ppm |
| Salt | `readings.salt.value` | ppm |
| LSI | `readings.lsi.value` | — |
| Battery | `readings.battery.value` | % |
| Actions Pending | `len(actions)` | — |

Each reading sensor exposes `status`, `range`, `date`, `source`, and the `actions` list as extra state attributes.

## Development Commands

```bash
# Install test dependencies
pip install -r requirements_test.txt

# Run all tests
pytest

# Run a single test
pytest tests/test_api.py::test_list_vessels_success

# Validate the integration manifest (requires a local HA dev checkout)
python -m script.hassfest --integration-path custom_components/crystal_water_monitor
```

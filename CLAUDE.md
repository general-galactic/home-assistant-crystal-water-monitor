# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Home Assistant custom component (integration) for the **Crystal Water Monitor** — an IoT device that measures pool/hot tub/swim spa water chemistry (pH, ORP, temperature, chlorine, etc.) every 10 minutes and uploads readings every 20 minutes.

The integration connects to the **Crystal Connect API**, a REST proxy in front of the Crystal platform.

### Reading object fields

`readingType`, `value`, `range {low, high}`, `unit`, `unitTitle`, `date` (ISO8601), `source` (`monitor` | `report` | `computed`), `status` (`really_low` | `low` | `ok` | `high` | `really_high` | `invalid` | `unknown`), `statusSinceDate`, `abbreviation`, `title`

### Water status color

`disc.waterStatusColor`: `blue` = balanced, `orange` = needs attention, `red` = needs immediate attention, `gray` = unknown

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
| Water Status | `disc.waterStatusColor` | — (Balanced / Needs Attention / Needs Immediate Attention / Unknown) |
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

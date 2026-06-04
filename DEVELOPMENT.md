# Development Guide

## API Types

Python TypedDicts for the Crystal Connect API response shapes live in [types.py](custom_components/crystal_water_monitor/types.py). They are generated from the OpenAPI spec at `https://dev.connect.crystalwatermonitor.app/docs/openapi.yaml`.

When the API changes, regenerate them:

```bash
./scripts/generate_types.sh        # from prod spec (default)
./scripts/generate_types.sh dev    # from dev spec
```

This requires `datamodel-code-generator` (installed automatically by the script). Review the diff after regenerating — new fields may need to be handled in `sensor.py` or `coordinator.py`.

## Installation

### Option A — HACS (recommended)

1. Open HACS in your Home Assistant sidebar.
2. Go to **Integrations → Custom repositories**.
3. Add this repository URL and select category **Integration**.
4. Search for **Crystal Water Monitor** and install it.
5. Restart Home Assistant.

### Option B — Manual

1. Copy the `custom_components/crystal_water_monitor/` folder into your Home Assistant config directory:

   ```
   <config>/custom_components/crystal_water_monitor/
   ```

   The config directory is usually `/config/` inside the HA container, or `~/.homeassistant/` for a local install.

2. Restart Home Assistant.

## Setup

```bash
git clone <repo-url>
cd home-assistant-plugin
pip install -r requirements_test.txt
```

## Run tests

```bash
pytest
```

## Lint

```bash
pip install ruff --index-url https://pypi.org/simple/
ruff check custom_components/
```

## Local HA instance

Run the dev script from the repo root to start a local HA container with the integration volume-mounted and dev mode enabled (`HA_CRYSTAL_DEV=1` shows the environment selector in the config flow):

```bash
./scripts/dev.sh
```

Then open `http://localhost:8123` in a browser and complete onboarding. The integration will appear under **Settings → Devices & Services → Add Integration**.

After any code change, restart the container:

```bash
docker restart ha-dev
```

To tail logs:

```bash
docker logs ha-dev --tail 50 | grep -i crystal
```

## Releases

Use the release script to bump the version, commit, and tag:

```bash
./scripts/release.sh
```

Enter a semver version like `1.0.2`. Dev builds enable the environment selector in the config flow via the `HA_CRYSTAL_DEV` env var.

## Validate the manifest

If you have a local Home Assistant core checkout, run:

```bash
python -m script.hassfest --integration-path custom_components/crystal_water_monitor
```

# Crystal Water Monitor — Home Assistant Integration

A Home Assistant custom component that surfaces pool, hot tub, and swim spa water chemistry from [Crystal Water Monitor](https://www.crystalwatermonitor.app) devices as native HA sensors.

## Prerequisites

- Home Assistant 2023.x or later
- A Crystal Water Monitor device connected to a pool or hot tub
- A Crystal Connect API key (contact Crystal customer support to obtain one)

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

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Crystal Water Monitor**.
3. Enter your **API key**, choose an environment (Production or Development), and set a poll interval (minimum 15 minutes; default 20).
4. Click **Submit**. HA will validate the key and discover your vessels automatically.

One device and a full set of sensors will be created for each vessel on your account.

## Sensors

Each vessel gets the following entities:

| Sensor | State | Unit |
|--------|-------|------|
| Water Status | Balanced / Needs Attention / Unsafe / Unknown | — |
| Actions Pending | Count of recommended actions | — |
| pH | Measured value | pH |
| ORP | Measured value | mV |
| Water Temperature | Measured value | °C |
| Free Chlorine | Measured value | ppm |
| Total Chlorine | Measured value | ppm |
| Total Alkalinity | Measured value | ppm |
| Total Hardness | Measured value | ppm |
| Cyanuric Acid | Measured value | ppm |
| Salt | Measured value | ppm |
| LSI | Langelier Saturation Index | — |
| Battery | Monitor battery level | % |
| WiFi Signal | Monitor signal strength | dBm |

Every reading sensor includes these extra attributes: `status` (ok / low / high / etc.), `source` (monitor / report / computed), `date`, and `actions` (the list of recommended actions for the vessel).

## Development Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd home-assistant-plugin
pip install -r requirements_test.txt
```

### 2. Run the test suite

```bash
pytest
```

### 3. Lint

ruff must be installed from PyPI directly (not a private index):

```bash
pip install ruff --index-url https://pypi.org/simple/
ruff check custom_components/
```

### 4. Load into a live Home Assistant for manual testing

The easiest way to test against a real HA instance is with the **HA dev container** or a local install.

**With the HA dev container (VS Code)**

1. Open the repo in VS Code. If prompted to reopen in container, accept — or run **Dev Containers: Reopen in Container** from the command palette.
2. Inside the container, run:
   ```bash
   scripts/develop
   ```
   This starts HA with the `custom_components/` folder mounted automatically.
3. Open `http://localhost:8123` and complete onboarding, then add the integration via **Settings → Devices & Services**.

**With an existing local HA install**

Symlink the component folder so changes are reflected without copying:

```bash
ln -s "$(pwd)/custom_components/crystal_water_monitor" \
  ~/.homeassistant/custom_components/crystal_water_monitor
```

Then restart HA. After any code change, restart again (or use the **Quick Reload** developer tool if only `sensor.py` or `coordinator.py` changed).

**With a production HA instance (Docker)**

```bash
docker cp custom_components/crystal_water_monitor \
  homeassistant:/config/custom_components/crystal_water_monitor
```

Then restart the container.

### 5. Validate the manifest

If you have a local Home Assistant core checkout, run:

```bash
python -m script.hassfest --integration-path custom_components/crystal_water_monitor
```

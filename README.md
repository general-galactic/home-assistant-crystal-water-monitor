# Crystal Water Monitor — Home Assistant Integration

The official Home Assistant integration from [Crystal Water Monitor](https://www.crystalwatermonitor.com) — bringing real-time pool & hot tub water chemistry directly into your smart home.

## Prerequisites

- Home Assistant 2026.3 or later
- A Crystal Water Monitor installed in a pool, hot tub, or swim spa with an active subscription.
- A Crystal Connect API key ([get one here](https://www.crystalwatermonitor.com/api-key))

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Crystal Water Monitor**.
3. Enter your **API key** and click **Submit**. HA will validate the key and discover your pools and hot tubs automatically.

One device and a full set of sensors will be created for each pool or hot tub on your account.

## Dashboard Cards

This integration includes two cards that can be added to Dashboards. Both cards appear in the **Add Card** picker under **Custom cards**.

### Crystal Disc

Displays the water status disc from the app for a pool or hot tub — color-coded by water status.

### Crystal Actions Card

Lists the recommended water care actions for your pool or hot tub.


> **Proprietary Software** — This integration is not open source. Copying, modification, or redistribution is prohibited. See [LICENSE](LICENSE) for details.

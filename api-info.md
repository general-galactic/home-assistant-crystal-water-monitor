# Home Assistant Plugin Generation Prompt

I need you to build a Home Assistant integration (custom component) for the **Crystal Water Monitor Connect API**. Here is everything you need to know about the API:

## Overview

The Crystal Connect API is a REST API that provides access to pool/hot tub/swim spa water quality data from Crystal Water Monitor devices. It is a proxy API — it sits in front of the internal Crystal platform and exposes a simplified, authenticated interface for external consumers.

## Base URLs

- **Production**: `https://connect.crystalwatermonitor.app`
- **Development**: `https://dev.connect.crystalwatermonitor.app`

## Authentication

All requests (except `/docs`) require an API key passed in the `x-api-key` header:

```
x-api-key: your-api-key-here
```

API keys are issued per account by Crystal customer support. Each key is scoped to a single account and cannot access other accounts' data.

## Rate Limiting

- **1 request per 15 minutes** per API key (enforced by AWS API Gateway Usage Plan)
- **10 requests per 5-minute window** per IP before WAF blocks with 429
- Throttled responses return HTTP `429` with body: `{"message": "Too many requests. Please slow down and try again shortly."}`
- Maintenance windows return HTTP `503` with body: `{"message": "The Crystal Connect API is temporarily unavailable for maintenance. Please try again shortly."}`

## Routes

### List Vessels
```
GET /connect/v1/vessels
x-api-key: <key>
```

Returns all vessels (pools, hot tubs, swim spas) associated with the account.

**Response:**
```json
{
  "vessels": [
    {
      "vesselId": 2934,
      "name": "My Pool",
      "type": "Pool",
      "volumeGallons": 20000
    }
  ]
}
```

### Get Vessel Detail
```
GET /connect/v1/vessels/{vesselId}
x-api-key: <key>
```

Returns full detail for a single vessel including all current water readings and recommended actions.

**Response:**
```json
{
  "vesselId": 2934,
  "type": "Pool",
  "volumeGallons": 20000,
  "disc": {
    "name": "My Pool",
    "text": "Water is balanced",
    "lastUpdatedText": "2 minutes ago",
    "tempC": 28.5,
    "waterStatusColor": "blue"
  },
  "readings": {
    "ph": {
      "readingType": "ph",
      "value": 7.4,
      "range": { "low": 7.2, "high": 7.6 },
      "unit": "ph",
      "unitTitle": "pH",
      "date": "2026-06-03T21:00:00Z",
      "source": "monitor",
      "status": "ok",
      "statusSinceDate": "2026-06-03T18:00:00Z",
      "abbreviation": "pH",
      "title": "pH"
    },
    "orp": {},
    "waterTemp": {},
    "totalAlkalinity": {},
    "totalHardness": {},
    "cyanuricAcid": {},
    "freeChlorine": {},
    "totalChlorine": {},
    "bromine": {},
    "salt": {},
    "lsi": {}
  },
  "actions": [
    {
      "title": "Raise pH",
      "details": "Add 12 oz of pH Up",
      "iconUrl": "https://..."
    }
  ]
}
```

## Reading Object Schema

Each reading in the `readings` object has this shape:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `readingType` | string | ✓ | e.g. `ph`, `orp`, `waterTemp` |
| `value` | number | | Current measured value |
| `range` | object | | `{ low, high }` — the ideal range |
| `unit` | string | ✓ | e.g. `ph`, `mV`, `C`, `ppm` |
| `unitTitle` | string | | Human-readable unit label |
| `date` | ISO8601 | ✓ | When this reading was taken |
| `source` | string | | `monitor`, `report`, or `computed` |
| `status` | string | ✓ | `really_low`, `low`, `ok`, `high`, `really_high`, `invalid`, `unknown` |
| `statusSinceDate` | ISO8601 | | When status last changed |
| `abbreviation` | string | ✓ | Short label e.g. `pH`, `ORP` |
| `title` | string | ✓ | Full label e.g. `Oxidation Reduction Potential` |

## Water Status Color

`disc.waterStatusColor` is an overall water health indicator:
- `blue` — water is balanced
- `orange` — water needs attention
- `red` — water is unsafe
- `gray` — unknown / no data

## Reading Types

The following reading types may be present in the `readings` object (all optional):
`ph`, `orp`, `longOrp`, `waterTemp`, `totalAlkalinity`, `totalHardness`, `cyanuricAcid`, `freeChlorine`, `totalChlorine`, `bromine`, `totalDissolvedSolids`, `salt`, `phosphates`, `wifiRssi`, `battery`, `smartChlor`, `lsi`

## Important Notes for Integration Design

1. **Poll at most once every 15 minutes** — the API enforces this via rate limiting. Polling more frequently will result in 429 errors. The monitor device itself only uploads readings every 20 minutes, so there is no benefit to polling more often.
2. **One API key = one account** — a single key can have multiple vessels. List vessels first, then fetch detail for each.
3. **Readings may be absent** — not all reading types will be present for every vessel. The integration must handle missing readings gracefully.
4. **Temperature is in Celsius** — `disc.tempC` and `waterTemp.value` are always in °C. Convert to °F if needed based on user preference.
5. **`status` field is the health indicator** — use this to drive Home Assistant sensor states and alerts, not the raw value.
6. **`source` field matters** — `monitor` means the reading came from the Crystal device; `report` means it was manually entered by the user; `computed` means it was calculated. You may want to surface this in sensor attributes.
7. **Handle 429 and 503 gracefully** — back off and retry after the rate limit window, surface maintenance mode as a sensor state rather than an error.

## Suggested Home Assistant Entities Per Vessel

- **Sensor: Water Status** — `disc.waterStatusColor` mapped to a state (`Balanced`, `Needs Attention`, `Unsafe`, `Unknown`)
- **Sensor: pH** — `readings.ph.value`, unit `pH`, attributes: status, range, date
- **Sensor: ORP** — `readings.orp.value`, unit `mV`, attributes: status, range, date
- **Sensor: Water Temperature** — `readings.waterTemp.value` (°C or °F), attributes: status, date
- **Sensor: Free Chlorine** — `readings.freeChlorine.value`, unit `ppm`
- **Sensor: Total Alkalinity** — `readings.totalAlkalinity.value`, unit `ppm`
- **Sensor: Total Hardness** — `readings.totalHardness.value`, unit `ppm`
- **Sensor: Cyanuric Acid** — `readings.cyanuricAcid.value`, unit `ppm`
- **Sensor: Salt** — `readings.salt.value`, unit `ppm`
- **Sensor: LSI** — `readings.lsi.value` (Langelier Saturation Index)
- **Sensor: Battery** — `readings.battery.value`, unit `%`
- **Sensor: Actions Pending** — count of items in `actions` array
- **Attribute on each sensor**: `actions` list so automations can read what needs to be done

## Configuration

The integration should ask the user for:
1. `api_key` — their Connect API key
2. `environment` — Production or Development (default Production)
3. `scan_interval` — polling interval in minutes (default 20, minimum 15)

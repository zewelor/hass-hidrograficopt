# Instituto Hidrográfico Integration

Custom Home Assistant integration for Portuguese tide data from Instituto Hidrográfico HMAPI.

## Disclaimer

- This is an unofficial, community-maintained integration.
- It is not affiliated with, endorsed by, or supported by Instituto Hidrográfico.
- Tide data is fetched from public HMAPI endpoints and may change, be delayed, or be temporarily unavailable.
- Do not use this integration as the sole source for navigation safety or other safety-critical decisions.

## Features

- Config flow setup (no YAML required)
- One tide station per config entry
- Sensors for:
  - Next high tide time
  - Next high tide height
  - Next low tide time
  - Next low tide height
  - Tide status (`rising`, `falling`, `unknown`)
- `tide_status` sensor includes `tides` attributes with parsed tide events
- Service `hidrograficopt.reload_data` for manual refresh

## Installation (HACS)

1. Open HACS -> Integrations -> Custom repositories
2. Add `https://github.com/zewelor/hass-hidrograficopt` as `Integration`
3. Install "Instituto Hidrográfico Integration"
4. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Add integration "Instituto Hidrográfico Integration"
3. Select a tide station

## Options

- Update interval in minutes (default: 60)

## Time handling

HMAPI tide predictions are published in Fuso 0 (UTC), without an explicit
offset in the response. The integration interprets these timestamps as UTC and
returns timezone-aware timestamp sensors. Home Assistant converts them to the
timezone selected by the frontend or user profile.

For example, an HMAPI prediction of `2026-07-12 18:18:00` is `18:18 UTC` and
is displayed as `19:18` in Madeira during WEST (UTC+1).

## Service

### `hidrograficopt.reload_data`

Forces coordinator refresh for all configured stations.

Example:

```yaml
service: hidrograficopt.reload_data
```

## Data source

- HMAPI base: `https://www.hidrografico.pt/hmapi`
- Internal API notes: `docs/development/HMAPI.md`
- Repository icon (`icon.png`) is prepared from the official IH logo asset.

## Breaking change notice

This repository was migrated from a template/demo integration to a real tide integration.
Existing template config entries are not migrated automatically and should be removed/re-added.

### 1.0.0 breaking changes

- Removed template-only internal modules and compatibility wrappers
- Config flow no longer falls back to manual port ID entry when station list cannot be fetched
- `hidrograficopt.reload_data` now raises Home Assistant exceptions on failure instead of returning error payloads

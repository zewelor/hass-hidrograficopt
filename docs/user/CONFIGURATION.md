# Configuration

> Unofficial integration notice: do not rely on this integration as the only data source for safety-critical navigation decisions.

## Initial setup fields

- `port_id` (selected station or manual numeric value)

## Options flow

- `update_interval_minutes`
  - Default: `60`
  - Range: `5` to `360`

## Tide times

HMAPI publishes tide predictions in Fuso 0 (UTC). Home Assistant stores the
timestamp in UTC and renders it using the timezone selected in the frontend or
user profile. Raw values shown in Developer Tools therefore remain in UTC.

## Service

### `hidrograficopt.reload_data`

Force refresh of tide data for every configured station.

```yaml
service: hidrograficopt.reload_data
```

# Configuration

> Unofficial integration notice: do not rely on this integration as the only data source for safety-critical navigation decisions.

## Initial setup fields

- `port_id` (selected station or manual numeric value)

## Options flow

- `update_interval_minutes`
  - Default: `60`
  - Range: `5` to `360`
- `timezone_override` (optional)
  - IANA timezone string, for example: `Atlantic/Madeira`
  - If empty, integration uses station timezone auto-detected from station coordinates
  - Use this only if you need to force a specific timezone

## Service

### `hidrograficopt.reload_data`

Force refresh of tide data for every configured station.

```yaml
service: hidrograficopt.reload_data
```

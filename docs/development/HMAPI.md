# HMAPI Technical Notes

This document records verified behavior of the Instituto Hidrografico HMAPI
used by this integration.

## Scope And Verification Date

- Last verified: 2026-07-11
- Verification method: live HTTP calls, inspection of the public IH website frontend code,
  and comparison with the official 2026 Tide Tables
- Purpose: provide a stable internal contract for API client and coordinator implementation

## Official Documentation Status

No public OpenAPI/Swagger endpoint was found during verification.

Checked endpoints (all returned HTTP 404):

- `https://www.hidrografico.pt/hmapi/docs/`
- `https://www.hidrografico.pt/hmapi/redoc/`
- `https://www.hidrografico.pt/hmapi/swagger/`
- `https://www.hidrografico.pt/hmapi/openapi.json`
- `https://www.hidrografico.pt/hmapi/swagger.json`

Because of this, behavior is inferred from:

- official website frontend API usage
- live endpoint responses
- official Tide Tables published by Instituto Hidrográfico

## Verified Endpoints

### `GET /hmapi/tides/`

Response shape:

- GeoJSON `FeatureCollection`
- station list in `features`
- relevant fields per feature:
  - `properties.CODP` (station/port id)
  - `properties.PORTO` (station display name)
  - `properties.MAREGRAPH`
  - `geometry.coordinates` (lon, lat)

Observed count at verification time: 43 stations.

### `GET /hmapi/tidestation/`

Query parameters:

- `portID` (required integer)
- `period` (expected values `1..7`, aligned with website selector)
- `startDate` (optional, `YYYY-MM-DD`)

Known response fields:

- `date` (string, usually `YYYY-MM-DD HH:MM:SS`)
- `height` (float or null)
- `marId` (int or null)
- `portCode` (int or null)
- `tide` (`PM`, `BM`, or null)
- `moon` (string, often empty for tide rows)
- `event` (event label, e.g. `Preia-Mar`, `Baixa-Mar`, moon-phase labels)

## Known Quirks And Edge Cases

1. Tide and moon events are mixed in the same array.
2. Moon rows commonly have `tide=null`, `height=null`.
3. `startDate` does not always fully constrain all returned rows server-side.
4. Missing `portID` returns JSON error with HTTP 400.
5. Non-integer `portID` returns upstream HTTP 400 error payload.
6. Unknown numeric `portID` may return moon-only rows instead of explicit error.
7. `date` has no UTC suffix or numeric offset, even though the published tide
   predictions use Fuso 0 (TU/UTC).

## Time Reference

HMAPI prediction timestamps are published in Fuso 0 (TU/UTC), not in each
station's civil timezone. This was verified for Funchal by matching the live
HMAPI response for 2026-07-11 (`04:39`, `11:02`, `17:18`, `23:30`) with the
official Volume I table, whose Funchal pages state `Horas do Fuso: 0 (TU)`.
The official Volume II general notes likewise state that its port predictions
were calculated for Fuso 0.

The station endpoint provides coordinates but no timezone or offset metadata.
The public IH frontend uses those coordinates for display-zone lookup while
labelling the source as UTC+00:00; integrations must not infer that the naive
API string is already local station time.

Macau (`portID=814`) is present in the station list but returned no tide events
during verification. Its separate tide publication uses TU+8, so its source
time convention must be re-verified before accepting forecast data if HMAPI
starts returning events for it.

## Integration Parsing Rules

Use these rules in the integration API layer and coordinator:

1. Keep only tide rows where `tide` is `PM` or `BM`, and `height` is non-null.
2. Parse `date` using:
   - primary: `%Y-%m-%d %H:%M:%S`
   - fallback: `%Y-%m-%d %H:%M`
3. Sort events chronologically after parsing.
4. Attach UTC to naive HMAPI timestamps; normalize any future offset-aware timestamps to UTC.
5. Do not apply the Home Assistant timezone or a station timezone while parsing.
6. Derive nearest high/low from upcoming filtered events only.
7. Derive tide direction from nearest upcoming tide event:
   - next high => `rising`
   - next low => `falling`
   - no upcoming tide => `unknown`

## Reproducible Checks

Station list:

```bash
curl -sS 'https://www.hidrografico.pt/hmapi/tides/'
```

Station tide data:

```bash
curl -sS 'https://www.hidrografico.pt/hmapi/tidestation/?portID=112&period=7'
```

`portID` missing:

```bash
curl -sS 'https://www.hidrografico.pt/hmapi/tidestation/'
```

`portID` invalid:

```bash
curl -sS 'https://www.hidrografico.pt/hmapi/tidestation/?portID=abc&period=7'
```

## Open Questions / Future Validation

1. Confirm whether `startDate` behavior is intentionally server-side loose or a temporary bug.
2. Re-validate endpoint behavior periodically and after IH website updates.
3. If official HMAPI docs become public, replace inferred assumptions with documented contracts.
4. Re-check Macau's source time convention if `portID=814` starts returning tide events.

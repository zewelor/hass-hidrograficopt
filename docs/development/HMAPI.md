# HMAPI Technical Notes

This document records verified behavior of the Instituto Hidrografico HMAPI
used by this integration.

## Scope And Verification Date

- Last verified: 2026-03-03
- Verification method: live HTTP calls and inspection of the public IH website frontend code
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

## Integration Parsing Rules

Use these rules in the integration API layer and coordinator:

1. Keep only tide rows where `tide` is `PM` or `BM`, and `height` is non-null.
2. Parse `date` using:
   - primary: `%Y-%m-%d %H:%M:%S`
   - fallback: `%Y-%m-%d %H:%M`
3. Sort events chronologically after parsing.
4. Treat parsed times in the Home Assistant configured timezone.
5. Derive nearest high/low from upcoming filtered events only.
6. Derive tide direction from nearest upcoming tide event:
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

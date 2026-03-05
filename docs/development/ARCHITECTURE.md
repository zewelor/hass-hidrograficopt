# Architecture Overview

This document describes the current architecture of the Instituto Hidrográfico custom integration for Home Assistant.

## Directory Structure

```text
custom_components/hidrograficopt/
├── __init__.py
├── config_flow.py
├── const.py
├── data.py
├── diagnostics.py
├── manifest.json
├── services.yaml
├── api/
│   ├── __init__.py
│   ├── client.py
│   ├── models.py
│   ├── parsers.py
│   └── timezone.py
├── config_flow_handler/
│   ├── __init__.py
│   ├── config_flow.py
│   ├── options_flow.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── options.py
│   └── validators/
│       ├── __init__.py
│       └── credentials.py
├── coordinator/
│   ├── __init__.py
│   └── base.py
├── entity/
│   ├── __init__.py
│   └── base.py
├── entity_utils/
│   └── __init__.py
├── service_actions/
│   ├── __init__.py
│   └── reload_data.py
├── sensor/
│   ├── __init__.py
│   └── tide.py
├── translations/
│   └── en.json
└── utils/
    └── __init__.py
```

## Core Components

### API Layer (`api/`)

- `client.py` handles HMAPI HTTP communication and translates transport/data failures to integration exceptions.
- `parsers.py` validates and normalizes station and tide payloads into typed models.
- `models.py` defines `TideStation`, `TideEvent`, and enum types used across the integration.

### Coordinator (`coordinator/base.py`)

- Fetches tide events for one configured station on an interval.
- Derives `next_high`, `next_low`, and `tide_status`.
- Resolves effective timezone with precedence: options override -> config entry station timezone -> Home Assistant timezone.
- Exposes a single data dictionary consumed by all entities.

### Config Flow (`config_flow_handler/`)

- `config_flow.py` implements user setup and reconfigure flows.
- `options_flow.py` manages mutable settings (update interval and timezone override).
- `schemas/` and `validators/` keep flow UI and validation logic modular.
- Root `config_flow.py` exists for Home Assistant/hassfest compatibility and re-exports the handler.

### Entity Layer (`entity/` + `sensor/`)

- `InstitutoHidrogrficoEntity` centralizes unique ID/device info behavior.
- `sensor/tide.py` defines timestamp/height/status sensors backed only by coordinator data.
- Platform setup in `sensor/__init__.py` registers sensor entities from static `EntityDescription` metadata.

### Service Actions (`service_actions/`)

- `hidrograficopt.reload_data` triggers coordinator refresh for loaded config entries.
- Service handlers raise Home Assistant exceptions on failure and provide structured response data on success.

## Data Flow

```text
Config Entry
   ↓
API Client  ← Coordinator (periodic polling)
   ↓
Parsed/derived coordinator data
   ↓
Sensor entities + diagnostics + service responses
```

## Notes

- This integration currently supports the `sensor` platform only.
- Timezone behavior is configuration-based (not geolocation-based).
- See `docs/development/HMAPI.md` for validated endpoint behavior and parsing assumptions.

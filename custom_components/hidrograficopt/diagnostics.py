"""Diagnostics support for hidrograficopt."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.redact import async_redact_data

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import InstitutoHidrogrficoConfigEntry

TO_REDACT = {
    "token",
    "api_key",
    "password",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    del hass

    coordinator = entry.runtime_data.coordinator
    data = coordinator.data or {}
    events = data.get("events", [])
    tide_status = data.get("tide_status")

    serialized_events = [
        {
            "time": event.time.isoformat(),
            "height": event.height_m,
            "type": event.tide_type.value,
        }
        for event in events[:10]
    ]

    return {
        "entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "version": entry.version,
            "minor_version": entry.minor_version,
            "data": async_redact_data(entry.data, TO_REDACT),
            "options": async_redact_data(entry.options, TO_REDACT),
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "last_exception": str(coordinator.last_exception) if coordinator.last_exception else None,
            "update_interval": str(coordinator.update_interval),
        },
        "station": {
            "port_id": data.get("port_id"),
            "station_name": data.get("station_name"),
            "station_timezone": entry.data.get("station_timezone"),
            "timezone_override": entry.options.get("timezone_override"),
            "effective_timezone": data.get("effective_timezone"),
            "timezone_source": data.get("timezone_source"),
            "events_count": len(events),
            "next_high": (
                {
                    "time": data["next_high"].time.isoformat(),
                    "height": data["next_high"].height_m,
                    "type": data["next_high"].tide_type.value,
                }
                if data.get("next_high")
                else None
            ),
            "next_low": (
                {
                    "time": data["next_low"].time.isoformat(),
                    "height": data["next_low"].height_m,
                    "type": data["next_low"].tide_type.value,
                }
                if data.get("next_low")
                else None
            ),
            "tide_status": tide_status.value if tide_status else None,
            "events_sample": serialized_events,
        },
    }

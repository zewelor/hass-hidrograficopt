"""Service handlers for reloading coordinator data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.hidrograficopt.const import LOGGER
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from custom_components.hidrograficopt.data import InstitutoHidrogrficoConfigEntry
    from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse


async def async_handle_reload_data(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
    call: ServiceCall,
) -> ServiceResponse:
    """Force coordinator refresh and return diagnostic response."""
    del hass, call

    coordinator = entry.runtime_data.coordinator
    started = dt_util.now()

    try:
        await coordinator.async_request_refresh()
    except (UpdateFailed, ConfigEntryNotReady) as exception:
        LOGGER.exception("Failed to reload data for %s", entry.entry_id)
        return {
            "status": "error",
            "entry_id": entry.entry_id,
            "error": str(exception),
            "timestamp": dt_util.now().isoformat(),
        }

    duration_ms = (dt_util.now() - started).total_seconds() * 1000
    return {
        "status": "success",
        "entry_id": entry.entry_id,
        "timestamp": dt_util.now().isoformat(),
        "duration_ms": round(duration_ms, 2),
        "last_update_success": coordinator.last_update_success,
    }

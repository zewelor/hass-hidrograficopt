"""Service registration for hidrograficopt."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from custom_components.hidrograficopt.const import DOMAIN, LOGGER
from custom_components.hidrograficopt.data import InstitutoHidrogrficoConfigEntry
from custom_components.hidrograficopt.service_actions.reload_data import async_handle_reload_data
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import ServiceValidationError

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

SERVICE_RELOAD_DATA = "reload_data"


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register integration services."""

    async def handle_reload_data(call: ServiceCall) -> ServiceResponse:
        entries = [
            cast(InstitutoHidrogrficoConfigEntry, entry)
            for entry in hass.config_entries.async_entries(DOMAIN)
            if entry.state is ConfigEntryState.LOADED
        ]
        if not entries:
            msg = f"No loaded config entries found for {DOMAIN}"
            raise ServiceValidationError(msg)

        results: dict[str, ServiceResponse] = {}
        for entry in entries:
            results[entry.entry_id] = await async_handle_reload_data(hass, entry, call)

        return cast(ServiceResponse, {"status": "ok", "results": results})

    if not hass.services.has_service(DOMAIN, SERVICE_RELOAD_DATA):
        hass.services.async_register(
            DOMAIN,
            SERVICE_RELOAD_DATA,
            handle_reload_data,
            supports_response=SupportsResponse.OPTIONAL,
        )

    LOGGER.debug("Registered services for %s", DOMAIN)

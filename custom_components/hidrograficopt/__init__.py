"""The hidrograficopt integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import InstitutoHidrogrficoApiClient
from .const import CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES, DOMAIN, LOGGER
from .coordinator import InstitutoHidrogrficoDataUpdateCoordinator
from .data import InstitutoHidrogrficoData
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import InstitutoHidrogrficoConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration from YAML (service registration only)."""
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
) -> bool:
    """Set up hidrograficopt from a config entry."""
    client = InstitutoHidrogrficoApiClient(async_get_clientsession(hass))

    update_interval_minutes = int(
        entry.options.get(
            CONF_UPDATE_INTERVAL_MINUTES,
            DEFAULT_UPDATE_INTERVAL_MINUTES,
        )
    )

    coordinator = InstitutoHidrogrficoDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=timedelta(minutes=update_interval_minutes),
        always_update=False,
    )

    entry.runtime_data = InstitutoHidrogrficoData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
) -> None:
    """Reload a config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

"""The hidrograficopt integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import InstitutoHidrogrficoApiClient, normalize_timezone_name
from .const import (
    CONF_PORT_ID,
    CONF_STATION_NAME,
    CONF_STATION_TIMEZONE,
    CONF_UPDATE_INTERVAL_MINUTES,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
    LOGGER,
)
from .coordinator import InstitutoHidrogrficoDataUpdateCoordinator
from .data import InstitutoHidrogrficoData
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import InstitutoHidrogrficoConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR]
CURRENT_CONFIG_VERSION = 3

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


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry data to the current schema."""
    if entry.version > CURRENT_CONFIG_VERSION:
        LOGGER.error(
            "Cannot migrate %s entry %s from unsupported future version %s",
            DOMAIN,
            entry.entry_id,
            entry.version,
        )
        return False

    if entry.version == CURRENT_CONFIG_VERSION:
        return True

    data = dict(entry.data)
    port_id_raw = data.get(CONF_PORT_ID, entry.unique_id)

    try:
        port_id = int(port_id_raw)
    except (TypeError, ValueError):
        LOGGER.error("Cannot migrate %s entry %s: missing valid port_id", DOMAIN, entry.entry_id)
        return False

    migrated_station_name = str(data.get(CONF_STATION_NAME) or entry.title or f"Port {port_id}")
    migrated_station_timezone = normalize_timezone_name(
        str(data.get(CONF_STATION_TIMEZONE)) if data.get(CONF_STATION_TIMEZONE) else None
    )
    if migrated_station_timezone is None:
        migrated_station_timezone = normalize_timezone_name(hass.config.time_zone) or "UTC"

    data[CONF_PORT_ID] = port_id
    data[CONF_STATION_NAME] = migrated_station_name
    data[CONF_STATION_TIMEZONE] = migrated_station_timezone

    hass.config_entries.async_update_entry(
        entry,
        version=CURRENT_CONFIG_VERSION,
        data=data,
    )
    LOGGER.info("Migrated %s entry %s to version %s", DOMAIN, entry.entry_id, CURRENT_CONFIG_VERSION)
    return True

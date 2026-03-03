"""Validation helpers for HMAPI config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.hidrograficopt.api import InstitutoHidrogrficoApiClient, InstitutoHidrogrficoApiClientDataError
from custom_components.hidrograficopt.const import DEFAULT_PERIOD_DAYS
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_port_id(hass: HomeAssistant, port_id: int) -> None:
    """Validate whether station id returns tide data."""
    client = InstitutoHidrogrficoApiClient(async_create_clientsession(hass))
    timezone = dt_util.get_time_zone(hass.config.time_zone) or dt_util.UTC
    events = await client.async_get_tide_events(
        port_id=port_id,
        timezone=timezone,
        period_days=DEFAULT_PERIOD_DAYS,
    )

    if not events:
        msg = f"No tide events returned for port_id={port_id}"
        raise InstitutoHidrogrficoApiClientDataError(msg)

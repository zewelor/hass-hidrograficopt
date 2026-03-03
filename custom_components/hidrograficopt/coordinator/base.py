"""DataUpdateCoordinator for HMAPI tides."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.hidrograficopt.api import (
    InstitutoHidrogrficoApiClientCommunicationError,
    InstitutoHidrogrficoApiClientDataError,
    InstitutoHidrogrficoApiClientError,
    TideDirection,
    TideEvent,
    TideType,
)
from custom_components.hidrograficopt.const import CONF_PORT_ID, CONF_STATION_NAME, DEFAULT_PERIOD_DAYS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from custom_components.hidrograficopt.data import InstitutoHidrogrficoConfigEntry


class InstitutoHidrogrficoDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that fetches and derives tide data for one station."""

    config_entry: InstitutoHidrogrficoConfigEntry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch station data and compute derived fields."""
        try:
            port_id = int(self.config_entry.data[CONF_PORT_ID])
            station_name = str(self.config_entry.data.get(CONF_STATION_NAME, f"Port {port_id}"))
            timezone = dt_util.get_time_zone(self.hass.config.time_zone) or dt_util.UTC
            now = dt_util.now()

            events = await self.config_entry.runtime_data.client.async_get_tide_events(
                port_id=port_id,
                timezone=timezone,
                period_days=DEFAULT_PERIOD_DAYS,
            )

            upcoming_events = [event for event in events if event.time >= now]
            next_high = _find_next_tide(upcoming_events, TideType.HIGH)
            next_low = _find_next_tide(upcoming_events, TideType.LOW)
            tide_status = _resolve_tide_direction(upcoming_events)
            data = {
                "port_id": port_id,
                "station_name": station_name,
                "events": events,
                "upcoming_events": upcoming_events,
                "next_high": next_high,
                "next_low": next_low,
                "tide_status": tide_status,
                "last_update": now,
            }
        except (InstitutoHidrogrficoApiClientCommunicationError, InstitutoHidrogrficoApiClientDataError) as exception:
            raise UpdateFailed(str(exception)) from exception
        except InstitutoHidrogrficoApiClientError as exception:
            raise UpdateFailed(str(exception)) from exception
        return data


def _find_next_tide(events: list[TideEvent], tide_type: TideType) -> TideEvent | None:
    """Return nearest upcoming tide for a given tide type."""
    for event in events:
        if event.tide_type == tide_type:
            return event
    return None


def _resolve_tide_direction(events: list[TideEvent]) -> TideDirection:
    """Resolve tide direction from nearest upcoming event."""
    if not events:
        return TideDirection.UNKNOWN

    first_upcoming = events[0]
    if first_upcoming.tide_type == TideType.HIGH:
        return TideDirection.RISING
    if first_upcoming.tide_type == TideType.LOW:
        return TideDirection.FALLING

    return TideDirection.UNKNOWN

"""HTTP client for Instituto Hidrografico HMAPI."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp

from custom_components.hidrograficopt.const import DEFAULT_PERIOD_DAYS, HMAPI_BASE_URL

from .models import TideEvent, TideStation
from .parsers import parse_stations, parse_tide_events


class InstitutoHidrogrficoApiClientError(Exception):
    """Base exception for HMAPI client errors."""


class InstitutoHidrogrficoApiClientCommunicationError(InstitutoHidrogrficoApiClientError):
    """Communication-level error with HMAPI."""


class InstitutoHidrogrficoApiClientDataError(InstitutoHidrogrficoApiClientError):
    """Unexpected or invalid HMAPI response payload."""


class InstitutoHidrogrficoApiClient:
    """Thin async HTTP client for HMAPI endpoints."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize client with shared Home Assistant session."""
        self._session = session

    async def async_get_stations(self) -> list[TideStation]:
        """Return all stations from HMAPI /tides endpoint."""
        payload = await self._api_get_json("/tides/")
        stations = parse_stations(payload)
        if not stations:
            msg = "Station list is empty or invalid"
            raise InstitutoHidrogrficoApiClientDataError(msg)
        return stations

    async def async_get_tide_events(
        self,
        *,
        port_id: int,
        timezone: Any,
        period_days: int = DEFAULT_PERIOD_DAYS,
    ) -> list[TideEvent]:
        """Return parsed tide events for a station."""
        payload = await self._api_get_json(
            "/tidestation/",
            params={
                "portID": port_id,
                "period": period_days,
            },
        )
        return parse_tide_events(payload, timezone)

    async def _api_get_json(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute HMAPI GET request and return decoded JSON."""
        url = f"{HMAPI_BASE_URL}{endpoint}"

        try:
            async with asyncio.timeout(15):
                response = await self._session.get(url, params=params)

            response.raise_for_status()

            try:
                return await response.json(content_type=None)
            except (aiohttp.ContentTypeError, ValueError) as exception:
                msg = f"Invalid JSON payload from HMAPI endpoint {endpoint}"
                raise InstitutoHidrogrficoApiClientDataError(msg) from exception

        except TimeoutError as exception:
            msg = f"Timeout while contacting HMAPI endpoint {endpoint}"
            raise InstitutoHidrogrficoApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Communication error for HMAPI endpoint {endpoint}: {exception}"
            raise InstitutoHidrogrficoApiClientCommunicationError(msg) from exception

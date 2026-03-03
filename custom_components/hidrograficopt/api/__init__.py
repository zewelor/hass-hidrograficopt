"""Exports for the HMAPI client package."""

from .client import (
    InstitutoHidrogrficoApiClient,
    InstitutoHidrogrficoApiClientCommunicationError,
    InstitutoHidrogrficoApiClientDataError,
    InstitutoHidrogrficoApiClientError,
)
from .models import TideDirection, TideEvent, TideStation, TideType
from .timezone import normalize_timezone_name, resolve_timezone_from_coordinates

__all__ = [
    "InstitutoHidrogrficoApiClient",
    "InstitutoHidrogrficoApiClientCommunicationError",
    "InstitutoHidrogrficoApiClientDataError",
    "InstitutoHidrogrficoApiClientError",
    "TideDirection",
    "TideEvent",
    "TideStation",
    "TideType",
    "normalize_timezone_name",
    "resolve_timezone_from_coordinates",
]

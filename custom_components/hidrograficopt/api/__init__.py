"""Exports for the HMAPI client package."""

from .client import (
    InstitutoHidrogrficoApiClient,
    InstitutoHidrogrficoApiClientCommunicationError,
    InstitutoHidrogrficoApiClientDataError,
    InstitutoHidrogrficoApiClientError,
)
from .models import TideDirection, TideEvent, TideStation, TideType

__all__ = [
    "InstitutoHidrogrficoApiClient",
    "InstitutoHidrogrficoApiClientCommunicationError",
    "InstitutoHidrogrficoApiClientDataError",
    "InstitutoHidrogrficoApiClientError",
    "TideDirection",
    "TideEvent",
    "TideStation",
    "TideType",
]

"""
API package for hidrograficopt.

Architecture:
    Three-layer data flow: Entities → Coordinator → API Client.
    Only the coordinator should call the API client. Entities must never
    import or call the API client directly.

Exception hierarchy:
    InstitutoHidrogrficoApiClientError (base)
    ├── InstitutoHidrogrficoApiClientCommunicationError (network/timeout)
    └── InstitutoHidrogrficoApiClientAuthenticationError (401/403)

Coordinator exception mapping:
    ApiClientAuthenticationError → ConfigEntryAuthFailed (triggers reauth)
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError             → UpdateFailed (auto-retry)
"""

from .client import (
    InstitutoHidrogrficoApiClient,
    InstitutoHidrogrficoApiClientAuthenticationError,
    InstitutoHidrogrficoApiClientCommunicationError,
    InstitutoHidrogrficoApiClientError,
)

__all__ = [
    "InstitutoHidrogrficoApiClient",
    "InstitutoHidrogrficoApiClientAuthenticationError",
    "InstitutoHidrogrficoApiClientCommunicationError",
    "InstitutoHidrogrficoApiClientError",
]

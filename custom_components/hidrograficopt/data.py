"""Runtime data types for hidrograficopt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import InstitutoHidrogrficoApiClient
    from .coordinator import InstitutoHidrogrficoDataUpdateCoordinator


type InstitutoHidrogrficoConfigEntry = ConfigEntry[InstitutoHidrogrficoData]


@dataclass
class InstitutoHidrogrficoData:
    """Runtime data for hidrograficopt config entries."""

    client: InstitutoHidrogrficoApiClient
    coordinator: InstitutoHidrogrficoDataUpdateCoordinator
    integration: Integration

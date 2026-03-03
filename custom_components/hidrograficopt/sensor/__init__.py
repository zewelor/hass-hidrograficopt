"""Sensor platform for hidrograficopt."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.hidrograficopt.const import PARALLEL_UPDATES as PARALLEL_UPDATES

from .tide import ENTITY_DESCRIPTIONS, InstitutoHidrogrficoTideSensor

if TYPE_CHECKING:
    from custom_components.hidrograficopt.data import InstitutoHidrogrficoConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InstitutoHidrogrficoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities for one config entry."""
    async_add_entities(
        InstitutoHidrogrficoTideSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )

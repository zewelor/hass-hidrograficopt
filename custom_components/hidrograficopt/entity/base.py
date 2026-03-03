"""Base entity for hidrograficopt sensors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.hidrograficopt.const import ATTRIBUTION, HMAPI_WEBSITE_URL
from custom_components.hidrograficopt.coordinator import InstitutoHidrogrficoDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class InstitutoHidrogrficoEntity(CoordinatorEntity[InstitutoHidrogrficoDataUpdateCoordinator]):
    """Shared entity behavior for all hidrograficopt entities."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: InstitutoHidrogrficoDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        station_name = str(coordinator.config_entry.data.get("station_name", coordinator.config_entry.title))
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.domain, coordinator.config_entry.entry_id)},
            name=station_name,
            manufacturer="Instituto Hidrografico",
            model="HMAPI Tide Station",
            serial_number=str(coordinator.config_entry.data.get("port_id", "unknown")),
            configuration_url=HMAPI_WEBSITE_URL,
        )

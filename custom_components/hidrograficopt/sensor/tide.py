"""Tide sensors for hidrograficopt."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from custom_components.hidrograficopt.api import TideDirection
from custom_components.hidrograficopt.entity import InstitutoHidrogrficoEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import UnitOfLength

if TYPE_CHECKING:
    from custom_components.hidrograficopt.api import TideEvent
    from custom_components.hidrograficopt.coordinator import InstitutoHidrogrficoDataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="next_high_tide_time",
        translation_key="next_high_tide_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:arrow-up-bold-outline",
        has_entity_name=True,
    ),
    SensorEntityDescription(
        key="next_high_tide_height",
        translation_key="next_high_tide_height",
        native_unit_of_measurement=UnitOfLength.METERS,
        icon="mdi:ruler",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        has_entity_name=True,
    ),
    SensorEntityDescription(
        key="next_low_tide_time",
        translation_key="next_low_tide_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:arrow-down-bold-outline",
        has_entity_name=True,
    ),
    SensorEntityDescription(
        key="next_low_tide_height",
        translation_key="next_low_tide_height",
        native_unit_of_measurement=UnitOfLength.METERS,
        icon="mdi:ruler",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        has_entity_name=True,
    ),
    SensorEntityDescription(
        key="tide_status",
        translation_key="tide_status",
        device_class=SensorDeviceClass.ENUM,
        options=[direction.value for direction in TideDirection],
        icon="mdi:waves",
        has_entity_name=True,
    ),
)


class InstitutoHidrogrficoTideSensor(SensorEntity, InstitutoHidrogrficoEntity):
    """Represents one derived tide sensor value."""

    def __init__(
        self,
        coordinator: InstitutoHidrogrficoDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize tide sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def native_value(self) -> datetime | float | str | None:
        """Return the current value for this sensor key."""
        next_high = self.coordinator.data.get("next_high")
        next_low = self.coordinator.data.get("next_low")
        tide_status = self.coordinator.data.get("tide_status")

        if self.entity_description.key == "next_high_tide_time":
            return next_high.time if next_high else None

        if self.entity_description.key == "next_high_tide_height":
            return next_high.height_m if next_high else None

        if self.entity_description.key == "next_low_tide_time":
            return next_low.time if next_low else None

        if self.entity_description.key == "next_low_tide_height":
            return next_low.height_m if next_low else None

        if self.entity_description.key == "tide_status":
            return tide_status.value if tide_status else TideDirection.UNKNOWN.value

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional attributes for status sensor."""
        if self.entity_description.key != "tide_status":
            return None

        events: list[TideEvent] = self.coordinator.data.get("events", [])
        serialized_events = [
            {
                "time": event.time.isoformat(),
                "height": event.height_m,
                "type": event.tide_type.value,
            }
            for event in events
        ]

        return {
            "port_id": self.coordinator.data.get("port_id"),
            "station_name": self.coordinator.data.get("station_name"),
            "tides": serialized_events,
            "events_count": len(serialized_events),
        }

from __future__ import annotations

from types import SimpleNamespace

import pytest

from custom_components.hidrograficopt.const import (
    CONF_PORT_ID,
    CONF_STATION_NAME,
    CONF_STATION_TIMEZONE,
    CONF_TIMEZONE_OVERRIDE,
)
from custom_components.hidrograficopt.coordinator.base import InstitutoHidrogrficoDataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed


def _build_coordinator(
    *,
    port_id: int = 112,
    station_name: str = "Leixoes",
    option_tz: str | None,
    station_tz: str,
    hass_tz: str,
) -> InstitutoHidrogrficoDataUpdateCoordinator:
    class _StubClient:
        async def async_get_tide_events(self, **_: object) -> list[object]:
            return []

    coordinator = InstitutoHidrogrficoDataUpdateCoordinator.__new__(InstitutoHidrogrficoDataUpdateCoordinator)
    coordinator.config_entry = SimpleNamespace(
        options={CONF_TIMEZONE_OVERRIDE: option_tz},
        data={
            CONF_PORT_ID: port_id,
            CONF_STATION_NAME: station_name,
            CONF_STATION_TIMEZONE: station_tz,
        },
        runtime_data=SimpleNamespace(client=_StubClient()),
    )
    coordinator.hass = SimpleNamespace(config=SimpleNamespace(time_zone=hass_tz))
    return coordinator


@pytest.mark.asyncio
async def test_update_data_uses_option_override_timezone() -> None:
    coordinator = _build_coordinator(
        option_tz="Atlantic/Madeira",
        station_tz="Europe/Lisbon",
        hass_tz="UTC",
    )

    data = await coordinator._async_update_data()  # noqa: SLF001

    assert data["effective_timezone"] == "Atlantic/Madeira"
    assert data["timezone_source"] == "override"


@pytest.mark.asyncio
async def test_update_data_raises_when_all_timezones_invalid() -> None:
    coordinator = _build_coordinator(
        option_tz="Not/AZone",
        station_tz="Invalid/Timezone",
        hass_tz="also-invalid",
    )

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()  # noqa: SLF001

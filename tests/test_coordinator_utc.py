from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from custom_components.hidrograficopt.api import TideEvent, TideType
from custom_components.hidrograficopt.const import CONF_PORT_ID, CONF_STATION_NAME
from custom_components.hidrograficopt.coordinator.base import InstitutoHidrogrficoDataUpdateCoordinator


@pytest.mark.asyncio
async def test_update_data_keeps_hmapi_events_in_utc() -> None:
    event = TideEvent(
        time=datetime(2099, 7, 12, 18, 18, tzinfo=UTC),
        height_m=0.53,
        tide_type=TideType.LOW,
    )

    class _StubClient:
        async def async_get_tide_events(self, **kwargs: object) -> list[TideEvent]:
            assert kwargs == {"port_id": 112, "period_days": 7}
            return [event]

    coordinator = InstitutoHidrogrficoDataUpdateCoordinator.__new__(InstitutoHidrogrficoDataUpdateCoordinator)
    coordinator.config_entry = SimpleNamespace(
        data={CONF_PORT_ID: 112, CONF_STATION_NAME: "Funchal"},
        runtime_data=SimpleNamespace(client=_StubClient()),
    )

    data = await coordinator._async_update_data()  # noqa: SLF001

    assert data["next_low"] == event
    assert data["source_timezone"] == "UTC"

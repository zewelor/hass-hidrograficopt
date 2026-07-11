from __future__ import annotations

from types import SimpleNamespace

import pytest

from custom_components.hidrograficopt.__init__ import async_migrate_entry
from custom_components.hidrograficopt.const import CONF_PORT_ID, CONF_STATION_NAME, CONF_UPDATE_INTERVAL_MINUTES


class _FakeConfigEntries:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def async_update_entry(self, entry: object, **kwargs: object) -> None:
        self.calls.append({"entry": entry, "kwargs": kwargs})


@pytest.mark.asyncio
async def test_async_migrate_entry_populates_required_fields_and_removes_timezones() -> None:
    config_entries = _FakeConfigEntries()
    hass = SimpleNamespace(
        config=SimpleNamespace(time_zone="Europe/Lisbon"),
        config_entries=config_entries,
    )
    entry = SimpleNamespace(
        version=2,
        entry_id="entry-1",
        unique_id="112",
        title="Leixoes",
        data={},
        options={},
        domain="hidrograficopt",
    )

    migrated = await async_migrate_entry(hass, entry)

    assert migrated is True
    assert len(config_entries.calls) == 1
    kwargs = config_entries.calls[0]["kwargs"]
    assert kwargs["version"] == 4
    data = kwargs["data"]
    assert isinstance(data, dict)
    assert data[CONF_PORT_ID] == 112
    assert data[CONF_STATION_NAME] == "Leixoes"
    assert "station_timezone" not in data
    assert kwargs["options"] == {}


@pytest.mark.asyncio
async def test_async_migrate_entry_removes_legacy_timezone_settings() -> None:
    config_entries = _FakeConfigEntries()
    hass = SimpleNamespace(config_entries=config_entries)
    entry = SimpleNamespace(
        version=3,
        entry_id="entry-legacy-timezone",
        unique_id="112",
        title="Funchal",
        data={
            CONF_PORT_ID: 112,
            CONF_STATION_NAME: "Funchal",
            "station_timezone": "Europe/Lisbon",
        },
        options={
            CONF_UPDATE_INTERVAL_MINUTES: 30,
            "timezone_override": "Atlantic/Madeira",
        },
        domain="hidrograficopt",
    )

    migrated = await async_migrate_entry(hass, entry)

    assert migrated is True
    kwargs = config_entries.calls[0]["kwargs"]
    assert kwargs["version"] == 4
    assert kwargs["data"] == {CONF_PORT_ID: 112, CONF_STATION_NAME: "Funchal"}
    assert kwargs["options"] == {CONF_UPDATE_INTERVAL_MINUTES: 30}


@pytest.mark.asyncio
async def test_async_migrate_entry_rejects_invalid_port_id() -> None:
    config_entries = _FakeConfigEntries()
    hass = SimpleNamespace(
        config=SimpleNamespace(time_zone="Europe/Lisbon"),
        config_entries=config_entries,
    )
    entry = SimpleNamespace(
        version=2,
        entry_id="entry-2",
        unique_id="not-an-int",
        title="Fallback title",
        data={},
        options={},
        domain="hidrograficopt",
    )

    migrated = await async_migrate_entry(hass, entry)

    assert migrated is False
    assert config_entries.calls == []

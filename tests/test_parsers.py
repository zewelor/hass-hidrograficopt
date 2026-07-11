from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from custom_components.hidrograficopt.api import TideType
from custom_components.hidrograficopt.api.parsers import parse_tide_events


def test_parse_funchal_fuso_zero_timestamp_as_utc() -> None:
    events = parse_tide_events(
        [
            {
                "date": "2026-07-12 18:18:00",
                "height": 0.53,
                "tide": "BM",
            }
        ]
    )

    assert len(events) == 1
    event = events[0]
    assert event.time == datetime(2026, 7, 12, 18, 18, tzinfo=UTC)
    assert event.time.astimezone(ZoneInfo("Atlantic/Madeira")) == datetime(
        2026,
        7,
        12,
        19,
        18,
        tzinfo=ZoneInfo("Atlantic/Madeira"),
    )
    assert event.height_m == 0.53
    assert event.tide_type is TideType.LOW


def test_parse_fuso_zero_timestamp_is_utc_in_winter() -> None:
    events = parse_tide_events([{"date": "2026-12-01 18:18", "height": 0.6, "tide": "PM"}])

    assert events[0].time == datetime(2026, 12, 1, 18, 18, tzinfo=UTC)
    assert events[0].time.astimezone(ZoneInfo("Atlantic/Madeira")).hour == 18


def test_parse_offset_aware_timestamp_normalizes_to_utc() -> None:
    events = parse_tide_events([{"date": "2026-07-12T18:18:00+01:00", "height": 0.6, "tide": "PM"}])

    assert events[0].time == datetime(2026, 7, 12, 17, 18, tzinfo=UTC)

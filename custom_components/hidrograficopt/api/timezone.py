"""Timezone helpers for HMAPI stations."""

from __future__ import annotations

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from timezonefinder import TimezoneFinder

_TIMEZONE_FINDER = TimezoneFinder(in_memory=True)


def normalize_timezone_name(value: str | None) -> str | None:
    """Normalize and validate an IANA timezone name."""
    if value is None:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    try:
        ZoneInfo(normalized)
    except ZoneInfoNotFoundError:
        return None

    return normalized


def resolve_timezone_from_coordinates(latitude: float | None, longitude: float | None) -> str | None:
    """Resolve IANA timezone from station coordinates."""
    if latitude is None or longitude is None:
        return None

    timezone_name = _TIMEZONE_FINDER.timezone_at(lat=latitude, lng=longitude)
    if timezone_name is None:
        return None

    return normalize_timezone_name(timezone_name)

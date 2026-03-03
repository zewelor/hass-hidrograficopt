"""Timezone helpers for HMAPI stations."""

from __future__ import annotations

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


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

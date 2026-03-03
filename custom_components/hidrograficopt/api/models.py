"""HMAPI domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TideDirection(StrEnum):
    """Direction of the tide movement."""

    RISING = "rising"
    FALLING = "falling"
    UNKNOWN = "unknown"


class TideType(StrEnum):
    """Type of tide event."""

    HIGH = "high"
    LOW = "low"


@dataclass(frozen=True, slots=True)
class TideStation:
    """Station metadata from /tides endpoint."""

    port_id: int
    name: str
    maregraph: str | None
    longitude: float | None
    latitude: float | None


@dataclass(frozen=True, slots=True)
class TideEvent:
    """A parsed and normalized tide event."""

    time: datetime
    height_m: float
    tide_type: TideType

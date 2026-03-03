"""Parsers for HMAPI responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .models import TideEvent, TideStation, TideType

_DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M")


def parse_stations(payload: Any) -> list[TideStation]:
    """Parse /tides GeoJSON payload into station models."""
    if not isinstance(payload, dict):
        return []

    features = payload.get("features")
    if not isinstance(features, list):
        return []

    stations: list[TideStation] = []
    for feature in features:
        if not isinstance(feature, dict):
            continue

        properties = feature.get("properties")
        if not isinstance(properties, dict):
            continue

        port_id = properties.get("CODP")
        name = properties.get("PORTO")
        if not isinstance(port_id, int) or not isinstance(name, str):
            continue

        geometry = feature.get("geometry")
        longitude: float | None = None
        latitude: float | None = None
        if isinstance(geometry, dict):
            coordinates = geometry.get("coordinates")
            if (
                isinstance(coordinates, list)
                and len(coordinates) >= 2
                and isinstance(coordinates[0], int | float)
                and isinstance(coordinates[1], int | float)
            ):
                longitude = float(coordinates[0])
                latitude = float(coordinates[1])

        maregraph = properties.get("MAREGRAPH")
        stations.append(
            TideStation(
                port_id=port_id,
                name=name,
                maregraph=maregraph if isinstance(maregraph, str) else None,
                longitude=longitude,
                latitude=latitude,
            )
        )

    return sorted(stations, key=lambda station: (station.name.casefold(), station.port_id))


def parse_tide_events(payload: Any, timezone: Any) -> list[TideEvent]:
    """Parse /tidestation payload into sorted tide events."""
    if not isinstance(payload, list):
        return []

    events: list[TideEvent] = []

    for item in payload:
        if not isinstance(item, dict):
            continue

        tide = item.get("tide")
        height = item.get("height")
        date_string = item.get("date")

        if not isinstance(tide, str) or height is None or not isinstance(date_string, str):
            continue

        tide_type: TideType | None = None
        tide_code = tide.upper()
        if tide_code == "PM":
            tide_type = TideType.HIGH
        elif tide_code == "BM":
            tide_type = TideType.LOW

        if tide_type is None:
            continue

        parsed_datetime: datetime | None = None
        for date_format in _DATE_FORMATS:
            try:
                parsed_datetime = datetime.strptime(date_string, date_format)
                break
            except ValueError:
                continue

        if parsed_datetime is None:
            continue

        if parsed_datetime.tzinfo is None:
            parsed_datetime = parsed_datetime.replace(tzinfo=timezone)

        try:
            height_m = round(float(height), 2)
        except (TypeError, ValueError):
            continue

        events.append(
            TideEvent(
                time=parsed_datetime,
                height_m=height_m,
                tide_type=tide_type,
            )
        )

    return sorted(events, key=lambda event: event.time)

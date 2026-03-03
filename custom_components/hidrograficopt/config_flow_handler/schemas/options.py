"""Schema for options flow."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.hidrograficopt.const import CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES
from homeassistant.helpers import selector


def get_options_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """Return options flow schema."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Optional(
                CONF_UPDATE_INTERVAL_MINUTES,
                default=defaults.get(
                    CONF_UPDATE_INTERVAL_MINUTES,
                    DEFAULT_UPDATE_INTERVAL_MINUTES,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=5,
                    max=360,
                    step=5,
                    unit_of_measurement="min",
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

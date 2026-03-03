"""Schemas for user and reconfigure steps."""

from __future__ import annotations

import voluptuous as vol

from custom_components.hidrograficopt.const import CONF_PORT_ID
from homeassistant.helpers import selector


def _port_selector_options(port_options: list[selector.SelectOptionDict]) -> selector.SelectSelector:
    """Build station selector from options list."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=port_options,
            mode=selector.SelectSelectorMode.DROPDOWN,
            custom_value=False,
            sort=False,
        )
    )


def get_user_schema(
    *,
    port_options: list[selector.SelectOptionDict],
    default_port_id: int | None = None,
) -> vol.Schema:
    """Build schema for user setup."""
    if port_options:
        default_value = str(default_port_id) if default_port_id is not None else port_options[0]["value"]
        return vol.Schema(
            {
                vol.Required(
                    CONF_PORT_ID,
                    default=default_value,
                ): _port_selector_options(port_options),
            }
        )

    return vol.Schema(
        {
            vol.Required(
                CONF_PORT_ID,
                default=default_port_id if default_port_id is not None else 112,
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=99999,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

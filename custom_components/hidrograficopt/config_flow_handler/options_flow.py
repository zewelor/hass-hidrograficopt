"""Options flow for hidrograficopt."""

from __future__ import annotations

from typing import Any

from custom_components.hidrograficopt.api import normalize_timezone_name
from custom_components.hidrograficopt.config_flow_handler.schemas import get_options_schema
from custom_components.hidrograficopt.const import CONF_TIMEZONE_OVERRIDE
from homeassistant import config_entries


class InstitutoHidrogrficoOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for hidrograficopt."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage integration options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            options_data = dict(user_input)
            timezone_override_raw = options_data.get(CONF_TIMEZONE_OVERRIDE)
            timezone_override = normalize_timezone_name(str(timezone_override_raw) if timezone_override_raw else None)
            if timezone_override_raw and timezone_override is None:
                errors[CONF_TIMEZONE_OVERRIDE] = "invalid_timezone"
            else:
                if timezone_override:
                    options_data[CONF_TIMEZONE_OVERRIDE] = timezone_override
                else:
                    options_data.pop(CONF_TIMEZONE_OVERRIDE, None)

                if not errors:
                    return self.async_create_entry(title="", data=options_data)

        return self.async_show_form(
            step_id="init",
            data_schema=get_options_schema(self.config_entry.options),
            errors=errors,
        )

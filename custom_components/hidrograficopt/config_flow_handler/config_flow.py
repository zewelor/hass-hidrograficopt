"""Config flow for hidrograficopt."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from custom_components.hidrograficopt.api import (
    InstitutoHidrogrficoApiClient,
    InstitutoHidrogrficoApiClientCommunicationError,
    InstitutoHidrogrficoApiClientDataError,
    normalize_timezone_name,
)
from custom_components.hidrograficopt.config_flow_handler.schemas import get_user_schema
from custom_components.hidrograficopt.config_flow_handler.validators import validate_port_id
from custom_components.hidrograficopt.const import CONF_PORT_ID, CONF_STATION_NAME, CONF_STATION_TIMEZONE, DOMAIN
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

if TYPE_CHECKING:
    from custom_components.hidrograficopt.api import TideStation
    from custom_components.hidrograficopt.config_flow_handler.options_flow import InstitutoHidrogrficoOptionsFlow


class InstitutoHidrogrficoConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for hidrograficopt."""

    VERSION = 2

    def __init__(self) -> None:
        """Initialize config flow handler."""
        self._stations: list[TideStation] = []

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> InstitutoHidrogrficoOptionsFlow:
        """Return options flow handler."""
        del config_entry
        from custom_components.hidrograficopt.config_flow_handler.options_flow import (  # noqa: PLC0415
            InstitutoHidrogrficoOptionsFlow,
        )

        return InstitutoHidrogrficoOptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle flow initialized by the user."""
        errors: dict[str, str] = {}

        if not self._stations:
            self._stations = await self._async_fetch_stations()

        if user_input is not None:
            try:
                port_id = int(user_input[CONF_PORT_ID])
                await validate_port_id(self.hass, port_id)
            except ValueError:
                errors["base"] = "invalid_port"
            except InstitutoHidrogrficoApiClientCommunicationError:
                errors["base"] = "connection"
            except InstitutoHidrogrficoApiClientDataError:
                errors["base"] = "invalid_port"
            else:
                station = self._resolve_station(port_id)
                station_name = station.name if station else f"Port {port_id}"
                station_timezone = self._resolve_default_timezone()
                await self.async_set_unique_id(str(port_id))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=station_name,
                    data={
                        CONF_PORT_ID: port_id,
                        CONF_STATION_NAME: station_name,
                        CONF_STATION_TIMEZONE: station_timezone,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=get_user_schema(
                port_options=self._selector_options(),
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle reconfigure flow."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if not self._stations:
            self._stations = await self._async_fetch_stations()

        default_port = entry.data.get(CONF_PORT_ID)

        if user_input is not None:
            try:
                port_id = int(user_input[CONF_PORT_ID])
                await validate_port_id(self.hass, port_id)
            except ValueError:
                errors["base"] = "invalid_port"
            except InstitutoHidrogrficoApiClientCommunicationError:
                errors["base"] = "connection"
            except InstitutoHidrogrficoApiClientDataError:
                errors["base"] = "invalid_port"
            else:
                for existing_entry in self._async_current_entries():
                    if existing_entry.entry_id != entry.entry_id and existing_entry.unique_id == str(port_id):
                        errors["base"] = "already_configured"
                        break

                if not errors:
                    station = self._resolve_station(port_id)
                    station_name = station.name if station else f"Port {port_id}"
                    station_timezone = self._resolve_default_timezone()
                    self.hass.config_entries.async_update_entry(
                        entry,
                        title=station_name,
                        unique_id=str(port_id),
                        data={
                            CONF_PORT_ID: port_id,
                            CONF_STATION_NAME: station_name,
                            CONF_STATION_TIMEZONE: station_timezone,
                        },
                    )
                    await self.hass.config_entries.async_reload(entry.entry_id)
                    return self.async_abort(reason="reconfigure_successful")

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=get_user_schema(
                port_options=self._selector_options(),
                default_port_id=int(default_port) if default_port is not None else None,
            ),
            errors=errors,
        )

    async def _async_fetch_stations(self) -> list[TideStation]:
        """Fetch station list from HMAPI."""
        client = InstitutoHidrogrficoApiClient(async_create_clientsession(self.hass))
        try:
            return await client.async_get_stations()
        except (InstitutoHidrogrficoApiClientCommunicationError, InstitutoHidrogrficoApiClientDataError):
            return []

    def _selector_options(self) -> list[selector.SelectOptionDict]:
        """Convert stations to selector options."""
        return [
            cast(
                selector.SelectOptionDict,
                {
                    "value": str(station.port_id),
                    "label": f"{station.name} ({station.port_id})",
                },
            )
            for station in self._stations
        ]

    def _resolve_station(self, port_id: int) -> TideStation | None:
        """Resolve station model for a given port id."""
        for station in self._stations:
            if station.port_id == port_id:
                return station
        return None

    def _resolve_default_timezone(self) -> str:
        """Resolve default timezone for new entries."""
        hass_timezone = normalize_timezone_name(self.hass.config.time_zone)
        return hass_timezone or "UTC"

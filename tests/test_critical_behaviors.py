from __future__ import annotations

from types import SimpleNamespace

import pytest

from custom_components.hidrograficopt.config_flow_handler.schemas.config import get_user_schema
from custom_components.hidrograficopt.service_actions.reload_data import async_handle_reload_data
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import UpdateFailed


def test_get_user_schema_requires_non_empty_port_options() -> None:
    with pytest.raises(ValueError):
        get_user_schema(port_options=[])


def test_get_user_schema_uses_first_option_if_default_missing() -> None:
    schema = get_user_schema(
        port_options=[
            {"value": "112", "label": "Leixoes (112)"},
            {"value": "113", "label": "Porto (113)"},
        ],
        default_port_id=99999,
    )

    required_key = next(iter(schema.schema))
    assert required_key.default() == "112"


@pytest.mark.asyncio
async def test_reload_data_raises_homeassistant_error_on_refresh_failure() -> None:
    class _FailingCoordinator:
        last_update_success = False

        async def async_request_refresh(self) -> None:
            raise UpdateFailed("upstream unavailable")

    entry = SimpleNamespace(
        entry_id="entry-1",
        runtime_data=SimpleNamespace(coordinator=_FailingCoordinator()),
    )

    with pytest.raises(HomeAssistantError):
        await async_handle_reload_data(
            hass=SimpleNamespace(),
            entry=entry,
            call=SimpleNamespace(),
        )


@pytest.mark.asyncio
async def test_reload_data_returns_success_payload_on_refresh_success() -> None:
    class _OkCoordinator:
        last_update_success = True

        async def async_request_refresh(self) -> None:
            return None

    entry = SimpleNamespace(
        entry_id="entry-2",
        runtime_data=SimpleNamespace(coordinator=_OkCoordinator()),
    )

    response = await async_handle_reload_data(
        hass=SimpleNamespace(),
        entry=entry,
        call=SimpleNamespace(),
    )

    assert response["status"] == "success"
    assert response["entry_id"] == "entry-2"
    assert response["last_update_success"] is True

"""Backward-compatible exports for config flow handler."""

from custom_components.hidrograficopt.config_flow_handler.config_flow import InstitutoHidrogrficoConfigFlowHandler
from custom_components.hidrograficopt.config_flow_handler.options_flow import InstitutoHidrogrficoOptionsFlow

__all__ = [
    "InstitutoHidrogrficoConfigFlowHandler",
    "InstitutoHidrogrficoOptionsFlow",
]

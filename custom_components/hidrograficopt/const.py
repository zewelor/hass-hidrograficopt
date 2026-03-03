"""Constants for the hidrograficopt integration."""

from logging import Logger, getLogger

DOMAIN = "hidrograficopt"
LOGGER: Logger = getLogger(__package__)

ATTRIBUTION = "Data provided by Instituto Hidrografico (www.hidrografico.pt)"

CONF_PORT_ID = "port_id"
CONF_STATION_NAME = "station_name"
CONF_STATION_TIMEZONE = "station_timezone"
CONF_TIMEZONE_OVERRIDE = "timezone_override"
CONF_UPDATE_INTERVAL_MINUTES = "update_interval_minutes"

DEFAULT_UPDATE_INTERVAL_MINUTES = 60
DEFAULT_PERIOD_DAYS = 7

HMAPI_BASE_URL = "https://www.hidrografico.pt/hmapi"
HMAPI_WEBSITE_URL = "https://www.hidrografico.pt/"

PARALLEL_UPDATES = 1

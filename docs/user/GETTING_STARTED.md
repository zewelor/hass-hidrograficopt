# Getting Started

## Prerequisites

- Home Assistant with HACS installed
- Internet access to `www.hidrografico.pt`

> This is an unofficial, community integration and is not officially supported by Instituto Hidrográfico.

## Install via HACS

1. HACS -> Integrations -> Custom repositories
2. Add repository URL: `https://github.com/zewelor/hass-hidrograficopt`
3. Category: `Integration`
4. Install and restart Home Assistant

## Add integration

1. Settings -> Devices & Services -> Add Integration
2. Search for "Instituto Hidrográfico Integration"
3. Pick tide station (or enter `port_id`)
4. (Optional) Set timezone override in integration options if you need a manual timezone
5. Finish setup

## Created entities

- `sensor.*_next_high_tide_time`
- `sensor.*_next_high_tide_height`
- `sensor.*_next_low_tide_time`
- `sensor.*_next_low_tide_height`
- `sensor.*_tide_status`

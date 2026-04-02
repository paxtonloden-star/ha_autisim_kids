# Installation

## HACS install

1. In HACS, open Custom repositories.
2. Add this repository URL.
3. Choose type: Integration.
4. Install Autism Kids Predictability Board.
5. Restart Home Assistant.
6. Add the integration in Settings > Devices & services.
7. In the config flow, choose your kid calendar, family calendar, weather entity, and optional people.
8. In the options flow, add helper entities and request/timer notification behavior.

## Manual setup path

This repo also includes YAML examples if you want to use manual package-based setup instead of the integration.

## Entities to choose during setup

- kid calendar
- family calendar
- weather entity
- optional person entities
- optional helper entities in the integration options

## Dashboard examples

See:
- dashboards/my_day_dashboard.yaml
- dashboards/request_buttons_example.yaml
- dashboards/visual_timer_example.yaml
- dashboards/full_kids_board_example.yaml

The button and number entity IDs in those example dashboards are placeholders. Replace them with the actual entity IDs Home Assistant assigns after the integration is added.

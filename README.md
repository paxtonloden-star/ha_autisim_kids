# Home Assistant Autism Kids

Autism-friendly Home Assistant dashboards and automations for predictability, communication, and transitions.

## Included now

- Home Status Board for Predictability
- Full custom integration under `custom_components/autism_kids`
- Config flow and options flow
- HACS configuration
- HACS and hassfest validation workflows
- Example YAML package and Lovelace dashboard

## Project goals

Build simple, visual, low-demand Home Assistant experiences for kids with autism, including:

- Home Status Board for Predictability
- Nonverbal Request Buttons
- Visual Countdown Timer Board
- future visual schedules, first/then boards, and calm corner tools

## Current starter

The current repo contains a full starter setup for the **Home Status Board for Predictability** as both:
- a HACS-installable custom integration
- standalone YAML examples for manual package-based setups

## Repository layout

```text
custom_components/autism_kids/
packages/
  kids_home_status_board.yaml
dashboards/
  my_day_dashboard.yaml
docs/
  installation.md
  customization.md
  roadmap.md
helpers/
  example-helper-values.yaml
scripts/
  setup-notes.md
screenshots/
  .gitkeep
.github/workflows/
hacs.json
```

## Install overview

1. Add this repository to HACS as a custom repository of type **Integration**.
2. Install **Autism Kids Predictability Board** from HACS.
3. Restart Home Assistant.
4. Add the integration in **Settings > Devices & services**.
5. Choose your calendars, people, weather entity, and helper entities in the config flow.

## Notes

This repo is meant to be practical first: stable layout, large readable cards, and predictable state updates.

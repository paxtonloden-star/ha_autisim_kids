# Home Assistant Autism Kids

Autism-friendly Home Assistant dashboards and automations for predictability, communication, and transitions.

## Included now

- Home Status Board for Predictability
- Home Assistant package YAML
- Lovelace dashboard YAML
- installation and customization docs

## Project goals

Build simple, visual, low-demand Home Assistant experiences for kids with autism, including:

- Home Status Board for Predictability
- Nonverbal Request Buttons
- Visual Countdown Timer Board
- future visual schedules, first/then boards, and calm corner tools

## Current starter

The current repo contains a full starter setup for the **Home Status Board for Predictability**.

It includes:
- Now / Next / Later
- Who is home
- Special change today
- Dinner
- Bedtime
- School tomorrow
- Weather

## Repository layout

```text
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
```

## Install overview

1. Enable Home Assistant packages.
2. Copy the package YAML into `/config/packages/`.
3. Import or paste the dashboard YAML into Lovelace.
4. Replace placeholder entities like calendars, people, and weather.
5. Reload helpers, templates, and automations or restart Home Assistant.

## Notes

This repo is meant to be practical first: stable layout, large readable cards, and predictable state updates.

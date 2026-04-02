# Home Assistant Autism Kids

Autism-friendly Home Assistant dashboards and automations for predictability, communication, and transitions.

## Included now

- Home Status Board for Predictability
- Built-in Nonverbal Request Buttons
- Built-in Visual Countdown Timer Board
- Full custom integration under `custom_components/autism_kids`
- Config flow and richer options flow
- HACS configuration
- HACS and hassfest validation workflows
- Example YAML dashboards and manual package examples

## Project goals

Build simple, visual, low-demand Home Assistant experiences for kids with autism, including:

- Home Status Board for Predictability
- Nonverbal Request Buttons
- Visual Countdown Timer Board
- future visual schedules, first/then boards, and calm corner tools

## Current starter

The current repo contains a starter setup for the **Home Status Board for Predictability**, **Nonverbal Request Buttons**, and **Visual Countdown Timer Board** as both:
- a HACS-installable custom integration
- standalone YAML examples for manual package-based setups

## Repository layout

```text
custom_components/autism_kids/
packages/
  kids_home_status_board.yaml
dashboards/
  my_day_dashboard.yaml
  request_buttons_example.yaml
  full_kids_board_example.yaml
  visual_timer_example.yaml
docs/
  installation.md
  customization.md
  automations.md
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
6. Optionally enable built-in persistent notifications for request buttons and timer completion in the options flow.

## What the integration creates

Sensors:
- Kid Now Activity
- Kid Next Activity
- Kid Later Activity
- Kid Who Is Home
- Kid Special Change Summary
- Kid Dinner Summary
- Kid Bedtime Summary
- Kid School Tomorrow Summary
- Kid Weather Summary
- Kid Last Request
- Kid Last Request Time
- Kid Timer Remaining
- Kid Timer Status
- Kid Timer Label

Buttons:
- Request Help
- Request Drink
- Request Snack
- Request Bathroom
- Request Break
- Request Hug
- Request Quiet
- Request Too Loud
- Request Mad
- Request Sad
- Request All Done
- Start 2 Minute Timer
- Start 5 Minute Timer
- Start 10 Minute Timer
- Start Custom Timer
- Pause Timer
- Resume Timer
- Cancel Timer

Numbers:
- Custom Timer Minutes

## Notes

This repo is meant to be practical first: stable layout, large readable cards, and predictable state updates.

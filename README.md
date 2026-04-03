# Autism Kids Predictability Board

A Home Assistant custom integration focused on autism-friendly, low-demand household dashboards for predictability, transitions, and communication.

## What this integration provides

This integration currently includes three practical building blocks:

- **Home Status Board for Predictability**
  - Now / Next / Later
  - Who is home
  - Special change today
  - Dinner
  - Bedtime
  - School tomorrow
  - Weather
- **Nonverbal Request Buttons**
  - Help, Drink, Snack, Bathroom, Break, Hug, Quiet, Too Loud, Mad, Sad, All Done
- **Visual Countdown Timer Board**
  - 3 preset timer buttons
  - custom timer minutes
  - pause, resume, cancel
  - timer status and remaining time sensors

The design goal is simple, visual, stable UI patterns that can be shown on a wall tablet, dashboard, or family display.

## Installation

### HACS

1. Open **HACS**.
2. Go to **Custom repositories**.
3. Add this repository:
   - `https://github.com/paxtonloden-star/ha_autisim_kids`
4. Select **Integration** as the category.
5. Install **Autism Kids Predictability Board**.
6. Restart Home Assistant.
7. Go to **Settings → Devices & Services → Add Integration**.
8. Search for **Autism Kids Predictability Board**.

### Manual installation

1. Copy `custom_components/autism_kids` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

## Configuration

The config flow will ask for:

- kid calendar
- family calendar
- weather entity
- optional first person entity and display name
- optional second person entity and display name

The options flow lets you configure:

- special change `input_text`
- dinner `input_text`
- bedtime `input_datetime`
- school tomorrow `input_boolean`
- fallback text for now / next / later
- request notifications
- request notification title
- timer notifications
- timer notification title
- preset timer minute values

## Entities created

### Sensors

- `Kid Now Activity`
- `Kid Next Activity`
- `Kid Later Activity`
- `Kid Who Is Home`
- `Kid Special Change Summary`
- `Kid Dinner Summary`
- `Kid Bedtime Summary`
- `Kid School Tomorrow Summary`
- `Kid Weather Summary`
- `Kid Last Request`
- `Kid Last Request Time`
- `Kid Timer Remaining`
- `Kid Timer Remaining Seconds`
- `Kid Timer Status`
- `Kid Timer Label`

### Buttons

- request buttons for communication needs
- timer preset and control buttons

### Number entities

- custom timer minutes

## Example dashboards

The repo includes example Lovelace YAML under `dashboards/`:

- `my_day_dashboard.yaml`
- `request_buttons_example.yaml`
- `visual_timer_example.yaml`
- `full_kids_board_example.yaml`

These example files use placeholder entity IDs in a few places. After installing the integration, replace them with the actual entity IDs Home Assistant creates in your system.

## Design principles

This project is intentionally biased toward autism-friendly UI choices:

- stable placement of controls
- minimal text density
- large tap targets
- predictable labels
- low visual clutter
- optional automation around transitions and communication

## Repository structure

```text
custom_components/autism_kids/
dashboards/
docs/
.github/workflows/
hacs.json
```

## Development status

This is an actively evolving custom integration. The current focus is reliability, HACS compatibility, and practical household use.

## Roadmap

Near-term priorities:

- better calendar sequencing for true Now / Next / Later
- request acknowledgement workflow
- first/then mode
- calmer kid-focused dashboard themes and examples

## Support

Please open an issue for bugs or feature requests.

## License

MIT

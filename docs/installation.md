# Installation

1. Enable Home Assistant packages in configuration.yaml.
2. Copy packages/kids_home_status_board.yaml into /config/packages/.
3. Reload configuration or restart Home Assistant.
4. Create or edit a Lovelace dashboard and paste dashboards/my_day_dashboard.yaml.
5. Replace placeholder entities to match your system.

Entities to update:
- calendar.kid_schedule
- calendar.family
- person.mom
- person.dad
- weather.home

Helpers to set:
- input_text.kid_special_change_text
- input_text.kid_dinner_text
- input_datetime.kid_bedtime
- input_boolean.kid_school_tomorrow

Main sensors created by the package:
- sensor.kid_now_activity
- sensor.kid_next_activity
- sensor.kid_later_activity
- sensor.kid_who_is_home
- sensor.kid_special_change_summary
- sensor.kid_dinner_summary
- sensor.kid_bedtime_summary
- sensor.kid_school_tomorrow_summary
- sensor.kid_weather_summary

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_BEDTIME_HELPER,
    CONF_DINNER_TEXT,
    CONF_FAMILY_CALENDAR,
    CONF_KID_CALENDAR,
    CONF_LATER_FALLBACK,
    CONF_NOW_FALLBACK,
    CONF_NEXT_FALLBACK,
    CONF_PERSON_ONE,
    CONF_PERSON_ONE_NAME,
    CONF_PERSON_TWO,
    CONF_PERSON_TWO_NAME,
    CONF_SCHOOL_TOMORROW,
    CONF_SPECIAL_CHANGE_TEXT,
    CONF_WEATHER,
    DEFAULT_LATER_FALLBACK,
    DEFAULT_NOW_FALLBACK,
    DEFAULT_NEXT_FALLBACK,
    DEFAULT_PERSON_ONE_NAME,
    DEFAULT_PERSON_TWO_NAME,
    DOMAIN,
)


def _user_schema() -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_KID_CALENDAR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="calendar")
            ),
            vol.Required(CONF_FAMILY_CALENDAR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="calendar")
            ),
            vol.Required(CONF_WEATHER): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="weather")
            ),
            vol.Optional(CONF_PERSON_ONE): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="person")
            ),
            vol.Optional(CONF_PERSON_ONE_NAME, default=DEFAULT_PERSON_ONE_NAME): str,
            vol.Optional(CONF_PERSON_TWO): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="person")
            ),
            vol.Optional(CONF_PERSON_TWO_NAME, default=DEFAULT_PERSON_TWO_NAME): str,
        }
    )


def _options_schema(options: dict[str, Any] | None = None) -> vol.Schema:
    options = options or {}
    return vol.Schema(
        {
            vol.Optional(CONF_SPECIAL_CHANGE_TEXT, default=options.get(CONF_SPECIAL_CHANGE_TEXT)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="input_text")
            ),
            vol.Optional(CONF_DINNER_TEXT, default=options.get(CONF_DINNER_TEXT)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="input_text")
            ),
            vol.Optional(CONF_BEDTIME_HELPER, default=options.get(CONF_BEDTIME_HELPER)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="input_datetime")
            ),
            vol.Optional(CONF_SCHOOL_TOMORROW, default=options.get(CONF_SCHOOL_TOMORROW)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="input_boolean")
            ),
            vol.Optional(CONF_NOW_FALLBACK, default=options.get(CONF_NOW_FALLBACK, DEFAULT_NOW_FALLBACK)): str,
            vol.Optional(CONF_NEXT_FALLBACK, default=options.get(CONF_NEXT_FALLBACK, DEFAULT_NEXT_FALLBACK)): str,
            vol.Optional(CONF_LATER_FALLBACK, default=options.get(CONF_LATER_FALLBACK, DEFAULT_LATER_FALLBACK)): str,
        }
    )


class AutismKidsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Autism Kids."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return AutismKidsOptionsFlow()

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Autism Kids Predictability Board",
                data=user_input,
                options={
                    CONF_NOW_FALLBACK: DEFAULT_NOW_FALLBACK,
                    CONF_NEXT_FALLBACK: DEFAULT_NEXT_FALLBACK,
                    CONF_LATER_FALLBACK: DEFAULT_LATER_FALLBACK,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_user_schema(),
            errors=errors,
        )


class AutismKidsOptionsFlow(config_entries.OptionsFlowWithReload):
    """Handle Autism Kids options."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _options_schema(self.config_entry.options),
                self.config_entry.options,
            ),
        )

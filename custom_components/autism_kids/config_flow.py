from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import *


def _user_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_KID_CALENDAR): selector.EntitySelector(selector.EntitySelectorConfig(domain="calendar")),
        vol.Required(CONF_FAMILY_CALENDAR): selector.EntitySelector(selector.EntitySelectorConfig(domain="calendar")),
        vol.Required(CONF_WEATHER): selector.EntitySelector(selector.EntitySelectorConfig(domain="weather")),
        vol.Optional(CONF_PERSON_ONE): selector.EntitySelector(selector.EntitySelectorConfig(domain="person")),
        vol.Optional(CONF_PERSON_ONE_NAME, default=DEFAULT_PERSON_ONE_NAME): str,
        vol.Optional(CONF_PERSON_TWO): selector.EntitySelector(selector.EntitySelectorConfig(domain="person")),
        vol.Optional(CONF_PERSON_TWO_NAME, default=DEFAULT_PERSON_TWO_NAME): str,
    })


def _options_schema(options: dict | None = None) -> vol.Schema:
    options = options or {}
    return vol.Schema({
        vol.Optional(CONF_NOW_FALLBACK, default=options.get(CONF_NOW_FALLBACK, DEFAULT_NOW_FALLBACK)): str,
        vol.Optional(CONF_NEXT_FALLBACK, default=options.get(CONF_NEXT_FALLBACK, DEFAULT_NEXT_FALLBACK)): str,
        vol.Optional(CONF_LATER_FALLBACK, default=options.get(CONF_LATER_FALLBACK, DEFAULT_LATER_FALLBACK)): str,
        vol.Optional(CONF_REQUEST_NOTIFICATIONS, default=options.get(CONF_REQUEST_NOTIFICATIONS, DEFAULT_REQUEST_NOTIFICATIONS)): bool,
        vol.Optional(CONF_REQUEST_NOTIFICATION_TITLE, default=options.get(CONF_REQUEST_NOTIFICATION_TITLE, DEFAULT_REQUEST_NOTIFICATION_TITLE)): str,
        vol.Optional(CONF_TIMER_NOTIFICATIONS, default=options.get(CONF_TIMER_NOTIFICATIONS, DEFAULT_TIMER_NOTIFICATIONS)): bool,
        vol.Optional(CONF_TIMER_NOTIFICATION_TITLE, default=options.get(CONF_TIMER_NOTIFICATION_TITLE, DEFAULT_TIMER_NOTIFICATION_TITLE)): str,
        vol.Optional(CONF_PRESET_1_MINUTES, default=options.get(CONF_PRESET_1_MINUTES, DEFAULT_PRESET_1_MINUTES)): selector.NumberSelector(selector.NumberSelectorConfig(min=1, max=60, step=1, mode=selector.NumberSelectorMode.BOX)),
        vol.Optional(CONF_PRESET_2_MINUTES, default=options.get(CONF_PRESET_2_MINUTES, DEFAULT_PRESET_2_MINUTES)): selector.NumberSelector(selector.NumberSelectorConfig(min=1, max=60, step=1, mode=selector.NumberSelectorMode.BOX)),
        vol.Optional(CONF_PRESET_3_MINUTES, default=options.get(CONF_PRESET_3_MINUTES, DEFAULT_PRESET_3_MINUTES)): selector.NumberSelector(selector.NumberSelectorConfig(min=1, max=60, step=1, mode=selector.NumberSelectorMode.BOX)),
    })


class AutismKidsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Autism Kids Predictability Board", data=user_input, options={
                CONF_NOW_FALLBACK: DEFAULT_NOW_FALLBACK,
                CONF_NEXT_FALLBACK: DEFAULT_NEXT_FALLBACK,
                CONF_LATER_FALLBACK: DEFAULT_LATER_FALLBACK,
                CONF_REQUEST_NOTIFICATIONS: DEFAULT_REQUEST_NOTIFICATIONS,
                CONF_REQUEST_NOTIFICATION_TITLE: DEFAULT_REQUEST_NOTIFICATION_TITLE,
                CONF_TIMER_NOTIFICATIONS: DEFAULT_TIMER_NOTIFICATIONS,
                CONF_TIMER_NOTIFICATION_TITLE: DEFAULT_TIMER_NOTIFICATION_TITLE,
                CONF_PRESET_1_MINUTES: DEFAULT_PRESET_1_MINUTES,
                CONF_PRESET_2_MINUTES: DEFAULT_PRESET_2_MINUTES,
                CONF_PRESET_3_MINUTES: DEFAULT_PRESET_3_MINUTES,
            })
        return self.async_show_form(step_id="user", data_schema=_user_schema(), errors={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AutismKidsOptionsFlow()


class AutismKidsOptionsFlow(config_entries.OptionsFlowWithReload):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        return self.async_show_form(step_id="init", data_schema=self.add_suggested_values_to_schema(_options_schema(self.config_entry.options), self.config_entry.options))

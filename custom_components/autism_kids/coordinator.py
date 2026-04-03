from __future__ import annotations

from datetime import time, timedelta
from logging import getLogger
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import *

_LOGGER = getLogger(__name__)


class AutismKidsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=1))
        self.entry = entry
        self._remove_listeners: list[Any] = []

    def _default_data(self) -> dict[str, Any]:
        return {
            "last_update": self.hass.loop.time(),
            "last_request": "No requests yet",
            "last_request_time": "Not set",
            "timer_running": False,
            "timer_paused": False,
            "timer_finished": False,
            "timer_label": "Timer",
            "timer_duration_seconds": 300,
            "timer_remaining_seconds": 300,
            "timer_end": None,
            "timer_pause_remaining": None,
            "timer_finish_notified": False,
            "custom_timer_minutes": 5.0,
            DATA_SPECIAL_CHANGE_TEXT: "No special changes today",
            DATA_DINNER_TEXT: "Dinner not set",
            DATA_BEDTIME: time(20, 30),
            DATA_SCHOOL_TOMORROW: True,
        }

    async def _async_update_data(self) -> dict[str, Any]:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        updated = {**self._default_data(), **current, "last_update": self.hass.loop.time()}
        if updated["timer_running"] and updated["timer_end"]:
            remaining = int((updated["timer_end"] - dt_util.utcnow()).total_seconds())
            if remaining <= 0:
                updated["timer_running"] = False
                updated["timer_paused"] = False
                updated["timer_finished"] = True
                updated["timer_remaining_seconds"] = 0
                updated["timer_pause_remaining"] = 0
                if not updated.get("timer_finish_notified", False):
                    await self._async_send_timer_notification(updated["timer_label"])
                    updated["timer_finish_notified"] = True
            else:
                updated["timer_remaining_seconds"] = remaining
                updated["timer_finished"] = False
        return updated

    async def async_config_entry_first_refresh(self) -> None:
        await super().async_config_entry_first_refresh()
        self._async_attach_listeners()

    @callback
    def _async_attach_listeners(self) -> None:
        entities = [
            self.entry.data.get(CONF_KID_CALENDAR),
            self.entry.data.get(CONF_FAMILY_CALENDAR),
            self.entry.data.get(CONF_PERSON_ONE),
            self.entry.data.get(CONF_PERSON_TWO),
            self.entry.data.get(CONF_WEATHER),
        ]
        for entity_id in [entity for entity in entities if entity]:
            self._remove_listeners.append(async_track_state_change_event(self.hass, [entity_id], self._handle_source_update))

    @callback
    def _handle_source_update(self, event: Any) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, "last_update": self.hass.loop.time()})

    @callback
    def async_set_last_request(self, request_label: str) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, "last_update": self.hass.loop.time(), "last_request": request_label, "last_request_time": dt_util.now().strftime("%-I:%M %p")})

    @callback
    def async_set_custom_timer_minutes(self, minutes: float) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, "custom_timer_minutes": minutes})

    @callback
    def async_start_timer(self, minutes: float, label: str) -> None:
        seconds = max(int(minutes * 60), 1)
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, "timer_running": True, "timer_paused": False, "timer_finished": False, "timer_label": label, "timer_duration_seconds": seconds, "timer_remaining_seconds": seconds, "timer_end": dt_util.utcnow() + timedelta(seconds=seconds), "timer_pause_remaining": None, "timer_finish_notified": False})

    @callback
    def async_pause_timer(self) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        if not current.get("timer_running") or not current.get("timer_end"):
            return
        remaining = max(int((current["timer_end"] - dt_util.utcnow()).total_seconds()), 0)
        self.async_set_updated_data({**current, "timer_running": False, "timer_paused": True, "timer_finished": False, "timer_remaining_seconds": remaining, "timer_pause_remaining": remaining, "timer_end": None})

    @callback
    def async_resume_timer(self) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        remaining = int(current.get("timer_pause_remaining") or 0)
        if remaining <= 0:
            return
        self.async_set_updated_data({**current, "timer_running": True, "timer_paused": False, "timer_finished": False, "timer_remaining_seconds": remaining, "timer_end": dt_util.utcnow() + timedelta(seconds=remaining), "timer_finish_notified": False})

    @callback
    def async_cancel_timer(self) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, "timer_running": False, "timer_paused": False, "timer_finished": False, "timer_remaining_seconds": current.get("timer_duration_seconds", 0), "timer_end": None, "timer_pause_remaining": None, "timer_finish_notified": False})

    @callback
    def async_set_special_change_text(self, value: str) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, DATA_SPECIAL_CHANGE_TEXT: value})

    @callback
    def async_set_dinner_text(self, value: str) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, DATA_DINNER_TEXT: value})

    @callback
    def async_set_bedtime(self, value: time) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, DATA_BEDTIME: value})

    @callback
    def async_set_school_tomorrow(self, value: bool) -> None:
        current = self.data if isinstance(self.data, dict) else self._default_data()
        self.async_set_updated_data({**current, DATA_SCHOOL_TOMORROW: value})

    async def _async_send_timer_notification(self, label: str) -> None:
        if not self.entry.options.get(CONF_TIMER_NOTIFICATIONS, DEFAULT_TIMER_NOTIFICATIONS):
            return
        await self.hass.services.async_call("persistent_notification", "create", {"title": self.entry.options.get(CONF_TIMER_NOTIFICATION_TITLE, DEFAULT_TIMER_NOTIFICATION_TITLE), "message": f"{label} finished", "notification_id": f"{DOMAIN}_{self.entry.entry_id}_timer_finished"}, blocking=True)

    async def async_send_request_notification(self, request_label: str) -> None:
        if not self.entry.options.get(CONF_REQUEST_NOTIFICATIONS, DEFAULT_REQUEST_NOTIFICATIONS):
            return
        await self.hass.services.async_call("persistent_notification", "create", {"title": self.entry.options.get(CONF_REQUEST_NOTIFICATION_TITLE, DEFAULT_REQUEST_NOTIFICATION_TITLE), "message": f"{request_label} requested", "notification_id": f"{DOMAIN}_{self.entry.entry_id}_{request_label.lower().replace(' ', '_')}"}, blocking=True)

    async def async_shutdown(self) -> None:
        for remove_listener in self._remove_listeners:
            remove_listener()
        self._remove_listeners.clear()

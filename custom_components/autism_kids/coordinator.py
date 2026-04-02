from __future__ import annotations

from datetime import timedelta
from logging import getLogger
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CONF_BEDTIME_HELPER,
    CONF_DINNER_TEXT,
    CONF_FAMILY_CALENDAR,
    CONF_KID_CALENDAR,
    CONF_PERSON_ONE,
    CONF_PERSON_TWO,
    CONF_SCHOOL_TOMORROW,
    CONF_SPECIAL_CHANGE_TEXT,
    CONF_WEATHER,
    DOMAIN,
)

_LOGGER = getLogger(__name__)


class AutismKidsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Autism Kids board state refreshes."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )
        self.entry = entry
        self._remove_listeners: list[Any] = []

    async def _async_update_data(self) -> dict[str, Any]:
        """Refresh the coordinator."""
        current = self.data if isinstance(self.data, dict) else {}
        return {
            **current,
            "last_update": self.hass.loop.time(),
            "last_request": current.get("last_request", "No requests yet"),
            "last_request_time": current.get("last_request_time", "Not set"),
        }

    async def async_config_entry_first_refresh(self) -> None:
        """Refresh and attach listeners."""
        await super().async_config_entry_first_refresh()
        self._async_attach_listeners()

    @callback
    def _async_attach_listeners(self) -> None:
        """Attach entity listeners for reactive updates."""
        entities = [
            self.entry.data.get(CONF_KID_CALENDAR),
            self.entry.data.get(CONF_FAMILY_CALENDAR),
            self.entry.data.get(CONF_PERSON_ONE),
            self.entry.data.get(CONF_PERSON_TWO),
            self.entry.data.get(CONF_WEATHER),
            self.entry.options.get(CONF_SPECIAL_CHANGE_TEXT),
            self.entry.options.get(CONF_DINNER_TEXT),
            self.entry.options.get(CONF_BEDTIME_HELPER),
            self.entry.options.get(CONF_SCHOOL_TOMORROW),
        ]
        for entity_id in [entity for entity in entities if entity]:
            self._remove_listeners.append(
                async_track_state_change_event(
                    self.hass,
                    [entity_id],
                    self._handle_source_update,
                )
            )

    @callback
    def _handle_source_update(self, event: Any) -> None:
        """Handle source state updates."""
        current = self.data if isinstance(self.data, dict) else {}
        self.async_set_updated_data(
            {
                **current,
                "last_update": self.hass.loop.time(),
            }
        )

    @callback
    def async_set_last_request(self, request_label: str) -> None:
        """Update the in-memory request state."""
        current = self.data if isinstance(self.data, dict) else {}
        self.async_set_updated_data(
            {
                **current,
                "last_update": self.hass.loop.time(),
                "last_request": request_label,
                "last_request_time": dt_util.now().strftime("%-I:%M %p"),
            }
        )

    async def async_shutdown(self) -> None:
        """Clean up listeners."""
        for remove_listener in self._remove_listeners:
            remove_listener()
        self._remove_listeners.clear()

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    DEFAULT_NEXT_FALLBACK,
    DEFAULT_NOW_FALLBACK,
    DOMAIN,
)
from .coordinator import AutismKidsCoordinator


@dataclass(frozen=True, kw_only=True)
class AutismKidsSensorDescription(SensorEntityDescription):
    value_fn: Callable[[HomeAssistant, ConfigEntry, AutismKidsCoordinator], str | int]


def _state(hass: HomeAssistant, entity_id: str | None) -> str:
    if not entity_id:
        return ""
    state = hass.states.get(entity_id)
    return "" if state is None else str(state.state)


def _attr(hass: HomeAssistant, entity_id: str | None, attr_name: str) -> str | None:
    if not entity_id:
        return None
    state = hass.states.get(entity_id)
    if state is None:
        return None
    value = state.attributes.get(attr_name)
    return None if value is None else str(value)


def _format_hhmmss(total_seconds: int) -> str:
    total_seconds = max(total_seconds, 0)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def _kid_now(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    calendar_id = entry.data.get(CONF_KID_CALENDAR)
    msg = _attr(hass, calendar_id, "message")
    state = _state(hass, calendar_id)
    if state == "on" and msg:
        return msg
    return entry.options.get(CONF_NOW_FALLBACK, DEFAULT_NOW_FALLBACK)


def _kid_next(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    calendar_id = entry.data.get(CONF_FAMILY_CALENDAR)
    msg = _attr(hass, calendar_id, "message")
    start_time = _attr(hass, calendar_id, "start_time")
    if msg and start_time:
        return msg
    return entry.options.get(CONF_NEXT_FALLBACK, DEFAULT_NEXT_FALLBACK)


def _kid_later(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return entry.options.get(CONF_LATER_FALLBACK, DEFAULT_LATER_FALLBACK)


def _kid_home(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    names: list[str] = []
    if entry.data.get(CONF_PERSON_ONE) and _state(hass, entry.data.get(CONF_PERSON_ONE)) == "home":
        names.append(entry.data.get(CONF_PERSON_ONE_NAME, "Person 1"))
    if entry.data.get(CONF_PERSON_TWO) and _state(hass, entry.data.get(CONF_PERSON_TWO)) == "home":
        names.append(entry.data.get(CONF_PERSON_TWO_NAME, "Person 2"))
    if not names:
        return "No one is home"
    if len(names) == 1:
        return f"{names[0]} is home"
    return f"{names[0]} and {names[1]} are home"


def _special_change(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    text = _state(hass, entry.options.get(CONF_SPECIAL_CHANGE_TEXT))
    return "No special changes today" if text in {"", "unknown", "unavailable", "none"} else text


def _dinner(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    text = _state(hass, entry.options.get(CONF_DINNER_TEXT))
    return "Dinner not set" if text in {"", "unknown", "unavailable", "none"} else text


def _bedtime(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    text = _state(hass, entry.options.get(CONF_BEDTIME_HELPER))
    return "Bedtime not set" if text in {"", "unknown", "unavailable", "none"} else f"Bedtime at {text[:5]}"


def _school_tomorrow(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return "School tomorrow" if _state(hass, entry.options.get(CONF_SCHOOL_TOMORROW)) == "on" else "No school tomorrow"


def _weather(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    condition = _state(hass, entry.data.get(CONF_WEATHER))
    temp = _attr(hass, entry.data.get(CONF_WEATHER), "temperature")
    if condition in {"", "unknown", "unavailable"}:
        return "Weather unavailable"
    return f"{condition.replace('_', ' ').title()}, {temp}°" if temp else condition.replace("_", " ").title()


def _last_request(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return str(coordinator.data.get("last_request", "No requests yet"))


def _last_request_time(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return str(coordinator.data.get("last_request_time", "Not set"))


def _timer_remaining(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return _format_hhmmss(int(coordinator.data.get("timer_remaining_seconds", 0)))


def _timer_remaining_seconds(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> int:
    return int(coordinator.data.get("timer_remaining_seconds", 0))


def _timer_status(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    if coordinator.data.get("timer_finished"):
        return "Finished"
    if coordinator.data.get("timer_running"):
        return "Running"
    if coordinator.data.get("timer_paused"):
        return "Paused"
    return "Idle"


def _timer_label(hass: HomeAssistant, entry: ConfigEntry, coordinator: AutismKidsCoordinator) -> str:
    return str(coordinator.data.get("timer_label", "Timer"))


SENSORS = (
    AutismKidsSensorDescription(key="kid_now_activity", name="Kid Now Activity", icon="mdi:play-circle", value_fn=_kid_now),
    AutismKidsSensorDescription(key="kid_next_activity", name="Kid Next Activity", icon="mdi:skip-next-circle", value_fn=_kid_next),
    AutismKidsSensorDescription(key="kid_later_activity", name="Kid Later Activity", icon="mdi:timeline-clock", value_fn=_kid_later),
    AutismKidsSensorDescription(key="kid_who_is_home", name="Kid Who Is Home", icon="mdi:home-account", value_fn=_kid_home),
    AutismKidsSensorDescription(key="kid_special_change_summary", name="Kid Special Change Summary", icon="mdi:calendar-alert", value_fn=_special_change),
    AutismKidsSensorDescription(key="kid_dinner_summary", name="Kid Dinner Summary", icon="mdi:silverware-fork-knife", value_fn=_dinner),
    AutismKidsSensorDescription(key="kid_bedtime_summary", name="Kid Bedtime Summary", icon="mdi:bed-clock", value_fn=_bedtime),
    AutismKidsSensorDescription(key="kid_school_tomorrow_summary", name="Kid School Tomorrow Summary", icon="mdi:school", value_fn=_school_tomorrow),
    AutismKidsSensorDescription(key="kid_weather_summary", name="Kid Weather Summary", icon="mdi:weather-partly-cloudy", value_fn=_weather),
    AutismKidsSensorDescription(key="kid_last_request", name="Kid Last Request", icon="mdi:message-text-fast", value_fn=_last_request),
    AutismKidsSensorDescription(key="kid_last_request_time", name="Kid Last Request Time", icon="mdi:clock-outline", value_fn=_last_request_time),
    AutismKidsSensorDescription(key="kid_timer_remaining", name="Kid Timer Remaining", icon="mdi:timer-sand", value_fn=_timer_remaining),
    AutismKidsSensorDescription(key="kid_timer_remaining_seconds", name="Kid Timer Remaining Seconds", icon="mdi:timer-outline", value_fn=_timer_remaining_seconds),
    AutismKidsSensorDescription(key="kid_timer_status", name="Kid Timer Status", icon="mdi:progress-clock", value_fn=_timer_status),
    AutismKidsSensorDescription(key="kid_timer_label", name="Kid Timer Label", icon="mdi:form-textbox", value_fn=_timer_label),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(AutismKidsSensor(coordinator, entry, description) for description in SENSORS)


class AutismKidsSensor(CoordinatorEntity[AutismKidsCoordinator], SensorEntity):
    entity_description: AutismKidsSensorDescription

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry, description: AutismKidsSensorDescription) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    @property
    def native_value(self) -> str | int:
        return self.entity_description.value_fn(self.hass, self._entry, self.coordinator)

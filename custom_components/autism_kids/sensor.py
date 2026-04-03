from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import *
from .coordinator import AutismKidsCoordinator


@dataclass(frozen=True, kw_only=True)
class AutismKidsSensorDescription(SensorEntityDescription):
    value_fn: Callable[[ConfigEntry, AutismKidsCoordinator], str | int]


def _state(hass, entity_id: str | None) -> str:
    if not entity_id:
        return ""
    state = hass.states.get(entity_id)
    return "" if state is None else str(state.state)


def _attr(hass, entity_id: str | None, attr_name: str) -> str | None:
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


def _kid_now(entry, coordinator):
    msg = _attr(coordinator.hass, entry.data.get(CONF_KID_CALENDAR), "message")
    state = _state(coordinator.hass, entry.data.get(CONF_KID_CALENDAR))
    return msg if state == "on" and msg else entry.options.get(CONF_NOW_FALLBACK, DEFAULT_NOW_FALLBACK)


def _kid_next(entry, coordinator):
    msg = _attr(coordinator.hass, entry.data.get(CONF_FAMILY_CALENDAR), "message")
    start_time = _attr(coordinator.hass, entry.data.get(CONF_FAMILY_CALENDAR), "start_time")
    return msg if msg and start_time else entry.options.get(CONF_NEXT_FALLBACK, DEFAULT_NEXT_FALLBACK)


def _kid_later(entry, coordinator): return entry.options.get(CONF_LATER_FALLBACK, DEFAULT_LATER_FALLBACK)
def _kid_home(entry, coordinator):
    names = []
    if entry.data.get(CONF_PERSON_ONE) and _state(coordinator.hass, entry.data.get(CONF_PERSON_ONE)) == "home": names.append(entry.data.get(CONF_PERSON_ONE_NAME, "Person 1"))
    if entry.data.get(CONF_PERSON_TWO) and _state(coordinator.hass, entry.data.get(CONF_PERSON_TWO)) == "home": names.append(entry.data.get(CONF_PERSON_TWO_NAME, "Person 2"))
    if not names: return "No one is home"
    return f"{names[0]} is home" if len(names) == 1 else f"{names[0]} and {names[1]} are home"

def _special_change(entry, coordinator): return str(coordinator.data.get(DATA_SPECIAL_CHANGE_TEXT, "No special changes today"))
def _dinner(entry, coordinator): return str(coordinator.data.get(DATA_DINNER_TEXT, "Dinner not set"))
def _bedtime(entry, coordinator):
    bedtime = coordinator.data.get(DATA_BEDTIME)
    return "Bedtime not set" if bedtime is None else f"Bedtime at {bedtime.strftime('%-I:%M %p')}"

def _school_tomorrow(entry, coordinator): return "School tomorrow" if coordinator.data.get(DATA_SCHOOL_TOMORROW, True) else "No school tomorrow"
def _weather(entry, coordinator):
    condition = _state(coordinator.hass, entry.data.get(CONF_WEATHER))
    temp = _attr(coordinator.hass, entry.data.get(CONF_WEATHER), "temperature")
    if condition in {"", "unknown", "unavailable"}: return "Weather unavailable"
    return f"{condition.replace('_', ' ').title()}, {temp}°" if temp else condition.replace("_", " ").title()

def _last_request(entry, coordinator): return str(coordinator.data.get("last_request", "No requests yet"))
def _last_request_time(entry, coordinator): return str(coordinator.data.get("last_request_time", "Not set"))
def _timer_remaining(entry, coordinator): return _format_hhmmss(int(coordinator.data.get("timer_remaining_seconds", 0)))
def _timer_remaining_seconds(entry, coordinator): return int(coordinator.data.get("timer_remaining_seconds", 0))
def _timer_status(entry, coordinator): return "Finished" if coordinator.data.get("timer_finished") else "Running" if coordinator.data.get("timer_running") else "Paused" if coordinator.data.get("timer_paused") else "Idle"
def _timer_label(entry, coordinator): return str(coordinator.data.get("timer_label", "Timer"))
def _feeling(entry, coordinator): return str(coordinator.data.get(DATA_FEELING, "Okay"))
def _feeling_time(entry, coordinator): return str(coordinator.data.get(DATA_FEELING_TIME, "Not set"))
def _calm_status(entry, coordinator): return str(coordinator.data.get(DATA_CALM_STATUS, "Not active"))
def _story_name(entry, coordinator): return str(coordinator.data.get(DATA_STORY_NAME, STORY_OPTIONS[0]))
def _story_step(entry, coordinator): return int(coordinator.data.get(DATA_STORY_STEP, 1))
def _story_step_text(entry, coordinator): return str(coordinator.data.get(f"story_step_{int(coordinator.data.get(DATA_STORY_STEP, 1))}", ""))
def _visual_morning(entry, coordinator): return str(coordinator.data.get(DATA_VISUAL_MORNING, "Breakfast"))
def _visual_afternoon(entry, coordinator): return str(coordinator.data.get(DATA_VISUAL_AFTERNOON, "School"))
def _visual_evening(entry, coordinator): return str(coordinator.data.get(DATA_VISUAL_EVENING, "Dinner"))
def _visual_tomorrow(entry, coordinator): return str(coordinator.data.get(DATA_VISUAL_TOMORROW, "Tomorrow note"))

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
    AutismKidsSensorDescription(key="kid_feeling", name="Kid Feeling", icon="mdi:emoticon-outline", value_fn=_feeling),
    AutismKidsSensorDescription(key="kid_feeling_time", name="Kid Feeling Time", icon="mdi:clock-outline", value_fn=_feeling_time),
    AutismKidsSensorDescription(key="kid_calm_status", name="Kid Calm Status", icon="mdi:meditation", value_fn=_calm_status),
    AutismKidsSensorDescription(key="kid_story_name", name="Kid Story Name", icon="mdi:book-open-page-variant", value_fn=_story_name),
    AutismKidsSensorDescription(key="kid_story_step", name="Kid Story Step", icon="mdi:numeric", value_fn=_story_step),
    AutismKidsSensorDescription(key="kid_story_step_text", name="Kid Story Step Text", icon="mdi:text", value_fn=_story_step_text),
    AutismKidsSensorDescription(key="kid_visual_morning", name="Kid Visual Morning", icon="mdi:weather-sunset-up", value_fn=_visual_morning),
    AutismKidsSensorDescription(key="kid_visual_afternoon", name="Kid Visual Afternoon", icon="mdi:weather-sunny", value_fn=_visual_afternoon),
    AutismKidsSensorDescription(key="kid_visual_evening", name="Kid Visual Evening", icon="mdi:weather-night", value_fn=_visual_evening),
    AutismKidsSensorDescription(key="kid_visual_tomorrow", name="Kid Visual Tomorrow", icon="mdi:calendar-arrow-right", value_fn=_visual_tomorrow),
)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
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
        return self.entity_description.value_fn(self._entry, self.coordinator)

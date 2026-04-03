from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import *
from .coordinator import AutismKidsCoordinator

@dataclass(frozen=True, kw_only=True)
class AutismKidsButtonDescription(ButtonEntityDescription):
    press_fn: Callable[[AutismKidsCoordinator, ConfigEntry], Awaitable[None] | None]

async def _request(c, label: str) -> None:
    c.async_set_last_request(label)
    await c.async_send_request_notification(label)

def _feel(c, label: str) -> None: c.async_set_feeling(label)

def _press_start_calm(c): c.async_start_calm_corner()
def _press_finish_calm(c): c.async_finish_calm_corner()
def _press_need_help(c): c.async_calm_need_help()
def _press_next_story(c): c.async_next_story_step()
def _press_prev_story(c): c.async_previous_story_step()
def _press_reset_story(c): c.async_reset_story()

def _start_timer(c, minutes: float): c.async_start_timer(minutes, f"{int(minutes)} Minute Timer")

BUTTONS = (
    AutismKidsButtonDescription(key="request_help", name="Request Help", icon="mdi:help-circle", press_fn=lambda c, e: _request(c, "Help")),
    AutismKidsButtonDescription(key="request_drink", name="Request Drink", icon="mdi:cup-water", press_fn=lambda c, e: _request(c, "Drink")),
    AutismKidsButtonDescription(key="request_snack", name="Request Snack", icon="mdi:food-apple", press_fn=lambda c, e: _request(c, "Snack")),
    AutismKidsButtonDescription(key="request_bathroom", name="Request Bathroom", icon="mdi:toilet", press_fn=lambda c, e: _request(c, "Bathroom")),
    AutismKidsButtonDescription(key="request_break", name="Request Break", icon="mdi:sofa", press_fn=lambda c, e: _request(c, "Break")),
    AutismKidsButtonDescription(key="request_hug", name="Request Hug", icon="mdi:heart", press_fn=lambda c, e: _request(c, "Hug")),
    AutismKidsButtonDescription(key="request_quiet", name="Request Quiet", icon="mdi:volume-off", press_fn=lambda c, e: _request(c, "Quiet")),
    AutismKidsButtonDescription(key="request_too_loud", name="Request Too Loud", icon="mdi:ear-hearing-off", press_fn=lambda c, e: _request(c, "Too Loud")),
    AutismKidsButtonDescription(key="request_mad", name="Request Mad", icon="mdi:emoticon-angry-outline", press_fn=lambda c, e: _request(c, "Mad")),
    AutismKidsButtonDescription(key="request_sad", name="Request Sad", icon="mdi:emoticon-sad-outline", press_fn=lambda c, e: _request(c, "Sad")),
    AutismKidsButtonDescription(key="request_all_done", name="Request All Done", icon="mdi:check-circle", press_fn=lambda c, e: _request(c, "All Done")),
    AutismKidsButtonDescription(key="start_2_minute_timer", name="Start 2 Minute Timer", icon="mdi:timer-play", press_fn=lambda c, e: _start_timer(c, float(e.options.get(CONF_PRESET_1_MINUTES, DEFAULT_PRESET_1_MINUTES)))),
    AutismKidsButtonDescription(key="start_5_minute_timer", name="Start 5 Minute Timer", icon="mdi:timer-play-outline", press_fn=lambda c, e: _start_timer(c, float(e.options.get(CONF_PRESET_2_MINUTES, DEFAULT_PRESET_2_MINUTES)))),
    AutismKidsButtonDescription(key="start_10_minute_timer", name="Start 10 Minute Timer", icon="mdi:timer-star", press_fn=lambda c, e: _start_timer(c, float(e.options.get(CONF_PRESET_3_MINUTES, DEFAULT_PRESET_3_MINUTES)))),
    AutismKidsButtonDescription(key="start_custom_timer", name="Start Custom Timer", icon="mdi:play-circle", press_fn=lambda c, e: _start_timer(c, float(c.data.get('custom_timer_minutes', 5.0)))),
    AutismKidsButtonDescription(key="pause_timer", name="Pause Timer", icon="mdi:pause-circle", press_fn=lambda c, e: c.async_pause_timer()),
    AutismKidsButtonDescription(key="resume_timer", name="Resume Timer", icon="mdi:play-circle-outline", press_fn=lambda c, e: c.async_resume_timer()),
    AutismKidsButtonDescription(key="cancel_timer", name="Cancel Timer", icon="mdi:cancel", press_fn=lambda c, e: c.async_cancel_timer()),
    AutismKidsButtonDescription(key="feel_happy", name="Feel Happy", icon="mdi:emoticon-happy-outline", press_fn=lambda c, e: _feel(c, 'Happy')),
    AutismKidsButtonDescription(key="feel_sad", name="Feel Sad", icon="mdi:emoticon-sad-outline", press_fn=lambda c, e: _feel(c, 'Sad')),
    AutismKidsButtonDescription(key="feel_mad", name="Feel Mad", icon="mdi:emoticon-angry-outline", press_fn=lambda c, e: _feel(c, 'Mad')),
    AutismKidsButtonDescription(key="feel_worried", name="Feel Worried", icon="mdi:emoticon-confused-outline", press_fn=lambda c, e: _feel(c, 'Worried')),
    AutismKidsButtonDescription(key="feel_tired", name="Feel Tired", icon="mdi:emoticon-neutral-outline", press_fn=lambda c, e: _feel(c, 'Tired')),
    AutismKidsButtonDescription(key="feel_overwhelmed", name="Feel Overwhelmed", icon="mdi:head-alert-outline", press_fn=lambda c, e: _feel(c, 'Overwhelmed')),
    AutismKidsButtonDescription(key="feel_excited", name="Feel Excited", icon="mdi:party-popper", press_fn=lambda c, e: _feel(c, 'Excited')),
    AutismKidsButtonDescription(key="start_calm_corner", name="Start Calm Corner", icon="mdi:meditation", press_fn=lambda c, e: _press_start_calm(c)),
    AutismKidsButtonDescription(key="calm_corner_finished", name="Calm Corner Finished", icon="mdi:check-circle-outline", press_fn=lambda c, e: _press_finish_calm(c)),
    AutismKidsButtonDescription(key="calm_corner_need_help", name="Calm Corner Need Help", icon="mdi:lifebuoy", press_fn=lambda c, e: _press_need_help(c)),
    AutismKidsButtonDescription(key="story_next_step", name="Story Next Step", icon="mdi:arrow-right-bold-circle", press_fn=lambda c, e: _press_next_story(c)),
    AutismKidsButtonDescription(key="story_previous_step", name="Story Previous Step", icon="mdi:arrow-left-bold-circle", press_fn=lambda c, e: _press_prev_story(c)),
    AutismKidsButtonDescription(key="story_reset", name="Story Reset", icon="mdi:restart", press_fn=lambda c, e: _press_reset_story(c)),
)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(AutismKidsActionButton(coordinator, entry, description) for description in BUTTONS)

class AutismKidsActionButton(CoordinatorEntity[AutismKidsCoordinator], ButtonEntity):
    entity_description: AutismKidsButtonDescription
    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry, description: AutismKidsButtonDescription) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")
    async def async_press(self) -> None:
        result = self.entity_description.press_fn(self.coordinator, self._entry)
        if result is not None:
            await result

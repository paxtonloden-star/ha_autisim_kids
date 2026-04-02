from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Awaitable

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_PRESET_1_MINUTES,
    CONF_PRESET_2_MINUTES,
    CONF_PRESET_3_MINUTES,
    DEFAULT_PRESET_1_MINUTES,
    DEFAULT_PRESET_2_MINUTES,
    DEFAULT_PRESET_3_MINUTES,
    DOMAIN,
)
from .coordinator import AutismKidsCoordinator


@dataclass(frozen=True, kw_only=True)
class AutismKidsButtonDescription(ButtonEntityDescription):
    press_fn: Callable[[AutismKidsCoordinator, ConfigEntry], Awaitable[None] | None]


async def _press_request_help(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Help")
    await coordinator.async_send_request_notification("Help")


async def _press_request_drink(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Drink")
    await coordinator.async_send_request_notification("Drink")


async def _press_request_snack(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Snack")
    await coordinator.async_send_request_notification("Snack")


async def _press_request_bathroom(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Bathroom")
    await coordinator.async_send_request_notification("Bathroom")


async def _press_request_break(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Break")
    await coordinator.async_send_request_notification("Break")


async def _press_request_hug(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Hug")
    await coordinator.async_send_request_notification("Hug")


async def _press_request_quiet(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Quiet")
    await coordinator.async_send_request_notification("Quiet")


async def _press_request_too_loud(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Too Loud")
    await coordinator.async_send_request_notification("Too Loud")


async def _press_request_mad(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Mad")
    await coordinator.async_send_request_notification("Mad")


async def _press_request_sad(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("Sad")
    await coordinator.async_send_request_notification("Sad")


async def _press_request_all_done(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_set_last_request("All Done")
    await coordinator.async_send_request_notification("All Done")


async def _press_start_preset_1(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    minutes = float(entry.options.get(CONF_PRESET_1_MINUTES, DEFAULT_PRESET_1_MINUTES))
    coordinator.async_start_timer(minutes, f"{int(minutes)} Minute Timer")


async def _press_start_preset_2(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    minutes = float(entry.options.get(CONF_PRESET_2_MINUTES, DEFAULT_PRESET_2_MINUTES))
    coordinator.async_start_timer(minutes, f"{int(minutes)} Minute Timer")


async def _press_start_preset_3(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    minutes = float(entry.options.get(CONF_PRESET_3_MINUTES, DEFAULT_PRESET_3_MINUTES))
    coordinator.async_start_timer(minutes, f"{int(minutes)} Minute Timer")


async def _press_start_custom(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    minutes = float(coordinator.data.get("custom_timer_minutes", 5.0))
    coordinator.async_start_timer(minutes, f"{int(minutes)} Minute Timer")


async def _press_pause_timer(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_pause_timer()


async def _press_resume_timer(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_resume_timer()


async def _press_cancel_timer(coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
    coordinator.async_cancel_timer()


BUTTONS: tuple[AutismKidsButtonDescription, ...] = (
    AutismKidsButtonDescription(key="request_help", name="Request Help", icon="mdi:help-circle", press_fn=_press_request_help),
    AutismKidsButtonDescription(key="request_drink", name="Request Drink", icon="mdi:cup-water", press_fn=_press_request_drink),
    AutismKidsButtonDescription(key="request_snack", name="Request Snack", icon="mdi:food-apple", press_fn=_press_request_snack),
    AutismKidsButtonDescription(key="request_bathroom", name="Request Bathroom", icon="mdi:toilet", press_fn=_press_request_bathroom),
    AutismKidsButtonDescription(key="request_break", name="Request Break", icon="mdi:sofa", press_fn=_press_request_break),
    AutismKidsButtonDescription(key="request_hug", name="Request Hug", icon="mdi:heart", press_fn=_press_request_hug),
    AutismKidsButtonDescription(key="request_quiet", name="Request Quiet", icon="mdi:volume-off", press_fn=_press_request_quiet),
    AutismKidsButtonDescription(key="request_too_loud", name="Request Too Loud", icon="mdi:ear-hearing-off", press_fn=_press_request_too_loud),
    AutismKidsButtonDescription(key="request_mad", name="Request Mad", icon="mdi:emoticon-angry-outline", press_fn=_press_request_mad),
    AutismKidsButtonDescription(key="request_sad", name="Request Sad", icon="mdi:emoticon-sad-outline", press_fn=_press_request_sad),
    AutismKidsButtonDescription(key="request_all_done", name="Request All Done", icon="mdi:check-circle", press_fn=_press_request_all_done),
    AutismKidsButtonDescription(key="start_2_minute_timer", name="Start 2 Minute Timer", icon="mdi:timer-play", press_fn=_press_start_preset_1),
    AutismKidsButtonDescription(key="start_5_minute_timer", name="Start 5 Minute Timer", icon="mdi:timer-play-outline", press_fn=_press_start_preset_2),
    AutismKidsButtonDescription(key="start_10_minute_timer", name="Start 10 Minute Timer", icon="mdi:timer-star", press_fn=_press_start_preset_3),
    AutismKidsButtonDescription(key="start_custom_timer", name="Start Custom Timer", icon="mdi:play-circle", press_fn=_press_start_custom),
    AutismKidsButtonDescription(key="pause_timer", name="Pause Timer", icon="mdi:pause-circle", press_fn=_press_pause_timer),
    AutismKidsButtonDescription(key="resume_timer", name="Resume Timer", icon="mdi:play-circle-outline", press_fn=_press_resume_timer),
    AutismKidsButtonDescription(key="cancel_timer", name="Cancel Timer", icon="mdi:cancel", press_fn=_press_cancel_timer),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: AutismKidsCoordinator = hass.data[DOMAIN][entry.entry_id]
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
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Autism Kids Predictability Board",
            manufacturer="Paxton Loden",
            model="Predictability Board",
        )

    async def async_press(self) -> None:
        result = self.entity_description.press_fn(self.coordinator, self._entry)
        if result is not None:
            await result

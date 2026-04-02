from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_REQUEST_NOTIFICATION_TITLE,
    CONF_REQUEST_NOTIFICATIONS,
    DEFAULT_REQUEST_NOTIFICATION_TITLE,
    DEFAULT_REQUEST_NOTIFICATIONS,
    DOMAIN,
)
from .coordinator import AutismKidsCoordinator


@dataclass(frozen=True, kw_only=True)
class AutismKidsButtonDescription(ButtonEntityDescription):
    request_label: str


BUTTONS: tuple[AutismKidsButtonDescription, ...] = (
    AutismKidsButtonDescription(key="request_help", name="Request Help", icon="mdi:help-circle", request_label="Help"),
    AutismKidsButtonDescription(key="request_drink", name="Request Drink", icon="mdi:cup-water", request_label="Drink"),
    AutismKidsButtonDescription(key="request_snack", name="Request Snack", icon="mdi:food-apple", request_label="Snack"),
    AutismKidsButtonDescription(key="request_bathroom", name="Request Bathroom", icon="mdi:toilet", request_label="Bathroom"),
    AutismKidsButtonDescription(key="request_break", name="Request Break", icon="mdi:sofa", request_label="Break"),
    AutismKidsButtonDescription(key="request_hug", name="Request Hug", icon="mdi:heart", request_label="Hug"),
    AutismKidsButtonDescription(key="request_quiet", name="Request Quiet", icon="mdi:volume-off", request_label="Quiet"),
    AutismKidsButtonDescription(key="request_too_loud", name="Request Too Loud", icon="mdi:ear-hearing-off", request_label="Too Loud"),
    AutismKidsButtonDescription(key="request_mad", name="Request Mad", icon="mdi:emoticon-angry-outline", request_label="Mad"),
    AutismKidsButtonDescription(key="request_sad", name="Request Sad", icon="mdi:emoticon-sad-outline", request_label="Sad"),
    AutismKidsButtonDescription(key="request_all_done", name="Request All Done", icon="mdi:check-circle", request_label="All Done"),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: AutismKidsCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AutismKidsRequestButton(coordinator, entry, description) for description in BUTTONS
    )


class AutismKidsRequestButton(CoordinatorEntity[AutismKidsCoordinator], ButtonEntity):
    entity_description: AutismKidsButtonDescription

    def __init__(
        self,
        coordinator: AutismKidsCoordinator,
        entry: ConfigEntry,
        description: AutismKidsButtonDescription,
    ) -> None:
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
        self.coordinator.async_set_last_request(self.entity_description.request_label)

        if self._entry.options.get(CONF_REQUEST_NOTIFICATIONS, DEFAULT_REQUEST_NOTIFICATIONS):
            await self.hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": self._entry.options.get(
                        CONF_REQUEST_NOTIFICATION_TITLE,
                        DEFAULT_REQUEST_NOTIFICATION_TITLE,
                    ),
                    "message": f"{self.entity_description.request_label} requested",
                    "notification_id": f"{DOMAIN}_{self._entry.entry_id}_{self.entity_description.key}",
                },
                blocking=True,
            )

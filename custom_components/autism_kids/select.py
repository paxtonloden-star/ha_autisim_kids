from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import *
from .coordinator import AutismKidsCoordinator

@dataclass(frozen=True, kw_only=True)
class AutismKidsSelectDescription(SelectEntityDescription):
    data_key: str
    options_list: list[str]

SELECTS = (
    AutismKidsSelectDescription(key="feeling_select", name="Feeling Select", icon="mdi:emoticon-outline", data_key=DATA_FEELING, options_list=FEELING_OPTIONS),
    AutismKidsSelectDescription(key="story_select", name="Story Select", icon="mdi:book-open-page-variant", data_key=DATA_STORY_NAME, options_list=STORY_OPTIONS),
)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(AutismKidsSelect(coordinator, entry, description) for description in SELECTS)

class AutismKidsSelect(CoordinatorEntity[AutismKidsCoordinator], SelectEntity):
    entity_description: AutismKidsSelectDescription
    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry, description: AutismKidsSelectDescription) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_options = description.options_list
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")
    @property
    def current_option(self) -> str | None:
        return str(self.coordinator.data.get(self.entity_description.data_key, self.options[0]))
    async def async_select_option(self, option: str) -> None:
        self.coordinator.async_set_data_value(self.entity_description.data_key, option)
        if self.entity_description.data_key == DATA_STORY_NAME:
            self.coordinator.async_reset_story()
        if self.entity_description.data_key == DATA_FEELING:
            self.coordinator.async_set_feeling(option)
        self.async_write_ha_state()

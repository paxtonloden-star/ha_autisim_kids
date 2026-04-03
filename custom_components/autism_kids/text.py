from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.text import TextEntity, TextEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import *
from .coordinator import AutismKidsCoordinator

@dataclass(frozen=True, kw_only=True)
class AutismKidsTextDescription(TextEntityDescription):
    data_key: str

TEXTS = (
    AutismKidsTextDescription(key="special_change_text", name="Special Change Text", icon="mdi:calendar-alert", data_key=DATA_SPECIAL_CHANGE_TEXT),
    AutismKidsTextDescription(key="dinner_text", name="Dinner Text", icon="mdi:silverware-fork-knife", data_key=DATA_DINNER_TEXT),
    AutismKidsTextDescription(key="calm_step_1", name="Calm Step 1", icon="mdi:numeric-1-box-outline", data_key=DATA_CALM_STEP_1),
    AutismKidsTextDescription(key="calm_step_2", name="Calm Step 2", icon="mdi:numeric-2-box-outline", data_key=DATA_CALM_STEP_2),
    AutismKidsTextDescription(key="calm_step_3", name="Calm Step 3", icon="mdi:numeric-3-box-outline", data_key=DATA_CALM_STEP_3),
    AutismKidsTextDescription(key="calm_step_4", name="Calm Step 4", icon="mdi:numeric-4-box-outline", data_key=DATA_CALM_STEP_4),
    AutismKidsTextDescription(key="story_step_1", name="Story Step 1", icon="mdi:numeric-1-box-outline", data_key=DATA_STORY_STEP_1),
    AutismKidsTextDescription(key="story_step_2", name="Story Step 2", icon="mdi:numeric-2-box-outline", data_key=DATA_STORY_STEP_2),
    AutismKidsTextDescription(key="story_step_3", name="Story Step 3", icon="mdi:numeric-3-box-outline", data_key=DATA_STORY_STEP_3),
    AutismKidsTextDescription(key="story_step_4", name="Story Step 4", icon="mdi:numeric-4-box-outline", data_key=DATA_STORY_STEP_4),
    AutismKidsTextDescription(key="story_step_5", name="Story Step 5", icon="mdi:numeric-5-box-outline", data_key=DATA_STORY_STEP_5),
    AutismKidsTextDescription(key="visual_morning", name="Visual Morning", icon="mdi:weather-sunset-up", data_key=DATA_VISUAL_MORNING),
    AutismKidsTextDescription(key="visual_afternoon", name="Visual Afternoon", icon="mdi:weather-sunny", data_key=DATA_VISUAL_AFTERNOON),
    AutismKidsTextDescription(key="visual_evening", name="Visual Evening", icon="mdi:weather-night", data_key=DATA_VISUAL_EVENING),
    AutismKidsTextDescription(key="visual_tomorrow", name="Visual Tomorrow", icon="mdi:calendar-arrow-right", data_key=DATA_VISUAL_TOMORROW),
)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(AutismKidsText(coordinator, entry, description) for description in TEXTS)

class AutismKidsText(CoordinatorEntity[AutismKidsCoordinator], RestoreEntity, TextEntity):
    entity_description: AutismKidsTextDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_native_max = 255
    _attr_native_min = 0

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry, description: AutismKidsTextDescription) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None:
            await self.async_set_value(last_state.state)

    @property
    def native_value(self) -> str:
        return str(self.coordinator.data.get(self.entity_description.data_key, ""))

    async def async_set_value(self, value: str) -> None:
        self.coordinator.async_set_data_value(self.entity_description.data_key, value)
        self.async_write_ha_state()

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_SCHOOL_TOMORROW, DOMAIN
from .coordinator import AutismKidsCoordinator

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AutismKidsSchoolTomorrowSwitch(coordinator, entry)])

class AutismKidsSchoolTomorrowSwitch(CoordinatorEntity[AutismKidsCoordinator], RestoreEntity, SwitchEntity):
    _attr_name = "School Tomorrow"
    _attr_icon = "mdi:school"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_school_tomorrow"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self.coordinator.async_set_data_value(DATA_SCHOOL_TOMORROW, last_state.state == "on")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DATA_SCHOOL_TOMORROW, True))

    async def async_turn_on(self, **kwargs) -> None:
        self.coordinator.async_set_data_value(DATA_SCHOOL_TOMORROW, True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        self.coordinator.async_set_data_value(DATA_SCHOOL_TOMORROW, False)
        self.async_write_ha_state()

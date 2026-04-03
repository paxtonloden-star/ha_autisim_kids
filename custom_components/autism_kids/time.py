from __future__ import annotations

from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_BEDTIME, DOMAIN
from .coordinator import AutismKidsCoordinator


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AutismKidsBedtimeTime(coordinator, entry)])


class AutismKidsBedtimeTime(CoordinatorEntity[AutismKidsCoordinator], RestoreEntity, TimeEntity):
    _attr_name = "Bedtime"
    _attr_icon = "mdi:bed-clock"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_bedtime"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None:
            try:
                await self.async_set_value(time.fromisoformat(last_state.state))
            except ValueError:
                pass

    @property
    def native_value(self) -> time:
        return self.coordinator.data.get(DATA_BEDTIME)

    async def async_set_value(self, value: time) -> None:
        self.coordinator.async_set_bedtime(value)
        self.async_write_ha_state()

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AutismKidsCoordinator


NUMBER_DESCRIPTION = NumberEntityDescription(key="custom_timer_minutes", name="Custom Timer Minutes", icon="mdi:timer-cog-outline")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AutismKidsCustomTimerNumber(coordinator, entry)])


class AutismKidsCustomTimerNumber(CoordinatorEntity[AutismKidsCoordinator], RestoreNumber, NumberEntity):
    entity_description = NUMBER_DESCRIPTION
    _attr_native_min_value = 1
    _attr_native_max_value = 60
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_mode = "box"

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_custom_timer_minutes"
        self._attr_native_value = float(coordinator.data.get("custom_timer_minutes", 5.0))

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if last_number_data is not None:
            self._attr_native_value = float(last_number_data.native_value)
            self.coordinator.async_set_custom_timer_minutes(float(last_number_data.native_value))

    @property
    def native_value(self) -> float:
        return float(self.coordinator.data.get("custom_timer_minutes", self._attr_native_value))

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = float(value)
        self.coordinator.async_set_custom_timer_minutes(float(value))
        self.async_write_ha_state()

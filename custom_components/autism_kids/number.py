from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import NumberEntity, NumberEntityDescription, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_FEELING_INTENSITY, DOMAIN
from .coordinator import AutismKidsCoordinator

@dataclass(frozen=True, kw_only=True)
class AutismKidsNumberDescription(NumberEntityDescription):
    data_key: str

NUMBERS = (
    AutismKidsNumberDescription(key="custom_timer_minutes", name="Custom Timer Minutes", icon="mdi:timer-cog-outline", data_key="custom_timer_minutes"),
    AutismKidsNumberDescription(key="feeling_intensity", name="Feeling Intensity", icon="mdi:gauge", data_key=DATA_FEELING_INTENSITY),
)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AutismKidsNumberEntity(coordinator, entry, d) for d in NUMBERS])

class AutismKidsNumberEntity(CoordinatorEntity[AutismKidsCoordinator], RestoreNumber, NumberEntity):
    entity_description: AutismKidsNumberDescription
    _attr_native_min_value = 1
    _attr_native_max_value = 60
    _attr_native_step = 1
    _attr_mode = "box"

    def __init__(self, coordinator: AutismKidsCoordinator, entry: ConfigEntry, description: AutismKidsNumberDescription) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        if description.data_key == "custom_timer_minutes":
            self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
            self._attr_native_max_value = 60
        else:
            self._attr_native_unit_of_measurement = "level"
            self._attr_native_max_value = 5
        self._attr_native_value = float(coordinator.data.get(description.data_key, 5.0))

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry.entry_id)}, name="Autism Kids Predictability Board", manufacturer="Paxton Loden", model="Predictability Board")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if last_number_data is not None:
            self._attr_native_value = float(last_number_data.native_value)
            self.coordinator.async_set_data_value(self.entity_description.data_key, float(last_number_data.native_value))

    @property
    def native_value(self) -> float:
        return float(self.coordinator.data.get(self.entity_description.data_key, self._attr_native_value))

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = float(value)
        self.coordinator.async_set_data_value(self.entity_description.data_key, float(value))
        self.async_write_ha_state()

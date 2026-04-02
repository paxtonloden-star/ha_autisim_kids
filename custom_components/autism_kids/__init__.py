from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import AutismKidsCoordinator


type AutismKidsConfigEntry = ConfigEntry


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Autism Kids integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: AutismKidsConfigEntry) -> bool:
    """Set up Autism Kids from a config entry."""
    coordinator = AutismKidsCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: AutismKidsConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

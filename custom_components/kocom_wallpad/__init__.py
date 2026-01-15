"""Component setup for Kocom Wallpad."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT, EVENT_HOMEASSISTANT_STOP

from .const import DOMAIN, PLATFORMS
from .gateway import KocomGateway


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kocom Wallpad from a config entry."""
    host: str = entry.data[CONF_HOST]
    port: int = entry.data[CONF_PORT]

    gateway = KocomGateway(hass, entry, host=host, port=port)
    await gateway.async_get_entity_registry()
    await gateway.async_start()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = gateway

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, gateway.async_stop)
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        gateway: KocomGateway = hass.data[DOMAIN].pop(entry.entry_id)
        try:
            await gateway.async_stop()
        except Exception as err:
            logging.getLogger(__name__).exception("Error stopping gateway: %s", err)
            return False
    return unload_ok

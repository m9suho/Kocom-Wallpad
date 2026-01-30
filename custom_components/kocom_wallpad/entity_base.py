"""Base platform for Kocom Wallpad."""

from __future__ import annotations

from typing import Callable

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity, RestoredExtraData
from homeassistant.core import callback
from homeassistant.const import Platform
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.light import LightEntityDescription
from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.components.climate import ClimateEntityDescription
from homeassistant.components.fan import FanEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.binary_sensor import BinarySensorEntityDescription

from .const import DOMAIN, DeviceType, SubType


ENTITY_DESCRIPTION_MAP = {
    Platform.LIGHT: LightEntityDescription,
    Platform.SWITCH: SwitchEntityDescription,
    Platform.CLIMATE: ClimateEntityDescription,
    Platform.FAN: FanEntityDescription,
    Platform.SENSOR: SensorEntityDescription,
    Platform.BINARY_SENSOR: BinarySensorEntityDescription
}


class KocomBaseEntity(RestoreEntity):
    """Base class for Kocom entities."""

    def __init__(self, gateway, device) -> None:
        """Initialize the base entity."""
        super().__init__()
        self.gateway = gateway
        self._device = device
        self._unsubs: list[Callable] = []

        # Performance optimization: Cache computed properties
        self._cached_format_key = self._compute_format_key()
        self._cached_format_identifiers = self._compute_format_identifiers()
        self._cached_translation_placeholders = self._compute_translation_placeholders()

        self._attr_unique_id = f"{device.key.unique_id}:{self.gateway.host}"
        self.entity_description = ENTITY_DESCRIPTION_MAP[self._device.platform](
            key=self._cached_format_key,
            has_entity_name=True,
            translation_key=self._cached_format_key,
            translation_placeholders={"id": self._cached_translation_placeholders}
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._cached_format_identifiers)},
            manufacturer="KOCOM Co., Ltd",
            model="Smart Wallpad",
            name=self._cached_format_identifiers,
            via_device=(DOMAIN, str(self.gateway.host)),
        )
        
    def _compute_format_key(self) -> str:
        """Compute format key once during initialization."""
        if self._device.key.sub_type == SubType.NONE:
            return self._device.key.device_type.name.lower()
        return f"{self._device.key.device_type.name.lower()}-{self._device.key.sub_type.name.lower()}"

    def _compute_translation_placeholders(self) -> str:
        """Compute translation placeholders once during initialization."""
        return f"{self._device.key.room_index}-{self._device.key.device_index}"

    def _compute_format_identifiers(self) -> str:
        """Compute format identifiers once during initialization."""
        device_type = self._device.key.device_type
        if device_type in {DeviceType.VENTILATION, DeviceType.GASVALVE, DeviceType.ELEVATOR, DeviceType.MOTION}:
            return "KOCOM"
        elif device_type in {DeviceType.LIGHT, DeviceType.DIMMINGLIGHT}:
            return "KOCOM LIGHT"
        return f"KOCOM {device_type.name}"

    @property
    def format_key(self) -> str:
        return self._cached_format_key

    @property
    def format_translation_placeholders(self) -> str:
        return self._cached_translation_placeholders

    @property
    def format_identifiers(self) -> str:
        return self._cached_format_identifiers

    async def async_added_to_hass(self):
        sig = self.gateway.async_signal_device_updated(self._device.key.unique_id)

        @callback
        def _handle_update(dev):
            self._device = dev
            self.update_from_state()
        self._unsubs.append(async_dispatcher_connect(self.hass, sig, _handle_update))

    async def async_will_remove_from_hass(self) -> None:
        for unsub in self._unsubs:
            try:
                unsub()
            except Exception:
                pass
        self._unsubs.clear()

    @callback
    def update_from_state(self) -> None:
        self.async_write_ha_state()

    @property
    def extra_restore_state_data(self) -> RestoredExtraData:
        return RestoredExtraData({
            "packet": getattr(self._device, "_packet", bytes()).hex(),
            "device_storage": self.gateway.controller._device_storage
        })

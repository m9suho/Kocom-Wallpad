"""Models for Kocom Wallpad."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple, Union

from homeassistant.const import Platform

from .const import DeviceType, SubType


DEVICE_TYPE_MAP = {
    0x0E: DeviceType.LIGHT,
    0x3B: DeviceType.OUTLET,
    0x36: DeviceType.THERMOSTAT,
    0x48: DeviceType.VENTILATION,
    0x2C: DeviceType.GASVALVE,
    0x44: DeviceType.ELEVATOR,
    0x60: DeviceType.MOTION,
    0x98: DeviceType.AIRQUALITY,
}

VENTILATION_PRESET_MAP = {
    0x00: "unknown",
    0x01: "ventilation",
    0x02: "auto",
    0x03: "bypass",
    0x05: "sleep",
    0x08: "air purification"
}

ELEVATOR_DIRECTION_MAP = {
    0x00: "idle",
    0x01: "downward",
    0x02: "upward",
    0x03: "arrival"
}


@dataclass(frozen=True)
class DeviceKey:
    """Device key."""
    device_type: DeviceType
    room_index: int
    device_index: int
    sub_type: SubType

    @property
    def unique_id(self) -> str:
        return f"{self.device_type.value}-{self.room_index}_{self.device_index}-{self.sub_type.value}"

    @property
    def key(self) -> Tuple[int, int, int, int]:
        return (self.device_type.value, self.room_index, self.device_index, self.sub_type.value)


@dataclass
class DeviceState:
    """Device state."""
    key: DeviceKey
    platform: Platform
    attribute: dict[str, Any] 
    state: Union[dict[str, Any], bool, int, float, str]

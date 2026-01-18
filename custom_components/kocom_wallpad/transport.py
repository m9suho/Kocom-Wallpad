"""Transport for Kocom Wallpad."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
import asyncio
import serial_asyncio
import time

from .const import LOGGER


@dataclass
class AsyncConnection:
    """Async Connection."""
    host: str
    port: Optional[int]
    serial_baud: int = 9600
    connect_timeout: float = 5.0
    reconnect_backoff: Tuple[float, float] = (1.0, 30.0)  # min, max seconds

    def __post_init__(self) -> None:
        """Initialize the connection."""
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._last_activity_mono: float = time.monotonic()
        self._last_reconn_delay: float = 0.0
        self._connected = False

    async def open(self) -> None:
        try:
            if self.port is None:
                self._reader, self._writer = await serial_asyncio.open_serial_connection(
                    url=self.host, baudrate=self.serial_baud
                )
                LOGGER.info("Connection opened for serial: %s", self.host)
            else:
                self._reader, self._writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=self.connect_timeout,
                )
                LOGGER.info("Connection opened for socket: %s:%s", self.host, self.port)
            self._connected = True
            self._touch()
        except Exception as e:
            LOGGER.warning("Connection open failed: %r", e)
            await self.reconnect()

    async def close(self) -> None:
        if self._writer is not None:
            LOGGER.info("Closing connection")
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
            finally:
                self._writer = None
        self._reader = None
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _touch(self) -> None:
        self._last_activity_mono = time.monotonic()

    def idle_since(self) -> float:
        return max(0.0, time.monotonic() - self._last_activity_mono)

    async def send(self, data: bytes) -> int:
        if not self._writer:
            raise RuntimeError("connection not open")
        try:
            LOGGER.debug("Sending: %s", data.hex())
            self._writer.write(data)
            await self._writer.drain()
            self._touch()
            return len(data)
        except Exception as e:
            LOGGER.warning("Send failed: %r", e)
            await self.reconnect()
            return 0

    async def recv(self, nbytes: int, timeout: float = 0.05) -> bytes:
        if not self._reader:
            raise RuntimeError("connection not open")
        try:
            chunk = await asyncio.wait_for(self._reader.read(nbytes), timeout=timeout)
        except asyncio.TimeoutError:
            return b""
        except Exception as e:
            LOGGER.warning("Recv failed: %r", e)
            await self.reconnect()
            return b""
        if chunk:
            self._touch()
        return chunk

    async def reconnect(self) -> None:
        self._connected = False
        delay_min, delay_max = self.reconnect_backoff
        if self._last_reconn_delay > 0.0:
            delay = self._last_reconn_delay
        else:
            delay = delay_min

        if self._writer is not None:
            self._writer.close()
            await self._writer.wait_closed()
        
        LOGGER.info("Connection lost. Reconnecting in %.1f sec...", delay)
        await asyncio.sleep(delay)
        self._last_reconn_delay = min(delay * 2, delay_max)
        await self.open()

        if self.is_connected:
            LOGGER.info("Connection reconnected")
            self._last_reconn_delay = delay_min

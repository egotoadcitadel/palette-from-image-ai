"""Output driver registry."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from palette_ai.drivers import clipboard_driver, gpl_driver, json_driver
from palette_ai.models.palette_result import PaletteResult

Driver = Callable[[PaletteResult, Path], None]

_REGISTRY: dict[str, Driver] = {
    "json": json_driver.write,
    "gpl": gpl_driver.write,
    "clipboard": clipboard_driver.write,  # type: ignore[dict-item]
}


def get_driver(fmt: str) -> Driver:
    return _REGISTRY[fmt]


def available() -> list[str]:
    return sorted(_REGISTRY)
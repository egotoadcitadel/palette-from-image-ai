"""Clipboard driver — copies the palette as a hex list for quick paste."""

from __future__ import annotations

import logging

import pyperclip

from palette_ai.models.palette_result import PaletteResult

logger = logging.getLogger(__name__)


def write(result: PaletteResult, path=None) -> None:
    """Copy the palette as a comma-separated hex string to the clipboard.

    *pyperclip shells out on Windows via the `clip` command; it can raise
    PyperclipException if no clipboard backend is available (headless CI).*
    """
    text = ", ".join(result.as_hex_list())
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as exc:
        logger.warning("clipboard unavailable: %s", exc)
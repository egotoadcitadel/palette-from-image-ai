"""Logging configuration for CLI and library use."""

from __future__ import annotations

import logging
import sys


def configure(level: str = "INFO") -> None:
    """Configure the root logger with a compact, color-free format."""
    root = logging.getLogger()
    root.setLevel(level.upper())
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S")
    )
    root.handlers = [handler]
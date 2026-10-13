"""Color extraction workers."""

from palette_ai.processors.base import BaseProcessor, ProcessorError
from palette_ai.processors.registry import available, get_processor

__all__ = ["BaseProcessor", "ProcessorError", "available", "get_processor"]
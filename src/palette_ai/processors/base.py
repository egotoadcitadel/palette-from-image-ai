"""Processor base class — every extraction worker implements this contract."""

from __future__ import annotations

import abc
import time

from palette_ai.models.palette_result import JobContext, PaletteResult


class BaseProcessor(abc.ABC):
    """Abstract color extraction worker.

    Contract:
      - Pure with respect to the input array; no mutation of caller state.
      - Returns a PaletteResult with swatch weights summing to ~1.0.
      - Raises ProcessorError on unrecoverable failure.
    """

    name: str = "base"

    @abc.abstractmethod
    def _extract(self, ctx: JobContext) -> PaletteResult:
        """Do the actual work. Called inside the timing wrapper."""

    def run(self, ctx: JobContext) -> PaletteResult:
        start = time.perf_counter()
        result = self._extract(ctx)
        result.elapsed_ms = (time.perf_counter() - start) * 1000.0
        result.processor = self.name
        return result


class ProcessorError(RuntimeError):
    """Raised when a processor cannot complete."""
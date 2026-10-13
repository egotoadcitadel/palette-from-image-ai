"""Core data models shared across the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Swatch:
    """A single palette entry."""

    hex: str
    rgb: tuple[int, int, int]
    weight: float
    name: str | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"swatch weight out of range: {self.weight}")


@dataclass(slots=True)
class PaletteResult:
    """The output of a processor run."""

    swatches: list[Swatch]
    source: Path
    processor: str
    elapsed_ms: float = 0.0
    meta: dict[str, str] = field(default_factory=dict)

    @property
    def dominant(self) -> Swatch:
        return max(self.swatches, key=lambda s: s.weight)

    def as_hex_list(self) -> list[str]:
        return [s.hex for s in self.swatches]


@dataclass(slots=True)
class JobContext:
    """Everything a processor needs to do its job."""

    image_path: Path
    palette_size: int
    settings_snapshot: dict[str, str]
    scratch_dir: Path
    attempt: int = 1
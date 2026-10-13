"""Runtime settings schema and defaults for the palette pipeline."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class IngestSettings(BaseModel):
    """Controls how images are loaded and normalized before processing."""

    max_pixels: int = Field(default=40_000_000, ge=1_000_000)
    downscale_long_edge: int = Field(default=1024, ge=64, le=4096)
    strip_alpha_background: str = Field(default="#FFFFFF")
    allowed_formats: tuple[str, ...] = ("PNG", "JPEG", "WEBP", "BMP", "TIFF")


class ProcessorSettings(BaseModel):
    """Controls the color extraction workers."""

    palette_size: int = Field(default=8, ge=2, le=64)
    ai_weight: float = Field(default=0.7, ge=0.0, le=1.0)
    min_cluster_pct: float = Field(default=0.005, ge=0.0, le=0.5)
    saturation_boost: float = Field(default=1.0, ge=0.0, le=3.0)
    use_ai_model: bool = True


class DriverSettings(BaseModel):
    """Controls output writers."""

    default_format: str = "json"
    output_dir: Path = Path("exports")
    clip_after_export: bool = False


class AppSettings(BaseModel):
    """Top-level settings container."""

    ingest: IngestSettings = IngestSettings()
    processor: ProcessorSettings = ProcessorSettings()
    driver: DriverSettings = DriverSettings()
    cache_dir: Path = Path("palette_cache")
    log_level: str = "INFO"


DEFAULT_SETTINGS = AppSettings()
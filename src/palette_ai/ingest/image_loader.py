"""Image ingest handler: load, validate, downscale, and hand off pixels.

*Pillow's MAX_IMAGE_PIXELS guard is a decompression-bomb defense; it fires
before the pixel buffer is allocated, so keep it set even for trusted input.*
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

from palette_ai.config.settings import IngestSettings

logger = logging.getLogger(__name__)

Image.MAX_IMAGE_PIXELS = 40_000_000


class IngestError(RuntimeError):
    """Raised when an image cannot be loaded or is rejected by policy."""


def load_image(path: Path, settings: IngestSettings) -> np.ndarray:
    """Load an image as an RGB uint8 array of shape (H, W, 3).

    Raises:
        IngestError: file missing, format not allowed, or decode failure.
    """
    if not path.is_file():
        raise IngestError(f"input not found: {path}")

    try:
        with Image.open(path) as img:
            if img.format not in settings.allowed_formats:
                raise IngestError(f"format {img.format!r} not in allowed set")

            img = img.convert("RGB")
            w, h = img.size
            if w * h > settings.max_pixels:
                raise IngestError(f"image exceeds {settings.max_pixels} pixels")

            long_edge = max(w, h)
            if long_edge > settings.downscale_long_edge:
                scale = settings.downscale_long_edge / long_edge
                new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            return np.asarray(img, dtype=np.uint8)
    except UnidentifiedImageError as exc:
        raise IngestError(f"unidentified image: {path.name}") from exc
    except OSError as exc:
        raise IngestError(f"decode failed for {path.name}: {exc}") from exc
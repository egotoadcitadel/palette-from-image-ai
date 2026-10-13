"""JSON output driver — the canonical machine-readable palette format."""

from __future__ import annotations

import json
from pathlib import Path

from palette_ai.models.palette_result import PaletteResult


def write(result: PaletteResult, path: Path) -> None:
    """Write a PaletteResult as pretty JSON to `path`."""
    payload = {
        "source": str(result.source),
        "processor": result.processor,
        "elapsed_ms": round(result.elapsed_ms, 3),
        "swatches": [
            {"hex": s.hex, "rgb": list(s.rgb), "weight": round(s.weight, 5), "name": s.name}
            for s in result.swatches
        ],
        "meta": result.meta,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
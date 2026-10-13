"""GIMP .gpl palette output driver."""

from __future__ import annotations

from pathlib import Path

from palette_ai.models.palette_result import PaletteResult


def write(result: PaletteResult, path: Path) -> None:
    """Write a PaletteResult as a GIMP .gpl palette file."""
    lines = ["GIMP Palette", f"Name: {result.source.stem}", "Columns: 8", "#"]
    for s in result.swatches:
        r, g, b = s.rgb
        label = s.name or f"swatch-{s.hex.lstrip('#').upper()}"
        lines.append(f"{r:3d} {g:3d} {b:3d}\t{label}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
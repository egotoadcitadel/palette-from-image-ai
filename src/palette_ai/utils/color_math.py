"""Color space conversions and hex helpers used across the pipeline."""

from __future__ import annotations

import numpy as np


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = (max(0, min(255, int(c))) for c in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) != 6:
        raise ValueError(f"bad hex: {value!r}")
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """sRGB uint8 (N,3) -> CIELAB float (N,3). D65 white point."""
    arr = rgb.astype(np.float64) / 255.0
    linear = np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)
    x = linear @ np.array([0.4124, 0.3576, 0.1805])
    y = linear @ np.array([0.2126, 0.7152, 0.0722])
    z = linear @ np.array([0.0193, 0.1192, 0.9505])
    xyz = np.stack([x, y, z], axis=-1) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16.0 / 116.0)
    lab = np.empty_like(f)
    lab[..., 0] = 116.0 * f[..., 1] - 16.0
    lab[..., 1] = 500.0 * (f[..., 0] - f[..., 1])
    lab[..., 2] = 200.0 * (f[..., 1] - f[..., 2])
    return lab


def lab_to_rgb(lab: np.ndarray) -> tuple[int, int, int]:
    """Single CIELAB (3,) -> sRGB uint8 tuple."""
    L, a, b = float(lab[0]), float(lab[1]), float(lab[2])
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    xr = fx**3 if fx**3 > 0.008856 else (fx - 16.0 / 116.0) / 7.787
    yr = ((L + 16.0) / 116.0) ** 3 if L > 8.0 else L / 903.3
    zr = fz**3 if fz**3 > 0.008856 else (fz - 16.0 / 116.0) / 7.787
    xyz = np.array([xr, yr, zr]) * np.array([0.95047, 1.0, 1.08883])
    linear = xyz @ np.array(
        [[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]
    )
    srgb = np.where(linear <= 0.0031308, 12.92 * linear, 1.055 * linear ** (1 / 2.4) - 0.055)
    return tuple(int(round(max(0.0, min(1.0, c)) * 255)) for c in srgb)  # type: ignore[return-value]
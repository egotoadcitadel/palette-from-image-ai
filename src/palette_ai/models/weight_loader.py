"""ONNX model loader with SHA-256 manifest verification.

*If the manifest is missing the loader returns None and callers fall back to
the classical kmeans path — this keeps a fresh clone runnable without weights.*
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import onnxruntime as ort

logger = logging.getLogger(__name__)

_WEIGHTS_DIR = Path(__file__).resolve().parent / "weights"
_MODEL_PATH = _WEIGHTS_DIR / "color_embed.onnx"
_MANIFEST_PATH = _WEIGHTS_DIR / "manifest.json"

_session: ort.InferenceSession | None = None


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify() -> bool:
    if not _MODEL_PATH.is_file() or not _MANIFEST_PATH.is_file():
        logger.info("model weights absent; AI processor disabled")
        return False
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = manifest.get("color_embed.onnx", {}).get("sha256")
    actual = _sha256(_MODEL_PATH)
    if expected != actual:
        logger.error("model hash mismatch: expected %s got %s", expected, actual)
        return False
    return True


def load_session() -> ort.InferenceSession | None:
    """Return a cached ONNX session, or None if weights are unavailable/invalid."""
    global _session
    if _session is not None:
        return _session
    if not _verify():
        return None
    _session = ort.InferenceSession(
        str(_MODEL_PATH),
        providers=["CPUExecutionProvider"],
        sess_options=_opts(),
    )
    return _session


def _opts() -> ort.SessionOptions:
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = 4
    opts.graph_optim
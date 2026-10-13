"""Worker pool — runs processors in a bounded thread pool with retry."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from palette_ai.models.palette_result import JobContext, PaletteResult
from palette_ai.processors import ProcessorError, get_processor

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class JobOutcome:
    image: Path
    result: PaletteResult | None
    error: str | None


def run_batch(
    images: list[Path],
    processor_name: str,
    palette_size: int,
    scratch_dir: Path,
    max_workers: int = 4,
    retries: int = 1,
) -> list[JobOutcome]:
    """Process a batch of images. Returns one JobOutcome per input, in order."""
    processor = get_processor(processor_name)
    outcomes: dict[Path, JobOutcome] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_run_one, processor, img, palette_size, scratch_dir, retries): img
            for img in images
        }
        for fut in as_completed(futures):
            img = futures[fut]
            outcomes[img] = fut.result()

    return [outcomes[img] for img in images]


def _run_one(processor, image: Path, palette_size: int, scratch: Path, retries: int) -> JobOutcome:
    last_err: str | None = None
    for attempt in range(1, retries + 2):
        ctx = JobContext(
            image_path=image,
            palette_size=palette_size,
            settings_snapshot={},
            scratch_dir=scratch,
            attempt=attempt,
        )
        try:
            return JobOutcome(image=image, result=processor.run(ctx), error=None)
        except ProcessorError as exc:
            last_err = str(exc)
            logger.warning("attempt %d failed for %s: %s", attempt, image.name, exc)
        except Exception as exc:  # noqa: BLE001 — worker boundary, log and continue
            last_err = f"unexpected: {exc}"
            logger.exception("unexpected failure on %s", image.name)
            break
    return JobOutcome(image=image, result=None, error=last_err)
# Contributing to palette-from-image-ai

Thanks for wanting to mash some taters with us. This repo is a Windows desktop
tool that pulls a usable color palette out of any image — photos, screenshots,
concept art, wallpapers — using an AI color-clustering pipeline plus a set of
classical quantizers as fallback.

## Ground rules

- Python 3.11+ on Windows 10/11. No Linux-only deps in the core path.
- One feature per PR. If you touch a processor, add a test in `tests/`.
- Run `ruff` and `pytest` before opening a PR. CI runs both.
- Keep the pipeline contract stable: every processor takes a `JobContext`
  and returns a `PaletteResult`. Handlers don't talk to each other directly.
- No new heavyweight deps without a note in the PR body explaining size and
  cold-start impact.

## Project layout

```
src/palette_ai/
  ingest/        image loading + validation handlers
  processors/    color extraction workers (AI + classical)
  drivers/       output writers (ase, gpl, json, png, clipboard)
  jobs/          queue, worker pool, retry policy
  models/        ONNX model wrappers + weight manifest
  utils/         color math, image helpers, logging
  config/        settings schema + defaults
cmd/             CLI entrypoints
tests/           unit + pipeline integration
```

## Adding a processor

1. Subclass `BaseProcessor` in `src/palette_ai/processors/`.
2. Implement `run(ctx: JobContext) -> PaletteResult`.
3. Register it in `processors/registry.py`.
4. Add a fixture image under `tests/fixtures/` and assert palette size +
   dominant hue within tolerance.

## Adding an output driver

Drivers write a `PaletteResult` to a file or the clipboard. Implement
`write(result, path) -> None` and register in `drivers/registry.py`. Keep
writers pure — no printing, no logging side effects beyond `logger.debug`.

## Style

- `ruff` config lives in `pyproject.toml`. Line length 100.
- Type hints on every public function. `mypy --strict` on `src/`.
- Prefer `pathlib.Path` over string paths.

## Reporting bugs

Open an issue with: Windows version, Python version, the input image (or a
similar one), the command you ran, and the traceback. If it's a color
accuracy bug, attach the palette you got and the palette you expected.
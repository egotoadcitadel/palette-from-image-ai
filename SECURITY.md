# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@palette-from-image-ai.dev` with a description, a minimal
reproducer, and the affected version. Do not open a public issue for
security bugs. We aim to acknowledge within 72 hours and ship a patch
within 14 days for confirmed issues.

## Scope

In scope:
- Malformed image files that crash the loader or escape the ingest sandbox.
- Path traversal in the export drivers (writing outside the chosen dir).
- ONNX model file tampering / weight manifest mismatch.
- Any code path that writes to disk without an explicit user-chosen path.

Out of scope:
- Palettes that are "ugly" or subjectively wrong.
- Performance on absurdly large inputs (>200MP) — we downscale by design.
- Third-party plugins that users drop into `plugins/` themselves.

## Hardening notes

- Image decoding runs through Pillow with `Image.MAX_IMAGE_PIXELS` capped.
- All export drivers resolve the target path and refuse to write outside the
  user-selected output directory.
- Model weights are verified against `models/weights/manifest.json` (SHA-256)
  before load.
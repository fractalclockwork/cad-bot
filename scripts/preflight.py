#!/usr/bin/env python3
"""Environment preflight for cad-bot (runs inside the Docker image)."""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import part_name, resolve  # noqa: E402


def fail(msg: str, *, remediation: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    print(f"Remediation: {remediation}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    report: dict = {"ok": True, "checks": []}

    uv = shutil.which("uv")
    if not uv:
        fail(
            "uv not found on PATH inside the container.",
            remediation="Rebuild the image: docker compose build",
        )
    report["checks"].append({"name": "uv", "path": uv, "ok": True})

    try:
        import cadquery as cq

        cq_ver = getattr(cq, "__version__", "unknown")
    except Exception as exc:  # noqa: BLE001
        fail(
            f"cadquery import failed: {exc}",
            remediation="Rebuild with locked deps: docker compose build",
        )
    report["checks"].append({"name": "cadquery", "version": cq_ver, "ok": True})

    out = Path(os.environ.get("CAD_BOT_OUTPUT", "/work/output"))
    try:
        out.mkdir(parents=True, exist_ok=True)
        probe = out / ".preflight_write"
        probe.write_text("ok\n", encoding="utf-8")
        probe.unlink(missing_ok=True)
    except OSError as exc:
        fail(
            f"output directory not writable at {out}: {exc}",
            remediation="Ensure ./output exists on the host and is mounted read-write",
        )
    report["checks"].append({"name": "output_writable", "path": str(out), "ok": True})

    parts = Path("/work/parts")
    if not parts.is_dir():
        fail(
            f"parts directory missing: {parts}",
            remediation="Mount ./parts into the container (see docker-compose.yml)",
        )
    report["checks"].append({"name": "parts_readable", "path": str(parts), "ok": True})

    name = part_name()
    paths = resolve(name)
    if not paths.root.is_dir():
        fail(
            f"PART={name} directory missing: {paths.root}",
            remediation=f"Create with ./scripts/new_part.sh {name} or set PART to an existing part",
        )
    if not paths.model.is_file():
        fail(
            f"PART={name} model missing: {paths.model}",
            remediation="Add model.py under the part directory",
        )
    report["checks"].append({"name": "part", "part": name, "model": str(paths.model), "ok": True})

    print(json.dumps(report, indent=2))
    print("PREFLIGHT PASS")


if __name__ == "__main__":
    main()

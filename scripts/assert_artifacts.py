#!/usr/bin/env python3
"""Verify CadQuery pipeline artifacts under ./output/<PART>/."""
from __future__ import annotations

import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import ensure_part_layout, resolve  # noqa: E402


def fail(msg: str) -> None:
    print(f"ASSERT FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_exists(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path}")
    if path.stat().st_size <= 0:
        fail(f"empty file: {path}")


def count_stl_facets(path: Path) -> int:
    data = path.read_bytes()
    if data.startswith(b"solid") and b"facet" in data[:2048]:
        return data.count(b"facet normal")
    if len(data) < 84:
        fail(f"STL too small to be binary: {path}")
    (n,) = struct.unpack_from("<I", data, 80)
    return int(n)


def check_dxf(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "SECTION" not in text and "0\nSECTION" not in text and "ENTITIES" not in text:
        if "LINE" not in text and "CIRCLE" not in text and "LWPOLYLINE" not in text and "SPLINE" not in text:
            if len(text) < 20:
                fail(f"DXF header/content invalid: {path}")
    entities = 0
    for token in ("LINE", "CIRCLE", "ARC", "LWPOLYLINE", "POLYLINE", "SPLINE", "POINT", "ELLIPSE"):
        entities += text.count(token)
    if entities <= 0:
        entities = text.count("VERTEX") + text.count("AcDb")
    if entities <= 0:
        fail(f"DXF has no recognizable 2D entities: {path}")
    return entities


def main() -> None:
    paths = ensure_part_layout(resolve())
    step, stl, dxf = paths.step, paths.stl, paths.profile_dxf

    check_exists(step)
    head = step.read_bytes()[:64]
    if b"ISO-10303" not in head and b"STEP" not in head.upper():
        if len(head) < 16:
            fail(f"STEP file looks corrupt: {step}")
    print(f"OK {step.name} ({step.stat().st_size} bytes)")

    check_exists(stl)
    facets = count_stl_facets(stl)
    if facets <= 0:
        fail(f"STL has zero facets: {stl}")
    print(f"OK {stl.name} ({stl.stat().st_size} bytes, facets={facets})")

    check_exists(dxf)
    entities = check_dxf(dxf)
    print(f"OK {dxf.name} ({dxf.stat().st_size} bytes, entity_tokens={entities})")

    print("ARTIFACT MATRIX PASS")


if __name__ == "__main__":
    main()

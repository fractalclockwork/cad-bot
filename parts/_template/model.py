#!/usr/bin/env python3
"""CadQuery part template — replace params and build_part()."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "PART_NAME")
DIM_TOL = 0.5

# Drawing-bound params (mm) — fill from drawings/dims.md
overall_length = 10.0


def build_part() -> cq.Workplane:
    return cq.Workplane("XY").box(overall_length, overall_length, 5.0)


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid() or float(solid.Volume()) <= 0:
        raise RuntimeError("invalid or empty solid")
    bb = solid.BoundingBox()
    print(f"ASSERT PASS BB=({bb.xlen:.2f},{bb.ylen:.2f},{bb.zlen:.2f})")


def export_artifacts(shape: cq.Workplane, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step = out_dir / f"{PART_NAME}.step"
    stl = out_dir / f"{PART_NAME}.stl"
    cq.exporters.export(shape, str(step))
    cq.exporters.export(shape, str(stl))
    print(f"EXPORT OK: {step}, {stl}")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"/work/output/{PART_NAME}")
    shape = build_part()
    assert_geometry(shape)
    export_artifacts(shape, out)


if __name__ == "__main__":
    main()

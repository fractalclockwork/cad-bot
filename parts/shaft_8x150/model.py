#!/usr/bin/env python3
"""Parametric Ø8 × 150 mm plain shaft — CadQuery solid.

Coordinate convention (matches KP08 bore for later assembly):
- Y: shaft axis (length)
- X / Z: radial
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "shaft_8x150")
DIM_TOL = 0.5

# Spec params (mm)
shaft_diameter = 8.0
shaft_length = 150.0


def build_part() -> cq.Workplane:
    """Cylinder centered at origin, axis along Y (−L/2 … +L/2)."""
    return (
        cq.Workplane("XZ")
        .workplane(offset=-shaft_length / 2.0)
        .circle(shaft_diameter / 2.0)
        .extrude(shaft_length)
    )


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    expected_vol = math.pi * (shaft_diameter / 2.0) ** 2 * shaft_length
    if volume <= 0:
        raise RuntimeError(f"Geometry assertion failed: Volume()={volume}")
    if abs(volume - expected_vol) > max(1.0, 0.02 * expected_vol):
        raise RuntimeError(
            f"Volume check failed: got {volume:.3f}, expected ~{expected_vol:.3f}"
        )

    bb = solid.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if abs(dy - shaft_length) > DIM_TOL:
        raise RuntimeError(
            f"Length (Y) check failed: BB.ylen={dy:.3f}, expected {shaft_length} ± {DIM_TOL}"
        )
    if abs(dx - shaft_diameter) > DIM_TOL:
        raise RuntimeError(
            f"Diameter (X) check failed: BB.xlen={dx:.3f}, expected {shaft_diameter} ± {DIM_TOL}"
        )
    if abs(dz - shaft_diameter) > DIM_TOL:
        raise RuntimeError(
            f"Diameter (Z) check failed: BB.zlen={dz:.3f}, expected {shaft_diameter} ± {DIM_TOL}"
        )

    print("SPEC CHECK:")
    print(f"  d shaft_diameter  expect  8.0  BB.x={dx:.2f} BB.z={dz:.2f}")
    print(f"  L shaft_length    expect 150.0 BB.y={dy:.2f}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"(expect ~{expected_vol:.3f}) BB=({dx:.2f},{dy:.2f},{dz:.2f}) shaft_axis=Y"
    )


def export_artifacts(shape: cq.Workplane, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{PART_NAME}.step"
    stl_path = out_dir / f"{PART_NAME}.stl"

    cq.exporters.export(shape, str(step_path))
    cq.exporters.export(shape, str(stl_path))

    for path in (step_path, stl_path):
        if not path.is_file() or path.stat().st_size <= 0:
            raise RuntimeError(f"Export failed or empty: {path}")
        print(f"EXPORT OK: {path} ({path.stat().st_size} bytes)")


def main() -> None:
    out = Path(f"/work/output/{PART_NAME}")
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])

    shape = build_part()
    assert_geometry(shape)
    export_artifacts(shape, out)
    print(f"{PART_NAME} CadQuery workflow complete")


if __name__ == "__main__":
    main()

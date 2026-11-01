#!/usr/bin/env python3
"""Parametric 100×150×5 mm plate for one McMaster 1434K33 flange bearing.

Coordinate convention (matches flange-mount mcm_1434k33):
- X: bolt pitch axis (plate width 100)
- Y: flange short / plate depth 150
- Z: up; bottom on Z=0; shaft through plate along Z

Two mount holes + centered shaft clearance for thru-plate flange mount.
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "plate_100x150x5_mcm_1434k33")
DIM_TOL = 0.5

# Plate (mm)
plate_width = 100.0  # X
plate_depth = 150.0  # Y
plate_thickness = 5.0  # Z

# mcm_1434k33 mounting (measured from framed vendor STEP)
bolt_hole_pitch = 30.9  # mount_pitch
bolt_hole_diameter = 5.5  # mount_hole_d
# Ø8 shaft + 2 mm clearance; no boss below bearing mount face
shaft_clearance_diameter = 10.0


def _bolt_hole_points() -> list[tuple[float, float]]:
    half = bolt_hole_pitch / 2.0
    return [(-half, 0.0), (half, 0.0)]


def build_part() -> cq.Workplane:
    """Plate centered in XY; two bolt holes + center shaft clearance."""
    plate = (
        cq.Workplane("XY")
        .box(plate_width, plate_depth, plate_thickness, centered=(True, True, False))
    )
    bolt_holes = (
        cq.Workplane("XY")
        .workplane(offset=-1.0)
        .pushPoints(_bolt_hole_points())
        .circle(bolt_hole_diameter / 2.0)
        .extrude(plate_thickness + 2.0)
    )
    shaft_hole = (
        cq.Workplane("XY")
        .workplane(offset=-1.0)
        .circle(shaft_clearance_diameter / 2.0)
        .extrude(plate_thickness + 2.0)
    )
    return plate.cut(bolt_holes).cut(shaft_hole)


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    solid_vol = plate_width * plate_depth * plate_thickness
    bolt_vol = 2.0 * math.pi * (bolt_hole_diameter / 2.0) ** 2 * plate_thickness
    shaft_vol = math.pi * (shaft_clearance_diameter / 2.0) ** 2 * plate_thickness
    expected_vol = solid_vol - bolt_vol - shaft_vol
    if volume <= 0:
        raise RuntimeError(f"Geometry assertion failed: Volume()={volume}")
    if abs(volume - expected_vol) > 1.0:
        raise RuntimeError(
            f"Volume check failed: got {volume:.3f}, expected ~{expected_vol:.3f}"
        )

    bb = solid.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if abs(dx - plate_width) > DIM_TOL:
        raise RuntimeError(
            f"Width (X) check failed: BB.xlen={dx:.3f}, expected {plate_width}"
        )
    if abs(dy - plate_depth) > DIM_TOL:
        raise RuntimeError(
            f"Depth (Y) check failed: BB.ylen={dy:.3f}, expected {plate_depth}"
        )
    if abs(dz - plate_thickness) > DIM_TOL:
        raise RuntimeError(
            f"Thickness (Z) check failed: BB.zlen={dz:.3f}, expected {plate_thickness}"
        )
    if abs(float(bb.zmin)) > DIM_TOL:
        raise RuntimeError(f"Plate bottom should sit on Z=0; zmin={bb.zmin:.3f}")

    if abs(bolt_hole_pitch - 30.9) > 1e-9:
        raise RuntimeError(f"bolt_hole_pitch must be 30.9, got {bolt_hole_pitch}")
    if abs(bolt_hole_diameter - 5.5) > 1e-9:
        raise RuntimeError(f"bolt_hole_diameter must be 5.5, got {bolt_hole_diameter}")
    if abs(shaft_clearance_diameter - 10.0) > 1e-9:
        raise RuntimeError(
            f"shaft_clearance_diameter must be 10.0, got {shaft_clearance_diameter}"
        )

    print("SPEC CHECK:")
    print(f"  W plate_width      expect 100.0 BB.x={dx:.2f}")
    print(f"  D plate_depth      expect 150.0 BB.y={dy:.2f}")
    print(f"  t plate_thickness  expect   5.0 BB.z={dz:.2f}")
    print(f"  e bolt_hole_pitch  expect  30.9 param={bolt_hole_pitch:.2f}")
    print(f"  s hole_diameter    expect   5.5 param={bolt_hole_diameter:.2f}")
    print(f"  shaft_clearance_d  expect  10.0 param={shaft_clearance_diameter:.2f}")
    print(f"  bolt_holes         {_bolt_hole_points()}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"(expect ~{expected_vol:.3f}) BB=({dx:.2f},{dy:.2f},{dz:.2f})"
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

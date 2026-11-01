#!/usr/bin/env python3
"""Parametric 100×150×5 mm plate for two KP08 pillow blocks.

Coordinate convention (matches KP08):
- X: bolt pitch axis (plate width 100)
- Y: shaft / block-spacing axis (plate depth 150)
- Z: up; bottom on Z=0

Two KP08 patterns centered on X=0 at Y=±50 (100 mm apart on center).
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "plate_100x150x5")
DIM_TOL = 0.5

# Plate (mm)
plate_width = 100.0   # X
plate_depth = 150.0   # Y
plate_thickness = 5.0  # Z

# KP08 mounting (match parts/kp08)
bolt_hole_pitch = 42.0  # e
bolt_hole_diameter = 4.8  # s
block_spacing = 100.0  # center-to-center along Y
block_centers_y = (block_spacing / 2.0, -block_spacing / 2.0)  # +50, -50


def _hole_points() -> list[tuple[float, float]]:
    half = bolt_hole_pitch / 2.0
    pts: list[tuple[float, float]] = []
    for cy in block_centers_y:
        pts.append((-half, cy))
        pts.append((half, cy))
    return pts


def build_part() -> cq.Workplane:
    """Plate centered in XY; four through-holes for two KP08 flanges."""
    plate = (
        cq.Workplane("XY")
        .box(plate_width, plate_depth, plate_thickness, centered=(True, True, False))
    )
    holes = (
        cq.Workplane("XY")
        .workplane(offset=-1.0)
        .pushPoints(_hole_points())
        .circle(bolt_hole_diameter / 2.0)
        .extrude(plate_thickness + 2.0)
    )
    return plate.cut(holes)


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    solid_vol = plate_width * plate_depth * plate_thickness
    hole_vol = 4.0 * math.pi * (bolt_hole_diameter / 2.0) ** 2 * plate_thickness
    expected_vol = solid_vol - hole_vol
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

    if abs(bolt_hole_pitch - 42.0) > 1e-9:
        raise RuntimeError(f"bolt_hole_pitch must be 42.0, got {bolt_hole_pitch}")
    if abs(block_spacing - 100.0) > 1e-9:
        raise RuntimeError(f"block_spacing must be 100.0, got {block_spacing}")

    end_margin = (plate_depth - block_spacing) / 2.0
    if abs(end_margin - 25.0) > 1e-9:
        raise RuntimeError(f"end margin to block centers must be 25, got {end_margin}")

    print("SPEC CHECK:")
    print(f"  W plate_width      expect 100.0 BB.x={dx:.2f}")
    print(f"  D plate_depth      expect 150.0 BB.y={dy:.2f}")
    print(f"  t plate_thickness  expect   5.0 BB.z={dz:.2f}")
    print(f"  e bolt_hole_pitch  expect  42.0 param={bolt_hole_pitch:.2f}")
    print(f"  s hole_diameter    expect   4.8 param={bolt_hole_diameter:.2f}")
    print(f"  block_spacing      expect 100.0 centers_y={block_centers_y}")
    print(f"  end_margin         expect  25.0 got={end_margin:.2f}")
    print(f"  holes              {_hole_points()}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"(expect ~{expected_vol:.3f}) BB=({dx:.2f},{dy:.2f},{dz:.2f})"
    )


def export_profile_dxf(dxf_path: Path) -> None:
    """Top view: outline, centerlines, four KP08 mounting holes."""
    import ezdxf

    half_w = plate_width / 2.0
    half_d = plate_depth / 2.0
    attrs = {"color": 0, "lineweight": 35}
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    msp.add_lwpolyline(
        [
            (-half_w, -half_d),
            (half_w, -half_d),
            (half_w, half_d),
            (-half_w, half_d),
        ],
        close=True,
        dxfattribs=attrs,
    )
    msp.add_line((-half_w, 0.0), (half_w, 0.0), dxfattribs=attrs)
    msp.add_line((0.0, -half_d), (0.0, half_d), dxfattribs=attrs)
    r = bolt_hole_diameter / 2.0
    for x, y in _hole_points():
        msp.add_circle((x, y), r, dxfattribs=attrs)
    doc.saveas(str(dxf_path))


def export_artifacts(shape: cq.Workplane, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{PART_NAME}.step"
    stl_path = out_dir / f"{PART_NAME}.stl"
    dxf_path = out_dir / f"{PART_NAME}_profile.dxf"

    cq.exporters.export(shape, str(step_path))
    cq.exporters.export(shape, str(stl_path))
    export_profile_dxf(dxf_path)

    for path in (step_path, stl_path, dxf_path):
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

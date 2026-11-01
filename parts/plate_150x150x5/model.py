#!/usr/bin/env python3
"""Parametric 150×150×5 mm plain mounting plate — CadQuery solid.

Coordinate convention (matches KP08 mounting frame):
- X / Y: plate plane
- Z: thickness (up); bottom on Z=0, top at Z=plate_thickness
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "plate_150x150x5")
DIM_TOL = 0.5

# Spec params (mm)
plate_width = 150.0   # X
plate_depth = 150.0   # Y
plate_thickness = 5.0  # Z


def build_part() -> cq.Workplane:
    """Square plate centered in XY; bottom on Z=0."""
    return (
        cq.Workplane("XY")
        .box(plate_width, plate_depth, plate_thickness, centered=(True, True, False))
    )


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    expected_vol = plate_width * plate_depth * plate_thickness
    if volume <= 0:
        raise RuntimeError(f"Geometry assertion failed: Volume()={volume}")
    if abs(volume - expected_vol) > DIM_TOL:
        raise RuntimeError(
            f"Volume check failed: got {volume:.3f}, expected {expected_vol:.3f}"
        )

    bb = solid.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if abs(dx - plate_width) > DIM_TOL:
        raise RuntimeError(
            f"Width (X) check failed: BB.xlen={dx:.3f}, expected {plate_width} ± {DIM_TOL}"
        )
    if abs(dy - plate_depth) > DIM_TOL:
        raise RuntimeError(
            f"Depth (Y) check failed: BB.ylen={dy:.3f}, expected {plate_depth} ± {DIM_TOL}"
        )
    if abs(dz - plate_thickness) > DIM_TOL:
        raise RuntimeError(
            f"Thickness (Z) check failed: BB.zlen={dz:.3f}, expected {plate_thickness} ± {DIM_TOL}"
        )
    if abs(float(bb.zmin)) > DIM_TOL:
        raise RuntimeError(f"Plate bottom should sit on Z=0; zmin={bb.zmin:.3f}")

    print("SPEC CHECK:")
    print(f"  W plate_width     expect 150.0 BB.x={dx:.2f}")
    print(f"  D plate_depth     expect 150.0 BB.y={dy:.2f}")
    print(f"  t plate_thickness expect   5.0 BB.z={dz:.2f}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"BB=({dx:.2f},{dy:.2f},{dz:.2f}) base_on_Z0"
    )


def export_profile_dxf(dxf_path: Path) -> None:
    """Top-view outline: 150×150 rectangle + drafting centerlines."""
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

#!/usr/bin/env python3
"""Parametric KP08 pillow block housing — CadQuery primary solid model.

Coordinate convention:
- X: long base axis / bolt-hole pitch
- Y: shaft axis (bore through the housing)
- Z: up from mounting base

Drawing reference (front elevation):
- a = overall_length = 55
- e = bolt_hole_pitch = 42
- s = bolt_hole_diameter = 4.8
- h = base_center_height = 15
- g = base_thickness = 5
- w = overall_height = 29
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

# --- KP08 top-level parametric variables (mm) — drawing labels ---
bore_diameter = 8.0
base_center_height = 15.0  # h
bolt_hole_pitch = 42.0  # e (center-to-center of mounting holes)
overall_length = 55.0  # a
housing_width = 13.0
bolt_hole_diameter = 4.8  # s
base_thickness = 5.0  # g
overall_height = 29.0  # w

# Derived from drawing: rounded ends centered on bolt holes → a = e + 2*r
flange_radius = (overall_length - bolt_hole_pitch) / 2.0  # 6.5
flange_diameter = flange_radius * 2.0
# Outer housing reaches z=w; shaft center at z=h → boss radius = w - h
boss_od = 2.0 * (overall_height - base_center_height)  # 28
boss_length = housing_width + 6.0
DIM_TOL = 0.5

PART_NAME = os.environ.get("PART", "kp08")


def _capsule_base() -> cq.Workplane:
    """Capsule base: length a, bolt holes on pitch e, end radii (a-e)/2."""
    half_pitch = bolt_hole_pitch / 2.0
    r = flange_radius

    left = cq.Workplane("XY").center(-half_pitch, 0).circle(r).extrude(base_thickness)
    right = cq.Workplane("XY").center(half_pitch, 0).circle(r).extrude(base_thickness)
    bridge = (
        cq.Workplane("XY")
        .box(bolt_hole_pitch, flange_diameter, base_thickness, centered=(True, True, False))
    )
    return left.union(right).union(bridge)


def build_part() -> cq.Workplane:
    """Build KP08-style pillow block: shaft bore along +Y."""
    half_pitch = bolt_hole_pitch / 2.0
    base = _capsule_base()

    body_height = overall_height - base_thickness
    body = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .box(
            boss_od,
            housing_width,
            body_height,
            centered=(True, True, False),
        )
    )

    boss = (
        cq.Workplane("XZ")
        .workplane(offset=-boss_length / 2.0)
        .center(0, base_center_height)
        .circle(boss_od / 2.0)
        .extrude(boss_length)
    )

    solid = base.union(body).union(boss)

    bore = (
        cq.Workplane("XZ")
        .workplane(offset=-overall_length)
        .center(0, base_center_height)
        .circle(bore_diameter / 2.0)
        .extrude(overall_length * 2.0)
    )
    solid = solid.cut(bore)

    holes = (
        cq.Workplane("XY")
        .workplane(offset=-1.0)
        .pushPoints([(-half_pitch, 0), (half_pitch, 0)])
        .circle(bolt_hole_diameter / 2.0)
        .extrude(base_thickness + 2.0)
    )
    solid = solid.cut(holes)

    return solid


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    if volume <= 0:
        raise RuntimeError(f"Geometry assertion failed: Volume()={volume} (expected > 0)")

    bb = solid.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if min(dx, dy, dz) <= 0:
        raise RuntimeError(f"Geometry assertion failed: empty BoundingBox {dx=}/{dy=}/{dz=}")

    if abs(dx - overall_length) > DIM_TOL:
        raise RuntimeError(
            f"Overall length (a) check failed: BB.xlen={dx:.3f}, expected {overall_length} ± {DIM_TOL}"
        )

    if abs(dz - overall_height) > DIM_TOL:
        raise RuntimeError(
            f"Overall height (w) check failed: BB.zlen={dz:.3f}, expected {overall_height} ± {DIM_TOL}"
        )

    if abs(float(bb.zmin)) > DIM_TOL:
        raise RuntimeError(f"Base should sit on Z=0; zmin={bb.zmin:.3f}")

    if not (float(bb.zmin) - DIM_TOL <= base_center_height <= float(bb.zmax) + DIM_TOL):
        raise RuntimeError(
            f"Center height (h) check failed: h={base_center_height} "
            f"not in BB z=[{bb.zmin:.3f},{bb.zmax:.3f}]"
        )

    if abs(bolt_hole_pitch - 42.0) > 1e-9:
        raise RuntimeError(f"bolt_hole_pitch (e) must be 42.0, got {bolt_hole_pitch}")
    if abs(bolt_hole_diameter - 4.8) > 1e-9:
        raise RuntimeError(f"bolt_hole_diameter (s) must be 4.8, got {bolt_hole_diameter}")
    if abs(base_thickness - 5.0) > 1e-9:
        raise RuntimeError(f"base_thickness (g) must be 5.0, got {base_thickness}")

    if dy < boss_length - 2.0:
        raise RuntimeError(
            f"Shaft-axis (Y) span too small: BB.ylen={dy:.3f}, expected ~boss_length={boss_length}"
        )

    print("DRAWING CHECK:")
    print(f"  a overall_length   expect 55.0  BB.x={dx:.2f}")
    print(f"  e bolt_hole_pitch  expect 42.0  param={bolt_hole_pitch:.2f}")
    print(f"  s hole_diameter    expect  4.8  param={bolt_hole_diameter:.2f}")
    print(f"  h center_height    expect 15.0  param={base_center_height:.2f}")
    print(f"  g base_thickness   expect  5.0  param={base_thickness:.2f}")
    print(f"  w overall_height   expect 29.0  BB.z={dz:.2f}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"BB=({dx:.2f},{dy:.2f},{dz:.2f}) shaft_axis=Y"
    )


def export_profile_dxf(dxf_path: Path) -> None:
    """Top-view 2D base profile: capsule + two flange holes only (no shaft bore)."""
    import ezdxf

    half_pitch = bolt_hole_pitch / 2.0
    r = flange_radius
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    msp.add_lwpolyline(
        [
            (-half_pitch, r, 0),
            (half_pitch, r, -1),
            (half_pitch, -r, 0),
            (-half_pitch, -r, -1),
        ],
        format="xyb",
        close=True,
        dxfattribs={"color": 0, "lineweight": 35},
    )
    hole_attrs = {"color": 0, "lineweight": 35}
    msp.add_circle((-half_pitch, 0), bolt_hole_diameter / 2.0, dxfattribs=hole_attrs)
    msp.add_circle((half_pitch, 0), bolt_hole_diameter / 2.0, dxfattribs=hole_attrs)
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

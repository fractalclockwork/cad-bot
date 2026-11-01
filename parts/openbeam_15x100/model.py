#!/usr/bin/env python3
"""Parametric OpenBeam-style 15×15 mm T-slot extrusion — 100 mm length.

Coordinate convention (assembly-ready, matches shaft axis):
- Y: extrusion length (−L/2 … +L/2)
- X / Z: cross-section (15 × 15)

Profile (approximation of OpenBeam):
- Outer square 15×15
- Four side T-slots (~3 mm opening, M3 nut capture)
- Center hollow sized for M3 tap (~Ø2.5 mm)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "openbeam_15x100")
DIM_TOL = 0.5

# Spec params (mm)
beam_size = 15.0
beam_length = 100.0
center_bore_diameter = 2.5  # M3 tap sized hollow
slot_opening = 3.0  # captures 3 mm panel / M3 access
nut_pocket_width = 5.5  # DIN934 M3 across flats
slot_neck_depth = 1.2
slot_total_depth = 3.8


def _t_slot_cutter(face: str) -> cq.Workplane:
    """Full-length T-slot cutter for one outer face (face in {+X,-X,+Z,-Z})."""
    half = beam_size / 2.0
    neck_w = slot_opening
    pocket_w = nut_pocket_width
    # Neck sits at outer face; pocket is inward of the neck
    # Build in local coords then rotate/translate onto the face.

    def bars_along_y(x0: float, z0: float, dx: float, dz: float) -> cq.Workplane:
        return (
            cq.Workplane("XZ")
            .workplane(offset=-beam_length / 2.0)
            .center(x0, z0)
            .rect(dx, dz)
            .extrude(beam_length)
        )

    if face == "+X":
        # Outer at x=+half; cut toward −X
        neck = bars_along_y(half - slot_neck_depth / 2.0, 0.0, slot_neck_depth + 0.2, neck_w)
        pocket = bars_along_y(
            half - slot_neck_depth - (slot_total_depth - slot_neck_depth) / 2.0,
            0.0,
            slot_total_depth - slot_neck_depth + 0.05,
            pocket_w,
        )
        return neck.union(pocket)
    if face == "-X":
        neck = bars_along_y(-(half - slot_neck_depth / 2.0), 0.0, slot_neck_depth + 0.2, neck_w)
        pocket = bars_along_y(
            -(half - slot_neck_depth - (slot_total_depth - slot_neck_depth) / 2.0),
            0.0,
            slot_total_depth - slot_neck_depth + 0.05,
            pocket_w,
        )
        return neck.union(pocket)
    if face == "+Z":
        neck = bars_along_y(0.0, half - slot_neck_depth / 2.0, neck_w, slot_neck_depth + 0.2)
        pocket = bars_along_y(
            0.0,
            half - slot_neck_depth - (slot_total_depth - slot_neck_depth) / 2.0,
            pocket_w,
            slot_total_depth - slot_neck_depth + 0.05,
        )
        return neck.union(pocket)
    if face == "-Z":
        neck = bars_along_y(0.0, -(half - slot_neck_depth / 2.0), neck_w, slot_neck_depth + 0.2)
        pocket = bars_along_y(
            0.0,
            -(half - slot_neck_depth - (slot_total_depth - slot_neck_depth) / 2.0),
            pocket_w,
            slot_total_depth - slot_neck_depth + 0.05,
        )
        return neck.union(pocket)
    raise ValueError(f"unknown face {face}")


def build_part() -> cq.Workplane:
    """15×15 OpenBeam-style bar, length along Y, centered at origin."""
    bar = (
        cq.Workplane("XZ")
        .workplane(offset=-beam_length / 2.0)
        .rect(beam_size, beam_size)
        .extrude(beam_length)
    )

    bore = (
        cq.Workplane("XZ")
        .workplane(offset=-beam_length / 2.0 - 0.5)
        .circle(center_bore_diameter / 2.0)
        .extrude(beam_length + 1.0)
    )
    solid = bar.cut(bore)

    for face in ("+X", "-X", "+Z", "-Z"):
        solid = solid.cut(_t_slot_cutter(face))

    return solid


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("Geometry assertion failed: shape.val().isValid() is False")

    volume = float(solid.Volume())
    solid_bar = beam_size * beam_size * beam_length
    if volume <= 0:
        raise RuntimeError(f"Geometry assertion failed: Volume()={volume}")
    if volume >= solid_bar - 1.0:
        raise RuntimeError(
            f"Volume {volume:.3f} too close to solid bar {solid_bar:.3f}; slots/bore missing?"
        )

    bb = solid.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if abs(dx - beam_size) > DIM_TOL:
        raise RuntimeError(f"BB.xlen={dx:.3f}, expected {beam_size}")
    if abs(dy - beam_length) > DIM_TOL:
        raise RuntimeError(f"BB.ylen={dy:.3f}, expected {beam_length}")
    if abs(dz - beam_size) > DIM_TOL:
        raise RuntimeError(f"BB.zlen={dz:.3f}, expected {beam_size}")

    print("SPEC CHECK:")
    print(f"  section          expect 15×15   BB.x={dx:.2f} BB.z={dz:.2f}")
    print(f"  beam_length      expect 100.0   BB.y={dy:.2f}")
    print(f"  center_bore_d    expect   2.5   param={center_bore_diameter:.2f}")
    print(f"  slot_opening     expect   3.0   param={slot_opening:.2f}")
    print(
        f"ASSERT PASS: valid={solid.isValid()} volume={volume:.3f} mm^3 "
        f"(solid_bar={solid_bar:.1f}) BB=({dx:.2f},{dy:.2f},{dz:.2f}) axis=Y"
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

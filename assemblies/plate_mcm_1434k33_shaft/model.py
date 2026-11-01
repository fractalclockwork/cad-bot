#!/usr/bin/env python3
"""Assembly: plate_100x150x5_mcm_1434k33 + mcm_1434k33 + shaft_8x100.

Thru-plate flange mount (mm):
- plate: identity (top face Z=5)
- mcm_1434k33 @ (0, 0, 5) — flange on plate; bolts along Z over plate holes
- shaft_8x100: rotate native Y→Z, centered so Ø8 spans through plate + bore
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from part_config import load_part_module  # noqa: E402

PART_NAME = os.environ.get("PART", "plate_mcm_1434k33_shaft")
DIM_TOL = 1.0

PLATE_THICKNESS = 5.0
BEARING_HEIGHT = 16.8  # mcm_1434k33 overall_height along shaft
SHAFT_LENGTH = 100.0
# Mid of plate+bearing stack [0 .. 5+16.8]; shaft protrudes both sides
SHAFT_Z = (PLATE_THICKNESS + BEARING_HEIGHT) / 2.0  # 10.9


def _solid(wp: cq.Workplane) -> cq.Shape:
    return wp.val()


def build_assembly() -> tuple[cq.Assembly, cq.Compound]:
    plate_mod = load_part_module("plate_100x150x5_mcm_1434k33")
    bearing_mod = load_part_module("mcm_1434k33")
    shaft_mod = load_part_module("shaft_8x100")

    plate = _solid(plate_mod.build_part())
    bearing = _solid(bearing_mod.build_part())
    # shaft_8x100 is along Y; rotate +90° about X so length is along Z
    shaft = _solid(shaft_mod.build_part()).rotate((0, 0, 0), (1, 0, 0), 90)

    assy = cq.Assembly(name=PART_NAME)
    assy.add(plate, name="plate_100x150x5_mcm_1434k33")
    assy.add(
        bearing,
        name="mcm_1434k33",
        loc=cq.Location(cq.Vector(0, 0, PLATE_THICKNESS)),
    )
    assy.add(
        shaft,
        name="shaft_8x100",
        loc=cq.Location(cq.Vector(0, 0, SHAFT_Z)),
    )

    compound = assy.toCompound()
    return assy, compound


def assert_geometry(compound: cq.Compound) -> None:
    if not compound.isValid():
        raise RuntimeError("Assembly compound isValid() is False")

    volume = float(compound.Volume())
    if volume <= 0:
        raise RuntimeError(f"Assembly volume <= 0: {volume}")

    plate_mod = load_part_module("plate_100x150x5_mcm_1434k33")
    bearing_mod = load_part_module("mcm_1434k33")
    shaft_mod = load_part_module("shaft_8x100")
    expected = (
        float(_solid(plate_mod.build_part()).Volume())
        + float(_solid(bearing_mod.build_part()).Volume())
        + float(_solid(shaft_mod.build_part()).Volume())
    )
    if abs(volume - expected) > max(5.0, 0.02 * expected):
        raise RuntimeError(
            f"Assembly volume {volume:.3f} != sum of parts {expected:.3f}"
        )

    bb = compound.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    if abs(dx - 100.0) > DIM_TOL:
        raise RuntimeError(f"BB.xlen={dx:.3f}, expected ~100")
    if abs(dy - 150.0) > DIM_TOL:
        raise RuntimeError(f"BB.ylen={dy:.3f}, expected ~150")
    # Shaft along Z dominates height (~100 mm)
    if abs(dz - SHAFT_LENGTH) > DIM_TOL:
        raise RuntimeError(f"BB.zlen={dz:.3f}, expected ~{SHAFT_LENGTH} (shaft along Z)")
    expected_zmin = SHAFT_Z - SHAFT_LENGTH / 2.0
    expected_zmax = SHAFT_Z + SHAFT_LENGTH / 2.0
    if abs(float(bb.zmin) - expected_zmin) > DIM_TOL:
        raise RuntimeError(
            f"BB.zmin={bb.zmin:.3f}, expected ~{expected_zmin} (shaft thru plate)"
        )
    if abs(float(bb.zmax) - expected_zmax) > DIM_TOL:
        raise RuntimeError(
            f"BB.zmax={bb.zmax:.3f}, expected ~{expected_zmax} (shaft thru plate)"
        )
    # Shaft must span the plate thickness
    if not (float(bb.zmin) < 0.0 and float(bb.zmax) > PLATE_THICKNESS):
        raise RuntimeError(
            f"Shaft does not span plate: z=[{bb.zmin:.2f},{bb.zmax:.2f}] "
            f"vs plate [0,{PLATE_THICKNESS}]"
        )

    print("MATE CHECK:")
    print(f"  plate                identity  top_z={PLATE_THICKNESS}")
    print(f"  mcm_1434k33          Z={PLATE_THICKNESS} (flange on plate, shaft along Z)")
    print(f"  shaft_8x100          Z={SHAFT_Z} (rotated Y→Z, thru plate + bore)")
    print(
        f"ASSERT PASS: volume={volume:.3f} mm^3 (expect ~{expected:.3f}) "
        f"BB=({dx:.2f},{dy:.2f},{dz:.2f}) z=[{bb.zmin:.2f},{bb.zmax:.2f}]"
    )


def export_artifacts(assy: cq.Assembly, compound: cq.Compound, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{PART_NAME}.step"
    stl_path = out_dir / f"{PART_NAME}.stl"

    assy.save(str(step_path), exportType="STEP")
    cq.exporters.export(compound, str(stl_path))

    for path in (step_path, stl_path):
        if not path.is_file() or path.stat().st_size <= 0:
            raise RuntimeError(f"Export failed or empty: {path}")
        print(f"EXPORT OK: {path} ({path.stat().st_size} bytes)")


def main() -> None:
    out = Path(f"/work/output/{PART_NAME}")
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])

    assy, compound = build_assembly()
    assert_geometry(compound)
    export_artifacts(assy, compound, out)
    print(f"{PART_NAME} assembly workflow complete")


if __name__ == "__main__":
    main()

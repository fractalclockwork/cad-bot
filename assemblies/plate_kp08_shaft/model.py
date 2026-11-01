#!/usr/bin/env python3
"""Assembly: plate_100x150x5 + 2× kp08 + shaft_8x150.

Mates (mm):
- plate: identity (top face Z=5)
- kp08 @ (0, +50, 5) and (0, −50, 5) — bases on plate, bolts over plate holes
- shaft @ (0, 0, 20) — Z = plate_thickness(5) + kp08.base_center_height(15);
  Y-centered cylinder through both bores
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from part_config import load_part_module  # noqa: E402

PART_NAME = os.environ.get("PART", "plate_kp08_shaft")
DIM_TOL = 1.0

PLATE_THICKNESS = 5.0
KP08_CENTER_HEIGHT = 15.0  # h
BLOCK_Y = (50.0, -50.0)
SHAFT_Z = PLATE_THICKNESS + KP08_CENTER_HEIGHT  # 20


def _solid(wp: cq.Workplane) -> cq.Shape:
    return wp.val()


def build_assembly() -> tuple[cq.Assembly, cq.Compound]:
    plate_mod = load_part_module("plate_100x150x5")
    kp08_mod = load_part_module("kp08")
    shaft_mod = load_part_module("shaft_8x150")

    plate = _solid(plate_mod.build_part())
    kp08_a = _solid(kp08_mod.build_part())
    kp08_b = _solid(kp08_mod.build_part())
    shaft = _solid(shaft_mod.build_part())

    assy = cq.Assembly(name=PART_NAME)
    assy.add(plate, name="plate_100x150x5")
    assy.add(
        kp08_a,
        name="kp08_pos",
        loc=cq.Location(cq.Vector(0, BLOCK_Y[0], PLATE_THICKNESS)),
    )
    assy.add(
        kp08_b,
        name="kp08_neg",
        loc=cq.Location(cq.Vector(0, BLOCK_Y[1], PLATE_THICKNESS)),
    )
    assy.add(
        shaft,
        name="shaft_8x150",
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

    # Expected ≈ plate + 2×kp08 + shaft (from known part asserts)
    plate_mod = load_part_module("plate_100x150x5")
    kp08_mod = load_part_module("kp08")
    shaft_mod = load_part_module("shaft_8x150")
    expected = (
        float(_solid(plate_mod.build_part()).Volume())
        + 2.0 * float(_solid(kp08_mod.build_part()).Volume())
        + float(_solid(shaft_mod.build_part()).Volume())
    )
    if abs(volume - expected) > max(5.0, 0.02 * expected):
        raise RuntimeError(
            f"Assembly volume {volume:.3f} != sum of parts {expected:.3f}"
        )

    bb = compound.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    # Plate 100×150; KP08 height 29 on plate → Z ≈ 34
    if abs(dx - 100.0) > DIM_TOL:
        raise RuntimeError(f"BB.xlen={dx:.3f}, expected ~100")
    if abs(dy - 150.0) > DIM_TOL:
        raise RuntimeError(f"BB.ylen={dy:.3f}, expected ~150")
    if abs(dz - (PLATE_THICKNESS + 29.0)) > DIM_TOL:
        raise RuntimeError(
            f"BB.zlen={dz:.3f}, expected ~{PLATE_THICKNESS + 29.0} (plate + KP08 height)"
        )
    if abs(float(bb.zmin)) > DIM_TOL:
        raise RuntimeError(f"Assembly should sit on Z=0; zmin={bb.zmin:.3f}")

    print("MATE CHECK:")
    print(f"  plate                identity  top_z={PLATE_THICKNESS}")
    print(f"  kp08_pos / kp08_neg  Y={BLOCK_Y}  Z={PLATE_THICKNESS}")
    print(f"  shaft_8x150          Z={SHAFT_Z} (through bore centers)")
    print(
        f"ASSERT PASS: volume={volume:.3f} mm^3 (expect ~{expected:.3f}) "
        f"BB=({dx:.2f},{dy:.2f},{dz:.2f})"
    )


def export_profile_dxf(dxf_path: Path) -> None:
    """Top view: plate outline + four mounting holes (assembly footprint)."""
    import ezdxf

    plate_mod = load_part_module("plate_100x150x5")
    half_w = float(plate_mod.plate_width) / 2.0
    half_d = float(plate_mod.plate_depth) / 2.0
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
    r = float(plate_mod.bolt_hole_diameter) / 2.0
    for x, y in plate_mod._hole_points():  # noqa: SLF001
        msp.add_circle((x, y), r, dxfattribs=attrs)
    # Shaft end as centerline circle at origin (top projection of axis)
    msp.add_circle((0.0, 0.0), 4.0, dxfattribs=attrs)
    doc.saveas(str(dxf_path))


def export_artifacts(assy: cq.Assembly, compound: cq.Compound, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{PART_NAME}.step"
    stl_path = out_dir / f"{PART_NAME}.stl"
    dxf_path = out_dir / f"{PART_NAME}_profile.dxf"

    assy.save(str(step_path), exportType="STEP")
    cq.exporters.export(compound, str(stl_path))
    export_profile_dxf(dxf_path)

    for path in (step_path, stl_path, dxf_path):
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

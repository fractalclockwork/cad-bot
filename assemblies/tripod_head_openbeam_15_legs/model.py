#!/usr/bin/env python3
"""Assembly: tripod_head_openbeam_15 + 3× openbeam_15x100 (equal legs).

Mates: each beam seated on a cube-corner cradle stop (head helpers drive
azimuth, splay, stop, and axis); T-slot (±X) faces align with M3 bolt
(section-center lateral).
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from part_config import load_part_module  # noqa: E402

PART_NAME = os.environ.get("PART", "tripod_head_openbeam_15_legs")
DIM_TOL = 1.0


def _solid(wp: cq.Workplane) -> cq.Shape:
    return wp.val()


def _orient_leg(beam: cq.Shape, azimuth_deg: float, splay_deg: float) -> cq.Shape:
    """Map openbeam Y-length → cradle axis; ±X slots → bolt lateral."""
    # Y → +X (horizontal radial)
    shaped = beam.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), -90.0)
    # +splay about +Y: length along +X pitches toward −Z (matches cradle_axis_direction)
    shaped = shaped.rotate((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), splay_deg)
    if abs(azimuth_deg) > 1e-9:
        shaped = shaped.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), azimuth_deg)
    return shaped


def build_assembly() -> tuple[cq.Assembly, cq.Compound]:
    head_mod = load_part_module("tripod_head_openbeam_15")
    beam_mod = load_part_module("openbeam_15x100")

    head = _solid(head_mod.build_part())
    beam_len = float(beam_mod.beam_length)
    splay = float(head_mod.splay_deg)
    azimuths = head_mod.cradle_azimuths()

    assy = cq.Assembly(name=PART_NAME)
    assy.add(head, name="tripod_head_openbeam_15")

    for i, az in enumerate(azimuths):
        axis = head_mod.cradle_axis_direction(az)
        stop = head_mod.cradle_stop_center(az)
        cx = stop[0] + axis[0] * (beam_len / 2.0)
        cy = stop[1] + axis[1] * (beam_len / 2.0)
        cz = stop[2] + axis[2] * (beam_len / 2.0)

        leg = _orient_leg(_solid(beam_mod.build_part()), az, splay)
        assy.add(
            leg,
            name=f"openbeam_15x100_{i}",
            loc=cq.Location(cq.Vector(cx, cy, cz)),
        )

    compound = assy.toCompound()
    return assy, compound


def assert_geometry(compound: cq.Compound) -> None:
    if not compound.isValid():
        raise RuntimeError("Assembly compound isValid() is False")

    volume = float(compound.Volume())
    if volume <= 0:
        raise RuntimeError(f"Assembly volume <= 0: {volume}")

    head_mod = load_part_module("tripod_head_openbeam_15")
    beam_mod = load_part_module("openbeam_15x100")
    expected = float(_solid(head_mod.build_part()).Volume()) + 3.0 * float(
        _solid(beam_mod.build_part()).Volume()
    )
    if abs(volume - expected) > max(5.0, 0.02 * expected):
        raise RuntimeError(
            f"Assembly volume {volume:.3f} != sum of parts {expected:.3f}"
        )

    bb = compound.BoundingBox()
    dx, dy, dz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    # Three 100 mm legs splayed outward — envelope well beyond head (~50 mm)
    if dx < 80.0 or dy < 80.0:
        raise RuntimeError(f"BB XY too small for splayed legs: ({dx:.1f},{dy:.1f})")
    if dz < 40.0:
        raise RuntimeError(f"BB Z too small for pitched legs: {dz:.1f}")

    # Cube-corner: pairwise axes ~90°; each −Y beam end maps to stop
    axes = [head_mod.cradle_axis_direction(az) for az in head_mod.cradle_azimuths()]
    for i, j in ((0, 1), (1, 2), (2, 0)):
        dot = axes[i][0] * axes[j][0] + axes[i][1] * axes[j][1] + axes[i][2] * axes[j][2]
        ang = math.degrees(math.acos(max(-1.0, min(1.0, dot))))
        if abs(ang - 90.0) > 1.0:
            raise RuntimeError(f"leg axes not cube-corner 90°: {ang:.2f}")

    print("MATE CHECK:")
    beam_len = float(beam_mod.beam_length)
    for i, az in enumerate(head_mod.cradle_azimuths()):
        stop = head_mod.cradle_stop_center(az)
        axis = head_mod.cradle_axis_direction(az)
        splay = float(head_mod.splay_deg)
        # Native (0,-L/2,0) → after _orient_leg → should land on stop when centered
        sp = math.radians(splay)
        x1, y1, z1 = -beam_len / 2.0, 0.0, 0.0  # after Y→+X (−90° Z)
        x2 = x1 * math.cos(sp) + z1 * math.sin(sp)
        y2 = y1
        z2 = -x1 * math.sin(sp) + z1 * math.cos(sp)
        azr = math.radians(az)
        x3 = x2 * math.cos(azr) - y2 * math.sin(azr)
        y3 = x2 * math.sin(azr) + y2 * math.cos(azr)
        z3 = z2
        cx = stop[0] + axis[0] * (beam_len / 2.0)
        cy = stop[1] + axis[1] * (beam_len / 2.0)
        cz = stop[2] + axis[2] * (beam_len / 2.0)
        end = (x3 + cx, y3 + cy, z3 + cz)
        err = math.sqrt(
            (end[0] - stop[0]) ** 2 + (end[1] - stop[1]) ** 2 + (end[2] - stop[2]) ** 2
        )
        if err > DIM_TOL:
            raise RuntimeError(f"leg_{i} −Y end not on stop: err={err:.3f} mm")
        print(
            f"  leg_{i} az={az:.0f}° stop=({stop[0]:.1f},{stop[1]:.1f},{stop[2]:.1f}) "
            f"axis=({axis[0]:.2f},{axis[1]:.2f},{axis[2]:.2f}) end_on_stop_err={err:.4f}"
        )
    print(
        f"ASSERT PASS: volume={volume:.3f} mm^3 (expect ~{expected:.3f}) "
        f"BB=({dx:.2f},{dy:.2f},{dz:.2f})"
    )


def export_artifacts(assy: cq.Assembly, compound: cq.Compound, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{PART_NAME}.step"
    stl_path = out_dir / f"{PART_NAME}.stl"

    assy.save(str(step_path), exportType="STEP")
    cq.exporters.export(compound, str(stl_path))

    for path in (step_path, stl_path):
        if not path.exists() or path.stat().st_size <= 0:
            raise RuntimeError(f"Export failed: {path}")
    print(f"EXPORT OK: {step_path}, {stl_path}")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"/work/output/{PART_NAME}")
    assy, compound = build_assembly()
    assert_geometry(compound)
    export_artifacts(assy, compound, out)


if __name__ == "__main__":
    main()

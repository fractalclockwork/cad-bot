#!/usr/bin/env python3
"""Assembly ASSY_NAME — compose parts via load_part_module + cq.Assembly.

Mates (mm) — document in drawings/dims.md and comments below:
- part_a: identity (example)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from part_config import load_part_module  # noqa: E402

PART_NAME = os.environ.get("PART", "ASSY_NAME")
DIM_TOL = 1.0


def _solid(wp: cq.Workplane) -> cq.Shape:
    return wp.val()


def build_assembly() -> tuple[cq.Assembly, cq.Compound]:
    # Example — replace with real parts and locations:
    # mod = load_part_module("kp08")
    # solid = _solid(mod.build_part())
    # assy.add(solid, name="kp08", loc=cq.Location(cq.Vector(0, 0, 0)))
    raise NotImplementedError("Wire load_part_module + cq.Assembly mates for ASSY_NAME")


def assert_geometry(compound: cq.Compound) -> None:
    if not compound.isValid():
        raise RuntimeError("Assembly compound isValid() is False")
    volume = float(compound.Volume())
    if volume <= 0:
        raise RuntimeError(f"Assembly volume <= 0: {volume}")
    bb = compound.BoundingBox()
    print(
        f"ASSERT PASS: volume={volume:.3f} mm^3 "
        f"BB=({bb.xlen:.2f},{bb.ylen:.2f},{bb.zlen:.2f})"
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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"/work/output/{PART_NAME}")
    assy, compound = build_assembly()
    assert_geometry(compound)
    export_artifacts(assy, compound, out)
    print(f"{PART_NAME} assembly workflow complete")


if __name__ == "__main__":
    main()

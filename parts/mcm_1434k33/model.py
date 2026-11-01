#!/usr/bin/env python3
"""McMaster 1434K33 mounted roller bearing, two-bolt flange — vendor STEP import.

Source: https://www.mcmaster.com/1434K33/
Geometry: cq.importers.importStep from gitignored vendor/mcmaster/
Prefer: 1434K33_Mounted Roller Bearing with Two-Bolt Flange.STEP

Axis convention after framing:
- X: flange long axis / bolt pitch
- Y: shaft / bearing axis
- Z: up in flange plane (short flange axis); mount face framed to Z≈0 family
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cadquery as cq

PART_NAME = os.environ.get("PART", "mcm_1434k33")
MCM_PART = "1434K33"
MCM_VENDOR_STEP = "1434K33_Mounted Roller Bearing with Two-Bolt Flange.STEP"
DIM_TOL = 1.0  # mm

# Envelope from McMaster STEP after framing (mm) — catalog table TBD if published
overall_length = 45.0  # X — flange long
shaft_depth = 16.8  # Y — along shaft
flange_width = 31.8  # Z — flange short / height after frame


def _vendor_dirs() -> list[Path]:
    return [
        Path("/work/vendor/mcmaster"),
        Path(__file__).resolve().parents[2] / "vendor" / "mcmaster",
    ]


def vendor_step_path() -> Path:
    """Resolve gitignored vendor STEP — prefer McMaster original download name."""
    candidates: list[Path] = []
    for d in _vendor_dirs():
        candidates.append(d / MCM_VENDOR_STEP)
        if d.is_dir():
            candidates.extend(sorted(d.glob(f"{MCM_PART}_*.STEP")))
            candidates.extend(sorted(d.glob(f"{MCM_PART}_*.step")))
        candidates.append(d / f"{MCM_PART}.STEP")
        candidates.append(d / f"{MCM_PART}.step")

    found: Path | None = None
    seen: set[Path] = set()
    for p in candidates:
        rp = p.resolve() if p.exists() else p
        if rp in seen:
            continue
        seen.add(rp)
        if p.is_file():
            found = p
            break
    if found is None:
        raise FileNotFoundError(
            f"Missing vendor STEP (gitignored) under vendor/mcmaster/\n"
            f"Expected McMaster download name e.g. {MCM_VENDOR_STEP!r}\n"
            f"Log in, download 3-D STEP from https://www.mcmaster.com/{MCM_PART}/, "
            f"keep the original filename. See skill_7_mcmaster_to_cadquery."
        )
    head = found.read_bytes()[:64]
    if b"ISO-10303" not in head:
        raise RuntimeError(
            f"Vendor file is not a STEP (missing ISO-10303 header): {found} "
            f"({found.stat().st_size} bytes). Re-download after McMaster login."
        )
    return found


def _bb_lens(solid) -> tuple[float, float, float]:
    bb = solid.BoundingBox()
    return float(bb.xlen), float(bb.ylen), float(bb.zlen)


def _frame_to_repo_axes(wp: cq.Workplane) -> cq.Workplane:
    """Map imported BB to X≈flange length, Y≈shaft depth, Z≈flange width; Zmin→0."""
    target = (overall_length, shaft_depth, flange_width)
    best = wp
    best_err = float("inf")
    best_solid = wp.val()

    for rx in (0, 90, 180, 270):
        for ry in (0, 90, 180, 270):
            for rz in (0, 90, 180, 270):
                trial = wp
                if rx:
                    trial = trial.rotate((0, 0, 0), (1, 0, 0), rx)
                if ry:
                    trial = trial.rotate((0, 0, 0), (0, 1, 0), ry)
                if rz:
                    trial = trial.rotate((0, 0, 0), (0, 0, 1), rz)
                s = trial.val()
                lx, ly, lz = _bb_lens(s)
                err = abs(lx - target[0]) + abs(ly - target[1]) + abs(lz - target[2])
                if err < best_err:
                    best_err = err
                    best = trial
                    best_solid = s

    if best_err > 3 * DIM_TOL:
        lx, ly, lz = _bb_lens(best_solid)
        print(
            f"WARN: framing BB=({lx:.2f},{ly:.2f},{lz:.2f}) "
            f"vs target ({target[0]},{target[1]},{target[2]}) err={best_err:.2f}"
        )

    bb = best_solid.BoundingBox()
    dx = -0.5 * (bb.xmin + bb.xmax)
    dy = -0.5 * (bb.ymin + bb.ymax)
    dz = -bb.zmin
    return best.translate((dx, dy, dz))


def build_part() -> cq.Workplane:
    path = vendor_step_path()
    print(f"IMPORT STEP: {path}")
    imported = cq.importers.importStep(str(path))
    return _frame_to_repo_axes(imported)


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid():
        raise RuntimeError("imported solid isValid() == False")
    vol = float(solid.Volume())
    if vol <= 0:
        raise RuntimeError("imported solid has non-positive volume")

    bb = solid.BoundingBox()
    lx, ly, lz = float(bb.xlen), float(bb.ylen), float(bb.zlen)
    print(
        f"SPEC CHECK:\n"
        f"  overall_length  expect {overall_length:.1f}  BB.x={lx:.2f}\n"
        f"  shaft_depth     expect {shaft_depth:.1f}  BB.y={ly:.2f}\n"
        f"  flange_width    expect {flange_width:.1f}  BB.z={lz:.2f}"
    )
    if abs(lx - overall_length) > DIM_TOL:
        raise RuntimeError(f"BB.x {lx:.2f} != overall_length {overall_length} ±{DIM_TOL}")
    if abs(ly - shaft_depth) > DIM_TOL:
        raise RuntimeError(f"BB.y {ly:.2f} != shaft_depth {shaft_depth} ±{DIM_TOL}")
    if abs(lz - flange_width) > DIM_TOL:
        raise RuntimeError(f"BB.z {lz:.2f} != flange_width {flange_width} ±{DIM_TOL}")
    if abs(float(bb.zmin)) > DIM_TOL:
        raise RuntimeError(f"base not near Z=0 (zmin={bb.zmin:.2f})")

    print(
        f"ASSERT PASS: valid=True volume={vol:.3f} mm^3 "
        f"BB=({lx:.2f},{ly:.2f},{lz:.2f}) framed"
    )


def export_artifacts(shape: cq.Workplane, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step = out_dir / f"{PART_NAME}.step"
    stl = out_dir / f"{PART_NAME}.stl"
    cq.exporters.export(shape, str(step))
    cq.exporters.export(shape, str(stl))
    print(f"EXPORT OK: {step} ({step.stat().st_size} bytes)")
    print(f"EXPORT OK: {stl} ({stl.stat().st_size} bytes)")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"/work/output/{PART_NAME}")
    shape = build_part()
    assert_geometry(shape)
    export_artifacts(shape, out)
    print(f"{PART_NAME} CadQuery workflow complete")


if __name__ == "__main__":
    main()

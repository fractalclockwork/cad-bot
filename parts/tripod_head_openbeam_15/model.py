#!/usr/bin/env python3
"""Cube-corner tripod head for three OpenBeam 15×15 legs (U-cradle + slot-aligned M3).

Coordinate convention:
- Hub on +Z; finished part seated on Z=0 (print: mount pad on bed, cradles up)
- Three mutually orthogonal U-cradle axes (cube corner): 120° in top view,
  pairwise 90°, splay = asin(1/√3) down from horizontal (fixed by orthogonality)
- U open toward −Z local (after splay ≈ downward) so legs drop in from below
- Convex hull(core_proxy, stop_back_proxy) fuses each U to the core — proxies do
  NOT include the U pocket (channel + bolt cut after hull on a single +X arm,
  then copied by rotation for identical sockets)
- Flat mount pad on +Z; M3 through cradle section / T-slot center
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh
from OCP.BRep import BRep_Tool
from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_MakeSolid,
    BRepBuilderAPI_Sewing,
)
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_FACE, TopAbs_IN, TopAbs_ON, TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location

PART_NAME = os.environ.get("PART", "tripod_head_openbeam_15")
DIM_TOL = 0.5

# Spec params (mm / deg) — locked in drawings/dims.md
beam_nominal = 15.0
print_clearance = 0.2
cradle_opening = beam_nominal + 2.0 * print_clearance  # 15.4
wall = 3.0
body_size = cradle_opening + 2.0 * wall  # 21.4
cradle_length = 16.0
bolt_from_stop = 7.5
bolt_hole_diameter = 3.4
bolt_nominal = 3.0
arm_length = cradle_length + wall
splay_deg = math.degrees(math.asin(1.0 / math.sqrt(3.0)))
hub_radius = 22.0
core_radius = 17.0
core_height = 30.0
mount_pad_radius = 22.0
mount_pad_height = 6.0
hull_anchor_radius = 8.0
num_cradles = 3


def _box_at(x0: float, y0: float, z0: float, dx: float, dy: float, dz: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .transformed(offset=(x0 + dx / 2.0, y0 + dy / 2.0, z0 + dz / 2.0))
        .box(dx, dy, dz)
    )


def _section_center_z_local() -> float:
    return cradle_opening / 2.0


def _cradle_pivot_z() -> float:
    return core_height / 2.0


def _mesh_points(shape: cq.Shape, lin: float = 0.5) -> np.ndarray:
    BRepMesh_IncrementalMesh(shape.wrapped, lin).Perform()
    pts: list[list[float]] = []
    exp = TopExp_Explorer(shape.wrapped, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None:
            trsf = loc.Transformation()
            for i in range(1, tri.NbNodes() + 1):
                p = tri.Node(i).Transformed(trsf)
                pts.append([p.X(), p.Y(), p.Z()])
        exp.Next()
    bb = shape.BoundingBox()
    for x in (bb.xmin, bb.xmax):
        for y in (bb.ymin, bb.ymax):
            for z in (bb.zmin, bb.zmax):
                pts.append([x, y, z])
    return np.asarray(pts, dtype=float)


def convex_hull_shapes(*shapes: cq.Shape, lin: float = 0.5) -> cq.Shape:
    """OpenSCAD-style 3D convex hull of CadQuery shapes (trimesh + OCP sew)."""
    if not shapes:
        raise ValueError("convex_hull_shapes requires at least one shape")
    pts = np.vstack([_mesh_points(s, lin=lin) for s in shapes])
    hull_mesh = trimesh.Trimesh(vertices=pts, process=False).convex_hull
    sewing = BRepBuilderAPI_Sewing(1.0e-3)
    for i, j, k in hull_mesh.faces:
        poly = BRepBuilderAPI_MakePolygon()
        for idx in (i, j, k):
            x, y, z = map(float, hull_mesh.vertices[idx])
            poly.Add(gp_Pnt(x, y, z))
        poly.Close()
        face = BRepBuilderAPI_MakeFace(poly.Wire(), True)
        if face.IsDone():
            sewing.Add(face.Face())
    sewing.Perform()
    mk = BRepBuilderAPI_MakeSolid()
    exp = TopExp_Explorer(sewing.SewedShape(), TopAbs_SHELL)
    n_shells = 0
    while exp.More():
        mk.Add(TopoDS.Shell_s(exp.Current()))
        n_shells += 1
        exp.Next()
    if n_shells == 0:
        raise RuntimeError("convex hull sewing produced no shells")
    solid = cq.Shape.cast(mk.Solid())
    if not solid.isValid() or float(solid.Volume()) <= 0:
        raise RuntimeError("convex hull solid invalid or empty")
    return solid


def _u_cradle_local() -> cq.Workplane:
    """U-cradle: stop at x=0, mouth +X, floor on +Z, open −Z. No bolt yet."""
    w, o, cl = wall, cradle_opening, cradle_length
    half = body_size / 2.0
    floor = _box_at(0.0, -half, o, cl, body_size, w)
    left = _box_at(0.0, -half, 0.0, cl, w, w + o)
    right = _box_at(0.0, half - w, 0.0, cl, w, w + o)
    stop = _box_at(-w, -half, 0.0, w, body_size, w + o)
    return floor.union(left).union(right).union(stop)


def _xform_from_plus_x(shape: cq.Workplane, azimuth_deg: float = 0.0) -> cq.Shape:
    """Pitch about stop on +X, then optional spin about Z."""
    z_ax = _cradle_pivot_z()
    placed = shape.rotate(
        (hub_radius, 0.0, z_ax),
        (hub_radius, 1.0, z_ax),
        splay_deg,
    )
    if abs(azimuth_deg) > 1e-9:
        placed = placed.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), azimuth_deg)
    return placed.val()


def _place_cradle_plus_x() -> cq.Shape:
    local = _u_cradle_local()
    cz = _section_center_z_local()
    z_ax = _cradle_pivot_z()
    placed = local.translate((hub_radius, 0.0, z_ax - cz))
    return _xform_from_plus_x(placed, 0.0)


def _stop_back_proxy_plus_x() -> cq.Shape:
    """Thin slab at the stop only — does NOT fill the U pocket.

    Hull target is the seating face / stop wall so the convex join stops at the
    cradle root instead of swallowing the channel.
    """
    w, o = wall, cradle_opening
    half = body_size / 2.0
    # Stop wall + 2 mm into the cradle floor/walls root (not the open pocket length)
    depth = w + 2.0
    box = _box_at(-w, -half, 0.0, depth, body_size, w + o)
    cz = _section_center_z_local()
    z_ax = _cradle_pivot_z()
    placed = box.translate((hub_radius, 0.0, z_ax - cz))
    return _xform_from_plus_x(placed, 0.0)


def _core_proxy_plus_x() -> cq.Shape:
    """Sphere on the +X core surface (arm built at az=0, then copied by rotation)."""
    z_ax = _cradle_pivot_z()
    r_c = max(1.0, core_radius - hull_anchor_radius * 0.35)
    return (
        cq.Workplane("XY")
        .transformed(offset=(r_c, 0.0, z_ax))
        .sphere(hull_anchor_radius)
        .val()
    )


def _channel_cut_plus_x() -> cq.Shape:
    """Square prism clearing the U pocket (opening × opening) from stop outward."""
    z_ax = _cradle_pivot_z()
    into = 0.5
    out = cradle_length + 2.0
    length = into + out
    mid_x = hub_radius + (out - into) / 2.0
    o = cradle_opening
    # Slightly proud of opening so hull leftovers cannot pinch the beam
    cut_o = o + 0.2
    box = cq.Workplane("XY").transformed(offset=(mid_x, 0.0, z_ax)).box(length, cut_o, cut_o)
    return _xform_from_plus_x(box, 0.0)


def _bolt_cut_plus_x() -> cq.Shape:
    """M3 clearance cylinder through cradle walls at bolt_from_stop / section center.

    Must use world XYZ placement — XZ-workplane local offsets map Y/Z differently and
    previously parked the cutter off the arm (0 volume removed).
    """
    z_ax = _cradle_pivot_z()
    r = bolt_hole_diameter / 2.0
    span = body_size + 6.0
    # Cylinder along +Y through (hub + bolt_from_stop, 0, z_ax), then pitch with cradle
    cyl = (
        cq.Workplane("XY")
        .transformed(
            offset=(hub_radius + bolt_from_stop, 0.0, z_ax),
            rotate=(90, 0, 0),
        )
        .circle(r)
        .extrude(span / 2.0, both=True)
    )
    return _xform_from_plus_x(cyl, 0.0)


def _arm_plus_x() -> cq.Shape:
    """One complete arm on +X: hull + U, then channel and bolt cuts (identical copies)."""
    hull = convex_hull_shapes(_core_proxy_plus_x(), _stop_back_proxy_plus_x())
    arm = cq.Workplane("XY").newObject([hull]).union(_place_cradle_plus_x())
    arm = arm.cut(_channel_cut_plus_x())
    arm = arm.cut(_bolt_cut_plus_x())
    return arm.val()


def _build_raw() -> cq.Workplane:
    core = cq.Workplane("XY").circle(core_radius).extrude(core_height)
    pad = (
        cq.Workplane("XY")
        .workplane(offset=core_height)
        .circle(mount_pad_radius)
        .extrude(mount_pad_height)
    )
    body = core.union(pad)

    arm0 = _arm_plus_x()
    body = body.union(arm0)
    for k in range(1, num_cradles):
        az = 360.0 * k / num_cradles
        spun = arm0.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), az)
        body = body.union(spun)

    solid = body.val()
    try:
        solids = solid.Solids()
        if len(solids) > 1:
            solids = sorted(solids, key=lambda s: float(s.Volume()), reverse=True)
            body = cq.Workplane("XY").newObject([solids[0]])
    except Exception:
        pass
    return body


def build_part() -> cq.Workplane:
    body = _build_raw()
    zmin = float(body.val().BoundingBox().zmin)
    if abs(zmin) > 1e-6:
        body = body.translate((0.0, 0.0, -zmin))
    return body


def cradle_axis_direction(azimuth_deg: float) -> tuple[float, float, float]:
    az = math.radians(azimuth_deg)
    sp = math.radians(splay_deg)
    hx, hy = math.cos(az), math.sin(az)
    return (hx * math.cos(sp), hy * math.cos(sp), -math.sin(sp))


def seat_z_offset() -> float:
    return -float(_build_raw().val().BoundingBox().zmin)


def cradle_stop_center(azimuth_deg: float) -> tuple[float, float, float]:
    az = math.radians(azimuth_deg)
    z_ax = _cradle_pivot_z() + seat_z_offset()
    return (
        hub_radius * math.cos(az),
        hub_radius * math.sin(az),
        z_ax,
    )


def cradle_azimuths() -> tuple[float, ...]:
    return tuple(360.0 * k / num_cradles for k in range(num_cradles))


def _point_in_solid(solid: cq.Shape, x: float, y: float, z: float) -> bool:
    clf = BRepClass3d_SolidClassifier(solid.wrapped)
    clf.Perform(gp_Pnt(x, y, z), 1.0e-6)
    return clf.State() in (TopAbs_IN, TopAbs_ON)


def assert_geometry(shape: cq.Workplane) -> None:
    solid = shape.val()
    if not solid.isValid() or float(solid.Volume()) <= 0:
        raise RuntimeError("invalid or empty solid")

    try:
        n_solids = len(solid.Solids())
    except Exception:
        n_solids = 1
    if n_solids != 1:
        raise RuntimeError(f"expected one solid for FDM, got {n_solids}")

    bb = solid.BoundingBox()
    if abs(bb.zmin) > DIM_TOL:
        raise RuntimeError(f"expected base near Z=0, zmin={bb.zmin:.2f}")
    if bb.zlen < core_height + mount_pad_height - DIM_TOL:
        raise RuntimeError(f"BB Z too small: {bb.zlen:.2f}")

    if abs(cradle_opening - (beam_nominal + 2.0 * print_clearance)) > 1e-9:
        raise RuntimeError("cradle_opening must equal beam_nominal + 2*print_clearance")
    if abs(bolt_from_stop - 7.5) > 1e-9:
        raise RuntimeError("bolt_from_stop locked at 7.5 mm")
    cube_splay = math.degrees(math.asin(1.0 / math.sqrt(3.0)))
    if abs(splay_deg - cube_splay) > 1e-6:
        raise RuntimeError(f"splay_deg must be cube-corner asin(1/√3)={cube_splay}")
    if num_cradles != 3:
        raise RuntimeError("num_cradles locked at 3")

    d0 = cradle_axis_direction(0.0)
    d1 = cradle_axis_direction(120.0)
    d2 = cradle_axis_direction(240.0)
    for d in (d0, d1, d2):
        n = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
        if abs(n - 1.0) > 1e-6:
            raise RuntimeError(f"cradle axis not unit: {d}")
        if d[2] >= 0:
            raise RuntimeError("cradle axis should pitch downward (dz < 0)")

    def _dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    for a, b in ((d0, d1), (d1, d2), (d2, d0)):
        ang = math.degrees(math.acos(max(-1.0, min(1.0, _dot(a, b)))))
        if abs(ang - 90.0) > 1.0:
            raise RuntimeError(f"cube-corner axes must be pairwise 90°, got {ang:.2f}")

    def h_ang(d: tuple[float, float, float]) -> float:
        return math.degrees(math.atan2(d[1], d[0])) % 360.0

    a0, a1, a2 = h_ang(d0), h_ang(d1), h_ang(d2)
    gaps = sorted([(a1 - a0) % 360.0, (a2 - a1) % 360.0, (a0 - a2) % 360.0])
    for g in gaps:
        if abs(g - 120.0) > 1.0:
            raise RuntimeError(f"top-view azimuth gaps not 120°: {gaps}")

    # Hull continuity (mid radial still solid) + pocket empty + bolt void
    seat = seat_z_offset()
    z_ax = _cradle_pivot_z() + seat
    for az_deg in cradle_azimuths():
        az = math.radians(az_deg)
        axis = cradle_axis_direction(az_deg)
        stop = cradle_stop_center(az_deg)

        r_mid = 0.5 * (core_radius + hub_radius)
        if not _point_in_solid(solid, r_mid * math.cos(az), r_mid * math.sin(az), z_ax):
            raise RuntimeError(f"hull gap at az={az_deg:.0f}°")

        # Pocket must be empty at stop + 4 mm along axis (beam seating volume)
        px = stop[0] + axis[0] * 4.0
        py = stop[1] + axis[1] * 4.0
        pz = stop[2] + axis[2] * 4.0
        if _point_in_solid(solid, px, py, pz):
            raise RuntimeError(
                f"U-pocket blocked at az={az_deg:.0f}° (leg would not fit)"
            )

        # Bolt must pierce both walls (not just the empty pocket center).
        # Wall midpoints: ±(body_size/2 - wall/2) along local Y before pitch;
        # after +X pitch about Y that offset stays world-perpendicular to the axis.
        bx = stop[0] + axis[0] * bolt_from_stop
        by = stop[1] + axis[1] * bolt_from_stop
        bz = stop[2] + axis[2] * bolt_from_stop
        # Horizontal perpendicular to cradle azimuth (local +Y spun by az)
        az = math.radians(az_deg)
        px_hat = -math.sin(az)
        py_hat = math.cos(az)
        wall_mid = body_size / 2.0 - wall / 2.0
        for side, sign in (("L", -1.0), ("R", 1.0)):
            wx = bx + sign * wall_mid * px_hat
            wy = by + sign * wall_mid * py_hat
            wz = bz
            if _point_in_solid(solid, wx, wy, wz):
                raise RuntimeError(
                    f"bolt hole missing through {side} wall at az={az_deg:.0f}°"
                )
            # Material should remain beside the hole (sanity: wall not deleted)
            ring = bolt_hole_diameter / 2.0 + 1.2
            # Offset along cradle axis from the wall hole center
            mx = wx + axis[0] * ring
            my = wy + axis[1] * ring
            mz = wz + axis[2] * ring
            if not _point_in_solid(solid, mx, my, mz):
                raise RuntimeError(
                    f"cradle wall missing beside bolt at az={az_deg:.0f}° ({side})"
                )

    vol = float(solid.Volume())
    if vol < 2000:
        raise RuntimeError(f"volume unexpectedly small: {vol:.1f}")

    print(
        f"ASSERT PASS BB=({bb.xlen:.2f},{bb.ylen:.2f},{bb.zlen:.2f}) "
        f"vol={vol:.1f} solids={n_solids} cradles={num_cradles}@120deg_top "
        f"splay={splay_deg:.4f} pairwise=90 identical_arms hull=stop_proxy "
        f"bolt_from_stop={bolt_from_stop}"
    )
    print(
        f"DIM CHECK opening={cradle_opening} hole_d={bolt_hole_diameter} "
        f"(M{bolt_nominal:.0f}) hub_r={hub_radius} core_r={core_radius} "
        f"mount_pad_r={mount_pad_radius}"
    )


def export_artifacts(shape: cq.Workplane, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    step = out_dir / f"{PART_NAME}.step"
    stl = out_dir / f"{PART_NAME}.stl"
    cq.exporters.export(shape, str(step))
    cq.exporters.export(shape, str(stl))
    print(f"EXPORT OK: {step}, {stl}")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"/work/output/{PART_NAME}")
    shape = build_part()
    assert_geometry(shape)
    export_artifacts(shape, out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Resolve PART env → part or assembly paths and artifact names."""
from __future__ import annotations

import importlib.util
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


@dataclass(frozen=True)
class PartPaths:
    name: str
    kind: str  # "part" | "assembly"
    root: Path
    model: Path
    views: Path
    drawings: Path
    output: Path
    previews: Path

    @property
    def step(self) -> Path:
        return self.output / f"{self.name}.step"

    @property
    def stl(self) -> Path:
        return self.output / f"{self.name}.stl"

    @property
    def profile_dxf(self) -> Path:
        return self.output / f"{self.name}_profile.dxf"

    @property
    def profile_svg(self) -> Path:
        return self.previews / f"{self.name}_profile.svg"

    @property
    def review_json(self) -> Path:
        return self.previews / "human_review.json"


def part_name() -> str:
    name = os.environ.get("PART", "kp08").strip()
    if not name or "/" in name or name.startswith("."):
        raise SystemExit(f"Invalid PART={name!r}")
    return name


def work_root() -> Path:
    """Container work root, or repo root when run on the host."""
    if Path("/work/parts").is_dir():
        return Path("/work")
    return Path(__file__).resolve().parent.parent


def resolve(name: str | None = None) -> PartPaths:
    n = name or part_name()
    root = work_root()
    output = root / "output" / n

    part_root = root / "parts" / n
    assy_root = root / "assemblies" / n
    if part_root.is_dir():
        kind = "part"
        target = part_root
    elif assy_root.is_dir():
        kind = "assembly"
        target = assy_root
    else:
        # Prefer parts/ in the returned paths for clearer errors
        kind = "part"
        target = part_root

    return PartPaths(
        name=n,
        kind=kind,
        root=target,
        model=target / "model.py",
        views=target / "views.py",
        drawings=target / "drawings",
        output=output,
        previews=output / "previews",
    )


def load_views(paths: PartPaths | None = None) -> ModuleType:
    p = paths or resolve()
    if not p.views.is_file():
        raise SystemExit(f"Missing views module: {p.views}")
    spec = importlib.util.spec_from_file_location(f"part_views_{p.name}", p.views)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load views: {p.views}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if not hasattr(mod, "VIEWS"):
        raise SystemExit(f"{p.views} must define VIEWS")
    return mod


def ensure_part_layout(paths: PartPaths | None = None) -> PartPaths:
    p = paths or resolve()
    if not p.root.is_dir():
        raise SystemExit(
            f"PART={p.name} not found under parts/ or assemblies/\n"
            f"Scaffold a part with: ./scripts/new_part.sh {p.name}"
        )
    if not p.model.is_file():
        raise SystemExit(f"Missing model: {p.model}")
    return p


def load_part_module(part_name_str: str) -> ModuleType:
    """Load parts/<name>/model.py for assembly composition."""
    path = work_root() / "parts" / part_name_str / "model.py"
    if not path.is_file():
        raise SystemExit(f"Missing part model: {path}")
    spec = importlib.util.spec_from_file_location(f"part_model_{part_name_str}", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load part model: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if not hasattr(mod, "build_part"):
        raise SystemExit(f"{path} must define build_part()")
    return mod

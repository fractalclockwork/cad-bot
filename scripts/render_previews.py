#!/usr/bin/env python3
"""Headless preview renders for part/assembly artifacts (STL + DXF → PNG/SVG + gallery)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import trimesh  # noqa: E402
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg  # noqa: E402
from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration  # noqa: E402
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import ensure_part_layout, load_views, resolve  # noqa: E402

IMG_SIZE = 10.0
DPI = 102

DRAW_CONFIG = Configuration(
    background_policy=BackgroundPolicy.WHITE,
    color_policy=ColorPolicy.BLACK,
)

CAMERA = {
    "iso": (25.0, 45.0),
    "front": (0.0, -90.0),
    "top": (90.0, -90.0),
    "right": (0.0, 0.0),
}


def fail(msg: str) -> None:
    print(f"RENDER FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _set_axes_equal(ax, vertices: np.ndarray) -> None:
    mins = vertices.min(axis=0)
    maxs = vertices.max(axis=0)
    centers = (mins + maxs) / 2.0
    span = float(np.max(maxs - mins))
    if span <= 0:
        span = 1.0
    half = span * 0.55
    ax.set_xlim(centers[0] - half, centers[0] + half)
    ax.set_ylim(centers[1] - half, centers[1] + half)
    ax.set_zlim(centers[2] - half, centers[2] + half)


def _plot_mesh(ax, mesh: trimesh.Trimesh, elev: float, azim: float, title: str) -> None:
    faces = mesh.vertices[mesh.faces]
    coll = Poly3DCollection(
        faces,
        alpha=0.92,
        facecolor=(0.72, 0.78, 0.86),
        edgecolor=(0.25, 0.28, 0.32),
        linewidths=0.15,
    )
    ax.add_collection3d(coll)
    _set_axes_equal(ax, mesh.vertices)
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_facecolor("white")


def _load_mesh(stl_path: Path) -> trimesh.Trimesh:
    loaded = trimesh.load(stl_path, force="mesh")
    if isinstance(loaded, trimesh.Scene):
        geoms = [g for g in loaded.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not geoms:
            fail(f"STL scene has no meshes: {stl_path}")
        loaded = trimesh.util.concatenate(geoms)
    if not isinstance(loaded, trimesh.Trimesh):
        fail(f"Could not load triangle mesh from {stl_path}")
    if loaded.is_empty or len(loaded.faces) == 0:
        fail(f"STL has no faces: {stl_path}")
    return loaded


def render_stl_views(stl_path: Path, preview_dir: Path, views) -> list[Path]:
    if not stl_path.is_file() or stl_path.stat().st_size <= 0:
        fail(f"STL missing or empty: {stl_path}")

    mesh = _load_mesh(stl_path)
    written: list[Path] = []
    for view in views:
        if view.kind != "stl3d":
            continue
        if view.key not in CAMERA:
            fail(f"No camera for view key '{view.key}'")
        elev, azim = CAMERA[view.key]
        fig = plt.figure(figsize=(IMG_SIZE, IMG_SIZE), dpi=DPI)
        ax = fig.add_subplot(111, projection="3d")
        _plot_mesh(ax, mesh, elev, azim, view.title)
        fig.patch.set_facecolor("white")
        out = preview_dir / view.filename
        fig.savefig(out, dpi=DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        if not out.is_file() or out.stat().st_size <= 0:
            fail(f"Failed to write preview: {out}")
        print(f"RENDER OK: {out} ({out.stat().st_size} bytes)")
        written.append(out)
    return written


def render_dxf(dxf_path: Path, preview_dir: Path, part_name: str, views) -> list[Path]:
    if not dxf_path.is_file() or dxf_path.stat().st_size <= 0:
        fail(f"DXF missing or empty: {dxf_path}")

    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    ctx = RenderContext(doc)
    written: list[Path] = []

    dxf_views = [v for v in views if v.kind == "dxf2d"]
    if not dxf_views:
        png_name = "profile.png"
        title = f"{part_name} profile (DXF)"
    else:
        png_name = dxf_views[0].filename
        title = dxf_views[0].title

    png_path = preview_dir / png_name
    fig = plt.figure(figsize=(IMG_SIZE, IMG_SIZE), dpi=DPI)
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    backend = MatplotlibBackend(ax)
    Frontend(ctx, backend, config=DRAW_CONFIG).draw_layout(msp, finalize=True)
    ax.set_aspect("equal")
    ax.autoscale(enable=True)
    ax.set_title(title)
    ax.set_facecolor("white")
    ax.grid(True, alpha=0.25)
    fig.patch.set_facecolor("white")
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    if not png_path.is_file() or png_path.stat().st_size <= 0:
        fail(f"Failed to write DXF PNG: {png_path}")
    print(f"RENDER OK: {png_path} ({png_path.stat().st_size} bytes)")
    written.append(png_path)

    svg_path = preview_dir / f"{part_name}_profile.svg"
    backend_svg = svg.SVGBackend()
    Frontend(ctx, backend_svg, config=DRAW_CONFIG).draw_layout(msp, finalize=True)
    page = layout.Page(297, 210, layout.Units.mm, margins=layout.Margins.all(10))
    svg_string = backend_svg.get_string(page, settings=layout.Settings(fit_page=True))
    svg_string = svg_string.replace("stroke: #ffffff", "stroke: #000000")
    svg_string = svg_string.replace('fill="#212830"', 'fill="#ffffff"')
    svg_path.write_text(svg_string, encoding="utf-8")
    if not svg_path.is_file() or svg_path.stat().st_size <= 0:
        fail(f"Failed to write DXF SVG: {svg_path}")
    print(f"RENDER OK: {svg_path} ({svg_path.stat().st_size} bytes)")
    written.append(svg_path)

    return written


def stage_model_stl(stl_path: Path, preview_dir: Path) -> Path:
    dest = preview_dir / "model.stl"
    shutil.copy2(stl_path, dest)
    print(f"MODEL STL OK: {dest} ({dest.stat().st_size} bytes)")
    return dest


def write_gallery(preview_dir: Path, part_name: str, views) -> Path:
    cards = []
    for view in views:
        if view.kind != "stl3d":
            continue
        criteria = "".join(f"<li>{c}</li>" for c in view.criteria)
        cards.append(
            f"""<figure id="{view.key}">
  <img src="{view.filename}" alt="{view.title}" loading="lazy"/>
  <figcaption>
    <strong>{view.title}</strong> (<code>{view.filename}</code>)
    <ul>{criteria}</ul>
  </figcaption>
</figure>"""
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>cad-bot {part_name} previews — human review</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ font-family: ui-sans-serif, system-ui, sans-serif; margin: 1.5rem; background: #f4f5f7; color: #1a1a1a; }}
    h1 {{ font-size: 1.4rem; margin-bottom: 0.25rem; }}
    p {{ color: #555; margin-top: 0; }}
    #viewer-wrap {{
      background: #fff; border: 1px solid #ddd; border-radius: 8px;
      margin: 0 0 1.25rem; overflow: hidden;
    }}
    #viewer-wrap header {{
      padding: 0.6rem 0.85rem; border-bottom: 1px solid #eee; font-size: 0.9rem;
    }}
    #viewer {{ width: 100%; height: 420px; display: block; background: #e8eaed; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }}
    figure {{ margin: 0; background: #fff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
    img {{ display: block; width: 100%; height: auto; background: #fff; }}
    figcaption {{ padding: 0.75rem; font-size: 0.85rem; border-top: 1px solid #eee; }}
    figcaption ul {{ margin: 0.4rem 0 0; padding-left: 1.1rem; }}
    code {{ font-size: 0.8em; }}
  </style>
</head>
<body>
  <h1>{part_name} preview gallery</h1>
  <p>Drag to orbit, scroll to zoom. Orthographic views below are used for human sign-off
     (<code>PART={part_name} ./scripts/human_verify.sh</code>).</p>
  <section id="viewer-wrap">
    <header><strong>Interactive 3D</strong> — <code>model.stl</code></header>
    <canvas id="viewer"></canvas>
  </section>
  <div class="grid">
    {"".join(cards)}
  </div>
  <script type="importmap">
  {{
    "imports": {{
      "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
      "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
    }}
  }}
  </script>
  <script type="module">
  import * as THREE from "three";
  import {{ OrbitControls }} from "three/addons/controls/OrbitControls.js";
  import {{ STLLoader }} from "three/addons/loaders/STLLoader.js";

  const canvas = document.getElementById("viewer");
  const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true }});
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.setClearColor(0xe8eaed);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 5000);
  camera.position.set(120, 100, 140);

  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;

  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 0.85);
  key.position.set(80, 120, 60);
  scene.add(key);

  function fit(object) {{
    const box = new THREE.Box3().setFromObject(object);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z) || 1;
    const dist = maxDim * 1.8;
    controls.target.copy(center);
    camera.position.set(center.x + dist * 0.7, center.y + dist * 0.55, center.z + dist * 0.85);
    camera.near = maxDim / 100;
    camera.far = maxDim * 100;
    camera.updateProjectionMatrix();
    controls.update();
  }}

  function resize() {{
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / Math.max(h, 1);
    camera.updateProjectionMatrix();
  }}
  window.addEventListener("resize", resize);
  resize();

  new STLLoader().load(
    "model.stl",
    (geometry) => {{
      geometry.computeVertexNormals();
      const material = new THREE.MeshStandardMaterial({{
        color: 0xb8c4d4,
        metalness: 0.15,
        roughness: 0.55,
      }});
      const mesh = new THREE.Mesh(geometry, material);
      // STL is often Z-up already (our CAD frame); Three default is Y-up — map Z-up → Three
      mesh.rotation.x = -Math.PI / 2;
      scene.add(mesh);
      fit(mesh);
    }},
    undefined,
    (err) => {{
      console.error(err);
      canvas.replaceWith(Object.assign(document.createElement("p"), {{
        textContent: "Failed to load model.stl (serve via open_gallery.sh over http).",
        style: "padding:1rem;color:#a00;",
      }}));
    }}
  );

  (function animate() {{
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }})();
  </script>
</body>
</html>
"""
    index = preview_dir / "index.html"
    index.write_text(html, encoding="utf-8")
    print(f"GALLERY OK: {index}")
    return index


def main() -> None:
    paths = ensure_part_layout(resolve())
    views_mod = load_views(paths)
    views = views_mod.VIEWS
    preview_dir = paths.previews
    preview_dir.mkdir(parents=True, exist_ok=True)

    render_stl_views(paths.stl, preview_dir, views)
    stage_model_stl(paths.stl, preview_dir)
    # DXF profile renders are not part of the default verification path.
    write_gallery(preview_dir, paths.name, views)
    print("RENDER PREVIEWS PASS")


if __name__ == "__main__":
    main()

# Unified part and assembly gallery

## Problem and proposed approach

The current gallery is generated inside one model's `output/<name>/previews/` directory, and `open_gallery.sh` starts a static server rooted at that directory. Users must therefore restart or reconfigure the server to inspect another model. Replace this with one local gallery UI served from a shared endpoint. The UI will discover available parts and assemblies, load their existing generated previews, and expose assembly components as individually selectable models. Selecting an assembly component will show that component by itself by default.

Keep the existing per-model PNG previews, captions, model artifacts, and human sign-off flow. Do not have the gallery build CAD geometry on demand; if previews are absent, show a clear unavailable state and indicate that the pipeline must generate them.

## Todos

1. Implement a shared gallery server and model inventory endpoint that can serve previews from all part and assembly output directories without restarting when the selection changes.
2. Extend assembly preview artifacts with individually selectable, named component-instance meshes, retaining each instance's assembly transform.
3. Implement a unified UI with grouped part/assembly selection, assembly component selection, standalone component preview, and the selected model's existing orthographic images and review criteria.
4. Document how to start and use the unified gallery, and validate model switching, component selection, absent previews, and unchanged human-review behavior.

## Notes and considerations

- Preserve `PART=<name>` as an optional initial selection for `open_gallery.sh`; the UI's selection changes should not launch another server.
- Component entries should identify assembly occurrences, not only part definitions, so repeated components (for example, two KP08 blocks) can be selected independently.
- Prefer reusing the assembly's existing named geometry and placements when creating component meshes; avoid duplicating mate definitions in gallery code.
- The main implementation surfaces are `scripts/open_gallery.sh`, `scripts/render_previews.py`, assembly model/export code, a gallery-serving/UI component, and `README.md` plus `docs/getting-started.md`.
- Keep generated files under `output/`; don't add dependencies or commit generated CAD artifacts.

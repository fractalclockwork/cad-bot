# Agent guide

## Skills

| Skill | When |
| --- | --- |
| [`skill_1_environment_preflight`](skills/skill_1_environment_preflight/SKILL.md) | Before geometry |
| [`skill_2_cadquery_workflow`](skills/skill_2_cadquery_workflow/SKILL.md) | Build/export a part (KP08 exemplar) |
| [`skill_3_render_preview`](skills/skill_3_render_preview/SKILL.md) | Headless PNG/SVG |
| [`skill_4_human_verify`](skills/skill_4_human_verify/SKILL.md) | Staged y/n per view |
| [`skill_5_drawing_to_cadquery`](skills/skill_5_drawing_to_cadquery/SKILL.md) | New part from dimensioned images |

## PART convention

```bash
export PART=kp08   # default
PART=my_part ./scripts/run_pipeline.sh --skip-human
```

| Resolve | Path |
| --- | --- |
| Model | `parts/$PART/model.py` |
| Views | `parts/$PART/views.py` |
| Drawings | `parts/$PART/drawings/` |
| Output | `output/$PART/` |

`scripts/part_config.py` is the shared resolver. Do not hardcode part names in shared scripts.

## Rules

- Never install CadQuery on the host
- Prefer `PART=… ./scripts/open_gallery.sh` over `file://` for previews
- Archive human reviews under `docs/reviews/`
- Assemblies: see `assemblies/README.md` (compose `parts/*` solids)

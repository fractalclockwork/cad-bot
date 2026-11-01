# Agent guide

## Skills

| Skill | When |
| --- | --- |
| [`skill_1_environment_preflight`](skills/skill_1_environment_preflight/SKILL.md) | Before geometry |
| [`skill_2_cadquery_workflow`](skills/skill_2_cadquery_workflow/SKILL.md) | Build/export a part |
| [`skill_3_render_preview`](skills/skill_3_render_preview/SKILL.md) | STL PNGs + gallery 3D |
| [`skill_4_human_verify`](skills/skill_4_human_verify/SKILL.md) | Staged y/n per view |
| [`skill_5_drawing_to_cadquery`](skills/skill_5_drawing_to_cadquery/SKILL.md) | New part from drawing/spec |
| [`skill_6_assembly_workflow`](skills/skill_6_assembly_workflow/SKILL.md) | Compose parts into an assembly |
| [`skill_7_mcmaster_to_cadquery`](skills/skill_7_mcmaster_to_cadquery/SKILL.md) | McMaster URL → importStep (gitignored vendor STEP) |
| [`skill_8_language_to_cadquery`](skills/skill_8_language_to_cadquery/SKILL.md) | New printable part from natural language |

Checklists: [`CONTRIBUTING.md`](CONTRIBUTING.md).

## PART convention

```bash
export PART=kp08
PART=my_part ./scripts/run_pipeline.sh --skip-human
PART=plate_kp08_shaft ./scripts/run_pipeline.sh --skip-human
PART=plate_mcm_1434k33_shaft ./scripts/run_pipeline.sh --skip-human
```

| Resolve | Path |
| --- | --- |
| Part | `parts/$PART/model.py` |
| Assembly | `assemblies/$PART/model.py` (if not under `parts/`) |
| Views | `$root/views.py` |
| Output | `output/$PART/` |

`scripts/part_config.py` resolves `parts/` first, then `assemblies/`.

## Rules

- Never install CadQuery on the host
- Prefer `PART=… ./scripts/open_gallery.sh` over `file://`
- Required artifacts: STEP + STL (DXF not a gate)
- Archive human reviews under `docs/reviews/`
- Assemblies: `load_part_module` + explicit mates — see skill_6
- Assemblies: classify pillow vs flange (measure bore vs mount axes) **before** mates; if intent conflicts with geometry, **stop and ask** human A/B with only valid options + plate cutouts (skill_6 human conflict resolution)
- Language → part: resolve ambiguity and print/assembly conflicts **before** CadQuery; do not invent critical dims (skill_8)

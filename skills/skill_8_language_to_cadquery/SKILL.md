---
name: skill_8_language_to_cadquery
description: >-
  Author a new printable CadQuery part from natural language under parts/<name>/
  (Docker + uv). Use when the user describes a part without a drawing or complete
  numeric spec. Resolve ambiguity and print/assembly conflicts before modeling.
  Clear specs/drawings → skill_5; assemblies → skill_6; McMaster URL → skill_7.
---

# Language → CadQuery Part

Turn underspecified natural language into a locked `dims.md`, then a printable
part. **Resolve conflicts before build** — same spirit as skill_6’s human A/B gate.

**Never** install CadQuery on the host.

## When to use

- User describes a **new part** in prose (function, mates, fasteners, print intent)
- Drawing missing or dims incomplete — do **not** invent critical numbers
- Printable / FDM-aware parts (clearance, wall thickness, assembly access)

## When not to use

| Case | Use instead |
| --- | --- |
| Dimensioned drawing or clear numeric spec | `skill_5_drawing_to_cadquery` |
| Compose existing parts | `skill_6_assembly_workflow` |
| McMaster product URL / vendor STEP | `skill_7_mcmaster_to_cadquery` |

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Natural-language description | yes | Function, mates, fasteners |
| Part name | yes | lowercase; `PART=<name>` |
| Mating part dims | when named | Read `parts/<mate>/drawings/dims.md` |
| Units | default mm | Confirm if inch |

## Workflow

### 1. Parse intent

Extract: purpose, mating parts, fastener size/count, print vs buy, part vs assembly.
If the request is really an assembly, stop and hand off to skill_6.

### 2. Conflict / ambiguity gate (before coding)

When mate style, axes, envelope, or critical dims are missing or multi-interpretable:

1. **Stop coding** — do not invent missing critical dims or mate geometry.
2. Ask **1–2 A/B questions**. Every option must be geometrically valid and
   physically assemblable. Never offer an impossible mate.
3. In the same answer, note **print/assembly implications** per option
   (clearance, hole position relative to mating ends, print orientation).
4. After the human chooses → lock values in `drawings/dims.md`, then continue.
5. Gallery / Phase E fail on fit or orientation → **new conflict cycle**
   (re-ask; do not silently “fix”).

### 3. Print + physical assembly gate

Before authoring CadQuery:

- Assume printer tolerance ~**0.2 mm** unless the user states otherwise.
- Put **explicit** clearances in `dims.md` (beam pockets, bolt holes — do not
  leave “nominal = as printed”).
- Pull mating envelope from existing part dims when present.
- Check: fastener access, wall thickness for clamp loads, unsupported bridges,
  how the physical part is bolted/assembled.
- Lock **print bed face** and an **overhang / support plan** (or redesign until
  the stated printer can build it without heroic supports).

Rules of thumb (document chosen values in `dims.md`): see `reference.md`.

### 4. Lock design spec (dims + axes) before CadQuery

Write a full design-spec section in `parts/<name>/drawings/dims.md` **before**
any CadQuery (template in `reference.md`): axes, mates, fasteners, join ops +
operands, openings, interfaces, print orientation/overhangs. Document X/Y/Z in
`model.py` and `views.py`. Do not treat a thin A/B chat as a finished drawing.

### 5. Author

```bash
./scripts/new_part.sh <name>
```

Implement `build_part()`, `assert_geometry()`, export **STEP + STL** (skill_2).

### 6. Validate

```bash
PART=<name> ./scripts/run_pipeline.sh --skip-human
PART=<name> ./scripts/open_gallery.sh
```

### 7. Human verification

Update `views.py` criteria; `skill_4` when signing off.

## Anti-patterns

| Mistake | Fix |
| --- | --- |
| Inventing missing dims | Stop; A/B or ask for the number |
| Skipping the conflict gate | Lock mates/axes in dims.md first |
| Treating prose as a finished drawing | Language → gate → dims → model |
| Vague “hull / connect / flip” | Lock the op + operands + open direction in dims.md (see `reference.md`) |
| Ignoring print clearance | Oversize fits/holes explicitly (~0.2 mm) |
| Skipping print orientation / overhangs | Lock bed face + overhang plan in dims.md before coding |
| Coding from thin A/B only | Finish design-spec template in dims.md first |
| Assembly under `parts/` | Use skill_6 under `assemblies/` |
| Assembly before part sign-off | Part Phase E first; then skill_6 |
| Endless gallery→patch loops | After repeated Phase E fails → re-spec / postmortem, don’t grind |

## Checklist

- [ ] Intent parsed; part vs assembly triaged
- [ ] Ambiguity / print-assembly gate passed (human A/B if needed)
- [ ] Design-spec in `drawings/dims.md` locked (axes, mates, fasteners, join ops, clearances, **bed face / overhangs**)
- [ ] STEP/STL via pipeline A–D
- [ ] Gallery / skill_4 as needed
- [ ] Assembly only after part human pass (when an assembly is in scope)

## Related

`skill_1`–`skill_4`; numeric/drawing → `skill_5`; assemblies → `skill_6`;
McMaster → `skill_7`; print clearances + design-spec template in `reference.md`.
Cautionary archive (not an exemplar):
[`docs/postmortems/tripod_head_openbeam_15.md`](../../docs/postmortems/tripod_head_openbeam_15.md).

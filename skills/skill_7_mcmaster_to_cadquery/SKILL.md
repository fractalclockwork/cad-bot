---
name: skill_7_mcmaster_to_cadquery
description: >-
  Import a McMaster-Carr catalog part from a product URL into parts/<name>/ by
  loading a local gitignored vendor STEP into CadQuery (importStep), framing
  axes, and re-exporting STEP+STL. Login + manual STEP drop-in only; no API;
  never commit vendor CAD; never automate CAD download.
---

# McMaster-Carr URL → CadQuery Part

Bring a McMaster product into the PART pipeline by **importing their STEP** in
CadQuery — do not reinvent the solid when vendor CAD is available.

**Never** install CadQuery on the host. **Never** commit vendor CAD.
**Never** call `api.mcmaster.com`. **Never** automate McMaster CAD download
(login wall).

## When to use

- User provides a McMaster product URL (e.g. `https://www.mcmaster.com/3971N31/`)
- Catalog hardware for assemblies (pillow blocks, fasteners, etc.)

For scratch solids from drawings/specs → `skill_5`. For assemblies → `skill_6`.

## Policy

| Rule | Detail |
| --- | --- |
| Use vendor STEP | `cq.importers.importStep` is the primary geometry path |
| No repo taint | Vendor files only under gitignored `vendor/mcmaster/` |
| Manual after login | Operator logs into McMaster and downloads **3-D STEP** by hand |
| No API / no scrape | Do not call the Product API or automate CAD fetch |
| Our exports | Pipeline re-exports STEP+STL to `output/<PART>/` (also gitignored) |
| Dims still required | Public catalog attributes in `drawings/dims.md` for asserts/mates |

If STEP is missing, **stop and ask** the operator to drop it in — do not rebuild
parametrically or invent a bootstrap solid unless the user explicitly requests that.

## Layout

```
vendor/mcmaster/<PartNumber>_<McMaster title>.STEP   # preferred — original download name
vendor/mcmaster/<PartNumber>.step                    # optional short alias
parts/mcm_<partnum_lower>/
  README.md
  model.py                          # importStep + frame
  views.py
  drawings/dims.md                  # URL + catalog attrs + axes
```

PART id: `mcm_<lowercase_partnum>` (e.g. `mcm_3971n31`).
Keep McMaster’s download filename under `vendor/mcmaster/` as the naming reference
(e.g. `3971N31_Ready-Mount Bearing Housing.STEP`).

## Workflow

### 1. Parse URL

From `https://www.mcmaster.com/<PartNumber>/` extract the part number.

### 2. Obtain STEP (manual, after login)

McMaster requires login to download CAD. The **operator** (not the agent) must:

1. Log into McMaster in a normal browser.
2. Open the product page → Product Detail.
3. Select **3-D STEP** in the CAD format control.
4. Use the download control (Save, or Save link as if needed).
5. Move the download into `vendor/mcmaster/` **keeping McMaster’s original
   filename** (e.g. `3971N31_Ready-Mount Bearing Housing.STEP`).
6. Confirm the file starts with `ISO-10303-21;` before continuing.

Docker mounts `./vendor` at `/work/vendor` (see `docker-compose.yml`), so the
gitignored path is visible in-container.

Reject stubs: tiny HTML/comment files are not CAD — re-download after login.

### 3. Catalog dims

Fill `parts/<PART>/drawings/dims.md` **before** coding:

- Source URL + product title
- Published attributes (overall L/W/H, bore, mount pitch, hole dia) → mm
- Convert inch fractions (`1/8"` → 3.175)
- Axis convention after framing
- Note: geometry comes from vendor STEP; dims are for asserts/mates

**Do not invent** missing mate-critical dims — ask.

### 4. Scaffold + import

```bash
./scripts/new_part.sh mcm_<partnum_lower>
```

In `build_part()`:

1. Resolve vendor STEP: prefer `vendor/mcmaster/<PartNumber>_*.STEP` (McMaster
   download name), then `<PartNumber>.step` (repo-relative and `/work/…`).
2. Raise a clear `FileNotFoundError` if missing (point at manual download steps).
3. `shape = cq.importers.importStep(str(path))`
4. Apply a documented **frame transform** for the mount type (measure bore vs
   mount-hole axes first — never force a flange STEP into Y=shaft when
   bolts ∥ bore):

   | Mount type | X | Y | Z |
   | --- | --- | --- | --- |
   | Pillow / base-mount (e.g. 3971N31) | bolt pitch / base length | **shaft / bore** | up from mount face |
   | Two-bolt flange (e.g. 1434K33) | bolt pitch / flange long | flange short (mount plane) | **shaft / bore**, mount face Z≈0 |

5. Return a `cq.Workplane` suitable for exporters.

### 5. Assert + export

- `isValid`; volume > 0
- Bounding box vs catalog overall dims (± `DIM_TOL`)
- Export **STEP + STL** only (no DXF gate)

### 6. Validate

```bash
PART=mcm_<partnum_lower> ./scripts/run_pipeline.sh --skip-human
PART=mcm_<partnum_lower> ./scripts/open_gallery.sh
```

## Forbidden

- `git add` of `vendor/mcmaster/*.step` (or any McMaster CAD)
- McMaster Product Information API / credentials in-repo
- Automating CAD download / scraping download endpoints
- Committing vendor CAD under `parts/`
- Silent parametric reinvent or bootstrap STEP when McMaster CAD is missing

## Checklist

- [ ] Part number + PART id chosen
- [ ] Operator logged in and dropped STEP in `vendor/mcmaster/` (gitignored)
- [ ] File has `ISO-10303` header — not staged in git
- [ ] `drawings/dims.md` with URL + catalog attrs + axes
- [ ] `importStep` + frame in `model.py`
- [ ] Pipeline A–D PASS
- [ ] `git status` shows no vendor STEP tracked

## Exemplars

| Mount | PART | Catalog |
| --- | --- | --- |
| Pillow / base-mount | `parts/mcm_3971n31/` | [3971N31](https://www.mcmaster.com/3971N31/) ready-mount housing |
| Two-bolt flange | `parts/mcm_1434k33/` | [1434K33](https://www.mcmaster.com/1434K33/) mounted roller bearing |

## Related

`skill_1`–`skill_4`; `skill_5` for scratch geometry; `skill_6` for assemblies
(pre-mate gate + human conflict resolution).

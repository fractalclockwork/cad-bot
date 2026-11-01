# McMaster-Carr vendor STEP cache

Local-only CAD for CadQuery `importStep`. **Do not commit** `.step` / `.STEP` /
other McMaster CAD — they are gitignored.

McMaster requires **login** to download CAD. Drop files in by hand; do not use
the Product Information API or automate downloads in this repo.

## Naming convention

Keep McMaster’s **original download filename** when you save into this folder.
That name is the reference for matching catalog CAD to PART ids
(`mcm_<lowercase_partnum>`).

| Kind | Example |
| --- | --- |
| McMaster download (preferred) | `3971N31_Ready-Mount Bearing Housing.STEP` |
| Short alias (optional) | `3971N31.step` |

Pattern: `<PartNumber>_<Product title>.STEP` as served by McMaster.

## Drop-in (manual)

1. Log into https://www.mcmaster.com/ in a normal browser.
2. Open the product page (e.g. https://www.mcmaster.com/3971N31/).
3. Product Detail → select **3-D STEP**.
4. Use the download control (Save, or Save link as if needed).
5. Move the file into `vendor/mcmaster/` **without renaming** (keep the McMaster name).

Example:

```text
vendor/mcmaster/3971N31_Ready-Mount Bearing Housing.STEP
```

Parts under `parts/mcm_<partnum_lower>/` resolve that path via skill_7
(prefer original name, then `<PartNumber>.step`).

## Validate the file

A real STEP starts with `ISO-10303-21;`. If the file is only a few dozen bytes
or looks like an HTML comment, the download failed (often not logged in) —
delete the stub and download again after login.

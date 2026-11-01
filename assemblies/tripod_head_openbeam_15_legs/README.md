# tripod_head_openbeam_15_legs — deferred with head

Fit-check assembly for `tripod_head_openbeam_15` + three `openbeam_15x100`
legs. **Deferred:** the head is an archived partial (FDM overhang debt); do not
treat this assembly as signed-off. See
[`docs/postmortems/tripod_head_openbeam_15.md`](../../docs/postmortems/tripod_head_openbeam_15.md).

```bash
PART=tripod_head_openbeam_15_legs ./scripts/run_pipeline.sh --skip-human
PART=tripod_head_openbeam_15_legs ./scripts/open_gallery.sh
```

Dims/mates: [`drawings/dims.md`](drawings/dims.md). Follow **skill_6** only after
the head is redesign-signed for print.

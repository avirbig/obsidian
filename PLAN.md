# Obsidian Provenance — Fresh Analysis (Claude)

**Goal.** From raw data only, build a clean, reproducible pipeline that (a)
assembles a verified reference database of obsidian source chemistry from the
article tables, and (b) attributes the researcher's own pXRF samples (Motza,
Einan/Ain Mallaha, Yiftahel) to their most likely geological source — with
honest, method-consistent confidence.

The previous attempt is archived in `Analysis with GitHub Copilot/`. Its
mistakes are documented in `docs/prior_work_audit.md` and must not be repeated.

## Layout
```
data/                  RAW INPUTS — read-only, never edited
  articles/            42 source article texts
  article_tables/      11 xlsx element tables extracted from articles
  samples/             9 Niton/xlsx files (raw pXRF sample exports)
  external_reference/  Chronology, Obsidian Sources List, DObsiSS (external, provenance TBD)
docs/                  knowledge that guides the work
  pxrf_sampling_methodology.md   (author-written)
  reference_data_verification_report.md   (AI-produced; verifies article data is traceable — under review)
  prior_work_audit_made_with_github_copilot.md   (Claude's audit of the old work)
analysis/              NEW scripts (built step by step, reproducible via __file__)
reference_db/          NEW verified reference outputs
results/               NEW figures + reports
CHANGELOG.md           running log of what was done
```

## Guardrails (from the audit)
1. Read only from `data/` and from files this pipeline itself produced.
2. Method→tier mapping re-derived from the articles; **primary attribution is
   pXRF-vs-pXRF only**. Cross-method comparison is a labeled secondary check.
3. Every attribution reports goodness-of-fit; items outside all sources are
   explicitly "unassigned", not force-fit to a nearest source.
4. All scripts resolve paths from `__file__` and run top-to-bottom on this machine.
5. Any calibration correction is a stated assumption + sensitivity check — never
   fitted to the source we then attribute to.

## Plan (to be filled in step by step, together)
- [ ] Step 0 — environment + confirm raw inputs inventory
- [ ] Step 1 — review `source_method_inventory.md` for correctness; finalize
      the article → method → tier mapping
- [ ] Step 2 — extract & verify reference tables from `data/article_tables/`
- [ ] Step 3 — build the reference database (per-source stats, by method)
- [ ] Step 4 — load & clean the raw pXRF samples from `data/samples/`
- [ ] Step 5 — internal structure of the assemblage (PCA / clustering)
- [ ] Step 6 — source attribution (pXRF-primary, with confidence + unassigned)
- [ ] Step 7 — report

*Steps beyond Step 1 are intentionally not detailed yet — we design each one as
we reach it.*

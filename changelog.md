# Changelog — Fresh Analysis (Claude)

Format: `[YYYY-MM-DD] | TYPE | Description`

## 2026-07-20
- `REORG` | Archived all prior GitHub Copilot work into `Analysis with GitHub Copilot/` (analysis scripts, outputs, reference_database, derived sample CSVs, old PLAN/REPORT_PLAN/changelog, .vscode agent files).
- `REORG` | Consolidated raw inputs under read-only `data/`: `articles/` (42), `article_tables/` (11, was obsidian_minerales_...), `samples/` (9 raw xlsx/xls), `external_reference/` (3 external xlsx — Chronology, Obsidian Sources List, DObsiSS; not author's own data).
- `REORG` | Kept knowledge docs in `docs/`: `pxrf_sampling_methodology.md` (author-written), `reference_data_verification_report.md` (AI-produced, ex `audit_cross_reference.md`, now `reference_data_verification_report.md`, to be reviewed).
- `DOC`   | Wrote `docs/prior_work_audit_made_with_github_copilot.md` (audit of the previous analysis) and a fresh `PLAN.md`.
- `SETUP` | Created empty working dirs: `analysis/`, `reference_db/`, `results/`.
- (committed as `14f2293`)

## 2026-07-20 (session 2 — reference-data verification review)
- `VERIFY` | Reviewed `docs/reference_data_verification_report.md` against the actual workbooks: all Section A articles exist; empty-sheet claims (Frahm 2014, Gratuze 1999) confirmed; Section E tier logic confirmed correct.
- `FIX`    | Corrected a mislabel: the `Carter et al 2013` sheet is **Körtik Tepe** (samples KT.002–KT.119, verified against the article), NOT Kenan Tepe. "Kenan" appears in no workbook cell. Moved to Section A; noted Source-column encoding corruption + stray `Bekle` row for extraction cleanup.
- `DECISION` | Dropped from reference set: Oddone 1997, Yellin et al. 1996 (no article), Gratuze 1999 (empty), Ozdemir 2006 (no confirmed data). Kept Bressy 2005 (via Forster 2012) and Kelle & Seifried 1990 (via Frahm & Hauck 2017) as traceable second-hand.
- `DOC`    | Added a table of contents and per-section legends to the verification report; refreshed `articles/` → `data/articles/` paths; updated Sections D/E/F.
- `DATA`   | Deleted duplicate article `data/articles/carter_2013_Networks_and_Neolithisation.txt` (a second copy of the Körtik Tepe paper); kept `Carter_2013_Sourcing_obsidian_Kortik_Tepe.txt`.
- `DATA`   | Author manually curated `data/article_tables/data2.xlsx` in Excel: deleted the `Gratuze 1999`, `Yellin et al 1996`, and `Frahm 2014` sheets (dropped / no original data). Now 12 sheets. Verified no data loss elsewhere: `Yellin and Perlman 1981` 38→10 rows was only Excel trimming empty trailing rows (10 data rows identical). Pristine originals remain in initial commit `a485ee2`.
- `DOC`    | Report: marked Craig 2007 / Sheppard 2011 / Moholy-Nagy 2013 / Nazaroff 2010 as non-Mediterranean, irrelevant (safe to remove); noted Frahm 2014 sheet deletion; noted Oddone 1997 sheet remains but is excluded.
- `DOC`    | Added a relevance-ranked summary table of all data-bearing papers (method/tier, region, sources/sites, ~N, role), ordered most→least relevant (pXRF+Anatolia first). Sources verified by scanning actual sheet cells. Flagged: Yellin & Maeir 2007 has no data sheet (article-only); Rosen 2011 is oxides-only (not usable for sourcing); Morgan 2015 is Aegean/Melian (low relevance).
- `VERIFY` | Verified author's Milic 2014 fix: standalone file removed; data1 sheet restructured into stacked summary + per-sample table (Source, Ti, Mn, Fe, Zn, Rb, Sr, Zr, Ba, Pb) with header. Göllü Dağ/Nenezi rows clean. Residual (Carpathian only, irrelevant): split source labels + 3 split Fe values.
- `SCAN`   | Structural scan of remaining sheets. Needs fixing: Körtik (data2, Source column + Bekle row), Frahm 2013 (data1, likely reference-glass standards not sources — verify), Carter 2006 (data2, 109-col sparse layout), Multiple (data2, split author/source cells). Confirmed clean: Campbell & Healey sheets, Frahm & Hauck MAIN, Schechter, Carter&Shackley, Carter 2017, Carter/Rosenberg 2022.
- `DOC`    | Updated report ranked table (Milic fixed; Frahm 2013 relevance flagged), Section D (Milic done + Frahm note), Section F (revised fix-list with sheet locations).
- `VERIFY` | Verified author fixes: Milic Carpathian rows repaired; Körtik (Carter 2013) Source column merged + negatives/brackets removed (learned the 'Bekle' row is a real Muş sample 'Muşe Konuk Bekler', not junk; 10 RGM-2 'Standard' rows to be filtered at build time); Carter 2006 re-aligned to column A (oxides wt% + trace ppm). Frahm 2013 = basalt-glass standards + collection-area-coded obsidian (CA05/06, EA30/36) -> recommend omit.
- `RULE`   | Recorded source-name normalisation: Turkish sources appear with/without diacritics (Göllü Dağ = Gollu Dag = Gollu Dag E/EGD; Nenezi Dağ = Nenezi Dag; Bingöl = Bingol; Nemrut Dağ = Nemrut Dag; Muş = Mus; Acıgöl = Acigol). A source-alias map must be applied at DB-build time. Also filter RGM-2/Standard rows.
- `DOC`    | Report Section D rewritten as brief fix-status; ranked table + Section F updated. (data1/data2 workbook edits pending commit until Excel is closed.)

## 2026-07-20 (session 3 — Step 2: reference DB build, first pass)
- `BUILD`  | Wrote `analysis/01_build_reference_db.py` (reproducible, __file__-based). Extracts Tier-1/2 clean sheets per-article into `reference_db/by_paper/*.csv` + `reference_db/reference_long.csv` (1495 rows, 8 papers). Schema keeps source_raw/source_norm/source_region/role/method/tier + trace elements; sources kept SEPARATE per article.
- `RULE`   | Source normalisation preserves East/West/general distinction (only fixes encoding: Gollu→Göllü, ǧ→ğ, etc.). Drops RGM-2/Standard/Average/header rows. Applied source-region tagging.
- `FLAG`   | role split: source_sample=326 (Milic, Frahm&Hauck, Carter/Rosenberg Table6) vs artifact_assigned=1169 (Campbell&Healey, Schechter, Carter&Shackley, Carter2017, Körtik, beads). Milic has no Nb; Y sparse (389/1495).
- `DEFER`  | Not yet extracted: Tier-3 (Carter 2006 oxides, Khalidi, Binder, Multiple), Morgan 2015 (Aegean), Forster & Grave 2012. Frahm & Hauck sub-source numbering (Acıgöl2/3, Göllü Dağ1/2/3) kept separate per author instruction.
- `DECISION` | **Decision B**: the reference uses ONLY geological source samples (role=source_sample), not artifacts-assigned-to-a-source. Reversible: reference_long.csv keeps all rows tagged; reference_source_only.csv (326 rows, Milic + Frahm&Hauck + Carter/Rosenberg Table6) is the active reference. Thin coverage noted for Bingöl A (4) and Nemrut (5).
- `DOC`    | Created `docs/PROJECT_JOURNAL_simple.md` — a plain-English record of the goal, steps, and decisions, for the author to follow and present.
- `DATA`   | Committed author's workbook fixes (Excel now closed): Milic Carpathian rows, Körtik Source column + negatives/brackets removed, Carter 2006 re-aligned to column A. data1.xlsx / data2.xlsx saved to git.

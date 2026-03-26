# Obsidian Provenance Project — Master Change Log

Entries are recorded in **reverse chronological order** (newest first).

**Format**:
```
[YYYY-MM-DD] | TYPE | File/Target | Description | Source/Reason
```

**Types**:
- `USER_PROMPT` — verbatim record of a user request that initiated work
- `STRUCTURE` — project structure changes (folders, git, config files)
- `DATA_ADD` — new data added to a dataset
- `DATA_EDIT` — values changed in a dataset
- `DATA_REMOVE` — rows or sheets excluded from a dataset
- `VERIFICATION` — values cross-checked against an article
- `BUG_FIX` — correction of a data entry error
- `NOTE` — contextual notes, decisions, or observations

---

## Phase 2 — Data Cleaning (current session)

[2025-07-16] | STRUCTURE | analysis/notebooks/02_data_cleaning.ipynb | Created Phase 2 cleaning notebook. Reads all 21 raw CSVs from extracted_raw/, applies 8 targeted fixes, outputs to reference_database/cleaned/. Builds master all_sources_cleaned.csv with 2375 source-reference rows. | Phase 2 execution

[2025-07-16] | BUG_FIX | reference_database/extracted_raw/ → cleaned/yellin_perlman_1981.csv | CRITICAL: Phase 1 extracted Yellin 1981 with wrong row as header. Row 0 = region group labels (Central, Anatolia, Eastern, Turkey). Row 1 = actual source abbreviations (GLD, HTMD, KRUD, NNZD, NMRD1, NMRD2, ZNKT, Sevan). Phase 2 re-extracts directly from data2.xlsx using row 1 as headers. ± notation in NNZD column ('174.3±5.6') parsed: mean 174.3 retained, SD discarded. | Root cause: df_y.iloc[0] in Phase 1 cell ce0e2361 took wrong row

[2025-07-16] | DATA_EDIT | reference_database/cleaned/khalidi_gratuze_2009.csv | (1) 'Unnamed: 2' source label replaced with 'BingolA (replicate)' — this was a duplicate BingolA column in original xlsx. (2) 'Meydan_Dag˘' (U+02D8 BREVE variant) normalised to MeydanDag. | PDF-to-xlsx transcription artefacts

[2025-07-16] | DATA_REMOVE | reference_database/cleaned/milic_2014.csv | 7 rows with source='Mean' removed — these were statistical summary rows from the original table, not geological source measurements. 8 actual source rows retained. | Row inspection: 'Mean' is a sub-header from the published table

[2025-07-16] | DATA_EDIT | reference_database/cleaned/yellin_perlman_1980.csv | Rows Beisamoun (1 row) and Nahal Lavan (1 row) flagged is_source_reference=False. These are archaeological site artefact groups, not geological source samples. Chemistry matches GolluDag (La≈22.9, Eu≈0.160). attributed_source=GolluDag added. GolluDag and ND rows remain is_source_reference=True. | Yellin & Perlman 1980 paper structure; chemistry cross-check with GolluDag reference values

[2025-07-16] | DATA_EDIT | reference_database/cleaned/frahm_2013.csv | All 65 rows flagged is_source_reference=False. This file contains pXRF measurements of Tell Mozan archaeological debitage, not geological source outcrop samples. Notes column updated. | Frahm 2013 paper: pXRF validation study on artefacts

[2025-07-16] | DATA_REMOVE | reference_database/cleaned/frahm_hauck_2017_main.csv | 17 Average rows removed (computed statistics not raw measurements). 5 artifact rows flagged is_source_reference=False. 230 geological source rows retained is_source_reference=True. | Row labels in source column; Average = table footer statistics

[2025-07-16] | DATA_EDIT | reference_database/cleaned/rosenberg_carter_2022_sources.csv | Sub-outcrop labels normalised: 'Pasinler Tizgi'→Pasinler, 'Pasinler Eksisu'→Pasinler, 'Sarakamis Hamamli'→Sarikamis, 'Sarakamis Sehetin'→Sarikamis, 'Gurgurbabatepe'→SuphanDag (Gürgür Baba Tepe is a sub-vent on Süphan Dağ), 'Nemrut Dag A'→NemrutDag. | Rosenberg & Carter 2022 source table; geological literature on Süphan Dağ sub-outcrops

[2025-07-16] | DATA_EDIT | reference_database/cleaned/carter_2013_kenan_tepe.csv | Generic 'Bingol' label (104 rows) split into BingolA/BingolB using Sr discriminant: Sr < 10 ppm → BingolA (34 rows), Sr ≥ 10 ppm → BingolB (69 rows), 1 row unresolved (Sr=NaN). Reference values: BingolA Sr≈0.5 ppm (Khalidi 2009), BingolB Sr≈33 ppm (Khalidi 2009). Bimodal distribution confirmed in this dataset (cluster 1: 3-8 ppm, cluster 2: 37-54 ppm). 2 outlier rows at Sr=113 and Sr=624 ppm classified as BingolB — anomalous but no alternative attribution available. | Campbell & Healey 2016 Rb/Sr discriminant methodology

[2025-07-16] | DATA_ADD | reference_database/cleaned/all_sources_cleaned.csv | Master reference database created: 2375 rows, is_source_reference=True only, 14 pXRF-compatible element columns (Rb, Sr, Zr, Nb, Y, Fe, Mn, Ba, Zn, Ti, Th, U, Pb, Ga). Source coverage: EGD=126, NemrutDag=370, BingolA=195, BingolB=240, ND=91, GolluDag=46, BingolB=240, MeydanDag=38, Sarikamis=53, Pasinler=11, Mus=5. Tiers: 1=1814, 2=273, 3=234, 4=13. | Phase 2 master merge; all_sources_cleaned.csv

[2025-07-16] | NOTE | reference_database/cleaned/ | Oxide wt% columns in carter_2006.csv, binder_2011.csv, rosen_2011.csv, forster_grave_2012.csv NOT converted to elemental ppm. Conversion requires stoichiometry and oxidation-state assumptions (esp. Fe2O3 vs FeO). These files contain ppm trace elements (Rb, Sr, Zr, Nb, Y etc.) which ARE in the master file. Decision deferred to Phase 3. | Phase 2 NOTE

---

## 2025-07-15

[2025-07-15] | USER_PROMPT | — | "continuing from previous session — run remaining extraction notebook cells, fix unmapped source labels, extract all data2.xlsx papers"

[2025-07-15] | DATA_ADD | reference_database/extracted_raw/ | Phase 1 extraction complete. 21 CSVs saved, 2467 rows total. New CSVs added this session vs prior summary: carter_2006.csv (101 rows, ICP-MS, EGD=55 ND=45 AciGolWest=1), oddone_1997.csv (3 rows, XRF, WGD+EGD), forster_grave_2012.csv (5 rows, EDXRF, ND+EGD+HotamisDag+AciGol), rosen_2011.csv (3 mean rows, Electron Microprobe, BingolA), binder_2011.csv (8 rows, LA-ICP-MS, all EGD sub-outcrops Göllüdag1-7/4a/4b), rosenberg_carter_2022_sources.csv (44 rows, EDXRF, EGD/BingolA/B/Mus/Pasinler/Sarikamis/SuphanDag), rosenberg_carter_2022_tel_tsaf_beads.csv (24 rows, bead data), frahm_hauck_2017_main.csv (252 rows, pXRF/EDXRF/NAA/WDXRF mixed methods), frahm_hauck_2017_gollu_dag_crossmethod.csv (17 rows, cross-method reference), khalidi_gratuze_2009.csv (4 source-mean rows, LA-ICP-MS) | Phase 1 execution; data2.xlsx remaining sheets extracted

[2025-07-15] | DATA_EDIT | reference_database/extracted_raw/carter_2013_kenan_tepe.csv | Source labels corrected: 'Bingöl' → 'Bingol' (generic; article does not split A/B), 'Nemrut' → 'NemrutDag', 'Mus¸' (garbled encoding) → 'Mus'. 121 rows: Bingol=104, NemrutDag=15, Mus=1 | SOURCE_MAP update + re-run of extraction cell; unicode artifact 'mus¸' → ş resolved

[2025-07-15] | DATA_ADD | reference_database/extracted_raw/yellin_perlman_1980.csv; yellin_1996.csv; yellin_perlman_1981.csv | Yellin NAA papers extracted from data2.xlsx (Tier 4). 4+3+4 rows of source-mean values. | Previously logged but now confirmed in final summary

[2025-07-15] | BUG_FIX | analysis/notebooks/01_data_extraction.ipynb — normalise_source() | Added unicodedata.normalize('NFC', ...) to normalise_source() before dict lookup. Fix resolves NFD-encoded characters from Excel files (e.g. Kömürcü stored as 'o'+combining-diaeresis instead of precomposed ö). Source map now correctly maps Kömürcü→EGD, Nenezi Daǧ→ND, Göllü Daǧ variants→GolluDag, Sarıkamış→Sarikamis, Süphan Daǧ→SuphanDag | reproduced by checking hex codepoints; unicodedata.normalize applied

[2025-07-15] | DATA_EDIT | analysis/notebooks/01_data_extraction.ipynb — SOURCE_MAP | Expanded source map from 81 to 122 entries. New entries added: east golu dag/golu dag variants (single-l spelling), bingôl a (caret artifact), acıgöl2/3 (Frahm & Hauck sub-outcrops), nenezi daǧ (ǧ variant), sarıkamış/2 → Sarikamis, suphan dag/daǧ → SuphanDag, kömürcü → EGD, hotamış/acıgöl/hasan daǧ variants → HotamisDag/AciGol/HasanDag. | Source label variants discovered during cell-by-cell extraction

[2025-07-15] | NOTE | reference_database/extracted_raw/frahm_2013.csv | IMPORTANT: This file contains pXRF measurements of Tell Mozan archaeological artefacts (obsidian debitage), NOT geological source reference samples. Do NOT use for building source reference ellipses. Source = EGD for all 65 rows (from provenance assignment in article). | Confirmed by reading article abstract; Frahm 2013 is a pXRF validity study, not a source reference paper

[2025-07-15] | NOTE | reference_database/extracted_raw/carter_2013_kenan_tepe.csv | 'Bingol' label (104 rows) is generically attributed to Bingöl volcanic complex without splitting into A/B. Cannot split from this dataset alone. Flagged for Phase 2 review — may need to map to BingolA or BingolB using chemistry in Phase 2 (Rb/Sr discriminant). | Campbell & Healey 2016 article shows BingolA/B are distinguishable by Rb/Sr

[2025-07-15] | NOTE | reference_database/extracted_raw/rosen_2011.csv; carter_2006.csv; binder_2011.csv; forster_grave_2012.csv | These CSVs contain oxide wt% columns (Al2O3, Fe2O3, K2O, etc.) not converted to elemental ppm. In Phase 2 data cleaning, decide whether to convert (e.g. Fe2O3 → Fe) or keep as oxides with appropriate column naming. | Data formats noted during extraction

[2025-07-15] | STRUCTURE | analysis/notebooks/01_data_extraction.ipynb | Added new cells for remaining data2.xlsx papers: 4B-i Oddone 1997, 4B-ii Forster & Grave 2012, 4B-iii Rosen 2011, 4B-iv Carter 2006, 4B-v Binder 2011. Skipped: Gratuze 1999 (empty sheet), Acquafredda 2018 (Italian/Sardinian — irrelevant for Levantine analysis), Multiple sheet (compilation of data already in source papers — would cause duplicates). | data2.xlsx sheet inspection

## 2026-03-25

[2026-03-25] | STRUCTURE | analysis/notebooks/01_data_extraction.ipynb | Created Phase 1 extraction notebook. Covers Tier 1 papers (Schechter 2016, Frahm 2013, Milic 2014, Campbell & Healey 2016, Morgan 2015), Tier 2 (Carter & Shackley 2007, Carter 2017, Carter 2013 Kenan Tepe, Rosenberg & Carter 2022), Tier 3 (Khalidi 2009, Frahm & Hauck 2017), Tier 4 (Yellin & Perlman 1980/1981, Yellin 1996). Outputs to reference_database/extracted_raw/. | Phase 1 execution per PLAN.md

[2026-03-25] | USER_PROMPT | — | "ive added frahm 2013 txt. proceed with the plan. later summarize me consicely what has been done and what is missing. git add and commit the changes"

[2026-03-25] | DATA_ADD | articles/Frahm_2013.txt | Added article text for Frahm 2013 (JAS 40:1080–1092) — pXRF validity paper for Near Eastern obsidian. 67 HHpXRF measurements of Göllü Dağ debitage; elements: Rb, Sr, Zr, Zn, Mn, Ti with error columns. Matches Frahm 2013.xlsx. audit_cross_reference.md Section A updated. | User added file; article abstract confirmed

[2026-03-25] | USER_PROMPT | — | "how would you suggest to proceed. notice i've added the frahm txt file 2014. but i dont see tables of element amounts in it."

[2026-03-25] | NOTE | articles/Frahm_2014.txt | Confirmed: Frahm 2014 (JAS 41:605-621) is a Bronze Age Northern Mesopotamia blade production paper — contains no elemental concentration tables. The empty Frahm 2014 sheet in data2.xlsx is correctly empty and will not be filled. audit_cross_reference.md updated accordingly. | Article read; abstract and body confirmed

[2026-03-25] | STRUCTURE | reference_database/PRE_PHASE1_INVENTORY.md | Created full pre-Phase-1 inventory of all xlsx files: every sheet, row counts, element columns, extraction status, and special handling notes. Python/openpyxl scan confirmed. | Python openpyxl scan of all obsidian_minerales_component_tables_from_articles/*.xlsx

[2026-03-25] | NOTE | data2.xlsx → Frahm 2014 sheet | Confirmed empty — Frahm 2014 article has no geochemical source tables (Bronze Age craft specialisation paper). Will remain empty. | PRE_PHASE1_INVENTORY.md; articles/Frahm_2014.txt

[2026-03-25] | NOTE | data2.xlsx → Gratuze 1999 sheet | Remains empty — PDF not yet available. Flag for future acquisition. | PRE_PHASE1_INVENTORY.md

[2026-03-25] | USER_PROMPT | — | "initiate phase 0 (and 6)" | User session

[2026-03-25] | USER_PROMPT | — | "this plan looks alright. i will add that my sampling data will also need some cleaning and ordering and verifications so add this to the plans. i want you to record the plan somewhere so it will be written and not lost if i restart another session. also in the log include my prompts will be recorded as well. also i want you to create a git tracking to this project if i decide later to push it to remote. how do we proceed?" | User session

[2026-03-25] | USER_PROMPT | — | "everything you've written is correct. but there are few more that i would like to add. currently i want to produce your suggested actions in order to later compare my pxrf samples on obsidian from south levant sites and find their origin. i want to prepare the data set that will be what i would compare my results too. i also want to produce some resolutions from all this data. see patterns and make visual representation of some of them. with AI help i want to create a new dataset or database in a new folder that will be the data that you've help to build and clean and verify against the articles. from the articles and the xlsx files that i've previously copied their tables into them. help me plan please. i want also to follow the latest protocols in the papers. i also want to log every changes or edits to the data verbaly and verbosely in a file so it will be clear to someone who would want to understand or recreate the data. also i will need help and understand the statistics you will use and explanations since i know very little on statistics. also i would like some explantation on what ratios to plot as they did in the papers. please also consider the project structure make it as clear and tidy as can be. also i want you to create dedicated agent and dedicated skills so they would help me reach my goals" | User session

[2026-03-25] | STRUCTURE | c:\work\code\obsidian | Initialized local git repository (git init). No remote set. Placeholder identity set (researcher@obsidian-project.local). | Plan Phase 0

[2026-03-25] | STRUCTURE | c:\work\code\obsidian | Created folder structure: reference_database/sources/, my_samples/, analysis/notebooks/, analysis/scripts/, outputs/figures/. Created .gitignore, utils.py placeholder, .gitkeep files | Plan Phase 0

[2026-03-25] | STRUCTURE | c:\work\code\obsidian\PLAN.md | Created permanent project plan document covering all 6 phases | Plan Phase 0

[2026-03-25] | STRUCTURE | c:\work\code\obsidian\changelog.md | Created this master change log file | Plan Phase 0

[2026-03-25] | STRUCTURE | .vscode/ | Created obsidian-research.agent.md (domain-aware agent), obsidian-data.instructions.md (data handling rules), obsidian-statistics.instructions.md (statistics explanations) | Plan Phase 6

[2026-03-25] | NOTE | audit_cross_reference.md | Updated audit file: added 7 newly matched papers to Section A (Binder 2011, Rosen 2011, Yellin & Perlman 1980/1981, Poupeau 2010, Carter 2017, Rosenberg/Carter 2022); removed resolved entries from Section B; added new articles to Section C (Carter 2008, Orange/Carter 2013, Carter/Grant 2013, JARMT, Yellin & Garfinkel 1986); fixed Carter 2013 disambiguation note | Workspace audit

[2026-03-25] | USER_PROMPT | — | "remind me the remaining steps by small description of each" | User session

[2026-03-25] | VERIFICATION | reference_database/cleaned/all_sources_cleaned.csv | Phase 6 complete (commit 8686541). Cross-verified 2337/2375 rows (98%). 0 element mismatches. Unverified 38 rows across 4 categories (missing article section, single-source, format variation). | analysis/06_verification.py

[2026-03-25] | USER_PROMPT | — | "fix this please [Yellin 1981 Sevan to Zincirkale]. then proceed to phase 3" | User session

[2026-03-25] | BUG_FIX | reference_database/cleaned/yellin_perlman_1981.csv | Row with La=132.6 had source label 'Sevan' — corrected to 'Zincirkale' per Yellin & Perlman 1981 Table 1 footnote. Master CSV rebuilt. Source count: 34 total. | commit 9168788

[2026-03-25] | ANALYSIS | reference_database/source_statistics.csv; reference_database/source_statistics_report.txt | Phase 3 complete (commit 9168788). 92 stat rows (34 sources × mean/SD). Key Tier 1 fingerprints: BingolA Rb=230 Zr=1238; BingolB Zr=327; NemrutDag Zr=1277; EGD Zr=77; Sta Nychia Rb=119 Sr=102; Group3d Rb=462. | analysis/07_source_statistics.py

[2026-03-25] | USER_PROMPT | — | "yes. proceed with phase 4" | User session

[2026-03-25] | USER_PROMPT | — | "why start phase 5 before phase 4?" | User session

[2026-03-25] | DATA_ADD | reference_database/tier1_comparison_ready.csv; reference_database/source_comparison_fingerprints.csv | Phase 4 complete (commit efcb1ab). Tier 1 filter applied: 1814 rows, 34 sources. Quality categories: strong(9), moderate(3), weak(8), no_pxrf(14). source_comparison_fingerprints.csv: one row per source with mean+SD for Rb/Sr/Zr/Nb/Y. | analysis/08_tier_filter.py; reference_database/phase4_report.txt

## 2026-03-26

[2026-03-26] | USER_PROMPT | — | "what folder should i put the results?" | User session

[2026-03-26] | NOTE | my_samples/ | Confirmed target folder for user pXRF data. Already existed as placeholder from Phase 0. | User session

[2026-03-26] | USER_PROMPT | — | "whats the next step? what should i do?" | User session

[2026-03-26] | USER_PROMPT | — | "I've put my files in the samples folder. first i want you to look at the files content and try to understand each file..." | User session [NOTE: full text not recoverable — was summarized before this session. User to supply if needed.]

[2026-03-26] | USER_PROMPT | — | "Start implementation" | User session

[2026-03-26] | USER_PROMPT | — | "alright please commit and add all changes. i also want to say that in the changelog put my full prompt. do not cut it like u done here: [2026-03-26] | USER_PROMPT | — | \"I've put my files in the samples folder. first i want you to look at the files content and try to understand each file...\" | User session -- now what should we do next? dont start just tell me" | User session

[2026-03-26] | DATA_ADD | my_samples/samples_raw.csv | Phase 5a: loaded 1224 pXRF readings from 'data manipulation.xlsx' (sheet 'First Changes'). Converted wt% to ppm (×10000). < LOD → NaN. item_id = site_prefix + '_' + basket. Joined filter times (main/low/high/light sec) from numbered session files 01–05 via Reading No. 3 sites: einan(226), motza(946), yiftahel(52). Periods: EPPNB, MPPNB, natufian. KEY: Y not measured in Niton Mining Cu/Zn mode; Sr coverage only 5% (mostly below LOD). 1224 rows, 49 cols. | analysis/09_load_samples.py

[2026-03-26] | DATA_ADD | my_samples/samples_clean.csv | Phase 5b: averaged duplicate readings per artifact. 510 unique items. quality_flag: good=286, repeat_divergent=192, single=26, beam_minimal=2, beam_minimal+repeat_divergent=4. CV threshold 10%. 40% of paired items have ≥1 heavy-4 element with CV≥10% (repeat_divergent) — large number, likely reflects dorsal/ventral geometry effect. | analysis/10_clean_samples.py

[2026-03-26] | VERIFICATION | my_samples/verification_report.txt | Phase 5c: completeness/repeatability/range checks. Rb/Zr/Nb coverage ≥99%; Sr only 9% at item level (mostly LOD). Mean CV%: Rb=3.8, Zr=5.5, Nb=5.1. Range outliers: 4 Fe items, 2 Ti items, 2 Pb items, 3 Zn items (non-critical for sourcing). Note: Y not measured — source attribution will use 3-element fingerprint Rb/Zr/Nb (Sr effectively absent). | analysis/11_verify_samples.py

---

## Template for future entries

```
[YYYY-MM-DD] | DATA_ADD | reference_database/sources/EGD.csv | Added 23 rows from Carter & Shackley 2007 Table 2 (EGD source measurements, EDXRF, ppm) | Carter_and_Shackley_2007.txt p.XXX, Table 2

[YYYY-MM-DD] | DATA_EDIT | reference_database/sources/EGD.csv | Corrected Rb value for sample CS07-14 from 185 to 158 (typo in xlsx, article confirms 158) | Carter_and_Shackley_2007.txt Table 2

[YYYY-MM-DD] | DATA_REMOVE | data2.xlsx | Skipped Gratuze 1999 sheet — empty, no data present | audit_cross_reference.md D1

[YYYY-MM-DD] | DATA_EDIT | Milic 2014.xlsx | Parsed range string "166-194" in column Rb for sample M14-07 to midpoint 180; original preserved in Rb_range_flag | Milic 2014 Table 3, range format

[YYYY-MM-DD] | VERIFICATION | reference_database/sources/EGD.csv | Spot-checked 5 rows against Carter_and_Shackley_2007.txt — no discrepancies found | Carter_and_Shackley_2007.txt Table 2

[YYYY-MM-DD] | USER_PROMPT | — | "exact user request text here" | User session
```

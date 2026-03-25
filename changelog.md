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

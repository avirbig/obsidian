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

## 2026-03-25

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

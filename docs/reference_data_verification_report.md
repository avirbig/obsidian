# Cross-Reference Audit: Tables vs Articles

*Purpose: verify that every obsidian reference table extracted from the
literature is (a) reliable and (b) traceable back to a source article. This is
the trusted foundation for the reference database — the analysis pipeline must
follow the tier logic in Section E exactly.*

## Contents

- [Summary](#summary-of-all-papers-referenced-in-your-spreadsheets)
- [Ranked Data Summary (most → least relevant)](#ranked-data-summary-most--least-relevant)
- [A. Papers WITH data tables AND matching articles](#a-papers-with-data-tables-and-matching-articles)
- [B. Papers WITH data tables but NO matching article](#b-papers-with-data-tables-but-no-matching-article-in-dataarticles)
- [C. Articles with NO corresponding data table](#c-articles-in-dataarticles-with-no-corresponding-data-table)
- [D. Data Quality Issues Found](#d-data-quality-issues-found)
- [E. Analytical Method Comparability for pXRF](#e-analytical-method-comparability-for-pxrf)
- [F. Priority Actions](#f-priority-actions)

---

## Summary of all papers referenced in your spreadsheets

*Legend — every paper/study referenced across the xlsx files in
`data/article_tables/`, mapped against the article texts in `data/articles/`.
Each paper is sorted into: has-data-and-article (A), has-data-but-no-article (B),
or has-article-but-no-data-yet (C).*

---

## Ranked Data Summary (most → least relevant)

*Legend — every paper that contributes **actual data**, ranked from most to least
relevant for sourcing Southern-Levant obsidian. Relevance combines **method
comparability** to our pXRF samples (pXRF > EDXRF > ICP / LA-ICP-MS / PIXE >
NAA / microprobe) with **how directly the sources/region bear on Anatolian→Levant
provenance**. "Sources" = geological obsidian sources characterised; "Site" =
archaeological assemblage attributed to sources. `~N` = approximate data rows
(sources or artifacts). Sources confirmed by scanning the actual sheet cells.*

| # | Paper | Method (Tier) | Region focus | Sources / sites present | ~N | Role | Relevance |
|---|-------|---------------|--------------|--------------------------|----|------|-----------|
| 1 | Campbell & Healey 2016 | pXRF (T1) | E Anatolia | Bingöl A/B, Nemrut Dağ, Muş, Meydan Dağ, Group 3d, Pasinler | ~880 | Source characterisation | ★★★★★ the peralkaline sources we must discriminate |
| 2 | Schechter et al 2016 | pXRF (T1) | S Levant sites + Anatolia | Göllü Dağ, Bingöl | ~100 | Levant artifacts + sources | ★★★★★ same region + method as our samples |
| 3 | Milic 2014 | pXRF (T1) | Cappadocia + Aegean | Göllü Dağ, Nenezi (+ Melos, Giali, Antiparos) | ~52 samples | Multi-source reference | ★★★★☆ key Cappadocian sources — **sheet fixed** (per-sample table, 9 elements) |
| 4 | Frahm & Hauck 2017 | Multi-method incl. pXRF (T1–T3) | Anatolia | Acıgöl, Bingöl, Göllü, Hasan, Meydan, Nenezi (+ Göllü cross-method sheet) | ~250 | Source + cross-method | ★★★★☆ ideal cross-method calibration reference |
| 5 | Frahm 2013 | pXRF / HHpXRF (T1) | *(verify — see §D7)* | **appears to be reference-glass standards** (Basalt_Glass…), not named obsidian sources | ~65 | verify | ★★★☆☆ may be instrument-validation data, not source data |
| 6 | Forster & Grave 2012 | pXRF (T1) | Cappadocia | Acıgöl, Nenezi | ~5 | Source reference | ★★★☆☆ pXRF but very small N |
| 7 | Carter & Shackley 2007 | EDXRF (T2) | Central Anatolia (Çatalhöyük) | Göllü Dağ, Nenezi | ~55 | Artifacts + sources | ★★★★☆ Cappadocian, near-pXRF |
| 8 | Carter et al 2017 | EDXRF (T2) | S Levant (Shaʿar Hagolan) | EGD, Göllü, Kaletepe, Kayırlı, Nemrut, Nenezi | ~35 | Levant artifacts + sources | ★★★★☆ |
| 9 | Carter et al 2013 (Körtik Tepe) | EDXRF (T2) | SE Anatolia | Bingöl B, Nemrut Dağ, Muş | 121 | Artifacts + sources | ★★★★☆ E Anatolian |
| 10 | Carter & Rosenberg 2022 (Tel Tsaf) | EDXRF (T2) | S Levant | beads + source samples: Bingöl, Göllü, Nemrut, Muş, Pasinler, Suphan | 25 + 45 | Levant beads + sources | ★★★★☆ |
| 11 | Carter et al 2006 | ICP-AES/MS (T3) | Cappadocia | Göllü Dağ, Nenezi | ~100 | Source reference | ★★★☆☆ non-pXRF — reference-only |
| 12 | Khalidi, Gratuze & Boucetta 2009 | LA-ICP-MS (T3) | E Anatolia | Bingöl, Meydan | ~24 | Source reference | ★★★☆☆ reference-only |
| 13 | Binder et al 2011 | LA-ICP-MS (T3) | Cappadocia | Göllü Dağ | ~10 | Source reference | ★★☆☆☆ reference-only |
| 14 | "Multiple" (Bressy 2005 / Poupeau 2010 / Carter 2006) | ICP-AES/MS, PIXE (T3) | Anatolia | Bingöl, Meydan, Nemrut, Nenezi, EGD | ~30 | Second-hand compilation | ★★☆☆☆ second-hand, reference-only |
| 15 | Yellin & Perlman 1980 | NAA (T4) | Anatolia + Levant | Göllü, Nenezi, Van; Beisamoun | ~12 | REE reference | ★★☆☆☆ different element suite (REE) |
| 16 | Yellin & Perlman 1981 | NAA (T4) | Anatolia | Göllü, Hasan, Nenezi, Nemrut, Van, Zincirkale | ~8 | REE reference | ★★☆☆☆ different element suite (REE) |
| 17 | Morgan 2015 | pXRF (T1) | Aegean (Melos) | Sta Nychia, Demenegaki, Giali | ~700 | Aegean sources | ★★☆☆☆ good method, but Melian sources don't reach the Levant |
| 18 | Rosen et al 2011 | Electron microprobe (T4) | major oxides | oxides only — no trace elements | ~18 | — | ★☆☆☆☆ not usable for trace-element sourcing |
| 19 | Acquafredda et al 2018 | XRF (T3) | Central Med / Aegean | Arci, Lipari, Palmarola, Melos, Yali | ~75 | Non-Levant sources | ★☆☆☆☆ wrong region for this study |

**Flags:**
- *Yellin & Maeir 2007* is listed in Section A as having a data table, but **no `Yellin and Maeir 2007` sheet exists in any workbook** — data location unconfirmed. Treat as article-only until a table is found.
- Ranking of *Morgan 2015* is low despite pXRF because its sources are **Melian (Aegean)** — obsidian that does not occur in Southern-Levant assemblages; useful only as a method/calibration comparison, not as a candidate source.

---

## A. Papers WITH data tables AND matching articles

*Legend — papers whose element tables were extracted **and** whose source
article text is on file, so every number can be traced back to its publication.
Columns: **Paper** · **Table Location** (workbook/sheet in `data/article_tables/`)
· **Article File** (text in `data/articles/`) · **Method** · **Units**.*

| Paper | Table Location | Article File | Method | Units |
|-------|---------------|--------------|--------|-------|
| Milic 2014 | `data1.xlsx`, `Milic 2014.xlsx` | `Milic_2014.txt` | pXRF | ppm |
| Campbell and Healey 2016 | `data1.xlsx`, `campbell and healey 1.xlsx`, `campbell and healey 2.xlsx` | `Campbell and Healey 2016.txt` | pXRF | ppm |
| Frahm 2013 | `data1.xlsx`, `Frahm 2013.xlsx` | `Frahm_2013.txt` | pXRF (HHpXRF) | ppm — Rb, Sr, Zr, Zn, Mn, Ti with error columns |
| Morgan 2015 | `data1.xlsx`, `Morgan 2015.xlsx` | `morgan_2015.txt` | pXRF | ppm |
| Schechter et al 2016 | `data1.xlsx`, `Schechter et al 2016.xlsx` | `Schechter_et_al_2016.txt` | pXRF | ppm |
| Khalidi, Gratuze & Boucetta 2009 | `data1.xlsx`, `Khalidi Gratuze Boucetta 2009.xlsx` | `khalidi Gratuze 2009.txt` | LA-ICP-MS | ppm |
| Frahm and Hauck 2017 | `data1.xlsx`, `Frahm and Hauck 2017.xlsx` | `Frahm and Hauck 2017.txt` | Mixed (comparison table of many techniques) | ppm |
| Carter and Shackley 2007 | `data2.xlsx` | `Carter_and_Shackley_2007.txt` | EDXRF | ppm |
| **Carter et al. 2013 (Körtik Tepe)** | `data2.xlsx` sheet `Carter et al 2013` (121 samples, KT.xxx) | `Carter_2013_Sourcing_obsidian_Kortik_Tepe.txt` | EDXRF | ppm — sources: Bingöl B, Nemrut Dağ, Muş. **Verified**: sample IDs & values match the article (see §D). Previously mislabelled "Kenan Tepe". |
| Carter et al. 2006 | `data2.xlsx` | `Carter_et_al_2006.txt` | ICP-AES/ICP-MS | mixed (oxides wt% + ppm) |
| Forster and Grave 2012 | `data2.xlsx` | `Forster_and_Grave_2012.txt` | pXRF | mixed (oxides wt% + ppm) |
| Yellin and Maeir 2007 | `data2.xlsx` | `Yellin_and_Maeir_2007.txt` | NAA (INAA) | ppm |
| Binder et al. 2011 | `data2.xlsx` | `Binder_et_al_2011.txt` | LA-ICP-MS | ppm |
| Rosen et al. 2011 | `data2.xlsx` | `Rosen_et_al_2011.txt` | Electron Microprobe | oxide wt% |
| Yellin and Perlman 1980 | `data2.xlsx` | `Yellin_and_Perlman_1980.txt` | NAA (INAA) | ppm |
| Yellin and Perlman 1981 | `data2.xlsx` | `Yellin_and_Perlman_1981.txt` | NAA | ppm |
| Poupeau et al. 2010 | `data2.xlsx` | `Poupeau_et_al_2010.txt` | PIXE | ppm/wt% |
| Carter et al. 2017 | `data2.xlsx` | `Carter_2017_Investigating_Pottery_Neolithic_Shaar_Hagolan.txt` | EDXRF | ppm |
| Rosenberg, Carter et al. 2022 | `Carter_Rosenberg_2022_Tel_Tsaf.xlsx` | `Carter_2022_Obsidian_Beads_Tel_Tsaf.txt` | EDXRF | ppm |
| Acquafredda et al. 2018 | `data2.xlsx` | `Acquafredda_et_al_2018.txt` | XRF | ppm — Italian/Sardinian sources (Arci, Palmarola, Lipari, Pantelleria) |

## B. Papers WITH data tables but NO matching article in `data/articles/`

*Legend — papers whose data (or a reference to it) appears in the xlsx files but
whose original article text is **not** on file. Subdivided by how this affects
traceability: name-only references (no data, harmless), data traceable via a
containing article you do have (acceptable), and papers dropped from the
reference set.*

**B1 — Name-only methodological references (`Indicative Elements` sheet; no data rows):**

*These appear only as citations in the "which elements are diagnostic" methodology
sheet — none contribute source data. Craig, Sheppard, Moholy-Nagy and Nazaroff are
from **non-Mediterranean contexts** (Pacific / Mesoamerican / general method) and are
**irrelevant to this study — safe to remove**. Delerue is retained (it concerns the
Mallaha/Einan site) but is name-only and needs verification.*

| Paper | Region / relevance | Disposition |
|-------|--------------------|-------------|
| Craig et al 2007 | General method, non-Mediterranean | **Irrelevant — remove** |
| P.J. Sheppard et al. 2011 | Pacific obsidian | **Irrelevant — remove** |
| Moholy-Nagy et al. 2013 | Mesoamerican obsidian | **Irrelevant — remove** |
| Nazaroff et al. 2010 | Method reference, non-Mediterranean | **Irrelevant — remove** |
| Delerue 2007 ("Delerou") | Mentioned in DObsiSS for Mallaha/Einan site | Keep (name-only; verify) |

**B2 — Data present, but traceable via another article you have (no standalone paper needed):**

| Paper | Table Location | Method | Traceable via |
|-------|---------------|--------|---------------|
| Bressy et al. 2005 | `data2.xlsx` `Multiple` sheet | ICP-AES/ICP-MS | Reproduced in **Forster & Grave 2012** (compilation "From Forster 2012"). Second-hand — Tier 3, reference-only. |
| Kelle & Seifried 1990 | `data2.xlsx` `Frahm & Hauck 2017 – Göllü Dağ` sheet | WDXRF | Reproduced in **Frahm & Hauck 2017** cross-method table. |

**B3 — Removed (no data of its own):**

| Paper | Notes |
|-------|-------|
| Frahm 2014 | Sheet **deleted from `data2.xlsx`** — it held only provenance values reproduced from other articles, no original data. Article (`Frahm_2014.txt`) confirmed: Bronze Age blade production, not a source-characterisation study. |

**B4 — Dropped from the reference set (excluded from all analysis):**

| Paper | Reason |
|-------|--------|
| Oddone et al. 1997 | No article available; data will not be used. |
| Yellin et al. 1996 | No matching article could be found; data will not be used. |
| Gratuze 1999 | Sheet is empty (no data) and no article. |
| Ozdemir et al. 2006 | Claimed Nemrut LA-ICP-MS data, but no confirmed data rows located and no article — treat as absent unless a table is found. |

## C. Articles in `data/articles/` with NO corresponding data table

*Legend — article texts on file that are **not** yet linked to any extracted
table. Candidates for new extraction (or confirmation that they hold no usable
geochemical data).*

| Article File | Likely Content |
|-------------|---------------|
| `Obsidian_and_the_Origins_of_Trade.txt` | Trade patterns — may not have extractable tables |
| `Bruker_Obsidian_Report.txt` | pXRF accuracy assessment — may have reference values |
| `Historyberkley.txt` | XRF history — may have reference data |
| `Hancock_and_Carter_2010.txt` | Accuracy assessment across methods — **may have comparative tables** |
| `Freund_KP_2013_An_assessment_of_the.txt` | Review paper — may reference key datasets |
| `Carter_T_2014_The_contribution_of_obsid.txt` | Review — may overlap with other Carter papers |
| `Carter_contribution_of_obsidian_characterization.txt` | Likely duplicate of `Carter_T_2014` above |
| `URMIA_Iran.txt` | WDXRF data from Lake Urmia — **likely has extractable tables** |
| `Binder_2007_PPN5.txt` | PPN analysis |
| `Chap_6_Chabot-Pelegrin.txt` | Book chapter |
| `Sesto_Italy.txt` | Italian obsidian |
| `Timor.txt` | Not relevant to Eastern Med |
| `Balkan-Atli_N_Kuhn_S_Astruc_L_Kayacan_gollu_dag_survey.txt` | Göllü Dağ survey — **may have source data** |
| `Carter_et_al_2008.txt` | Bingöl/Nemrut at Çatalhöyük; EDXRF — **likely has extractable tables** |
| `Carter_2013_Orange_Sourcing_obsidian_Tell_Aswad_Syria.txt` | Tell Aswad & Qdeir 1 (Syria); SEM-EDS and EDXRF — **likely has extractable tables** |
| `JARMT.txt` | Agent-based modelling of obsidian exchange; Ortega et al. 2013 — methodological, likely no raw data |
| `Yellin_and_Garfinkel_1986.txt` | PPNB Yiftahel (Israel) obsidian sourcing; NAA — **likely has extractable tables** |
| Hebrew articles (5 files) | Various — check for tables |

*Note: `Carter_2013_Sourcing_obsidian_Kortik_Tepe.txt` was previously listed here
but is now matched to its data table (see Section A).*

---

## D. Data Quality Issues Found

*Legend — specific data-quality problems in the source spreadsheets that must be
handled before or during extraction.*

1. **Removed sheets**: `Frahm 2014`, `Gratuze 1999`, and `Yellin et al 1996` sheets have been **deleted from `data2.xlsx`** (no original data / dropped — see §B). `data2.xlsx` now holds 12 sheets. The `Oddone et al. 1997` sheet remains in the workbook but is **excluded** from the reference set (no article; see §B4). *(Note: Excel trimmed empty trailing rows on save — e.g. `Yellin and Perlman 1981` 38→10 rows — no data was lost, verified.)*
2. **Incomplete reference**: "Delerou" in `data1.xlsx` — likely "Delerue 2007".
3. **Corrected mislabel — `Carter et al 2013` sheet is Körtik Tepe, not Kenan Tepe**: the sheet's sample IDs are `KT.002 … KT.119`, which match the Körtik Tepe article (`Carter_2013_Sourcing_obsidian_Kortik_Tepe.txt`; 204 `KT.0xx` codes). The string "Kenan" appears in **no cell of any workbook**. The earlier "Kenan Tepe" attribution was an error and has been corrected in Section A. **Extraction cleanups for this sheet**: (a) the `Source` field is split across 3 columns and has encoding corruption — `Nemrut | Da_x0002_g` → "Nemrut Dağ", `Muş | e | Konuk` → rejoin; (b) drop the stray final row `Bekle` (a text fragment, no data). Spot-check verified: KT.002 → Rb 230, Sr 46, Zr 329, Nb 22, Bingöl B (exact match to article).
4. **Encoding**: `Obsidian Sources List.xlsx` has garbled characters (Agicšl, GollŸ Dag) — Turkish characters corrupted.
5. **Complex layout**: `Carter et al. 2006` in `data2.xlsx` has ~102 rows and many NaN columns — the table structure may be misaligned; verify alignment.
6. **`Milic 2014` — FIXED**: the side-by-side layout was restructured into a stacked sheet — a per-source summary (rows 1–15) plus a **per-sample table with a proper header** (`Source, Ti, Mn, Fe, Zn, Rb, Sr, Zr, Ba, Pb`, rows 19–71). The redundant means-only block and the standalone `Milic 2014.xlsx` were removed. **Use the per-sample block** as canonical (avoids the range strings, which now live only in the summary block). *Residual (low priority, Carpathian only — not a Levant source)*: `Carpathian 1/2` labels sit in 2 cells, and 3 Carpathian-2 Fe values are split across cells (`11671→11|671`, r63/69/70).
7. **Frahm 2013 (`data1.xlsx`)**: has element+`Error` column pairs and section labels like `Basalt_Glass`; the rows look like **measurements of reference glasses/standards, not named obsidian sources**. Verify against `Frahm_2013.txt` whether it contributes any source data before using it (relevance may drop).

---

## E. Analytical Method Comparability for pXRF

*Legend — how each analytical method compares to your pXRF samples, and the
resulting comparability tiers. **This tier table is the authoritative
method→tier mapping**; the pipeline must follow it exactly (the previous
analysis failed because its code diverged from this — see
`prior_work_audit_made_with_github_copilot.md`).*

### Can you directly compare values across methods?

**Short answer: NOT always. It depends on the element and the method.**

### Method categories in your data:

| Method | Papers Using It | Measures | Directly Comparable to pXRF? |
|--------|----------------|----------|------------------------------|
| **pXRF** | Milic 2014, Campbell & Healey 2016, Frahm 2013, Morgan 2015, Schechter et al 2016, Forster & Grave 2012 | Trace elements in ppm | **YES** — same method family, BUT instrument calibration matters |
| **EDXRF** (lab) | Carter & Shackley 2007, Carter et al 2013 (Körtik Tepe), Carter et al 2017 | Trace elements in ppm | **Mostly yes** for trace elements (Rb, Sr, Zr, Nb, Y, Fe). Lab EDXRF is more precise but measures the same physics |
| **NAA / INAA** | Yellin & Perlman 1980/1981, Yellin & Maeir 2007 | REE + trace elements in ppm | **Limited** — NAA measures different elements (La, Ce, Nd, Sm, Eu, Yb). Overlap only on some elements (Fe, Rb) |
| **LA-ICP-MS** | Khalidi et al 2009, Binder et al 2011 | Trace elements in ppm | **Partially** — measures same elements but different matrix effects. Values can differ systematically |
| **ICP-AES/ICP-MS** | Carter et al 2006, Bressy et al 2005 | Oxides (wt%) + trace (ppm) | **For trace ppm: partially**. Oxides need conversion. Destructive method — different sample prep |
| **PIXE** | Poupeau et al 2010 | Trace elements in ppm | **Limited** — different excitation physics, values may differ |
| **WDXRF** | Kelle & Seifried 1990, URMIA article | Trace elements in ppm | **Mostly yes** — same physics as EDXRF, higher precision |
| **Electron Microprobe** | Rosen et al 2011 | Oxides in wt% | **NO** — measures major oxides only, not trace elements |

### Recommendation for your pXRF dataset:

**Tier 1 — Directly comparable (use these first):**
- Milic 2014 (pXRF, ppm)
- Campbell & Healey 2016 (pXRF, ppm)
- Frahm 2013 (pXRF, ppm)
- Morgan 2015 (pXRF, ppm)
- Schechter et al 2016 (pXRF, ppm)
- Forster & Grave 2012 (pXRF, ppm for trace elements)

**Tier 2 — Comparable with caution (same elements, similar method):**
- Carter & Shackley 2007 (lab EDXRF)
- Carter et al 2013 — Körtik Tepe (lab EDXRF)
- Carter et al. 2017 (EDXRF)
- Frahm & Hauck 2017 (multi-method comparison — use their pXRF values)
- Kelle & Seifried 1990 (WDXRF, via Frahm & Hauck 2017)

**Tier 3 — Use for reference patterns only (different method, values may differ):**
- LA-ICP-MS papers (Khalidi, Binder)
- ICP-AES/MS papers (Carter et al 2006, Bressy et al 2005)
- PIXE (Poupeau et al 2010)

**Tier 4 — Different element suites, not directly comparable:**
- NAA/INAA papers (Yellin & Perlman, Yellin & Maeir — measure REE, not the same trace elements as pXRF)
- Electron Microprobe (Rosen et al 2011 — major oxides only)

### Key insight from Frahm & Hauck 2017:
Your `Frahm and Hauck 2017.xlsx` "Gollu Dag" sheet is exactly the cross-method comparison you need — it lists Göllü Dağ values measured by WDXRF, NAA, ICP-AES/MS, pXRF, LA-ICP-MS, and EDXRF side by side. **This table directly answers your comparability question for Göllü Dağ source data** and is the right basis for any cross-method calibration check.

### What about unit differences?
- **ppm vs ppm**: Directly comparable (just watch for calibration offsets)
- **Oxide wt% vs ppm**: Need conversion. E.g., Fe2O3 wt% → Fe ppm requires: Fe(ppm) = Fe2O3(wt%) × 6993.5
- **Range values** (like in Milic 2014): Use the mean values for comparison

---

## F. Priority Actions

*Legend — recommended follow-up tasks, ordered by priority.*

1. ~~Reconcile Milic 2014~~ — **DONE** (§D6). Optional: repair the Carpathian split cells (low priority — not a Levant source).
2. **Clean the Körtik Tepe (`Carter et al 2013`) sheet** — `data2.xlsx`: rejoin/repair the `Source` column (`Bingöl|B`, `Nemrut|Da_x0002_g`→Nemrut Dağ, `Muş|e|Konuk`) and drop the `Bekle` junk row (see §D3). *Relevant — E Anatolian sources.*
3. **Verify Frahm 2013** (`data1.xlsx`) — confirm whether it holds obsidian-source data or only reference-glass standards (see §D7).
4. **Verify `Carter et al 2006`** (`data2.xlsx`) — 109-col, 33%-filled layout; header not in row 0, needs reconstruction (Tier 3 reference-only — lower priority).
5. **Tidy the `Multiple` sheet** (`data2.xlsx`) — author/source names split across cells (`Bressy|et|al.,|2005`, `East Golu Da[ğ]`); second-hand Tier 3, low priority.
6. **Fix encoding** in `Obsidian Sources List.xlsx` (Agicšl → Acıgöl) *if that external file is used*.
7. **Optionally extract** tables from unlinked articles (§C): `Carter_et_al_2008.txt`, `Carter_2013_Orange...Tell_Aswad...txt`, `Yellin_and_Garfinkel_1986.txt`, `URMIA_Iran.txt`, `Balkan-Atli...gollu_dag_survey.txt`.
8. **Build the master pXRF-comparable table** starting from Tier 1 papers first, adding Tier 2/3 only as clearly-labelled reference-only rows.

**Sheets confirmed clean (no fix needed):** Campbell & Healey source sheets + `Kenan sources assignments`, Frahm & Hauck `MAIN`, Schechter 2016, Carter & Shackley 2007, Carter 2017, Carter/Rosenberg 2022.

*Resolved / dropped since first draft:* Kenan Tepe "missing article" — was a mislabel; the data is Körtik Tepe and its article is on file. Oddone 1997, Yellin et al. 1996, Gratuze 1999 — dropped (§B4). Morgan 2015 & Acquafredda 2018 articles — now on file (§A).

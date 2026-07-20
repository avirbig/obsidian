# Pre-Phase-1 Inventory: All xlsx Sheets & Extraction Notes

Generated: 2026-03-25  
Purpose: Full map of every xlsx sheet — its content, element columns, row counts,
known issues, and what needs to happen in notebook 01_data_extraction.ipynb.

---

## LEGEND

| Symbol | Meaning |
|--------|---------|
| ✅ | Ready to extract — clean structure |
| ⚠️ | Needs special handling (see notes) |
| ❌ | Cannot extract — empty or non-chemical content |
| 🔁 | Duplicate of data in another file |

For each file, **relevant sheets** = sheets with trace-element ppm/oxide data.
**Skip sheets** = morphology, metadata, or non-geochemical content.

---

## 1. `Campbell and healey 2.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Sheet1 | 911 | 15 | ❌ Morphology/typology | Skip — no geochemical data |

**Note**: Contains Reference number, Trench, Locus, Length, Width, Thickness, Weight, Notes.
No source geochemistry here. The geochemistry for Campbell & Healey is in `campbell and healey 1.xlsx`.

---

## 2. `Carter_Rosenberg_2022_Tel_Tsaf.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Table5_Bead_Measurements | 24 | 13 | ✅ Archaeological samples | Extract — bead measurements per sample |
| Table6_Source_Samples | 44 | 11 | ✅ Source reference data | Extract — source reference data |

**Elements present**: Mn, Fe, Zn, Ga, Rb, Sr, Y, Zr, Nb, Th  
**Method**: EDXRF (Tier 2)  
**Paper**: Rosenberg, Rizzutto, Klimscha & Carter 2022 → `Carter_2022_Obsidian_Beads_Tel_Tsaf.txt`  
**Source labels in file**: Already clean source names expected (EGD, Bingöl, etc.)  
**Special notes**: `Table5` has a `Stat` column (mean/SD per sample?) — check structure carefully.

---

## 3. `Frahm 2013.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| גיליון1 (Sheet1) | 67 | 12 | ✅ Source/site measurements | Extract |

**Elements present**: Zr (±error), Sr (±error), Rb (±error), Zn (±error), Mn (±error), Ti  
**Method**: pXRF — HHpXRF, "off-the-shelf" handheld Bruker (Tier 1)  
**Paper**: Frahm 2013 (JAS 40:1080–1092) → `Frahm_2013.txt` ✅ article now available  
**Special notes**: Error columns present alongside values — keep both (`Rb`, `Rb_err`, etc.).
Paper is a validity test of pXRF on Göllü Dağ debitage (Tell Mozan, Syria). 94–100% source assignment success rate. Data = actual measurements of Göllü Dağ-sourced artefacts, not geological source reference samples.
Header row is in Hebrew sheet tab. Column `Point` = sample identifier.

---

## 4. `Frahm and Hauck 2017.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| MAIN | 252 | 7 | ✅ Multi-source measurements | Extract |
| Frahm and Hauck 2017-Gollu Dag | 17 | 7 | ✅ Cross-method comparison | Extract separately |

**Elements present (MAIN)**: Source, Specimen, Nb, Zr, Sr, Rb, Fe  
**Method**: Mixed — see `method` column; includes pXRF, WDXRF, NAA, LA-ICP-MS, EDXRF  
**Paper**: Frahm & Hauck 2017 → no matching article txt yet  
**Special notes**:
- MAIN sheet: must tag each row with its method from the `Technique`/source column
- Gollu Dag sheet: This is the cross-method comparison table — **highly valuable**. Each row is a reference (different paper/technique) measuring Göllü Dağ. Columns Nb, Zr, Sr, Rb, Fe each appear twice (mean + SD or two values). Parse carefully.

---

## 5. `Khalidi Gratuze Boucetta 2009.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| גיליון2 (Sheet2) | 4 | 24 | ✅ Source statistical summary | Extract |
| גיליון1 (Sheet1) | 23 | 4 | ⚠️ Oxide% data, partial | Extract with conversion |

**Elements present (Sheet2)**: Li, B, Ca, Ti, Fe, Mn, Zn, As, Rb, Sr, Y, Zr, Nb, Cs + more  
**Method**: LA-ICP-MS (Tier 3)  
**Paper**: Khalidi, Gratuze & Boucetta 2009 → `khalidi Gratuze 2009.txt`  
**Special notes**:
- Only 4 data rows (Sheet2) — likely source means/ranges, not individual measurements
- Sheet1: Oxide% format for Bingöl_A, Bingöl_B, Meydan_Dağ — need oxide→ppm conversion for Fe, Mn if used
- `Oxide` column = row labels (element names)

---

## 6. `Milic 2014.xlsx` (standalone file)

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| גיליון1 (Sheet1) | 15 | 4 | ⚠️ Source summary, range strings | Extract with parsing |

**Elements present**: Source, Rb (ppm), Sr (ppm), Zr (ppm)  
**Method**: pXRF (Tier 1)  
**Paper**: Milic 2014 → no matching article txt yet  
**Special notes**:
- Only 3 elements (Rb, Sr, Zr) — limited but key discriminators
- Values may be range strings ("166-194") → parse to midpoint, preserve original
- 15 rows = 15 source entries (mean summary per source)

---

## 7. `Morgan 2015.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Table1 | 714 | 17 | ✅ Individual measurements | Extract |
| Table2 | 714 | 9 | ✅ Metadata (site, source) | Join to Table1 on Analysis ID |
| Combine | 673 | 18 | 🔁 Subset of Table1+2 merged | Skip — use Table1+Table2 instead |
| Dhemenegaki | 84 | 17 | ✅ Aegean source subset | Extract |
| Sta Nychia | 588 | 17 | ✅ Aegean source subset | Extract |

**Elements present**: Ba, Ti, Mn, Fe, Co, Ni, Cu, Zn, Ga, Pb, Th, Rb, Sr, Y, Zr + more  
**Method**: pXRF (Tier 1)  
**Paper**: Morgan 2015 → no matching article txt yet  
**Special notes**:
- Table1 and Table2 must be joined on `Analysis ID` to get source assignments
- Three separate source populations: general dataset + Dhemenegaki + Sta Nychia (Greek/Aegean sources — not relevant to Near East, but include with `region=Aegean` tag)
- 714 rows is large — check for duplicates between Table1 and Combine

---

## 8. `Schechter et al 2016.xlsx` (standalone file)

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| גיליון1 (Sheet1) | 101 | 12 | ✅ Individual measurements | Extract |

**Elements present**: Mn, Fe, Zn, Ga, Th, Rb, Sr, Y, Zr, Nb, Source  
**Method**: pXRF (Tier 1)  
**Paper**: Schechter et al. 2016 → no matching article txt yet  
**Special notes**:
- Column headers use XRF line notation (`RbKa1`, `SrKa1`, etc.) → rename to `Rb`, `Sr`, etc.
- 101 rows of individual measurements — good sample size
- `ID #` = sample identifier

---

## 9. `campbell and healey 1.xlsx`  ← PRIMARY Campbell & Healey file

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Kenan sources assignments v3 | 911 | 18 | ✅ Individual measurements | Extract |
| Nemrut Dağ Bingöl A | 5 | 18 | ✅ Source samples (NemrutDag/BingolA) | Extract |
| Nemrut Dağ | 340 | 18 | ✅ Source samples | Extract |
| Muş | 3 | 18 | ✅ Source samples (Muş) | Extract (small, flag n<5) |
| Meydan Dağ | 6 | 18 | ✅ Source samples | Extract |
| Group 3d | 279 | 18 | ✅ Source samples | Extract |
| Bingöl A | 123 | 18 | ✅ Source samples | Extract |
| Bingöl B | 123 | 18 | ✅ Source samples | Extract |

**Elements present**: Al, Si, K, Ca, Ti, Mn, Fe, Zn, Rb, Sr, Y, Zr + more (18 cols incl. metadata)  
**Method**: pXRF (Tier 1)  
**Paper**: Campbell & Healey 2016 → no matching article txt yet  
**Special notes**:
- `Kenan sources assignments` = archaeological site data (Kenan Tepe) — includes source assignments
- Other sheets = geological source reference measurements (very valuable, large n)
- **This is one of the richest Tier 1 source datasets** — Bingöl A (n=123), Bingöl B (n=123), Nemrut Dağ (n=340)
- `Group 3d` = unknown source group (n=279) — investigate what this is

---

## 10. `data1.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Indicative Elements | 12 | 17 | ⚠️ Reference comparison table | Extract as lookup table only |
| General Info | 27 | 9 | ⚠️ Paper metadata | Extract as metadata, not measurements |
| Schechter et al 2016 | 101 | 12 | 🔁 Duplicate of standalone file | Skip — use standalone xlsx |
| Milic 2014 | 41 | 18 | ⚠️ Side-by-side layout | Extract with care — see notes |
| Morgan 2015 | 5 | 17 | ⚠️ Summary only (5 rows) | Extract as source summary |
| Frahm 2013 | 67 | 13 | 🔁 Duplicate of standalone file | Skip — use standalone xlsx |
| Khalidi Gratuze Boucetta 2009 | 4 | 24 | 🔁 Duplicate | Skip — use standalone xlsx |
| Frahm and Hauck 2017-Gollu Dag | 17 | 7 | 🔁 Duplicate | Skip — use standalone xlsx |
| Campbell and Healey 2016 | 11 | 16 | ⚠️ Summary only (11 rows) | Extract summary statistics only |

**Special notes for Milic 2014 in data1.xlsx**:
- 41 rows, 18 cols with empty column headers — side-by-side table layout
- Columns repeat (Source, Rb, Sr, Zr appear twice) — split into two separate sub-tables
- Range strings expected — parse to midpoints

---

## 11. `data2.xlsx`

| Sheet | Rows | Cols | Type | Action |
|-------|------|------|------|--------|
| Frahm 2014 | 0 | 0 | ❌ Empty | Skip (confirmed: paper has no source tables) |
| Carter and Shackley 2007 | 56 | 15 | ✅ Individual measurements | Extract |
| Oddone et al. 1997 | 14 | 3 | ⚠️ Transposed, 3 source cols | Extract with transpose |
| Carter et al. 2017 | 35 | 13 | ✅ Individual measurements | Extract |
| Acquafredda et al. 2018 | 76 | 9 | ✅ Italian/Sardinian sources | Extract (Aegean/Italian — tag region) |
| Forster and Grave 2012 | 5 | 15 | ⚠️ Only 5 rows (summary) | Extract, flag low n |
| Multiple | 31 | 1 | ⚠️ Mixed/commentary | Read manually — label unclear |
| Carter et al 2013 | 121 | 14 | ✅ Individual measurements | Extract |
| ROSEN et al 2011 | 19 | 3 | ⚠️ Transposed, oxide format | Extract with transpose + conversion |
| Yellin and Perlman 1980 | 12 | 4 | ⚠️ Transposed, sources as cols | Extract with transpose |
| Yellin et al 1996 | 8 | 3 | ⚠️ Transposed, sources as cols | Extract with transpose |
| Carter et al. 2006 | 101 | 35 | ⚠️ Complex 35-col layout | Extract carefully — 101 rows of data |
| Yellin and Perlman 1981 | 18 | 4 | ⚠️ Transposed, merged headers | Extract with transpose |
| Gratuze 1999 | 0 | 0 | ❌ Empty | Skip (PDF not available) |
| Binder et al. 2011 | 9 | 2 | ⚠️ Mixed oxide%+ppm format | Extract with unit handling |

**Elements in Carter and Shackley 2007**: Ti, Mn, Fe, Zn, Ga, Th, Rb, Sr, Y, Zr, Nb + ratio cols Nb/Zr, Y/Zr  
**Elements in Carter et al. 2017**: Ti, Mn, Fe, Rb, Sr, Y, Zr, Nb, Ba, Pb, Th  

---

## Summary: Extraction Priority Order

### Tier 1 (pXRF) — Extract first

| File | Sheet(s) | Rows | Status |
|------|----------|------|--------|
| `campbell and healey 1.xlsx` | Source sheets | ~880 source rows | ✅ Ready |
| `Schechter et al 2016.xlsx` | Sheet1 | 101 | ✅ Rename headers only |
| `Frahm 2013.xlsx` | Sheet1 | 67 | ✅ Keep error cols |
| `Morgan 2015.xlsx` | Table1+Table2 | 714 | ✅ Join on Analysis ID |
| `Milic 2014.xlsx` | Sheet1 | 15 | ⚠️ Parse range strings |
| `data1.xlsx` Milic sheet | Milic 2014 | 41 | ⚠️ Split side-by-side layout |

### Tier 2 (EDXRF) — Extract second

| File | Sheet(s) | Rows | Status |
|------|----------|------|--------|
| `data2.xlsx` Carter & Shackley | Sheet | 56 | ✅ Ready |
| `data2.xlsx` Carter et al. 2017 | Sheet | 35 | ✅ Ready |
| `data2.xlsx` Carter et al. 2013 | Sheet | 121 | ✅ Ready |
| `Carter_Rosenberg_2022_Tel_Tsaf.xlsx` | Table5+6 | 68 | ✅ Ready |

### Tier 3 (LA-ICP-MS / PIXE / WDXRF) — Extract third

| File | Sheet(s) | Rows | Status |
|------|----------|------|--------|
| `Khalidi Gratuze Boucetta 2009.xlsx` | Sheet2 | 4 | ⚠️ Summary only |
| `Frahm and Hauck 2017.xlsx` | MAIN + Gollu Dag | 252+17 | ⚠️ Mixed methods — tag per row |
| `data2.xlsx` Forster & Grave 2012 | Sheet | 5 | ⚠️ Low n, oxide format |
| `data2.xlsx` Binder et al. 2011 | Sheet | 9 | ⚠️ Mixed oxide+ppm |

### Tier 4 (NAA / Microprobe) — Extract last, reference-only

| File | Sheet(s) | Rows | Status |
|------|----------|------|--------|
| `data2.xlsx` Yellin & Perlman 1980 | Sheet | 12 | ⚠️ Transposed |
| `data2.xlsx` Yellin & Perlman 1981 | Sheet | 18 | ⚠️ Transposed, merged header |
| `data2.xlsx` Yellin et al. 1996 | Sheet | 8 | ⚠️ Transposed |
| `data2.xlsx` ROSEN et al 2011 | Sheet | 19 | ⚠️ Oxides, transposed |
| `data2.xlsx` Oddone et al. 1997 | Sheet | 14 | ⚠️ Transposed |

### Skip / Non-geochemical

| File | Sheet(s) | Reason |
|------|----------|--------|
| `Campbell and healey 2.xlsx` | Sheet1 | Morphology/typology only |
| `data2.xlsx` Frahm 2014 | Empty | Confirmed no tables |
| `data2.xlsx` Gratuze 1999 | Empty | PDF unavailable |
| `data2.xlsx` Multiple | Unclear | Read manually first |
| `data1.xlsx` duplicates | Various | Use standalone files instead |

---

## Special Issues Requiring Manual Attention

1. **`data2.xlsx` → Acquafredda et al. 2018**: Italian/Sardinian obsidian (Arci source) — not Anatolian. Extract but tag `region=Italian/Sardinian`. May still be useful to exclude these sources from biplots.

2. **`campbell and healey 1.xlsx` → `Group 3d` (n=279)**: Large unidentified group. What is "Group 3d"? Check article for definition before assigning a source label.

3. **`data2.xlsx` → Carter et al. 2006 (35 cols, 101 rows)**: Very wide table — the first 15 column headers all came back empty from the scan, suggesting complex merged/nested headers at the top. This will need careful manual inspection.

4. **`Khalidi Gratuze Boucetta 2009.xlsx` → Sheet1**: `Oxide` column is used as row labels. The data is transposed (elements as rows, sources as columns). Only 4 data rows in Sheet2 — these are likely source means across multiple measurements, not individual analyses.

5. **`Frahm and Hauck 2017.xlsx` → Gollu Dag sheet**: Columns Nb through Fe each appear twice (likely mean + SD). Need to confirm which column is which from article before extracting.

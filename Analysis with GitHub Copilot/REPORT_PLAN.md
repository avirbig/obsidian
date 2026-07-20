# Final Obsidian Provenance Report — Plan

**Status**: In progress  
**Target output**: `outputs/reports/final_report.pdf` (Markdown → pandoc → PDF)  
**Language**: English  
**Audience**: Colleagues/supervisors with no statistics background  
**Style**: Draft paper (will be submitted to a journal later)  
**Code**: Hidden  

---

## Decisions

| Topic | Decision |
|---|---|
| Language | English |
| Format | PDF via Markdown + pandoc |
| Audience | No stats background — all methods explained plainly |
| Code | Hidden |
| GolluDag / EGD | Keep as two separate labels, explain they are same volcano (statistical artifact) |
| Group3d `yif_` (no basket) | **Excluded from all plots**, flagged as unreliable in §7e text |
| yif_10671 (BingolA) | Own sub-section §7d as a new finding |
| Calibration | Prominent dedicated section §6b |
| Bibliography | Full, all articles used for reference DB |
| Archaeological context | Minimal — focus on geochemistry |

---

## Report Structure

### 1. Title + Authors

### 2. Abstract (~200 words)

### 3. Introduction
- What pXRF obsidian sourcing is
- The three sites (Motza EPPNB, Einan/Ain Mallaha Natufian, Yiftahel MPPNB)
- Research goals and questions

### 4. Materials
- 507 obsidian samples from 3 sites (+ 3 flint excluded below)
- Instrument: Niton XL3t pXRF, Mining Cu/Zn mode, 60-second readings
- Two readings per item (dorsal and ventral surfaces), averages computed
- Quality flags: `repeat_divergent`, missing Rb/Nb

### 5. Reference Database
- Which source articles were used and why
- Method tiers (Tier 1 = pXRF, Tier 2 = EDXRF, Tier 3 = LA-ICP-MS, Tier 4 = NAA)
- 9 Levant-relevant Tier-1 sources
- **Table 1**: Reference DB summary — Source | N | Mean Rb | Mean Zr | Mean Nb

### 6. Methods

#### 6a. Data Cleaning
- Duplicate handling, LOD assignment, `repeat_divergent` flag explanation

#### 6b. Calibration and Instrument Offset *(prominent section)*
- Rb systematic under-read ~×2 vs published pXRF references (empirically derived from EGD comparison)
- Y not measured in Mining mode
- Sr mostly below LOD
- Consequence: Zr and Nb are the primary attribution elements; Rb used only as secondary check (scaled ×2)
- Recommended future validation: measure against known-provenance standards

#### 6c. Biplot Visualization *(explained from scratch)*
- What a biplot shows and how to read it
- 95% confidence ellipses from reference data

#### 6d. Mahalanobis Distance *(layman explanation + formula)*
- What it measures (distance in units of standard deviations, accounting for correlations)
- Two-element PRIMARY (Zr, Nb) and three-element SECONDARY (Rb×2, Zr, Nb) attribution
- Chi-squared threshold at 95% confidence (df=2 → 5.991; df=3 → 7.815)
- How confident/unconfident attributions are flagged

#### 6e. PCA *(layman explanation)*

#### 6f. K-means Clustering *(layman explanation)*

#### 6g. Hierarchical Clustering *(layman explanation)*

---

### 7. Results

#### 7a. Internal Structure of Assemblage
- PCA, k-means, dendrogram results
- What clusters emerged and their correspondence to reference sources

#### 7b. Source Attribution Summary
- **Table 2**: Attribution counts per source per site  
  (columns = EGD, GolluDag, BingolA, BingolB, NemrutDag, WGD, ND; rows = Motza, Einan, Yiftahel, Total)
- Per-site brief summaries

#### 7c. GolluDag vs EGD Split Explanation
- Both refer to Göllü Dağ East (same volcano, Cappadocia, Turkey)
- Split is a statistical artifact of mixing LA-ICP-MS (EGD reference, N=63, artificially tight ellipse) and pXRF (GolluDag reference, N=25, wider cloud)
- In interpretation: treat as "Göllü Dağ complex"

#### 7d. New Finding: yif_10671 — BingolA Attribution
- Only confident Bingöl A attribution in the entire assemblage
- Rb=100 ppm (×2 → ~200), Zr=1005 ppm, Nb=65 ppm — dramatically different from EGD cluster
- Significance: long-distance procurement from eastern Anatolia (Bingöl, Lake Van region)
- Yiftahel MPPNB context

#### 7e. Unreliable Item: `yif_` (no basket number)
- Attributed to Group3d (unknown geological location, very high Rb ~462 ppm published)
- Our reading: Rb=82.5, Zr=205, Nb=27.5 — flagged `repeat_divergent`, 2el/3el disagree
- Excluded from all plots and attribution counts
- Reason: no basket number → cannot link to excavation context; geochemically suspicious

#### 7f. Non-Obsidian Items — Excluded from Analysis *(from anomaly screen)*

**5 confirmed non-obsidian items** excluded from all attribution counts and plots. One additional ambiguous case noted separately.

| Item ID | Site | Locus | Basket | Material label | Reason for exclusion |
|---|---|---|---|---|---|
| `ein_` (no basket) | Einan | — | — | "Chert" / "flint?" | Explicitly labelled as chert; no Rb/Zr/Nb signal; no basket → unprovenanced |
| `mot_41350` | Motza | 4080 | 41350 | "flint?" | Explicitly labelled; no Rb/Zr/Nb signal; high Si (431,658 ppm) consistent with flint/chert |
| `mot_50683` | Motza | 5060 | 50683 | "flint?" | Explicitly labelled; no Rb/Zr/Nb signal; high Si (516,545 ppm) consistent with flint/chert |
| `mot_50633` | Motza | 5060 | 50633 | "obsidian" | Described as "light green"; no Rb/Zr/Nb signal; Ca=102,320 ppm; Fe=30,945 ppm; high Si — not volcanic glass |
| `mot_40878` | Motza | 4032 | 40878 | "obsidian" | Described as "light green"; no Rb/Zr/Nb signal; Ca=55,875 ppm (SD=43,989 — readings wildly inconsistent); high Si — not volcanic glass |

**Ambiguous case — `mot_40816` (Motza, locus 4050, basket 40816)**:
- 4 readings from 2017-08-07/09 (readings 852–855): normal obsidian chemistry (Rb~85, Zr~62, Nb=20, Ca<11,000 ppm)
- 2 readings from 2018-02-21 (readings 1759–1760, described as "green"): zero Rb, zero Zr, Ca>101,000 ppm — identical to `mot_50633`/`mot_40878`
- Both 2018 readings cover opposite faces (ventral + dorsal) of what was logged as the same artifact, yet show zero signal on both — this is inconsistent with a surface weathering explanation
- **Most likely interpretation**: a second, physically different green non-obsidian object was inadvertently measured in the 2018 session and logged under the same basket number. The original `mot_40816` (4 × 2017 readings) is genuine obsidian.
- **Treatment**: `mot_40816` retained as obsidian but its averaged values are contaminated by the 2018 readings. Attribution computed from 2017-only readings (Rb=87.5, Zr=62.5, Nb=20). Flag in footnote. The unidentified green object is treated as a 6th non-obsidian item in the notes but cannot be given a separate item ID.

#### 7g. High-Calcium Anomalous Items — Burial Contamination *(new section — from anomaly screen)*
- 82 items have Ca > 30,000 ppm (some up to 100,000+ ppm) despite normal Rb/Zr/Nb fingerprint
- Predominantly Einan/Ain Mallaha items (Natufian, deeply buried in calcareous sediment)
- Also some Motza items
- **Interpretation**: Ca absorbed from carbonate-rich burial matrix; surface contamination only
- Rb, Zr, Nb (the volcanic fingerprint elements) are not affected — attributions remain valid
- These items are **NOT reclassified** as non-obsidian
- Note in report that Ca values are unreliable for these items and should not be used for comparative purposes

Additionally, 2 items with unusual Nb/Zr ratios (Category 3 outliers):

| Item ID | Nb/Zr | Assemblage range (±3σ) | Possible explanation |
|---|---|---|---|
| `mot_40935a` | 0.500 | 0.341 ± 0.150 | Too high — different source? measurement error? |
| `mot_50662b` | 0.184 | 0.341 ± 0.150 | Too low — unusual chemistry |

These two items are flagged for caution; their attributions should be treated tentatively.

---

### 8. Figures (6 total, embedded in PDF)

| # | Title | Script | Notes |
|---|---|---|---|
| Fig 1 | Nb vs Zr biplot (reference ellipses + all attributed samples) | `13_source_attribution.py` | `yif_` (no basket) excluded |
| Fig 2 | Rb vs Zr biplot (calibration offset visible) | `13_source_attribution.py` | `yif_` (no basket) excluded |
| Fig 3 | Nb/Zr ratio strip chart by site | `13_source_attribution.py` | - |
| Fig 4 | Pie charts by site (attribution proportions) | `13_source_attribution.py` | - |
| Fig 5 | PCA plot | `12_internal_statistics.py` | - |
| Fig 6 | Dendrogram | `12_internal_statistics.py` | - |

---

### 9. Discussion (minimal)
- Göllü Dağ dominance across all three sites
- Comparison with regional literature
- Significance of BingolA find at Yiftahel
- Caveats: pXRF limitations, Rb calibration, sample surface condition

### 10. Conclusions

### 11. Bibliography (full)
All articles in `articles/` folder that contributed reference data.

---

## Implementation Steps

### Phase A — Figure Updates
1. Verify all 6 figures exist in `outputs/figures/attribution/` and `outputs/figures/statistics/`
2. Regenerate Nb/Zr and Rb/Zr biplots with `yif_` (no basket) explicitly excluded  
   → update filter in `analysis/13_source_attribution.py`
3. Verify Group3d noise item absent from all plots

### Phase B — Report Generator Script
4. Create `analysis/14_generate_report.py`:
   - Reads `source_attribution.csv`, `source_statistics.csv`, `tier1_comparison_ready.csv`, `anomaly_screen_report.txt`
   - Generates Table 1 (reference DB) and Table 2 (attribution by site) as Markdown tables
   - Writes `outputs/reports/final_report.md` with all sections
   - Embeds figure paths as relative links

### Phase C — PDF Generation
5. Convert `final_report.md` → `outputs/reports/final_report.pdf` via pandoc  
   - YAML front matter: title, author, date, margins, bibliography  
   - Verify pandoc installed; install via winget if not

### Phase D — Review and Iterate
6. User reviews PDF draft, requests edits

---

## Key Files

| File | Role |
|---|---|
| `my_samples/samples_clean.csv` | Full sample data (510 rows) |
| `outputs/reports/source_attribution.csv` | Per-item attribution results |
| `outputs/reports/source_attribution_report.txt` | Attribution summary stats |
| `outputs/reports/anomaly_screen_report.txt` | Non-obsidian / anomalous items |
| `reference_database/source_statistics.csv` | Table 1 source data |
| `reference_database/tier1_comparison_ready.csv` | Reference DB |
| `outputs/figures/attribution/` | Biplots, strip chart, pies |
| `outputs/figures/statistics/` | PCA, dendrogram |
| `outputs/figures/anomaly/` | Anomaly screen figures |
| `analysis/13_source_attribution.py` | Attribution + figure generation |
| `analysis/12_internal_statistics.py` | PCA + clustering |
| `analysis/14_generate_report.py` | Report generator (TO CREATE) |
| `analysis/15_anomaly_screen.py` | Anomaly screen (done) |

---

## Anomaly Screen Summary (from `analysis/15_anomaly_screen.py`)

**Run date**: 2026-03-28  
**Total items**: 510  

| Category | Count | Description |
|---|---|---|
| Cat 0 — Normal obsidian | 419 | Clean, no flags |
| Cat 1 — NOT obsidian | 5 | `ein_` (Chert), `mot_41350`, `mot_50683` (Flint?), `mot_50633`, `mot_40878` (no Rb/Nb; extreme Ca/Fe) |
| Cat 2 — High Ca, Rb present | 82 | Burial Ca contamination; obsidian geochemistry intact |
| Cat 3 — Source outliers | 4 | `mot_40935a` (Nb/Zr=0.500), `mot_50662b` (Nb/Zr=0.184), `yif_` (high Zr, Group3d noise), `yif_10671` (BingolA) |
| Cat 4 — Rb/Nb low only | 0 | None |

Reference stats: Nb/Zr mean=0.341 SD=0.050; Zr mean=70.6 SD=43.4 ppm; Fe mean=8,281 SD=2,908 ppm; Ca mean=17,508 SD=15,768 ppm

---

## Verification Checklist

- [ ] PDF renders without errors, all 6 figures embedded and captioned
- [ ] `yif_` (no basket) absent from all plots
- [ ] Table 1 values match `source_statistics.csv`
- [ ] Table 2 counts match `source_attribution_report.txt`
- [ ] §7d (yif_10671 / BingolA) present with Rb/Zr/Nb values
- [ ] §7e (`yif_` no basket exclusion) documented
- [ ] §7f (5 non-obsidian items) listed with reasons
- [ ] §7g (82 high-Ca items + 2 Nb/Zr outliers) explained
- [ ] Bibliography complete
- [ ] Rb×2 calibration caveat prominent in §6b

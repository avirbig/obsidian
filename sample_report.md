# Obsidian pXRF Sample Report

**Project:** Near Eastern Obsidian Provenance Study  
**Instrument:** Niton XL3t (Mining Cu/Zn mode, 60-second readings)  
**Last updated:** 2026-03-26

---

## 1. What Was Measured and Why

Three archaeological assemblages were measured with a portable X-ray fluorescence (pXRF) device to determine which volcanic obsidian sources supplied the raw material. Each artifact was placed flat on the instrument aperture and measured once on the dorsal side and once on the ventral side (two readings per artifact) to assess repeatability.

| Site | Period | Abbreviation | Why it matters |
|------|--------|-------------|----------------|
| Motza | EPPNB (Early Pre-Pottery Neolithic B) | mot_ | Large knapping assemblage; expected Anatolian connections |
| Einan (Eynan/Ain Mallaha) | Natufian | ein_ | Pre-Neolithic; tests whether long-distance obsidian exchange pre-dates farming |
| Yiftahel | MPPNB (Middle Pre-Pottery Neolithic B) | yif_ | Ground-truth test; previous INAA data (Yellin & Garfinkel 1986) shows Eastern Galilee Dikili Tash (EGD) |

**Instrument note:** The Niton Mining mode does not measure Yttrium (Y). The usable geochemical fingerprint is therefore **Rb / Zr / Nb** (3 elements). Strontium (Sr) was measured but is mostly below the detection limit (only 9% of items have a Sr value) and is not used for source attribution.

---

## 2. Sample Inventory

### 2a. Obsidian samples

| Site | N items | Period |
|------|---------|--------|
| Motza | 381 | EPPNB |
| Einan | 103 | Natufian |
| Yiftahel | 23 | MPPNB |
| **Total** | **507** | |

### 2b. Non-obsidian items (kept for comparison)

### 2b. Non-obsidian items (flint/chert) — why the readings differ

**Why obsidian and flint give completely different pXRF signals** comes down to their mineralogy and formation process:

**Obsidian** is a volcanic glass — rapidly quenched rhyolitic to rhyodacitic magma (~70–75% SiO₂). Because it solidified from a melt, all the incompatible trace elements that couldn't fit into mineral crystal structures (Rb, Zr, Nb, Sr, Y) became concentrated in the glass at ppm-level abundances. These elements are homogeneously distributed throughout the glass matrix, which is why they produce stable, reproducible pXRF readings and serve as geochemical fingerprints. Different Anatolian volcanic centers (Göllü Dağ, Nemrut Dağ, Bingöl) cooled from magmas with distinct trace-element ratios, allowing source discrimination.

**Flint and chert** are sedimentary silica rocks — essentially pure microcrystalline or cryptocrystalline quartz (SiO₂ > 95%), formed by the diagenetic recrystallization of biogenic silica (sponge spicules, diatoms, radiolaria) or by silica precipitation in carbonate sediments. Because they form at low temperatures from silica-saturated fluids rather than from a trace-element-rich magma, they contain almost none of the fingerprinting elements:

| Element | Obsidian (typical) | Flint/Chert (typical) | pXRF result |
|---------|-------------------|----------------------|-------------|
| Rb | 100–500 ppm | < 5 ppm | Below LOD in flint |
| Zr | 50–1300 ppm | < 5 ppm | Below LOD in flint |
| Nb | 10–70 ppm | < 2 ppm | Below LOD in flint |
| Sr | 0–150 ppm | variable (0–100 ppm from carbonate) | Occasionally detectable |
| Si | Very high | Dominant | High in both |
| Fe | Moderate | Low–trace | Lower in flint |

The three flint/chert items in this dataset all returned Rb = Zr = Nb = NaN (below the instrument's lower detection limit), while their Si signal was large and their Fe was either below range or minimal. This pattern is diagnostic: **any item with no Rb, Zr, or Nb signal is almost certainly not obsidian**.

Two artifacts from Motza and one reading pair from Einan were flagged as possible **flint** on this basis. They are retained in `samples_clean.csv` with `material = flint?` for reference but are excluded from all obsidian provenance calculations.

| item_id | site | basket | locus | identification basis |
|---------|------|--------|-------|----------------------|
| mot_41350 | motza | 41350 | — | `remarks = 'Flint?'` in master xlsx |
| mot_50683 | motza | 50683 | — | `remarks = 'Flint?'` in master xlsx |
| ein_ | einan | (none) | Chert | `ndt_label = 'Dark colored flint'` / `'light colored flint'` (readings 1783–1784, 23/02/2017); `locus = 'Chert'` |

---

## 3. Data Quality

### 3a. Element coverage (obsidian items only, N=508)

| Element | Coverage | Used for attribution? |
|---------|----------|-----------------------|
| Rb | ~99% | Yes |
| Zr | ~99% | Yes |
| Nb | ~99% | Yes |
| Sr | ~9% | No (mostly below LOD) |
| Y | 0% | No (not measured in this mode) |
| Fe, Mn, Zn, Ti, Ba, Th, Pb, Ga | ~80-95% | Supporting data only |

### 3b. Repeatability (dorsal vs. ventral readings)

484 of 510 items have two readings. CV% = coefficient of variation between the two readings.

| Max CV% between readings | N items | Meaning |
|--------------------------|---------|---------|
| < 5% | 152 | Excellent agreement |
| 5 -- 10% | 136 | Acceptable agreement |
| >= 10% (divergent) | 196 | One or more elements disagreed |

Items with divergent readings are flagged `repeat_divergent` in the `quality_flag` column. The specific element(s) that caused the disagreement are listed in the `divergent_elements` column (e.g., `Rb,Zr` means both Rb and Zr had CV >= 10% between the two sides).

A 40% divergence rate is normal for obsidian flakes: the curved dorsal surface (which may retain cortex or have variable thickness) often gives a noisier reading than the flat ventral surface. All divergent items are **included** in the analysis but flagged so they can be checked or weighted accordingly.

### 3c. Quality flag summary

| Flag | N items | Meaning |
|------|---------|---------|
| good | 286 | 2+ readings, all heavy elements agree within 10% |
| repeat_divergent | 192 | 2+ readings, at least one element diverges >= 10% |
| single | 26 | Only one reading available |
| beam_minimal | 2 | Beam coverage classified as Minimal (small artifact) |
| beam_minimal+repeat_divergent | 4 | Both conditions apply |

### 3d. Items needing attention

Two items have empty basket numbers and may represent data entry issues:

| item_id | issue |
|---------|-------|
| yif_ (empty basket) | Zr CV = 141%, Nb CV = 55% -- extreme divergence; likely entry error |
| ein_ (empty basket) | Confirmed flint (readings 1783-1784); `material = flint?`; excluded from obsidian analysis |

The yif_ item appears in `samples_clean.csv` but should be treated with caution in attribution.

---

## 3e. Methodological Note: Inter-Instrument Calibration

**The problem:** The Niton XL3t used for this project was operated in Mining Cu/Zn mode. The reference datasets used for source attribution (compiled from published studies) were measured on a variety of instruments and modes — Olympus DELTA, Bruker, Niton Geo mode, laboratory EDXRF. No geological obsidian source sample (a piece of raw volcanic glass of known provenance) was measured with *this* specific Niton in this *specific* mode. That means we cannot directly verify that a reading of, say, Rb = 250 ppm on this instrument corresponds to Rb = 250 ppm in the reference datasets.

**Why this matters:** If the Mining Cu/Zn calibration systematically over- or under-reads Rb by X%, all 507 samples will be shifted together in Rb-space. Depending on the direction and magnitude of the offset, they could be pushed closer to a wrong source and away from the correct one.

**Three strategies to mitigate the problem:**

| Strategy | How it helps | Limitation |
|----------|-------------|-----------|
| **Element ratios (Rb/Zr, Nb/Zr, Rb/Nb)** | If the calibration offset affects all heavy elements proportionally, numerator and denominator shift together and the ratio stays correct | Fails if different elements are offset differently |
| **Yiftahel as implicit calibration check** | Yiftahel was independently sourced as EGD via INAA (Yellin & Garfinkel 1986). If Phase 5 Mahalanobis also places Yiftahel closest to EGD, the calibration offset is small enough not to cause misattribution | Only validates one source; cannot quantify the offset precisely |
| **PCA-space comparison** | Projection into principal component space partially absorbs uniform scaling offsets; relative clustering of samples vs. reference sources is more stable than absolute ppm distances | Large offsets can still shift cluster membership |

**Both absolute ppm values and element ratios are analysed in parallel** throughout this project so that results can be interpreted and cross-checked with either approach.

**Recommended future step:** Measure 3–5 obsidian pieces of known geological origin (e.g., from the Hebrew University reference collection, or geological samples used in published studies) with the same Niton instrument and settings. Comparing those readings to published reference values would yield per-element correction factors (slope + intercept) for the Mining Cu/Zn mode.

---

## 4. Internal Statistics (Phase 3b — Completed)

> **Completed.** Full output: `my_samples/internal_stats_report.txt` and `outputs/figures/internal/` (9 figures).

The assemblage was examined internally before comparison against the reference database. The guiding question: **can we see chemical groupings within and between our own samples, and do they correlate with site or period?**

### 4a. Sample counts for internal analysis

| Site | N (obsidian) | Period |
|------|-------------|--------|
| Motza | 381 | EPPNB |
| Einan | 103 | Natufian |
| Yiftahel | 23 | MPPNB |

### 4b. Elements analysed

- **Primary fingerprint:** Rb, Zr, Nb (≈ 99% coverage)
- **Ratio variants:** Rb/Zr, Nb/Zr, Rb/Nb — analysed in parallel with absolute values as a calibration-offset-robust alternative (see Section 3e)

### 4c. Descriptive statistics

Mean ppm per site and full descriptive tables (N, mean, SD, min, median, max, CV%) appear in `internal_stats_report.txt` Section 1, for both raw ppm and element ratios.

### 4d. Significance tests

**Kruskal-Wallis** (3-site comparison) and **Mann-Whitney pairwise** tests (Motza vs Einan, Motza vs Yiftahel, Einan vs Yiftahel) for all three elements and all three ratios. Results in `internal_stats_report.txt` Section 2. Non-parametric tests were chosen because normality is not assumed for geochemical data.

### 4e. Biplots

Three biplots (Rb vs Zr, Nb vs Zr, Rb vs Nb), each with two panels:
- **Left:** absolute ppm, sites colour-coded with 2-SD confidence ellipses
- **Right:** element ratios — offset-robust version of the same comparison

Generated files: `biplot_Rb_Zr.png`, `biplot_Nb_Zr.png`, `biplot_Rb_Nb.png`

### 4f. PCA

PCA on StandardScaler(Rb, Zr, Nb). Two panels: coloured by site (with loading arrows) and coloured by period. A separate ratio-based PCA (Rb/Zr, Nb/Zr, Rb/Nb) was also computed as a calibration-robust alternative.

Generated files: `pca_sites_periods.png`, `pca_ratios.png`

### 4g. Unsupervised clustering

**K-means** (k = 2–6): elbow curve + silhouette score to select best k. Best k is determined by highest silhouette score; cluster membership cross-tabulated against site and period.

**Hierarchical clustering** (Ward linkage): dendrogram with cut line at best k; membership vs site cross-tabulated.

Generated files: `kmeans_elbow_silhouette.png`, `kmeans_k{k}_pca.png`, `dendrogram.png`

### 4h. Element distributions

Kernel density plots for Rb, Zr, Nb, Rb/Zr, Nb/Zr, Rb/Nb — one panel per element, all three sites overlaid, with median dashed lines.

Generated file: `distributions_by_site.png`

---

## 5. Source Attribution Results

> **PLACEHOLDER -- To be completed after Phase 6b (Mahalanobis distance comparison)**

This section will show, for each artifact, the most likely obsidian source. The comparison will use:
- Reference dataset: `reference_database/tier1_comparison_ready.csv` (1814 Tier 1 pXRF readings, 9 strong sources with N >= 10)
- Method: Mahalanobis distance in Rb/Zr/Nb space
- Elements used: Rb, Zr, Nb (Sr and Y excluded -- see Section 1)

**Expected result for Yiftahel (ground truth):** EGD (Eastern Galilee Dikili Tash), as reported by Yellin & Garfinkel (1986) using INAA.

---

## 6. Files

| File | Description |
|------|-------------|
| `my_samples/samples_raw.csv` | 1224 individual readings, one row per measurement (2 per artifact) |
| `my_samples/samples_clean.csv` | 510 aggregated items, one row per artifact; includes `material`, `quality_flag`, `divergent_elements` columns |
| `my_samples/verification_report.txt` | Automated completeness and range-sanity check |
| `my_samples/internal_stats_report.txt` | Descriptive stats, significance tests, clustering results (Phase 3b) |
| `outputs/figures/internal/` | 9 figures: biplots, PCA, k-means elbow, dendrogram, distributions |
| `reference_database/tier1_comparison_ready.csv` | Reference source data for comparison |
| `reference_database/source_comparison_fingerprints.csv` | Per-source mean/SD fingerprints |
| `reference_database/phase4_report.txt` | Source quality tier breakdown |

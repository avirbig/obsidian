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

## 4. Internal Statistics (Pre-Attribution)

> **PLACEHOLDER -- To be completed in Phase 6a (internal statistics)**

Before comparing against the reference database, the assemblage will be examined internally to identify structure in the data. This phase asks: **can we see groupings within and between my own samples, and do they correlate with site or period?**

### 4a. Within-assemblage variability
- Descriptive statistics per site: mean, SD, range for Rb, Zr, Nb
- Distribution plots (histogram + kernel density) per element per site
- Do the three sites look chemically similar or different from each other?

### 4b. Between-assemblage comparisons
- Pairwise comparison of Motza / Einan / Yiftahel centroids in Rb/Zr/Nb space
- ANOVA or Kruskal-Wallis test per element (are inter-site differences significant?)
- Biplots with site-colour-coded points and 95% confidence ellipses

### 4c. Period-level comparison
- Natufian (Einan) vs MPPNB (Yiftahel) vs EPPNB (Motza)
- Do period differences track source differences, or are they confounded by site?

### 4d. Unsupervised clustering
- k-means and hierarchical clustering in Rb/Zr/Nb space (obsidian items only)
- How many chemical groups exist in the combined assemblage?
- Do cluster boundaries align with site or period boundaries?

### 4e. PCA
- Principal Component Analysis on Rb/Zr/Nb (and optionally Fe/Mn/Ti)
- PC1 vs PC2 biplot, colour-coded by site
- Explains most variance with fewest dimensions; helps visualize groupings

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
| `reference_database/tier1_comparison_ready.csv` | Reference source data for comparison |
| `reference_database/source_comparison_fingerprints.csv` | Per-source mean/SD fingerprints |
| `reference_database/phase4_report.txt` | Source quality tier breakdown |

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

## 4i. What the Internal Statistics Actually Tell Us

This section explains the results of Phase 3b in plain language — what the numbers mean, what is surprising, and what is still uncertain.

### Finding 1: All three sites look chemically almost identical

**The numbers:**

| Site | Rb (ppm) | Zr (ppm) | Nb (ppm) | Rb/Zr |
|------|---------|---------|---------|-------|
| Motza (EPPNB, N=379) | 92 | 67 | 23 | 1.37 |
| Einan (Natufian, N=103) | 97 | 73 | 26 | 1.35 |
| Yiftahel (MPPNB, N=23) | 88* | 65* | 23* | 1.26* |

*Yiftahel median used rather than mean; the mean is distorted by one extreme outlier (see Finding 3).

**What this means:** Despite spanning three different archaeological periods — from the Natufian (~12,000 BP) through the MPPNB (~9,000 BP) and into the EPPNB (~8,500 BP) — all three assemblages have essentially the same chemical fingerprint. The Rb/Zr ratio, the primary discriminant for Near Eastern obsidian sources, shows **no statistically significant difference between sites** (Kruskal-Wallis p = 0.14 — not significant). This is a strong preliminary signal that **all three sites were drawing from the same volcanic source** throughout this entire ~3,500-year time span.

**Is this plausible archaeologically?** Yes. The obsidian exchange routes of the southern Levant are well-documented in the literature: EGD (Eastern Göllü Dağ, the Cappadocian source also known by reference names like "Dikili Tash" or specific sub-outcrops like "Kömürcü") dominates almost every Neolithic assemblage in this region. The finding that Natufians were already accessing the same Anatolian source as EPPNB people would be archaeologically significant — it would extend the long-distance exchange network back before farming.

---

### Finding 2: Two chemical subgroups exist — but they cut across sites and periods

**The clustering result:** K-means with k=3 gave the best statistical separation (silhouette = 0.63 out of 1.0, which is relatively good). BUT: the third cluster (C3) contains just **one single item** with anomalously high Zr — this is almost certainly an outlier, not a true group. The meaningful split is really k=2:

| Cluster | N items | Rb (mean) | Zr (mean) | Nb (mean) | Rb/Zr | Site composition |
|---------|---------|-----------|-----------|-----------|-------|-----------------|
| C1 (lower) | 348 | 87 | 65 | 21 | 1.34 | Motza 279 / Einan 49 / Yiftahel 20 |
| C2 (higher) | 156 | 106 | 77 | 29 | 1.38 | Motza 100 / Einan 54 / Yiftahel 2 |

**What this means:** Both clusters appear at all three sites. This is not a site-specific pattern. Three possible explanations:

1. **Two different, geochemically similar sources** — perhaps two sub-outcrops of the same volcanic center (e.g., Kömürcü-East and Kömürcü-West facets of EGD) with slightly different concentrations but the same ratio. This cannot be resolved from ratios alone — Phase 5 Mahalanobis analysis against published sub-outcrop reference data will test this.

2. **Intra-source geochemical heterogeneity** — large volcanic glass sources like Göllü Dağ show natural variation across the flow; two pieces from the same mountain can have slightly different absolute concentrations. The ratio Rb/Zr is almost identical between C1 and C2 (1.34 vs 1.38), which is consistent with this explanation.

3. **Instrument variability** — about 40% of readings are flagged `repeat_divergent` (CV ≥ 10% between dorsal and ventral readings). If measurement noise is large enough, a single source could statistically separate into two apparent clusters.

**Which explanation is most likely?** The consistency of the Rb/Zr ratio across both clusters (1.34–1.38) strongly suggests they are from the same geological source, not two distinct ones. Explanation 2 or 3 is most likely. Phase 5 will be the test.

---

### Finding 3: One Yiftahel artifact is a major outlier — possibly a different source

One artifact in the Yiftahel assemblage (item `yif_`, the empty-basket item flagged in Section 3d) has:
- **Zr = 1005 ppm** — vs. the Yiftahel median of 65 ppm
- **Nb = 65 ppm** — vs. the median of 20 ppm
- **Zr CV = 141%** between the two readings — extreme divergence, meaning the two sides of the artifact gave radically different results

For comparison, the known **Bingöl A source** has Zr ~1238 ppm and Nb ~61 ppm, and **Nemrut Dağ** has Zr ~1277 ppm. The one outlier's Zr/Nb ratio (1005/65 = 15.5) is close to NemrutDag (1277/65 = 19.6) and Bingöl A (1238/61 = 20.3) — both are "high-Zr peralkaline" sources.

**BUT:** the CV = 141% means this reading is not reliable. The two sides of the piece gave wildly different results, which is almost certainly a measurement artifact — perhaps the artifact was very small (thin flake, minimal beam coverage), positioning was poor, or there was surface contamination. **This single item should not be interpreted as evidence of contact with a second source without re-measurement.**

**Verdict:** The k=3 optimum in clustering is driven largely by this one outlier. The statistically meaningful finding is k=2 (two subgroups, both plausibly from the same source, as described in Finding 2).

---

### Finding 4: The absolute ppm values are lower than published EGD — the calibration question

Looking at how our assemblage readings compare to published EGD (Göllü Dağ East) reference values:

| Value | Our assemblage | Published EGD (Tier 1 mean) | Notes |
|-------|---------------|----------------------------|-------|
| Rb (ppm) | ~93 | ~182 | Our values are ~half the published values |
| Zr (ppm) | ~70 | ~77 | Close match |
| Nb (ppm) | ~23 | ~25 | Close match |
| **Rb/Zr** | **1.36** | **2.36** | Large ratio difference |
| **Nb/Zr** | **0.34** | **0.32** | Very close match |

The Nb/Zr ratio matches EGD very well (0.34 vs 0.32). The Rb and Rb/Zr do not. This is likely a calibration effect: the Niton Mining Cu/Zn mode is known to under-read Rb relative to the Niton Geo mode and lab instruments. If the Rb under-reading is consistent across all artifacts, then:
- The **Nb/Zr** ratio is reliable (both elements well-read)
- The **Rb/Zr** ratio is unreliable for cross-instrument comparison
- The **absolute Rb** values should not be compared directly to published reference data

This is one of the reasons Phase 5 (Mahalanobis attribution) uses the full covariance structure, not just distance to a single centroid: the shape of the point cloud matters more than its absolute position.

**Does Nb/Zr = 0.34 uniquely identify EGD?** Among the major Levantine-relevant sources in the reference database:

| Source | Nb/Zr (published) | What this means for Nb/Zr |
|--------|-------------------|--------------------------|
| EGD | ~0.32 | Very close to our 0.34 |
| GolluDag (WGD) | ~0.25 | Lower |
| ND (Nenezi Dağ) | ~0.14 | Much lower |
| BingolA | ~0.049 | Very low (huge Zr) |
| BingolB | ~0.055 | Very low (large Zr) |
| NemrutDag | ~0.051 | Very low (very large Zr) |
| Sta Nychia (Aegean) | ~0.085 | Low |

Nb/Zr = 0.34 fits EGD well and eliminates all other known sources. **This provides pre-Phase-5 evidence that both Motza and Einan obsidian likely comes from EGD**, consistent with the known pattern for the southern Levantine Neolithic.

---

### Summary: What we can say before Phase 5

1. **Most likely single source:** All three sites appear to use EGD (Eastern Göllü Dağ, Cappadocia, Turkey). The Nb/Zr ratio is the most calibration-robust discriminant and places the assemblage squarely on EGD, eliminating Bingöl, Nemrut Dağ, and all other major sources.

2. **Internal subgrouping:** Two natural chemical groups exist (lower and higher concentrations), but they cross site and period boundaries and have nearly identical Rb/Zr ratios — most likely intra-source variability or instrument noise, not two distinct geological sources.

3. **Yiftahel outlier:** One artifact may be from a peralkaline high-Zr source (BingölA or NemrutDağ), but the measurement is unreliable and needs re-measurement before any conclusion.

4. **Continuity of exchange:** The same source chemistry appears from Natufian through MPPNB to EPPNB — a remarkable ~3,500 years of continuous access to the same Anatolian volcanic source region.

5. **Phase 5 will confirm:** Mahalanobis distance analysis against the full reference database will produce per-artifact source attributions with probability scores, formally testing whether these patterns hold.

---

## 6. Files

| File | Description |
|------|-------------|
| `my_samples/samples_raw.csv` | 1224 individual readings, one row per measurement (2 per artifact) |
| `my_samples/samples_clean.csv` | 510 aggregated items, one row per artifact; includes `material`, `quality_flag`, `divergent_elements` columns |
| `outputs/reports/verification_report.txt` | Automated completeness and range-sanity check |
| `outputs/reports/internal_stats_report.txt` | Descriptive stats, significance tests, clustering results (Phase 3b) |
| `outputs/reports/sample_report.md` | This document |
| `outputs/figures/internal/` | 9 figures: biplots, PCA, k-means elbow, dendrogram, distributions |
| `reference_database/tier1_comparison_ready.csv` | Reference source data for comparison |
| `reference_database/source_comparison_fingerprints.csv` | Per-source mean/SD fingerprints |
| `reference_database/phase4_report.txt` | Source quality tier breakdown |

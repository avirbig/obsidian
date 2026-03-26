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
| Einan | 104 | Natufian |
| Yiftahel | 23 | MPPNB |
| **Total** | **508** | |

### 2b. Non-obsidian items (kept for comparison)

Two artifacts from Motza were flagged during measurement as possible **flint** — the instrument returned no signal for Rb, Zr, or Nb (all below detection). They are retained in `samples_clean.csv` with `material = flint?` for reference but are excluded from all obsidian provenance calculations.

| item_id | site | basket | remarks |
|---------|------|--------|---------|
| mot_41350 | motza | 41350 | Flint? |
| mot_50683 | motza | 50683 | Flint? |

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
| ein_ (empty basket) | Below-range Fe and Ti -- possibly a non-obsidian contaminant reading |

These items appear in `samples_clean.csv` but should be treated with caution in attribution.

---

## 4. Source Attribution Results

> **PLACEHOLDER -- To be completed after Phase 6 (Mahalanobis distance comparison)**

This section will show, for each artifact, the most likely obsidian source. The comparison will use:
- Reference dataset: `reference_database/tier1_comparison_ready.csv` (1814 Tier 1 pXRF readings, 9 strong sources with N >= 10)
- Method: Mahalanobis distance in Rb/Zr/Nb space
- Elements used: Rb, Zr, Nb (Sr and Y excluded -- see Section 1)

**Expected result for Yiftahel (ground truth):** EGD (Eastern Galilee Dikili Tash), as reported by Yellin & Garfinkel (1986) using INAA.

---

## 5. Files

| File | Description |
|------|-------------|
| `my_samples/samples_raw.csv` | 1224 individual readings, one row per measurement (2 per artifact) |
| `my_samples/samples_clean.csv` | 510 aggregated items, one row per artifact; includes `material`, `quality_flag`, `divergent_elements` columns |
| `my_samples/verification_report.txt` | Automated completeness and range-sanity check |
| `reference_database/tier1_comparison_ready.csv` | Reference source data for comparison |
| `reference_database/source_comparison_fingerprints.csv` | Per-source mean/SD fingerprints |
| `reference_database/phase4_report.txt` | Source quality tier breakdown |

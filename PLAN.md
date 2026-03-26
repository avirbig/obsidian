# Obsidian Provenance Research — Project Plan

**Project**: Build a clean, verified reference database of obsidian source chemical signatures
from published articles and extracted xlsx tables, then compare the researcher's own pXRF
samples from South Levant archaeological sites against it.

**Sites of interest**: Motza, Einan (Ain Mallaha), Yiftahel — Neolithic / Chalcolithic, Israel

**Anatolian sources to discriminate**:
- Göllü Dağ East (EGD), West (WGD) — calc-alkaline, Cappadocia
- Nenezi Dağ (ND) — calc-alkaline, Cappadocia
- Bingöl A / B — peralkaline, Eastern Anatolia
- Nemrut Dağ (Lake Van area) — peralkaline, Eastern Anatolia
- Lake Urmia, Lake Sevan (secondary)

---

## Folder Structure

```
c:\work\code\obsidian\
├── articles/                              ← READ-ONLY source articles (txt)
├── obsidian_minerales_component_tables_from_articles/  ← READ-ONLY raw xlsx
├── reference_database/                    ← cleaned verified output
│   ├── sources/                           ← one CSV per geological source
│   └── master_reference.csv              ← all sources unified
├── my_samples/                            ← researcher's pXRF data
│   ├── samples_raw.csv                   ← as received, never modified
│   └── samples_clean.csv                 ← cleaned, verified output
├── analysis/
│   ├── notebooks/
│   │   ├── 00_environment_check.ipynb
│   │   ├── 01_data_extraction.ipynb      ← parse xlsx, verify vs article
│   │   ├── 02_data_cleaning.ipynb        ← standardize, fix encoding, ranges
│   │   ├── 03_reference_database.ipynb   ← build master_reference.csv + stats
│   │   ├── 04_visualization.ipynb        ← biplots, PCA, source ellipses
│   │   ├── 05_sample_comparison.ipynb    ← compare pXRF to reference
│   │   └── 06_sample_cleaning.ipynb      ← clean researcher's own samples
│   └── scripts/
│       └── utils.py                      ← shared helpers used by notebooks
├── outputs/
│   └── figures/                          ← PNG + PDF plots
├── .vscode/
│   ├── obsidian-research.agent.md        ← specialized AI agent
│   └── instructions/
│       ├── obsidian-data.instructions.md
│       └── obsidian-statistics.instructions.md
├── .gitignore
├── audit_cross_reference.md              ← cross-reference tracker
├── changelog.md                          ← MASTER LOG (all changes + prompts)
└── PLAN.md                               ← this file
```

---

## Phase 0 — Project Scaffolding ✅

1. Initialize git locally (`git init`) — no remote yet
2. Create folder structure (above)
3. Create `PLAN.md` (this file)
4. Create `changelog.md`
5. Create `.vscode/` agent and skill files
6. Install Python/Anaconda (see instructions below)
7. Initial git commit

### Python Installation (Windows, one-time)
1. Download Anaconda from https://www.anaconda.com/download — choose the Windows 64-bit installer
2. Run the installer — accept defaults, tick "Add to PATH" if asked
3. Open Anaconda Prompt and run:
   ```
   conda create -n obsidian python=3.11 -y
   conda activate obsidian
   pip install pandas openpyxl matplotlib seaborn scikit-learn scipy jupyter
   ```
4. Open notebook 00 in VS Code to verify installation

---

## Phase 1 — Reference Data Extraction & Verification

**Notebook**: `analysis/notebooks/01_data_extraction.ipynb`

For each xlsx in `obsidian_minerales_component_tables_from_articles/`:
- Parse and standardize column names to element symbols (Rb, Sr, Zr, Nb, Y…)
- Spot-check 3–5 rows against the matching article `.txt` file
- Handle special cases:
  - Milic 2014: range strings "166-194" → numeric midpoint, flag in `_range_flag` column
  - Side-by-side table layouts → split into tidy format
  - Empty sheets (Frahm 2014, Gratuze 1999) → log and skip
- Standardize source labels (EGD, WGD, ND, BingolA, BingolB, NemrutDag…)
- Tag every row: paper, year, method, method_tier, units, source/site
- Log every decision in `changelog.md`
- **Git commit** after each paper

**Priority order** (Tier 1 first):
1. Milic 2014.xlsx
2. Campbell and healey 1.xlsx + 2.xlsx
3. Frahm 2013.xlsx
4. Morgan 2015.xlsx
5. Schechter et al 2016.xlsx
6. Frahm and Hauck 2017.xlsx
7. Khalidi Gratuze Boucetta 2009.xlsx
8. data2.xlsx sheets (Carter & Shackley 2007, Forster & Grave 2012, etc.)
9. Carter_Rosenberg_2022_Tel_Tsaf.xlsx

---

## Phase 2 — Reference Database Construction

**Notebooks**: `02_data_cleaning.ipynb`, `03_reference_database.ipynb`

- Collect all verified measurements per geological source
- Compute per-source descriptive statistics: n, mean, SD, min, max, 2SD range
- Pool by tier:
  - Tier 1 (pXRF): primary reference
  - Tier 2 (EDXRF): included with `method_tier=2` flag
  - Tier 3–4: `method_tier=3/4`, reference-only columns
- Write `reference_database/sources/*.csv` and `master_reference.csv`
- Log outlier exclusion decisions
- **Git commit**

**Method tiers** (from audit_cross_reference.md Section E):
| Tier | Methods | Comparability |
|------|---------|---------------|
| 1 | pXRF | Directly comparable |
| 2 | EDXRF (lab) | Mostly comparable, flag |
| 3 | LA-ICP-MS, ICP-AES/MS, PIXE, WDXRF | Partial, reference-only |
| 4 | NAA/INAA, Electron Microprobe | Different element suite |

---

## Phase 3 — Researcher's Sample Cleaning & Verification

**Notebook**: `analysis/notebooks/06_sample_cleaning.ipynb`

- Load `my_samples/samples_raw.csv`
- Standardize column names to match reference database
- Check for: missing values, out-of-range values, duplicate IDs, unit mismatches
- Flag suspicious values vs known instrument noise floor and source ranges
- Log every cleaning decision in `changelog.md` with sample ID and reasoning
- Save to `my_samples/samples_clean.csv`
- **Git commit**

---

## Phase 3b — Internal Statistics ✅

**Script**: `analysis/12_internal_statistics.py`  
**Output**: `my_samples/internal_stats_report.txt`, figures in `outputs/figures/internal/`

Before comparing against the reference database, examine the assemblage internally to detect chemical structure.

### Questions
1. **How many chemical groups exist within the combined 507 obsidian items?**
2. **Do those groups align with site (Motza / Einan / Yiftahel) or period (Natufian / MPPNB / EPPNB)?**
3. **Are there statistically significant between-site or between-period differences?**

### Steps

**Descriptive statistics**
- Mean, SD, min, max, range for Rb / Zr / Nb per site and per period
- Export as tables to `internal_stats_report.txt`

**Biplots (internal, no reference sources)**
- Rb vs Zr, Nb vs Zr, Rb vs Nb
- Points colour-coded by site; separate marker shapes by period
- 95% confidence ellipses per site
- Save to `outputs/figures/internal/`

**PCA**
- StandardScaler on Rb/Zr/Nb (obsidian only, non-null rows)
- Scatter of PC1 vs PC2 coloured by site
- Loadings plot

**Significance testing**
- Kruskal-Wallis test per element (Rb, Zr, Nb) across sites (3 groups)
- Post-hoc pairwise Mann-Whitney U (Motza/Einan, Motza/Yiftahel, Einan/Yiftahel)
- Report p-values; note where sites are chemically indistinguishable

**Unsupervised clustering**
- k-means (k = 2, 3, 4, 5) on standardized Rb/Zr/Nb
- Elbow curve (inertia vs k) to select optimal k
- Hierarchical clustering dendrogram (Ward linkage)
- Cross-tabulate cluster membership vs site to measure alignment

**Expected outcomes / hypotheses**
- Yiftahel (MPPNB) = distinct low-Zr, moderate-Rb cluster (expected EGD)
- Motza (EPPNB) = possibly 2+ clusters (Anatolian sources are diverse)
- Einan (Natufian) = uncertain; rarer long-distance exchange pre-farming

**Output files**

| File | Description |
|------|-------------|
| `my_samples/internal_stats_report.txt` | Tables: descriptive stats, test results, cluster assignments |
| `outputs/figures/internal/biplot_Rb_Zr.png` | Rb vs Zr by site |
| `outputs/figures/internal/biplot_Nb_Zr.png` | Nb vs Zr by site |
| `outputs/figures/internal/pca_sites.png` | PCA coloured by site |
| `outputs/figures/internal/kmeans_elbow.png` | Elbow curve |
| `outputs/figures/internal/dendrogram.png` | Hierarchical clustering |

**Git commit** after completion.

---

## Phase 4 — Visualization (reference sources + samples)

**Notebook**: `analysis/notebooks/04_visualization.ipynb`

Standard biplots with 95% confidence ellipses per source (in priority order):

| Plot | Elements | Why |
|------|----------|-----|
| 1 | Rb vs Sr | Cappadocian source discrimination |
| 2 | Rb vs Zr | Second-level discriminator |
| 3 | Nb vs Zr | **Critical**: peralkaline vs calc-alkaline |
| 4 | Sr vs Zr | ND vs EGD separation |
| 5 | Fe vs Mn | Nemrut sub-groups |
| 6 | Rb/Sr vs Zr | Normalized, reduces calibration bias |

Also: PCA plot (PC1 vs PC2) of all sources, standardized.
Save all to `outputs/figures/` as .png (300 dpi) and .pdf.

---

## Phase 5 — Sample Comparison & Attribution

**Notebook**: `analysis/notebooks/05_sample_comparison.ipynb`

- Plot researcher's samples on top of Phase 4 biplots
  - Symbols: Motza=★, Einan=◆, Yiftahel=▲ (all black)
- Compute **Mahalanobis distance** from each sample to each source centroid
- Report probability scores (via chi-squared p-value on MD²)
- Flag ambiguous assignments (MD < 2 for two or more sources)
- **Ground-truth check**: Yiftahel assignments should match Yellin & Garfinkel 1986 (INAA → Göllü Dağ)
- **Git commit**

---

## Phase 6 — VS Code Agent & Skill Files ✅

- `.vscode/obsidian-research.agent.md` — domain-aware agent
- `.vscode/instructions/obsidian-data.instructions.md` — data handling rules
- `.vscode/instructions/obsidian-statistics.instructions.md` — stats explanations

---

## Next Steps (as of 2026-03-26)

**Completed:**
- Phase 0 (scaffolding) ✅
- Phase 1 (reference data extraction) ✅
- Phase 2 (reference database, 34 sources, 2375 rows) ✅
- Phase 3 (sample loading, cleaning, verification -- 507 obsidian + 3 flint, 510 total) ✅
- Phase 3b (internal statistics: descriptive stats, biplots, PCA, k-means, hierarchical clustering, calibration note) ✅

**Immediate next step:**
1. **Phase 4 — Visualization** -- overlay samples on reference source biplots
2. **Phase 5 — Source attribution** -- Mahalanobis distance comparison

---

## Key Conventions

- **Raw files are NEVER modified**
- `samples_raw.csv` is IMMUTABLE after creation — do not edit
- `changelog.md` format: `[YYYY-MM-DD] | TYPE | File | Description | Source`
- User prompts logged as: `[YYYY-MM-DD] | USER_PROMPT | — | "exact text"`
- **Changelog rule**: After every session, before git commit, `changelog.md` MUST be updated with one `USER_PROMPT` entry per user message and one `DATA_ADD`/`ANALYSIS`/`BUG_FIX`/`VERIFICATION` entry per script run or output file created.
- Git commit after each completed paper or major milestone
- Source label standards: `EGD`, `WGD`, `ND`, `BingolA`, `BingolB`, `NemrutDag`, `Urmia`, `Sevan`
- Element column names: `Rb`, `Sr`, `Zr`, `Nb`, `Y`, `Fe`, `Mn`, `Ba`, `Zn`, `Ti`
- Sample master file: `my_samples/data manipulation.xlsx`, sheet `First Changes` (1224 readings, 3 sites)
- Y not measured in Niton Mining Cu/Zn mode — use Rb/Zr/Nb for source attribution (Sr mostly below LOD)

---

## Outstanding Gaps (from audit)

- Frahm 2014 and Gratuze 1999 xlsx sheets are empty — PDFs needed
- Carter et al. 2013 (Kenan Tepe) article text not yet available
- Oddone et al. 1997 and Yellin et al. 1996 article texts not available
- Researcher's own pXRF samples not yet provided (will be samples_raw.csv)

---

*Last updated: 2026-03-25 | Phase 0 completed*

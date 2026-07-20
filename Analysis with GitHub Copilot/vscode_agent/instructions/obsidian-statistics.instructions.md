---
applyTo: "analysis/**"
---

# Obsidian Statistics & Visualization Instructions

## Core Principle

**Always explain every statistical method in plain language before applying it.**
The researcher has limited statistics background. Every notebook cell that performs
a statistical operation MUST be preceded by a markdown cell containing:
1. What the method does (one short paragraph, no jargon)
2. What the output means
3. What to watch out for

---

## Descriptive Statistics

For each geological source and each element, compute and report:

| Statistic | What it means (plain language) |
|-----------|-------------------------------|
| **n** | How many measurements we have for this source |
| **Mean** | The average — "the typical value for this source" |
| **SD** (standard deviation) | How spread out the values are — "how much measurements vary from the mean" |
| **Min / Max** | The smallest and largest observed values |
| **2SD range** | Mean ± 2×SD — "the range that captures ~95% of all measurements from this source" |

**Plain language for 2SD to include in notebooks**:
> "If we imagine measuring 100 obsidian samples from Göllü Dağ East, about 95 of them would
> fall within this range. If an unknown sample falls outside this range, it is probably NOT
> from this source."

**Minimum n before computing statistics**:
- n ≥ 10: safe to compute all statistics and draw confidence ellipses
- 5 ≤ n < 10: compute but flag all outputs as low-confidence
- n < 5: report mean and range only; do NOT draw a confidence ellipse

---

## Biplots with 95% Confidence Ellipses

**What it is** (for notebook markdown cell):
> "A biplot is a scatter plot where each dot is one obsidian measurement, and we draw an
> ellipse around each source's cluster of dots. The ellipse captures ~95% of all measurements
> from that source. Importantly, the ellipse is NOT a circle — it stretches in the direction
> where measurements vary most, because sources can vary more in one element than another.
> When you plot your unknown samples on the same chart, you can visually see which source
> ellipse they fall inside."

**Standard biplots — always produce in this order**:

| # | X | Y | Key insight |
|---|---|---|-------------|
| 1 | `Rb` | `Sr` | Primary Cappadocian discrimination — EGD has high Rb/low Sr; WGD intermediate |
| 2 | `Rb` | `Zr` | Second discriminator — helps separate ND from EGD |
| 3 | `Nb` | `Zr` | **Most important**: Bingöl and Nemrut have Nb > 30 ppm; Göllü Dağ < 15 ppm |
| 4 | `Sr` | `Zr` | Separates ND (high Sr) from EGD (low Sr) |
| 5 | `Fe` | `Mn` | Sub-group discrimination within Nemrut |
| 6 | `Rb/Sr` | `Zr` | Ratio reduces instrument calibration bias across labs |

**Code pattern for confidence ellipse**:
```python
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def confidence_ellipse(ax, x, y, n_std=2.0, facecolor='none', **kwargs):
    """
    Draw a confidence ellipse for 2D data x, y.
    n_std=2.0 gives a ~95% confidence ellipse (2-sigma).
    """
    if len(x) < 3:
        return  # not enough points
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    rx = np.sqrt(1 + pearson)
    ry = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=rx * 2, height=ry * 2,
                      facecolor=facecolor, **kwargs)
    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    t = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(np.mean(x), np.mean(y))
    ellipse.set_transform(t + ax.transData)
    ax.add_patch(ellipse)
```

---

## PCA (Principal Component Analysis)

**What it is** (for notebook markdown cell):
> "PCA takes many measurements at once (for example, 8 different elements per sample) and
> finds the two directions in which the data varies the most. It then projects everything
> onto those two directions so you can see it in a 2D scatter plot. Samples that are close
> together in the PCA plot have similar chemical compositions overall. The axes (PC1, PC2)
> no longer represent single elements — they are combinations of all elements. We always
> report what percentage of the total variation each axis captures."

**Protocol — always follow this sequence**:
1. Select only elements present in both Tier 1 and Tier 2 data
2. Drop samples with more than 3 missing element values
3. **Z-score standardize** before PCA:
   ```python
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(df[element_cols].dropna())
   ```
   > **Why standardize?** Without this, elements measured in large numbers (Fe ~10,000 ppm)
   > would completely dominate elements in small numbers (Nb ~5 ppm). Standardizing puts
   > all elements on equal footing.
4. Run PCA:
   ```python
   from sklearn.decomposition import PCA
   pca = PCA(n_components=2)
   coords = pca.fit_transform(X_scaled)
   var_explained = pca.explained_variance_ratio_ * 100
   print(f"PC1: {var_explained[0]:.1f}%,  PC2: {var_explained[1]:.1f}%")
   ```
5. Always print and display variance explained
6. Plot with source color-coding and researcher's samples overlaid

**What to watch for**:
- If PC1 + PC2 < 60% of variance, there is important structure in higher dimensions — note this
- A very high PC1 (>80%) means one element dominates — check for outliers or unit errors

---

## Mahalanobis Distance for Sample Attribution

**What it is** (for notebook markdown cell):
> "When we want to find out which source an unknown obsidian sample most likely came from,
> we need a way to measure 'how far' the sample is from the center of each source's
> chemical signature. Simple distance (Euclidean) treats all elements equally, but that is
> misleading — some elements vary a lot naturally within a source, and some vary very
> little. Mahalanobis distance accounts for this. Think of it as asking: 'How many
> standard deviations is this sample from the center of this source's cloud, given the
> shape of the cloud?'
>
> A Mahalanobis distance below 2 means the sample is inside the 95% confidence region of
> that source — it is consistent with that origin. Above 3 means it is very unlikely to
> come from that source."

**Thresholds**:
| MD value | Interpretation |
|----------|---------------|
| < 2.0 | Consistent with this source (inside 2-sigma) |
| 2.0 – 3.0 | Marginal — possible but uncertain |
| > 3.0 | Inconsistent — likely a different source |

**Protocol**:
1. Use only elements present in both the reference data AND the researcher's samples
2. Compute mean vector and covariance matrix for each source (Tier 1 + Tier 2)
3. Skip sources with n < 5 (singular covariance matrix risk)
4. For each sample, compute MD to every source; report the full table
5. Highlight the minimum MD (most likely source); flag ties
6. Report p-value using chi-squared distribution on MD² with k degrees of freedom (k = number of elements used)

**Code pattern**:
```python
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2
import numpy as np

def attribute_sample(sample_vals, reference_df, element_cols):
    """
    Compute Mahalanobis distance from a sample to each source in reference_df.
    Returns a DataFrame of sources sorted by MD (ascending = most likely first).
    """
    results = []
    for source, grp in reference_df.groupby('source'):
        sub = grp[element_cols].dropna()
        if len(sub) < 5:
            continue
        mu = sub.mean().values
        cov = sub.cov().values
        try:
            VI = np.linalg.inv(cov)
            md = mahalanobis(sample_vals, mu, VI)
            # p-value: probability that a sample from this source has MD >= observed
            p = 1 - chi2.cdf(md**2, df=len(element_cols))
            results.append({'source': source, 'MD': round(md, 3), 'p_value': round(p, 4), 'n_ref': len(sub)})
        except np.linalg.LinAlgError:
            results.append({'source': source, 'MD': np.nan, 'p_value': np.nan, 'n_ref': len(sub), 'note': 'singular matrix'})
    return pd.DataFrame(results).sort_values('MD')
```

---

## Outlier Detection

Before computing source statistics:
1. For each source and element, compute the mean and SD
2. Flag any value > 3 SD from the mean as a potential outlier
3. **Never automatically remove outliers** — flag, investigate, log decision
4. Show outliers in a boxplot per source per element (notebook 02)

> "An outlier might be: a measurement error, a wrong source label in the original paper,
> or genuine within-source variation. We must check the article before deciding."

---

## Visual Style Conventions

Apply these consistently across ALL figures:

**Source colors** (fixed):
```python
SOURCE_COLORS = {
    'EGD': '#1f77b4',      # blue
    'WGD': '#17becf',      # cyan
    'ND': '#2ca02c',       # green
    'BingolA': '#d62728',  # red
    'BingolB': '#ff7f0e',  # orange
    'NemrutDag': '#9467bd',# purple
    'Urmia': '#8c564b',    # brown
    'Sevan': '#e377c2',    # pink
}
```

**Researcher's samples** (always black, unique marker per site):
```python
SITE_MARKERS = {
    'Motza': '*',    # star
    'Einan': 'D',    # diamond
    'Yiftahel': '^', # triangle up
}
```

**Ellipse style**: `alpha=0.15` (fill), `alpha=0.8` (edge), `linewidth=1.5`

**Saving figures**: Always save as both PNG and PDF:
```python
fig.savefig('outputs/figures/biplot_Rb_Sr.png', dpi=300, bbox_inches='tight')
fig.savefig('outputs/figures/biplot_Rb_Sr.pdf', bbox_inches='tight')
```

**Axis labels**: Always include element name and units, e.g., `"Rb (ppm)"`, `"Sr (ppm)"`

**Figure caption template** (include as a print statement or markdown cell):
> "Figure X: Rb vs Sr biplot for Anatolian obsidian sources. Ellipses represent 95%
> confidence regions (2-sigma) based on [Tier 1 + Tier 2] reference data from [list papers].
> Black symbols show researcher's pXRF samples from South Levant sites."

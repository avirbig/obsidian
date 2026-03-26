"""
12_internal_statistics.py -- Phase 3b: Internal statistics on user pXRF samples.

Input:  my_samples/samples_clean.csv  (obsidian items only, material == 'obsidian')
Output:
  my_samples/internal_stats_report.txt   -- text tables + test results
  outputs/figures/internal/              -- all figures (PNG 300 dpi)

Questions answered:
  1. How are Rb / Zr / Nb distributed within each site and period?
  2. Are between-site differences statistically significant?
  3. How many natural chemical groups are there (k-means, hierarchical)?
  4. Does PCA structure align with site or period?
  5. Do element ratios (Rb/Zr, Nb/Zr, Rb/Nb) show the same groupings?

NOTE on inter-instrument calibration:
  The user's Niton XL3t (Mining Cu/Zn mode) has not been validated against any
  known geological source measured in the published reference datasets.
  Absolute ppm values may carry a systematic offset vs. published data.
  This script therefore analyses BOTH absolute values AND element ratios.
  Ratios are more robust to instrument-to-instrument offsets because both
  numerator and denominator are shifted in the same direction by calibration bias.
  The Yiftahel assemblage serves as implicit ground-truth: if internal analysis
  places Yiftahel in a distinct, internally coherent cluster, and that cluster
  later maps onto EGD in Phase 5 (Mahalanobis), we have indirect validation.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

ROOT      = Path(r'c:\work\code\obsidian')
SAMPLES   = ROOT / 'my_samples'
FIGURES   = ROOT / 'outputs' / 'figures' / 'internal'
REPORT    = SAMPLES / 'internal_stats_report.txt'

FIGURES.mkdir(parents=True, exist_ok=True)

ELEMS  = ['Rb', 'Zr', 'Nb']   # core fingerprint elements (Y not measured, Sr ~9%)
EXTRA  = ['Fe', 'Mn', 'Ti']   # secondary elements for supporting plots

SITE_COLORS  = {'einan': '#1f77b4', 'motza': '#ff7f0e', 'yiftahel': '#2ca02c'}
PERIOD_MARKS = {'natufian': 'o', 'MPPNB': '^', 'EPPNB': 's'}

SITE_ORDER   = ['motza', 'einan', 'yiftahel']
PERIOD_ORDER = ['natufian', 'MPPNB', 'EPPNB']


# ──────────────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────────────

def load_obsidian() -> pd.DataFrame:
    path = SAMPLES / 'samples_clean.csv'
    df = pd.read_csv(path)
    obs = df[df['material'] == 'obsidian'].copy()
    print(f'Loaded {len(obs)} obsidian items (of {len(df)} total).')

    # Add element ratios (avoid division by zero -> NaN)
    for num, den in [('Rb', 'Zr'), ('Nb', 'Zr'), ('Rb', 'Nb')]:
        col = f'{num}/{den}'
        obs[col] = np.where(
            obs[den].notna() & obs[num].notna() & (obs[den] > 0),
            (obs[num] / obs[den]).round(4),
            np.nan
        )

    return obs


# ──────────────────────────────────────────────────────────────────────────────
# Text report helpers
# ──────────────────────────────────────────────────────────────────────────────

class Report:
    def __init__(self, path: Path):
        self._lines = []
        self._path  = path

    def h1(self, text):
        self._lines.append('\n' + '=' * 70)
        self._lines.append(text.upper())
        self._lines.append('=' * 70)

    def h2(self, text):
        self._lines.append('\n' + text)
        self._lines.append('-' * len(text))

    def line(self, text=''):
        self._lines.append(text)

    def table(self, df: pd.DataFrame, float_fmt='{:.1f}'):
        self._lines.append(df.to_string(float_format=lambda x: float_fmt.format(x)))

    def save(self):
        self._path.write_text('\n'.join(self._lines), encoding='utf-8')
        print(f'Report saved: {self._path}')


# ──────────────────────────────────────────────────────────────────────────────
# 1. Descriptive statistics
# ──────────────────────────────────────────────────────────────────────────────

def descriptive_stats(obs: pd.DataFrame, rpt: Report):
    rpt.h1('1. Descriptive Statistics')

    all_cols = ELEMS + ['Rb/Zr', 'Nb/Zr', 'Rb/Nb']

    for groupby_col, order, label in [
        ('site',   SITE_ORDER,   'BY SITE'),
        ('period', PERIOD_ORDER, 'BY PERIOD'),
    ]:
        rpt.h2(f'1.1 {label}')
        rows = []
        for grp in order:
            sub = obs[obs[groupby_col] == grp]
            if len(sub) == 0:
                continue
            for col in all_cols:
                if col not in sub.columns:
                    continue
                vals = sub[col].dropna()
                rows.append({
                    groupby_col: grp,
                    'element': col,
                    'N':     len(vals),
                    'mean':  vals.mean(),
                    'SD':    vals.std(ddof=1),
                    'min':   vals.min(),
                    'median':vals.median(),
                    'max':   vals.max(),
                    'CV%':   (vals.std(ddof=1) / vals.mean() * 100) if vals.mean() else np.nan,
                })
        tbl = pd.DataFrame(rows)
        rpt.table(tbl, float_fmt='{:.2f}')
        rpt.line()

    # Overall
    rpt.h2('1.2 OVERALL (all obsidian items)')
    rows = []
    for col in all_cols:
        if col not in obs.columns:
            continue
        vals = obs[col].dropna()
        rows.append({
            'element': col, 'N': len(vals),
            'mean': vals.mean(), 'SD': vals.std(ddof=1),
            'min': vals.min(), 'median': vals.median(), 'max': vals.max(),
        })
    rpt.table(pd.DataFrame(rows), float_fmt='{:.2f}')


# ──────────────────────────────────────────────────────────────────────────────
# 2. Significance tests
# ──────────────────────────────────────────────────────────────────────────────

def significance_tests(obs: pd.DataFrame, rpt: Report):
    rpt.h1('2. Significance Tests (Kruskal-Wallis + post-hoc Mann-Whitney)')
    rpt.line('Non-parametric tests used because normality is not assumed.')
    rpt.line('Alpha = 0.05. p < 0.05 = significant difference.')
    rpt.line()

    test_cols  = ELEMS + ['Rb/Zr', 'Nb/Zr', 'Rb/Nb']
    sites      = SITE_ORDER
    site_pairs = [('motza', 'einan'), ('motza', 'yiftahel'), ('einan', 'yiftahel')]

    kw_rows  = []
    mw_rows  = []

    for col in test_cols:
        if col not in obs.columns:
            continue
        groups = [obs[obs['site'] == s][col].dropna().values for s in sites]
        groups = [g for g in groups if len(g) >= 3]
        if len(groups) < 2:
            continue

        # Kruskal-Wallis
        try:
            stat, p = stats.kruskal(*groups)
            kw_rows.append({'element': col, 'H-stat': round(stat, 2),
                            'p-value': p, 'significant': 'YES' if p < 0.05 else 'no'})
        except Exception:
            pass

        # Pairwise Mann-Whitney U
        for s1, s2 in site_pairs:
            g1 = obs[obs['site'] == s1][col].dropna().values
            g2 = obs[obs['site'] == s2][col].dropna().values
            if len(g1) < 3 or len(g2) < 3:
                continue
            try:
                u, p2 = stats.mannwhitneyu(g1, g2, alternative='two-sided')
                mw_rows.append({
                    'element': col, 'group1': s1, 'group2': s2,
                    'U': round(u, 0), 'p-value': p2,
                    'significant': 'YES' if p2 < 0.05 else 'no',
                })
            except Exception:
                pass

    rpt.h2('2.1 Kruskal-Wallis (3-site comparison)')
    rpt.table(pd.DataFrame(kw_rows), float_fmt='{:.4f}')

    rpt.h2('2.2 Pairwise Mann-Whitney U')
    rpt.table(pd.DataFrame(mw_rows), float_fmt='{:.4f}')


# ──────────────────────────────────────────────────────────────────────────────
# 3. Biplots (internal — no reference sources)
# ──────────────────────────────────────────────────────────────────────────────

def _confidence_ellipse(x, y, ax, n_std=2.0, color='gray', alpha=0.15, lw=1.5):
    """Draw a 95% confidence ellipse (2 SD) for a set of (x, y) points."""
    if len(x) < 4:
        return
    cov  = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    w, h  = 2 * n_std * np.sqrt(np.abs(vals))
    ell   = mpatches.Ellipse(
        xy=(np.mean(x), np.mean(y)), width=w, height=h, angle=angle,
        facecolor=color, alpha=alpha, edgecolor=color, linewidth=lw,
    )
    ax.add_patch(ell)


def biplots(obs: pd.DataFrame, rpt: Report):
    rpt.h1('3. Biplots (Raw Values, Colour by Site)')

    pairs = [('Rb', 'Zr'), ('Nb', 'Zr'), ('Rb', 'Nb')]

    for x_el, y_el in pairs:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        for ax_idx, (use_ratio, suffix) in enumerate([(False, ''), (True, '_ratios')]):
            ax = axes[ax_idx]

            if use_ratio:
                # Axes become ratios Rb/Zr vs Nb/Zr etc.
                x_col = f'{x_el}/Zr' if x_el != 'Zr' else f'Rb/Zr'
                y_col = f'{y_el}/Zr' if y_el != 'Zr' else f'Nb/Zr'
                if x_col == y_col:
                    ax.axis('off')
                    continue
                ax.set_xlabel(x_col, fontsize=11)
                ax.set_ylabel(y_col, fontsize=11)
                ax.set_title(f'{x_col} vs {y_col}  (ratios, offset-robust)', fontsize=10)
            else:
                x_col, y_col = x_el, y_el
                ax.set_xlabel(f'{x_el} (ppm)', fontsize=11)
                ax.set_ylabel(f'{y_el} (ppm)', fontsize=11)
                ax.set_title(f'{x_el} vs {y_el}  (absolute ppm)', fontsize=10)

            handles = []
            for site in SITE_ORDER:
                sub = obs[obs['site'] == site][[x_col, y_col]].dropna()
                if len(sub) == 0:
                    continue
                c = SITE_COLORS[site]
                ax.scatter(sub[x_col], sub[y_col], c=c, alpha=0.5, s=20,
                           label=site, zorder=3)
                _confidence_ellipse(sub[x_col].values, sub[y_col].values,
                                    ax, color=c, n_std=2.0)
                handles.append(mpatches.Patch(color=c, label=site))

            ax.legend(handles=handles, fontsize=9)
            ax.grid(True, alpha=0.3)

        fname = FIGURES / f'biplot_{x_el}_{y_el}.png'
        plt.tight_layout()
        plt.savefig(fname, dpi=300)
        plt.close()
        rpt.line(f'  Saved: {fname.name}')

    rpt.line()
    rpt.line('Each figure: left = absolute ppm; right = element ratios (offset-robust).')
    rpt.line('Ellipses = 2 SD confidence region per site.')


# ──────────────────────────────────────────────────────────────────────────────
# 4. PCA
# ──────────────────────────────────────────────────────────────────────────────

def run_pca(obs: pd.DataFrame, rpt: Report) -> pd.DataFrame:
    rpt.h1('4. Principal Component Analysis (PCA)')
    rpt.line('Input:  Rb, Zr, Nb  (z-scored per element before PCA)')
    rpt.line('Items with any NaN in Rb/Zr/Nb excluded from PCA.')
    rpt.line()

    sub = obs[['item_id', 'site', 'period', 'Rb', 'Zr', 'Nb']].dropna()
    rpt.line(f'N items used in PCA: {len(sub)}')

    X = sub[['Rb', 'Zr', 'Nb']].values
    scaler = StandardScaler()
    X_sc   = scaler.fit_transform(X)

    pca  = PCA(n_components=3)
    pcs  = pca.fit_transform(X_sc)
    evr  = pca.explained_variance_ratio_

    rpt.h2('4.1 Explained Variance')
    for i, v in enumerate(evr):
        rpt.line(f'  PC{i+1}: {v*100:.1f}%  (cumulative: {evr[:i+1].sum()*100:.1f}%)')

    rpt.h2('4.2 Loadings (correlation of each element with each PC)')
    load_df = pd.DataFrame(
        pca.components_.T,
        index=['Rb', 'Zr', 'Nb'],
        columns=['PC1', 'PC2', 'PC3']
    )
    rpt.table(load_df, float_fmt='{:.3f}')

    sub = sub.copy()
    sub['PC1'] = pcs[:, 0]
    sub['PC2'] = pcs[:, 1]
    sub['PC3'] = pcs[:, 2]

    # Plot PC1 vs PC2 coloured by site
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, color_by, palette, label in [
        (axes[0], 'site',   SITE_COLORS,  'Site'),
        (axes[1], 'period', {p: plt.cm.Set1(i/4) for i, p in enumerate(PERIOD_ORDER)}, 'Period'),
    ]:
        for grp, color in palette.items():
            mask = sub[color_by] == grp
            s = sub[mask]
            if len(s) == 0:
                continue
            ax.scatter(s['PC1'], s['PC2'], c=[color], alpha=0.55, s=22,
                       label=grp, zorder=3)
            _confidence_ellipse(s['PC1'].values, s['PC2'].values,
                                ax, color=color, n_std=2.0)

        ax.set_xlabel(f'PC1 ({evr[0]*100:.1f}% variance)', fontsize=11)
        ax.set_ylabel(f'PC2 ({evr[1]*100:.1f}% variance)', fontsize=11)
        ax.set_title(f'PCA — coloured by {label}', fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    # Loadings overlay on left plot
    ax0 = axes[0]
    scale = 3.0
    for elem, (lx, ly) in zip(['Rb', 'Zr', 'Nb'],
                               zip(pca.components_[0], pca.components_[1])):
        ax0.annotate('', xy=(lx * scale, ly * scale), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
        ax0.text(lx * scale * 1.1, ly * scale * 1.1, elem,
                 ha='center', va='center', fontsize=9, color='black')

    plt.tight_layout()
    fname = FIGURES / 'pca_sites_periods.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'\n  Saved: {fname.name}')

    # Ratio-based PCA
    rpt.h2('4.3 PCA on element ratios (Rb/Zr, Nb/Zr, Rb/Nb)')

    ratio_cols = ['Rb/Zr', 'Nb/Zr', 'Rb/Nb']
    sub_r = obs[['item_id', 'site', 'period'] + ratio_cols].dropna()
    rpt.line(f'N items used in ratio-PCA: {len(sub_r)}')

    X_r   = StandardScaler().fit_transform(sub_r[ratio_cols].values)
    pca_r = PCA(n_components=3)
    pcs_r = pca_r.fit_transform(X_r)
    evr_r = pca_r.explained_variance_ratio_

    for i, v in enumerate(evr_r):
        rpt.line(f'  PC{i+1}: {v*100:.1f}%  (cumulative: {evr_r[:i+1].sum()*100:.1f}%)')

    sub_r = sub_r.copy()
    sub_r['PC1'] = pcs_r[:, 0]
    sub_r['PC2'] = pcs_r[:, 1]

    fig, ax = plt.subplots(figsize=(8, 6))
    for grp, color in SITE_COLORS.items():
        mask = sub_r['site'] == grp
        s = sub_r[mask]
        if len(s) == 0:
            continue
        ax.scatter(s['PC1'], s['PC2'], c=[color], alpha=0.55, s=22, label=grp, zorder=3)
        _confidence_ellipse(s['PC1'].values, s['PC2'].values, ax, color=color)
    ax.set_xlabel(f'PC1 ({evr_r[0]*100:.1f}%)', fontsize=11)
    ax.set_ylabel(f'PC2 ({evr_r[1]*100:.1f}%)', fontsize=11)
    ax.set_title('PCA on Rb/Zr, Nb/Zr, Rb/Nb ratios (offset-robust)', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fname = FIGURES / 'pca_ratios.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'  Saved: {fname.name}')

    return sub   # PC scores for use in clustering


# ──────────────────────────────────────────────────────────────────────────────
# 5. K-means clustering
# ──────────────────────────────────────────────────────────────────────────────

def kmeans_clustering(obs: pd.DataFrame, pc_sub: pd.DataFrame, rpt: Report):
    rpt.h1('5. K-Means Clustering (Rb / Zr / Nb, standardized)')

    sub   = obs[['item_id', 'site', 'period', 'Rb', 'Zr', 'Nb']].dropna()
    X     = StandardScaler().fit_transform(sub[['Rb', 'Zr', 'Nb']].values)
    k_range = range(2, 7)

    inertias   = []
    silhouettes = []

    for k in k_range:
        km  = KMeans(n_clusters=k, random_state=42, n_init=20)
        lbl = km.fit_predict(X)
        inertias.append(km.inertia_)
        sil = silhouette_score(X, lbl) if k > 1 else np.nan
        silhouettes.append(sil)

    # Elbow + silhouette figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(list(k_range), inertias, 'o-', color='steelblue')
    ax1.set_xlabel('Number of clusters k')
    ax1.set_ylabel('Inertia (within-cluster sum of squares)')
    ax1.set_title('Elbow curve')
    ax1.grid(True, alpha=0.3)

    ax2.plot(list(k_range), silhouettes, 's-', color='darkorange')
    ax2.set_xlabel('Number of clusters k')
    ax2.set_ylabel('Silhouette score')
    ax2.set_title('Silhouette score (higher = better separation)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fname = FIGURES / 'kmeans_elbow_silhouette.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'  Saved: {fname.name}')

    # Best k = highest silhouette
    best_k = list(k_range)[int(np.nanargmax(silhouettes))]
    rpt.h2(f'5.1 Best k = {best_k}  (silhouette = {silhouettes[list(k_range).index(best_k)]:.3f})')
    rpt.line()

    km_best  = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    labels   = km_best.fit_predict(X)
    sub      = sub.copy()
    sub['cluster'] = [f'C{l+1}' for l in labels]

    # Cross-tab cluster vs site
    rpt.h2('5.2 Cluster membership vs Site (count)')
    ct = pd.crosstab(sub['cluster'], sub['site'])
    rpt.table(ct, float_fmt='{:.0f}')
    rpt.line()

    rpt.h2('5.3 Cluster membership vs Period (count)')
    ct2 = pd.crosstab(sub['cluster'], sub['period'])
    rpt.table(ct2, float_fmt='{:.0f}')
    rpt.line()

    rpt.h2('5.4 Cluster centroids (ppm)')
    ctr_rows = []
    for cl in sorted(sub['cluster'].unique()):
        mask = sub['cluster'] == cl
        row  = {'cluster': cl, 'N': mask.sum()}
        for e in ELEMS:
            row[e] = sub.loc[mask, e].mean()
        ctr_rows.append(row)
    rpt.table(pd.DataFrame(ctr_rows), float_fmt='{:.1f}')

    # Scatter PC1/PC2 coloured by cluster
    merged = pc_sub.merge(sub[['item_id', 'cluster']], on='item_id', how='inner')
    fig, ax = plt.subplots(figsize=(8, 6))
    palette  = plt.cm.tab10.colors
    for i, cl in enumerate(sorted(merged['cluster'].unique())):
        s = merged[merged['cluster'] == cl]
        ax.scatter(s['PC1'], s['PC2'], c=[palette[i]], s=22, alpha=0.6,
                   label=cl, zorder=3)
    ax.set_xlabel('PC1', fontsize=11)
    ax.set_ylabel('PC2', fontsize=11)
    ax.set_title(f'K-means clusters (k={best_k}) in PCA space', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fname = FIGURES / f'kmeans_k{best_k}_pca.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'  Saved: {fname.name}')

    return sub, best_k


# ──────────────────────────────────────────────────────────────────────────────
# 6. Hierarchical clustering
# ──────────────────────────────────────────────────────────────────────────────

def hierarchical_clustering(obs: pd.DataFrame, best_k: int, rpt: Report):
    rpt.h1('6. Hierarchical Clustering (Ward linkage, Rb/Zr/Nb standardized)')

    sub   = obs[['item_id', 'site', 'period', 'Rb', 'Zr', 'Nb']].dropna()
    X     = StandardScaler().fit_transform(sub[['Rb', 'Zr', 'Nb']].values)
    Z     = linkage(X, method='ward')

    # Colour dendrogram leaves by site
    site_arr = sub['site'].values
    leaf_colors = {
        s: SITE_COLORS[s] for s in SITE_ORDER if s in SITE_COLORS
    }

    fig, ax = plt.subplots(figsize=(16, 5))
    d = dendrogram(Z, ax=ax, no_labels=True, color_threshold=0,
                   above_threshold_color='gray', leaf_rotation=90)
    # Colour leaves manually
    for idx, (leaf_x, leaf_site) in enumerate(zip(d['icoord'], site_arr[d['leaves']])):
        pass  # skip individual leaf colouring — dendrogram colors branches

    ax.set_title(f'Hierarchical clustering (Ward linkage, n={len(sub)})\n'
                 'branch colours: grey = above threshold (single tree)', fontsize=10)
    ax.set_ylabel('Distance')

    # Add horizontal line at distance corresponding to best_k groups
    cut = best_k
    # Find the cut distance that gives best_k clusters
    from scipy.cluster.hierarchy import fcluster
    for d_cut in np.linspace(Z[:, 2].max(), 0, 500):
        if len(np.unique(fcluster(Z, d_cut, criterion='distance'))) == cut:
            ax.axhline(d_cut, color='red', lw=1.5, linestyle='--',
                       label=f'Cut for k={cut}')
            break

    # Add legend patches for sites
    site_patches = [mpatches.Patch(color=c, label=s) for s, c in SITE_COLORS.items()]
    ax.legend(handles=site_patches, loc='upper right', fontsize=9, title='Sites')

    plt.tight_layout()
    fname = FIGURES / 'dendrogram.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'  Saved: {fname.name}')
    rpt.line(f'  Red dashed line = cut point for k={best_k} clusters.')
    rpt.line()

    # Cluster assignment cross-tab
    hc_labels = fcluster(Z, best_k, criterion='maxclust')
    sub = sub.copy()
    sub['hc_cluster'] = [f'HC{l}' for l in hc_labels]

    rpt.h2('6.1 Hierarchical cluster membership vs Site')
    ct = pd.crosstab(sub['hc_cluster'], sub['site'])
    rpt.table(ct, float_fmt='{:.0f}')
    rpt.line()

    rpt.h2('6.2 Cluster centroids (ppm)')
    ctr_rows = []
    for cl in sorted(sub['hc_cluster'].unique()):
        mask = sub['hc_cluster'] == cl
        row  = {'hc_cluster': cl, 'N': mask.sum()}
        for e in ELEMS:
            row[e] = sub.loc[mask, e].mean().round(1)
        ctr_rows.append(row)
    rpt.table(pd.DataFrame(ctr_rows), float_fmt='{:.1f}')


# ──────────────────────────────────────────────────────────────────────────────
# 7. Calibration note in report
# ──────────────────────────────────────────────────────────────────────────────

def calibration_note(rpt: Report):
    rpt.h1('7. Inter-Instrument Calibration Note')
    rpt.line("""
The user's Niton XL3t (Mining Cu/Zn mode, 60-second readings) has NOT been
validated against any known geological obsidian source sample that also appears
in the published reference datasets. This means absolute ppm values in
samples_clean.csv may carry a systematic offset relative to the reference
literature (which uses a mix of Niton Geo mode, Olympus DELTA, Bruker, EDXRF).

WHY THIS MATTERS:
  If the Niton Mining mode reads Rb as consistently 10% higher than the reference
  instrument, then comparing raw ppm to source centroids will shift all samples
  towards sources with higher Rb -- a systematic misattribution.

THREE STRATEGIES IMPLEMENTED IN THIS PROJECT TO MITIGATE THIS:

  1. Element ratios (Rb/Zr, Nb/Zr, Rb/Nb):
     If the calibration offset affects all heavy elements proportionally,
     ratios cancel the bias. Ratios are analysed in parallel with absolute values
     throughout this script and in Phases 4-5.
     LIMITATION: If different elements are offset differently (e.g. Rb over-read
     but Zr under-read), ratios will be biased in the opposite direction.

  2. Yiftahel ground truth:
     Yiftahel (MPPNB) was independently sourced by Yellin & Garfinkel (1986)
     using INAA -- a method free of pXRF calibration issues. Their result: EGD
     (Eastern Galilee Dikili Tash / Gollu Dag East). If Phase 5 Mahalanobis
     attribution places Yiftahel closest to EGD, we have implicit validation
     that the instrument offset is not large enough to cause misattribution.
     If Yiftahel does NOT cluster with EGD, we should estimate and apply a
     per-element offset correction before attributing Motza and Einan.

  3. PCA-space comparison (Phase 4-5):
     Plotting samples in PCA space alongside reference sources partially
     absorbs uniform scaling offsets because PCA is relative. A systematic
     shift of all samples by +10% Rb will shift them along the Rb principal
     component axis uniformly, which may still allow correct cluster assignment.

RECOMMENDED FUTURE STEP (if resources allow):
  Measure 3-5 obsidian pieces of known geological origin (e.g. from the
  reference collection at the Hebrew University, or from geological samples
  used in published studies) with the same Niton instrument and settings.
  Compare the readings to published values for those sources to derive
  per-element correction factors (slope + intercept).
""")


# ──────────────────────────────────────────────────────────────────────────────
# 8. Distribution plots
# ──────────────────────────────────────────────────────────────────────────────

def distribution_plots(obs: pd.DataFrame, rpt: Report):
    rpt.h1('8. Element Distributions by Site')

    all_cols = ELEMS + ['Rb/Zr', 'Nb/Zr', 'Rb/Nb']

    fig, axes = plt.subplots(len(all_cols), 1, figsize=(10, 3 * len(all_cols)))

    for i, col in enumerate(all_cols):
        ax = axes[i]
        for site in SITE_ORDER:
            vals = obs[obs['site'] == site][col].dropna()
            if len(vals) == 0:
                continue
            vals.plot.kde(ax=ax, label=site, color=SITE_COLORS[site],
                          bw_method=0.4, linewidth=2)
            ax.axvline(vals.median(), color=SITE_COLORS[site],
                       linestyle='--', linewidth=1, alpha=0.7)
        ax.set_xlabel(col)
        ax.set_ylabel('Density')
        ax.set_title(f'{col} distribution by site (dashed = median)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.25)

    plt.tight_layout()
    fname = FIGURES / 'distributions_by_site.png'
    plt.savefig(fname, dpi=300)
    plt.close()
    rpt.line(f'  Saved: {fname.name}')


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print('=== Phase 3b: Internal Statistics ===\n')

    obs = load_obsidian()
    rpt = Report(REPORT)

    rpt.h1('Phase 3b -- Internal Statistics Report')
    rpt.line(f'Date: 2026-03-26')
    rpt.line(f'Input: {SAMPLES / "samples_clean.csv"}')
    rpt.line(f'N obsidian items: {len(obs)}')
    rpt.line(f'Sites: {obs["site"].value_counts().to_dict()}')
    rpt.line(f'Periods: {obs["period"].value_counts().to_dict()}')
    rpt.line()
    rpt.line('ELEMENT RATIOS COMPUTED: Rb/Zr, Nb/Zr, Rb/Nb')
    rpt.line('These ratios are robust to uniform inter-instrument calibration offsets.')
    rpt.line('Analysed in parallel with absolute ppm values throughout.')

    print('Running descriptive stats...')
    descriptive_stats(obs, rpt)

    print('Running significance tests...')
    significance_tests(obs, rpt)

    print('Generating biplots...')
    biplots(obs, rpt)

    print('Running PCA...')
    pc_sub = run_pca(obs, rpt)

    print('Running k-means...')
    km_sub, best_k = kmeans_clustering(obs, pc_sub, rpt)

    print('Running hierarchical clustering...')
    hierarchical_clustering(obs, best_k, rpt)

    print('Writing calibration note...')
    calibration_note(rpt)

    print('Generating distribution plots...')
    distribution_plots(obs, rpt)

    rpt.h1('Summary of Figures Generated')
    for f in sorted(FIGURES.glob('*.png')):
        rpt.line(f'  {f.name}')

    rpt.save()
    print(f'\nDone. {len(list(FIGURES.glob("*.png")))} figures in {FIGURES}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Phase 5 -- Source attribution via Mahalanobis distance

For each obsidian artifact in samples_clean.csv, compute the Mahalanobis
distance to each reference source (Tier 1, strong/moderate quality) in:

  PRIMARY:   Zr / Nb space      (calibration-robust, 2 elements, df=2)
  SECONDARY: Rb / Zr / Nb space (Rb scaled x2 to correct for instrument offset, df=3)

Assigns each artifact to the nearest source, reports chi-squared p-values.

Outputs:
  outputs/reports/source_attribution.csv        -- per-artifact table
  outputs/reports/source_attribution_report.txt -- plain-language summary
  outputs/figures/attribution/biplot_Nb_Zr_attributed.png
  outputs/figures/attribution/biplot_Nb_Zr_log.png
  outputs/figures/attribution/biplot_Rb_Zr_attributed.png
  outputs/figures/attribution/ratio_NbZr_comparison.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
from scipy.stats import chi2

# ---- paths ----------------------------------------------------------------
ROOT      = Path(__file__).parent.parent
REF_CSV   = ROOT / 'reference_database' / 'tier1_comparison_ready.csv'
CLEAN_CSV = ROOT / 'my_samples' / 'samples_clean.csv'
FIGS      = ROOT / 'outputs' / 'figures' / 'attribution'
REPORTS   = ROOT / 'outputs' / 'reports'
FIGS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

REPORT     = REPORTS / 'source_attribution_report.txt'
ATTRIB_CSV = REPORTS / 'source_attribution.csv'

# ---- configuration --------------------------------------------------------
# Levant-relevant sources only (excludes Aegean, Carpathian, etc.)
LEVANT_RELEVANT_SOURCES = [
    'BingolA', 'BingolB', 'EGD', 'GolluDag', 'ND', 'NemrutDag',
    'MeydanDag', 'Mus', 'Group3d',
]
# Minimum N per source to compute a covariance matrix
MIN_N = 5

# Calibration correction: Niton Mining Cu/Zn mode under-reads Rb by ~2x
# relative to geo-mode and lab instruments.  Applied only in secondary (3-el) run.
RB_SCALE = 2.0

# chi-squared threshold for 95% confidence ellipse / interval
# With df degrees of freedom: sqrt(chi2.ppf(0.95, df)) gives the Mahalanobis
# radius at which a point lies on the 95% boundary.
CHI2_95_2DF = chi2.ppf(0.95, df=2)  # ~5.991
CHI2_95_3DF = chi2.ppf(0.95, df=3)  # ~7.815

SITE_COLORS  = {'motza': '#2196F3', 'einan': '#4CAF50', 'yiftahel': '#FF5722'}
SITE_MARKERS = {'motza': 's',       'einan': 'D',       'yiftahel': '^'}

SOURCE_PALETTE = [
    '#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4',
    '#42d4f4', '#f032e6', '#bfef45', '#469990', '#dcbeff', '#9A6324',
]


# ---- geometry helpers -----------------------------------------------------

def confidence_ellipse_patch(mean2d, cov2d, n_std, **kwargs):
    """
    Return a matplotlib Ellipse patch for the Mahalanobis ellipse.

    n_std = sqrt(chi2.ppf(confidence, df=2)):
      95% -> n_std = sqrt(5.991) = 2.4477
      68% -> n_std = sqrt(2.296) = 1.515
    """
    eigvals, eigvecs = np.linalg.eigh(cov2d)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    angle  = np.degrees(np.arctan2(*eigvecs[:, 0][::-1]))
    width  = 2 * n_std * np.sqrt(max(eigvals[0], 0))
    height = 2 * n_std * np.sqrt(max(eigvals[1], 0))
    return Ellipse(xy=mean2d, width=width, height=height, angle=angle, **kwargs)


def mahal(x, mean, cov_inv, df):
    """
    Mahalanobis D^2, D_M, and chi-squared p-value.
    Returns (D_M, D2, p) or (nan, nan, nan) on singular matrix.
    """
    try:
        diff = np.asarray(x, dtype=float) - np.asarray(mean, dtype=float)
        d2   = float(diff @ cov_inv @ diff)
        d_m  = float(np.sqrt(max(d2, 0.0)))
        p    = float(1.0 - chi2.cdf(d2, df=df))
        return d_m, d2, p
    except Exception:
        return np.nan, np.nan, np.nan


# ---- source statistics ----------------------------------------------------

def build_source_stats(ref_df, elements):
    """
    Per source: compute mean vector, covariance matrix, and its inverse.
    Only sources with N >= MIN_N complete rows are included.
    Returns dict: source -> {mean, cov, cov_inv, n}
    """
    stats = {}
    for source, grp in ref_df.groupby('source'):
        sub = grp[elements].dropna()
        if len(sub) < MIN_N:
            continue
        cov = sub.cov().values
        # Guard against singular (near-zero variance in one element for small N)
        try:
            cov_inv = np.linalg.inv(cov)
        except np.linalg.LinAlgError:
            continue
        if np.any(np.isnan(cov_inv)):
            continue
        stats[source] = {
            'mean':    sub.mean().values,
            'cov':     cov,
            'cov_inv': cov_inv,
            'n':       len(sub),
        }
    return stats


# ---- attribution ----------------------------------------------------------

def attribute_samples(samples, source_stats, elements):
    """
    For each artifact (row in samples with non-NaN elements), compute D_M
    to every source and record the best assignment.

    Returns a DataFrame with columns:
      item_id, site, period,
      d2_<source>, p_<source>  (per source),
      best_source, best_d2, best_p, confident
    """
    valid = samples.dropna(subset=elements).copy()
    df = int(len(elements))
    records = []

    for _, row in valid.iterrows():
        x_vec = row[elements].values.astype(float)
        rec   = {'item_id': row['item_id'], 'site': row['site'],
                 'period': row.get('period', '')}
        best_src, best_d2, best_p = None, np.inf, 0.0

        for src, s in source_stats.items():
            _, d2, p = mahal(x_vec, s['mean'], s['cov_inv'], df)
            rec[f'd2_{src}'] = round(d2, 3) if not np.isnan(d2) else np.nan
            rec[f'p_{src}']  = round(p,  4) if not np.isnan(p)  else np.nan
            if not np.isnan(d2) and d2 < best_d2:
                best_d2, best_src, best_p = d2, src, p

        rec['best_source'] = best_src
        rec['best_d2']     = round(best_d2, 3) if best_src else np.nan
        rec['best_p']      = round(best_p,  4) if best_src else np.nan
        rec['confident']   = bool(best_p >= 0.05)  # within 95% ellipse
        records.append(rec)

    return pd.DataFrame(records)  # after all rows processed


# ---- plotting -------------------------------------------------------------

def biplot_ellipses(ref_df, src_stats, samples_df,
                    x_col, y_col, xlabel, ylabel, title, outpath,
                    logscale=False):
    """
    Scatter plot with:
      - 95% Mahalanobis confidence ellipses per source (filled, translucent)
      - reference cloud scatter (small, translucent)
      - sample points coloured by site
    """
    source_list = list(src_stats.keys())
    colors_map  = {s: SOURCE_PALETTE[i % len(SOURCE_PALETTE)]
                   for i, s in enumerate(source_list)}

    fig, ax = plt.subplots(figsize=(11, 8))
    legend_handles = []

    for src in source_list:
        s  = src_stats[src]
        c  = colors_map[src]
        m2 = s['mean']
        cv = s['cov']

        # Reference cloud (tiny dots)
        sub = ref_df[ref_df['source'] == src][[x_col, y_col]].dropna()
        ax.scatter(sub[x_col], sub[y_col], c=c, alpha=0.12, s=7, zorder=2)

        if not logscale:
            # 95% ellipse
            patch = confidence_ellipse_patch(
                m2, cv, n_std=np.sqrt(CHI2_95_2DF),
                facecolor=c, alpha=0.18, edgecolor=c, linewidth=1.8, zorder=3)
            ax.add_patch(patch)

        # Centroid cross
        ax.plot(m2[0], m2[1], 'x', color=c, markersize=9,
                markeredgewidth=2.2, zorder=5)
        ax.annotate(src, xy=(m2[0], m2[1]), fontsize=7.5,
                    color=c, fontweight='bold', ha='center', va='bottom',
                    xytext=(0, 7), textcoords='offset points')
        legend_handles.append(
            mpatches.Patch(facecolor=c, edgecolor=c, alpha=0.5, label=src))

    # Sample scatter
    for site in ['motza', 'einan', 'yiftahel']:
        sub = samples_df[samples_df['site'] == site][[x_col, y_col]].dropna()
        if sub.empty:
            continue
        ax.scatter(sub[x_col], sub[y_col],
                   c=SITE_COLORS[site], marker=SITE_MARKERS[site],
                   s=28, zorder=6, alpha=0.85,
                   linewidths=0.4, edgecolors='black')
        legend_handles.append(
            mpatches.Patch(facecolor=SITE_COLORS[site],
                           label=f'{site.capitalize()} (our samples)'))

    if logscale:
        ax.set_xscale('log')
        ax.set_yscale('log')

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=12)
    ax.legend(handles=legend_handles, fontsize=7, loc='upper right',
              ncol=2, framealpha=0.85)
    ax.grid(True, alpha=0.3, which='both' if logscale else 'major')
    fig.tight_layout()
    fig.savefig(outpath, dpi=200)
    plt.close(fig)
    print(f"  Saved: {outpath.name}")


def ratio_strip_plot(ref_df, src_stats, samples_df, x_col, y_col,
                     ratio_name, outpath):
    """
    Horizontal strip chart of Nb/Zr ratio: sources (IQR box) vs sample
    assemblage medians (vertical dashed lines).
    """
    rows = []
    for src in src_stats:
        sub = ref_df[ref_df['source'] == src][[x_col, y_col]].dropna()
        if len(sub) < 3:
            continue
        r = sub[y_col] / sub[x_col]
        rows.append({'source': src, 'median': r.median(),
                     'q25': r.quantile(0.25), 'q75': r.quantile(0.75)})
    ref_df2 = pd.DataFrame(rows).sort_values('median').reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ypos = list(range(len(ref_df2)))
    ax.barh(ypos,
            ref_df2['q75'] - ref_df2['q25'],
            left=ref_df2['q25'],
            color='lightsteelblue', edgecolor='steelblue',
            alpha=0.65, label='Reference IQR')
    ax.scatter(ref_df2['median'], ypos,
               color='steelblue', s=55, zorder=5, label='Reference median')
    ax.set_yticks(ypos)
    ax.set_yticklabels(ref_df2['source'].tolist(), fontsize=9)

    samp = samples_df[[x_col, y_col, 'site']].dropna()
    for site in ['motza', 'einan', 'yiftahel']:
        r = samp[samp['site'] == site][y_col] / samp[samp['site'] == site][x_col]
        if r.empty:
            continue
        ax.axvline(r.median(), color=SITE_COLORS[site], linestyle='--',
                   linewidth=2, alpha=0.9,
                   label=f'{site.capitalize()} median ({r.median():.3f})')

    ax.set_xlabel(f'{ratio_name} ratio', fontsize=12)
    ax.set_title(f'{ratio_name}: reference sources vs our assemblage\n'
                 '(IQR boxes = source geochemical range; dashed = sample median)',
                 fontsize=11)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.3, axis='x')
    fig.tight_layout()
    fig.savefig(outpath, dpi=200)
    plt.close(fig)
    print(f"  Saved: {outpath.name}")


# ---- main -----------------------------------------------------------------

def main():
    lines = []

    def log(s=''):
        print(s)
        lines.append(str(s))

    ref_all     = pd.read_csv(REF_CSV)
    samples_all = pd.read_csv(CLEAN_CSV)

    # Reference: Tier 1 only, levant-relevant sources, strong or moderate quality
    ref_t1 = ref_all[
        (ref_all['method_tier'] == 1) &
        (ref_all['source'].isin(LEVANT_RELEVANT_SOURCES)) &
        (ref_all['ref_quality'].isin(['strong', 'moderate']))
    ].copy()

    # Samples: obsidian only
    samples = samples_all[samples_all['material'] == 'obsidian'].copy()

    log("=" * 70)
    log("PHASE 5 -- OBSIDIAN SOURCE ATTRIBUTION (Mahalanobis Distance)")
    log("=" * 70)
    log(f"Reference: {ref_t1['source'].nunique()} Tier-1 sources, {len(ref_t1)} rows")
    log(f"Samples:   {len(samples)} obsidian items")
    log(f"Elements:  PRIMARY = Zr/Nb (calibration-robust)")
    log(f"           SECONDARY = Rb(x{RB_SCALE})/Zr/Nb (Rb scaled for instrument offset)")
    log()

    # ==============================================================
    # PRIMARY: 2-element Zr/Nb
    # ==============================================================
    ELEMS_2   = ['Zr', 'Nb']
    stats_2el = build_source_stats(ref_t1, ELEMS_2)

    log("PRIMARY: Zr/Nb (2-element, df=2)")
    log("-" * 45)
    for src, s in sorted(stats_2el.items()):
        log(f"  {src:22s}  N={s['n']:4d}  "
            f"Zr={s['mean'][0]:7.1f}  Nb={s['mean'][1]:6.1f}")
    log()

    res_2el = attribute_samples(samples, stats_2el, ELEMS_2)

    # ==============================================================
    # SECONDARY: 3-element Rb(scaled)/Zr/Nb
    # ==============================================================
    ELEMS_3     = ['Rb', 'Zr', 'Nb']
    samples_3el = samples.copy()
    samples_3el['Rb'] = samples_3el['Rb'] * RB_SCALE  # correct for under-read

    stats_3el = build_source_stats(ref_t1, ELEMS_3)

    log("SECONDARY: Rb(x2)/Zr/Nb (3-element, df=3)")
    log("-" * 45)
    for src, s in sorted(stats_3el.items()):
        log(f"  {src:22s}  N={s['n']:4d}  "
            f"Rb={s['mean'][0]:7.1f}  Zr={s['mean'][1]:7.1f}  Nb={s['mean'][2]:6.1f}")
    log()

    res_3el = attribute_samples(samples_3el, stats_3el, ELEMS_3)

    # Rename 3-el columns to avoid clash
    res_3el = res_3el.rename(columns={
        'best_source': 'best_source_3el',
        'best_d2':     'best_d2_3el',
        'best_p':      'best_p_3el',
        'confident':   'confident_3el',
    })

    # ==============================================================
    # Merge results + raw values
    # ==============================================================
    keep_cols = ['item_id', 'quality_flag', 'divergent_elements',
                 'locus', 'basket', 'Rb', 'Zr', 'Nb']
    merged = (
        res_2el[['item_id', 'site', 'period',
                 'best_source', 'best_d2', 'best_p', 'confident']]
        .merge(res_3el[['item_id', 'best_source_3el',
                         'best_d2_3el', 'best_p_3el', 'confident_3el']],
               on='item_id', how='left')
        .merge(samples_all[keep_cols], on='item_id', how='left')
    )
    merged['2el_3el_agree'] = merged['best_source'] == merged['best_source_3el']
    merged.to_csv(ATTRIB_CSV, index=False)
    log(f"Attribution table saved: {ATTRIB_CSV.name}  ({len(merged)} rows)")
    log()

    # ==============================================================
    # RESULTS SUMMARY
    # ==============================================================
    log("=" * 70)
    log("RESULTS")
    log("=" * 70)
    total     = len(merged)
    confident = merged['confident'].sum()
    agree     = merged['2el_3el_agree'].sum()
    log(f"Total items:                {total}")
    log(f"Confident (within 95% CI): {confident} ({100*confident/total:.1f}%)")
    log(f"2-el and 3-el agree:        {agree}   ({100*agree/total:.1f}%)")
    log()

    for site in ['motza', 'einan', 'yiftahel']:
        sub = merged[merged['site'] == site]
        if sub.empty:
            continue
        log(f"{site.upper()}  (N={len(sub)}):")
        counts = sub['best_source'].value_counts()
        for src, cnt in counts.items():
            pct  = 100 * cnt / len(sub)
            conf = int((sub[sub['best_source'] == src]['confident']).sum())
            log(f"  {src:24s} {cnt:4d} ({pct:5.1f}%)  confident: {conf}")
        log()

    # Detail on the yif_10671 outlier
    yif_row = merged[merged['item_id'] == 'yif_10671']
    if len(yif_row):
        r = yif_row.iloc[0]
        log("YIFTAHEL OUTLIER: yif_10671")
        log(f"  Raw ppm:  Rb={r.get('Rb',float('nan')):.0f}  "
            f"Zr={r.get('Zr',float('nan')):.0f}  Nb={r.get('Nb',float('nan')):.0f}")
        log(f"  2-el attribution: {r['best_source']}  "
            f"(D^2={r['best_d2']:.2f}, p={r['best_p']:.4f})")
        log(f"  3-el attribution: {r['best_source_3el']}  "
            f"(D^2={r['best_d2_3el']:.2f}, p={r['best_p_3el']:.4f})")
        log()

    # Items outside ALL 95% ellipses (low confidence)
    unconf = merged[~merged['confident']]
    if len(unconf):
        log(f"OUTSIDE 95% ELLIPSE (N={len(unconf)}) -- ambiguous or uncovered sources:")
        for _, r in unconf.iterrows():
            log(f"  {r['item_id']:22s}  site={r['site']:10s}  "
                f"nearest={r['best_source']}  p={r['best_p']:.4f}")
        log()

    # Per-source how many confident
    log("CONFIDENT ATTRIBUTIONS PER SOURCE (2-element primary):")
    conf_src = merged[merged['confident']]['best_source'].value_counts()
    for src, cnt in conf_src.items():
        log(f"  {src:24s}: {cnt:4d}")
    log()

    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\nReport written: {REPORT}")

    # ==============================================================
    # FIGURES
    # ==============================================================
    print("\nGenerating figures...")

    # 1. Nb vs Zr -- linear scale with 95% ellipses
    biplot_ellipses(
        ref_t1, stats_2el, samples,
        x_col='Zr', y_col='Nb',
        xlabel='Zr (ppm)', ylabel='Nb (ppm)',
        title='Source attribution: Nb vs Zr\n'
              '(shaded = 95% Mahalanobis ellipses, Tier 1 sources)',
        outpath=FIGS / 'biplot_Nb_Zr_attributed.png',
    )

    # 2. Nb vs Zr -- log scale (separates peralkaline sources)
    biplot_ellipses(
        ref_t1, stats_2el, samples,
        x_col='Zr', y_col='Nb',
        xlabel='Zr (ppm) [log]', ylabel='Nb (ppm) [log]',
        title='Source attribution: Nb vs Zr (log scale)\n'
              '(reference clouds + sample overlay)',
        outpath=FIGS / 'biplot_Nb_Zr_log.png',
        logscale=True,
    )

    # 3. Rb vs Zr (calibration offset visible between source ellipses and samples)
    stats_rb_zr = build_source_stats(ref_t1, ['Rb', 'Zr'])
    biplot_ellipses(
        ref_t1, stats_rb_zr, samples,
        x_col='Rb', y_col='Zr',
        xlabel='Rb (ppm)  [samples under-read ~2x vs reference]',
        ylabel='Zr (ppm)',
        title='Rb vs Zr with 95% source ellipses\n'
              '(Note: sample Rb is ~half of reference -- calibration offset)',
        outpath=FIGS / 'biplot_Rb_Zr_attributed.png',
    )

    # 4. Nb/Zr ratio strip chart
    ratio_strip_plot(
        ref_t1, stats_2el, samples,
        x_col='Zr', y_col='Nb',
        ratio_name='Nb/Zr',
        outpath=FIGS / 'ratio_NbZr_comparison.png',
    )

    # 5. Per-site source pie charts
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for ax, site in zip(axes, ['motza', 'einan', 'yiftahel']):
        sub = merged[merged['site'] == site]
        if sub.empty:
            ax.set_visible(False)
            continue
        counts = sub['best_source'].value_counts()
        pal = [SOURCE_PALETTE[list(stats_2el.keys()).index(s)
                              % len(SOURCE_PALETTE)]
               if s in stats_2el else 'gray'
               for s in counts.index]
        ax.pie(counts.values, labels=counts.index, colors=pal,
               autopct='%1.0f%%', startangle=90,
               textprops={'fontsize': 8})
        ax.set_title(f'{site.capitalize()}\n(N={len(sub)})', fontsize=11)
    fig.suptitle('Source attribution by site (primary: Zr/Nb)', fontsize=12)
    fig.tight_layout()
    fig.savefig(FIGS / 'attribution_pie_by_site.png', dpi=200)
    plt.close(fig)
    print(f"  Saved: attribution_pie_by_site.png")

    n_figs = len(list(FIGS.glob('*.png')))
    print(f"\nPhase 5 complete. {n_figs} figures in {FIGS.relative_to(ROOT)}")


if __name__ == '__main__':
    main()

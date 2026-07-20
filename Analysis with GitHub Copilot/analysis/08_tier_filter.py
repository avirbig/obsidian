"""
Phase 4: Tier/quality filtering -- build the comparison-ready reference subset.

Outputs:
  reference_database/tier1_comparison_ready.csv
      All Tier 1 (pXRF/EDXRF) rows; adds columns:
        ref_quality   -- 'strong' (N>=10), 'moderate' (N>=3), 'weak' (N<3)
        heavy5_cover  -- count of heavy-5 elements (Rb/Sr/Zr/Nb/Y) measured in
                         this specific row (useful for geometry-effect weighting)

  reference_database/source_comparison_fingerprints.csv
      One row per source; the mean/SD/N for each of Rb/Sr/Zr/Nb/Y drawn from
      the BEST available tier (Tier 1 preferred, then Tier 2, then Tier 3).
      Used directly by Phase 5b for source attribution.
      Columns:
        source, best_tier, ref_quality, usable_elements,
        N_Rb, mean_Rb, sd_Rb, N_Sr, mean_Sr, sd_Sr,
        N_Zr, mean_Zr, sd_Zr, N_Nb, mean_Nb, sd_Nb,
        N_Y, mean_Y, sd_Y

  reference_database/phase4_report.txt
      Human-readable summary.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT   = Path(r'c:\work\code\obsidian')
CLEAN  = ROOT / 'reference_database' / 'cleaned'
OUTDIR = ROOT / 'reference_database'

HEAVY5 = ['Rb', 'Sr', 'Zr', 'Nb', 'Y']
EXTRA  = ['Fe', 'Mn', 'Zn', 'Ti', 'Ba', 'Th', 'Pb', 'Ga']

QUALITY_THRESHOLDS = {'strong': 10, 'moderate': 3}   # N >= threshold

TIER_LABELS = {1: 'pXRF/EDXRF', 2: 'ICP-MS/INAA', 3: 'XRF (lab)', 4: 'NAA (REE)'}


def load_master() -> pd.DataFrame:
    df = pd.read_csv(CLEAN / 'all_sources_cleaned.csv')
    # Coerce element columns to numeric
    for col in HEAVY5 + EXTRA:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def assign_quality(n: int) -> str:
    if n >= QUALITY_THRESHOLDS['strong']:
        return 'strong'
    if n >= QUALITY_THRESHOLDS['moderate']:
        return 'moderate'
    return 'weak'


def build_tier1_ready(df: pd.DataFrame) -> pd.DataFrame:
    """Return Tier 1 rows with ref_quality and heavy5_cover columns added."""
    t1 = df[df['method_tier'] == 1].copy()

    # Per-source N for quality flag
    source_n = t1.groupby('source').size().rename('source_n')
    t1 = t1.join(source_n, on='source')
    t1['ref_quality'] = t1['source_n'].apply(assign_quality)
    t1 = t1.drop(columns=['source_n'])

    # Per-row heavy5 coverage count
    t1['heavy5_cover'] = t1[HEAVY5].notna().sum(axis=1)

    return t1.reset_index(drop=True)


def best_tier_stats(df: pd.DataFrame, source: str) -> dict:
    """
    For a given source, pick the best available tier (1 > 2 > 3 > 4) and
    compute per-element N/mean/SD for Rb/Sr/Zr/Nb/Y.
    Returns a dict ready to become a row in the fingerprints CSV.
    """
    src = df[df['source'] == source]
    best_tier = None
    for tier in [1, 2, 3, 4]:
        if (src['method_tier'] == tier).any():
            best_tier = tier
            break

    if best_tier is None:
        return {}

    grp = src[src['method_tier'] == best_tier]
    n_total = len(grp)
    quality = assign_quality(n_total)

    row = {
        'source':     source,
        'best_tier':  best_tier,
        'tier_label': TIER_LABELS.get(best_tier, str(best_tier)),
        'ref_quality': quality,
        'n_total':    n_total,
    }

    usable = []
    for e in HEAVY5:
        if e not in grp.columns:
            row[f'N_{e}'] = 0
            row[f'mean_{e}'] = np.nan
            row[f'sd_{e}'] = np.nan
            continue
        vals = grp[e].dropna()
        n_e = len(vals)
        row[f'N_{e}']    = n_e
        row[f'mean_{e}'] = round(vals.mean(), 2) if n_e else np.nan
        row[f'sd_{e}']   = round(vals.std(ddof=1), 2) if n_e > 1 else np.nan
        if n_e >= 3:
            usable.append(e)

    row['usable_elements'] = ','.join(usable)  # elements with N>=3 for covariance
    return row


def build_fingerprints(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for source in sorted(df['source'].dropna().unique()):
        r = best_tier_stats(df, source)
        if r:
            records.append(r)
    fp = pd.DataFrame(records)
    col_order = (
        ['source', 'best_tier', 'tier_label', 'ref_quality', 'n_total', 'usable_elements']
        + [f'{p}_{e}' for e in HEAVY5 for p in ['N', 'mean', 'sd']]
    )
    col_order = [c for c in col_order if c in fp.columns]
    return fp[col_order].reset_index(drop=True)


def build_report(df: pd.DataFrame, t1: pd.DataFrame, fp: pd.DataFrame) -> str:
    lines = []
    sep = '=' * 70

    lines += [
        'PHASE 4 -- TIER/QUALITY FILTER  (comparison-ready reference subset)',
        sep,
        f'Master rows:    {len(df)}',
        f'Tier 1 rows:    {len(t1)}  (pXRF/EDXRF -- primary comparison tier)',
        f'Unique sources: {df["source"].nunique()}  total  |  '
        f'{t1["source"].nunique()} with Tier 1 data',
        '',
        'QUALITY FLAGS (based on Tier 1 N per source):',
        '  strong   -- N >= 10  (reliable mean + SD, usable for Mahalanobis distance)',
        '  moderate -- N >= 3   (usable mean, SD less stable)',
        '  weak     -- N < 3    (single-point or duplicate; treat as indicative only)',
        '  no_pxrf  -- no Tier 1 data at all (Tier 2/3 fingerprint used in fallback col)',
        '',
    ]

    # Quality breakdown (Tier 1 sources)
    quality_counts = t1.groupby('source')['ref_quality'].first().value_counts()
    lines.append('Tier 1 source quality breakdown:')
    for q in ['strong', 'moderate', 'weak']:
        n = quality_counts.get(q, 0)
        srcs = sorted(t1[t1['ref_quality'] == q]['source'].dropna().unique())
        lines.append(f'  {q:10s}: {n} sources  -- {", ".join(srcs)}')
    lines.append('')

    # Sources with no Tier 1
    all_sources = set(df['source'].dropna().unique())
    t1_sources  = set(t1['source'].dropna().unique())
    no_pxrf = sorted(all_sources - t1_sources)
    lines.append(f'Sources with NO Tier 1 data ({len(no_pxrf)}):')
    lines.append(f'  {", ".join(no_pxrf)}')
    lines.append('')

    # Fingerprint table
    lines += [
        sep,
        'SOURCE COMPARISON FINGERPRINTS  (mean +/- SD, ppm)',
        'Best tier used per source; elements shown only if N>=3 in that tier.',
        sep,
        '',
        f'{"Source":<16} {"BestTier":>8} {"Quality":>10} {"N":>5}  '
        f'{"Rb":>8}  {"Sr":>8}  {"Zr":>8}  {"Nb":>8}  {"Y":>8}  {"Usable":>20}',
        '-' * 110,
    ]

    def fmt(val):
        return f'{val:7.1f}' if not pd.isna(val) else '    --  '

    for _, r in fp.iterrows():
        tier_lbl = f"T{int(r['best_tier'])}"
        lines.append(
            f'{r["source"]:<16} {tier_lbl:>8} {r["ref_quality"]:>10} {int(r["n_total"]):>5}  '
            f'{fmt(r["mean_Rb"])}  {fmt(r["mean_Sr"])}  '
            f'{fmt(r["mean_Zr"])}  {fmt(r["mean_Nb"])}  '
            f'{fmt(r["mean_Y"])}  {r["usable_elements"]:>20}'
        )

    lines += [
        '',
        sep,
        'ELEMENT COVERAGE IN TIER 1 ROWS',
        sep,
    ]
    for e in HEAVY5 + EXTRA:
        if e in t1.columns:
            nn = t1[e].notna().sum()
            pct = nn / len(t1) * 100
            lines.append(f'  {e:4s}: {nn:5d} / {len(t1):5d}  ({pct:.0f}%)')

    lines += [
        '',
        'Files written:',
        '  reference_database/tier1_comparison_ready.csv',
        '  reference_database/source_comparison_fingerprints.csv',
        '  reference_database/phase4_report.txt',
    ]

    return '\n'.join(lines) + '\n'


def main():
    df = load_master()
    print(f'Master: {len(df)} rows, {df["source"].nunique()} sources')

    t1 = build_tier1_ready(df)
    print(f'Tier 1 rows: {len(t1)}')

    fp = build_fingerprints(df)
    print(f'Fingerprints: {len(fp)} sources')

    report = build_report(df, t1, fp)

    # Write outputs
    t1.to_csv(OUTDIR / 'tier1_comparison_ready.csv', index=False)
    fp.to_csv(OUTDIR / 'source_comparison_fingerprints.csv', index=False)
    (OUTDIR / 'phase4_report.txt').write_text(report, encoding='utf-8')

    print(report)


if __name__ == '__main__':
    main()

"""
Phase 3: Per-source statistical summaries.

Outputs:
  reference_database/source_statistics.csv       -- one row per (source, tier) with N/mean/SD/min/max per element
  reference_database/source_statistics_report.txt -- human-readable fingerprint table
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT   = Path(r'c:\work\code\obsidian')
CLEAN  = ROOT / 'reference_database' / 'cleaned'
OUTDIR = ROOT / 'reference_database'

# Elements to summarise, in priority order for pXRF comparison
PXRF_ELEMS  = ['Rb', 'Sr', 'Zr', 'Nb', 'Y']          # heavy 5 -- least geometry-sensitive
EXTRA_ELEMS = ['Fe', 'Mn', 'Zn', 'Ti', 'Ba', 'Th', 'Pb', 'Ga']
ALL_ELEMS   = PXRF_ELEMS + EXTRA_ELEMS
NAA_ELEMS   = ['La', 'Ce', 'Sm', 'Eu', 'Yb', 'Lu']    # Tier 4 only

TIER_LABELS = {1: 'pXRF/EDXRF', 2: 'ICP-MS/INAA', 3: 'XRF (lab)', 4: 'NAA (REE)'}


def load_master() -> pd.DataFrame:
    df = pd.read_csv(CLEAN / 'all_sources_cleaned.csv')
    # Rebuild master from individual CSVs to pick up Yellin 1981 fix
    ELEMS_ALL = ALL_ELEMS + NAA_ELEMS
    META = ['source', 'sample_id', 'site', 'notes', 'verification_flag',
            'paper', 'year', 'method', 'method_tier', 'units', 'is_source_reference']
    parts = []
    for f in sorted(CLEAN.glob('*.csv')):
        if f.name == 'all_sources_cleaned.csv':
            continue
        part = pd.read_csv(f)
        if 'is_source_reference' in part.columns:
            part = part[part['is_source_reference'] == True]
        cols = [c for c in ELEMS_ALL + META if c in part.columns]
        parts.append(part[cols])
    master = pd.concat(parts, ignore_index=True)
    master.to_csv(CLEAN / 'all_sources_cleaned.csv', index=False)
    return master


def compute_stats(group: pd.DataFrame, elems: list) -> dict:
    row = {}
    for e in elems:
        if e not in group.columns:
            continue
        vals = pd.to_numeric(group[e], errors='coerce').dropna()
        n = len(vals)
        row[f'{e}_n']    = n
        row[f'{e}_mean'] = round(vals.mean(), 2) if n else np.nan
        row[f'{e}_sd']   = round(vals.std(ddof=1), 2) if n > 1 else np.nan
        row[f'{e}_min']  = round(vals.min(), 2) if n else np.nan
        row[f'{e}_max']  = round(vals.max(), 2) if n else np.nan
    return row


def build_stats_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build one row per (source, method_tier) with stats for all elements."""
    records = []

    # Group by source + tier
    for (source, tier), grp in df.groupby(['source', 'method_tier'], dropna=False):
        tier_int = int(tier) if not pd.isna(tier) else 0
        elems = (ALL_ELEMS + NAA_ELEMS) if tier_int == 4 else ALL_ELEMS
        rec = {
            'source':       source,
            'method_tier':  tier_int,
            'tier_label':   TIER_LABELS.get(tier_int, str(tier_int)),
            'n_samples':    len(grp),
            'papers':       '; '.join(sorted(grp['paper'].dropna().unique())),
        }
        rec.update(compute_stats(grp, elems))
        records.append(rec)

    # Also add an "ALL_TIERS" row per source for easy lookup
    for source, grp in df.groupby('source', dropna=False):
        tier_int = 99  # sentinel for "all"
        tier1 = grp[grp['method_tier'] == 1]
        rec = {
            'source':       source,
            'method_tier':  0,
            'tier_label':   'ALL (combined)',
            'n_samples':    len(grp),
            'papers':       '; '.join(sorted(grp['paper'].dropna().unique())),
        }
        rec.update(compute_stats(grp, ALL_ELEMS))
        # Prefix so it sorts first per source
        rec['method_tier'] = 0
        records.append(rec)

    stats = pd.DataFrame(records)
    # Sort: source alpha, then method_tier (0=ALL first, then 1..4)
    stats = stats.sort_values(['source', 'method_tier']).reset_index(drop=True)
    return stats


def fmt(val, decimals=1):
    if pd.isna(val):
        return '  --  '
    return f'{val:.{decimals}f}'


def build_report(df: pd.DataFrame, stats: pd.DataFrame) -> str:
    lines = []
    lines.append('PHASE 3 -- SOURCE FINGERPRINT STATISTICS')
    lines.append('=' * 70)
    lines.append(f'Master rows: {len(df)}  |  Verified: {df["verification_flag"].sum()}')
    lines.append(f'Unique sources: {df["source"].nunique()}')
    lines.append(f'Tier 1 (pXRF/EDXRF) rows: {(df["method_tier"]==1).sum()}')
    lines.append(f'Tier 2 rows: {(df["method_tier"]==2).sum()}')
    lines.append(f'Tier 3 rows: {(df["method_tier"]==3).sum()}')
    lines.append(f'Tier 4 (NAA) rows: {(df["method_tier"]==4).sum()}')
    lines.append('')
    lines.append('ELEMENT KEY  (ppm unless noted)')
    lines.append('  Heavy 5 (most reliable for pXRF): Rb  Sr  Zr  Nb  Y')
    lines.append('  Additional:                        Fe  Mn  Zn  Ti  Ba  Th  Pb  Ga')
    lines.append('  NAA (Tier 4 only):                 La  Ce  Sm  Eu  Yb  Lu')
    lines.append('')

    # Per-source section: Tier 1 preferred, else best available
    lines.append('=' * 70)
    lines.append('PER-SOURCE FINGERPRINTS  (format: mean +/- SD  [N])')
    lines.append('=' * 70)

    tier1_stats = stats[stats['method_tier'] == 1].set_index('source')
    all_stats   = stats[stats['method_tier'] == 0].set_index('source')

    PXRF = PXRF_ELEMS

    for source in sorted(df['source'].dropna().unique()):
        lines.append(f'\n--- {source} ---')
        t1_papers = '; '.join(sorted(df[(df['source']==source) & (df['method_tier']==1)]['paper'].dropna().unique()))
        all_papers = '; '.join(sorted(df[df['source']==source]['paper'].dropna().unique()))
        all_tiers = sorted(df[df['source']==source]['method_tier'].dropna().unique().astype(int).tolist())
        lines.append(f'  Tiers available: {all_tiers}  |  Papers: {all_papers}')

        # Tier 1 pXRF fingerprint
        if source in tier1_stats.index:
            r = tier1_stats.loc[source]
            n = int(r.get('Rb_n', 0) or 0)
            lines.append(f'  Tier 1 (pXRF, N={n}):')
            row_str = '    '
            for e in PXRF:
                m  = r.get(f'{e}_mean', np.nan)
                sd = r.get(f'{e}_sd',   np.nan)
                n2 = int(r.get(f'{e}_n', 0) or 0)
                row_str += f'{e}: {fmt(m)} +/-{fmt(sd)}  '
            lines.append(row_str)
            # Extra elements if present
            extras = [(e, r.get(f'{e}_mean'), r.get(f'{e}_sd'), r.get(f'{e}_n'))
                      for e in EXTRA_ELEMS
                      if not pd.isna(r.get(f'{e}_mean', np.nan))]
            if extras:
                ex_str = '    '
                for e, m, sd, n2 in extras:
                    ex_str += f'{e}: {fmt(m)}+/-{fmt(sd)}  '
                lines.append(ex_str)
        else:
            lines.append(f'  Tier 1 (pXRF): no data')

        # Other tiers summary
        for tier in all_tiers:
            if tier == 1:
                continue
            tname = TIER_LABELS.get(tier, str(tier))
            trows = df[(df['source']==source) & (df['method_tier']==tier)]
            n = len(trows)
            lines.append(f'  Tier {tier} ({tname}, N={n}): present -- see CSV for element details')

    # Summary table: Tier 1 means for Rb/Sr/Zr/Nb/Y
    lines.append('\n')
    lines.append('=' * 70)
    lines.append('TIER 1 SUMMARY TABLE  (mean ppm)')
    lines.append('=' * 70)
    hdr = f'{"Source":<22} {"N":>4}  {"Rb":>7}  {"Sr":>7}  {"Zr":>7}  {"Nb":>7}  {"Y":>7}  Papers'
    lines.append(hdr)
    lines.append('-' * 90)

    for source in sorted(df['source'].dropna().unique()):
        t1 = df[(df['source']==source) & (df['method_tier']==1)]
        if t1.empty:
            n, rb, sr, zr, nb, y = 0, '--', '--', '--', '--', '--'
        else:
            n = len(t1)
            def m(e): return f'{t1[e].mean():.1f}' if e in t1.columns and t1[e].notna().any() else '--'
            rb, sr, zr, nb, y = m('Rb'), m('Sr'), m('Zr'), m('Nb'), m('Y')
        papers_short = '; '.join(sorted(df[df['source']==source]['paper'].dropna().unique()))
        lines.append(f'{source:<22} {n:>4}  {rb:>7}  {sr:>7}  {zr:>7}  {nb:>7}  {y:>7}  {papers_short}')

    return '\n'.join(lines)


def main():
    print('Loading and rebuilding master CSV...')
    df = load_master()
    print(f'  {len(df)} rows, {df["source"].nunique()} sources')

    print('Computing per-source statistics...')
    stats = build_stats_table(df)
    out_csv = OUTDIR / 'source_statistics.csv'
    stats.to_csv(out_csv, index=False)
    print(f'  Saved {len(stats)} stat rows -> {out_csv}')

    print('Building report...')
    report = build_report(df, stats)
    out_txt = OUTDIR / 'source_statistics_report.txt'
    out_txt.write_text(report, encoding='utf-8')
    print(f'  Saved -> {out_txt}')
    print()
    print(report)


if __name__ == '__main__':
    main()

"""
10_clean_samples.py -- Phase 5b: Average duplicate readings per artifact.

Input:  my_samples/samples_raw.csv
Output: my_samples/samples_clean.csv

Algorithm:
  - Group rows by item_id
  - For items with N >= 2 readings: compute mean and SD per element
  - For items with N = 1 reading: mean = that reading, SD = NaN
  - Compute CV% (SD/mean * 100) for heavy-4 (Rb, Sr, Zr, Nb)
  - Assign quality_flag:
      'good'             -- N >= 2 and max CV < 10% across heavy-4
      'single'           -- N = 1
      'repeat_divergent' -- N >= 2 but max CV >= 10% for any heavy-4
      'beam_minimal'     -- beam_coverage = Minimal (geometric uncertainty)
      Combinations allowed: 'beam_minimal+single', 'beam_minimal+repeat_divergent'

Heavy-4 instead of heavy-5 because Y is not measured in this Niton configuration.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT    = Path(r'c:\work\code\obsidian')
SAMPLES = ROOT / 'my_samples'

HEAVY4 = ['Rb', 'Sr', 'Zr', 'Nb']
EXTRA  = ['Fe', 'Mn', 'Zn', 'Ti', 'Ba', 'Th', 'Pb', 'Ga']
ATTR   = ['Si', 'K', 'Ca']             # trend-monitoring (average but lower priority)
ALL_ELEMS = HEAVY4 + EXTRA + ATTR

CV_THRESHOLD = 10.0   # % -- flag if CV >= this value for any heavy-4 element


def load_raw() -> pd.DataFrame:
    path = SAMPLES / 'samples_raw.csv'
    df = pd.read_csv(path)
    print(f'Loaded samples_raw.csv: {len(df)} rows, {df["item_id"].nunique()} unique items')
    return df


def cv_pct(series: pd.Series) -> float:
    """Coefficient of variation in %."""
    vals = series.dropna()
    if len(vals) < 2 or vals.mean() == 0:
        return np.nan
    return vals.std(ddof=1) / vals.mean() * 100


def aggregate_item(group: pd.DataFrame) -> dict:
    """Aggregate all readings of one item into a single row."""
    n = len(group)
    first = group.sort_values('reading_no').iloc[0]

    # Detect material type from remarks and locus
    remarks_str = ' '.join(group['remarks'].fillna('').astype(str)).lower() if 'remarks' in group.columns else ''
    locus_str   = str(first.get('locus', '') or '').lower()
    is_flint = 'flint' in remarks_str or 'chert' in locus_str or 'flint' in locus_str
    material = 'flint?' if is_flint else 'obsidian'
    remarks_val = '; '.join(group['remarks'].dropna().unique()) if 'remarks' in group.columns else None

    row = {
        'item_id':       first['item_id'],
        'site':          first['site'],
        'period':        first['period'] if 'period' in group.columns else None,
        'locus':         first.get('locus', None),
        'basket':        first.get('basket', None),
        'material':      material,
        'n_readings':    n,
        'beam_coverage': first.get('beam_coverage', None),
        'dirt_flag':     group['dirt_flag'].any() if 'dirt_flag' in group.columns else False,
        'remarks':       remarks_val,
        'session_date':  first.get('session_date', None),
    }

    # Average numeric element columns
    max_cv = 0.0
    divergent_elems = []  # heavy-4 elements with CV >= threshold
    for e in ALL_ELEMS:
        if e not in group.columns:
            continue
        vals = pd.to_numeric(group[e], errors='coerce').dropna()
        row[e]       = round(vals.mean(), 2) if len(vals) else np.nan
        row[f'{e}_sd'] = round(vals.std(ddof=1), 2) if len(vals) > 1 else np.nan

        # Track max CV for quality flag (heavy-4 only)
        if e in HEAVY4 and len(vals) >= 2:
            cv = cv_pct(group[e].apply(pd.to_numeric, errors='coerce'))
            if not np.isnan(cv):
                max_cv = max(max_cv, cv)
                if cv >= CV_THRESHOLD:
                    divergent_elems.append(e)

    row['max_cv_pct'] = round(max_cv, 1) if n >= 2 else np.nan
    row['divergent_elements'] = ','.join(divergent_elems) if divergent_elems else ''

    # Quality flag
    beam = str(row.get('beam_coverage', '')).lower()
    is_minimal = beam == 'minimal'

    if n == 1:
        flag = 'single'
    elif max_cv >= CV_THRESHOLD:
        flag = 'repeat_divergent'
    else:
        flag = 'good'

    if is_minimal:
        flag = f'beam_minimal+{flag}' if flag != 'good' else 'beam_minimal'

    row['quality_flag'] = flag
    return row


def build_clean(raw: pd.DataFrame) -> pd.DataFrame:
    records = []
    for item_id, grp in raw.groupby('item_id', sort=False):
        records.append(aggregate_item(grp))
    clean = pd.DataFrame(records)
    return clean


def build_col_order(df: pd.DataFrame) -> list:
    meta = ['item_id', 'site', 'period', 'locus', 'basket', 'material',
            'n_readings', 'beam_coverage', 'dirt_flag', 'remarks',
            'session_date', 'quality_flag', 'divergent_elements', 'max_cv_pct']
    elem_cols = []
    for e in ALL_ELEMS:
        if e in df.columns:
            elem_cols.append(e)
        sd = f'{e}_sd'
        if sd in df.columns:
            elem_cols.append(sd)
    present = [c for c in meta if c in df.columns]
    return present + elem_cols


def main():
    print('=== Phase 5b: Clean & Average Duplicate Readings ===\n')
    raw = load_raw()

    print('\nAggregating per item...')
    clean = build_clean(raw)

    # Reorder columns
    col_order = build_col_order(clean)
    clean = clean[col_order].sort_values(['site', 'item_id']).reset_index(drop=True)

    # Summary
    print(f'\nSummary:')
    print(f'  Unique items (artifacts): {len(clean)}')
    print(f'  Material: {clean["material"].value_counts().to_dict()}')
    print(f'  Sites: {clean["site"].value_counts().to_dict()}')
    print(f'  Periods: {clean["period"].value_counts().to_dict()}')
    print(f'  Quality flags:')
    for flag, cnt in clean['quality_flag'].value_counts().items():
        print(f'    {flag}: {cnt}')

    print(f'\n  Items with n_readings >= 2: {(clean["n_readings"] >= 2).sum()}')
    print(f'  Items with n_readings == 1: {(clean["n_readings"] == 1).sum()}')

    # Repeatability summary for paired readings
    paired = clean[clean['n_readings'] >= 2].copy()
    if len(paired) > 0:
        print(f'\n  Repeatability (CV%) for paired readings (N={len(paired)}):')
        print(f'    max_cv_pct distribution:')
        print(f'      < 5%:  {(paired["max_cv_pct"] < 5).sum()} items')
        print(f'      5-10%: {((paired["max_cv_pct"] >= 5) & (paired["max_cv_pct"] < 10)).sum()} items')
        print(f'      >= 10% (divergent): {(paired["max_cv_pct"] >= 10).sum()} items')

    print(f'\n  Element coverage (% of items with non-null value):')
    for e in HEAVY4:
        if e in clean.columns:
            pct = clean[e].notna().mean() * 100
            print(f'    {e:4s}: {pct:.0f}%')

    out = SAMPLES / 'samples_clean.csv'
    clean.to_csv(out, index=False)
    print(f'\nWritten: {out}  ({len(clean)} items, {len(clean.columns)} cols)')


if __name__ == '__main__':
    main()

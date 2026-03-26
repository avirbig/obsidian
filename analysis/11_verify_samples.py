"""
11_verify_samples.py -- Phase 5c: Verify completeness and quality of cleaned samples.

Input:   my_samples/samples_raw.csv
         my_samples/samples_clean.csv
Output:  my_samples/verification_report.txt  (human-readable)

Checks:
  1. Completeness:      % of items with valid (non-null) value per element
  2. Repeatability:     CV% distribution for items with N >= 2 readings
  3. Range sanity:      flag items outside expected obsidian ppm ranges
  4. Session consistency: identify re-test readings (item_id appears in consecutive
                          sessions -- the last item from previous session re-measured)
  5. Beam coverage summary
  6. Divergent readings: list items flagged 'repeat_divergent' with their CV% per element
  7. Cross-check: compare raw reading count vs clean item count
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT    = Path(r'c:\work\code\obsidian')
SAMPLES = ROOT / 'my_samples'

HEAVY4 = ['Rb', 'Sr', 'Zr', 'Nb']
EXTRA  = ['Fe', 'Mn', 'Zn', 'Ti', 'Ba', 'Th', 'Pb', 'Ga']

# Expected obsidian ranges (ppm) -- outside these values are suspicious
OBSIDIAN_RANGES = {
    'Rb':  (10,   600),
    'Sr':  (0,    300),
    'Zr':  (10,  2000),
    'Nb':  (3,    100),
    'Fe':  (5000, 50000),
    'Ti':  (100,  5000),
    'Ba':  (0,    1000),
    'Th':  (0,    80),
    'Pb':  (0,    100),
    'Zn':  (0,    100),
    'Ga':  (5,    50),
    'Mn':  (50,   2000),
}


def load() -> tuple:
    raw   = pd.read_csv(SAMPLES / 'samples_raw.csv')
    clean = pd.read_csv(SAMPLES / 'samples_clean.csv')
    return raw, clean


def fmt_pct(n, total):
    if total == 0:
        return '  0 /  0 (--)'
    return f'{n:4d} / {total:4d} ({n/total*100:.0f}%)'


def check_completeness(clean: pd.DataFrame) -> list:
    lines = ['1. ELEMENT COMPLETENESS (% items with non-null value)', '-' * 60]
    n = len(clean)
    for e in HEAVY4 + EXTRA:
        if e not in clean.columns:
            lines.append(f'  {e:4s}: NOT IN DATA')
            continue
        nn = clean[e].notna().sum()
        marker = '' if nn / n >= 0.95 else '  [LOW]'
        lines.append(f'  {e:4s}: {fmt_pct(nn, n)}{marker}')
    lines.append('')
    lines.append('  Note: Y (Yttrium) is NOT measured in this Niton Mining Cu/Zn mode.')
    lines.append('        Source attribution will use Rb/Sr/Zr/Nb (4-element fingerprint).')
    return lines


def check_repeatability(raw: pd.DataFrame) -> list:
    lines = ['', '2. REPEATABILITY  (CV% for items with N >= 2 readings)', '-' * 60]

    # Compute per-item CV% for each heavy-4 element
    paired_items = raw.groupby('item_id').filter(lambda x: len(x) >= 2)
    if len(paired_items) == 0:
        lines.append('  No items with >= 2 readings.')
        return lines

    n_paired = paired_items['item_id'].nunique()
    lines.append(f'  Items with N >= 2 readings: {n_paired}')
    lines.append('')
    lines.append(f'  {"Element":6s}  {"Mean CV%":>8s}  {"<5%":>6s}  {"5-10%":>6s}  {">=10%":>7s}')
    lines.append(f'  {"-"*6}  {"-"*8}  {"-"*6}  {"-"*6}  {"-"*7}')

    for e in HEAVY4:
        if e not in raw.columns:
            continue
        cvs = []
        for iid, grp in paired_items.groupby('item_id'):
            vals = pd.to_numeric(grp[e], errors='coerce').dropna()
            if len(vals) >= 2 and vals.mean() != 0:
                cvs.append(vals.std(ddof=1) / vals.mean() * 100)

        if not cvs:
            lines.append(f'  {e:6s}: no data')
            continue
        cvs = np.array(cvs)
        lines.append(
            f'  {e:6s}  {np.mean(cvs):8.1f}  {(cvs<5).sum():6d}  '
            f'{((cvs>=5)&(cvs<10)).sum():6d}  {(cvs>=10).sum():7d}'
        )
    return lines


def check_range_sanity(clean: pd.DataFrame) -> list:
    lines = ['', '3. RANGE SANITY CHECK  (expected obsidian ppm ranges)', '-' * 60]
    flagged = {}

    for e, (lo, hi) in OBSIDIAN_RANGES.items():
        if e not in clean.columns:
            continue
        vals = pd.to_numeric(clean[e], errors='coerce')
        out = clean[vals.notna() & ((vals < lo) | (vals > hi))]
        if len(out) > 0:
            flagged[e] = out[['item_id', 'site', e]].to_dict('records')

    if not flagged:
        lines.append('  All values within expected ranges.')
    else:
        lines.append(f'  {len(flagged)} elements have out-of-range values:\n')
        for e, rows in flagged.items():
            lo, hi = OBSIDIAN_RANGES[e]
            lines.append(f'  {e} (expected {lo}–{hi} ppm): {len(rows)} items')
            for r in rows[:5]:   # show max 5
                lines.append(f'    {r["item_id"]} ({r["site"]}): {r[e]} ppm')
            if len(rows) > 5:
                lines.append(f'    ... and {len(rows) - 5} more')
    return lines


def check_divergent(clean: pd.DataFrame, raw: pd.DataFrame) -> list:
    lines = ['', '4. DIVERGENT READINGS  (quality_flag = repeat_divergent)', '-' * 60]
    div = clean[clean['quality_flag'].str.startswith('repeat_divergent', na=False)].copy()

    if len(div) == 0:
        lines.append('  None.')
        return lines

    lines.append(f'  {len(div)} items with CV >= 10% on at least one heavy-4 element:\n')
    lines.append(f'  {"item_id":20s} {"site":8s} {"cv%":>6s}  '
                 f'{"Rb_cv":>6s}  {"Sr_cv":>6s}  {"Zr_cv":>6s}  {"Nb_cv":>6s}')
    lines.append('  ' + '-' * 70)

    for _, row in div.iterrows():
        iid = row['item_id']
        grp = raw[raw['item_id'] == iid]
        cv_vals = {}
        for e in HEAVY4:
            if e not in raw.columns:
                cv_vals[e] = np.nan
                continue
            vals = pd.to_numeric(grp[e], errors='coerce').dropna()
            if len(vals) >= 2 and vals.mean() != 0:
                cv_vals[e] = vals.std(ddof=1) / vals.mean() * 100
            else:
                cv_vals[e] = np.nan

        def fv(v):
            return f'{v:6.1f}' if not np.isnan(v) else '   -- '

        lines.append(
            f'  {iid:20s} {str(row["site"]):8s} {row["max_cv_pct"]:6.1f}  '
            f'{fv(cv_vals.get("Rb", np.nan))}  {fv(cv_vals.get("Sr", np.nan))}  '
            f'{fv(cv_vals.get("Zr", np.nan))}  {fv(cv_vals.get("Nb", np.nan))}'
        )
    return lines


def check_beam_coverage(clean: pd.DataFrame) -> list:
    lines = ['', '5. BEAM COVERAGE SUMMARY', '-' * 60]
    if 'beam_coverage' not in clean.columns:
        lines.append('  Column not found.')
        return lines
    counts = clean['beam_coverage'].value_counts(dropna=False)
    total  = len(clean)
    for val, cnt in counts.items():
        label = str(val) if not pd.isna(val) else '(not noted)'
        lines.append(f'  {label:20s}: {cnt:4d} items ({cnt/total*100:.0f}%)')
    not_noted = clean['beam_coverage'].isna().sum()
    lines.append(f'\n  Not noted (likely Full Coverage): {not_noted}')
    return lines


def check_counts(raw: pd.DataFrame, clean: pd.DataFrame) -> list:
    lines = ['', '6. COUNT CROSS-CHECK', '-' * 60]
    lines.append(f'  Total NDT readings (samples_raw):  {len(raw)}')
    lines.append(f'  Unique item_ids  (samples_clean):  {len(clean)}')
    # Per site
    lines.append('')
    for site, grp in raw.groupby('site'):
        n_read = len(grp)
        n_item = grp['item_id'].nunique()
        n_s1   = (grp.groupby('item_id').cumcount() == 0).sum()
        lines.append(f'  {site:10s}: {n_read:4d} readings, {n_item:4d} items '
                     f'(avg {n_read/n_item:.1f} readings/item)')
    return lines


def main():
    print('=== Phase 5c: Verification ===\n')
    raw, clean = load()
    print(f'Loaded: {len(raw)} raw readings, {len(clean)} clean items\n')

    sep = '=' * 70
    report_lines = [
        'PHASE 5 -- SAMPLE VERIFICATION REPORT',
        sep,
        f'Raw readings:  {len(raw)}',
        f'Clean items:   {len(clean)}',
        f'Sites:         {sorted(clean["site"].dropna().unique().tolist())}',
        f'Periods:       {sorted(clean["period"].dropna().unique().tolist())}',
        '',
        'NOTE: Y (Yttrium) is NOT measured in this Niton Mining Cu/Zn configuration.',
        'Heavy-4 fingerprint elements: Rb, Sr, Zr, Nb',
        sep,
        '',
    ]

    report_lines += check_completeness(clean)
    report_lines += check_repeatability(raw)
    report_lines += check_range_sanity(clean)
    report_lines += check_divergent(clean, raw)
    report_lines += check_beam_coverage(clean)
    report_lines += check_counts(raw, clean)

    report_lines += [
        '',
        sep,
        'Files:',
        '  my_samples/samples_raw.csv   -- immutable raw record',
        '  my_samples/samples_clean.csv -- per-item averaged, quality-flagged',
        '  my_samples/verification_report.txt -- this report',
    ]

    report = '\n'.join(report_lines) + '\n'
    out = SAMPLES / 'verification_report.txt'
    out.write_text(report, encoding='utf-8')
    print(report)
    print(f'Written: {out}')


if __name__ == '__main__':
    main()

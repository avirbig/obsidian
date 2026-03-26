"""
09_load_samples.py -- Phase 5a: Normalize user pXRF measurements into samples_raw.csv

Source:
  my_samples/all 19.2.2018-5.3.2018 copy.xls.xlsx  (sheet: 'First Changes')
    -> primary data: all 1224 readings with full field annotations

  my_samples/01-05 *.xlsx  (sheets: 'editted_2026' or similar)
    -> extra columns: filter times (main/low/high/light), Area
    -> joined to master by Reading No

Normalization:
  - Values are in wt% (NDT Units column = '%')
  - Conversion: wt% * 10000 = ppm  (e.g. 0.012% Rb = 120 ppm)
  - '< LOD' -> NaN  (below detection limit)
  - Error columns also converted wt% -> ppm
  - item_id = {site_prefix}_{basket}  (e.g. ein_6016, yif_30195, mot_1234)
  - side_no: 1 = first reading per item (by Reading No order), 2 = second, etc.

Note: Y (Yttrium) is NOT measured in this Niton Mining Cu/Zn configuration.
Source attribution will use Rb/Sr/Zr/Nb (4-element fingerprint).

Output: my_samples/samples_raw.csv
"""

import pandas as pd
import numpy as np
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

ROOT    = Path(r'c:\work\code\obsidian')
SAMPLES = ROOT / 'my_samples'
MASTER  = SAMPLES / 'data manipulation.xlsx'
MASTER_SHEET = 'First Changes'

# Elements to convert and keep (in priority order for attribution)
HEAVY4   = ['Rb', 'Sr', 'Zr', 'Nb']            # Y not measured in this config
EXTRA    = ['Fe', 'Mn', 'Zn', 'Ti', 'Ba', 'Th', 'Pb', 'Ga']
TREND    = ['Si', 'K', 'Ca']                     # trend-monitoring elements
ALL_ELEM = HEAVY4 + EXTRA + TREND

# Metadata columns in master
META_MASTER = {
    'Reading No':   'reading_no',
    'site':         'site',
    'Period':       'period',
    'side':         'side',
    'Locus\\Square': 'locus',
    'Basket':       'basket',
    'cover':        'beam_coverage',
    'Dirt':         'dirt',
    'remarks':      'remarks',
    'Time':         'session_date',
    'Duration':     'duration_sec',
    'SAMPLE':       'ndt_label',
}

SITE_PREFIX = {
    'einan': 'ein', 'eynan': 'ein',
    'yiftahel': 'yif',
    'motza': 'mot',
}

COVER_MAP = {
    'full': 'Full',
    'almost full': 'Full',
    'partial': 'Partial',
    'very partial': 'Partial',
    'tiny': 'Minimal',
}


def lod_to_nan(val):
    """Convert '< LOD' string or any non-numeric to NaN."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s.startswith('<') or s.upper() == 'LOD' or s == '':
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def load_master() -> pd.DataFrame:
    print(f'Loading master: {MASTER.name}, sheet: {MASTER_SHEET}')
    df = pd.read_excel(MASTER, sheet_name=MASTER_SHEET, dtype=str)
    print(f'  Raw rows: {len(df)}, cols: {len(df.columns)}')

    # Rename metadata columns
    rename = {k: v for k, v in META_MASTER.items() if k in df.columns}
    df = df.rename(columns=rename)

    # Normalise site strings
    df['site'] = df['site'].str.strip().str.lower()
    # Eynan = Einan, normalise spelling
    df['site'] = df['site'].replace({'eynan': 'einan'})

    # Normalise period
    if 'period' in df.columns:
        df['period'] = df['period'].str.strip()

    # Normalise side
    if 'side' in df.columns:
        df['side'] = df['side'].str.strip().str.lower()

    # Normalise beam_coverage
    if 'beam_coverage' in df.columns:
        df['beam_coverage'] = (
            df['beam_coverage'].str.strip().str.lower()
            .map(COVER_MAP)
        )

    # dirt -> flag
    if 'dirt' in df.columns:
        df['dirt_flag'] = df['dirt'].notna() & (df['dirt'].str.strip() != '')
        df = df.drop(columns=['dirt'])
    else:
        df['dirt_flag'] = False

    # reading_no as int
    df['reading_no'] = pd.to_numeric(df['reading_no'], errors='coerce').astype('Int64')

    # basket as str (preserve leading zeros if any; strip whitespace)
    df['basket'] = df['basket'].fillna('').astype(str).str.strip()

    # duration_sec to float
    if 'duration_sec' in df.columns:
        df['duration_sec'] = pd.to_numeric(df['duration_sec'], errors='coerce')

    # Build item_id = {site_prefix}_{basket}
    df['site_prefix'] = df['site'].map(SITE_PREFIX)
    # Fall back to first 3 chars if unknown site
    mask_unknown = df['site_prefix'].isna()
    df.loc[mask_unknown, 'site_prefix'] = df.loc[mask_unknown, 'site'].str[:3]
    df['item_id'] = df['site_prefix'] + '_' + df['basket']
    df = df.drop(columns=['site_prefix'])

    return df


def load_numbered_extras() -> pd.DataFrame:
    """
    Load editted_2026 sheets from numbered files.
    Extract: Reading No, filter times (main/low/high/light), Area.
    Return merged dataframe keyed on reading_no.
    """
    extras = []
    for f in sorted(SAMPLES.glob('[0-9]*.xls*')):
        xl = pd.ExcelFile(f)
        # Pick the first 'editted' sheet
        target_sheet = None
        for sh in xl.sheet_names:
            if 'edit' in sh.lower() or '2026' in sh.lower():
                target_sheet = sh
                break
        if target_sheet is None:
            continue

        df = pd.read_excel(f, sheet_name=target_sheet, dtype=str)
        # Normalise col names (case-insensitive)
        df.columns = [c.strip() for c in df.columns]
        col_lower = {c.lower(): c for c in df.columns}

        # Reading No
        rn_col = col_lower.get('reading no') or col_lower.get('reading_no')
        if rn_col is None:
            print(f'  [WARN] No Reading No in {f.name} / {target_sheet}')
            continue
        row = {'reading_no': df[rn_col].tolist()}

        sub = pd.DataFrame({'reading_no': df[rn_col]})
        sub['reading_no'] = pd.to_numeric(sub['reading_no'], errors='coerce').astype('Int64')

        # Filter times
        for col_name, out_name in [('main', 'filter_main_sec'), ('low', 'filter_low_sec'),
                                    ('high', 'filter_high_sec'), ('light', 'filter_light_sec')]:
            orig = col_lower.get(col_name)
            if orig:
                sub[out_name] = pd.to_numeric(df[orig], errors='coerce')

        # Area (mostly NaN but capture it)
        area_col = col_lower.get('area')
        if area_col:
            sub['area'] = df[area_col].str.strip()

        sub['source_file'] = f.name
        extras.append(sub)

    if not extras:
        print('  No numbered-file extras found.')
        return pd.DataFrame(columns=['reading_no'])

    all_extras = pd.concat(extras, ignore_index=True)
    # Deduplicate (same reading_no in multiple numbered files shouldn't happen, but just in case)
    all_extras = all_extras.drop_duplicates(subset=['reading_no']).sort_values('reading_no')
    print(f'Extras from numbered files: {len(all_extras)} readings, '
          f'{all_extras["reading_no"].nunique()} unique')
    return all_extras


def convert_elements(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each element in ALL_ELEM:
      - find column (element name or 'element Error')
      - apply lod_to_nan
      - multiply by 10000 (wt% -> ppm)
    """
    present_elems = []
    present_err   = []

    for e in ALL_ELEM:
        if e in df.columns:
            df[e] = df[e].apply(lod_to_nan) * 10000
            df[e] = df[e].round(2)
            present_elems.append(e)

        err_col = f'{e} Error'
        out_err = f'{e}_err'
        if err_col in df.columns:
            df[out_err] = df[err_col].apply(lod_to_nan) * 10000
            df[out_err] = df[out_err].round(2)
            df = df.drop(columns=[err_col])
            present_err.append(out_err)

    print(f'  Elements converted: {present_elems}')
    print(f'  Error cols:         {present_err}')
    return df


def assign_side_number(df: pd.DataFrame) -> pd.DataFrame:
    """
    Within each item_id (grouped by Reading No order, ascending),
    assign side_no: 1 for first reading, 2 for second, etc.
    """
    df = df.sort_values('reading_no').reset_index(drop=True)
    df['side_no'] = df.groupby('item_id').cumcount() + 1
    return df


def drop_irrelevant_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Remove NDT administrative columns we don't need."""
    drop = ['Units']  # keep ndt_label for material identification (e.g. 'Dark colored flint')
    # Also drop all element columns NOT in our list (Sn, Cd, Bi, etc.)
    keep_elems = set(ALL_ELEM + [f'{e}_err' for e in ALL_ELEM])
    all_cols = set(df.columns)
    # Any column that looks like an element or element error not in our keep list
    ndt_leftover = [c for c in df.columns
                    if c not in keep_elems
                    and c not in ['reading_no', 'item_id', 'site', 'period', 'side',
                                  'side_no', 'locus', 'basket', 'beam_coverage',
                                  'dirt_flag', 'remarks', 'ndt_label', 'session_date', 'duration_sec',
                                  'filter_main_sec', 'filter_low_sec', 'filter_high_sec',
                                  'filter_light_sec', 'area', 'source_file']
                    and not c.startswith('Unnamed')]
    if ndt_leftover:
        df = df.drop(columns=ndt_leftover, errors='ignore')
    # Drop Unnamed cols
    unnamed = [c for c in df.columns if str(c).startswith('Unnamed')]
    if unnamed:
        df = df.drop(columns=unnamed, errors='ignore')
    # Drop unused NDT cols explicitly
    df = df.drop(columns=[c for c in drop if c in df.columns], errors='ignore')
    return df


def build_col_order(df: pd.DataFrame) -> list:
    meta = ['reading_no', 'item_id', 'site', 'period', 'locus', 'basket',
            'side', 'side_no', 'beam_coverage', 'dirt_flag', 'remarks', 'ndt_label',
            'session_date', 'duration_sec',
            'filter_main_sec', 'filter_low_sec', 'filter_high_sec', 'filter_light_sec',
            'area', 'source_file']
    elem_cols = []
    for e in ALL_ELEM:
        if e in df.columns:
            elem_cols.append(e)
        err = f'{e}_err'
        if err in df.columns:
            elem_cols.append(err)
    present_meta = [c for c in meta if c in df.columns]
    return present_meta + elem_cols


def main():
    print('=== Phase 5a: Load & Normalize User pXRF Samples ===\n')

    # 1. Master
    master = load_master()

    # 2. Extras from numbered files
    extras = load_numbered_extras()
    if 'reading_no' in extras.columns and len(extras) > 0:
        master = master.merge(extras, on='reading_no', how='left')
        print(f'  After merge: {len(master)} rows')

    # 3. Convert elements wt% -> ppm
    print('\nConverting elements (wt% -> ppm):')
    master = convert_elements(master)

    # 4. Remove irrelevant NDT columns (keep only what we need)
    master = drop_irrelevant_cols(master)

    # 5. Assign side_no
    master = assign_side_number(master)

    # 6. Reorder columns
    col_order = build_col_order(master)
    master = master[col_order]

    # 7. Quick summary
    print(f'\nSummary:')
    print(f'  Total readings: {len(master)}')
    print(f'  Unique items (baskets): {master["item_id"].nunique()}')
    print(f'  Sites: {sorted(master["site"].dropna().unique())}')
    print(f'  Periods: {sorted(master["period"].dropna().unique())}')
    print(f'  Side 1 readings: {(master["side_no"]==1).sum()}, '
          f'Side 2: {(master["side_no"]==2).sum()}, '
          f'Side 3+: {(master["side_no"]>=3).sum()}')
    print(f'  Beam coverage: {master["beam_coverage"].value_counts().to_dict()}')
    print(f'  Dirt flagged: {master["dirt_flag"].sum()}')
    print(f'\n  Rb coverage: {master["Rb"].notna().sum()} / {len(master)} '
          f'({master["Rb"].notna().mean()*100:.0f}%)')
    print(f'  Sr coverage: {master["Sr"].notna().sum()} / {len(master)} '
          f'({master["Sr"].notna().mean()*100:.0f}%)')
    print(f'  Zr coverage: {master["Zr"].notna().sum()} / {len(master)} '
          f'({master["Zr"].notna().mean()*100:.0f}%)')
    print(f'  Nb coverage: {master["Nb"].notna().sum()} / {len(master)} '
          f'({master["Nb"].notna().mean()*100:.0f}%)')
    print(f'  Note: Y (Yttrium) not measured in this Niton Mining Cu/Zn mode.')

    # 8. Write output
    out = SAMPLES / 'samples_raw.csv'
    master.to_csv(out, index=False)
    print(f'\nWritten: {out}  ({len(master)} rows, {len(master.columns)} cols)')
    print('NOTE: This file is IMMUTABLE -- do not modify it after creation.')


if __name__ == '__main__':
    main()

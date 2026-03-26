"""
09a_inspect_samples.py  --  Read every file in my_samples/ and print:
  - Sheet names
  - Raw rows 0-4 (no header assumed) to see true column layout
  - Total row counts per sheet
  - All distinct non-null values in any column that looks like a category
    (few unique values -> likely beam_coverage, site, etc.)

Run this BEFORE writing the normalizer so column names are known.
"""
import pandas as pd
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

FOLDER = Path(r'c:\work\code\obsidian\my_samples')


def peek(f: Path):
    print(f'\n{"=" * 70}')
    print(f'FILE: {f.name}')
    try:
        xl = pd.ExcelFile(f)
    except Exception as e:
        print(f'  Cannot open: {e}')
        return

    print(f'  Sheets: {xl.sheet_names}')

    for sh in xl.sheet_names:
        print(f'\n  --- Sheet: [{sh}] ---')
        try:
            # Read raw (no header) to see what row 0 really is
            raw = pd.read_excel(f, sheet_name=sh, header=None, dtype=str)
            nrows = len(raw)
            ncols = len(raw.columns)
            print(f'  Dimensions (raw): {nrows} rows x {ncols} cols')

            print(f'  Row 0 (first 25 cells): {raw.iloc[0, :25].tolist()}')
            if nrows > 1:
                print(f'  Row 1:                  {raw.iloc[1, :25].tolist()}')
            if nrows > 2:
                print(f'  Row 2:                  {raw.iloc[2, :25].tolist()}')
            if nrows > 3:
                print(f'  Row 3:                  {raw.iloc[3, :25].tolist()}')
            if nrows > 4:
                print(f'  Row 4:                  {raw.iloc[4, :25].tolist()}')

            # Now try to read with header=0 and show column names
            df = pd.read_excel(f, sheet_name=sh, dtype=str)
            print(f'\n  Columns (with header=0, {len(df.columns)} total):')
            for i, c in enumerate(df.columns):
                print(f'    [{i:02d}] "{c}"')

            print(f'  Data rows (with header): {len(df)}')

            # Identify likely categorical columns (<=15 unique non-null values)
            print(f'\n  Categorical-looking columns (<=15 unique vals):')
            for c in df.columns:
                vals = df[c].dropna().unique()
                if 0 < len(vals) <= 15:
                    print(f'    "{c}": {sorted([str(v) for v in vals])}')

        except Exception as e:
            print(f'  Error reading sheet [{sh}]: {e}')


for f in sorted(FOLDER.glob('*.xls*')):
    if f.name == '.gitkeep':
        continue
    peek(f)

print('\n\nDONE.')

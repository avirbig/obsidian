#!/usr/bin/env python3
"""
Step 3 -- Map the raw pXRF sample workbooks and profile their quality.

Answers, BEFORE any cleaning:
  * Does the master workbook contain every reading from the session files?
  * Are there readings that exist ONLY in the master?
  * What condition is the data in (usable elements, duplicates, missing context)?

Design principles:
  * READ-ONLY. Nothing in data/ is written or modified.
  * The identity of a reading is (Reading No, Time). The instrument counter was
    RESET between 2017 and 2018, so 94 reading numbers occur twice -- keying on
    Reading No alone would merge a Yiftahel tool with a Motza tool.
  * 3 rows have a BLANK Time. A timestamp-only key drops them silently -- that is
    how reading 1490 (a lost Motza obsidian) escaped the first pass. Rows without
    a timestamp fall back to (Reading No, Duration, label). Never filter on
    notna(ts) when the question is "what is missing".
  * Blank labels are not trusted: unlabelled 'Mining' readings are judged by
    their chemistry (obsidian = low Ca, high Rb/Zr) rather than assumed.

Output: the tables reproduced in docs/raw_sample_data_map_and_quality.md
"""

from pathlib import Path
import re
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

# Windows consoles default to cp1252 and raise on Turkish characters; keep the
# console safe without touching file output (which is always UTF-8).
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
pd.set_option('display.width', 200)

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / 'data' / 'samples'
MASTER = 'obsidian_pxrf_master_2017-2018.xlsx'   # renamed 2026-07-21 from 'data manipulation.xlsx'

# (file, sheet) of every original instrument session / dump
SESSIONS = [
    ("01 obsidian yiftahel (mppnb) hamudi iaa 9.2.2017.xlsx", 'obsidian yiftahel (mppnb) origi'),
    ("02 obsidian einan natufian 23.2.17.xlsx", 'obsidian einan natufian 23.2.17'),
    ("03 obsidian eynan 9.3.17.xlsx", 'obsidian eynan 9.3.17'),
    ("04 obsidian einan 30.3.17.xlsx", 'editted_2026'),
    ("05 obsidian einan 05.04.17.xlsx", 'editted_2026'),
    ("all 19.2.2018-5.3.2018 copy.xls.xlsx", 'Sheet1'),
    ("Avishai_Obsidian 12.2017.xlsx", 'Sheet1'),
    ("all analyses 13.3.18 copy.xls", 'all analyses 13.3.18'),
]

# elements we care about for sourcing (Y/Ga/Th checked but known absent)
SOURCING = ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Ti', 'Mn', 'Fe', 'Zn', 'Ga', 'Ba', 'Pb', 'Th']
CHEM = ['Rb', 'Sr', 'Zr', 'Nb', 'Fe', 'Ca', 'K', 'Ti', 'Mn']


# ---- helpers --------------------------------------------------------------

def find_col(df, *names):
    """Locate a column by loose name match (case/punctuation insensitive)."""
    norm = {re.sub(r'[^a-z]', '', str(c).lower()): c for c in df.columns}
    for n in names:
        k = re.sub(r'[^a-z]', '', n.lower())
        if k in norm:
            return norm[k]
    return None


def extract(path, sheet):
    """Minimal common view of any workbook: reading, ts, type, labels, chemistry."""
    df = pd.read_excel(path, sheet_name=sheet)
    rc = find_col(df, 'Reading No')
    if rc is None:
        return None
    out = pd.DataFrame()
    out['reading'] = pd.to_numeric(df[rc], errors='coerce')
    tc = find_col(df, 'Time', 'Date')
    out['ts'] = pd.to_datetime(df[tc], errors='coerce') if tc is not None else pd.NaT
    for lbl, cand in [('type', 'Type'), ('sample', 'SAMPLE'), ('site', 'site'),
                      ('dur', 'Duration')]:
        c = find_col(df, cand)
        out[lbl] = df[c] if c is not None else np.nan
    for e in CHEM:
        c = find_col(df, e)
        out[e] = pd.to_numeric(df[c], errors='coerce') if c is not None else np.nan
    out['file'] = path.name
    out['xlrow'] = df.index + 2          # so a finding can be located in Excel
    return out.dropna(subset=['reading'])


def rkey(df):
    """Identity of a reading. Falls back for the 3 rows with a blank Time."""
    r = df['reading'].astype(int).astype(str)
    dur = pd.to_numeric(df['dur'], errors='coerce').round(2).astype(str)
    lab = df['sample'].astype(str).str.strip().str.lower()
    return np.where(df['ts'].notna(),
                    r + '@' + df['ts'].astype(str),
                    r + '#' + dur + '#' + lab)


def hdr(title):
    print("\n" + "=" * 78)
    print(title)


# ---- 1. load --------------------------------------------------------------

M = extract(SAMPLES / MASTER, 'Original')
M['k'] = rkey(M)
mts, mk = set(M['ts'].dropna()), set(M['k'])

frames = []
for fname, sheet in SESSIONS:
    s = extract(SAMPLES / fname, sheet)
    if s is not None:
        frames.append(s)
S = pd.concat(frames, ignore_index=True)
S['k'] = rkey(S)
S = S.sort_values('file').drop_duplicates(subset=['k'], keep='first')

hdr("1. MASTER OVERVIEW")
print(f"  readings          : {len(M)}")
print(f"  unique Reading No : {M['reading'].nunique()}  "
      f"(-> counter was reset; key must be Reading No + Time)")
print(f"  date range        : {M['ts'].min()} -> {M['ts'].max()}")

# ---- 2. coverage ----------------------------------------------------------

hdr("2. COVERAGE -- session readings present in the master")
for fname, sheet in SESSIONS:
    s = extract(SAMPLES / fname, sheet)
    s['k'] = rkey(s)
    print(f"  {fname[:44]:46s} {s['k'].isin(mk).sum():4d}/{len(s):4d}")

hdr("3. BLANK TIMESTAMPS -- the trap that hid reading 1490")
print(f"  master : {M['ts'].isna().sum()} of {len(M)}")
for fname, sheet in SESSIONS:
    s = extract(SAMPLES / fname, sheet)
    if s['ts'].isna().any():
        print(f"  {fname[:44]:46s} {s['ts'].isna().sum()} blank")

hdr("4. MASTER-ONLY readings (exist in master, in no session file)")
only = M[~M['k'].isin(set(S['k']))]
print(f"  count: {len(only)}")
if len(only):
    print(only[['reading', 'ts', 'site', 'sample']].to_string(index=False))
else:
    print("  -> none. The master is a strict subset; nothing is unsourced.")

# ---- 3. what was excluded, and was any of it obsidian? --------------------

excl = S[~S['k'].isin(mk)].copy()
hdr(f"5. EXCLUDED from the master: {len(excl)} of {len(S)} distinct readings")
print(excl['type'].fillna('(blank)').value_counts().to_string())

print("\n  5a. excluded readings LABELLED obsidian (all spellings):")
lab = excl['sample'].astype(str).str.lower()
hit = excl[lab.str.contains('obsid|obidian|obsdian|obsidan', na=False)]
print(hit[['file', 'xlrow', 'reading', 'ts', 'dur', 'sample'] + CHEM].to_string(index=False))
print("      -> short duration = aborted (correct drop); full duration = REAL LOSS.")

print("\n  5b. unlabelled 'Mining' readings -- obsidian or not? (judge by chemistry)")
mb = excl[(excl['type'].astype(str).str.strip() == 'Mining') & (excl['sample'].isna())]
print(f"      count: {len(mb)}")
print("      median chemistry:")
print(mb[CHEM].median().to_string())
print("      -> high Ca / low Rb+Zr = carbonate rock, NOT obsidian. Correctly excluded.")

# ---- 4. quality profile of the master ------------------------------------

O = pd.read_excel(SAMPLES / MASTER, sheet_name='Original')

hdr("5. ELEMENT USABILITY in the master")
print(f"  {'elem':6s} {'usable':>7s} {'<LOD':>7s} {'%':>7s}")
for e in SOURCING:
    if e not in O.columns:
        print(f"  {e:6s} {'column absent from workbook':>30s}")
        continue
    s = O[e]
    lod = (s.astype(str).str.strip() == '< LOD').sum()
    ok = pd.to_numeric(s, errors='coerce').notna().sum()
    print(f"  {e:6s} {ok:7d} {lod:7d} {100 * ok / len(O):6.1f}%")
print("  -> build on Rb/Zr/Nb (+Fe,Ti,Mn). Sr, Ba, Y, Ga, Th are unusable.")

hdr("6. READINGS ARE PAIRED -- they are not independent samples")
key = (O['site'].astype(str).str.strip() + '|' +
       O['Locus\\Square'].astype(str).str.strip() + '|' +
       O['Basket'].astype(str).str.strip())
g = key.groupby(key).size()
print(f"  {len(O)} readings -> ~{len(g)} excavation baskets (objects)")
print("  readings per basket:")
print(g.value_counts().sort_index().to_string())
print("  -> aggregate to the object before any statistics.")

hdr("7. SURFACE CONDITION (pXRF reads the surface -> quality flags)")
for c in ['cover', 'Dirt']:
    print(f"\n  {c}  (blank: {O[c].isna().sum()})")
    print(O[c].astype(str).str.strip().str.lower().value_counts().head(8).to_string())

hdr("8. CONTEXT COMPLETENESS / SITE BALANCE")
for c in ['site', 'side', 'Locus\\Square', 'Basket']:
    print(f"  {c:14s} blank: {O[c].isna().sum():4d}")
print("\n  site counts (note the imbalance):")
print(O['site'].astype(str).str.strip().value_counts().to_string())

hdr("9. SHEET-TO-SHEET DRIFT inside the master")
C = pd.read_excel(SAMPLES / MASTER, sheet_name='First Changes')
O2 = O.copy()
O2['ts'] = pd.to_datetime(O2['Time'], errors='coerce')
C['ts'] = pd.to_datetime(C['Time'], errors='coerce')
dropped = set(zip(O2['Reading No'], O2['ts'])) - set(zip(C['Reading No'], C['ts']))
print(f"  Original {len(O2)} rows -> First Changes {len(C)} rows; dropped {len(dropped)}:")
for r, t in sorted(dropped, key=lambda x: str(x[1])):
    row = O2[(O2['Reading No'] == r) & (O2['ts'] == t)]
    print(f"    reading {r} @ {t}  duration={row['Duration'].iloc[0]:.2f}s  "
          f"site={row['site'].iloc[0]}  locus={row['Locus\\Square'].iloc[0]}")
print("  -> aborted readings are fair to drop; a ~full-duration reading is not.")

print("\nDone. Narrative version: docs/raw_sample_data_map_and_quality.md")

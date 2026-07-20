#!/usr/bin/env python3
"""
Step 2 -- Build the reference database from the verified article tables.

Design principles (from docs/reference_data_verification_report.md and PLAN.md):
  * One extractor per paper; sources are kept SEPARATE per article (no cross-
    article merging here -- unification, if any, happens later and deliberately).
  * Source names are normalised for ENCODING/spelling only (Gollu -> Göllü),
    NEVER collapsing the East/West/general distinction (Göllü Dağ E stays distinct).
  * Every row keeps: paper, year, method, method_tier, source_raw, source_norm,
    source_region, role (geological source sample vs artifact assigned to a source),
    sample_id, units, and the trace elements used for sourcing.
  * Instrument QC standard rows (RGM-2 / Source == 'Standard') are dropped.

Outputs (in reference_db/):
  by_paper/<slug>.csv   -- one file per paper
  reference_long.csv    -- all rows, long format
  build_report.txt      -- per-paper / per-source counts + flags
"""

from pathlib import Path
import re
import pandas as pd
import openpyxl
import warnings
warnings.filterwarnings('ignore')

ROOT   = Path(__file__).resolve().parent.parent
TABLES = ROOT / 'data' / 'article_tables'
OUTDIR = ROOT / 'reference_db'
BYPAPER = OUTDIR / 'by_paper'
BYPAPER.mkdir(parents=True, exist_ok=True)

# Trace elements we carry through (majors/oxides deferred to a later pass)
CANON = ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Ti', 'Mn', 'Fe', 'Zn', 'Ga', 'Ba', 'Pb', 'Th']

META_COLS = ['paper', 'year', 'method', 'method_tier', 'role',
             'source_raw', 'source_norm', 'source_region', 'sample_id', 'units', 'notes']
OUT_COLS = META_COLS + CANON


# ---- helpers --------------------------------------------------------------

def load(fname, sheet):
    wb = openpyxl.load_workbook(TABLES / fname, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows


def num(v):
    """Parse a numeric cell; blanks/dashes/non-numeric -> None. Keeps 0."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(',', '')
    if s in ('', '-', '--', 'bdl', 'n.d.', 'nd', 'na'):
        return None
    try:
        return float(s)
    except ValueError:
        return None


_SUFFIXES = ['Ka1', 'Kb1', 'La1', 'Lb1', 'Ka', 'La', '(ppm)', 'ppm', '(wt%)']

def norm_elem(header):
    """Map a column header to a canonical element symbol, or None."""
    if header is None:
        return None
    h = str(header).strip()
    for suf in _SUFFIXES:
        if h.endswith(suf):
            h = h[:-len(suf)].strip()
    h = h.replace('(ppm)', '').replace('ppm', '').strip()
    return h if h in CANON else None


def norm_source(raw):
    """Fix Turkish encoding/spelling ONLY. Preserve East/West/sub-source codes."""
    if raw is None:
        return None
    s = str(raw).strip()
    s = s.replace('ǧ', 'ğ').replace('̧', '')   # caron-g -> breve-g; strip combining cedilla
    s = re.sub(r'\s+', ' ', s)
    # encoding / ASCII -> diacritic (whole-word-ish, order matters)
    repl = [
        ('Gollu', 'Göllü'), ('gollu', 'Göllü'),
        ('Bingol', 'Bingöl'), ('bingol', 'Bingöl'),
        ('Acigol', 'Acıgöl'),
        ('Da_x0002_g', 'Dağ'),
        (' Dag', ' Dağ'), ('_Dag', ' Dağ'),
        ('Mus e Konuk', 'Muşe Konuk'),
    ]
    for a, b in repl:
        s = s.replace(a, b)
    s = s.replace('_', ' ').strip()
    return s


_REGION = [
    ('Eastern Anatolia', ['bingöl', 'bingol', 'nemrut', 'muş', 'mus', 'meydan',
                          'group 3', 'pasinler', 'suphan', 'sarıkam', 'sarakam', 'kars',
                          'gurgur', 'zincirkale', ' van']),
    ('Central Anatolia (Cappadocia)', ['göllü', 'gollu', 'egd', 'wgd', 'nenezi',
                                       'acıgöl', 'acigol', 'hasan', 'kaletepe',
                                       'kömürcü', 'komurcu', 'kayırlı', 'kayirli']),
    ('Aegean', ['melos', 'giali', 'yali', 'antiparos', 'demene', 'nychia']),
    ('Central Europe', ['carpathian']),
    ('Central Mediterranean', ['arci', 'lipari', 'palmarola', 'pantelleria']),
]

def region(source_norm):
    if not source_norm:
        return 'unknown'
    s = source_norm.lower()
    for name, toks in _REGION:
        if any(t in s for t in toks):
            return name
    return 'other/verify'


def find_source_col(header):
    for j, h in enumerate(header):
        if h is not None and str(h).strip().lower() == 'source':
            return j
    return None


def extract(rows, header_idx, meta, role, source_col=None, source_fixed=None,
            id_col=0, drop_standard=True):
    """Generic row extractor given a header row index."""
    header = rows[header_idx]
    if source_col is None:
        source_col = find_source_col(header)
    colmap = {}
    for j, h in enumerate(header):
        e = norm_elem(h)
        if e and e not in colmap:
            colmap[e] = j
    recs = []
    for r in rows[header_idx + 1:]:
        if not any(c is not None and str(c).strip() != '' for c in r):
            continue
        src = None
        if source_col is not None and source_col < len(r):
            src = r[source_col]
        if src is None or str(src).strip() == '':
            src = source_fixed
        if src is None:
            continue
        src_raw = str(src).strip()
        if src_raw.lower() in ('source', 'average', 'mean', 'nan'):
            continue  # stray header / aggregate rows
        if drop_standard and re.search(r'\b(standard|rgm-?2|std)\b', src_raw, re.I):
            continue
        sid = None
        if id_col is not None and id_col < len(r) and r[id_col] is not None:
            sid = str(r[id_col]).strip()
        sn = norm_source(src_raw)
        rec = dict(meta)
        rec.update(role=role, source_raw=src_raw, source_norm=sn,
                   source_region=region(sn), sample_id=sid)
        for e in CANON:
            j = colmap.get(e)
            rec[e] = num(r[j]) if (j is not None and j < len(r)) else None
        recs.append(rec)
    return recs


# ---- per-paper extractors -------------------------------------------------

def milic_2014():
    rows = load('data1.xlsx', 'Milic 2014')
    # find the per-sample header row: col0 == 'Source' AND 'Ti' present
    hidx = None
    for i, r in enumerate(rows):
        cells = [str(c).strip() if c is not None else '' for c in r]
        if cells and cells[0] == 'Source' and any(c.startswith('Ti') for c in cells):
            hidx = i
            break
    meta = dict(paper='Milic 2014', year=2014, method='pXRF', method_tier=1,
                units='ppm', notes='per-sample block')
    return extract(rows, hidx, meta, role='source_sample', source_col=0, id_col=None)


def campbell_healey():
    recs = []
    meta = dict(paper='Campbell & Healey 2016', year=2016, method='pXRF',
                method_tier=1, units='ppm',
                notes='Kenan Tepe artifacts grouped by assigned source')
    for sheet in ['Bingöl A', 'Bingöl B', 'Nemrut Dağ', 'Muş', 'Meydan Dağ', 'Group 3d']:
        rows = load('campbell and healey 1.xlsx', sheet)
        recs += extract(rows, 0, meta, role='artifact_assigned', id_col=0)
    return recs


def schechter_2016():
    rows = load('data1.xlsx', 'Schechter et al 2016')
    meta = dict(paper='Schechter et al 2016', year=2016, method='pXRF',
                method_tier=1, units='ppm', notes='Levant-site artifacts assigned to source')
    return extract(rows, 0, meta, role='artifact_assigned', id_col=0)


def frahm_hauck_main():
    rows = load('Frahm and Hauck 2017.xlsx', 'MAIN')
    meta = dict(paper='Frahm & Hauck 2017', year=2017, method='multi (see paper)',
                method_tier=2, units='ppm', notes='MAIN sheet; per-specimen source data')
    recs = extract(rows, 0, meta, role='source_sample', source_col=0, id_col=1)
    # Drop aggregate ('Average') and mislabelled ('artifact') rows -- not source samples
    drop = {'average', 'artifact'}
    return [r for r in recs if r['source_raw'].strip().lower() not in drop]


def carter_shackley_2007():
    rows = load('data2.xlsx', 'Carter and Shackley 2007')
    meta = dict(paper='Carter & Shackley 2007', year=2007, method='EDXRF',
                method_tier=2, units='ppm', notes='Çatalhöyük artifacts assigned to source')
    return extract(rows, 0, meta, role='artifact_assigned', id_col=0)


def carter_2017():
    rows = load('data2.xlsx', 'Carter et al. 2017')
    meta = dict(paper='Carter et al 2017', year=2017, method='EDXRF',
                method_tier=2, units='ppm', notes='Shaʿar Hagolan artifacts assigned to source')
    return extract(rows, 0, meta, role='artifact_assigned', id_col=0)


def kortik_2013():
    rows = load('data2.xlsx', 'Carter et al 2013')
    meta = dict(paper='Carter et al 2013 (Körtik Tepe)', year=2013, method='EDXRF',
                method_tier=2, units='ppm', notes='Körtik Tepe artifacts; RGM-2 standards dropped')
    return extract(rows, 0, meta, role='artifact_assigned', id_col=0)


def carter_rosenberg_2022():
    recs = []
    f = 'Carter_Rosenberg_2022_Tel_Tsaf.xlsx'
    m6 = dict(paper='Carter & Rosenberg 2022', year=2022, method='EDXRF',
              method_tier=2, units='ppm', notes='Tel Tsaf source reference samples')
    recs += extract(load(f, 'Table6_Source_Samples'), 0, m6,
                    role='source_sample', source_col=0, id_col=None)
    m5 = dict(paper='Carter & Rosenberg 2022', year=2022, method='EDXRF',
              method_tier=2, units='ppm', notes='Tel Tsaf obsidian beads (artifacts)')
    recs += extract(load(f, 'Table5_Bead_Measurements'), 0, m5,
                    role='artifact_assigned', id_col=0)
    return recs


EXTRACTORS = [milic_2014, campbell_healey, schechter_2016, frahm_hauck_main,
              carter_shackley_2007, carter_2017, kortik_2013, carter_rosenberg_2022]


def slug(p):
    return re.sub(r'[^a-z0-9]+', '_', p.lower()).strip('_')


def main():
    all_recs = []
    for fn in EXTRACTORS:
        recs = fn()
        all_recs += recs
    df = pd.DataFrame(all_recs)
    df = df.reindex(columns=OUT_COLS)

    # per-paper CSVs
    for paper, g in df.groupby('paper'):
        g.to_csv(BYPAPER / f'{slug(paper)}.csv', index=False)
    df.to_csv(OUTDIR / 'reference_long.csv', index=False)

    # report
    lines = ['REFERENCE DB BUILD -- Step 2 (Tier 1/2 clean sheets)',
             '=' * 64, f'Total rows: {len(df)}   Papers: {df["paper"].nunique()}', '']
    for paper, g in df.groupby('paper'):
        tier = g['method_tier'].iloc[0]
        meth = g['method'].iloc[0]
        roles = g['role'].value_counts().to_dict()
        lines.append(f'{paper}  [T{int(tier)} {meth}]  n={len(g)}  roles={roles}')
        for (src, reg), gs in g.groupby(['source_norm', 'source_region']):
            miss = [e for e in ['Rb', 'Sr', 'Zr', 'Nb'] if gs[e].isna().all()]
            missnote = f'  (no {",".join(miss)})' if miss else ''
            lines.append(f'    {src:22s} [{reg:28s}] n={len(gs):4d}{missnote}')
        lines.append('')
    rep = '\n'.join(lines)
    (OUTDIR / 'build_report.txt').write_text(rep, encoding='utf-8')
    print(rep)
    print(f'Wrote {len(list(BYPAPER.glob("*.csv")))} per-paper CSVs + reference_long.csv')


if __name__ == '__main__':
    main()

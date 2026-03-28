#!/usr/bin/env python3
"""
Phase 5b -- Anomaly screening: identify non-obsidian and chemically unusual items.

Criteria tested (in order of severity):
  A. Explicitly flagged as flint/chert in remarks or locus field
  B. Near-zero Rb (< 30 ppm) AND near-zero Nb (< 10 ppm) -- obsidian always has both
  C. Very high Ca (> 30,000 ppm) -- carbonate/limestone matrix, not volcanic glass
  D. Very high Fe (> 25,000 ppm) -- can indicate chert/ironstone
  E. Rb absent (NaN) AND Nb absent (NaN) -- no volcanic fingerprint measurable
  F. Nb/Zr ratio extreme outlier (outside 3-sigma of assemblage)
  G. Zr extreme outlier (> 3-sigma) -- possible different volcanic source family

Outputs:
  outputs/reports/anomaly_screen_report.txt   -- plain-language per-item table
  outputs/figures/anomaly/anomaly_biplot.png  -- Nb vs Zr with anomalies highlighted
  outputs/figures/anomaly/Ca_Fe_screen.png    -- Ca vs Fe scatter to show non-obsidian
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT    = Path(__file__).parent.parent
CSV     = ROOT / 'my_samples' / 'samples_clean.csv'
FIGS    = ROOT / 'outputs' / 'figures' / 'anomaly'
REPORTS = ROOT / 'outputs' / 'reports'
FIGS.mkdir(parents=True, exist_ok=True)

REPORT = REPORTS / 'anomaly_screen_report.txt'

# ---- load ----------------------------------------------------------------
df = pd.read_csv(CSV)

lines = []
def log(s=''):
    lines.append(s)
    print(s)

log('=' * 70)
log('PHASE 5b -- ANOMALY SCREEN: NON-OBSIDIAN / UNUSUAL ITEMS')
log('=' * 70)
log(f'Total items in samples_clean.csv: {len(df)}')
log()

# ---- reference values from normal obsidian -------------------------------
# Compute from items with material == 'obsidian' and quality not beam_minimal
obs = df[(df['material'] == 'obsidian')].copy()
log(f'Items labelled "obsidian": {len(obs)}')
log()

# --------------------------------------------------------------------------
# FLAG EACH CRITERION
# --------------------------------------------------------------------------

df['flag_A'] = (
    df['remarks'].astype(str).str.contains('flint|chert', case=False, na=False) |
    df['locus'].astype(str).str.contains('chert', case=False, na=False) |
    df['material'].astype(str).str.contains('flint|chert', case=False, na=False)
)

# Rb < 30 ppm (or NaN) AND Nb < 10 ppm (or NaN) -- both must be near-zero
rb_low  = df['Rb'].fillna(0) < 30
nb_low  = df['Nb'].fillna(0) < 10
df['flag_B'] = rb_low & nb_low

# Ca > 30,000 ppm
df['flag_C'] = df['Ca'].fillna(0) > 30000

# Fe > 25,000 ppm
df['flag_D'] = df['Fe'].fillna(0) > 25000

# Both Rb AND Nb NaN (no volcanic fingerprint at all)
df['flag_E'] = df['Rb'].isna() & df['Nb'].isna()

# Nb/Zr ratio outlier (compute only where Zr > 0)
with np.errstate(divide='ignore', invalid='ignore'):
    df['NbZr'] = np.where(df['Zr'].fillna(0) > 0, df['Nb'].fillna(0) / df['Zr'].fillna(0), np.nan)

# Refresh obs after new column added
obs = df[(df['material'] == 'obsidian')].copy()

# Use only normal obsidian to set the reference distribution
obs_nbzr = obs['NbZr'].dropna()
nbzr_mean = obs_nbzr.mean()
nbzr_std  = obs_nbzr.std()
df['flag_F'] = (df['NbZr'] - nbzr_mean).abs() > 3 * nbzr_std

# Zr extreme outlier (> mean+3sd on obsidian)
obs_zr   = obs['Zr'].dropna()
zr_mean  = obs_zr.mean()
zr_std   = obs_zr.std()
df['flag_G'] = df['Zr'].fillna(0) > (zr_mean + 3 * zr_std)

# ---- combined anomaly flag -----------------------------------------------
any_flag = df[['flag_A','flag_B','flag_C','flag_D','flag_E','flag_F','flag_G']].any(axis=1)
anomalies = df[any_flag].copy()

log(f'Nb/Zr reference (obsidian): mean={nbzr_mean:.3f}  SD={nbzr_std:.3f}')
log(f'Zr reference (obsidian):    mean={zr_mean:.1f}   SD={zr_std:.1f}')
log(f'3-sigma Zr threshold:       > {zr_mean + 3*zr_std:.1f} ppm')
log()
log(f'Items flagged by at least one criterion: {len(anomalies)}')
log()

# ---- per-criterion summary -----------------------------------------------
log('-' * 70)
log('PER-CRITERION COUNTS')
log('-' * 70)
criteria = {
    'A': 'Explicitly labelled flint/chert',
    'B': 'Near-zero Rb (<30 ppm) AND Nb (<10 ppm)',
    'C': 'High Ca (>30,000 ppm) -- carbonate matrix',
    'D': 'High Fe (>25,000 ppm)',
    'E': 'Both Rb and Nb values absent (NaN)',
    'F': 'Nb/Zr ratio outside 3-sigma of obsidian assemblage',
    'G': 'Zr > mean+3SD of obsidian (possible peralkaline or other source)',
}
for k, desc in criteria.items():
    n = df[f'flag_{k}'].sum()
    log(f'  {k}: {desc}')
    log(f'     --> {n} item(s) flagged')
log()

# ---- detailed table ------------------------------------------------------
log('=' * 70)
log('DETAILED ANOMALY TABLE')
log('=' * 70)
log()

# Build a readable flag string
def flag_str(row):
    flags = []
    for k in 'ABCDEFG':
        if row[f'flag_{k}']:
            flags.append(k)
    return ','.join(flags)

anomalies = anomalies.copy()
anomalies['flags'] = anomalies.apply(flag_str, axis=1)

# Sort: A flags first (definite flint), then by flag combination
anomalies = anomalies.sort_values(['flag_A', 'flag_C', 'flag_D'], ascending=False)

cols_show = ['item_id', 'site', 'locus', 'basket', 'material', 'remarks',
             'Rb', 'Zr', 'Nb', 'NbZr', 'Fe', 'Ca', 'quality_flag', 'flags']

for _, row in anomalies.iterrows():
    log(f"item_id  : {row['item_id']}")
    log(f"  site   : {row['site']}   locus={row['locus']}   basket={row['basket']}")
    log(f"  material: {row['material']}   remarks: {row['remarks']}")
    nbzr_str = f"{row['NbZr']:.3f}" if pd.notna(row['NbZr']) else 'n/a'
    log(f"  Rb={row['Rb']}  Zr={row['Zr']}  Nb={row['Nb']}  Nb/Zr={nbzr_str}")
    log(f"  Fe={row['Fe']}  Ca={row['Ca']}")
    log(f"  quality_flag: {row['quality_flag']}")
    log(f"  FLAGS: {row['flags']}  ({', '.join(criteria[f] for f in row['flags'].split(',') if f)})")
    log()

# ---- category summary ----------------------------------------------------
log('=' * 70)
log('INTERPRETATION CATEGORIES')
log('=' * 70)
log()

# Category 1: very likely NOT obsidian (A or (B and C/D))
cat1 = anomalies[anomalies['flag_A'] | (anomalies['flag_B'] & (anomalies['flag_C'] | anomalies['flag_D']))]
log(f'CATEGORY 1 -- Almost certainly NOT obsidian (flint/chert/limestone): {len(cat1)} item(s)')
for _, r in cat1.iterrows():
    log(f"  {r['item_id']:20s}  Rb={r['Rb']}  Zr={r['Zr']}  Nb={r['Nb']}  Ca={r['Ca']}  Fe={r['Fe']}  flags={r['flags']}")
log()

# Category 2: high Ca/Fe without zero Rb -- possibly surface contamination or unusual obsidian
cat2 = anomalies[~anomalies.index.isin(cat1.index) & (anomalies['flag_C'] | anomalies['flag_D'])]
log(f'CATEGORY 2 -- Anomalous Ca or Fe, but Rb/Nb present (possible contamination or unusual material): {len(cat2)} item(s)')
for _, r in cat2.iterrows():
    _nbzr2 = f"{r['NbZr']:.3f}" if pd.notna(r['NbZr']) else 'n/a'
    log(f"  {r['item_id']:20s}  Rb={r['Rb']}  Zr={r['Zr']}  Nb={r['Nb']}  Nb/Zr={_nbzr2}  Ca={r['Ca']}  Fe={r['Fe']}  flags={r['flags']}")
log()

# Category 3: Nb/Zr outlier (unusual source signal)
cat3 = anomalies[~anomalies.index.isin(cat1.index) & ~anomalies.index.isin(cat2.index) & (anomalies['flag_F'] | anomalies['flag_G'])]
log(f'CATEGORY 3 -- Source chemistry outlier (unusual Nb/Zr or high Zr -- different source family): {len(cat3)} item(s)')
for _, r in cat3.iterrows():
    _nbzr3 = f"{r['NbZr']:.3f}" if pd.notna(r['NbZr']) else 'n/a'
    log(f"  {r['item_id']:20s}  Rb={r['Rb']}  Zr={r['Zr']}  Nb={r['Nb']}  Nb/Zr={_nbzr3}  Ca={r['Ca']}  Fe={r['Fe']}  flags={r['flags']}")
log()

# Category 4: all other flagged (Rb/Nb near zero but no other red flag -- possibly measurement issue)
cat4 = anomalies[~anomalies.index.isin(cat1.index) & ~anomalies.index.isin(cat2.index) & ~anomalies.index.isin(cat3.index)]
log(f'CATEGORY 4 -- Rb/Nb near zero only (possible measurement artifact, no positive non-obsidian indicator): {len(cat4)} item(s)')
for _, r in cat4.iterrows():
    log(f"  {r['item_id']:20s}  Rb={r['Rb']}  Zr={r['Zr']}  Nb={r['Nb']}  Ca={r['Ca']}  Fe={r['Fe']}  flags={r['flags']}")
log()

log('=' * 70)
log('REFERENCE: Typical obsidian assemblage values')
log('=' * 70)
log(f'  Rb:   mean={obs["Rb"].mean():.1f}  SD={obs["Rb"].std():.1f}')
log(f'  Zr:   mean={obs["Zr"].mean():.1f}  SD={obs["Zr"].std():.1f}')
log(f'  Nb:   mean={obs["Nb"].mean():.1f}  SD={obs["Nb"].std():.1f}')
log(f'  Nb/Zr mean={nbzr_mean:.3f}  SD={nbzr_std:.3f}')
log(f'  Fe:   mean={obs["Fe"].mean():.0f}  SD={obs["Fe"].std():.0f}')
log(f'  Ca:   mean={obs["Ca"].mean():.0f}  SD={obs["Ca"].std():.0f}')

# ---- write report --------------------------------------------------------
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'\nReport saved: {REPORT}')

# ---- FIGURES -------------------------------------------------------------

# --- Fig 1: Nb vs Zr, anomalies highlighted -------------------------------
fig, ax = plt.subplots(figsize=(10, 7))

normal = df[~any_flag & (df['material'] == 'obsidian')]
ax.scatter(normal['Zr'], normal['Nb'], c='steelblue', alpha=0.3, s=15,
           label=f'Normal obsidian (N={len(normal)})')

colors_cat = {
    'Cat1 (not obsidian)':    ('#d32f2f', cat1),
    'Cat2 (Ca/Fe anomaly)':   ('#f57c00', cat2),
    'Cat3 (source outlier)':  ('#7b1fa2', cat3),
    'Cat4 (Rb/Nb low)':       ('#388e3c', cat4),
}
for label, (color, catdf) in colors_cat.items():
    if len(catdf):
        ax.scatter(catdf['Zr'], catdf['Nb'], c=color, s=60, zorder=5,
                   edgecolors='k', linewidths=0.5, label=f'{label} (N={len(catdf)})')
        for _, r in catdf.iterrows():
            ax.annotate(str(r['item_id']), (r['Zr'], r['Nb']),
                        fontsize=6, xytext=(4, 4), textcoords='offset points')

ax.set_xlabel('Zr (ppm)')
ax.set_ylabel('Nb (ppm)')
ax.set_title('Nb vs Zr — anomaly screening\n(all items in samples_clean.csv)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig1_path = FIGS / 'anomaly_NbZr.png'
fig.savefig(fig1_path, dpi=150)
plt.close()
print(f'Figure saved: {fig1_path}')

# --- Fig 2: Ca vs Fe scatter to show non-obsidian matrix ------------------
fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(normal['Ca'].fillna(0), normal['Fe'].fillna(0),
           c='steelblue', alpha=0.3, s=15, label=f'Normal obsidian (N={len(normal)})')

for label, (color, catdf) in colors_cat.items():
    if len(catdf):
        ax.scatter(catdf['Ca'].fillna(0), catdf['Fe'].fillna(0),
                   c=color, s=60, zorder=5, edgecolors='k', linewidths=0.5,
                   label=f'{label} (N={len(catdf)})')
        for _, r in catdf.iterrows():
            ax.annotate(str(r['item_id']), (r['Ca'] if pd.notna(r['Ca']) else 0,
                                             r['Fe'] if pd.notna(r['Fe']) else 0),
                        fontsize=6, xytext=(4, 4), textcoords='offset points')

ax.set_xlabel('Ca (ppm)')
ax.set_ylabel('Fe (ppm)')
ax.set_title('Ca vs Fe — non-obsidian matrix screening\n(high Ca or Fe = likely not volcanic glass)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig2_path = FIGS / 'anomaly_CaFe.png'
fig.savefig(fig2_path, dpi=150)
plt.close()
print(f'Figure saved: {fig2_path}')

# --- Fig 3: Rb vs Zr with anomalies highlighted ---------------------------
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(normal['Zr'], normal['Rb'], c='steelblue', alpha=0.3, s=15,
           label=f'Normal obsidian (N={len(normal)})')
for label, (color, catdf) in colors_cat.items():
    if len(catdf):
        ax.scatter(catdf['Zr'], catdf['Rb'].fillna(0), c=color, s=60, zorder=5,
                   edgecolors='k', linewidths=0.5, label=f'{label} (N={len(catdf)})')
        for _, r in catdf.iterrows():
            ax.annotate(str(r['item_id']), (r['Zr'], r['Rb'] if pd.notna(r['Rb']) else 0),
                        fontsize=6, xytext=(4, 4), textcoords='offset points')
ax.set_xlabel('Zr (ppm)')
ax.set_ylabel('Rb (ppm)')
ax.set_title('Rb vs Zr — anomaly screening')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig3_path = FIGS / 'anomaly_RbZr.png'
fig.savefig(fig3_path, dpi=150)
plt.close()
print(f'Figure saved: {fig3_path}')

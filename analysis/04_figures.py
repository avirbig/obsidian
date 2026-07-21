#!/usr/bin/env python3
"""
Step 6 -- Figures for the supervisor report.

Four figures, each making ONE point about the data:
  fig1  the resolution limit      -- Rb/Zr/Nb take only 9/15/6 distinct values
  fig2  the calibration gap       -- our samples sit below every Anatolian source
  fig3  one chemical group        -- why we cannot count how many sources there are
  fig4  the second source         -- the peralkaline Yiftahel object

Design (from the dataviz skill's reference palette, light mode only -- these are
printed in a report, so a single deliberate look):
  * marks thin, grid a hairline one shade off the surface, axes recessive
  * text in ink tokens, never in a series colour
  * legend whenever there are 2+ series; direct labels used selectively
  * emphasis form (one accent + grey) wherever one series is the point
  * palette slots 1 and 2 only -- the documented all-pairs-validated pair
"""

from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

warnings.filterwarnings('ignore')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'results' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

# ---- palette (reference instance, light mode) -------------------------------
SURFACE = '#fcfcfb'
INK = '#0b0b0b'
INK2 = '#52514e'
MUTED = '#898781'
GRID = '#e1e0d9'
AXIS = '#c3c2b7'
S1 = '#2a78d6'      # slot 1 blue  -- "our data"
S2 = '#008300'      # slot 2 green -- reference / the highlighted finding

plt.rcParams.update({
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE,
    'savefig.facecolor': SURFACE,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'DejaVu Sans', 'sans-serif'],
    'text.color': INK, 'axes.labelcolor': INK2, 'axes.titlecolor': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'axes.edgecolor': AXIS, 'axes.linewidth': 0.8,
    'grid.color': GRID, 'grid.linewidth': 0.8, 'grid.linestyle': '-',
    'axes.grid': True, 'axes.axisbelow': True,
    'legend.frameon': False, 'figure.dpi': 150,
})


def style(ax, xlabel=None, ylabel=None):
    """Axis chrome only. Titles are placed at FIGURE level by titles() below --
    axes-level titles plus a subtitle collide once the subtitle wraps."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    ax.tick_params(labelsize=9, length=0)


def titles(fig, title, sub=None, top=0.86):
    """Title + wrapped subtitle above the plot, with the plot area shrunk to fit.
    Reserving the space explicitly is what prevents the overlap."""
    fig.text(0.012, 0.985, title, fontsize=13, fontweight='bold',
             color=INK, ha='left', va='top')
    if sub:
        fig.text(0.012, 0.925, sub, fontsize=9.5, color=INK2,
                 ha='left', va='top', wrap=True)
    fig.subplots_adjust(top=top)


O = pd.read_csv(ROOT / 'samples_db' / 'samples_objects.csv')
RD = pd.read_csv(ROOT / 'samples_db' / 'samples_readings.csv')
REF = pd.read_csv(ROOT / 'reference_db' / 'reference_source_only.csv')

# archaeological objects only -- the "Modern" locus item is a modern comparative
# specimen the researcher measured, not an excavated artefact.
MODERN = O['object_id'].str.contains('reading-1703', regex=False)
ARCH = O[~MODERN].copy()
print(f"objects: {len(O)} total, {len(ARCH)} archaeological, "
      f"{int(MODERN.sum())} modern comparative")

# =============================================================== FIGURE 1 ====
# The resolution limit. One series -> one colour, no legend needed.

kept = RD[RD['kept'] == True]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.9))
NOTE = {'Zr': '+ 3 readings at 640–1,020 ppm\n(the peralkaline object, off scale)'}
# each element has its own range -- a shared x-limit hides Nb entirely
XLIM = {'Rb': (45, 145), 'Zr': (40, 205), 'Nb': (10, 80)}
WIDTH = {'Rb': 6, 'Zr': 6, 'Nb': 4}
for ax, el in zip(axes, ['Rb', 'Zr', 'Nb']):
    v = (pd.to_numeric(kept[el], errors='coerce') * 10000).dropna()
    counts = v.value_counts().sort_index()
    lo, hi = XLIM[el]
    shown = counts[(counts.index >= lo) & (counts.index <= hi)]
    ax.bar(shown.index, shown.values, width=WIDTH[el], color=S1, zorder=3)
    style(ax, xlabel='ppm', ylabel='measurements' if el == 'Rb' else None)
    ax.set_xlim(lo, hi)
    ax.text(0.02, 1.06, el, transform=ax.transAxes, fontsize=11.5,
            fontweight='bold', color=INK, va='bottom')
    ax.text(0.98, 1.06, f'{v.nunique()} distinct values', transform=ax.transAxes,
            ha='right', va='bottom', fontsize=10, color=S1, fontweight='bold')
    if el in NOTE:
        ax.text(0.97, 0.82, NOTE[el], transform=ax.transAxes, ha='right', va='top',
                fontsize=8, color=MUTED, style='italic')
    ax.grid(axis='x', visible=False)
titles(fig,
       'The instrument records in steps of 10 ppm, so these elements take very few values',
       'Each bar is one value the instrument is able to express. Rubidium has 8 in the whole '
       'dataset; Niobium is effectively two, so it cannot carry a fine distinction.',
       top=0.74)
fig.savefig(OUT / 'fig1_resolution.png', bbox_inches='tight')
plt.close(fig)
print('fig1_resolution.png')

# =============================================================== FIGURE 2 ====
# The calibration gap. Two series -> legend + selective direct labels.

g = REF.groupby('source_norm').agg(n=('Rb', 'size'), Rb=('Rb', 'median'),
                                   Zr=('Zr', 'median'),
                                   region=('source_region', 'first')).reset_index()
g = g[(g['n'] >= 3) & g['Rb'].notna() & g['Zr'].notna()]

fig, ax = plt.subplots(figsize=(9.5, 6.2))
ax.scatter(g['Rb'], g['Zr'], s=62, color=S2, zorder=4,
           edgecolors=SURFACE, linewidths=2, label=f'Published volcano sources (n={len(g)})')
ax.scatter(ARCH['Rb_ppm'], ARCH['Zr_ppm'], s=24, color=S1, alpha=.45,
           edgecolors='none', zorder=3, label=f'Our objects (n={len(ARCH)})')

LABEL = ['Göllü Dağ', 'Nenezi Dağ', 'Acıgöl', 'Hasan Dağ', 'Bingöl A',
         'Nemrut Dağ A', 'Meydan Dağ', 'Kars-Digor']
OFFSET = {'Nemrut Dağ A': (-8, -14), 'Bingöl A': (8, -4), 'Hasan Dağ': (8, -2),
          'Kars-Digor': (-8, 6), 'Meydan Dağ': (8, -2), 'Nenezi Dağ': (8, 6)}
for _, r in g.iterrows():
    if r['source_norm'] in LABEL:
        dx, dy = OFFSET.get(r['source_norm'], (8, 3))
        ax.annotate(r['source_norm'], (r['Rb'], r['Zr']), fontsize=8.5, color=INK2,
                    xytext=(dx, dy), textcoords='offset points',
                    ha='right' if dx < 0 else 'left')

# the peralkaline object -- worth naming, it is the one point of ours near the top
pk = ARCH.loc[ARCH['Zr_ppm'].idxmax()]
ax.annotate('our peralkaline object', (pk['Rb_ppm'], pk['Zr_ppm']), fontsize=8.5,
            color=S1, fontweight='bold', xytext=(10, -14), textcoords='offset points',
            ha='left')

ax.set_yscale('log')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:,.0f}'))
ax.set_xlim(40, 290)
style(ax, xlabel='Rubidium (ppm)', ylabel='Zirconium (ppm, log scale)')
titles(fig, 'Our objects sit apart from every published source',
       'Rubidium against Zirconium. Our objects cluster at Rb ≈ 90 ppm and Zr ≈ 65 ppm — low and '
       'to the left of the whole reference set. A calibration offset is the likeliest cause.',
       top=0.845)
ax.legend(fontsize=9.5, loc='upper left', labelcolor=INK2)
fig.savefig(OUT / 'fig2_calibration_gap.png', bbox_inches='tight')
plt.close(fig)
print('fig2_calibration_gap.png')

# =============================================================== FIGURE 3 ====
# One chemical group. Single series -> one colour, no legend.

fig, ax = plt.subplots(figsize=(9.5, 4.6))
d = ARCH['Rb_Zr'].dropna()
d = d[d > 0.5]
ax.hist(d, bins=np.arange(0.55, 1.95, 0.05), color=S1, zorder=3, rwidth=.86)
style(ax, xlabel='Rb / Zr ratio', ylabel='objects')
ax.grid(axis='x', visible=False)
med = d.median()
ax.axvline(med, color=INK2, lw=1, zorder=4)
ax.annotate(f'median {med:.2f}', (med, ax.get_ylim()[1] * 0.99), fontsize=9.5,
            color=INK2, ha='left', va='top', xytext=(6, 0), textcoords='offset points')
titles(fig, 'The bulk of the assemblage forms a single chemical group',
       'Rb/Zr ratio of each object. One peak, no separate clusters. But the ragged spikes are the '
       'instrument’s 10 ppm steps, not real sub-groups — which is exactly why we cannot count how '
       'many sources are present.',
       top=0.80)
fig.savefig(OUT / 'fig3_one_group.png', bbox_inches='tight')
plt.close(fig)
print('fig3_one_group.png')

# =============================================================== FIGURE 4 ====
# The second source. Emphasis form: accent for the finding, grey for context.

fig, ax = plt.subplots(figsize=(9.5, 5.0))
srt = ARCH.dropna(subset=['Zr_ppm']).sort_values('Zr_ppm').reset_index(drop=True)
is_out = srt['Zr_ppm'] > 300
ax.scatter(srt.index[~is_out], srt.loc[~is_out, 'Zr_ppm'], s=14, color=S1,
           alpha=.45, edgecolors='none', zorder=3,
           label=f'Ordinary objects (n={int((~is_out).sum())})')
ax.scatter(srt.index[is_out], srt.loc[is_out, 'Zr_ppm'], s=95, color=S2,
           edgecolors=SURFACE, linewidths=2, zorder=5,
           label=f'Peralkaline object (n={int(is_out.sum())})')
for i in srt.index[is_out]:
    ax.annotate(f"Yiftahel — {srt.loc[i, 'Zr_ppm']:,.0f} ppm",
                (i, srt.loc[i, 'Zr_ppm']), fontsize=9.5, color=S2, fontweight='bold',
                xytext=(-14, -4), textcoords='offset points', ha='right', va='center')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:,.0f}'))
ax.set_ylim(38, 2600)
# reference lines labelled on the LEFT, where the plot is empty
# the two lines are close on a log scale -- label one above, one below, or they collide
for y, lab, va, mult in [(1354, 'Bingöl A (reference source)', 'bottom', 1.09),
                         (1229, 'Nemrut Dağ A (reference source)', 'top', 0.93)]:
    ax.axhline(y, color=MUTED, lw=.9, zorder=2)
    ax.text(6, y * mult, lab, fontsize=8.5, color=INK2, ha='left', va=va)
style(ax, xlabel='objects, ordered by Zirconium content',
      ylabel='Zirconium (ppm, log scale)')
ax.grid(axis='x', visible=False)
titles(fig, 'One object comes from a different, high-Zirconium source',
       'Every archaeological object by Zirconium. The flat steps are the instrument’s resolution. '
       'A calibration error shifts all points together — it cannot lift one object 15× above the '
       'rest, so this finding holds despite the calibration problem.',
       top=0.80)
ax.legend(fontsize=9.5, loc='center left', labelcolor=INK2,
          bbox_to_anchor=(0.02, 0.42))
fig.savefig(OUT / 'fig4_second_source.png', bbox_inches='tight')
plt.close(fig)
print('fig4_second_source.png')

print(f'\nwritten to {OUT}')

# Audit of the Previous Analysis (GitHub Copilot work)

*Prepared by Claude, 2026-07-20. The prior work is preserved untouched in
`../Analysis with GitHub Copilot/`. This document records what was found so the
new analysis does not repeat the same mistakes.*

## Bottom line
The extraction of reference data from the article tables was careful and well
verified (0 element mismatches on re-check). The reporting was faithful to the
computed numbers. **But the source-attribution step rested on a data-integrity
bug that undermines its statistical claims**, and the pipeline was not
reproducible. The headline archaeological conclusion (Göllü Dağ dominance) is
probably still directionally correct, but the confidence numbers and the
EGD-vs-GolluDag split are not trustworthy as reported.

## Critical findings

### 1. Analytical tiers were mislabeled → cross-instrument comparison
The project's own inventory defines **Tier 1 = pXRF only**; LA-ICP-MS and
ICP-MS are only "partially comparable" (Tier 3). But in the master reference
table, **Carter et al. 2006 (ICP-MS)** and **Binder et al. 2011 (LA-ICP-MS)**
were tagged `method_tier = 1`. Consequences:

| Source | "Tier 1" rows used | Actual method |
|---|---|---|
| EGD | 63 | 55 ICP-MS + 8 LA-ICP-MS = **0% pXRF** |
| ND  | 46 | 45 ICP-MS + 1 pXRF |
| GolluDag | 25 | genuine pXRF |

The samples are pXRF. So EGD (and half the "Göllü Dağ complex") was attributed
by comparing pXRF samples against non-pXRF references — the exact cross-method
comparison the tier system was meant to prevent. The EGD/GolluDag split that the
old report calls a "statistical artifact of the same volcano" is really a
consequence of this mislabel.

### 2. Only ~40% of items fall inside any 95% confidence ellipse
201 / 505 items were `confident`; the other ~60% are "nearest source" but a poor
statistical fit. The headline percentages counted every nearest-neighbor
assignment regardless of goodness of fit.

### 3. Nearest-source Mahalanobis with heterogeneous covariances
Per-source covariances came from different instruments (tight ICP vs. wide
pXRF), which biases assignment. Every item is forced onto some source — there is
no "unassigned/unknown" outcome. `Group3d` (unknown geological location, N=279)
sat in the candidate pool as a real attractor.

### 4. Rb×2 calibration is ad hoc and circular
The ×2 Rb factor was "empirically derived from EGD comparison" and then used to
attribute back toward EGD. Mitigated (primary attribution used Zr/Nb only), but
unvalidated by any external standard.

### 5. Not reproducible
9 of 12 scripts hardcoded `Path(r'c:\work\code\obsidian')`, a path that does not
exist on this machine. The pipeline could not be regenerated end-to-end.

## Minor
- 38% of items (192/510) flagged `repeat_divergent` (≥10% CV between readings)
  yet used in attribution with no down-weighting.
- Non-obsidian bookkeeping inconsistent: report says 5 excluded, only 3 were
  re-labeled `flint?`; the 2 "green" items stayed labeled obsidian (they drop
  out of attribution anyway for lacking Zr/Nb, so no numeric harm).
- Sr essentially unusable (47/507 measured).

## Principles for the redo (guardrails)
1. **Raw vs. derived is now physical**: raw inputs live in `data/` (read-only);
   all new outputs go in `reference_db/` and `results/`. Never read a derived
   file the new pipeline did not itself produce.
2. **Tier discipline**: method → tier mapping is re-derived from the articles,
   not inherited. Attribution uses **pXRF-vs-pXRF only** as the primary result;
   any cross-method comparison is a clearly-labeled secondary sensitivity check.
3. **Report fit, not just nearest**: every attribution carries a goodness-of-fit
   / confidence value; items outside all sources get an explicit "unassigned".
4. **Reproducible paths**: all scripts resolve paths from `__file__`; the whole
   pipeline must run top-to-bottom on this machine.
5. **Calibration is declared, not fitted to the target**: any Rb (or other)
   correction is stated as an assumption with a sensitivity check, never derived
   from the source we then attribute to.

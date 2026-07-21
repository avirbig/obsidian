# ⚠️ CRITICAL: Our measurements cannot currently be matched to the published sources

*Found 2026-07-21, while checking whether the reference volcanoes are separated
by more than our measurement uncertainty. They are — 85% of source pairs are
separable in principle. The problem is different, and more serious.*

---

## The finding in one sentence

**Our samples read Rb ≈ 90 ppm, but every Anatolian source in the reference
database sits at Rb ≥ 109 ppm, and most between 130 and 270 ppm — our numbers
fall below the entire published range, and we have no standard measurement that
would let us correct for it.**

---

## The evidence

Our samples (1227 readings, converted from % to ppm):

| | median | 5–95% |
|---|---:|---|
| Rb | **90 ppm** | 80–110 |
| Zr | **70 ppm** | 60–90 |
| Rb/Zr | **1.33** | 1.12–1.57 |

The reference sources, sorted by Rb — the **lowest** Anatolian value is Kars-Digor
at 110 ppm; the main candidates (Göllü Dağ, Nenezi, Acıgöl, Bingöl, Meydan) run
**155–270 ppm**:

| Source | Rb | Zr |
|---|---:|---:|
| Kars-Digor | 110 | 172 |
| Hasan Dağ | 133 | 43 |
| Sarıkamış | 131 | 93 |
| Nenezi Dağ (Milic, pXRF) | 155 | 137 |
| Göllü Dağ (Milic, pXRF) | 178 | 75 |
| Acıgöl | 270 | 65 |
| Bingöl A | 243 | 1354 |
| Nemrut Dağ A | 205 | 1229 |

Only two sources in the whole database fall inside our Rb **and** Zr range —
**Melos Adamas** and **Giali**, both **Aegean**, and both with Zr above our range.
Aegean obsidian in the Levantine Neolithic would be an extraordinary claim.

The likeliest explanation is far more ordinary: **our instrument reads low.**

---

## Testing the calibration-offset hypothesis

If a single calibration offset explains it, then for the true source the factor
needed to scale our Rb onto it should equal the factor for Zr. Testing all 32
sources:

| Source | ref Rb | ref Zr | factor needed (Rb) | factor needed (Zr) | agree? |
|---|---:|---:|---:|---:|---|
| Acıgöl2 | 173 | 139 | 0.52 | 0.50 | ✅ |
| Nenezi Dağ (F&H) | 169 | 125 | 0.53 | 0.56 | ✅ |
| Carpathian 2 | 174 | 127 | 0.52 | 0.55 | ✅ |
| Sarıkamış | 131 | 93 | 0.69 | 0.75 | ✅ |
| Giali | 122 | 96 | 0.74 | 0.73 | ✅ |
| Göllü Dağ (Milic) | 178 | 75 | 0.51 | 0.93 | ❌ |
| Hasan Dağ | 133 | 43 | 0.67 | 1.64 | ❌ |
| Bingöl A | 243 | 1354 | 0.37 | 0.05 | ❌ |

**Five sources survive** with consistent factors, implying our instrument reads
roughly **50–75% of true concentration**. That is entirely plausible for a
factory "Mining" calibration applied to rhyolitic glass — those modes are built
for soils and ores, not obsidian, and trace-element errors of this size are
normal and well documented.

**But we cannot confirm it**, because the offset is exactly what we lack the
means to measure.

---

## Why we cannot simply use ratios instead

Ratios survive a *uniform* offset, and this was our plan (§D2 of the cleaning
plan). Two problems:

1. **The offset is not uniform.** The surviving factors range 0.50–0.75, and for
   most sources the Rb and Zr factors disagree badly. If the offset differs
   between elements, the ratio shifts too.
2. **The ratio does not identify a unique source anyway.** Our Rb/Zr of 1.33
   matches **6 of 32 sources** within ±15%: Acıgöl2, Nenezi Dağ (both papers),
   Sarıkamış, Carpathian 2, Giali. A ratio alone cannot choose among them.

---

## We searched for a standard. There is none.

The one thing that would resolve this is a **certified reference material**
measured on the same instrument. We searched every raw workbook for any label
mentioning a standard, RGM, NIST, SRM, QC, or control.

**Nothing.** The only non-sample readings are 14 `System Check` entries, which are
the instrument testing *itself* in counts-per-second against its internal target.
They contain no concentrations and cannot calibrate anything.

---

## ✅ Update 2026-07-21 — what the data CAN still do

Testing the ratio question produced a positive result that survives the
calibration gap entirely.

**Two objects from Yiftahel have Zr 10–15× the assemblage median** (1005 and
640 ppm vs 65), with Nb and Fe elevated in step — the **peralkaline** signature
of Bingöl A or Nemrut Dağ. The stronger object was measured on both faces and the
two readings agree within 3%.

**A calibration offset scales everything together; it cannot create a fifteen-fold
difference.** So this second-source identification is valid despite everything
below.

This bounds the problem usefully: our data **cannot** make fine distinctions, but
it **can** detect a grossly different source. The instrument is not
uninformative — only imprecise.

⚠️ Reading 1703 (the weaker outlier) has locus recorded as **"Modern"** and no
basket. Its archaeological context must be verified before use.

### And a caution about the reference data itself

While matching ratios we found the published fingerprints are less firm than
assumed: **Nenezi Dağ** is reported at Rb/Zr **1.35** (Frahm & Hauck) and **1.13**
(Milic) — a 19% disagreement for one volcano, comparable to our own uncertainty.
"Göllü Dağ" spans **1.55–3.46** across its sub-sources. Between-laboratory
variation in the reference literature is of the same order as the effect we are
trying to measure, which independently limits how finely anyone can attribute.

---

## What our data still supports

Not everything is lost. **Internal comparison does not need cross-instrument
calibration**, because every sample was measured on the same machine under the
same settings.

Comparing the three sites on Rb/Zr:

| Site | n | median | sd | 5–95% |
|---|---:|---:|---:|---|
| Motza | 934 | 1.33 | 0.14 | 1.12–1.57 |
| Einan | 225 | 1.33 | 0.14 | 1.11–1.57 |
| Yiftahel | 50 | 1.33 | 0.16 | 1.12–1.50 |

The three sites are **chemically indistinguishable** — identical medians, spreads
and percentiles, across roughly a thousand years of occupation.

⚠️ **But read that carefully.** The spread (sd 0.14) is about **one quantization
step**, so the apparent variation may be nothing but rounding noise. The honest
statement is: *we find no evidence of more than one source, and we lack the
resolution to rule one out.* It is **not** proof of a single source.

---

## What would fix this

In order of value:

1. **Measure RGM-2 on the same pXRF, with the same settings.** RGM-2 is a USGS
   rhyolite-glass standard — obsidian, matrix-matched, and the standard used
   throughout this literature. A single short session gives the calibration
   factor for Rb, Zr and Nb, and would let us place our samples on the published
   scale. **This is the single highest-value action available to the project.**
2. If the instrument is gone or inaccessible, **measure a few obsidian pieces of
   independently known source** on whatever instrument is available.
3. **Anchor a subset by laboratory analysis** (ICP-MS or NAA) — the most
   accurate, and the most expensive.

Options 1 and 2 are cheap. Without one of them, the project can characterise and
group the assemblage, but **cannot honestly name the volcano**.

---

## A second, separate constraint

Our standing rule is **pXRF-to-pXRF**. Of the reference database:

| Method | rows | sources |
|---|---:|---:|
| pXRF | 52 | 8 |
| multi (see paper) | 230 | 17 |
| EDXRF | 44 | 11 |

Only **Milic 2014** is true pXRF, and its Anatolian coverage is just **Göllü Dağ
and Nenezi Dağ** — the rest are Aegean and Carpathian. So a strict pXRF-to-pXRF
comparison has only two relevant Anatolian sources to work with. This is a
separate problem from the calibration gap and also needs a decision.

---

## Recommendation

**Do not proceed to source attribution yet.** Cleaning the samples (Step 5) is
still worth doing — it is needed regardless, and none of it is wasted. But the
attribution step should wait until either a standard is measured, or we
consciously accept a much weaker claim:

> *"The obsidian from all three sites is chemically homogeneous at the resolution
> available to us, consistent with a single dominant source, which we cannot
> identify from these measurements alone."*

That is a defensible statement. "These tools came from Göllü Dağ" is not — not
with the data as it stands.

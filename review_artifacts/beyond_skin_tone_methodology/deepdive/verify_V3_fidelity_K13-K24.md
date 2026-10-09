# V3 verification, text-fidelity lens: K13–K24 and S-h to S-m

**Stance.** I tried to refute each issue. Every quote was checked against `run/manuscript.txt`, including the supplement and captions. I re-transcribed Table 3 from `render/pg_p6.png`; it matches the text extraction exactly, including the bold on ArcFace Red 95.36. I re-transcribed Table 4 and the Fig. 4 and Fig. S3 values from the text and from `pg_p7.png` and `pg_p13.png`.

All arithmetic was re-derived independently. The scripts are in `deepdive/verify_scripts/`:

| Script | What it does |
|---|---|
| `t3_exact_permodel.py` | Searches each model separately, with free N ≤ 2000 and free cell sizes. Supports rounding or truncation, with or without the swap. |
| `t3_minviol_tests.py` | Joint search at N = 1000 for the minimum number of violated cells; Fisher, Wilson and MDE calculations. |
| `t3_chance_fit.py` | Null calibration: how often a random row fits a partition exactly. |
| `t4_share.py` | Interval-arithmetic check that the class share is constant across Table 4 columns. |
| `t12_gen.py` | Tests Tables 1–2 against each other and checks the Table 1(b) margins. |

## Summary

| ID | Verdict | Severity (proposed → mine) | One-line reason |
|---|---|---|---|
| K13 | CONFIRMED (one number corrected) | Major / poss. Critical → **Major** | Invalidates the face-verification half of claim (iii); the cropping half is untouched. Non-significance is robust even without the reconstruction. |
| K14 | CONFIRMED (one nuance) | Major → **Major** | No denominator, unit or rounding scheme reproduces ArcFace's printed row. The swap cuts the residuals from about 0.29 pp to ≤ 0.006 pp and falsifies the caption's "all models". |
| K15 | CONFIRMED (grayscale point reframed) | Major → **Major** | The estimand is undefined (pair rule, mixed FMR/FNMR), and the input regime is unreported. Needs a redesign, not just more data. |
| K16 | CONFIRMED (one sub-point is inferred) | Major / poss. Critical → **Major** | Specificity is unidentified, not shown false. The finding survives as "effect of these latent edits"; the causal-skin wording does not. |
| K17 | CONFIRMED | Major → **Major (low end)** | The orthogonality claim and the contrast with "pale" are contradicted. The L\* leakage is too small to explain the hue→smile effect. |
| K18 | CONFIRMED (alternative noted) | Minor → **Minor** | Three cells are inconsistent; for FairFace a second explanation is arithmetically equivalent. No headline claim depends on them. |
| K19 | PARTLY CONFIRMED | Minor → **Minor** | "Half true" is right. The "masks differ" argument is weak; the real gap is that the mask and resolution for generated images are unreported. |
| K20 | CONFIRMED (one nuance) | Minor → **Minor** | The segmenter is named for CFD only; every other listed item is absent. |
| K21 | CONFIRMED | Minor → **Minor** | The method is in A.2 only, and the main-text pointer goes to Fig. S3. |
| K22 | PARTLY CONFIRMED | "Major writing / Minor method" → **Minor** | There is no consolidated limitations section, but there is real ethical content (§2 social impact, the §4.3 gender statement, A.1). |
| K23 | CONFIRMED | Minor → **Minor** | All five quoted phrases were found; the evidence base is as described, except that smile uses 2 classifiers, not 4. |
| K24 | CONFIRMED (one premise unnecessary) | Minor → **Minor** | All three slips are verified; four more trivial slips were found. |

| Strength | Verdict |
|---|---|
| S-h (contrast confound examined) | PARTLY CONFIRMED |
| S-i (F/M, S/NS split) | CONFIRMED |
| S-j (CFD consented, controlled capture) | CONFIRMED |
| S-k (ethical framing of gender classification) | CONFIRMED (with a wording caveat) |
| S-l (candid reconstruction limitation) | CONFIRMED (scope caveat) |
| S-m (histograms beyond binary cuts) | CONFIRMED (limited) |

---

## K13. Face verification: no counts, CIs or tests

**Text check.** §4.2.2 (ll. 552–561, 562–567, 631–640) and the Table 3 caption (ll. 546–549) give no subgroup n, intervals or tests. The caption also leaves "L+R/L+Y/D+R/D+Y" and the bold font undefined.

The paper never claims significance for Table 3. What it does claim is "better identified by all face verification models", "affected by skin tone differences", and "more robust … but as prone to skin hue differences as Dlib". These read noise-level gaps as substantive.

**Reconstruction, re-derived from scratch.**

- The tone split is unique: nL = 715 is the only value consistent with Light, Dark and Overall for all three models at N = 1000.
- The hue split is unique: nR = 548 is the only value consistent for FaceNet and Dlib.
- With nL fixed at 715, a scan of all (nLR, nDR) gives exactly one tuple with ≤ 4 total violated cells: (387, 328, 161, 124), with 3 violations (ArcFace R, ArcFace Y, FaceNet LY).
- Strongest anchor: Dlib's 9 values alone, with no cross-model constraint and any N ≤ 1000, admit exactly one exact partition, which is that tuple.
  - Null calibration: 0/400 randomly jittered rows admit any exact fit.
  - Solver check: it recovered 25/25 synthetic consistent rows.

**Tests** (Fisher exact, Wilson CIs):

| Contrast | Gap | p |
|---|---|---|
| ArcFace L vs D | +1.14 pp | 0.51 |
| FaceNet L vs D | +0.51 pp | 0.76 |
| Dlib L vs D | +0.72 pp | 0.66 |
| ArcFace R vs Y (swap-corrected) | −0.28 pp | 0.88 |
| FaceNet R vs Y | +1.09 pp | 0.49 |
| Dlib R vs Y | +1.12 pp | 0.50 |

- Across all 24 contrasts (2 marginal + 6 intersectional pairwise, × 3 models), the minimum p is 0.086 (ArcFace LR vs DR), and the next is 0.19.
- MDE at 80% power: 4.47 pp for tone and 4.06 pp for hue.

**Correction to the canonical text.** "Every Fisher p is at least 0.19 for the marginal contrasts" is wrong. The marginal p-values are all **≥ 0.49**; 0.19 is the second-smallest *intersectional* p. "At least 0.09 across all contrasts" is correct (0.086).

**Robustness.** The conclusion does not depend on the reconstruction. Even the most favourable 500/500 split gives z ≈ 0.8 for the largest marginal gap (1.13 pp).

**Severity: Major.** "Critical" would require invalidating a core claim on its own. K13 removes the face-verification support for claim (iii), but the cropping evidence for (iii) stands (subject to K11/K12).

## K14. ArcFace Red/Yellow columns swapped

**Confirmed facts.**

- At n = 548, the attainable Red values are 95.26 and 95.44, so the printed **95.36 is unattainable**.
- At n = 452, the attainable Yellow values are 94.91 and 95.13, so the printed **Yellow 95.07 is also unattainable**. Without the swap, both hue cells fail.
- ArcFace's four intersectional cells (372/387, 311/328, 149/161, 120/124) reproduce Light, Dark and Overall exactly. They imply Red 521/548 = 95.073 and Yellow 431/452 = 95.354.

**Alternatives tested and rejected.**

1. **Model-specific denominators** (face-detection failures, or a different N per model). With free cell sizes and N ≤ 2000, ArcFace's printed row has **no** exact solution under rounding, and none under truncation. No choice of denominators rescues the printed direction.
2. **Per-image units** (N = 2000). There is no unswapped solution. With the swap there is one exact solution, (773, 657, 322, 248). It differs from Dlib's doubled tuple (774, 656, 322, 248) by a single image, so it is consistent with the swap rather than against it.
3. **Truncation instead of rounding.** No model fits under truncation. Dlib fits rounding exactly, so the rounding convention is established.
4. **Different pair-assignment rules for the marginal and intersectional groupings** (non-partitioning cells). Arithmetic alone cannot exclude this. It is implausible, though, because Dlib's 9 values and all three models' tone margins fit one partition exactly and uniquely, and skin labels do not depend on the model.

**Nuance to add.** The swap is not perfectly exact. Printed Red 95.36 vs the derived Yellow 95.354 leaves a 0.006 residual. That needs a second 0.01-level slip, of the same type as FaceNet's LY, where 93.293 is printed as 93.30; both are rounded up. The wording should be "near-exact (residual ≤ 0.006 pp vs ≈ 0.29 pp unswapped); most parsimonious explanation, inferred and not directly observable".

**FaceNet LY.** 93.30 is unattainable at n = 328. The value 93.29 is forced: DY = 118/124 is the only fit for 95.16, and Yellow 424/452 fixes LY at 306.

**Consequence.** As printed, the caption ("red skin hue … better identified by all face verification models") and l. 564 ("All models tend to prefer … red skin hues") are false for ArcFace. The bold font on 95.36 is mis-assigned.

**Severity: Major.** It falsifies a stated universal claim and signals table-integrity problems; there are 4+ transcription anomalies across Tables 1b, 3 and 4a. Its *inferential* impact is subsumed by K13. If the editor merges the two, K14 becomes an erratum within K13.

## K15. Face-verification design

- **Pair-assignment rule.** Absent from the text (ll. 552–567). The reconstruction shows pair-level units, one cell per pair, with N = 1000, so some undisclosed rule exists. Confirmed.
- **Accuracy only.** Only accuracy is reported. There is no FMR/FNMR split, no threshold, and no genuine/impostor mix per cell. DeepFace's default per-model thresholds are implied but not stated. Confirmed.
- **scikit-learn loader.** The defaults were verified locally with the `fetch_lfw_pairs` signature (sklearn 1.9.1): `funneled=True, resize=0.5, color=False, slice_=(70:195, 78:172)`, giving 62×47. The `test` subset is the 1,000-pair dev-test split, which matches the paper's "1,000 test pairs (500 positives and 500 negatives)".
  - **Correction:** "skin colour cannot be computed from grayscale" should not read as an accusation. The authors *must* have set `color=True` (otherwise h\* is undefined).
  - The real issues are three: unreported settings; a probably low-resolution, tight crop if `resize` and `slice_` were left at their defaults; and the skin-mask source for LFW, which is never stated.
  - ArcFace at 95.20% is well below its published LFW accuracy of about 99.8%. That is consistent with a degraded input regime, though this is an inference.

**Severity: Major.** Even with adequate n, the estimand is undefined, so a redesign is needed. Its incremental impact beyond K13 is on the paper's *method*, not on the already-unsupported verification claim.

## K16. Causal edits not shown to be skin-specific

**Text.** §4.3 (ll. 666–677) describes unconditioned InterFaceGAN SVM directions. There is no mention of conditional manipulation, of projecting out the gender or smile boundaries, of identity or attribute-preservation checks, or of re-labelling after edits. The CelebA ground-truth labels are reused for the edited images (ll. 706–709, 739–742).

**Sub-point corrections.**

- "Whole-image classifier" is an **inference**. The paper says only "train a classifier on CelebAMask-HQ to predict the skin tone … and skin hue". The input is never specified, although classifying 500,000 unmasked StyleGAN3 samples makes image-level input likely.
- "Threshold labels" is implied by the binary light/dark and red/yellow categories, but the paper never states it.

**What the paper does address** (to credit it): the reconstruction baseline (ll. 743–753), the "pale" contrast (ll. 732–738), and the RMS contrast check (A.2). None of these addresses semantic entanglement of the edit directions.

The Table 4 pattern fits both readings equally well:

- +light: F↑ and M↓ in all four models.
- +dark: M↑.
- +red and +light: NS↓.

**Severity: Major, not Critical.** The design identifies "the effect of these latent edits". It does not identify "the causal effect of skin colour". Re-scoping the claim, or running conditional directions with a preservation check, would fix it. Nothing shows the findings are *false*.

## K17. "Orthogonal" edits contradicted by Fig. 4

All Fig. 4 values were checked against `pg_p7.png`. Deltas are relative to the reconstruction, with faces listed 1, 2, 3:

| Edit | ΔL\* | Δh\* |
|---|---|---|
| +light | +9.82, +14.30, +5.28 | −1.00, −1.37, −0.08 |
| +dark | −13.72, −20.65, −9.75 | −0.07, +3.52, +0.88 |
| +red | +2.17, **+7.62**, −0.81 | −10.00, −12.87, −13.80 |
| +yellow | −0.42, +2.27, **+3.77** | +8.51, +6.94, +10.36 |
| +pale | +7.64, +16.05, +8.45 | +1.11, +7.36, +3.51 |
| −pale | −7.01, −16.88, −10.75 | −3.22, −8.60, −4.26 |

- Both canonical numbers are confirmed: +7.62 and +3.77.
- An added point: on face 1, "pale"'s off-target Δh\* (+1.11 / −3.22) is *smaller* than the +red edit's off-target ΔL\* on face 2. Fig. 4 therefore does not support the "ours vs pale" distinction claimed in ll. 731–738 and in the caption.
- Only 3 faces are shown. There is no dataset-level ΔL\*/Δh\* for the 4 × 30,000 edits; A.2 reports only RMS contrast, and only for the tone edits. No edit strength is reported, and there is no dose–response. The checks use the same estimator that defined the labels. All confirmed.

**Mitigating point (my own).** L\* leakage cannot explain the hue→smile effect. The mean off-target ΔL\* of +red (+2.99) is about 0.31× the mean ΔL\* of +light (+9.80). Scaling the +light non-smiling (NS) effect linearly therefore predicts only about −1.4 pp for Azure (observed −11.08) and about −0.6 pp for AWS (observed −7.28).

**Severity: Major, at the low end.** What is weakened is the paper's "independent control over L\* and h\*" justification for claim (iv). The direction of the Table 4 hue findings is not weakened. It would be Minor if a dataset-level manipulation check showed small mean off-target shifts.

## K18. Table 4 inference and inconsistent cells

**Text.** There are no tests or CIs. The quote "redder or darker in male sample results in a increase in accuracy for all models" (ll. 765–767) is verbatim. The +red male deltas are AWS +0.06, Azure +0.21, Clarifai +0.58 and FairFace +0.19 pp; AWS's gain is about 7 of roughly 11,070 male images.

A further over-reading: "while it stays the same for smiling individuals" (Azure, +red), yet S accuracy rises from 97.29 to 99.00 (+1.71 pp).

**Share check** (interval arithmetic, ±0.005 per printed value):

- Every gender cell implies a female share in **[0.6311, 0.6318]**, except three:
  - AWS +dark: 0.487 [0.477, 0.495].
  - FairFace +red: 0.603 [0.601, 0.604].
  - FairFace +yellow: 0.660 [0.659, 0.662].
- Table 4b is fully consistent, with a smiling share in [0.4699, 0.4705].

**AWS +dark.** The implied All is 98.43, against 98.27 printed. Alternatively M would have to be 97.29, or F 98.58. Which value is wrong cannot be determined.

**FairFace +red/+yellow.** The implied All values are 97.15–97.16 and 96.97, against 96.97 and 97.16 printed. That is consistent with the two All values being swapped.

- **Alternative not in the canonical text.** Swapping the F/M *pairs* between the two columns fits the arithmetic identically. Under that reading, FairFace +red M = 92.77 < 92.91, so the "male accuracy increases for all models" claim would fail for FairFace.
- The cross-model pattern (+red M↑ and +yellow M↓ in the other three models) favours the All-swap, but this cannot be proven.

**Detection-failure explanation rejected.** It would need about 11% of one class to drop out in opposite directions in adjacent columns (and about 45% for AWS +dark).

**Severity: Minor.** No headline claim depends on these cells.

## K19. Generative-model comparison

**Re-derived** (two-proportion z, generated n = 10,000 vs FFHQ n = 70,000):

| Comparison | Gap | p |
|---|---|---|
| P2 dark | +0.96 pp | 0.058 |
| P2 red | +1.49 pp | 2.8e-4 |
| P2 4-cell GOF | — | 2.4e-4 |
| StyleGAN3 4-cell GOF | — | 0.86 (all margins ≤ 0.25 pp) |

"P2 slightly amplifying the bias" (ll. 428–430) is therefore half true:

- P2 amplifies red.
- P2 slightly *reduces* the light share (borderline).
- On the paper's own light-red / dark-yellow framing, the cells move in the "amplifying" direction (LR +0.47, DY −0.06) but are not significant (p = 0.38 and 0.79).

**Mask point.**

- The canonical contradicts itself here. If FFHQ-Ageing masks are DeepLabV3 predictions ("as done in FFHQ-Ageing", ll. 491–492), and the generated images were presumably masked with the same DeepLabV3, then the pipelines may well be *like for like*.
- What is confirmed: the paper calls the FFHQ-Ageing masks "ground truth" (ll. 367–369), contradicting its own l. 492.
- The mask source and output resolution of the generated images are unreported. P2's FFHQ model is 256 px to my knowledge (external, unverified here).
- Sampling settings and seeds are unreported.

**Severity: Minor.**

## K20. Reproducibility gaps

All listed items are absent from the text: edit strengths; generation seeds, ψ and steps; LFW loader arguments; API versions and dates ("latest available version", l. 702); cropper release ("Twitter"); Elo game order; and the LFW, generated and edited-image mask sources.

**Nuance.** The segmentation model *is* named for CFD: DeepLabV3 trained on CelebAMask-HQ (ll. 491–492). A code URL is given (l. 357), which partly mitigates.

**Severity: Minor.**

## K21. Structure

- The main text never describes extraction (segmentation, K-means, top-3, mode) and never cites §A.2. The only pointer, ll. 332–334, sends the reader to "Figure S3" (relighting) for "the details of the methodology".
- Secs. 2–3 (ll. 126–326) are almost all background, about 1.5–2 pages.
- The abstract (ll. 11–26) has no method and only a generic finding ("reveals additional biases").
- Terminology drift is confirmed: score / scale / measure; FFHQ vs FFHQ-Ageing; race vs ethnic labels; the symbol *a* is overloaded.

**Severity: Minor**, against the claim-based bands. It would be weighted higher as a writing issue.

## K22. Limitations and responsible use

**Confirmed absences.** There is no limitations section and nothing in the Conclusion (ll. 783–806). There is no race-proxy discussion; A.3 presents ethnic separability as a *benefit* (ll. 1345–1358). Dual use of the edit directions is not discussed. Neither is consent or licensing for sending CelebAMask-HQ images ("non-commercial research agreement", l. 365; "crawled from social media", l. 371) to AWS, Azure and Clarifai. The vocabulary concerns are real: "Asian subjects … mostly in the yellow side" (l. 1342), "more feminine" (ll. 355, 694), and "transgendered" (l. 717).

**Partly refuted.** The paper does contain ethical content:

- the §2 "Social impact of skin color scales" paragraph, on the harm of using skin type as a race descriptor (ll. 194–210);
- the gender-classification disclaimer (ll. 715–720);
- the reconstruction caveat (ll. 743–753);
- A.1 on confounding factors.

**Severity: Minor**, since no core claim changes. An ethics reviewer may weigh it more.

## K23. Over-generalisation

All quotes were verified:

- "any camera" (l. 1172);
- "any face pose" (ll. 330–331, 1183);
- "datasets and models" (abstract, l. 24);
- "previously invisible" (ll. 124, 792, 1358);
- "from data collection to model deployment" (ll. 805–806).

The evidence base is as stated, with one correction: smile uses **2** classifiers (AWS and Azure); only gender uses 4.

**Severity: Minor.**

## K24. Minor numeric slips

**Table 1(b).** 52.82 + 29.06 = 81.88, while 81.87 is printed. The red and yellow shares are complementary, so 81.87 + 18.12 = 99.99 cannot be two correctly rounded values.

- **Correction:** the canonical premise "cells are exact at N = 70,000" is unnecessary and unproven, since each cell admits about 7 integer counts. The slip follows from the cell sums plus complementarity alone.
- Strictly, either 81.87 or 18.12 is off by 0.01. The printed cell sums favour 81.88.

**Fig. S3.** Checked on `pg_p13.png`: the original is the panel without a sphere, L\* = 66.63. The minimum relit value is 59.41, a deviation of −7.22, which crosses 60. "Up to 6 points" is wrong.

**FaceNet LY.** Confirmed, see K14.

**Additional slips:**

- ArcFace's swapped value carries a 0.006 rounding residual.
- "Alahuf" (l. 666) vs "Alaluf" (l. 808).
- "verify the identify" (l. 567).
- "a increase" (l. 766).
- The Fig. S2 caption is truncated at "to get the f" (l. 1171).

**Severity: Minor.**

## Strengths

- **S-h, contrast examined: PARTLY CONFIRMED.** RMS contrast is reported (0.644 / 0.630 / 0.652; ll. 1296–1310). The paper concedes "Manipulating images has an effect on the overall contrast". However:
  - contrast is reported only for the tone edits;
  - Fig. S4 shows a single face;
  - there is no adjustment.

  This is engagement with the confound, not a resolution of it.
- **S-i: CONFIRMED.** Table 4 reports F/M/All and S/NS/All.
- **S-j: CONFIRMED.** "acquired in a controlled setting" and "informed consent" (ll. 484–490); this covers CFD and CFD-India. The caveat is that this capture regime differs from in-the-wild data (K05).
- **S-k: CONFIRMED.** "we do not condone the gender classification task …" (ll. 715–720). Caveats: "transgendered" and the "more feminine" framing elsewhere.
- **S-l: CONFIRMED.** ll. 743–753. It covers reconstruction artefacts, not the side effects of edit directions.
- **S-m: CONFIRMED (limited).** The Fig. S6 20-bin stacked histograms were checked on `pg_p14.png`. They are marginal histograms and still have no reference distribution (K05).

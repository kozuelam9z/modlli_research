# Local empirical and arithmetic checks (outside the sprint contract)

Run date: 2026-10-08. All scripts are in the session scratchpad (`scripts/`). These checks are **not** part of the contract panel's evidence and were not shown to the two contract seats.

---

## 1. Table 3 (LFW face verification): reconstructing the subgroup sizes

**Method.** Exact rational reachability (`lfw_reach.py`, `lfw_reconstruct.py`). The question is: for which subgroup sizes is every reported 2-decimal accuracy an attainable k/n, for all three models at once, given that the subgroups partition the 1,000 test pairs and their correct counts add up to the Overall column (952 / 944 / 942)?

**Result.** Only one cell configuration is consistent:

| Cell | n (pairs) |
|---|---|
| LR | 387 |
| LY | 328 |
| DR | 161 |
| DY | 124 |
| Light | 715 |
| Dark | 285 |
| Red | 548 |
| Yellow | 452 |

The tone split is unique: 715/285 at N=1000, or 1430/570 if images rather than pairs are counted. No red/yellow split of 1,000 (or 2,000) units reproduces the printed hue columns.

With these cell sizes, every printed value checks out except the following:

- **ArcFace Red and Yellow appear swapped.** The reconstructed counts are 521/548 = 95.07 for red and 431/452 = 95.35 for yellow. The table prints Red 95.36 (in bold) and Yellow 95.07. With n=548, a red accuracy of 95.36 cannot be reached at all: the nearest attainable values are 95.26 and 95.44. Once the swap is corrected, ArcFace is *more* accurate on yellow, which contradicts the caption "Individuals with ... a red skin hue are better identified by all face verification models".
- **FaceNet L+Y prints 93.30.** This cannot be reached with n=328: 306/328 = 93.29. The Yellow margin, 93.81 = 424/452, requires 306, so 93.29 is the true value. This is a minor rounding error.

**Significance with the reconstructed counts** (Fisher exact, Wilson 95% CI):

| Model | Light vs Dark | Red vs Yellow | Largest intersectional gap |
|---|---|---|---|
| ArcFace | +1.14 pp, p = 0.51 | −0.28 pp, p = 0.88 | DY vs DR, p = 0.19 |
| FaceNet | +0.51 pp, p = 0.76 | +1.09 pp, p = 0.49 | p = 0.29 |
| Dlib | +0.72 pp, p = 0.66 | +1.12 pp, p = 0.50 | p = 0.38 |

Every CI overlaps heavily (for example, ArcFace light is 93.8–96.8 and dark is 91.1–96.5). No Table 3 difference is distinguishable from sampling noise.

## 2. MST-E replication of the extraction pipeline

**Data.** MST-E, the local copy of 19 subjects photographed the same day on the same Pixel camera under well-lit and poorly-lit conditions. Of 1,489 JPGs, Apple Vision detected a face in 1,364. Of those, 1,304 had no face mask and were analysed; 732 are well-lit.

**Pipeline.** A faithful re-implementation of the authors' released `extract/predict.py`:

- Gaussian blur with σ=1.
- sRGB to CIELAB (D65, 2°). Validated against `colour-science`; maximum error is 0.02.
- Hue computed as `arctan(b/(a+1e-8))`.
- KMeans with 5 clusters and seed 2021, on raw [L, hue].
- Per-cluster Sturges histogram mode, taken as the left bin edge.
- Pixel-weighted mean of the top-3 clusters by L.

**Skin mask.** Approximated from Apple Vision landmarks: the face hull minus the eyes, brows and lips, then eroded. A cheek-only variant was used for sensitivity. **Caveat:** these masks are not the authors' DeepLabV3/CelebAMask-HQ masks. The two mask variants agree closely (r = 0.98 for L\*, 0.92 for h\*; 95.1% agreement on the 4-cell category).

### 2.1 Reliability: same person, same session

ICC(1,1) is one-way random with subjects as targets. The within SD is the pooled within-subject SD.

| Score | All images: ICC [95% cluster-bootstrap CI] | All images: within SD | All images: between SD of subject means | Well-lit only: ICC | Well-lit: within SD | Well-lit: between SD |
|---|---|---|---|---|---|---|
| L\* (paper estimator, full mask) | 0.13 [0.05, 0.21] | 18.1 | 7.2 | 0.50 | 8.7 | 8.7 |
| h\* (paper estimator, full mask) | 0.29 [0.17, 0.40] | 12.2° | 8.0° | 0.46 | 11.8° | 10.9° |
| h\* (paper estimator, cheeks) | 0.19 | 13.8° | 6.9° | 0.30 | 14.9° | 9.8° |
| h\* (pixel-mean hue, cheeks) | 0.17 | 8.9° | 4.2° | 0.28 | 8.0° | 5.1° |

- **Variance share.** 86% of the variance in L\* and 72% of the variance in h\* lies *within* subjects, not between them.
- **Well-lit images.** 25.7% of well-lit images fall more than 10° from their own subject's median h\*.

### 2.2 The robustness claim for h\*

Moving from well-lit to poorly-lit images, L\* drops by an average of 29.4 points (SD 7.4). The hue angle h\* shifts by +1.9° on average (p = 0.49), but the per-person shift ranges from −18.5° to +32.0° (SD 11.6°). Real lighting changes therefore move h\* by person-specific, unpredictable amounts.

For the golden vs. "not ideal" image pair of each subject (n = 15 pairs scored), |Δh\*| averages 16.3° and reaches 70.8°. Six of the 15 subjects change their 4-cell (tone × hue) category between the two photos.

### 2.3 The estimator is not invariant across skin tone

In well-lit images, the within-subject SD of the paper's h\* rises with darker oracle MST:

| Oracle MST | Within-subject SD of h\* |
|---|---|
| MST 1–3 | 6.6° |
| MST 4–6 | 8.2° |
| MST 7–10 | 16.2° |

Across subjects, Spearman ρ = 0.69 (p = 0.001).

Relative to the plain pixel-mean hue, the top-3-brightest-cluster mode estimator shifts darker subjects toward "red" by about 14° (MST 7–10), compared with about 1° for MST 1–3. The trend is ρ = −0.40 (p = 0.09) and is driven mostly by two MST 9–10 subjects, whose specular highlights fall in the brightest clusters.

Hue values below 0° occur in 51 of 1,304 images. They concentrate in MST 8–10 subjects, and the definition in Eq. (2) does not allow them.

### 2.4 Association with MST (oracle, subject level, n = 19, well-lit, cheeks)

| Score | Spearman ρ with oracle MST |
|---|---|
| L\* | −0.76 (p < 0.001) |
| h\* (paper estimator) | −0.43 (p = 0.06) |
| h\* (pixel-mean hue) | 0.03 (p = 0.90) |

The apparent "darker → redder" association therefore comes from the estimator, not from the pixels. This runs opposite to the paper's own CFD observation that Black subjects are "darker and more yellow".

### 2.5 Thresholds do not transfer across capture pipelines

On MST-E photos, only 21/1304 = 1.6% of images reach h\* ≥ 55°. Every subject's mean hue is below 55°, so nearly everyone is classed "red". On CFD the paper reports 533/739 = 72% "yellow"; on CelebAMask-HQ, 34% yellow; on FFHQ, 18%.

The official MST reference swatches themselves measure h\* = 47–79°, non-monotonic across the scale:

| Swatch | MST1 | MST2 | MST3 | MST4 | MST5 | MST6 | MST7 | MST8 | MST9 | MST10 |
|---|---|---|---|---|---|---|---|---|---|---|
| h\* | 58.1 | 67.0 | 78.6 | 74.0 | 74.0 | 67.6 | 53.9 | 47.3 | 52.9 | 64.6 |

At MST10, the swatch's chroma is only 5.8, so one unit of a\* moves h\* by about 9°. Compare about 2–3° per unit for MST3–7. Script: `scripts/mst_swatches.py`.

A fixed 55° cut therefore measures where a camera, rendering and estimator pipeline sits relative to 55°, as much as it measures people.

## 3. Arithmetic notes on the text

- **Fig. S3.** The original image is L\* = 66.63. The relit versions span 59.41–71.34, a deviation of −7.22 / +4.71. This contradicts "varies by up to 6 points w.r.t. the original image".
- **Table 1(b) FFHQ.** The cells are exact at N = 70,000 (36,974 + 20,342 + 9,408 + 3,276 = 70,000). The Red row total is therefore 57,316 / 70,000 = 81.88%, not the printed 81.87%, and the printed margins sum to 99.99. Trivial.
- **Fig. 3 group sizes.** These are internally consistent: 334 + 127 = 461 light; 199 + 79 = 278 dark; 127 + 79 = 206 red; 334 + 199 = 533 yellow. The red group is 61.7% light and the yellow group 62.7% light, so the marginal hue effect is not driven by dichotomised tone composition.
- **Elo conversions.** 60.73% corresponds to a mean rating gap of about 75.7 Elo points; 58.25% to about 57.9 points (M = 400).

## 4. Verified facts about the methods the paper relies on

- **DPR relighting (Zhou et al. 2019; Fig. S3 source).** The public demo converts to Lab, feeds only the L channel to the network, and writes the output back into L, leaving a and b unchanged. Under this procedure, h\* is invariant by construction, up to 8-bit and gamut-clipping effects. Fig. S3 therefore cannot provide evidence that h\* is robust to illumination.
- **Authors' released code.** Hue uses `arctan`, not `arctan2`, and the histogram mode is the left bin edge. KMeans clusters raw, unstandardised [L, hue].
- **Cropping benchmark code** (`cropping/generate.py` and `predict_twitter.py`, read 2026-10-08):
  - **Pairing.** Pairs come from `it.combinations(product(ethnicities, genders), 2)`, with `top = combinations[i][0]` and `bottom = combinations[i][1]`. Top/bottom position is never randomised or swapped; `np.random.shuffle` only shuffles which image files fill a pair. The group order is fixed, so position is perfectly confounded with the group contrast:
    - White faces are always on top;
    - Latino faces are always on the bottom;
    - within an ethnicity, F is always above M.
  - **Resizing.** Every source image is resized to a fixed 859×611 on a 3000×859 white canvas. Aspect ratio is kept only insofar as the source already has that ratio, whereas the paper says aspect ratio is preserved.
  - **Winner rule.** The winner is decided by `top_left_y_twitter < 887`.
  - **No Elo code.** No Elo implementation is released, so the game order is unknown.
- **LFW loader in released code** (`face-verification/lfw.py`, read 2026-10-08):
  - The loader is called with `fetch_lfw_pairs(subset='test', color=True, resize=1)`, so inputs are 125×94 RGB rather than the scikit-learn default of grayscale 62×47.
  - `DeepFace.verify(..., enforce_detection=False)` puts every pair through verification. This matches the reconstruction above, in which every model's denominator is 1,000.
  - The script runs both the cosine and the euclidean metric, and the paper does not say which one Table 3 reports.
  - The file contains no skin-colour computation and no group-assignment code, so the pair-to-group rule is defined in neither the paper nor the code.

---

## 5. Corrections after adversarial verification (V1–V4, see `deepdive/verify_*.md`)

### Reliability (§2.1)

- **Lead with the well-lit ICCs.** The fair figures are well-lit h\* 0.46 [0.30, 0.56] and well-lit frontal 0.50 [0.34, 0.58], with L\* at about 0.50.
- **All-image figures are a stress test.** The all-image values (0.13 / 0.29, "72% within") come mostly from MST-E's deliberately poor lighting. Under the paper's "apparent" construct, L\* is expected to change with lighting.
- **Not driven by two subjects.** Dropping subjects 4 and 12 *lowers* the h\* ICC.
- **Pixel-mean hue barely separates people.** In the cleanest subset its between-subject SD is only about 4.5°.

### Golden vs not-ideal pairs (§2.2)

All six category changes are **tone** flips, and nine of the fifteen pairs also change pose. Do not use these pairs as h\* evidence.

### Estimator vs pixel-mean hue (§2.3)

- **What is robust:**
  - The estimator-specific gradient in within-subject SD: ρ = 0.67 for the estimator against 0.16 for pixel-mean hue.
  - It survives atan2 and cheek-only masks.
  - It survives dropping subjects 4 and 12 (ρ = 0.55, p = 0.02).
  - Chroma mechanism at image level: ρ = −0.49 across 732 well-lit images.
- **What is not robust:**
  - The gradient is not significant in the well-lit frontal subset (ρ = 0.34, p = 0.16).
  - The "≈14° toward red" shift is driven by two subjects. The median shift for MST 7–10 is about −8°.

### Association with MST (§2.4)

Drop the between-subject r(L\*, h\*) = 0.53. It is estimator-driven and not robust (well-lit 0.42, p = 0.07).

### Swatch evidence (§2.5)

The MST swatch values are display swatches, not skin measurements, and they depend on the swatch source. Treat them as illustrative only. The robust part is that MST-E has a 1.5–1.9% "yellow" share under every estimator variant.

### arctan vs atan2

Negative h\* values are mostly quadrant IV (a\* > 0, b\* < 0), so atan2 gives the same values. The share of negative h\* in the released scores is 1.16% for CelebA, 2.85% for FFHQ and 0% for CFD. All of them land in "red".

### Released per-image scores (V2, read in memory from the authors' repo)

These scores reproduce Table 1 and the Fig. 3 group sizes exactly.

| Dataset | % yellow at 50° | at 55° | at 60° | % light at L\* 60 | at 65 |
|---|---|---|---|---|---|
| CelebA | 56.8 | 33.8 | 16.8 | 74.4 | 56.7 |
| FFHQ | 34.2 | 18.1 | 8.0 | 66.3 | 49.9 |
| CFD | 93.4 | 72.1 | 37.3 | 62.4 | 49.1 |

- **L\* and h\* are nearly uncorrelated:** |Spearman ρ(L\*, h\*)| ≤ 0.11.
- **Same population, different yellow shares:** CFD White subjects are 60% yellow, against 34% for CelebA.
- **Ethnicity and source in the cropping cells:** η²(hue | ethnicity) = 0.14. The DR cell is 56% Indian, all from CFD-India; the DY cell is 76% Black.

### Cropping position (code)

- **Marginal groups are balanced.** The share of games played on top is light 0.560 vs dark 0.561, and red 0.547 vs yellow 0.565.
- **Intersectional cells are not.** DR 0.43, DY 0.61, LR 0.62, LY 0.54.
- **Conclusion.** The fixed positions cannot explain the marginal effects, but they can distort Fig. 3c.

### K-means defaults

The released code relies on scikit-learn defaults. From scikit-learn 1.4 onward, `n_init` defaults to 1 instead of 10. With a single run, h\* and L\* change by about 7 at the 95th percentile, and 2.9% of tone labels flip. The output therefore depends on the installed version.

### CFD-INDIA

Lakshmi et al. 2021 state: "Where necessary, additional corrections were made to reach a realistic skin tone." The apparent colour of the 142 Indian faces is therefore partly an editorial decision.

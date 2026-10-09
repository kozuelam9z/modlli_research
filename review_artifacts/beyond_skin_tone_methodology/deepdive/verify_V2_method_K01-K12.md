# V2 adversarial verification: methodological-correctness lens, K01–K12 and S-a–S-g

**Paper:** Thong, Joniak and Xiang, "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color" (ICCV 2023, arXiv 2309.05148v2).

**Stance.** I tried to refute each critique on technical grounds. I judged each against the paper's stated construct: apparent colour, as a computer-vision model sees it. I also allowed for CV-conference norms.

**Severity bands.**

- Critical: on its own, it invalidates a core claim.
- Major: it materially weakens a core claim and needs substantial reanalysis or new data.
- Minor: it affects clarity or rigour only.

## 0. What I recomputed (new evidence, used throughout)

Scripts are in `scratchpad/deepdive/verify_scripts/`:

- `v2_mste_stress.py`
- `v2_rescore.py`
- `v2_golden.py`
- `v2_released_scores.py`

None of them write data files. Results were read from stdout.

1. **The authors' released per-image scores.** I read `extract/results/{CFD,CelebA,FFHQ}.csv` and `cropping/cfd_meta.csv` from the public repo into memory.
   - They reproduce Table 1 exactly. CelebA: 46.95 / 19.28 / 27.48 / 6.29. FFHQ: 52.82 / 29.06 / 13.45 / 4.68; the printed LY of 13.44 is a rounding difference.
   - They reproduce the Fig. 3 n's exactly: LR 127, LY 334, DR 79, DY 199.
   - So these files are the paper's own scores. They allow threshold sweeps, L–h association, the share of negative hue, and the ethnicity composition, all without any replication-fidelity caveat.
2. **The released code.** I read `extract/predict.py`, `cropping/generate.py` and `cropping/predict_twitter.py`, and the DPR demo (`zhhoper/DPR/testNetwork_demo_512.py`).
3. **A stress test of the local MST-E replication** (1,304 no-mask images, 19 subjects). Subsets:
   - well-lit (732);
   - well-lit and frontal or facing-camera (320);
   - without images that have negative h\*;
   - leaving out the two noisiest dark subjects (subject_4, MST 9; subject_12, MST 10);
   - jackknife.

   Estimator variants: K-means seeds 1 and 2 (n_init=10); n_init=1; atan2 hue; the hue of the aggregated (a\*, b\*) over the top-3 clusters; chroma diagnostics.

### How faithful the MST-E replication is

| Aspect | Assessment |
|---|---|
| Colour pipeline | Faithful. Images are sRGB-tagged both before and after downscaling. The conversion matches skimage. The blur is applied before masking, as in the code. |
| K-means | n_init=10 is faithful to scikit-learn versions before 1.4, whose default was 10. The seed is irrelevant at n_init=10 (see K02). |
| Resolution | 600×800 images with a face width of about 200–280 px, close to CelebAMask-HQ's 512-px faces. |
| Mask | **Not faithful.** The Apple-Vision hull keeps the nose bridge, any eyeglass frames and lenses, some stubble and beard, and occasionally a hand (checked against `overlay.png`). A CelebAMask-HQ "skin" mask excludes the nose and eyeglasses as separate classes. This biases the replication toward *more* bright and specular pixels. However, the cheek-only variant reproduces the key dark-subject effects (estimator shift of −28.8° and −31.3° for subjects 4 and 12, against −28.0 and −36.6 with the full mask), so the nose bridge is not what drives them. Glasses glare cannot be excluded, because MST-E does not label glasses. |
| Fairness of MST-E as a test | MST-E deliberately includes poor lighting. Under the paper's construct, changes in L\* across lighting are *expected* (Fig. S3 caption), so the all-image L\* ICC of 0.13 is **not** a fair indictment of the instrument. The fair tests are the **well-lit** and **well-lit frontal** subsets. MST-E is also phone photography (Pixel, HDR+ / auto white balance, AWB). Results transfer to CelebA, FFHQ and CFD only as an existence proof. |

### Key MST-E results after stress-testing

**1. ICC(1), with subjects as targets.**

| Subset | h\* ICC [cluster-bootstrap CI] | h\* within SD / between SD | L\* ICC |
|---|---|---|---|
| All images | 0.29 [0.17, 0.39] | 12.2 / 8.0 | 0.13 |
| Well-lit | 0.46 [0.30, 0.56] | 11.8 / 10.8 | 0.50 |
| Well-lit frontal | 0.50 [0.34, 0.58] | 11.1 / 11.3 | 0.51 |
| Well-lit frontal, no negative h\* | 0.44 | 8.0 / 7.7 | 0.52 |

- Dropping subjects 4 and 12 *lowers* the h\* ICC (well-lit 0.37; frontal 0.40). Restricting to MST ≤ 7 gives 0.40. **The low reliability is not driven by 2 subjects.**
- **The paper's estimator has a *higher* ICC than the naive pixel-mean hue** (well-lit: 0.46 against 0.28). But its between-subject SD is twice as large (10.8° against 5.4°). Much of that between-subject variance is the tone-linked estimator bias described in K06, so its "reliability" is partly inflated by a stable bias.
- In the cleanest subset, the pixel-mean hue reaches an ICC of 0.46–0.47 with a between-subject SD of only about 4.5°. In phone photos of 19 people spanning MST 1–10, apparent hue hardly separates the people.

**2. Same-image estimator repeatability.**

| Variant (vs. seed 2021, n_init=10) | p95 \|Δh\*\| | p95 \|ΔL\*\| | Hue-category flips | Tone-category flips |
|---|---|---|---|---|
| Seeds 1 and 2, n_init=10 | ≈ 1.0° | ≈ 1.1 | 0.1–0.2% | 0.8% |
| n_init=1 (the scikit-learn ≥ 1.4 default 'auto', since the released code relies on defaults) | 6.9° | 7.4 | — | 2.9% |

With n_init=10 the estimator is repeatable. With n_init=1, r(h\*) = 0.94. **The released code's outputs therefore depend on the installed scikit-learn version.** This is a new reproducibility point.

**3. The estimator's tone-dependence.** Within-subject SD of h\* in well-lit images:

| Estimator | MST 1–3 | MST 4–6 | MST 7–10 | ρ with MST (p) |
|---|---|---|---|---|
| Paper estimator | 6.7° | 8.2° | 16.2° | 0.67 (0.002) |
| Pixel-mean hue | 4.4° | 5.1° | 8.7° | 0.16 (0.50) |

- The excess instability belongs to the estimator, not to the pixels.
- It survives atan2 (ρ = 0.67) and aggregated-(a\*, b\*) hue (ρ = 0.58).
- It survives dropping subjects 4 and 12 (ρ = 0.55, p = 0.02).
- It is **not significant in the well-lit frontal subset** (ρ = 0.34, p = 0.16; dropping the 2 subjects gives 0.08).
- **Mechanism.** Across 732 well-lit images, |estimator h\* − pixel-mean h\*| rises as the chroma of the selected top-3 clusters falls: Spearman ρ = −0.49, p ≈ 3e-45. For subjects 4 and 12, the top-3 clusters have C\* ≈ 8–10, against a whole-face median of 13–15.
- The "≈14° shift toward red for MST 7–10" is **driven by subjects 4 and 12** (−28°, −37°). The other four MST 7–10 subjects shift by −0.1° to −8.5°; dropping the 2 gives ρ = −0.17, p = 0.53.

**4. The threshold result is robust.** On MST-E, the share of images with h\* ≥ 55 is 1.5–1.9% under every estimator variant: paper estimator, cheeks, pixel-mean, and atan2.

**5. Golden vs. "not-ideal" pairs (n = 15).**

- All 6 changes of 4-cell category are **tone** flips. There are **0 hue flips**, because almost everything on MST-E is "red".
- The pairs also differ in pose for 9 of the 15 subjects.

### New design facts from the released code (relevant to K11/K12)

- **Fixed positions in `cropping/generate.py`.** Top or bottom position is fixed by group order (`itertools.combinations` over W, B, A, I, L × F, M). The share of a group's games played on top is deterministic: White-F 100%, White-M 89%, Black-F 78%, Black-M 67%, Asian-F 56%, Asian-M 44%, Indian-F 33%, Indian-M 22%, Latino-F 11%, Latino-M 0%.
- **Fixed resize.** Images are resized to a fixed 859×611 (`cv2.resize`). This is not an aspect-preserving resize, although the text says the aspect ratio is preserved.
- **Win rule.** A face "wins" when the crop's top-left y-coordinate is below 887.
- **Games per face.** These are exactly 4500 / n_group, ranging from 43.3 (Black-F, n = 104) to 86.5 (Asian-M, Latino-M and Indian-F, n = 52).

---

## K01. No external validity anchor for L\*/h\*

- **Verdict: PARTLY CONFIRMED.**
- **Corrected severity: Major (not Critical).** The paper does report no anchor. But for an image-level construct, a colorimeter anchor is the wrong criterion, the right anchors are cheap to add, and tone already shows robust convergent validity.

**Technical corrections.**

- **Wrong criterion.** Spectrophotometer readings measure *constitutive* colour, which the paper explicitly disclaims (p2). Demanding them is a demand for a different construct. They become necessary *only* for the person-level claims (see K05, K09).
- **The right anchors for "apparent colour as a model sees it":**
  1. agreement with human perception of the *image*, since the paper invokes "perceptual" CIELAB;
  2. agreement with existing image-level tone labels (MST/Fitzpatrick annotations);
  3. fidelity of the estimator to the masked skin pixels, against simple robust summaries such as the median a\* and b\*.
- **Tone has convergent validity, and it is robust.** Subject-level L\* against the MST oracle gives ρ = −0.70 (full mask, well-lit) to −0.76 (cheeks). The jackknife range is −0.64 to −0.84, and dropping 2 subjects gives −0.70 / −0.78.
- **Hue has none.** This cannot be tested on MST-E, since MST is a tone scale. The pixel-mean hue's ρ with MST of about 0 is not a validity failure.
- **The critique misses one piece of evidence the paper does give.** There is known-groups evidence on CFD (Fig. S5b; released scores): Asian 61.8° > Latino 59.2 > Black 58.7 > White 56.8 > Indian 55.4, with η² = 0.14. Asian > White matches the direction in the in-vivo literature the paper cites ([17]). This is weak but genuine evidence.

**Strongest author rebuttal.** "Apparent colour *is* the pixel colour, so CIELAB conversion is the measurement, and validity is definitional."

**Does it succeed?** Partly. It covers the colour conversion, but not the estimator: on MST-E, the estimator's h\* correlates only r = 0.54 with the pixel-mean hue. Nor does it cover the person-level claims.

---

## K02. No reliability evidence

- **Verdict: CONFIRMED** for the paper. The **local evidence is partly over-stated** and needs to be re-cut.
- **Corrected severity: Major.** Even in the fairest subset (well-lit frontal), half the variance of both L\* and h\* is within-person. Many images sit within ±3 units of the cut-points (25% of CelebA and 36% of CFD images within ±3° of 55°), so the binary labels are unstable.

**Technical corrections to the canonical text.**

- **Lead with the well-lit figures.** The headline "72% of h\* variance within subjects" and "L\* ICC 0.13" are all-image figures, dominated by MST-E's *deliberately* poor lighting. Under the paper's own construct, L\* is expected to move with lighting. The fair figures are:
  - well-lit: h\* ICC 0.46 [0.30, 0.56], L\* ICC 0.50;
  - well-lit frontal: h\* 0.50 [0.34, 0.58], L\* 0.51.

  That is about 50–54% within-person variance, not 72%.
- **The result is not driven by 2 subjects.** Dropping them lowers the ICC.
- **The ICC is sample-dependent.** MST-E's between-person hue spread is small (pixel-mean SD of about 5°). A better transportable statistic is the within-person SD:
  - h\*: 8–12° (8.0° in the cleanest subset);
  - L\*: about 8.5.
- **The K-means seed concern is refuted** for the authors' configuration. At n_init=10, seeds change h\* by p95 ≈ 1°, with 0.1–0.2% category flips. In its place there is a **version-dependence** issue: under scikit-learn ≥ 1.4 the defaults give n_init=1, which moves p95 |Δh\*| to 6.9° and |ΔL\*| to 7.4, and flips tone in 2.9% of images. The code should pin n_init.
- **Mask sensitivity** (full vs. no-forehead variant): r = 0.92 for h\*, 95% agreement on the 4-cell category. This is moderate.
- **Distinguish two reliability concepts.**
  - *Instrument repeatability* (same image under seed, mask or compression changes) is the right reliability for an image-level construct.
  - *Within-person stability* across images is a test of the person-level reading (K09/K05).

  The canonical issue mixes the two.

**Strongest author rebuttal.** "Cross-image variation of the same person *is* apparent-colour variation, not unreliability."

**Does it succeed?** Partly. It does succeed for the cross-lighting L\* variation. It fails for h\*, which the paper explicitly claims is "stable and robust" (p13). It also fails for the dataset and person claims, and for repeatability, which the paper never reports.

---

## K03. Fig. S3 cannot support h\* robustness and misreports L\*

- **Verdict: CONFIRMED** (mechanism verified in the DPR code; numbers verified on p13).
- **Corrected severity: Major, to be merged with K02 in the final count.** Its substantive consequence is that the paper has no valid evidence that h\* is robust to illumination. That is the same gap and the same new data as K02. Standalone, what remains is a misreport and a non sequitur.

**Technical corrections.**

- **DPR verified.** The demo replaces only `Lab[:,:,0]` (OpenCV Lab), and the SH lighting is a single grey channel of 9 coefficients. So per-pixel a\* and b\* are preserved up to 8-bit rounding and gamut clipping. The residual 57.08–59.12° spread reflects changes in cluster selection.
- **A nuance in the authors' favour.** For diffuse reflection under *achromatic* intensity change, CIELAB hue is theoretically nearly invariant (outside clipping and the low-L\* region). So the narrow claim ("h\* stable to white-light direction and intensity") is plausibly *true*; the test simply cannot show it. The real threats are illuminant chromaticity and AWB, camera tone curves, speculars, and low-light noise. The paper's own Fig. S1(a) shows h\* = −25.38 under a colour cast.
- **Numbers.**
  - The original is 66.63 and the minimum is 59.41: a deviation of −7.22 (max +4.71, range 11.93), not "up to 6".
  - The 59.41 panel crosses L\* = 60.
  - Also notable: the Fig. S3 subject, a visibly dark-skinned face, scores "light" (66.63) and "yellow" (59.12) in the original image, which illustrates K04.
- **The local MST-E evidence needs caveats.**
  - The well-lit to poorly-lit h\* shift (per-person −18.5° to +32°; frontal-only SD 11.7°, pixel-mean SD 8.2°) confounds intensity with illuminant chromaticity. It therefore does not test the paper's narrow claim, but it does refute "h\* remains stable" as a general property.
  - The golden-pair statistic "6/15 change 4-cell category" should be **dropped as h\* evidence**. All 6 are L\* flips, there are 0 hue flips, and 9 of the 15 pairs also change pose.

**Strongest author rebuttal.** "S3 was scoped to direction and intensity, and S1 already concedes cast effects."

**Does it succeed?** Partly. The test's scope was stated honestly. But the conclusion drawn from it ("robust … orthogonal") over-reaches, and the misreported "6 points" stands.

---

## K04. Thresholds 60 / 55° transplanted without justification or sensitivity analysis

- **Verdict: CONFIRMED.**
- **Corrected severity: Major.** With the released scores, the reported proportions move a long way under 5-unit shifts of either cut. Fixing it needs reanalysis: sweeps or continuous analyses, and calibration if the categories are to mean "light" or "yellow".

**Technical corrections and additions.**

- **Literature provenance (partly resolved).** Ly et al. 2020 (JID, "Research Techniques Made Simple") is a methods primer. Its well-known cut-points are **ITA** bands, and **55° is the ITA "very light / light" boundary**. I found no evidence that Ly et al. gives an h_ab = 55° or L\* = 60 cut-point. The full text was not accessible (HTTP 403), so this remains **unverified**.
  - A secondary extraction of Ly et al.'s per-ITA-group mean L\*, a\* and b\* (unverified) gives in-vivo h_ab ≈ 76 / 68 / 68 / 63 / 60 / 53° from very light to dark.
  - If that is right, h ≥ 55 would label almost all in-vivo skin "yellow".
  - L\* = 60 falls between the "intermediate" (63.3) and "tan" (57.5) means, near ITA 28°, which is the paper's own quoted light/dark ITA boundary. So 60 has a plausible rationale and 55° does not.
  - The paper should state the derivation.
- **Sensitivity using the released scores** (% of images "yellow" at hue cut-points 50 / 55 / 60, and % "light" at L\* cut-points 60 / 65):

  | Dataset | % yellow at 50° | at 55° | at 60° | % light at L\* 60 | at 65 |
  |---|---|---|---|---|---|
  | CelebA | 56.8 | 33.8 | 16.8 | 74.4 | 56.7 |
  | FFHQ | 34.2 | 18.1 | 8.0 | 66.3 | 49.9 |
  | CFD | 93.4 | 72.1 | 37.3 | 62.4 | 49.1 |

  - At 50°, CelebA is *yellow*-majority.
  - Near the cut-points: 24.8% of CelebA, 15.9% of FFHQ and 36.3% of CFD images lie within ±3° of 55°; 14–18% lie within ±3 of L\* = 60.
- **Weak evidence to drop.** The MST-swatch evidence (h\* = 47–79°) depends on the swatch source. Recomputing from the commonly published MST hex codes gives h ≈ 49–89° and C\* ≈ 3.8 for MST10. The *non-monotonic* conclusion holds, but display swatches are not skin measurements. Drop this or caveat it.
- **Strong evidence to keep.** The MST-E "1.5% yellow" figure is robust across all estimator variants (1.5–1.9%).

**Strongest author rebuttal.** "Fixed literature cut-points are a convention; Fig. S6 shows full histograms."

**Does it succeed?** No. Fig. S6 colours the histograms by the same binary split and never sweeps the cut-points. The text claims "different thresholds confirm" (p5) without showing any.

---

## K05. Dataset "skew" has no reference distribution; capture conditions are confounded with population

- **Verdict: CONFIRMED** for hue. **PARTLY CONFIRMED** for tone.
- **Corrected severity: Major, not Critical.**
  - The descriptive numbers are correct and reproducible.
  - The generative-model "reproduces" half of claim (ii) is a cut-independent relative comparison, and it survives.
  - The tone half has external support from literature and demographics.
  - The *hue-skew* sentence on its own is effectively uninterpretable as a bias claim: its direction flips between 55° and 50°.

**Technical corrections.**

- **The light-tone skew is also cut-relative.** At L\* = 65, FFHQ is 49.9% light and CelebA 56.7%. Against CFD (a deliberately diverse population, 62.4% light at 60), CelebA's 74.4% is only a modest excess.
- **Capture confound: the cleanest within-paper contrast.** CFD *White* subjects (mean h 56.8°) are about 60% "yellow" (110/183). CelebA, which is mostly White celebrities, is 34% yellow. MST-E's diverse phone photos are 1.5% yellow. Comparable populations give hugely different yellow shares under different capture pipelines.
- **Medians.** h\* is 51.5 in CelebA, 45.6 in FFHQ and 58.2 in CFD. The 55° cut sits above both web-dataset medians.

**Strongest author rebuttal.** "Binary reporting against fixed scale cut-points is standard in fairness audits (e.g., Gender Shades)."

**Does it succeed?** Partly, for tone. Gender Shades used a *balanced benchmark* plus external demographics. It fails for hue, which has no external anchor and whose skew direction is determined by the cut.

---

## K06. Estimator design unjustified and unablated; skin-tone-dependent error

- **Verdict: CONFIRMED** on the design and ablation. **PARTLY CONFIRMED** on the empirical tone-dependent error.
- **Corrected severity: Major.** The estimator is the paper's core contribution. On MST-E the estimator and the pixel-mean hue correlate only r = 0.54. And there is reproducible, mechanism-backed evidence that the estimator adds tone-linked hue instability.

**Technical corrections.**

- **Robust:**
  - the within-person h\* SD gradient in well-lit images (6.7° / 8.2° / 16.2° across MST groups; ρ = 0.67);
  - survives atan2, aggregated (a\*, b\*), cheek-only masks and dropping 2 subjects (ρ = 0.55, p = 0.02);
  - absent for the pixel-mean hue (ρ = 0.16), so it is estimator-specific;
  - the mechanism is supported at image level (|Δ from pixel mean| against chroma of the selected clusters: ρ = −0.49, n = 732).
- **Not robust:**
  - in well-lit *frontal* images the gradient is not significant (ρ = 0.34, p = 0.16);
  - the "≈14° toward red for MST 7–10" figure is driven by subjects 4 and 12 (other dark subjects shift −0.1° to −8.5°; dropping the 2 gives ρ = −0.17, p = 0.53).

  Report it as "suggestive; median shift for MST 7–10 ≈ −8°; 2 of 6 dark subjects shift > 25°".
- **The arctan bug (K08) is not the driver.** The atan2 variant has the same gradient.
- **Transfer is uncertain.** Fidelity limits (landmark mask, phone HDR+) mean the size of the effect on CelebA, FFHQ and CFD is unknown. The *direction* of the risk is credible: brightest-cluster selection picks low-chroma, specular-rich pixels.
- **Seed robustness is fine** at n_init=10 (see K02).

**Strongest author rebuttal.** "Top-3 removes beard and shadow, and the code is released for others to ablate."

**Does it succeed?** No. The ablation burden falls on the instrument's proposer, and the art-book justification [57] is not methodological.

---

## K07. Low-chroma ill-conditioning; chroma dropped

- **Verdict: PARTLY CONFIRMED.**
- **Corrected severity: Minor as a standalone item.** The material mechanism is the estimator's selection of low-chroma bright clusters, which is already counted in K06. Omitting chroma as a reported dimension is a rigour issue.

**Technical corrections.**

- **The mathematics is right.** σ_h ≈ σ_ab / C\*. At C\* ≈ 15, 1 unit of a\* moves h by about 3.8°; at C\* ≈ 8, by about 7°.
- **The "MST10 swatch C\* ≈ 5.8, 1 unit → 9°" evidence is mis-specified.** It refers to a display swatch, not measured skin.
- **On real MST-E photos, whole-face median C\* is not strongly tone-dependent.** It is 21.6 for MST 1–3, 24.4 for MST 4–6 and 17.3 for MST 7–10; ρ = −0.29, p = 0.23. Low chroma arises in the *selected top-3 clusters* of some darker subjects (C\* ≈ 8–10).
- **Chroma gating helps.** Excluding the lowest quartile of selected-cluster chroma cuts the within-person h\* SD from 11.8° to 6.8° (well-lit). That supports the proposed fix.

**Strongest author rebuttal.** "Clustering plus histogram modes is robust to pixel noise."

**Does it succeed?** Partly. It holds for typical images, but not for low-chroma highlight clusters.

---

## K08. arctan, not atan2; Eq. 2 range inconsistent

- **Verdict: CONFIRMED** (code), but the **impact claims are over-stated**.
- **Corrected severity: Minor**, as proposed.

**Technical corrections.**

- **Negative h\* is mostly not an arctan artefact.** Negative values with a\* > 0 and b\* < 0 (quadrant IV) are identical under atan2 in (−180°, 180°].
  - On MST-E, atan2 gives 53 negative images against arctan's 51.
  - Switching changes the ≥ 55 share from 1.6% to 1.9%.
  - Reliability is unchanged (well-lit ICC 0.44 against 0.46).
- **A non-obvious side effect.** atan2 changes final h\* by more than 1° in 33% of MST-E images. A few a\* ≤ 0 pixels (median 0.01%, p95 3.8% of pixels) re-shape the K-means partition.
- **Size of the impact in the released scores.** The share of h\* < 0 images is CelebA 1.16%, FFHQ 2.85% and CFD 0%; none exceed 90°. All of them land in "red". That bounds the effect on Table 1 at about 1–3 points of the red share.
- **Under the paper's own stated 0–360° convention, these images would wrap to ≥ 270° and count as "yellow".** The real defect is the absence of a rule for values outside 0–90°, plus the Eq. 2 / code mismatch.

**Strongest author rebuttal.** "Skin pixels sit in quadrant I, so arctan equals atan2 there."

**Does it succeed?** Largely, for the aggregate tables. It does not fix the documentation inconsistency.

---

## K09. Construct drift

- **Verdict: PARTLY CONFIRMED.** The quotes are verified: "constitutive complexity" (p9); "predict people with lighter skin tones as more feminine" (p4); "under-represent dark-yellow skin color" (p2); and the balancing recommendation (p5).
- **Corrected severity: Minor**, for the residual not already counted in K01, K02 and K05. The fix is textual: scope the claims to images, and add a caveat on capture covariates to the balancing recommendation.

**Technical corrections.**

- **The person-level evidentiary gap is real.** On MST-E, well-lit ICCs are about 0.5. But it is already counted in K02 (stability), K05 (dataset composition) and K01 (anchor).
- **"Classify people with lighter skin as more feminine"** describes image edits. It is shorthand, and it is not a substantive error.
- **The balancing recommendation's Goodhart risk is credible.** MST-E shows that lighting alone moves L\* by about 29 points and h\* by ±12° per person. It needs a caveat, not new data.

**Strongest author rebuttal.** "For robustness, diversity of *apparent* colour, including lighting, is exactly what a model needs."

**Does it succeed?** Yes for robustness. No for the demographic framing: A.3's "Indian or Asian skin colors" and "under-represent".

---

## K10. Incremental value of hue never tested; L\* and h\* correlated, contradicting "orthogonal"

- **Verdict: PARTLY CONFIRMED.** The incremental-value half holds only against ITA and continuous models. The **correlation half is largely refuted** by the paper's own released scores.
- **Corrected severity: Minor.**
  - In the paper's data, the hue groups are nearly independent of L\*.
  - Fig. 3c already gives within-tone hue contrasts.
  - The remaining threats to core claim (iii) are confounding (K11), non-significance (K13) and edit specificity (K16), all counted elsewhere.

**Technical corrections.**

- **Continuous association in the released scores is tiny.**

  | Dataset | Spearman ρ(L\*, h\*) | Pearson r |
  |---|---|---|
  | CelebA | +0.11 | +0.02 |
  | FFHQ | +0.03 | −0.02 |
  | CFD | +0.10 | +0.14 |

  The binary odds ratios (CelebA 0.557, FFHQ 0.633, CFD 0.958; recomputed) reflect a modest, heteroscedastic dependence: dark images spread more widely in hue (Fig. 2 funnel). They do not reflect a correlation.
- **Drop the local MST-E r = 0.53.** It is estimator-driven and not robust: well-lit 0.42 (p = 0.07), frontal 0.35 (n.s.), pixel-mean 0.35–0.40 (n.s.).
- **"Orthogonal" as coordinates is correct by definition.** The S3 "orthogonal information" inference is still a non sequitur (K03).
- **Still missing:** an ITA baseline, since ITA contains b\*, and continuous nested models.

**Strongest author rebuttal.** "Fig. 3c tests hue within tone strata, and L\*/h\* are empirically near-independent."

**Does it succeed?** Mostly. Both points are verifiable from the released data.

---

## K11. Cropping audit: hue confounded with ethnicity and source; position and cropper version unreported

- **Verdict: CONFIRMED** for ethnicity and source. **PARTLY CONFIRMED** for position, for which there is new evidence from the code.
- **Corrected severity: Major.** Claim (iii) for cropping is an association that cannot be separated from ethnicity or source. A Bradley–Terry model with covariates, or within-ethnicity contrasts, is required.

**Ethnicity and source, computed from the released scores and metadata.**

- Hue differs by ethnicity: F = 30.1, η² = 0.14. Means: Asian 61.8, Latino 59.2, Black 58.7, White 56.8, Indian 55.4.
- Composition of the intersectional cells:
  - **DR (79):** 56% Indian, all from CFD-India; 38% Black.
  - **DY (199):** 76% Black.
  - **LR (127):** 57% White, 20% Indian, 19% Latino.
  - **LY (334):** Asian 97, White 109, Latino 79.
- So the within-dark hue contrast is roughly CFD-India Indian vs. CFD Black, and within-light it is roughly White vs. Asian/Latino.

**Position (new evidence from `generate.py`).**

- Group order fixes placement deterministically: White-F always on top, Latino-M always on bottom. The paper never reports this.
- **But the marginal groups are position-balanced:**
  - top share for light 0.560 vs. dark 0.561;
  - red 0.547 vs. yellow 0.565.

  So position **cannot explain the marginal tone and hue effects**.
- The intersectional cells are not balanced: DR 0.43, DY 0.61, LR 0.62, LY 0.54. Position can therefore distort Fig. 3c, in a direction that depends on the cropper's unknown top/bottom preference.
- Recommend counterbalancing.

**Other corrections.**

- **The cropper version is identifiable from the code.** It is Twitter's public `image-crop-analysis` binary and the `fastgaze.vxm` model; only the commit is missing. Minor.
- **The text says aspect ratio is preserved, but the code uses a fixed 859×611 `cv2.resize`.** CFD's native ratio is about 1.42, so the distortion is about 1.2%. Whether CFD-India images share CFD's dimensions is unverified; if they do not, the distortion is aliased with the Indian group.
- **Strength retained.** Binary tone composition is 61.65% vs. 62.66% light (OR 0.96).

**Strongest author rebuttal.** "Adjusting for ethnicity over-adjusts, because skin colour is part of what ethnicity labels capture."

**Does it succeed?** Partly. The paper's own causal language ("skin hue reveals additional differences", "preference") needs the colour channel to be isolated from morphology, hair and source. A within-ethnicity analysis (White and Latino faces span 45–70°) is feasible.

---

## K12. Elo inference

- **Verdict: PARTLY CONFIRMED.** Every technical point is correct, but none can manufacture the marginal effects.
- **Corrected severity: Minor.**
  - The direction is robust.
  - Unequal games are design-balanced at group level, and they attenuate rather than create gaps.
  - The fix is a cheap refit (Bradley–Terry) on existing outcomes.
  - The intersectional ordering is the only fragile part.

**Technical corrections.**

- **Games per face are exactly 43.3–86.5.** By group:
  - dark 50.1 vs. light 67.4 games per face;
  - red 58.4 vs. yellow 61.9.

  Fewer games mean more shrinkage toward 1400, which **attenuates** the light–dark gap. That is conservative.
- **If true strengths are equal, expected Elo changes are zero.** Unequal schedules add variance, not bias.
- **Rough robustness check.** With implied gaps of 75.7 and 57.9, rating SDs of 100–160 and a design effect of 2, t ≈ 4.4–7.0 for tone and 3.1–5.0 for hue. The marginal p-values survive.
- **Still valid:**
  - zero-sum dependence;
  - "% preference" is model-implied (Jensen);
  - undefined Bonferroni family;
  - the Elo script and game order are not released (only `generate.py` and `predict_twitter.py`);
  - if Elo is run in file order (combination by combination), early groups play against unrated opponents, so there is an order effect of unknown size.

**Strongest author rebuttal.** "With 22,500 games, the gaps are many standard errors wide."

**Does it succeed?** Yes for the marginal claims. No for the exact percentages and the claim that "all pairwise intersectional groups differ".

---

## Strengths

| ID | Verdict | Notes / corrections |
|---|---|---|
| **S-a** Scope stated as apparent colour | **CONFIRMED** | Explicit (p2, p12). Weakened by the drift in K09, but genuine. |
| **S-b** L\* + h\* rather than ITA; cylindrical CIELAB basis | **PARTLY CONFIRMED** | The algebraic separation is real. The released scores show L\* and h\* are empirically near-independent (\|ρ\| ≤ 0.11), which *supports* this strength more than the canonical list credits. Caveats: the implementation is not h_ab (arctan); chroma is dropped; "L\* = 50 is max chroma" (p3) is incorrect. |
| **S-c** Code and dataset scores released | **CONFIRMED** | The scores reproduce Table 1 and the Fig. 3 n's exactly. The release is also what exposed arctan, the left-edge mode, the reliance on scikit-learn defaults, fixed cropping positions and the fixed resize. Missing: the Elo script, edit strengths and the LFW loader. |
| **S-d** Fig. 3 n's; balanced binary tone composition | **CONFIRMED** | 61.65% vs. 62.66% light, OR 0.96. Continuous ρ(L, h) in CFD is 0.10. New: the marginal top-position share is also balanced (0.547 vs. 0.565). Not balanced: ethnicity (K11). |
| **S-e** Tone × hue intersections with Bonferroni | **PARTLY CONFIRMED** | The right *type* of within-stratum analysis, but the family is undefined, it uses t-tests on dependent Elo ratings, there is no factorial model, and it covers cropping only (Table 3 has no tests). |
| **S-f** Edits compared with reconstructions | **CONFIRMED** | p8. Caveats: original-image accuracy and reconstruction fidelity are not reported. Reconstruction itself moves the scores: face 1 L\* 67.29 → 61.92; face 3 h\* 59.07 → 55.96, near the cut. |
| **S-g** "Pale" as a discriminant contrast | **PARTLY CONFIRMED** | Works for the *tone* edits: light/dark \|Δh\*\| ≤ 3.5° against pale/−pale \|Δh\*\| up to 8.6°. Fails to discriminate for the *hue* edits, whose L\* cross-talk (+7.62 on face 2; +2.17, +3.77 elsewhere) is comparable to pale's hue cross-talk. n = 3, checked with the same instrument. |

---

## Summary table

| ID | Verdict | Proposed → corrected severity | One-line reason |
|---|---|---|---|
| K01 | PARTLY CONFIRMED | Major / possibly Critical → **Major** | No anchor reported, but the colorimeter criterion is mis-targeted for an image construct, and tone has robust convergent validity (ρ ≈ −0.70 to −0.76). |
| K02 | CONFIRMED (local stats re-cut) | Major → **Major** | Well-lit frontal ICC ≈ 0.5 for both L\* and h\* (not 0.13/0.29); robust to dropping subjects; seed concern refuted; scikit-learn-version dependence is new. |
| K03 | CONFIRMED | Major → **Major (merge with K02)** | DPR is L-only by code; 7.22, not 6; the golden-pair "6/15" flips are all tone, so drop them as h\* evidence. |
| K04 | CONFIRMED | Major → **Major** | 55° matches an ITA band boundary, not an h_ab cut (unverified); sweeps flip the CelebA hue majority at 50°. |
| K05 | CONFIRMED (hue) / PARTLY (tone) | Major / possibly Critical → **Major** | Descriptives are correct; the "skew" depends on the cut and the capture pipeline (CFD White 60% (110/183) yellow vs. CelebA 34% vs. MST-E 1.5%). |
| K06 | CONFIRMED (design) / PARTLY (empirics) | Major → **Major** | Estimator-specific, tone-linked h\* instability (ρ = 0.67; robust to atan2 and drop-2) with a chroma mechanism; n.s. in frontal-only; the 14° shift is 2-subject driven. |
| K07 | PARTLY CONFIRMED | Major → **Minor** | Whole-face chroma is not tone-dependent on MST-E; ill-conditioning arises in the selected clusters (K06); the swatch evidence is mis-specified. |
| K08 | CONFIRMED (impact overstated) | Minor → **Minor** | Negative h\* is mostly quadrant IV, the same under atan2; ≤ 1–3% of images; a documentation and rule gap. |
| K09 | PARTLY CONFIRMED | Major → **Minor** | The residual after K01/K02/K05 is wording plus a balancing caveat. |
| K10 | PARTLY CONFIRMED | Major → **Minor** | Released scores give \|ρ(L, h)\| ≤ 0.11; Fig. 3c gives within-tone contrasts; only an ITA/continuous baseline is missing. |
| K11 | CONFIRMED (+ new code evidence) | Major → **Major** | DR ≈ CFD-India Indian, DY ≈ Black (η² = 0.14); positions fixed by group order but balanced marginally. |
| K12 | PARTLY CONFIRMED | Major → **Minor** | The directions survive (t ≈ 3–7); unequal games attenuate gaps; percentages and intersectional ordering are fragile. |
| S-a | CONFIRMED | — | — |
| S-b | PARTLY CONFIRMED | — | — |
| S-c | CONFIRMED | — | — |
| S-d | CONFIRMED | — | — |
| S-e | PARTLY CONFIRMED | — | — |
| S-f | CONFIRMED | — | — |
| S-g | PARTLY CONFIRMED | — | — |

**Not done (would strengthen K02).** A within-identity ICC on CelebAMask-HQ using the authors' released scores. This needs the CelebA identity file and the CelebA-HQ mapping, which are distributed via Google Drive or on request. I did not download them.

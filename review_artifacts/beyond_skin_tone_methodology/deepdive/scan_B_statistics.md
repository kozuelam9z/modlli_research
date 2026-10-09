# Scan B: Statistical inference and audit design

**Paper:** Thong, Joniak and Xiang, "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color" (arXiv 2309.05148v2).
**Perspective:** statistical inference and audit design. I checked every quantitative comparison: Tables 1 to 4, Figure 3, Figure 4 and Figures S3 to S6.
**Reproducible arithmetic** (all in `deepdive/`):
- `checks_B.py`: table margins, z and χ² tests, Elo conversions, rough intersectional t-tests, and the Table 4 consistency check.
- `table3_cells.py`: recovers the integer counts behind Table 3.
- `table3_tests.py`: exact Fisher tests and Newcombe confidence intervals on those counts.
- `elo_sim.py` and `elo_sim2.py`: simulations of the Elo design.

Python environment: the scratchpad venv (numpy, scipy, statsmodels).

Severity scale:
- **Critical:** on its own, invalidates a core claim.
- **Major:** materially weakens a core claim; fixing it needs substantial reanalysis or new data.
- **Minor:** affects clarity or rigour without changing the core claims.

Confidence runs from 1 (low) to 5 (certain).

---

## Summary verdict per table and figure

| Item | Claim wording | Do the reported numbers support it? |
|---|---|---|
| Table 1 | "Images are skewed towards a light skin tone and a red skin hue" | The arithmetic holds (one 0.01 rounding slip). "Skew" or "bias" has no reference distribution and depends on the threshold (B8). |
| Table 2 | "Both StyleGAN3 and P2 reproduce the skin color bias"; "P2 slightly amplifying the bias" | StyleGAN3 matches FFHQ to within about ±1 pp (χ² p = 0.86), so "reproduce" holds. P2 amplifies on hue (+1.50 pp, p ≈ 3×10⁻⁴) but *attenuates* the light-tone skew (+0.96 pp dark, p ≈ 0.04 to 0.06). The "amplifying" claim is therefore only half supported (B12). |
| Fig. 3 | Light preferred over dark, red over yellow, all intersectional pairs significant except LY–DR | The direction is plausible. The hue effect is confounded with ethnicity and dataset source (B4). The Elo estimator and the t-tests are not a sound inferential basis (B5). The "% preference" numbers are model-implied, not observed win rates (B9). |
| Table 3 | "better identified by all face verification models" | **Not supported.** All 18 contrasts I tested have p ≥ 0.09 and every CI spans 0 (B1). The ArcFace hue columns appear swapped; corrected, ArcFace favours yellow (B2). |
| Table 4 | Lighter tone gives more "female" predictions; redder hue gives more "smiling" predictions | The large effects are real as *prediction changes*. Attributing them to skin colour is not identified: the edits may also change the true attributes (B6), and there is leakage between L\* and h\* (B7). Small effects are overclaimed (B13). Three "All" cells are internally inconsistent (B14). |

---

## Critical

### B1. Face verification differences are statistically indistinguishable from zero, yet are reported as model bias in "all" models
- **Quotes:**
  - Table 3 caption: "Individuals with a light skin tone or a red skin hue are better identified by all face verification models."
  - §4.2.2: "both ArcFace and Dlib models are affected by skin tone differences"
  - "FaceNet has a different behaviour, it is more robust to skin tone differences but as prone to skin hue differences as Dlib."
  - "Overall, this benchmark confirms that in well-established methods for face verification, there exist performance differences in both skin tones and skin hues"
- **Location:** §4.2.2 Results; Table 3 (p. 6–7).
- **Problem:**
  - Table 3 has no CIs, no tests and no subgroup sizes. I recovered the integer counts behind it exactly (`table3_cells.py`). With 1,000 pairs and an overall accuracy of 95.20% (952 correct), the tone split is feasible for **only** n_light = 715 / n_dark = 285, and this holds for all three models. The hue split (FaceNet and Dlib) is feasible only at n_red = 548 / n_yellow = 452. The intersectional cells are uniquely LR = 387, LY = 328, DR = 161, DY = 124.
  - Dlib reproduces every cell exactly. FaceNet does too, except LY = 306/328 = 93.29, which is printed as 93.30.
  - With these counts (`table3_tests.py`, Fisher exact test, Newcombe 95% CI):
    - ArcFace tone gap: +1.14 pp, CI [−1.63, +4.69], p = 0.51.
    - FaceNet tone gap: +0.51 pp, CI [−2.41, +4.18], p = 0.76.
    - Dlib tone gap: +0.72 pp, CI [−2.27, +4.46], p = 0.65.
    - Hue gaps: FaceNet +1.09 pp (p = 0.49), Dlib +1.12 pp (p = 0.50), ArcFace −0.28 pp after the correction in B2 (p = 0.88).
    - Across 18 tone, hue and intersectional contrasts, the smallest p-value is 0.09 (ArcFace LR vs DR).
  - The gaps amount to roughly 1–5 pairs in the smaller group.
  - The claim that FaceNet is "more robust" than Dlib on tone rests on a 0.22 pp difference in gaps. That is about 0.6 of one dark-group pair.
  - Power: the minimum detectable tone gap (80% power, α = 0.05) is about 2.8 × √(.05·.95/715 + .056·.944/285) ≈ 4.4 pp. Detecting a 1 pp gap would need about 8,000 pairs per group.
- **Consequence:** The face-verification half of contribution (ii) ("revealing multidimensional skin color biases in … face verification models") has no statistical support. The data are equally compatible with reversed gaps. The model-ranking sentences ("affected" vs "more robust") interpret noise.
- **Fix:**
  - Report the subgroup n, Wilson or Newcombe CIs, and paired tests across models (McNemar on the same pairs).
  - Use a benchmark powered for gaps of 1 pp or less: many thousands of pairs per group, for example by constructing pairs from all LFW identities or by using demographically balanced verification sets.
  - Or reword the section as descriptive, with no claim of bias.
- **Severity:** Critical, because the only evidence for face-verification "bias" is a set of gaps that are entirely within sampling noise.
- **Confidence:** 5 for the arithmetic; 4 that the recovered counts are the actual ones (they are unique integer solutions).

---

## Major

### B2. ArcFace "Red/Yellow" columns are inconsistent with N = 1,000; integer reconstruction shows they are swapped, which reverses the hue direction for ArcFace
- **Quote:** Table 3, ArcFace row: "95.20 95.52 94.39 95.36 95.07 96.12 94.82 92.55 96.77". Text: "All models tend to prefer light skin tones and red skin hues."
- **Location:** Table 3 (p. 6).
- **Problem:**
  - With 1,000 pairs and 952 correct, **no** split n_red + n_yellow = 1000 yields red = 95.36% and yellow = 95.07% at 2-decimal rounding. Only N ∈ {938, 958, 979, 980, 999} would work, and those contradict the paper's 1,000 pairs.
  - At the n_red = 548 / n_yellow = 452 split, which FaceNet and Dlib reproduce, the possible ArcFace values are red ∈ {95.26, 95.44} and yellow ∈ {94.91, 95.13}.
  - ArcFace's intersectional cells are exactly consistent with the common cell sizes: LR 372/387, LY 311/328, DR 149/161, DY 120/124, and these also reproduce Light 683/715 = 95.52 and Dark 269/285 = 94.39. From these cells:
    - red = (372 + 149)/548 = **95.07**
    - yellow = (311 + 120)/452 = **95.35** (printed 95.36)
  - These are the reported values in swapped columns. The bold font on "95.36" under Red is therefore probably mis-assigned too.
- **Consequence:** After correction, ArcFace verifies *yellow* better than red (−0.28 pp, ns). The claim that light tone or red hue is better identified "by all face verification models" is false for one of three models, on top of B1.
- **Fix:** Recompute Table 3 from the raw predictions, publish per-group counts, and correct the text and the bolding.
- **Severity:** Major, because it directly contradicts a stated finding, and the transcription error lowers trust in the other tables.
- **Confidence:** 4. The integer argument is exact; the swap is the most parsimonious explanation.

### B3. Face-verification audit design: pair-to-group assignment is undefined, and accuracy at a fixed threshold conflates false non-matches with false matches
- **Quotes:**
  - "which contains 1,000 test pairs (500 positives and 500 negatives)"
  - "broken down by skin tone (light vs. dark) and by skin hue (red vs. yellow)"
- **Location:** §4.2.2 Method and Results.
- **Problem:**
  - The recovered counts show that each *pair* is counted in exactly one group (715 + 285 = 1000). The paper never says how a pair is assigned. A negative pair contains two different people, often with different skin colours, and a positive pair contains two photos whose measured L\* and h\* can differ.
  - Possible rules include the first image, the mean of the two, or requiring agreement. These give different groups. Cross-group impostor pairs are also easier to reject, so the group composition of negatives drives accuracy.
  - Overall accuracy at a single DeepFace default threshold mixes the false non-match rate (genuine pairs) with the false match rate (impostor pairs). The genuine/impostor mix per group is not reported, so an accuracy gap could reflect composition rather than model behaviour.
- **Consequence:** Even with adequate n, the estimand behind "better identified" is undefined. Group accuracy differences may be artefacts of the pair mix.
- **Fix:**
  - Define group membership at the identity level.
  - Report the false non-match rate on genuine pairs per group, and the false match rate on *same-group* impostor pairs per group.
  - Report per-group ROC curves and AUC, or rates at a threshold fixed for a target false match rate.
- **Severity:** Major, because the metric and the grouping both need redefinition before any bias claim can be made.
- **Confidence:** 4.

### B4. The cropping "hue effect" is not identified as a skin-hue effect: it is aliased with ethnicity, and partly with dataset source (CFD vs CFD-India)
- **Quotes:**
  - "From CFD, we sample pairs of facial images that are equally distributed with respect to gender and ethnicity."
  - Fig. 3 caption: "Complementary to the skin tone, the skin hue reveals additional differences in performance."
  - "with light-red skin colors being favored and dark-yellow skin colors being disfavored"
- **Location:** §4.2.1; Fig. 3; Fig. S5b.
- **Problem:**
  1. *Tone balance (in the paper's favour).* The Fig. 3 group sizes give red = 127 light / 79 dark (61.7% light) and yellow = 334 light / 199 dark (62.7% light). The binary-tone odds ratio is 0.96 (χ² p = 0.86), so binary tone composition cannot produce the marginal hue gap. Within-tone hue gaps are visible in Fig. 3c (medians roughly LR 1477 vs LY 1405, and DR 1412 vs DY 1312).
  2. *Ethnicity.* Fig. S5b shows that hue tracks ethnicity:
     - Asians are almost all yellow and light.
     - Black subjects are mostly dark-yellow.
     - The dark-red cell is mainly Indian, plus some Black subjects.
     - Light-red is mainly White.
     So the within-dark hue contrast is approximately "Indian vs Black", and the within-light contrast approximately "White vs Asian/Latino". A saliency model reads the whole image: face morphology, hair, eyes and background all co-vary with ethnicity. Any ethnicity effect maps onto hue. In a toy model with *no* skin-colour effect and only ethnicity effects, I obtained a light–dark gap of about 59 Elo points (`elo_sim.py`).
  3. *Dataset source.* All 142 Indian faces come from CFD-India, and the other 597 from CFD. The paper itself says "From CFD, we sample", although 739 = 597 + 142. The resolution, framing, background and lighting of the two collections are not reported. Any difference is perfectly aliased with Indian ethnicity, and hence with the dark-red cell. This matters because the authors note that "we noticed effects on the cropping algorithm when resizing images" and preserve aspect ratio, so image geometry demonstrably affects outcomes.
  4. *Gender* composition per skin group is not reported, although cropping is known to be gender-sensitive.
- **Consequence:** The wording "the skin hue reveals additional differences" and "multidimensional hierarchy on the skin color preference" implies that hue drives the preference. The design supports only an association between hue group and preference. That association is confounded with ethnicity and data source.
- **Fix:**
  - Fit a Bradley–Terry or logistic paired-comparison model on the 22,500 game outcomes. Use face random effects and covariates: continuous L\*, continuous h\*, ethnicity, gender, source dataset, image size, and position (B11). Test the h\* coefficient *within ethnicity*.
  - Alternatively, run the cropping audit on the paper's own hue-manipulated images (§4.3), which would hold identity fixed.
  - Report the ethnicity × skin-group cross-tabulation.
- **Severity:** Major, because the headline "hue reveals additional bias" claim for cropping cannot be separated from ethnicity and source effects.
- **Confidence:** 4.

### B5. The Elo estimator is unconverged and schedule-dependent, the design gives faces unequal numbers of games, and t-tests on ratings are a weak inferential basis
- **Quotes:**
  - "we set M = 400 and K = 16 and we initialize scores at 1400"
  - "We sample 500 pairwise comparisons for each combination, for a total of 22,500."
  - "confirmed with a statistically significant independent t-test (p < 0.0001)"
- **Location:** §4.2.1 Method and Results; Fig. 3.
- **Problem:**
  1. *Unequal games per face, fixed by design.* There are 45 cross-group combinations of the 10 gender × ethnicity groups (there are no within-group games), with 500 games each. Every group therefore makes 9 × 500 = 4,500 appearances regardless of its size, so the number of games per face is 4,500/n_group.
     - Using CFD's per-gender counts (recalled from CFD documentation and consistent with the paper's totals of 359 F / 380 M and 109/197/142/108/183), the range is 43 games per face (Black F, n = 104) to 87 (Asian M, Latino M and Indian F, n = 52). The mean is 60.9.
     - Even without the exact gender split, the ethnicity totals alone give about 46 games for Black faces vs about 83 for Asian faces.
  2. *Ratings are far from converged, and unequally so.* With heterogeneity tuned so that simulated Elo ratings span roughly 1040–1780 (the whisker range in Fig. 3), the regression slope of Elo on true strength is (`elo_sim2.py`):
     - 0.14–0.21 for faces with fewer than 55 games;
     - 0.19–0.30 for faces with more than 75 games.
     The rating SD is 132–135 vs 188–200. Ratings are compressed about 30% more for under-played groups, and those are exactly the Black and White subgroups, which drive the tone and hue contrasts. Group mean gaps are therefore not on a common scale. In `elo_sim.py`, the Elo group gap recovered only 45–57% of the true strength gap.
  3. *Sequential and zero-sum dependence.* Ratings sum to 739 × 1400, so the two group means are deterministic functions of each other. The ratings are also correlated through shared games. The game order (shuffled, or combination by combination) is not reported. In simulation, order effects were modest (SD ≈ 10 Elo points per face across permutations), so this is a secondary concern.
  4. *Test choice.* An "independent t-test" on Elo ratings compares estimated ratings with group-dependent shrinkage and variance. Student's or Welch's variant is not specified, and the simulated SDs differ by about 1.4×.
- **Consequence:** The *direction* of the tone and hue differences is probably robust: large n, and the gaps are consistent with the medians in Fig. 3. The *magnitudes*, the cross-cell comparisons (Fig. 3c), and the stated p-values rest on an estimator whose bias differs by ethnicity × gender group because of the sampling design.
- **Fix:**
  - Replace Elo with a Bradley–Terry maximum-likelihood fit (or a GLMM with face random effects), which handles unbalanced schedules, and add covariates (B4).
  - Report group effects with bootstrap CIs that resample faces and games.
  - Alternatively, balance games per face, or run Elo to convergence averaged over many random orders.
- **Severity:** Major, because the inferential statistics behind Fig. 3 need to be recomputed with an appropriate model, although the direction will probably survive.
- **Confidence:** 4. Simulation parameters are illustrative; the games-per-face arithmetic is exact given the stated design.

### B6. Table 4 does not identify a "causal effect of skin color": the latent directions may change the target attributes themselves
- **Quotes:**
  - "measuring the causal effect of skin color in attribute prediction"
  - Table 4 caption: "models classify individuals as smiling when their skin tone becomes lighter or when their skin hue becomes redder."
  - "Two linear SVMs, one for skin tone and one for skin hue, are finally trained on the most confident positive and negative predictions"
- **Location:** §4.3 Method and Results; Table 4.
- **Problem:**
  - The InterfaceGAN directions are learned from labels that a skin-colour classifier assigns to 500,000 StyleGAN3 samples. The directions are unconditioned: nothing projects out the gender or smile directions.
  - Any CelebA correlate of "red" or "light" is absorbed into the direction. Examples include makeup or lipstick, flushed cheeks and smiling, and femininity. These correlates are themselves predictive of the target attributes.
  - The Table 4b pattern under +red is exactly what a direction that genuinely increases smiling would produce: accuracy on smiling faces rises (AWS 92.80 → 96.88; Azure 97.29 → 99.00) and accuracy on non-smiling faces falls (93.66 → 86.38; 80.84 → 69.76). Likewise, "+light → classified female" is what a direction entangled with femininity would produce.
  - Ground truth is the *original* CelebA label. Whether the edited images still carry that label is never checked.
- **Consequence:** The data cannot distinguish "the classifier is biased by skin colour" from "the edit changed the smile or gender cues and the classifier correctly followed them". The causal claims in the abstract, introduction and §4.3 are therefore not identified.
- **Fix:**
  - Report the cosine similarity between the tone and hue directions and the InterfaceGAN gender and smile directions.
  - Use conditional manipulation (project out the attribute directions).
  - Have humans re-label a random sample of edited images for smile and gender, and report label-flip rates.
  - Report the effect as a function of edit strength (dose–response).
- **Severity:** Major, because contribution (iii) rests on this identification step.
- **Confidence:** 4.

### B7. The "orthogonal" manipulation claim rests on 3 faces and is contradicted by those faces; edit magnitudes are uncalibrated
- **Quotes:**
  - "Modifying the image in one direction does not affect the skin color score in the other direction, making them orthogonal."
  - "the skin hue does not seem to have a large effect"
- **Location:** §4.3; Fig. 4 (p. 7).
- **Problem:** The off-target shifts relative to the reconstruction in Fig. 4 (`checks_B.py`) are:

  | Edit | ΔL\* | Δh\* |
  |---|---|---|
  | +red | +2.2, **+7.6**, −0.8 | |
  | +yellow | −0.4, +2.3, +3.8 | |
  | +dark | | −0.1, **+3.5**, +0.9 |
  | +pale (CelebA) | | +1.1, +7.4, +3.5 |
  | −pale (CelebA) | | −3.2, −8.6, −4.3 |

  - The +red edit shifts L\* by up to 7.6 points. That exceeds the "up to 6 points" relighting shift which §A.2 treats as material.
  - The contrast between "ours is orthogonal" and "pale is not" is therefore not established at n = 3.
  - Because +light *also* increases "smiling" predictions, the L\* rise under +red is a direct alternative explanation for part of the red–smile effect.
  - The edit sizes are also unequal: ΔL\* ranges from +5.3 to +14.3 for +light and from −9.8 to −20.7 for +dark, while Δh\* is about −10 to −14 for +red and +7 to +10 for +yellow. Statements comparing tone and hue effects ("does not seem to have a large effect") therefore compare different dose sizes.
- **Consequence:** Attributing the smile effect to hue, and comparing tone effects with hue effects, are both unsupported.
- **Fix:**
  - Report the distribution of ΔL\* and Δh\* over all 30,000 edited images for each direction (mean, SD, and the correlation between on-target and off-target shifts).
  - Express accuracy changes per unit ΔL\* or Δh\*, or per natural SD of each measure.
  - Regress prediction change on both ΔL\* and Δh\* jointly.
- **Severity:** Major, because the hue-specific causal claim depends on edits being separable, and that is not shown.
- **Confidence:** 4.

### B8. Dataset "skew" and "bias" have no reference distribution, and the binary labels depend on borrowed thresholds whose meaning shifts with acquisition conditions
- **Quotes:**
  - Table 1 caption: "Images are skewed towards a light skin tone and a red skin hue while dark and yellow skin colors are underrepresented."
  - "This paper enables to quantify such skin color bias."
  - "Threshold values are taken from Ly et al. [46]."
- **Location:** §4.1; Tables 1 and 2; Fig. 2; Figs. S5 and S6.
- **Problem:**
  1. A 74/26 or 66/34 split is "skewed" only relative to a target distribution, such as a census population, a deployment population, or a balanced design. None is stated, so the percentages are descriptive, not a measure of bias.
  2. The cut-points (L\* = 60, h\* = 55°) come from colorimetry under controlled measurement. Here they are applied to sRGB pixel modes of in-the-wild photos. By eye, the Fig. S6 L\* histograms peak at about 65, so a shift of about 5 L\* units would move the light/dark split towards 50/50.
  3. The paper's own data show the hue cut-point is not comparable across acquisition settings. CFD is deliberately diverse (183 White, 109 Asian, 197 Black, 142 Indian, 108 Latino) and is 72% yellow (533/739). FFHQ is 18% yellow. In Fig. S5b, White CFD subjects straddle 55°. The "red skew" of in-the-wild datasets may therefore reflect capture and processing (white balance, lighting, makeup, flushing; see Fig. S1) as much as population composition.
- **Consequence:** Contribution (i), quantifying how much datasets are "skewed towards light-red", is threshold-relative and reference-free. The direction may well be right for light tone, but the magnitudes in Table 1 are not interpretable as bias.
- **Fix:**
  - State the reference distribution.
  - Report threshold-sensitivity curves: the share in each cell as each cut-point varies over a plausible range.
  - Report continuous summaries with CIs (medians and quantiles of L\* and h\*).
  - Validate h\* thresholds on images with known spectrophotometer readings, or at least compare against CFD captured under the same pipeline.
- **Severity:** Major, because the headline dataset-bias numbers depend on arbitrary cut-points and lack a comparator.
- **Confidence:** 4.

---

## Minor

### B9. "60.73% / 58.25% preference" are model-implied transforms of mean ratings, not observed preference rates
- **Quote:** "with an average Elo score indicating a 60.73% preference"; "an average Elo score indicating a 58.25% preference".
- **Location:** §4.2.1 Results.
- **Problem:**
  - Inverting p = 1/(1 + 10^(−Δ/400)) gives Δ = 400·log₁₀(p/(1−p)):
    - 75.7 Elo points for 60.73%;
    - 57.9 Elo points for 58.25%.
  - Under the zero-sum constraint, the implied group means are 1428.5 / 1352.8 (light/dark) and 1441.7 / 1383.9 (red/yellow), which is consistent with Fig. 3.
  - The logistic of a *mean* gap is not the mean win probability over cross-group pairs (Jensen's inequality). With within-group rating SDs of 100, 150 and 200, the latter is 59.4%, 58.4% and 57.4% instead of 60.73%.
  - Unconverged Elo (B5) pushes the other way: in simulation, the Elo-implied % (55.5–57%) fell *below* the empirical cross-group win rate (57–59%).
  - The direct, assumption-free estimand, the share of light-vs-dark games won by the light face, is available from the 22,500 games and is not reported.
- **Fix:** Report the empirical cross-group win rates with bootstrap CIs, and a Bradley–Terry-implied probability.
- **Severity:** Minor, because it affects only the stated magnitudes, not the direction.
- **Confidence:** 5 for the arithmetic; 3 for the direction of the net bias.

### B10. Intersectional testing: undefined test family, pairwise t-tests instead of a factorial model, and one contrast looks borderline
- **Quote:** "When performing independent t-tests with a Bonferroni correction, we find that all pairwise groups are statistically different (p <0.01), except for the light-yellow and dark-red skin colors."
- **Location:** §4.2.1; Fig. 3c.
- **Problem:**
  - The Bonferroni family is not stated. It could be the 6 intersectional pairs, or all 8 tests in Fig. 3.
  - Six pairwise t-tests on a 2 × 2 layout do not test the question the paper cares about: whether hue adds information beyond tone. That needs a model with tone, hue and their interaction (plus covariates, B4).
  - A rough reconstruction from Fig. 3c (medians, with SD = IQR/1.349, Welch test) gives LR vs DR: diff ≈ 65, t ≈ 2.5, raw p ≈ 0.012, Bonferroni-adjusted p ≈ 0.07 (×6). That is not obviously below 0.01. This is figure-read and imprecise.
- **Fix:** Report exact test statistics and adjusted p-values, and fit tone × hue as a factorial (Bradley–Terry with an interaction term).
- **Severity:** Minor, because it is a rigour and clarity issue.
- **Confidence:** 2 for the borderline claim; 4 for the design point.

### B11. Top/bottom position, image geometry and the definition of a "win" are unreported
- **Quote:** "we concatenate both facial images vertically with a white space in between and preserve their aspect ratio"
- **Location:** §4.2.1.
- **Problem:**
  - The paper does not say whether the position (top or bottom) was randomised or counterbalanced within each of the 45 combinations. If, for example, the first-listed group were always on top, any positional preference of the saliency model would be aliased with group.
  - "Preserve their aspect ratio" leaves the relative scale of the two faces unspecified. This matters when CFD and CFD-India images differ in size (B4), and the authors themselves observed sensitivity to resizing.
  - How "kept" is decided (for example, whether the argmax saliency point falls in which half) and how ties are handled are not stated.
  - Whether the 500 pairs per combination were drawn with replacement is not stated. The model is deterministic, so duplicate pairs would replicate outcomes and inflate precision.
- **Fix:** Randomise or counterbalance position, include it as a covariate, and report the scaling rule, the win rule and the sampling scheme.
- **Severity:** Minor, as a reporting gap. It would become Major if position was not randomised.
- **Confidence:** 3.

### B12. "P2 slightly amplifying the bias" is half supported; generated-image measurement is not shown to be comparable
- **Quotes:**
  - "Table 2 shows that both StyleGAN3 and P2 are reproducing the skin color bias present in the FFHQ dataset, with P2 slightly amplifying the bias over the original dataset distribution."
  - Table 2 caption: "Both StyleGAN3 and P2 reproduce the skin color bias of FFHQ."
- **Location:** §4.1; Table 2.
- **Problem:** The tests below compare n = 10,000 generated images with FFHQ n = 70,000 (`checks_B.py`).
  - **StyleGAN3:** every margin and cell is within ±0.25 pp of FFHQ (red −0.11 pp, z = −0.27; dark −0.25 pp, z = −0.49), and the 4-cell χ² goodness-of-fit gives p = 0.86. The 95% CIs are about ±0.8–1.0 pp. "Reproduce" is supported as approximate equivalence.
  - **P2, hue:** red is +1.50 pp (CI +0.77 to +2.23; z = 3.7–3.9, p ≈ 1–3×10⁻⁴), which is amplification on hue.
  - **P2, tone:** dark is **+0.96 pp** (z = 1.9–2.0, p ≈ 0.04–0.06), i.e. *less* light-skewed than FFHQ.
  - **P2, dark-yellow:** 4.62 vs 4.68, no change.
  - P2's 4-cell χ² gives p = 2×10⁻⁴. So P2 differs from FFHQ, but it does not uniformly "amplify".
  - Differences of 1–1.5 pp are also within reach of measurement artefacts that are not addressed:
    - The mask source for generated images is unreported. They have no ground-truth masks, so a predicted mask is needed.
    - Output resolution is not stated. P2's FFHQ model is, to my knowledge, 256 px, vs 1024 px FFHQ, and the histogram-mode estimator is resolution-sensitive.
    - Sampling settings (StyleGAN3 truncation ψ; P2 sampling steps) and seeds are not given. Truncation below 1 directly inflates majority cells.
- **Fix:**
  - Add CIs and tests for the generated-vs-FFHQ differences.
  - Reword as "P2 amplifies the red-hue share but slightly reduces the light-tone share".
  - Measure FFHQ and generated images with the same mask model at the same resolution.
  - Report ψ and steps, and use several seeds.
- **Severity:** Minor, because the gross "reproduce" claim survives and only the "amplifying" nuance is wrong.
- **Confidence:** 4.

### B13. Table 4: no paired tests or CIs, subgroup N not reported, and small changes are called increases "for all models"
- **Quote:** "Interestingly, manipulating the skin to be redder or darker in male sample results in a increase in accuracy for all models."
- **Location:** §4.3 Results; Table 4.
- **Problem:**
  - The design is paired (the same 30,000 images under each edit), but no McNemar tests or CIs are given, and F/M and S/NS counts are not reported.
  - The counts can be recovered from the margins: female share ≈ 0.631, so about 18,930 F / 11,070 M; smiling share ≈ 0.470.
  - The large effects clearly survive. For example, AWS male accuracy 94.82 → 90.66 under +light is about 4.2 pp on about 11,000 images (z ≈ 14 even unpaired).
  - The "+red increases male accuracy for all models" claim, however, includes AWS at +0.06 pp, about 7 net images out of about 11,070. Azure is +0.21 pp (about 23 images), FairFace +0.19 pp, Clarifai +0.58 pp. Whether these are significant depends on discordant-pair counts, which are not shown.
  - Commercial API versions and query dates are not recorded ("we use their latest available version"), so the comparisons cannot be reproduced.
- **Fix:** Report group N, McNemar tests with discordant counts, paired bootstrap CIs, and API version and date.
- **Severity:** Minor, because the headline effects are large; only secondary claims are overstated.
- **Confidence:** 4.

### B14. Table 4a has three "All" cells inconsistent with their F/M cells; FairFace +red and +yellow appear swapped
- **Quote:** Table 4a rows "AWS … 98.84 97.73 98.27 …" and "FairFace … 99.52 93.10 96.97 99.42 92.77 97.16".
- **Location:** Table 4a (p. 8).
- **Problem:**
  - Every other column of every model implies the same female share, w = (All − M)/(F − M) ∈ [0.631, 0.632], allowing for rounding.
  - AWS +dark implies w ∈ [0.477, 0.495]. The expected All is 0.631·98.84 + 0.369·97.73 = 98.43, but 98.27 is reported. Either M (it would be 97.30) or F (98.59) or All is mis-transcribed.
  - FairFace +red implies w = 0.60 and +yellow implies w = 0.66. The expected values are +red All = 97.15 and +yellow All = 96.97, while the reported values are 96.97 and 97.16. That pattern is a swap.
  - (Table 4b is fully consistent, with smiling share 0.47 throughout.)
- **Fix:** Recompute the table from raw predictions.
- **Severity:** Minor, because none of these cells drives a headline claim. Together with B2, though, they indicate transcription errors across tables.
- **Confidence:** 4.

### B15. Tone and hue are strongly associated in every in-the-wild dataset (but not in CFD), which contradicts the "orthogonal" framing
- **Quote:** §A.2: "which confirms that it provides complementary and orthogonal information about skin color than the skin tone"
- **Location:** §A.2 (based on one relit face, Fig. S3); Tables 1 and 2.
- **Problem:**
  - The odds of "red" given light vs dark are:

    | Dataset | Odds ratio | χ² p |
    |---|---|---|
    | CelebAMask-HQ | 0.56 | ≈ 10⁻⁸⁶ |
    | FFHQ | 0.63 | ≈ 10⁻⁹⁶ |
    | StyleGAN3 | 0.66 | |
    | P2 | 0.68 | |
    | CFD | 0.96 | 0.86 |

  - Darker in-the-wild images are measured as redder. The fact that controlled-capture CFD shows no such association suggests the coupling comes from acquisition: low light and colour casts (see Fig. S1, where the low-light example has h\* = −14.7).
  - The highlighted "under-representation of dark-yellow" is partly this association. CelebA DY is 6.29% observed vs 8.63% under independence; FFHQ 4.68% vs 6.11%.
  - One relit face (Fig. S3) cannot establish orthogonality.
- **Fix:** Report the correlation between L\* and h\* per dataset, and stop calling the scores "orthogonal". Separate population association from measurement coupling, for example with relighting at scale.
- **Severity:** Minor, as an interpretation issue.
- **Confidence:** 4.

### B16. Out-of-range hue values are silently binned as "red"
- **Quotes:** "h∗ = arctan (b∗/a∗)"; "whereh∗ goes from 0 to 360◦"; Fig. S1 values "h∗=− 25.38", "h∗=− 14.70", "h∗=− 0.70", "h∗=− 4.22".
- **Location:** Eq. (2); §4.1; Fig. S1.
- **Problem:**
  - arctan(b/a) returns values in (−90°, 90°), not 0–360°. The atan2 function is needed for the stated range.
  - The binary rule "yellow if h\* > 55°, otherwise red" counts every colour-cast, low-light, makeup or flushing failure, including the negative-h\* examples in Fig. S1, as "red".
  - The number of such images is not reported, so the red margins in Tables 1 and 2 are inflated by an unknown amount. Low-light failures also carry low L\*, which inflates dark-red specifically.
- **Fix:** Use atan2, define a validity domain (for example 0° < h\* < 90° and minimum chroma), report the exclusion counts, and recompute Tables 1 and 2.
- **Severity:** Minor, because it is probably a few percent at most. It is still a measurement-validity gap.
- **Confidence:** 3.

### B17. The FFHQ "ground truth" masks are model predictions by the paper's own account; the mask source differs across datasets
- **Quotes:** "Both datasets provide ground truth segmentation masks of the skin"; "We extract the skin masks with DeepLabV3 [11], trained on CelebAMask-HQ [43] as done in FFHQ-Ageing [52]."
- **Location:** §4.1 vs §4.2.1.
- **Problem:**
  - The second sentence states that FFHQ-Ageing's masks come from DeepLabV3. CelebAMask-HQ masks are manual.
  - Table 1 therefore compares datasets whose skin pixels were selected by different procedures. Table 2 compares FFHQ (predicted masks) with generated images (mask procedure unreported).
  - Mask boundary differences (hair, beard, lips) shift the L\* and h\* modes.
- **Fix:** Correct the wording. Apply one mask model to all compared sets, or report the agreement between manual and predicted masks on CelebAMask-HQ.
- **Severity:** Minor.
- **Confidence:** 4.

### B18. Table 1(b) rounding inconsistency
- **Quote:** FFHQ "Hue Red 52.82 29.06 81.87" and "Yellow 13.44 04.68 18.12".
- **Location:** Table 1(b).
- **Problem:**
  - 52.82 + 29.06 = 81.88, not 81.87.
  - Red ∈ [81.865, 81.875) and yellow ∈ [18.115, 18.125) sum to less than 100.00, so the two cannot both be correctly rounded complementary shares. The cause is either truncation or some unclassified images.
  - Every other margin in Tables 1 and 2 is exact, and all cells map to integer counts: 14,085/5,784/8,244/1,887 of 30,000; 36,974/20,342/9,408/3,276 of 70,000; 5,305/2,871/1,346/478 and 5,329/3,008/1,201/462 of 10,000.
- **Fix:** Report counts and state whether any images were unscorable.
- **Severity:** Minor.
- **Confidence:** 5.

### B19. LFW preprocessing is unreported; scikit-learn defaults would make the hue analysis impossible, and the model accuracies suggest degraded inputs
- **Quote:** "We rely on the pre-processed version of LFW available in scikit-learn [54]"
- **Location:** §4.2.2.
- **Problem:**
  - The defaults of `fetch_lfw_pairs`, as I recall them, are color=False (grayscale), resize=0.5, and a fixed slice_ crop of about 125 × 94 px, which becomes about 62 × 47 px. With the defaults, h\* cannot be computed at all, so non-default settings must have been used, and they are not reported.
  - The resulting crops are tiny and tightly cropped. Skin segmentation and L\*/h\* estimation on such crops are unvalidated.
  - ArcFace at 95.20%, far below its usual LFW accuracy of about 99.5% or higher, indicates that the models were run in a degraded regime. Group gaps measured there may not describe the models as deployed.
- **Fix:** Report the loader arguments, use full-resolution aligned LFW images, and report baseline accuracy against published values.
- **Severity:** Minor, as a reporting and external-validity issue (B1 already sinks the claim).
- **Confidence:** 3.

---

## Strengths (with anchors)

1. **The cropping hue contrast is tone-balanced.** The Fig. 3 group sizes give 61.7% vs 62.7% light within the red vs yellow groups (OR 0.96). The marginal hue gap is therefore not an artefact of binary tone composition, and Fig. 3c shows hue gaps *within* each tone stratum. Reporting the n per box is what makes this check possible.
2. **The cropping benchmark is stratified by design.** It uses 45 gender × ethnicity combinations with 500 games each, preserves aspect ratio after an observed resizing artefact, and reports a per-face score rather than a single aggregate. Together these are an improvement over two-group designs (§4.2.1).
3. **Reconstruction is used as the counterfactual baseline in Table 4.** Comparing edits with the e4e reconstruction rather than the original isolates the effect of the edit from reconstruction artefacts (§4.3, "we compare the performance of manipulated images with the reconstructed version rather than the original one"). The paired design on the same 30,000 images is efficient.
4. **Table 4 reports accuracy by class.** Splitting by class (F/M, S/NS) shows the *direction* of errors, for example that lighter tone shifts predictions towards "female", which an overall accuracy figure would hide.
5. **Tables 1 and 2 are arithmetically sound and well powered.** All cells sum correctly and map to integer counts at the stated N (one 0.01 slip, B18). Sampling error is negligible at N = 30,000 and 70,000. The StyleGAN3-vs-FFHQ comparison supports equivalence to within about ±1 pp.
6. **The tables are almost fully reconstructible.** Table 3 (Dlib exactly; FaceNet to within 0.01) and Table 4b are internally consistent. That consistency is what allowed recovery of the subgroup sizes and detection of B2 and B14.
7. **Threshold dependence is partly acknowledged.** §A.4 and Fig. S6 go beyond binary thresholds with histograms, and Fig. S3 and §A.1 discuss illumination and acquisition effects.

# Scan C: Causal/counterfactual design, generalisation, reproducibility and ethics

Paper: "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color" (Thong, Joniak, Xiang; arXiv 2309.05148v2).
Sources: the pypdf text (`run/manuscript.txt`) and the rendered pages p7, p12, p13 and p14.
Quotes are verbatim. I only normalised the pypdf spacing around symbols such as L*, h* and D.

**Reviewer-computed numbers.** Every delta below comes from the L*/h* values the authors print in Figure 4 (p.7). A few items are marked "crude". Those are my own corner-patch colour measurements on the rendered PDF page (`deepdive/fig4_bg.py`). They are indicative only, because the page went through PDF rendering and compression.

## Summary

| # | Title | Severity | Conf. |
|---|---|---|---|
| C1 | Edit directions not shown to be specific to skin colour. The gender and smile "causal" findings are fully explained by entanglement | **Critical** | 4 |
| C2 | The paper's own manipulation-check numbers contradict the "orthogonal / independent control" claim, and the check covers only n=3 | Major | 5 |
| C3 | Edit magnitude ("dose") unreported and asymmetric. No dose-response, so tone and hue effects cannot be compared | Major | 4 |
| C4 | CelebA gender/smile labels assumed unchanged after editing (label validity) | Major | 4 |
| C5 | Global photometric confound (exposure, white balance, non-skin regions). The contrast control in A.2 is a weak control | Major | 4 |
| C6 | Reconstructed baseline: a good idea, but original-image accuracy and reconstruction fidelity are not reported, and reconstruction itself shifts skin colour | Minor | 4 |
| C7 | No uncertainty or paired analysis in Table 4. Sub-1-point differences are over-read | Minor | 5 |
| C8 | Estimand and causal language overstated. Average over a 74%-light population, with no heterogeneity analysis | Minor | 4 |
| C9 | Commercial-API protocol: no dates, versions, thresholds or face-detection-failure handling | Minor | 4 |
| C10 | "Additional" hue bias in the observational benchmarks is confounded with tone, ethnicity and colour cast. Incremental validity not shown | Major | 4 |
| C11 | Face-verification design: degraded LFW variant, undefined pair-level grouping, accuracy only, no uncertainty | Major | 4 |
| C12 | Generalisation from a narrow evidence base to "datasets and models" and "data collection to model deployment" | Major | 4 |
| C13 | Dataset-skew claims are relative to transplanted thresholds with no reference distribution. The P2 "amplification" claim is contradicted by Table 2 | Major | 4 |
| C14 | Hue validity in the wild: robustness tested only under achromatic relighting of one face, while S1 shows colour cast moves h* by tens of degrees | Major | 4 |
| C15 | Section 4.3 pipeline is under-specified (classifier, SVM, latent space, alpha, conditioning, checkpoints, seeds). Release scope unclear | Minor | 5 |
| C16 | Skin-score and generation details missing or inconsistent ("ground truth" FFHQ-Ageing masks, h* range, CIELAB conversion, K-means, sampling settings) | Minor | 4 |
| C17 | Cropping benchmark: Elo is order-dependent, t-tests run on interdependent ratings, model version not given | Minor | 3 |
| C18 | Hue measure increases ethnicity separability, so race-proxy and sensitive-inference risk is unaddressed in the dataset-collection recommendation | Major | 3 |
| C19 | Editing skin colour of identifiable real people, plus dual use of skin-colour editing directions | Minor | 4 |
| C20 | Data governance for submitting about 150k non-consented web images to three commercial APIs | Minor | 3 |
| C21 | Gender framing ("more feminine") and racialised colour vocabulary ("yellow" for Asian subjects) | Minor | 4 |

Counts: **1 Critical, 10 Major, 10 Minor** (21 findings).

---

## Strengths (anchored)

- **ST1. Reconstruction-matched comparison.** "we compare the performance of manipulated images with the reconstructed version rather than the original one in Table 4" (p.8). This correctly removes inversion error from the contrast. It is the right baseline for a latent-edit design.
- **ST2. "Pale" attribute as a comparison direction.** "The same does not hold when selecting the "pale" attribute available in CelebA [44] as a comparison" (p.8). Showing that an off-the-shelf attribute direction moves both L* and h* is a useful negative-control style check. It also motivates purpose-built directions (the check is limited; see C2).
- **ST3. Class-disaggregated results.** Reporting F/M and S/NS separately in Table 4 shows the *direction* of decision shifts: male accuracy falls under +light, and NS accuracy falls under +red. This is much more informative than overall accuracy and is what makes the "toward female / toward smiling" reading possible.
- **ST4. Interventional design instead of only observational breakdowns.** "We are inspired by the idea of transects [4] to reveal causal effects by manipulating one particular property in the image at a time" (p.7). This is the right instinct for separating skin colour from identity-correlated attributes. It is also applied to commercial and open models.
- **ST5. Candid limitations and nuisance checks.** "A current limitation of this setup lies in the image reconstruction and manipulation methods, which struggle with spurious correlations" (p.8). Other good points: the A.2 contrast analysis, the S3 relighting check, and the explicit apparent-vs-true colour scoping (p.2, A.1).
- **ST6. Controlled benchmark for cropping.** CFD/CFD-India images were acquired in a controlled setting with self-reported labels and informed consent ("Individuals have given their informed consent for data collection", p.5). Pairs were balanced over gender × ethnicity, and aspect ratio was preserved after the authors noticed resizing effects (p.6). The tone × hue intersectional tests use a Bonferroni correction.
- **ST7. Openness and ethical signposting.** There is a code URL (p.4). Dataset licences are stated (p.4–5). There is an explicit disclaimer that the authors "do not condone the gender classification task" (p.8). A.4 goes beyond binary thresholds with histograms.

---

## Part 1: Causal / counterfactual design (Section 4.3)

### C1. Edit directions are not shown to be specific to skin colour, and the headline gender and smile effects are fully explained by entanglement

- **Quote:** "we first train a classifier on CelebAMask-HQ [43] to predict the skin tone (light vs. dark) and skin hue (red vs. yellow)" and "Two linear SVMs, one for skin tone and one for skin hue, are finally trained on the most confident positive and negative predictions" (p.7). Conclusion drawn: "In gender classification, models classify individuals as more feminine when their skin tone becomes lighter. (b) In smile classification, models classify individuals as smiling when their skin tone becomes lighter or when their skin hue becomes redder." (Table 4 caption, p.8).
- **Location:** §4.3 Method (p.7); Table 4 and Results (p.8–9); Fig. 4.
- **Problem:**
  1. **The labelling classifier can learn any correlate of skin colour.** It sees the *whole image*, and its labels are thresholded skin L*/h* values. Anything in CelebA-HQ that correlates with those labels is fair game:
     - gender-typed presentation (foundation/makeup, lipstick, beard and stubble shadow, hair length and colour);
     - age and skin smoothness;
     - photographic exposure and white balance (S1 shows colour cast and makeup move h* drastically);
     - expression.

     Apparent facial lightness is very plausibly higher for female-labelled CelebA images: makeup and foundation, studio and beauty lighting, and within-population sexual dimorphism in skin reflectance. The paper never reports L*/h* by CelebA "Male" or "Smiling" label, though it has all the data needed to do so.
  2. **The direction comes from standard (unconditioned) InterFaceGAN.** The latent direction is the SVM normal. The paper does not say whether InterFaceGAN's *conditional manipulation* was used, i.e. projecting the tone/hue normal orthogonal to the gender, smile, age, makeup and eyeglasses boundaries (n₁ − (n₁ᵀn₂)n₂). It does not even say whether the tone and hue normals were orthogonalised to each other.
  3. **Training only on the "most confident" extremes makes entanglement worse.** The most confidently "light" StyleGAN3 samples will be over-represented in female, made-up, young, brightly lit faces. The most confidently "dark" samples will be over-represented in male, bearded, shadowed, low-light faces. The SVM normal then loads onto those attributes.
  4. **The edits visibly change non-skin content.** Row 1 +dark/−pale darkens the hair from blonde to brown and darkens the eyebrows. Non-skin regions also shift (C5).
  5. **The departure from the cited method matters.** The cited transect approach [4] validated synthesised images with human annotation and attribute-orthogonal directions. No equivalent validation is done here.
- **Consequence:** A tone direction that partly encodes "femaleness" would make every gender classifier predict "female" more often under +light and "male" more often under +dark. That is exactly the pattern in Table 4a: male accuracy falls 4–6 points, rises 3–6 points under +dark, and female accuracy is at ceiling. This would happen *even if the classifiers ignored skin colour entirely*.

  The smile result has the same problem. A "red" direction that adds blush or rosy cheeks, raised cheeks or lip-corner changes, which co-occur with smiling in portrait photos, would produce Table 4b. The Azure NS drop of 80.84 → 69.76 for a hue shift of roughly 10–14° is the largest effect in the table, which is a warning sign of semantic rather than purely chromatic change.

  So the core claim (iii), "measuring the causal effect of skin color in attribute prediction" (p.2), and both directional conclusions are **not identified**. The estimate is the effect of "moving along a CelebA-learned latent direction", not the effect of skin colour.
- **Fix / discriminating controls:**
  - (a) Report cos(D_tone, n_gender), cos(D_tone, n_makeup / n_beard / n_age / n_smile), cos(D_hue, n_smile / n_makeup / n_lipstick / n_rosy_cheeks) and cos(D_tone, D_hue), using InterFaceGAN boundaries trained the same way.
  - (b) Re-run with **conditional manipulation** that projects out gender, smile, age, makeup and facial hair (and the other colour axis). Show whether the Table 4 effects survive.
  - (c) Score every edited image with an independent attribute panel: a CelebA-40 attribute classifier (Male, Heavy_Makeup, Wearing_Lipstick, No_Beard, 5_o_Clock_Shadow, Young, Rosy_Cheeks, High_Cheekbones, Mouth_Slightly_Open, Smiling). Add an action-unit / landmark analysis: AU6/AU12 intensity, mouth-corner displacement and mouth aspect ratio. Report the mean change per edit.
  - (d) Add a **pixel-space, skin-mask-only counterfactual**: shift L* or h* only inside the skin mask with feathered blending, holding geometry, hair, lips and background fixed. Estimate the classifier response per unit ΔL*/Δh* and compare it with the latent edit. If the latent effect far exceeds the masked-recolour effect at matched ΔL*, the excess is entanglement.
  - (e) Add negative-control edits: random latent directions with the same norm, and a background-only brightness direction. These calibrate how much an arbitrary edit of this size moves each classifier.
  - (f) Run a human perception study (blinded) on perceived gender and smile for a sample of edited images (see C4).
- **Proposed severity:** **Critical**. One unaddressed alternative (entanglement) predicts the exact observed sign pattern, so on its own it invalidates the causal interpretation of the headline 4.3 findings.
- **Confidence:** 4 for gender, where the prior for a tone–gender correlation in CelebA is strong; 3 for smile.

### C2. The manipulation check is limited to 3 faces, and its own numbers contradict "orthogonal / independent control"

- **Quote:** "Modifying the image in one direction does not affect the skin color score in the other direction, making them orthogonal." (p.8). "As such, our proposal (c-f) is better for measuring the multidimensional causal effect of skin color as we have an independent control over L* and h*." (Fig. 4 caption, p.7).
- **Location:** Fig. 4 (p.7); §4.3 (p.8).
- **Problem:** The only manipulation check is L*/h* on three faces. Off-axis shifts computed from the printed values, relative to the reconstructed image:

  | Face | +light ΔL* / Δh* | +dark ΔL* / Δh* | +red Δh* / **ΔL*** | +yellow Δh* / **ΔL*** | +pale ΔL* / Δh* | −pale ΔL* / Δh* |
  |---|---|---|---|---|---|---|
  | Row 1 | +9.82 / −1.00 | −13.72 / −0.07 | −10.00 / **+2.17** | +8.51 / −0.42 | +7.64 / +1.11 | −7.01 / −3.22 |
  | Row 2 | +14.30 / −1.37 | −20.65 / **+3.52** | −12.87 / **+7.62** | +6.94 / **+2.27** | +16.05 / +7.36 | −16.88 / −8.60 |
  | Row 3 | +5.28 / −0.08 | −9.75 / +0.88 | −13.80 / −0.81 | +10.36 / **+3.77** | +8.45 / +3.51 | −10.75 / −4.26 |

  - The tone direction is fairly clean in the L*–h* plane.
  - The **hue direction is not**:
    - Row 2 +red raises L* by 7.6, which is more than the whole +light effect on row 3 (+5.3).
    - Row 3 +yellow raises L* by 3.8, about 70% of that face's +light effect.
  - The off-axis/on-axis ratio for row 2 +red (0.59) is as large as for the "pale" direction the paper rejects as entangled (0.42–0.51 on rows 2–3, 0.15 on row 1 +pale). L* units and degrees are not commensurate, but this is the paper's own framing.

  Chroma C* is never reported. A "red" edit can change saturation, which is a third colour dimension classifiers may use. There is no dataset-level check over the 4 × 30,000 edited images: no distribution of ΔL*, Δh*, ΔC*, no fraction moved in the intended direction, and no stratification by gender or label. The paper also does not say which masks were used to measure skin on edited and reconstructed images (original GT masks can misalign after inversion).

  This direction-dependent L* leakage also fits the data. In CelebA-HQ, P(light | yellow) = 27.48/33.77 = 0.81 while P(light | red) = 46.95/66.23 = 0.71 (Table 1a), so an unconditioned hue direction inherits tone loading.
- **Consequence:** The claims of "independent control" and of superiority over "pale" rest on n=3 and are partly contradicted. Hue effects in Table 4 (for example +red → smiling, and the role of +red in the gender result) may be partly lightness effects.
- **Fix:** Report dataset-level manipulation checks: mean ± SD and the full distribution of ΔL*, Δh*, ΔC* for each edit, overall and by gender and smile label. Report cross-talk regressions, and ΔL*/Δh* for "pale" on the same 30k images. Orthogonalise D_hue against D_tone and verify. State the measurement masks used.
- **Proposed severity:** Major. It directly undercuts the stated advantage of the method and needs a new dataset-level analysis.
- **Confidence:** 5 for the arithmetic; 4 for the interpretation.

### C3. Edit magnitude is unreported and asymmetric, with no dose-response

- **Quote:** "Modifying x then consists of moving in the latent space towards specific and meaningful directions D, i.e., w + D." (p.7). "the skin hue does not seem to have a large effect" (p.8).
- **Location:** §4.3 Method and Results.
- **Problem:**
  - The step size α (or ‖D‖) is never given. It is not stated whether the same α was used for all images and directions, which latent space or layers were edited (e4e for StyleGAN3 outputs W+), or whether ±α were symmetric.
  - Achieved effects vary roughly 2.7× across faces: +light ΔL* = 9.8 / 14.3 / 5.3.
  - Effects are systematically asymmetric. |ΔL*| for +dark averages 14.7 versus 9.8 for +light (larger in all 3 faces). |Δh*| for +red averages 12.2 versus 8.6 for +yellow (larger in all 3).
  - A uniform α applied to already-light faces can push them out of distribution (row 3 +pale reaches L* = 80.6), where artefacts rather than colour may drive errors.
- **Consequence:**
  - "+light vs +dark" and "tone vs hue" effect sizes are not comparable. "Hue does not have a large effect on gender" could just mean the hue step was smaller in perceptual or natural-variation units.
  - Asymmetric doses make the apparent asymmetries in Table 4 uninterpretable.
  - No dose-response means no evidence of a monotone, graded (causal-looking) relation.
- **Fix:** Report α and ‖D‖. Sweep α over several values in both directions. Plot accuracy and flip rate against **achieved** ΔL*/Δh*, standardised to the natural SD of L*/h* in CelebA-HQ. Report slopes (Δaccuracy per SD) with CIs. Add an image-quality/realism metric per α (FID or no-reference IQA).
- **Proposed severity:** Major. Without dose, the comparative and directional claims cannot be interpreted, and fixing it needs new experiments.
- **Confidence:** 4.

### C4. Ground-truth labels are assumed to survive editing (label validity)

- **Quote:** "We focus on gender and smile classifications, as both attributes can be predicted with the above systems and come with ground truth labels annotated by a professional company in the CelebA dataset [44]." (p.8)
- **Location:** §4.3; Table 4.
- **Problem:** Edited (and reconstructed) images are scored against the CelebA labels of the *original* photo. If an edit changes expression (C1: +red/+light may raise cheeks or lip corners) or perceived gender presentation (makeup, facial hair, hair), the "correct" label for the edited image may differ. A "misclassification" may then be a correct response to a real semantic change.

  Reconstruction already changes semantics. In Fig. 4, row 1 loses the earring, row 3's dark plum lipstick becomes red and the gaze changes, and row 2's clothing and background change. CelebA "Smiling" is also a noisy, borderline-heavy label, so small expression changes near the boundary flip ground truth easily.
- **Consequence:** Table 4 accuracy changes can't be read as model bias. They may be label drift caused by the intervention, which is the exact mechanism behind C1.
- **Fix:** Have blinded human raters re-annotate a stratified random sample of reconstructed and edited images (perceived smile and perceived gender presentation; the gender framing caveat is in C21), and report agreement with the CelebA labels per condition. Use an AU12/landmark-based smile measure as an objective check. Report results restricted to images whose re-annotated label is unchanged. Alternatively, use agreement with the model's own prediction on the reconstructed image (flip rate) as the primary outcome, since that does not need the label to survive.
- **Proposed severity:** Major. The outcome measure itself may be invalid under the intervention, and fixing it needs new annotation.
- **Confidence:** 4.

### C5. Global photometric confound: the edit may act through exposure or white balance rather than skin colour, and the contrast control is a weak control

- **Quote:** "Manipulating images has an effect on the overall contrast." and "Figure S4 shows that image contrast should not be conflated with the skin tone." (A.2, p.14).
- **Location:** A.2 "Contrast" (p.14); Fig. S4 (p.13); Fig. 4.
- **Problem:**
  - The authors themselves find global RMS contrast changes (0.644 → 0.652 for +light, 0.630 for +dark).
  - The comparison control (plain pixel scaling) is a weak control. It clips highlights (L* 91.74, h* 14.05) and is obviously unrealistic, so its *difference* from the latent edit says nothing about whether the latent edit acts partly through global exposure or colour temperature.
  - My crude corner-patch measurements of Fig. 4 suggest non-skin regions move:
    - Row 1, uniform beige wall: background b* goes 9.5 → 6.5 under +red and → 11.7 under +yellow, i.e. the background hue shifts *with* the skin hue, consistent with a white-balance component.
    - Row 2: background L* goes 72.8 → 81.0 under +dark and → 64.7 under +light.
    - Row 1 +dark: the hair visibly darkens.
  - Since the hue classifier was trained on labels contaminated by colour cast (S1a: h* = −25°), a white-balance component in D_hue is expected.
- **Consequence:** "Lighter skin → more female" or "redder → more smiling" may in part be "brighter / warmer photo → …". That is a different finding, about photographic sensitivity rather than skin colour.
- **Fix:**
  - For every edit, report ΔL*, Δa*, Δb* in **non-skin** regions (background, hair, clothing) using segmentation, not only on skin.
  - Add matched photometric controls: global gamma/exposure and global white-balance shifts tuned to produce the *same* skin ΔL*/Δh* as each latent edit. Pair them with skin-mask-only recolouring (C1d).
  - Compare classifier responses across the three interventions (latent, global, skin-only). This separates skin-specific from global effects.
- **Proposed severity:** Major. A plausible alternative mechanism is untested, and the existing control does not tell the two apart.
- **Confidence:** 4 for the logic; 2–3 for my figure-based measurements.

### C6. The reconstructed baseline is a strength, but the original-image accuracy and reconstruction fidelity are missing

- **Quote:** "To avoid capturing performance discrepancies due to imperfect reconstruction, we compare the performance of manipulated images with the reconstructed version rather than the original one in Table 4." (p.8)
- **Location:** §4.3; Table 4; Fig. 4.
- **Problem:**
  - Accuracy on the *original* CelebA-HQ images is never reported, so we can't see how much inversion alone moves each classifier.
  - Reconstruction is itself a skin-colour intervention of similar size to the edits. Row 1: ΔL* = −5.37, Δh* = +4.04 (comparable to +light on row 3, +5.28). Row 3: Δh* = −3.11.
  - Reconstruction also drops accessories, changes lip colour and alters gaze (Fig. 4).
  - e4e (trained on FFHQ) may reconstruct darker or atypical faces less faithfully, so the baseline population may already be shifted unequally by skin colour.
  - No fidelity metrics are reported (ID similarity, LPIPS, prediction agreement between original and reconstructed).
- **Consequence:** The reference condition is not a neutral "same people" point. Effects are conditional on an unquantified distribution shift, and possibly a skin-colour-dependent one.
- **Fix:** Report accuracy on original, reconstructed and edited images. Report per-image fidelity and original↔reconstructed prediction agreement, stratified by baseline L*/h* and gender. Add a sensitivity analysis restricted to images whose prediction is unchanged by reconstruction.
- **Proposed severity:** Minor. It improves interpretability but probably does not overturn the direction of effects on its own.
- **Confidence:** 4.

### C7. No uncertainty or paired analysis in Table 4, and very small differences are over-read

- **Quote:** "Interestingly, manipulating the skin to be redder or darker in male sample results in a increase in accuracy for all models." (p.9)
- **Location:** Table 4; Results (p.8–9).
- **Problem:**
  - Cell sizes (number of F/M and S/NS images) are not given.
  - There are no CIs and no tests, even though the design is perfectly paired (same image, 5 conditions).
  - The "redder → higher male accuracy for all models" increases are +0.06 (AWS), +0.21 (Azure), +0.58 (Clarifai) and +0.19 (FairFace) points. With about 11k male images these are at or within roughly one binomial SE (~0.2–0.35 pts), and the paired SE is unknown.
  - "Hue does not seem to have a large effect" is a null claim made without any equivalence test.
  - Accuracy hides two-way flips. For the smile classifiers, Azure's output is a continuous score, so score shifts are more sensitive and threshold-free.
- **Consequence:** Secondary claims are unsupported. The large effects (male −4 to −6 pts under +light; Azure NS −11 pts under +red) probably survive, but this is not shown.
- **Fix:** Report n per cell. Report paired flip-rate matrices (M→F and F→M per condition) with McNemar tests, or a paired bootstrap over images for Δaccuracy. Report mean score/confidence shifts. Use TOST equivalence bounds for the "no effect" statements, and correct for multiple comparisons across models × conditions × classes.
- **Proposed severity:** Minor. Headline effects likely survive, the fix is cheap, and only the secondary sentences need removing or testing.
- **Confidence:** 5 that uncertainty is missing; 4 that the "all models" sentence is within noise.

### C8. Estimand and causal language are overstated, and heterogeneity is not analysed

- **Quote:** "Any discrepancy would then corresponds to the effect of a bias towards light skin tone in the model." (p.7); "(iii) measuring the causal effect of skin color in attribute prediction" (p.2).
- **Location:** §1 contributions; §4.3 Task.
- **Problem:**
  - The estimand actually measured is the population-average effect, over CelebA-HQ (74.4% light, 66.2% red), of moving w by a fixed latent step. The paper calls it "the causal effect of skin color" and labels it "bias towards light skin tone".
  - A change in accuracy shows that predictions *depend on* the edited features. It does not by itself show a bias *favouring* a group. For example, +dark *raises* male accuracy.
  - There is no stratification by baseline L*/h*, gender or label. Effects could be heterogeneous, for instance larger for faces near the tone threshold, or artefact-driven for faces pushed out of range.
- **Consequence:** Readers may take a dataset- and generator-specific average treatment effect of a bundled intervention as a general causal property of skin colour. The fairness meaning (who is harmed in deployment) is not established.
- **Fix:** Define the estimand formally (intervention, population, outcome). Report conditional effects by baseline skin-colour bin and gender. Rephrase as "sensitivity of predictions to a latent skin-tone/hue edit". Connect to harm by showing how the sensitivity maps onto real darker-skinned female errors (for example on CFD or another dataset with real skin-colour variation).
- **Proposed severity:** Minor. This is framing and analysis rather than new data, though it overlaps with C1.
- **Confidence:** 4.

### C9. Commercial-API protocol not reported: dates, versions, thresholds, detection failures

- **Quote:** "we use their latest available version for attribute prediction." (p.8)
- **Location:** §4.3 Benchmarking (p.8); refs [3], [14], [49].
- **Problem:**
  - No query dates, API versions or model identifiers are given (e.g. Rekognition face-model version, Azure detection/attribute model, Clarifai model ID).
  - Ref [14] points to a Clarifai *face-detection* model page, so which Clarifai model produced the gender predictions is unclear.
  - No decision thresholds are given. Azure smile is a score, and the S/NS asymmetry (97.29 vs 80.84) suggests the threshold strongly affects the results.
  - It is not said how failed face detections were counted (as errors, or dropped). Detection rates may differ by condition, e.g. under +dark, and could explain the small female-accuracy drops under +dark (Clarifai 95.31 → 93.04).
  - To this reviewer's knowledge, Microsoft retired Azure Face's gender/age/smile and other attribute inference (new customers in June 2022, existing customers by mid-2023). If so, the Azure results can no longer be reproduced, and readers need the query date.
- **Consequence:** The commercial-system findings can't be verified or reproduced. Denominators may differ across conditions.
- **Fix:** Report query dates, versions, endpoints and parameters, thresholds, and per-condition detection-failure counts with the rule used. Archive the raw API responses with timestamps. Run a sensitivity analysis with failures counted as errors versus dropped.
- **Proposed severity:** Minor. This is reproducibility and transparency; it does not invalidate the claims as of the query date.
- **Confidence:** 4 that the information is missing; 3 on the Azure retirement detail.

---

## Part 2: External validity and generalisation

### C10. "Additional" hue bias in the observational benchmarks is confounded with tone, ethnicity and colour cast, and incremental validity is not shown

- **Quote:** "The algorithm also prefers red skin hues over yellow ones with an average Elo score indicating a 58.25% preference" (p.6); "Complementary to the skin tone, the skin hue reveals additional differences in performance." (Fig. 3 caption, p.6).
- **Location:** §4.2.1 Fig. 3; §4.2.2 Table 3; A.3 Fig. S5.
- **Problem:** The red-vs-yellow comparisons are *marginal* contrasts on observational data, and hue is correlated with other things:
  - **Tone.** In CFD, S5 shows Black subjects darker *and* more yellow. In CelebA-HQ and FFHQ, yellow is lighter (Table 1: P(light | yellow) 0.81 vs 0.71 for red in CelebA-HQ; 0.74 vs 0.65 in FFHQ).
  - **Ethnicity.** In CFD, "Asian subjects ... are mostly in the yellow side of skin hue" (p.14).
  - **Colour cast** in the in-the-wild LFW images (C14).

  So the "red preferred" cropping result may partly be the tone effect, or a preference for faces with different ethnicity-associated morphology, rather than hue. The intersectional test does not settle this: light-yellow vs dark-red is not significant, and no model holds tone fixed while estimating hue with a CI. "Previously invisible" is asserted, not shown.
- **Consequence:** The central thesis, that hue reveals biases *beyond* tone, is not established by the observational benchmarks.
- **Fix:**
  - Fit joint models: logistic or Bradley–Terry regression of crop win on ΔL* and Δh* as continuous variables, with ethnicity and gender as covariates. Do the same for verification error.
  - Report the partial effect of h* with a CI, and a likelihood-ratio / ΔAIC test for adding h* to L*.
  - Analyse within ethnicity in CFD, e.g. White and Latino subjects, who span hue at similar tone.
  - Apply a counterfactual skin-only hue recolouring to CFD pairs to test hue causally in the cropping model.
- **Proposed severity:** Major. It bears directly on the paper's main contribution and needs reanalysis.
- **Confidence:** 4.

### C11. Face-verification design: a degraded LFW variant, undefined pair grouping, accuracy only, no uncertainty

- **Quote:** "We rely on the pre-processed version of LFW available in scikit-learn [54]" (p.6); "Individuals with a light skin tone or a red skin hue are better identified by all face verification models." (Table 3 caption, p.6).
- **Location:** §4.2.2; Table 3.
- **Problem:**
  - **Degraded inputs.** scikit-learn's `fetch_lfw_pairs` defaults to funneled, `resize=0.5`, a center `slice_`, and **grayscale** (`color=False`), giving roughly 62×47 crops. Colour must have been enabled for skin measurement, but none of these parameters are reported. Baseline accuracies (ArcFace 95.2%) are far below this model's usual LFW performance (~99.8%), which suggests a heavily degraded, atypical operating point. Skin segmentation and L*/h* on ~62×47 crops is also of doubtful reliability.
  - **Undefined grouping.** A *pair* has two images, and negative pairs have two people who may fall in different groups. How a pair is assigned to "light/dark/red/yellow" is not defined.
  - **Small cells, no uncertainty.** Cell sizes are not given (dark-yellow is ~5% of images in CelebA/FFHQ terms, so possibly a few dozen pairs here). There are no CIs.
  - **Over-generalised headline.** The "all models" claim rests on differences such as FaceNet light vs dark 94.55 vs 94.04 (0.5 pts on ≤1,000 pairs).
  - **Accuracy only.** Accuracy at DeepFace's default global thresholds mixes false match and false non-match rates, which group-composition differences can drive. Intersectional reversals (ArcFace dark-yellow is *best*, 96.77) are consistent with noise.
- **Consequence:** The claim of verification bias by hue (and by tone, for FaceNet) is not supported, and it would not generalise to realistic verification pipelines.
- **Fix:**
  - Specify the loader parameters and the DeepFace version, detector, alignment, metric and thresholds.
  - Use full-resolution LFW or a demographically richer benchmark (e.g. RFW, or Casual Conversations-style data with consent).
  - Define pair-level grouping (e.g. same-group pairs only).
  - Report FMR and FNMR per group at a fixed global threshold (NIST-style), with bootstrap CIs and cell counts.
- **Proposed severity:** Major. It weakens one of the three model-bias demonstrations, and a fix needs reanalysis or new data.
- **Confidence:** 4.

### C12. Generalisation from a narrow evidence base

- **Quote:** "the hue dimension reveals additional biases related to skin color in both computer vision datasets and models" (Abstract, p.1); "we recommend the usage of a multidimensional skin color measure as a fairness tool to assess the computer vision pipeline, from data collection to model deployment." (Conclusion, p.9).
- **Location:** Abstract; §4; §5.
- **Problem:** The evidence is narrow:
  - **Datasets:** two dataset skews, both web-sourced, aligned, frontal, high-resolution portrait sets (CelebA-HQ celebrities; FFHQ Flickr), plus two generators trained on one of them.
  - **Cropping:** one algorithm (Twitter's saliency cropper, a model Twitter already withdrew) on one controlled dataset.
  - **Verification:** three open verification models in one degraded LFW setting (C11).
  - **Attributes:** two attributes from four classifiers on one dataset, with one generator/encoder.
  - **Missing comparisons:** no comparison with alternative second dimensions (a*, b*, chroma C*, ITA, Monk) showing that h* specifically is the right extra axis, and no evidence that balancing on h* reduces downstream disparities.

  The A.3 argument that tone-only collection "would be enough" with White and Black subjects is a hypothetical. It does not show that tone-balanced datasets actually fail.
- **Consequence:** The general recommendation goes beyond what the data support.
- **Fix:** Either narrow the claims to the studied settings or add evidence:
  - more datasets with real skin-colour diversity and consent (e.g. CFD-style, Casual Conversations);
  - several cropping and saliency models;
  - in-the-wild non-face human-centric tasks if those are claimed;
  - an ablation showing h* adds predictive value for performance disparities beyond L* (and beyond a*/b*/C*);
  - a mitigation experiment showing hue-aware balancing reduces disparities.
- **Proposed severity:** Major. It materially limits the stated contribution. Rewording alone would bring it down to Minor.
- **Confidence:** 4.

### C13. Dataset-skew claims are relative to transplanted thresholds, and the "amplification" claim is contradicted by Table 2

- **Quote:** "Threshold values are taken from Ly et al. [46]." (p.4); "with P2 slightly amplifying the bias over the original dataset distribution" (p.5); "we recommend tracking both skin tone and skin hue for skin color scores, such that all subgroups are well balanced" (p.5).
- **Location:** §4.1; Tables 1–2; A.4.
- **Problem:**
  - **Transplanted thresholds.** L* = 60 and h* = 55° come from colorimetric (spectrophotometer/chromameter) skin measurement. They are applied to uncalibrated sRGB web photos of unknown white balance and exposure, with no calibration showing they mean the same thing.
  - **No reference distribution for hue.** For tone there is at least an informal external reference (world populations are darker than celebrity photos). For hue there is none, so "skewed towards red" and "under-represent dark-yellow" just mean the bulk of a unimodal distribution (A.4) falls below an imported cut-off.
  - **Table 2 contradicts the amplification sentence.**
    - P2 is *less* skewed in tone than FFHQ: light 65.30% vs 66.26%; dark 34.70% vs 33.74%.
    - P2 is more skewed in hue: red 83.37% vs 81.87%.
    - The dark-yellow cell is unchanged (4.62% vs 4.68%).
    - With n = 10,000 (SE ≈ 0.4 pts) and no generation settings (truncation ψ, sampler steps, seeds), the ~1.5-pt hue difference is weak evidence.
- **Consequence:** The "skew" and "amplification" findings are partly threshold artefacts. The data-collection recommendation ("well balanced" subgroups) has no defensible target.
- **Fix:**
  - Run a threshold sensitivity analysis: report the proportions over a grid of L*/h* cut-offs, or use quantile-free summaries.
  - Specify a reference population (e.g. measurements from a consented, diverse, calibrated capture set such as CFD) and report divergence from it.
  - Report CIs for the generated-sample proportions with sampling settings and seeds.
  - Correct the P2 sentence to "amplifies the hue skew but not the tone skew".
- **Proposed severity:** Major. It weakens contribution (i) and the dataset-collection recommendation, and needs reanalysis.
- **Confidence:** 4; 5 for the Table 2 contradiction.

### C14. Hue validity in the wild: robustness was tested only for achromatic relighting of one face

- **Quote:** "Interestingly, h* remains stable and robust to face relighting, which confirms that it provides complementary and orthogonal information about skin color than the skin tone." (A.2, p.13); "images in CFD have been captured in a controlled setting, enabling fair comparisons among images." (A.3, p.14).
- **Location:** A.2 Fig. S3 (one identity, 7 relightings); A.1 Fig. S1; §4.1–4.2.
- **Problem:**
  - **The robustness test cannot fail for hue.** The relighting model [81] changes only the direction and intensity of grey-scale shading (the S3 spheres are achromatic). Hue is close to invariant to intensity scaling by construction, so "h* is stable" is close to a tautology.
  - **The tested condition is not the one that matters in the wild.** That is illuminant colour, white balance and camera processing. S1 shows these move h* to −25° (colour cast) and to about 0° (makeup, flushing), shifts larger than the entire red/yellow range used in the paper.
  - **One stable case does not prove "orthogonal".** It does not establish orthogonality of the two dimensions in the population.
  - **CFD results do not transfer.** Validity was shown only in the controlled CFD setting, while the dataset and verification claims use in-the-wild images where h* is confounded with photographic white balance.
  - **The confound propagates into the causal pipeline.** Hue labels for the 4.3 classifier come from such images (see C5).
- **Consequence:** In-the-wild hue groups (CelebA-HQ, FFHQ, LFW) may partly reflect colour cast, which could explain hue-linked performance differences (e.g. poorly white-balanced LFW news photos).
- **Fix:**
  - Test robustness to chromatic illuminant changes (e.g. CCT 2700–6500 K) and camera white-balance variation, using a colour checker or a multi-illuminant capture of the same subjects.
  - Run a sensitivity analysis with colour-constancy preprocessing (gray-world or learned white balance) or background-referenced normalisation before computing h*.
  - Report the correlation between skin h* and a background/sclera colour-cast estimate, and repeat the Table 1/3 analyses after controlling for it.
- **Proposed severity:** Major. It undermines the interpretability of in-the-wild hue groupings and the transfer from CFD, and needs new analysis.
- **Confidence:** 4.

---

## Part 3: Reproducibility

### C15. The Section 4.3 manipulation pipeline is under-specified, and the release scope is unclear

- **Quote:** "Following Alahuf et al. [1], we rely on e4e [68] to encode images and on StyleGAN3 [37] to generate images." (p.7); "Code can be found at https://github.com/SonyResearch/apparent skincolor." (p.4).
- **Location:** §4.3 Method.
- **Problem:** The following are not specified:
  - **Tone/hue classifier:** architecture, input (whole image or masked), training split, held-out accuracy and calibration, and how it was applied to StyleGAN3 samples (domain shift from CelebA-HQ to FFHQ-trained StyleGAN3).
  - **Training data for the SVMs:** the number or percentile of "most confident" samples, SVM regularisation, and whether the boundaries were validated.
  - **Latent editing:** which latent space (Z/W/W+/S), which layers were edited, normalisation of D, α (see C3), and whether conditional manipulation was used (see C1).
  - **Generator and encoder:** StyleGAN3 configuration (T or R, aligned or unaligned FFHQ, 1024 px), truncation ψ for the 500k samples, seeds, the e4e/StyleGAN3 encoder checkpoint, and CelebA-HQ alignment to FFHQ alignment.
  - **Measurement masks:** which masks were used to measure L*/h* on edited images.

  It is also unclear whether the code release includes the learned directions, the classifier weights, the edited-image manifests, the raw API responses, the LFW pair-to-group assignments and the cropping game order.
- **Consequence:** The Table 4 results can't be reproduced or audited, which matters especially for the commercial APIs (C9).
- **Fix:** Add a reproducibility table with all of the above. Release the directions (D_tone, D_hue), the classifier, seeds, the edited-image IDs or images where licences allow, and the API outputs with timestamps.
- **Proposed severity:** Minor. This is reporting, though it is needed before others can test C1–C5.
- **Confidence:** 5.

### C16. Skin-score extraction and generation details are missing or inconsistent

- **Quote:** "Both datasets provide ground truth segmentation masks of the skin" (p.4) versus "We extract the skin masks with DeepLabV3 [11], trained on CelebAMask-HQ [43] as done in FFHQ-Ageing [52]." (p.5); "h* goes from 0 to 360°" (p.4) versus Fig. S1 "h*=−25.38" (p.12).
- **Location:** §3, §4.1, §4.2.1, A.2.
- **Problem:**
  - **"Ground truth" masks.** The FFHQ-Ageing masks are themselves DeepLabV3 predictions, which the paper's own wording implies, so they are not ground truth.
  - **Segmentation.** It is not said which CelebAMask-HQ classes count as skin (face skin, nose, neck, ears). The DeepLabV3 backbone, checkpoint and training details are missing.
  - **Colour conversion.** The sRGB → CIELAB conversion (white point D65/D50, linearisation, library) is not given.
  - **Clustering.** It is not said what K-means clusters on (L* only, or L*/h*/a*/b*), and the initialisation, seed and number of restarts are missing.
  - **Hue formula.** Negative h* values in S1 imply arctan rather than atan2, which contradicts "0 to 360°". This changes results for pixels with a* < 0.
  - **Sampling settings.** For Table 2 and the 500k samples, the StyleGAN3 and P2 settings (seeds, ψ, sampler steps) are missing. Truncation below 1 would itself concentrate samples toward the light-red mode.
- **Consequence:** Skin scores, and therefore every grouping in the paper, can't be reproduced exactly. Mask provenance affects the validity of the scores.
- **Fix:** Specify all of the above, fix the h* definition (atan2 with an explicit range), and correct "ground truth" for FFHQ-Ageing.
- **Proposed severity:** Minor.
- **Confidence:** 4.

### C17. Cropping benchmark: Elo order-dependence and inference on interdependent ratings

- **Quote:** "Following common practice in chess playing [21], we set M = 400 and K = 16 and we initialize scores at 1400." (p.5); "which is confirmed with a statistically significant independent t-test (p < 0.0001)" (p.6).
- **Location:** §4.2.1.
- **Problem:**
  - **Elo depends on game order.** Sequential Elo with K = 16 and about 61 games per image depends on the order of the 22,500 games, and the paper gives no ordering, seed or number of repeats.
  - **The t-test assumptions do not hold.** Final ratings are not independent observations: the system is zero-sum and ratings are coupled through shared opponents. That violates the assumptions of the independent t-tests behind p < 0.0001 and the Bonferroni tests.
  - **The "60.73% preference" is model-derived.** It comes from plugging mean group ratings into the logistic formula, not from observed win rates.
  - **The model version is unspecified.** Which released Twitter saliency model and version was used is not stated.
- **Consequence:** The reported p-values are probably anti-conservative, and the results may not reproduce exactly. The direction of the main effect will probably hold.
- **Fix:** Report empirical cross-group win rates with bootstraps clustered by image. Fit a Bradley–Terry or logistic model with image random effects and skin covariates (as in C10). Average Elo over many random orderings, or use the batch MLE. Give the model version and commit.
- **Proposed severity:** Minor (from a reproducibility perspective). The statistical-validity part may be rated higher by the statistics scanner.
- **Confidence:** 3.

---

## Part 4: Ethics and responsible use

### C18. The hue measure increases ethnicity separability, and race-proxy / sensitive-inference risk is unaddressed in the dataset-collection recommendation

- **Quote:** "skin tone annotations may serve as a proxy for race or ethnicity annotations. Indeed, such sensitive attributes are subject to significant data privacy protections [22]" (p.1); "We show the relevance of skin hue to better represent different ethnical groups, as some ethnicities can have a similar skin tone but different skin hue profile." (p.5).
- **Location:** §1; §4.1; A.3 (Fig. S5b).
- **Problem:** The paper justifies skin colour partly as a privacy-friendlier alternative to race and ethnicity labels. It then argues for h* largely because it *better separates ethnic groups* (Asian vs White/Latino; Indian vs Black). A two-dimensional apparent-colour score designed to tell ethnic groups apart works as an automated ethnicity proxy, extracted with no human annotation or consent from any face image.

  That risks:
  - sensitive-attribute inference (special-category data under data-protection law, which the paper itself cites);
  - the "skin colour" variable being used as a covert race variable;
  - reifying hue categories as ethnic categories.

  The recommendation to track the score "from data collection to model deployment" has no safeguards attached.
- **Consequence:** The paper's ethical premise is in tension with its finding, and the recommendation may enable the harms it means to avoid.
- **Fix:**
  - Quantify the proxy risk: ethnicity predictability from (L*, h*) versus L* alone on CFD (e.g. balanced accuracy and mutual information).
  - Discuss legal status and governance: purpose limitation, aggregate-only reporting, no per-individual release.
  - Recommend use only for disaggregated evaluation, not individual inference.
  - State that the hue categories are apparent-colour bins, not ethnic categories.
- **Proposed severity:** Major. It bears on a core recommendation and needs new analysis and a substantive governance section.
- **Confidence:** 3.

### C19. Editing skin colour of identifiable real people, and dual use of the editing directions

- **Quote:** "Figure 4: Skin color manipulation on CelebAMask-HQ." (p.7); "Our skin color scores could inform which samples models are struggling with, and provide a solution by augmenting images or mitigating model representations in a multidimensional manner." (p.3).
- **Location:** Fig. 4; Fig. S3; §2 (mitigation); code release.
- **Problem:**
  - Fig. 4 publishes darkened, lightened and "pale"-edited versions of real, identifiable CelebA celebrities. Fig. S3 shows a recognisable public figure.
  - Changing the apparent skin colour of real people touches on dignity and representation (whitening and "blackface" connotations), and none of them consented to it.
  - Releasing skin-colour editing directions or code enables colourist beautification filters, deceptive media and racial misrepresentation.
  - Using synthetic skin-colour augmentation as a "solution" risks replacing real diverse data collection.
  - None of this is discussed.
- **Consequence:** Responsible-AI gap. Reputational and dignity harms.
- **Fix:** Use synthetic (GAN-sampled) or consented identities in the figures. Add a dual-use statement and release terms (research licence, no editing of real persons) for any released directions. Discuss the limits of synthetic augmentation.
- **Proposed severity:** Minor.
- **Confidence:** 4.

### C20. Data governance for submitting non-consented web images to commercial APIs

- **Quote:** "composed of 30,000 images available with a non-commercial research agreement" (p.4); "Individuals have given their informed consent for data collection." (p.5, about CFD only).
- **Location:** §4.1; §4.3.
- **Problem:**
  - About 150,000 images (30k reconstructed plus 4 × 30k edited) of non-consenting CelebA subjects were sent to each of three third-party commercial services.
  - It is not stated whether this is compatible with the CelebA agreement, whether the APIs' data-retention or service-improvement settings were opted out of, or whether ethics/IRB review was sought.
  - Consent is mentioned only for CFD.
- **Consequence:** Possible licence or privacy non-compliance, and the governance is not transparent.
- **Fix:** Add a data-governance statement covering licence compatibility, API data-handling settings, retention, and ethics review.
- **Proposed severity:** Minor.
- **Confidence:** 3.

### C21. Gender framing and racialised colour vocabulary

- **Quote:** "models classify individuals as more feminine when their skin tone becomes lighter" (Table 4 caption, p.8); "Another difference lies in Asian subjects, which are mostly in the yellow side of skin hue" (p.14); "when aging, Asian skin becomes darker and more yellow while Caucasian skin becomes darker and redder" (p.2).
- **Location:** §1, §4.3, A.3.
- **Problem:**
  - **Gender.** The disclaimer is commendable, but the analysis still treats the CelebA binary "Male" annotation (perceived gender) as "ground truth labels". It also turns binary classifier outputs into "more feminine", which conflates a label flip with femininity.
  - **Colour words.** Pairing "yellow" with Asian subjects repeats historically racist colour terminology, even though h* is a neutral colorimetric quantity.
- **Consequence:** Framing risk. It could reinforce the categories the paper critiques.
- **Fix:**
  - Use "predicted as female/male (perceived binary label)" and "perceived-gender annotations".
  - Use neutral hue labels (e.g. "lower/higher hue angle" or "redder/yellower undertone" in colorimetric terms) and avoid attaching colour names to ethnic groups.
  - Add a short note on this terminology.
- **Proposed severity:** Minor.
- **Confidence:** 4.

---

## Notes for the panel

- **C1 is the pivotal issue.** C2–C5 are its concrete, testable parts: cross-talk, dose, labels, and photometric effects. The cheapest decisive test is the set of cosine similarities with existing InterFaceGAN boundaries plus a CelebA-40 attribute panel on the edited images. The most decisive one is the skin-mask-only pixel counterfactual at matched ΔL*/Δh*.
- **Possible overlap with other scanners:** C13, C14 and C16 overlap with measurement validity (perspective A/B); C7, C11 and C17 overlap with statistics. The angle here is causal, external validity and reproducibility.
- The figure-derived background measurements (C5) come from `deepdive/fig4_bg.py` run on `render/pg_p7.png`. They are crude and indicative only.

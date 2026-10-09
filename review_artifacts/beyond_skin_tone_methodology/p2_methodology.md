contract_role: methodology
## Dimension Scores

### D1: methodology_rigor
score: block
trigger: "a required analysis or control is missing and can be supplied by reanalysing data the authors already hold, adding controls, or documenting"
block_class: repairable

Rationale. I score this dimension block, repairable. Mapping the manuscript onto my Phase 1 plan:

- (a) The construct is well scoped (S1, S6), but the incremental value of hue is never tested (W7) and chroma is dropped (W5).
- (b) The pipeline is partly specified and the code is released (S8), with documentation gaps (W17, W18).
- (c) There is no reliability evidence (W2).
- (d) There is no external validity anchor (W1), and the only robustness probe cannot test chromatic illumination (W3).
- (e) The audits lack intervals, tests that respect their dependence structure, sensitivity to bin edges, and adjustment for covariates the authors already hold (W4, W8–W11, W15).
- (f) The counterfactual benchmark has no dataset-level manipulation or off-target checks (W12–W14).

Each gap can be closed by reanalysing data the authors hold, adding controls, documenting, or adding a bounded validation sub-study. None requires a redesign of the audits. That is why I use the repairable class rather than the fatal one; the reasoning is in the Review Body.

### D2: writing_and_structure
score: not_assessed

## Review Body

The paper proposes describing the apparent skin colour of a face image with two CIELAB coordinates, perceptual lightness L* and hue angle h*. These are extracted from segmented skin pixels by K-means clustering, taking the histogram mode within each cluster and keeping the three brightest of five clusters. The authors use the measure to audit two face datasets and two generative models, a saliency cropper, three face verifiers, and four attribute classifiers, the last through StyleGAN3 latent edits. The question is worth asking, and several design choices are sound. The scoping to apparent colour, the reconstruction baseline for edits, and the tone-by-hue intersections all help.

Judged as a measurement instrument and as a set of fairness audits, though, the evidence is thin. The instrument itself is never validated. There is no reliability study and no external anchor, and the single robustness probe varies only luminance on one face. Two of the three model audits report no uncertainty, and the third uses an order-dependent rating system with t-tests that ignore how the ratings depend on each other. Disparities by skin colour are not separated from ethnicity, gender, or source dataset, although the authors hold those labels. The causal benchmark reports manipulation sizes for only three faces, and those numbers already contradict the claimed independence of the tone and hue edits.

Why repairable rather than fatal. My fatal trigger asks whether "what it captures cannot be established". It is not met here. For display-referred sRGB images, converting segmented skin pixels to CIELAB gives a definable apparent-colour quantity. What has not been shown is whether the scalar summary is faithful and reliable, and whether it agrees with human perception. Both can be added with a bounded validation sub-study. Existing annotated corpora the paper already cites allow at least a tone check without new collection.

My fatal example about counterfactual interventions also does not apply in full. The off-target drift is computable on the existing edited images, and conditional edit directions can be built with the same pipeline. These gaps fall under my block trigger. Taken together, they keep the paper below the bar for D1 until they are addressed.

criteria_binding_unavailable

No #684 criteria authority was supplied for this run, so this card makes no venue-alignment claim.

### S1: Construct explicitly scoped to apparent colour
The paper separates apparent colour (as rendered in the image) from constitutive skin colour and says it measures only the former. That is the right construct for auditing vision models, and it avoids implying dermatological validity.
**Evidence Anchor**: text: §1 "that a computer vision model would see"

### S2: Per-group sample sizes shown on the cropping results
Every box in Figure 3 prints its n (461/278 for tone, 206/533 for hue, 127/334/79/199 for the intersections), so readers can judge group balance directly.
**Evidence Anchor**: figure: Figure 3 (a)–(c) — n printed inside each box

### S3: Reconstruction, not the original image, as the counterfactual baseline
Comparing edited images with their reconstructions removes encoder–decoder reconstruction error from the estimated effect. This is a sound design choice.
**Evidence Anchor**: text: §4.3 "we compare the performance of manipulated images with the reconstructed version rather than the original one in Table 4."

### S4: Comparison against an existing entangled direction
Showing the CelebA "pale" direction next to the proposed edits is a useful discriminant contrast, even though the proposed edits' own cross-talk still needs quantifying (W12).
**Evidence Anchor**: figure: Figure 4 (g)–(h) — "pale" edits shift both L* and h*

### S5: Contrast confound taken seriously
The authors compare their tone edits with plain contrast scaling and report whole-image RMS contrast. This engages directly with the concern that "tone" edits may be contrast edits, even if the result is only partly conclusive (W12).
**Evidence Anchor**: figure: Figure S4 (b)–(d) — +light/+dark h* 55.88/56.84 vs +contrast h* 14.05

### S6: Coordinate choice
Pairing h* with L* rather than ITA avoids two indices that share b*. L* and h* are two of the three cylindrical CIELAB coordinates, so the choice has a principled colorimetric basis.
**Evidence Anchor**: text: §3 "avoids having correlated measures as both ITA"

### S7: Tone-by-hue intersections with multiplicity control
Figure 3c tests hue within tone strata using Bonferroni-corrected pairwise comparisons. This is the right kind of analysis for an incremental-value claim, though it needs the fixes in W8–W9.
**Evidence Anchor**: text: §4.2.1 "independentt-tests with a Bonferroni"

### S8: Code release
A public repository is linked, so readers can check the pipeline details that are missing from the text (W17).
**Evidence Anchor**: text: §4 "Code can be found at"

### S9: Distributions shown beyond binary cuts
The 20-bin histograms by tone and hue show the shape of each distribution beyond the 2×2 tables.
**Evidence Anchor**: figure: Figure S6 — 20-bin histograms of h* and L* split by the other dimension for CelebAMask-HQ and FFHQ

### S10: Known-groups check on consented, self-labelled, controlled-capture data
The CFD breakdown by self-reported ethnicity is weak but genuine construct evidence: the hue axis separates groups that L* does not.
**Evidence Anchor**: figure: Figure S5 (b) — CFD L*/h* scatter coloured by self-reported ethnicity

### W1: No external validity anchor for the L*/h* scores
**Problem**: The image-derived scores are never compared with any independent reference for what they claim to measure. There are no multi-rater perceptual judgments of skin lightness or hue in the images. There are no colorimeter or spectrophotometer readings of the people photographed. There are no captures with a colour target that would allow a ΔE between the pipeline output and a known reference.

The only checks are a one-subject relighting probe (Figure S3), a qualitative pattern by self-reported ethnicity on CFD (Figure S5b), and three faces in Figure 4. The paper argues that automatic scores are more objective than human annotation (§2–§3). Being automatic, however, is not evidence of validity.
**Evidence Anchor**: absence: §3 and §A.2 — expected a convergent-validity comparison of image-derived L* and h* against an external reference (multi-rater perceptual ratings, instrument readings, or colour-target captures) with agreement statistics; checked §2, §3, §4.1–§4.3, §A.1–§A.4, Figures 2–4 and S1–S6, Tables 1–4
**Why it matters**: Every downstream claim is a claim about this instrument: dataset skew, cropping and verification disparities, and causal effects. Without convergent evidence, a reader cannot tell whether a "yellow" or "dark" label tracks the skin colour a viewer would perceive, a colour cast, makeup, or segmentation leakage. Figure S1 shows how far the pipeline can drift, returning h* = −25.38 under a colour cast. On its own, this gap justifies a block on D1. It is repairable rather than fatal because a validation study can be added without redesigning the audits (see the opening of this Review Body).
**Suggestion**: Add a validation sub-study with three parts.
- Tone: report agreement between L* and existing image-level skin-tone annotations (for example, the Monk-scale annotation work cited as [63], or the Fitzpatrick labels in the dataset cited as [31]), using rank correlation and ordinal agreement with CIs.
- Hue: run a small multi-rater perceptual study, such as paired redness-versus-yellowness judgments on a sample stratified by L* and h*. Report rater composition, inter-rater agreement, and agreement with h*.
- Where possible, use captures that include a colour target to report ΔE00 against a measured reference under known illuminants.
**Severity**: Critical
**Confidence**: 4 — core expertise: measurement validity and image colorimetry

### W2: No reliability evidence for the instrument
**Problem**: The paper reports no agreement statistic for the scores across conditions that should leave them unchanged or nearly so:
- repeated images of the same person;
- a different segmenter (ground-truth masks for CelebAMask-HQ and FFHQ, DeepLabV3 predictions for CFD);
- K-means initialisation (no seed or restarts are reported, and K-means is stochastic);
- the number of clusters and the number retained (5 and top-3);
- Sturges binning;
- JPEG compression or resolution.

The data for several of these checks are already in hand. CelebA-derived images and LFW contain multiple images per identity, and CelebAMask-HQ has ground-truth masks that could be compared with DeepLabV3 predictions on the same images.
**Evidence Anchor**: absence: §A.2 Robustness — expected an agreement statistic (ICC or Bland–Altman limits with CIs) for L* and h* across repeated images of an identity, segmenters, K-means seeds, cluster settings, and compression levels; checked §3, §4.1, §4.2.1, §A.2, Figures S2–S3
**Why it matters**: Every group assignment is a hard cut (L* = 60, h* = 55°). Noise of a few units in the score therefore moves boundary images between groups. If that noise differs by tone, it creates spurious disparities. Without reliability evidence, measured group differences cannot be told apart from measurement noise.
**Suggestion**: Report the following, each stratified by tone so that any differential error is visible:
- within-identity ICC(2,1) and Bland–Altman limits for L* and h* on CelebAMask-HQ and LFW identities;
- agreement between scores from ground-truth and DeepLabV3 masks on CelebAMask-HQ;
- the spread of scores over at least 10 K-means seeds, over k from 3 to 7, and over alternative retention rules.
**Severity**: Major
**Confidence**: 5 — core expertise: reliability of automated measurement instruments

### W3: The robustness probe cannot test the main threat to hue, and its conclusion is overstated
**Problem**: The robustness analysis takes one person relit by a neural relighting network [81]. To my understanding of that method, it changes the luminance channel under monochrome spherical-harmonic lighting and keeps chroma from the input. If so, a* and b* are essentially fixed by construction. The small h* variation (57.08–59.12°) would then reflect only which clusters are retained.

The probe never changes illuminant chromaticity or white balance, which is the condition most likely to move h*. The paper's own Figure S1 shows this effect (colour cast h* = −25.38; low light h* = −14.70). Even so, the text concludes that hue carries "orthogonal" information.
**Evidence Anchor**: text: §A.2 "h∗ remains stable and robust to face relighting, which confirms that it provides complementary and"
**Why it matters**: The paper's case for adding hue rests on hue being a stable second dimension that is largely free of illumination effects. The probe offered cannot support that, and a single subject cannot support any claim about robustness across a population.
**Suggestion**: Run a controlled sensitivity analysis over illuminant chromaticity (for example, correlated colour temperature from 2700 K to 6500 K, plus green/magenta tint) and over camera white-balance error. Use many subjects stratified by tone. The shifts can come from physically based rendering or a von Kries/CAT transform applied to linearised sRGB. Report the distributions of ΔL*, Δh* and ΔE00. Also state whether [81] alters chroma.
**Severity**: Major
**Confidence**: 4 — core expertise: illumination and white balance; the detail of [81] is from my own knowledge and should be confirmed by the authors

### W4: Cut-points taken from instrument colorimetry, with no justification or sensitivity analysis
**Problem**: Every group (light/dark at L* = 60, red/yellow at h* = 55°) uses thresholds from a review of cutaneous colorimetry [46]. That review concerns instrument readings of skin under a standard illuminant and observer. Here the thresholds are applied to display-referred sRGB pixels from uncalibrated cameras, summarised by a mode-of-clusters heuristic, and the paper gives no argument that the two scales are commensurable.

Section A.4 shows 20-bin histograms for dataset composition only. The model audits (Figure 3, Tables 3–4) are never re-run at other cut-points or on continuous scores.
**Evidence Anchor**: text: §4.1 "Threshold values are taken from Ly et al. [46]."
**Why it matters**: The size and even the sign of a disparity can depend on where the bins are cut. The 55° cut falls in very different parts of different distributions: CFD is 72% "yellow" (533 of 739, Figure 3b), while FFHQ is 18% (Table 1b). Conclusions such as "dark-yellow under-represented" are statements about this cut as much as about the data.
**Suggestion**: Report the audits three ways: on continuous scores (L* and h* as continuous covariates, or splines); across a grid of cut-points (for example, L* from 50 to 70 and h* from 45 to 65); and with dataset-specific quantile bins. Then either explain why instrument-derived thresholds apply to image-derived values, or drop that implied equivalence.
**Severity**: Major
**Confidence**: 5 — core expertise: colorimetry and categorisation of continuous measures

### W5: Chroma is omitted, and hue angle is ill-conditioned for low-chroma pixels
**Problem**: The measure keeps L* and h* and drops chroma C*, the third CIELCh coordinate. Hue angle becomes numerically unstable as C* approaches zero: to first order, the error in h* is about σ/C* radians. As an illustration, with ±1 unit of a*/b* noise the error is about 5.7° at C* = 10 but about 2.3° at C* = 25.

Low-chroma pixels are typical of dim light, colour casts, and darker image regions. Hue precision may therefore be worst exactly where the paper makes its dark-yellow claims. The paper reports no per-image C* and no rule for excluding near-neutral pixels.
**Evidence Anchor**: text: §3 "focus on the measurement of L∗ for skin tone and h∗ for skin hue"
**Why it matters**: Measurement error that differs by tone is a known source of spurious fairness disparities. The paper also calls the measure "comprehensive" while leaving one of the three colour-appearance coordinates out.
**Suggestion**: Report C* per image and by group. Either exclude or down-weight pixels below a chroma floor when computing h*, or propagate per-image h* uncertainty (for example, a bootstrap over pixels). Check whether the dark-yellow and dark-red results hold in a chroma-restricted subset.
**Severity**: Major
**Confidence**: 3 — core expertise: colorimetry; how large the effect is on these data is unknown

### W6: Dataset-composition claims treat apparent image colour as population composition
**Problem**: The introduction and §4.1 describe face datasets as skewed toward light-red skin and under-representing dark-yellow skin. Yet the measure is apparent colour, which the paper itself says (§A.1, Figure S1) includes colour casts, illumination, makeup, flushing and camera processing. The paper's own controlled-capture data point the same way. CFD shows less spread than the in-the-wild sets, which the authors attribute to controlled capture. And 72% of CFD faces are "yellow", against 18% in FFHQ and 34% in CelebAMask-HQ.

This suggests capture conditions move h* a long way, so the red/yellow split in in-the-wild datasets cannot be read as the make-up of the people photographed. In addition, the proportions are counted per image, not per identity. CelebA-derived sets contain repeated identities, so some people are counted many times.
**Evidence Anchor**: text: §1 "skewed towards light-red skin color and under-represent dark-yellow skin color"; §A.3 "This is explained by the fact that images in CFD have been captured in a controlled setting"
**Why it matters**: The recommendation to balance future datasets on tone and hue relies on this reading. If the skew partly reflects photographic style (warm grading, flash, white balance), balancing on h* would balance capture conditions, not skin.
**Suggestion**: Describe Table 1 explicitly as apparent-colour composition. Estimate how much h* variance comes from capture conditions: compare repeated images of the same identities, and regress h* on image-condition proxies such as illuminant chromaticity estimated from non-skin regions, exposure, and saturation statistics. Report identity-level proportions alongside image-level ones.
**Severity**: Major
**Confidence**: 4 — core expertise: image colour pipelines; the CFD contrast is suggestive rather than conclusive because the population mixes differ

### W7: The added value of (L*, h*) over single-scalar baselines is never tested
**Problem**: The title claim is that hue reveals biases a tone-only scale misses. Yet no audit compares the two-dimensional grouping with ITA (the established quantitative baseline discussed in §3) or with L* alone, in terms of how much variation in model performance each explains. The L*–h* correlation in each dataset is not reported either, even though §A.4 notes that hue spread differs by tone. The tone-by-hue intersections in Figure 3c are a partial test within one audit. Tables 3–4 offer none.
**Evidence Anchor**: absence: §4.2–§4.3 — expected a comparison of (L*, h*) against ITA-only and L*-only groupings or covariates in explaining performance differences (e.g., nested models with a likelihood-ratio test or ΔR²); checked §3, §4.1–§4.3, §A.3–§A.4, Tables 1–4, Figure 3
**Why it matters**: ITA already includes b* (yellowness), so hue might add little beyond ITA, or it might add a great deal. As written, the central "beyond skin tone" contribution is asserted rather than measured.
**Suggestion**: For each audit, fit nested models on continuous scores (performance ~ L*; ~ ITA; ~ L* + h*; ~ L* × h*) with cluster-robust inference, and report the gain in fit with CIs. Report the L*–h* and ITA–h* correlations for each dataset.
**Severity**: Major
**Confidence**: 4 — core expertise: incremental validity testing

### W8: Cropping disparities are confounded with ethnicity, gender and source dataset
**Problem**: The cropping pairs are balanced on self-reported gender × ethnicity, and skin colour groups are formed afterwards from L*/h*. Figure S5b shows those groups are strongly structured by ethnicity: Asian and Black faces fall mostly on the yellow side, while White and Latino faces spread across hue. All Indian faces come from CFD-India, a separately collected set, so source dataset is confounded with one ethnic group.

The tone and red-versus-yellow comparisons are unadjusted t-tests. Any saliency preference for particular ethnic groups or genders, or any capture difference between CFD and CFD-India, would therefore show up as a "hue" effect.
**Evidence Anchor**: text: §4.2.1 "The product of both gender and ethnicity label sets results in 10"
**Why it matters**: To claim the cropper has a multidimensional skin colour preference, the h* effect has to survive conditioning on covariates the authors already hold. As reported, hue is not separated from ethnicity, gender or source.
**Suggestion**: Model the game outcomes directly. A Bradley–Terry or logistic model of each comparison, with the two faces' L* and h* differences plus ethnicity, gender, source and position indicators (see W21), would separate hue from these covariates. Report hue effects within ethnic groups where the h* range allows.
**Severity**: Major
**Confidence**: 4 — core expertise: confounding in fairness audits

### W9: Elo-based estimation, and t-tests on dependent ratings
**Problem**: Each face gets a single-pass Elo rating (K = 16, starting at 1400). Elo was built for players whose strength changes over time. Its result depends on the order of games, and a player with few games stays close to the starting value.

Game counts differ by design. Each of the 10 gender × ethnicity cells receives 9 × 500 = 4,500 appearances, but ethnic groups range from 108 to 197 faces. A face in a smaller cell therefore plays more games: roughly 45 to 85, if each group splits evenly by gender (my assumption).

The ratings are then compared with independent t-tests. Elo updates are zero-sum, so the ratings are not independent observations. Results are given only as thresholds (p below 0.0001, below 0.01), with no test statistic, df, effect size or CI. The "60.73% preference" is the mean Elo difference passed through the logistic curve, not an observed group win rate.
**Evidence Anchor**: text: §4.2.1 "we set M = 400 andK = 16 and we initialize scores at 1400."
**Why it matters**: Order dependence and unequal shrinkage toward the starting value can create or hide group differences that have nothing to do with the algorithm's preferences. The reported p-values do not reflect how the ratings depend on each other, so the inferential claims in Figure 3 are not established.
**Suggestion**: Use either of two estimators:
- Bradley–Terry strengths fitted by maximum likelihood, with standard errors or a bootstrap over games;
- Elo averaged over many random game orders, with order-bootstrap intervals.

Test group differences with a permutation test that reshuffles group labels across faces. Report observed between-group win rates with CIs, along with effect sizes and exact test statistics.
**Severity**: Major
**Confidence**: 4 — core expertise: rating systems and pairwise-comparison models

### W10: Face-verification disparities reported without counts, intervals or tests
**Problem**: Table 3 splits 1,000 LFW pairs into two marginal and four intersectional cells per model, but gives no per-cell counts, intervals or tests. The text nonetheless concludes that all models "prefer light skin tones and red skin hues".

The marginal gaps are 0.29–1.13 points. The intersectional cells contradict the marginal pattern: for ArcFace and FaceNet, dark-yellow is among the best-verified cells. As an illustration, at 94% accuracy the binomial SE is about 1.4 points with 300 pairs and about 3.4 points with 50 pairs. Gaps of this size may not differ from zero, and the small intersectional cells are likely noisy. LFW also reuses identities across pairs, so the pairs are clustered.
**Evidence Anchor**: table: Table 3 — ArcFace D+Y 96.77 exceeds L+R 96.12 while marginals report Light 95.52 vs Dark 94.39 and Red 95.36 vs Yellow 95.07; no per-cell n, interval, or test
**Why it matters**: Without uncertainty, bias cannot be distinguished from noise, and the directional claims in the caption and text are not supported by the reported data.
**Suggestion**: Report per-cell pair and identity counts, with Wilson or identity-clustered bootstrap CIs. Test differences with a model, for example logistic regression of correctness on group with identity-clustered errors, and correct across the model × cell family. Consider a larger protocol, such as the full 6,000-pair LFW View 2: the 1,000-pair test split is small for eight cells.
**Severity**: Major
**Confidence**: 5 — core expertise: uncertainty in disaggregated metrics

### W11: The rule assigning a verification pair to a skin colour cell is undefined
**Problem**: A verification pair has two images. In a negative pair they belong to two different people, who may fall in different tone or hue groups. The paper does not say how a pair is assigned to a cell: by the first image, by either image, only when both share a group, or by averaging. Impostor errors are known to concentrate in same-demographic pairs (as in the NIST demographic report the paper cites, [29]). The share of cross-group negatives in each cell therefore directly changes that cell's accuracy.
**Evidence Anchor**: text: §4.2.2 "which contains 1,000 test pairs (500 positives and 500 negatives)"
**Why it matters**: The quantity Table 3 estimates is undefined. Depending on the rule, differences between cells may reflect how the negative pairs are composed rather than how well the model handles a given skin colour.
**Suggestion**: State the assignment rule. Analyse genuine pairs (false non-match) and impostor pairs (false match) separately. For impostors, report same-group and cross-group pairs separately, following the NIST demographic-effects protocol.
**Severity**: Major
**Confidence**: 4 — core expertise: biometric fairness evaluation

### W12: The hue edit moves lightness, contradicting the independence claim used to reject "pale"
**Problem**: The paper states that each edit leaves the other colour dimension unchanged ("making them orthogonal"). It rejects CelebA's "pale" direction because that direction moves both. Its own Figure 4 contradicts this for one of the three faces. In row 2, the +red edit raises L* from 44.43 to 52.05 (+7.62). That is larger than the up-to-6-point lightness change the paper treats as meaningful under relighting, and similar in size to the h* change from the −pale edit on the same face (70.19 to 61.59). The +dark edit on that face also moves h* by +3.52°.

The edits also act beyond the skin. Section A.2 shows they change whole-image RMS contrast (0.644 reconstructed, 0.630 darker, 0.652 lighter). In Figure S4, the −contrast edit gives the same L*/h* signature as +dark (51.10/56.56 vs 62.40/56.84). By the paper's own metrics, then, darkening and contrast reduction are not distinguished; the distinction rests on visual realism. The independence claim rests on three hand-picked faces, with no dataset-level distribution.
**Evidence Anchor**: figure: Figure 4 row 2 — reconstructed L*=44.43 vs +red L*=52.05 (h* 70.19 to 57.32)
**Why it matters**: Reading Table 4 causally (hue causes the shift in smile predictions) requires the hue edit to change hue and not tone. With cross-talk, the smile result may partly be a lightness effect, and the paper itself links lightness to smile errors.
**Suggestion**: For all 4 × 30,000 edits, report on skin the distributions of ΔL*, Δh*, ΔC* and ΔE00, plus the change in non-skin regions (background ΔE, global contrast). Re-estimate Table 4 conditional on, or matched on, the off-target change. Consider projecting each latent direction orthogonal to the other and re-checking.
**Severity**: Major
**Confidence**: 5 — figure values read directly; core expertise: manipulation checks for counterfactual edits

### W13: Edit directions are not conditioned on the attributes being predicted, so semantic entanglement is unchecked
**Problem**: The latent directions come from two linear SVMs trained only on skin colour labels inferred for StyleGAN3 samples. In CelebA-type data, apparent lightness correlates with gender presentation (makeup, foundation, lighting style) and possibly with smiling. An unconditioned InterfaceGAN "light" direction can therefore carry feminine cues, and a "red" direction can carry expression cues. The reported findings, that lighter edits read as more feminine and redder edits as more smiling, are exactly what such entanglement would produce even without any skin colour effect.

The paper acknowledges that attributes are not preserved, but its control removes reconstruction error, not the side effects of the edit direction itself. It reports no identity-similarity check, no independent gender or smile probe, and no human verification of edited images.
**Evidence Anchor**: text: §4.3 "SVMs, one for skin tone and one for skin hue, are finally trained on the most confident positive and negative"
**Why it matters**: The headline causal findings, stated in §4 and the introduction (lighter tone reads as more feminine, redder hue as more smiling), may be artefacts of the intervention rather than evidence that the models are sensitive to skin colour.
**Suggestion**:
- Use InterfaceGAN's conditional manipulation to project the tone and hue directions orthogonal to the gender, smile, age and makeup boundaries.
- Report off-target drift using identity-embedding similarity, independent attribute classifiers that are not themselves under audit, and human verification of a stratified sample.
- Add a sham edit (a random direction of equal norm) to separate generator artefacts from colour effects.
- As a complementary design, edit only skin pixels in colour space under the mask; such an intervention cannot change facial geometry.
**Severity**: Major
**Confidence**: 4 — core expertise: generative counterfactuals for causal fairness evaluation

### W14: Manipulation dose is not reported or standardised
**Problem**: Edit sizes in perceptual units are shown for only three faces, and they vary widely: +light ΔL* from 5.28 to 14.30, +dark from −9.75 to −20.65, +red Δh* from −10.00 to −13.80, and +yellow from +6.94 to +10.36. There is no dataset-level distribution and no dose–response, yet the text compares effect sizes across directions ("the skin hue does not seem to have a large effect" on gender).
**Evidence Anchor**: text: §4.3 "we modify all images in the CelebAMask-HQ datasets"
**Why it matters**: Tone and hue effects cannot be compared without knowing how far each edit moved its target. An effect produced by a large edit may not hold at the magnitudes seen in natural images.
**Suggestion**: Report dataset-level ΔL* and Δh* for each direction. Evaluate several edit strengths to give a dose–response curve, expressed per unit of L* or per degree of h*.
**Severity**: Minor
**Confidence**: 4 — core expertise: manipulation checks

### W15: Table 4 effects reported without paired tests or intervals
**Problem**: Edited and reconstructed images form a paired design on the same images, but Table 4 gives point accuracies only. Changes of 0.06–0.58 points (+red, male samples, all four models) are described as "a increase in accuracy for all models". There is no McNemar test, paired bootstrap, or identity clustering (CelebAMask-HQ repeats identities). There is also no multiplicity control across the 4 models × 4 edits × 3 subsets.
**Evidence Anchor**: text: §4.3 "results in a increase in accuracy for all models"
**Why it matters**: The large effects (for example, Azure non-smiling accuracy falling from 80.84 to 69.76 under +red) would probably survive formal inference. The smaller directional claims and the null claims cannot be judged.
**Suggestion**: Report paired differences with identity-clustered bootstrap CIs and McNemar tests, and control the false discovery rate across the family.
**Severity**: Minor
**Confidence**: 5 — core expertise: paired inference

### W16: The brightest-cluster retention rule is not ablated
**Problem**: The final score keeps the three brightest of five K-means clusters, justified by how artists group values. Under the dichromatic reflection model, the brightest clusters are the most likely to contain specular highlights, whose colour follows the illuminant rather than the skin. Highlights are relatively more conspicuous on darker skin. Pixel-weighting and the per-cluster mode reduce this effect but may not remove it, and the rule is never compared with alternatives.
**Evidence Anchor**: text: §A.2 "We cluster the face skin into five groups and keep the top-3 groups with the highest L∗"
**Why it matters**: The rule could push L* upward and pull h* toward the illuminant colour by different amounts for different tones. How large that bias is remains unknown.
**Suggestion**: Ablate the rule: all clusters, middle clusters only, and specular masking (for example, excluding pixels above an L* percentile). Report the changes in scores and in group assignment, broken down by tone.
**Severity**: Minor
**Confidence**: 3 — core expertise: reflectance models; effect size unknown

### W17: Pipeline documentation gaps
**Problem**: Several details needed to rebuild the instrument are missing from the paper:
- the sRGB-to-CIELAB conversion (transfer-function linearisation, reference white, library);
- the feature space K-means clusters on, the seed, and how ties in the mode are broken;
- the segmentation source for LFW, for the generated images (Table 2), and for the edited images (Table 4);
- the LFW loading parameters.

The last point matters more than it may seem. To my knowledge, scikit-learn's LFW loader returns grayscale, downsampled crops by default unless told otherwise. The colour and resolution settings therefore affect both the skin measurement and the verification accuracy. The released code partly mitigates these gaps.
**Evidence Anchor**: absence: §3, §4.2.2, §4.3 and §A.2 — expected the colour-conversion assumptions, K-means feature space and seed, LFW loading parameters, and the skin-segmentation source for LFW, generated and edited images; checked §3, §4.1–§4.3, §A.2, Figures S2–S4, footnote 1
**Why it matters**: Different variants of the instrument appear to have produced different tables, which confounds comparisons across them (W20), and the text alone does not allow the method to be reproduced.
**Suggestion**: Add a methods table giving, for each dataset, the mask source, image resolution, conversion settings and clustering parameters.
**Severity**: Minor
**Confidence**: 4 — core expertise: reproducibility of image pipelines; the scikit-learn defaults are from my own knowledge

### W18: Hue-angle formula and range are inconsistent, and negative hues fall into "red"
**Problem**: Equation 2 defines h* as arctan(b*/a*). That form does not resolve the quadrant and returns values in (−90°, 90°). The text says h* runs from 0 to 360°, which requires a two-argument arctangent wrapped to [0, 360). Figure S1 shows negative values (−25.38, −14.70, −0.70, −4.22).

The paper does not say how such values are handled. Under the 55° rule they would count as "red". With the single-argument form, a green cast (a* below zero, b* above zero) would also produce a negative angle and be labelled red.
**Evidence Anchor**: equation: Eq. (2) h∗ = arctan(b∗/a∗) with stated 0–360° range, versus negative h* values in Figure S1 (a), (c)–(e)
**Why it matters**: Images with colour casts, which are the least valid measurements, end up in a substantive hue group.
**Suggestion**: Use atan2 wrapped to [0, 360). Report how many images fall outside 0–90°, and flag or exclude them rather than binning them.
**Severity**: Minor
**Confidence**: 5 — core expertise: CIELCh computation

### W19: Figure S3 understates the lightness change, and one relit image crosses the cut-point
**Problem**: The caption and text say L* "varies by up to 6 points". In Figure S3, the original image has L* = 66.63 and one relit image has L* = 59.41, a drop of 7.22; the relit values span 59.41–71.34. That image falls below the L* = 60 cut-point, so this person moves from light to dark under a lighting change alone.
**Evidence Anchor**: figure: Figure S3 — original L*=66.63 vs sixth relit panel L*=59.41
**Why it matters**: The paper understates how much illumination moves the score, and its own example shows that the binary tone groups are sensitive to lighting.
**Suggestion**: Correct the stated range, and report the share of images that lie within a few units of each cut-point.
**Severity**: Minor
**Confidence**: 5 — values read directly from the figure

### W20: The claim that generative models amplify skew lacks an interval and comparable masks
**Problem**: The paper describes P2 as "slightly amplifying" FFHQ's skew, based on 83.37% red in P2 output versus 81.87% in FFHQ. FFHQ scores come from ground-truth masks (§4.1). Generated images have no such masks, so an unnamed predicted mask must have been used. Sampling error at n = 10,000 is about 0.4 points, so the 1.5-point gap may exceed sampling noise. A change of segmenter alone, however, could shift binary shares by a similar amount.
**Evidence Anchor**: table: Table 2(b) — P2 red-hue total 83.37 vs FFHQ 81.87 in Table 1(b), reported as amplification without an interval
**Why it matters**: The apparent amplification may come from the change of instrument rather than from the generator.
**Suggestion**: Score real FFHQ images with the same predicted-mask pipeline used for the generated images, and report CIs for the differences.
**Severity**: Minor
**Confidence**: 4 — core expertise: measurement invariance

### W21: Cropping composites: face position and cropper version not reported
**Problem**: The two faces are stacked vertically, but the paper does not say whether top and bottom placement was randomised or counterbalanced within each group combination. Saliency croppers are known to have position preferences. The specific cropper release is also not identified beyond "Twitter".
**Evidence Anchor**: text: §4.2.1 "both facial images vertically with a white space in"
**Why it matters**: If placement was not counterbalanced, any top-or-bottom preference becomes a group effect.
**Suggestion**: Present each pair in both orders, or randomise placement and include position as a covariate (see W8). Name the cropper release and commit.
**Severity**: Minor
**Confidence**: 4 — core expertise: audit design

### W22: Commercial endpoints are not versioned or dated
**Problem**: The AWS, Azure and Clarifai results use "their latest available version", with no API version, model identifier or query date.
**Evidence Anchor**: text: §4.3 "we use their latest available version for attribute prediction"
**Why it matters**: Commercial attribute endpoints change and can be withdrawn, so Table 4 can be neither reproduced nor placed in time.
**Suggestion**: Report API versions, model identifiers and query dates, and archive the raw responses.
**Severity**: Minor
**Confidence**: 5 — core expertise: reproducibility of audits

### Questions for Authors
1. How is an LFW pair, especially a negative pair of two different people, assigned to a tone or hue cell in Table 3? How many pairs fall in each cell?
2. Which segmentation produced the skin masks for LFW, for the StyleGAN3/P2 samples, and for the edited CelebAMask-HQ images? Which scikit-learn LFW loading parameters (colour, resize, crop) were used?
3. Does the relighting method in [81] alter the a*/b* channels, or only luminance?
4. In the cropping composites, was top/bottom placement randomised or counterbalanced within each group combination?
5. How many images in each dataset have h* outside 0–90°, and how are they binned?

### Minor Issues (non-finding channel)
- §4.3 cites "Alahuf et al. [1]", but the reference list gives Alaluf.
- §4.2.2: "verify the identify of light-skinned" should read "identity".
- §4.3: "results in a increase" should read "an increase".
- The Figure S2 caption is truncated ("to get the f").
- The Figure S5 caption orders the hue labels "(yellow vs. red)", whereas Figure 2 uses "(red vs. yellow)".
- §4.3: "transgendered" should read "transgender".

### Note on the arithmetic attestation
I agree with the injected no_recomputable_statistics attestation. The manuscript reports p-values only as thresholds, with no t statistics, df or SDs. The Figure 3 group sizes are printed, but no df is given to check them against. All other figures are percentages or continuous summaries outside the bounded procedures. The one numeric inconsistency I found (the 6-point versus 7.22-point L* change in Figure S3) is outside those procedures and is reported as W19.

## Arithmetic Receipts

no_recomputable_statistics: Checked Section 4.2.1 and the Figure 3 caption and box plots (independent t-tests reported only as p below 0.0001 and Bonferroni-corrected p below 0.01, with no t statistic and no df; Figure 3 group sizes n = 461, 278, 206, 533, 334, 127, 79, 199 are printed but no df is reported, so neither p_from_test_statistic nor n_from_df has its inputs); Tables 1 and 2 (dataset and generated-image shares in % over 30,000, 70,000 and 10,000 images, with no stated per-item response scale); Table 3 (LFW accuracies in % over 1,000 test pairs, with no stated per-item response scale and no subgroup N); Table 4 (CelebAMask-HQ accuracies in % with no subgroup N); the Elo-derived 60.73% and 58.25% preferences and the RMS contrast means 0.644, 0.630 and 0.652 (continuous quantities, not discrete-scale means); no SDs are reported anywhere, so no grim, grimmer, p_from_test_statistic or n_from_df claim has every required input stated in the manuscript.

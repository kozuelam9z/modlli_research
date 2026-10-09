# V4 adversarial verification (methodological-correctness lens): K13–K24 and S-h to S-m

Paper: Thong, Joniak & Xiang, "Beyond Skin Tone" (ICCV 2023, arXiv 2309.05148v2).

**Stance.** I tried to refute each critique on technical grounds, testing it against the paper's own design defences: the reconstruction baseline, the "pale" contrast, Bonferroni correction, and the apparent-colour scoping.

**Evidence used:**
- the manuscript text;
- page renders p6, p7, p13 and p14;
- zoomed crops of Fig. 4;
- independent scripts, listed below;
- the authors' public repository (`github.com/SonyResearch/apparent_skincolor`: README, `face-verification/lfw.py`, `cropping/generate.py`, `attribute/`);
- scikit-learn's `fetch_lfw_pairs` documentation;
- the FFHQ-Aging README;
- Microsoft's Azure Face retirement notice.

Web and repository content was treated as data. The code was read through a fetch tool that summarises it, but the specific lines quoted below were returned verbatim.

**Scripts.** All are in `deepdive/verify_scripts/` and run with the scratchpad venv using `-I`.
- `v4_table3.py`: an independent joint search for the Table 3 cell sizes, the ArcFace swap test (including a test of the N<1000 rebuttal), Fisher exact tests with Newcombe CIs, a pairs-vs-images sensitivity check, and minimum detectable difference (MDD) and power.
- `v4_table4.py`: the constant-share check with rounding intervals, the detection-failure rebuttal, an equal-variance probit "single decision shift" model, the L\*-leakage arithmetic, and McNemar bounds.
- `v4_tables12.py`: P2 and StyleGAN3 vs FFHQ (one-sample and two-sample tests), and Table 1(b) integer feasibility.

## Summary

| ID | Verdict | Proposed → **corrected severity** | One-line reason |
|---|---|---|---|
| K13 | CONFIRMED (reframed: "uninformative/underpowered", not "no bias") | Major/Critical → **Major** | It voids the face-verification half of claim (iii). The cropping half survives in direction, so the core claim is not wholly invalidated. |
| K14 | CONFIRMED | Major → **Minor** (merge into K13) | The fix is trivial, and it flips the sign of a non-significant gap. Its real weight is as evidence of transcription errors across tables. |
| K15 | PARTLY CONFIRMED (the grayscale / 62×47 sub-claim is **refuted** by the released code) | Major → **Major** | The pair-to-group rule is undefined even in the code. Accuracy at one threshold mixes FMR and FNMR. The models run far below their usual LFW accuracy. |
| K16 | PARTLY CONFIRMED (non-identification confirmed; "entanglement explains the patterns" overstated) | Major/Critical → **Major** | Plausible but untested alternative. The asymmetries are non-diagnostic, and some in-paper evidence (direction specificity) mildly favours the authors. |
| K17 | PARTLY CONFIRMED (the arithmetic is right; the "circular" sub-claim is refuted; the claimed consequence is quantitatively weak) | Major → **Minor** (fold into K16) | By the paper's own slopes, L\* leakage of the size shown explains ≤10–30% of the +red→smile effect and predicts the wrong sign for gender. |
| K18 | CONFIRMED | Minor → **Minor** | Exactly three inconsistent cells. The rebuttal (detection failures) fails for FairFace. "+red raises male accuracy" is a null effect in probit terms. |
| K19 | CONFIRMED with corrections | Minor → **Minor** | Hue amplification is robust (p≈1e-4). The tone "attenuation" is itself marginal (p≈0.04–0.06). The mask mismatch is smaller than claimed (same DeepLabV3 family). Resolution and settings remain unreported. |
| K20 | CONFIRMED with corrections | Minor → **Minor** | Several items are in the released code. Edit strength, latent space, API versions and dates, the pair grouping and the Elo order remain missing. Azure attributes were retired by 30 June 2023. |
| K21 | CONFIRMED | Minor → **Minor** | Writing and structure only. |
| K22 | PARTLY CONFIRMED | Major (writing) / Minor (method) → **Minor** (method lens) | Scattered caveats exist. The race-proxy tension is real but does not change the validity of any claim. ICCV 2023 had no mandatory limitations section. |
| K23 | CONFIRMED | Minor → **Minor** | Rewording fixes it. |
| K24 | CONFIRMED with a correction | Minor → **Minor** | The Table 1(b) cells are *not* uniquely determined at N=70,000. The two margins are jointly impossible, and 81.88 is the more likely, but not certain, correct value. |

| Strength | Verdict |
|---|---|
| S-h contrast confound examined | PARTLY CONFIRMED (genuine but weak control) |
| S-i F/M and S/NS split | CONFIRMED (the most useful design feature of §4.3) |
| S-j CFD consented and controlled | CONFIRMED with caveats (two capture sources; see the new finding N1) |
| S-k gender-classification framing | CONFIRMED with caveats |
| S-l candid reconstruction limitation | CONFIRMED, with an irony: the same sentence concedes the K16 mechanism |
| S-m histograms beyond binary cuts | CONFIRMED (partial: not a sensitivity analysis) |

**New findings outside my range, for the orchestrator.**
- **N1 (bears on K11 and K12).** `cropping/generate.py` does **not** randomise top/bottom position. The groups are `product(['W','B','A','I','L'], ['F','M'])` and the code iterates `it.combinations(product, 2)` with `top = combinations[i][0]` and `bottom = combinations[i][1]`. The top image is always the earlier group.
  - White faces are therefore **always on top** against every non-White group, and Latino-M is always at the bottom.
  - Position is perfectly aliased with group order. Any top/bottom preference of the Twitter saliency model maps directly onto the light/dark and red/yellow contrasts.
  - Shuffling happens only *within* each combination (seed 2022). Images are resized to a fixed 859×611.
  - This probably raises K11 to the upper end of Major.
- **N2 (bears on K12).** No Elo script is in the repository according to the README. If games were rated in file order, the order is combination by combination (systematic, not random).

---

## K13. Face verification: no counts, CIs or tests; nothing is significant

**Verdict: CONFIRMED, with a reframing.** **Severity: Major** (not Critical).

**Independent re-derivation** (`v4_table3.py`). I searched all `(nL, nR, nLR)` at N=1000 jointly over the nine printed values, requiring every value to be attainable as k/n and the counts to be additive.
- Dlib has exactly **one** solution: LR=387, LY=328, DR=161, DY=124 (Light 715, Red 548).
- FaceNet has one solution, the same one, once L+Y is read as 93.29.
- On the tone margins alone, every model admits only nL=715.

The counts in K13 are therefore reproduced.

**Tests on the recovered counts** (pairs as units, Fisher exact, Newcombe CI). Across 24 contrasts (8 per model):
- the minimum p is **0.086** (ArcFace LR vs DR);
- every tone and hue margin has p ≥ 0.49;
- the CIs span roughly −3 to +5 pp.

Treating images (two per pair) as units, which is anti-conservative, still gives p ≥ 0.29 for every margin.

**Power and MDD.** Two-sided α=.05, 80% power, baseline ~95%:
- tone (715/285): MDD ≈ **4.6 pp** (Wald), or **5.2 pp** (arcsine);
- hue (548/452): about 4.1–4.6 pp;
- intersectional contrasts: 6.7–9.7 pp;
- the observed power for ArcFace's tone gap (1.1 pp) is **0.11**;
- detecting a 1-pp gap needs about **8,100 pairs per group**.

LFW test pairs reuse identities, so identity clustering would widen all of these further. The "≈4.4 pp" in the canonical entry is within the approximation range.

**Framing correction.** "No difference is significant" is literally true, but it invites the wrong reading (no bias). The correct statement is:

> Table 3 is uninformative. Its gaps (0.3–1.1 pp marginal) are a fifth to a quarter of the MDD. The CIs are compatible with bias of several points in *either* direction.

So the paper's directional claims ("all models tend to prefer light … and red", "FaceNet … more robust") and its model comparisons are unsupported. Absence of bias is not shown either.

**Strongest author rebuttal.** "Table 3 is descriptive and shows consistent direction across three models." This **fails** for three reasons:
- the three models are scored on the *same* 1,000 pairs, so their errors are highly correlated and agreement across models is not replication;
- after the K14 correction, the direction is not even consistent;
- the intersectional cells reverse (ArcFace DY is the best cell).

**Severity reasoning.** Core claim (iii) covers cropping *and* verification. K13 alone voids the verification half, but the cropping half survives in direction (it has its own problems: K11, K12, N1). So K13 is "Major, upper end". It is Critical only if the face-verification sub-claim is scored as a core claim in its own right.

## K14. ArcFace Red/Yellow columns swapped

**Verdict: CONFIRMED.** **Severity: Minor** (down from Major; merge into K13).

**Tests.**
- With ArcFace's hue margins removed, the cells and tone margins admit a single configuration. It implies **red = 95.07, yellow = 95.35**; the table prints 95.36 / 95.07 with 95.36 in bold under Red (page render p6).
- **Rebuttal tested:** "ArcFace dropped a few pairs (detection failure), so its N differs." I ran a full joint search for N = 990–999. **No N reproduces all nine ArcFace values.** At N=1000, 95.36 is unattainable for n_red=548.
- FaceNet L+Y = 93.30 is unattainable at n=328 (306/328 = 93.29); this is a rounding slip.

**Why I downgrade.**
- The correction is a column swap, which needs no reanalysis.
- It flips the sign of a −0.28 pp, p=0.88 difference that K13 already shows to be noise.
- The caption "all face verification models" is already unsupported by K13.

Its standalone importance is diagnostic. Together with K18 (three cells) and K24, it shows transcription errors in three of the four results tables, which justifies asking for all tables to be regenerated from raw outputs. Report K14 as a sub-bullet of K13.

## K15. Face-verification design

**Verdict: PARTLY CONFIRMED.** **Severity: Major.**

**Sub-claim refuted.** The suggestion that "the loader defaults are grayscale and about 62×47" does not describe what was run.
- The scikit-learn defaults are indeed `color=False`, `resize=0.5` and `slice_=(slice(70,195), slice(78,172))`, which give 62×47 grayscale. That part is verified.
- But the released `face-verification/lfw.py` calls `fetch_lfw_pairs(subset='test', color=True, resize=1)`. The inputs were therefore **125×94 RGB, funnelled, central crops**.
- The test subset is the 1,000-pair set the paper describes.

What remains is a reporting gap in the paper, not an impossibility. Skin colour was computable.

**Confirmed sub-claims.**
1. **Pair-to-group rule undefined.** It is absent from the paper *and* from the released code: `lfw.py` contains no skin grouping, and the README does not mention LFW pair groupings. The recovered counts show that each pair is counted once (715+285=1000), so some rule was used, but it is unknown. For negative pairs this defines the estimand.
2. **Accuracy at one threshold mixes FMR and FNMR.** `DeepFace.verify(..., enforce_detection=False)` is called with the default detector and threshold. Standard LFW benchmarking reports accuracy, so this is conventional for *benchmarking*. For a *fairness* audit, NIST-style per-group FNMR on genuine pairs and same-group FMR is the accepted estimand.
3. **Off-nominal operating point.** ArcFace scores 95.20% here. DeepFace's own README lists about 99.4% for ArcFace (and Facenet 99.2%, Dlib 99.38%) on LFW. The likely causes are tight 125×94 crops with `enforce_detection=False` and default thresholds. Group gaps at an off-nominal operating point may not describe the deployed models.

**Strongest author rebuttal.** "LFW accuracy is the standard protocol, and the setup is in the code." This succeeds only for the loader settings. It fails for the grouping rule (which is in neither the paper nor the code) and for the fairness estimand.

**Severity.** The design problems persist even if K13's sample-size problem were fixed. Redefining groups and metrics needs new analysis, so Major stands. In practice §4.2.2 is already disposed of by K13, so K13, K14 and K15 can be presented as one "verification evidence is uninformative" item.

## K16. Causal edits not shown to be skin-specific

**Verdict: PARTLY CONFIRMED.** **Severity: Major** (not Critical).

**What is right.**
- The directions are unconditioned InterFaceGAN SVM normals. They are trained on whole-image classifier labels for 500k StyleGAN3 samples, using only the "most confident" extremes (§4.3).
- There is no conditional manipulation, no cosine with the gender or smile boundaries, no attribute panel or human re-labelling, and no non-skin colour check.
- Labels are assumed to survive editing.
- The paper itself concedes the mechanism: "struggle with spurious correlations. This results in attributes not being preserved." Its mitigation, the reconstruction baseline, removes *inversion* error but not *edit* side-effects.
- The authors released `hue_skin_boundary.npy` and `lum_skin_boundary.npy`, so the decisive cosine check was cheap and is still feasible.

**Does entanglement actually predict the Table 4 asymmetries? It is observationally equivalent, not uniquely predictive.**

I fitted an equal-variance probit "single decision shift" (`v4_table4.py`). Every Table 4 change is well described by **one** shift δ of each classifier's decision variable, applied to both classes:
- **AWS +light:** δ = +0.31 SD toward "female", estimated from male accuracy (94.82→90.66). This predicts female accuracy of 99.88; observed 99.84. Azure fits 99.91 vs 99.91, and FairFace 99.80 vs 99.77.
- **Smile:** the two classes give nearly identical δ. Azure +red gives δ = 0.355 from non-smiling vs 0.401 from smiling; AWS +red gives 0.429 vs 0.402. AWS +yellow gives −0.31 vs −0.29.

So "+light lowers male accuracy but barely changes female" is a **ceiling artefact** (female accuracy is about 99.7%), and "+red lowers non-smiling accuracy" is the mirror of "+red raises smiling accuracy". *Any* mechanism that moves the decision variable predicts these patterns: skin-colour sensitivity, semantic entanglement (femininity or expression cues), or global exposure and white balance. The asymmetries carry **no** diagnostic information. The canonical wording ("entanglement … would produce the same Table 4 patterns") is correct only as a statement of non-identification. It should not be presented as evidence *for* entanglement.

**In-paper evidence that mildly favours the authors** (not in the scans):
1. **Directions are attribute-specific, not generic.**
   - +red shifts gender by essentially zero (|δ| ≤ 0.03 SD in all four models) while shifting smile by about 0.36–0.43 SD.
   - +light shifts gender by about 0.23–0.32 SD and smile by only about 0.15 SD.
   - A "red" direction carrying generic feminising or "attractive portrait" content would be expected to move gender too. It does not.
2. **The L\* leakage of the hue edit cannot explain the hue effects** (see K17). It also predicts the wrong sign for the effect of +red on gender.
3. **Expression in Fig. 4.** At print resolution, the two non-smiling faces (rows 1 and 3) show no visible change of expression under +red. This is weak evidence (n=2, chosen by the authors).

Counter-evidence also exists:
- +dark visibly darkens the hair in row 1, so off-skin changes do occur.
- Scan C's crude background measurements suggest the background b\* moves with the hue edit, consistent with a white-balance component.

**Strongest author defence.** The construct is *apparent* skin colour, and the paper's own Fig. S1(d–e) lists makeup and face flushing as determinants of apparent colour. Entanglement with **chromatic correlates inside the skin mask** (blush, foundation) is therefore in-construct. A classifier that calls flushed or redder skin "smiling" is showing exactly the hue sensitivity the paper claims.
- This defence **succeeds** for chromatic changes on the skin.
- It **fails** for out-of-construct changes: mouth or cheek geometry, lips, hair, facial hair, background or global white balance. None of these was measured.
- **Label validity** differs by attribute. For smile (an image-level, expression label), an edit that changes expression genuinely changes the correct label, so K16's label point bites hard. For gender (a person-level label), the label cannot change, but the *cue* attribution can.

**Severity reasoning.** The critique establishes that claim (iv) is **not identified**. It does not establish that the effects are artefacts:
- no evidence of material entanglement is presented;
- the in-paper evidence modestly favours colour-driven effects;
- the latent-transect design with a reconstruction baseline is accepted practice in this literature, although Balakrishnan et al. [4] added human validation;
- the decisive checks need no new data: cosines with released boundaries, an attribute or action-unit panel on existing edits, a skin-mask-only recolour, and human re-labels of a sample.

That is "materially weakens, needs substantial reanalysis", which is **Major**. It would escalate to Critical only if, for example, cos(D_hue, n_smile) or cos(D_tone, n_gender) turned out to be material, or re-labelling showed label drift on the order of the accuracy changes.

## K17. The "orthogonal" edit claim

**Verdict: PARTLY CONFIRMED.** **Severity: Minor** (down from Major; fold its fix into K16).

**Arithmetic verified** from the p7 render:
- row 2 +red moves L\* from 44.43 to 52.05 (**+7.62**);
- row 3 +yellow moves L\* from 72.15 to 75.92 (**+3.77**);
- the tone edits keep |Δh\*| ≤ 3.52°.

Off-axis/on-axis ratios:
- the tone directions are clearly cleaner than "pale" (Δh/ΔL ≤ 0.17, vs 0.15–0.51 for ±pale);
- the hue directions match pale on 2 of 6 instances (ΔL/Δh of 0.59 for row 2 +red, and 0.33–0.36 for +yellow on rows 2–3).

So "orthogonal" holds for tone and is overstated for hue. There are only n=3 faces and no dataset-level distribution. The doses are unreported and asymmetric (|ΔL\*| for +dark averages 14.7 vs 9.8 for +light; |Δh\*| for +red averages 12.2 vs 8.6 for +yellow). All of this is confirmed.

**Sub-claim refuted.** "The manipulation is checked with the same instrument that defined the directions" is **not a valid circularity objection**. A manipulation check *should* use the measure that defines the treatment. The real gap is that L\*/h\* on skin cannot detect off-target non-colour changes, and that belongs to K16.

**The claimed consequence is quantitatively weak** (`v4_table4.py`).
- **Smile.** Calibrate L\* sensitivity from the paper's own tone edits: Azure non-smiling accuracy falls 0.46 pp per +1 L\*, AWS 0.21 pp. The mean +red L\* leakage is +2.99 (maximum 7.62). That predicts a change in non-smiling accuracy of −1.4 (up to −3.5) pp for Azure against an observed **−11.08**, and −0.6 (up to −1.6) pp for AWS against an observed **−7.28**. Leakage explains roughly 10–30% at most.
- **Gender.** Leakage predicts that +red *lowers* male accuracy by 1.0–1.8 pp, but male accuracy rises slightly in all four models.

The specific alternative that "the red→smile effect is partly a lightness effect" is therefore real but small, on the only evidence available.

**Strongest author rebuttal.** "Tone edits are clean, and hue leakage is small relative to hue's own effect." This largely **succeeds** for the Table 4 conclusions. It does **not** rescue the word "orthogonal", the n=3 basis, or the missing dose reporting.

**Severity reasoning.** What remains is an overstated word, an n=3 manipulation check, and unreported doses. Those are rigour and reporting issues whose fix (ΔL\*, Δh\* and ΔC\* distributions over the 4×30k edits, plus a dose sweep) is already part of K16's remedy. Standalone it is Minor. Keep it Major only if it is merged with K16 into a single "manipulation validity" item.

## K18. Table 4: no paired tests or CIs; three inconsistent cells

**Verdict: CONFIRMED.** **Severity: Minor.**

**Constant-share check** (rounding intervals). The female share w lies in [0.626, 0.643] for every cell except:
- **AWS +dark:** w ∈ [0.477, 0.495]. The expected All is 98.43; the table prints 98.27.
- **FairFace +red:** w ∈ [0.601, 0.604]. Expected 97.15; printed 96.97.
- **FairFace +yellow:** w ∈ [0.659, 0.662]. Expected 96.97; printed 97.16.

The smiling share is constant at about 0.47 throughout Table 4b.

**Rebuttal tested:** "per-condition detection failures change the denominators."
- To produce w=0.486 for AWS +dark by dropping female images alone, about **45% of female images** (8.5k) would have to be dropped. That is implausible.
- Counting failures as errors can only *lower* All. FairFace +yellow's printed All *exceeds* the w-weighted mean, so the swap remains the parsimonious explanation for FairFace.
- For AWS +dark, failure handling cannot be fully excluded, and the mis-typed value could be F or M rather than All. Either way, the cell is internally inconsistent.

**Over-reading.** "Redder … in male samples results in an increase in accuracy for all models" groups a null with a real effect.
- The +red male changes are +0.06, +0.21, +0.58 and +0.19 pp, which is about 7, 23, 64 and 21 net images out of about 11,060 males. In probit terms the gender shift is |δ| ≤ 0.03 SD.
- Significance depends on the unreported discordant counts. With 51 or more discordant pairs, the AWS p is at least 0.40. With 201 or more, Azure and FairFace p ≥ 0.12.
- A sign test for 4/4 positive gives p = 0.125.
- The "+dark" half of the sentence is robust (+1.9 to +6.3 pp).

Severity stays Minor. The headline effects are large and survive; only the secondary sentences and three cells are affected.

## K19. Generative-model comparison not like for like; "amplification" half true

**Verdict: CONFIRMED with corrections.** **Severity: Minor.**

**Tests** (`v4_tables12.py`). FFHQ is the full population, so the one-sample test is the appropriate one. P2 vs FFHQ:

| Quantity | P2 | FFHQ | Difference | One-sample z (p) | Two-sample z (p) |
|---|---|---|---|---|---|
| Yellow | 16.63 | 18.12 | −1.49 pp | −3.87 (1.1e-4) | −3.63 (2.8e-4) |
| Dark | 34.70 | 33.74 | +0.96 pp | 2.03 (0.042) | 1.90 (0.058) |
| Dark-yellow | 4.62 | 4.68 | −0.06 pp | | p = 0.78 |
| Light-red | | | +0.47 pp | | p = 0.35 |

- The 4-cell goodness-of-fit test gives p = 2.4e-4.
- StyleGAN3 matches FFHQ: goodness-of-fit p = 0.86, and every margin is within ±0.25 pp.

**Corrections.**
- "P2 is less light-skewed" is itself marginal (p≈0.04–0.06, a single 10k draw, no seeds). The defensible statement is: "P2 amplifies the red-hue share; tone is unchanged within noise; the 'under-represented' dark-yellow cell is unchanged".
- On masks, the FFHQ-Aging README confirms that the semantic maps "were acquired by training … DeepLabV3 … on the CelebAMASK-HQ dataset" (19 classes, 256 px by default). Calling them "ground truth" (§4.1) is a misdescription.
- But the authors' README says missing masks are generated with DeepLabV3 trained on CelebAMask-HQ. The generated images were therefore probably segmented by the **same model family**, so "masks differ" is weaker than stated.
- The live comparability threats are output resolution (the P2 FFHQ model is 256 px), the unreported truncation and sampler settings, and the absence of seeds. These could plausibly move binary shares by about 1 pp.

**Strongest rebuttal:** "same segmenter family." It partly succeeds. Severity is unchanged.

## K20. Reproducibility gaps

**Verdict: CONFIRMED for the paper, with corrections where the code fills gaps.** **Severity: Minor.**

| Item | Status | Where |
|---|---|---|
| LFW loader | **In code** | `subset='test'`, `color=True`, `resize=1` |
| DeepFace call | **In code** | `enforce_detection=False`, default detector and thresholds; the DeepFace version is not pinned |
| Cropper | **Pointed to** | the Twitter image-crop-analysis repo; the commit is unstated |
| Cropping pairs | **In code** | seed 2022, top/bottom not randomised (N1) |
| Latent boundaries | **Released** | `hue_skin_boundary.npy`, `lum_skin_boundary.npy` |
| Edit strength or α, latent space and layers, StyleGAN3 config and truncation for the 500k samples, Table 2 generation seeds and settings, the skin classifier | Missing | |
| LFW pair-to-group rule | Missing | |
| Masks for LFW and generated images | Missing | |
| Elo script and game order | Missing | |
| Commercial API versions and dates | Missing | |

**Azure, verified.** Microsoft's 2022 notice retired the Face API attributes for emotion, gender, age, smile, facial hair, hair and makeup. New customers lost access from 21 June 2022, and existing customers kept access until **30 June 2023**. Later documentation lists gender as retired and smile as limited. The Azure gender results in Table 4 can therefore no longer be reproduced, and the query date is necessary metadata. This strengthens the case for K20 but does not change its severity: it is reproducibility, not validity.

## K21. Structure

**Verdict: CONFIRMED.** **Severity: Minor.**
- The abstract names neither the extraction method nor any quantitative finding.
- The extraction pipeline (segmentation, K-means, top-3 clusters, Sturges mode) appears only in §A.2. The main text points to it with "We provide the details of the methodology … in Figure S3".
- §2 plus the colorimetry and ITA part of §3 take about 2 pages.
- Naming drifts: "Alahuf/Alaluf", "Interface/InterFaceGAN", "FFHQ-Ageing/Aging", "skin color scale/score/measure".

These are clarity issues with no effect on the claims.

## K22. No consolidated limitations or responsible-use discussion

**Verdict: PARTLY CONFIRMED.** **Severity: Minor** (methodology lens).

There is no consolidated section, but caveats are scattered through the paper:
- apparent vs true colour (p2, A.1);
- the reconstruction limitation (§4.3);
- the gender-classification disclaimer (§4.3);
- CFD consent (§4.2.1).

So "no limitations" overstates. The substantive points do hold:
- **Race-proxy tension.** The paper motivates skin tone as a privacy-friendlier proxy (p1), then promotes hue partly *because* it separates ethnic groups (A.3).
- Dual use of released skin-colour edit directions is not discussed.
- Sending CelebA images to commercial APIs is not addressed.
- "Yellow" is applied to Asian subjects (p14).

None of these alters the validity of a claim. ICCV 2023 did not mandate a limitations section. For writing, I would rate it moderate rather than Major.

## K23. Over-generalisation

**Verdict: CONFIRMED.** **Severity: Minor.**

All five phrases are verbatim:
- "any camera" (A.2);
- "any face pose" (§3, A.2);
- "both computer vision datasets and models" (Abstract);
- "previously invisible" (§1, §5, A.3);
- "from data collection to model deployment" (§5).

The evidence base is:
- 2 in-the-wild datasets plus CFD;
- 1 cropper, which Twitter itself withdrew;
- 3 verifiers on 1,000 LFW pairs (uninformative, K13);
- 4 classifiers × 2 attributes on one dataset with one generator.

There is no pose or camera experiment. The verification "biases" are not significant, so "previously invisible" is unsupported for that task. Rewording fixes it.

## K24. Minor numeric slips

**Verdict: CONFIRMED with a technical correction.** **Severity: Minor.**

**Table 1(b).**
- The canonical says the cells are "exact at N=70,000". **This is wrong.** At N=70,000, 0.01% equals 7 images, so each printed cell admits 7 integer counts, and 231 four-cell tuples sum to 70,000.
- Even so, **no tuple** makes Red round to 81.87 *and* Yellow round to 18.12. The two margins are jointly impossible under a full partition.
- Red = 81.88 is the more likely correct value (203 of the 231 tuples give Yellow 18.12; only 14 give Red 81.87), but it is not certain. Alternatively, some images were left unscored.

**Fig. S3.** The original image is the first panel (the one without a lighting sphere), at L\* = 66.63. The relit range is 59.41–71.34, so the maximum deviation is **−7.22**, not "up to 6". The 59.41 panel crosses L\* = 60.

**FaceNet L+Y.** 93.30 is unattainable at n=328; the true value is 93.29.

---

## Strengths

**S-h. Contrast confound examined.** PARTLY CONFIRMED.
- RMS contrast values (0.644 / 0.630 / 0.652) and the Fig. S4 comparison are reported. This is a real engagement with the confound.
- But the control (pixel scaling) is unrealistic. +contrast saturates, giving L\* = 91.74 and h\* = 14.05, so the h\* change comes from clipping.
- −contrast has the **same L\*/h\* signature as +dark**: 51.10 / 56.56 vs 62.40 / 56.84. The instrument cannot tell darkening from contrast reduction, and the distinction rests on visual realism.
- Everything is measured on the whole image, with no skin vs non-skin split.
- Keep it as a minor strength.

**S-i. F/M and S/NS disaggregation.** CONFIRMED. This is the most informative design feature of §4.3. The probit analysis shows that it is exactly what reveals a single decision-variable shift per edit, so the direction of bias is interpretable. Group n's are not printed (they are recoverable: w ≈ 0.631 and 0.470).

**S-j. CFD consented and controlled capture.** CONFIRMED with caveats.
- Consent is stated, and capture is controlled.
- But two collections are pooled (CFD and CFD-India, from different sites), whereas the text says "From CFD".
- The code resizes images to a fixed 859×611 canvas slot and does not randomise position (N1). The benchmark's *data* is a strength; its *composition design* is not.

**S-k. Ethical framing of gender classification.** CONFIRMED with caveats. The disclaimer is explicit and apt. It is undercut by "more feminine", by calling binary CelebA labels "ground truth", and by "transgendered".

**S-l. Candid reconstruction limitation.** CONFIRMED. Note that the candid sentence ("struggle with spurious correlations … attributes not being preserved") concedes K16's mechanism, while the mitigation (the reconstruction baseline) only addresses inversion error. Credit the candour, but do not treat the sentence as addressing K16.

**S-m. Histograms beyond binary cuts (Fig. S6).** CONFIRMED, partial.
- Fig. S6 shows 20-bin histograms stacked by the other binary dimension, which reveals distribution shape.
- It is not a threshold-sensitivity analysis. "The different thresholds confirm…" is asserted without numbers.
- The figure itself shows that the hue modes (about 45–50°) sit below 55°, which supports K05. It is a strength because it lets readers see the problem.

---

## Sources (web, treated as data)

- [scikit-learn `fetch_lfw_pairs`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_lfw_pairs.html): defaults `color=False`, `resize=0.5`, `slice_=(70:195, 78:172)`, 62×47.
- [SonyResearch/apparent_skincolor](https://github.com/SonyResearch/apparent_skincolor): README, `face-verification/lfw.py`, `cropping/generate.py`, `attribute/`.
- [FFHQ-Aging-Dataset README](https://github.com/royorel/FFHQ-Aging-Dataset): DeepLabV3 trained on CelebAMask-HQ; 256 px by default.
- [Azure update: Responsible AI investments and safeguards for Facial Recognition](https://azure.microsoft.com/en-in/updates/facelimitedaccess/): attribute retirement; existing customers until 30 June 2023.
- [DeepFace README via PyPI 0.0.82](https://pypi.org/project/deepface/0.0.82): creator-declared LFW accuracies (ArcFace about 99.41%).

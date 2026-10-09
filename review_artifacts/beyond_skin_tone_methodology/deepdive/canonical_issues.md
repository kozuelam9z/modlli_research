# Canonical issue list: Thong, Joniak & Xiang, "Beyond Skin Tone" (ICCV 2023)

Raw findings were merged from five sources:

- the contract methodology seat (METH W1–W22) in `review_artifacts/beyond_skin_tone_methodology/p2_methodology.md`;
- the contract Journal-Fit seat (EIC W1–W10) in `p2_eic.md`;
- three independent scans (A = measurement, B = statistics, C = causal) in `scratchpad/deepdive/scan_*.md`;
- the orchestrator's local checks (LOCAL §x) in `review_artifacts/beyond_skin_tone_methodology/local_checks.md`.

Proposed severities come from the merger. Verifiers must challenge them.

**Severity bands.**

- Critical: this single defect, uncorrected, invalidates a core claim.
- Major: it materially weakens a core claim and needs substantial reanalysis or new data, but the core survives.
- Minor: it affects clarity or rigour without changing the core claims.

**The paper's core claims.**

- (i) L* + h* is a valid, more comprehensive measure of apparent skin colour.
- (ii) Face datasets are skewed toward light-red skin, and generative models reproduce this skew.
- (iii) Hue reveals additional model biases in cropping and face verification.
- (iv) Latent edits measure the causal effect of skin tone and hue on attribute classifiers.
- (v) Multidimensional scales are therefore recommended for fairness assessment, from data collection to deployment.

---

**K01. No external validity anchor for L*/h*.** Proposed: Major, possibly Critical.
The scores are never compared with colorimeter or spectrophotometer readings of the same people, with human perceptual ratings, or with captures that include a colour target. The paper's own argument is that automatic scores are "objective".
Sources: METH W1 (Critical), A2.
LOCAL §2.4: subject-level L* tracks the MST oracle (ρ = −0.76), so tone has some convergent validity. No hue reference exists to test h* against.

**K02. No reliability evidence.** Proposed: Major.
There is no within-identity, segmenter, K-means seed, k, binning, or compression agreement.
Sources: METH W2, A2.
LOCAL §2.1, on MST-E (same people, same day, same camera), using the authors' estimator:
- h*: ICC(1) = 0.29 [0.17, 0.40] across all images and 0.46 for well-lit images. The within-subject SD (12°) is about the size of the between-subject SD (8–11°).
- L*: ICC = 0.13 across all images and 0.50 for well-lit images.
- 72% of h* variance lies within subjects.

**K03. The Fig. S3 robustness test cannot support h* robustness and misreports L*.** Proposed: Major.
- DPR [81] relights only the Lab L channel and copies a/b back (verified in the public demo code), so h* stability is guaranteed by construction.
- The test uses one face and white light only.
- The text's "up to 6 points" is contradicted by the printed values: the deviation is −7.22 (59.41 vs 66.63), and that relit image crosses L* = 60.
- The paper's own Fig. S1 shows h* = −25.38 under a colour cast.
- The "orthogonal information" conclusion drawn from this test is a non sequitur.

Sources: METH W3 and W19; A7; C14; EIC W3 (partly).
LOCAL §2.2: real lighting changes move h* by person-specific amounts (−18.5° to +32°). The golden vs not-ideal pair gives |Δh*| = 16° on average (max 71°), and 6/15 subjects change 4-cell category.

**K04. The 60 / 55° thresholds are borrowed from in-vivo colorimetry, with no transfer argument or sensitivity analysis.** Proposed: Major.
The cut-points come from [46] Ly et al., which concerns spectrophotometer or colorimeter readings. Literature provenance is still pending: does Ly et al. state these cut-points at all? Is 55° an ITA boundary?
Sources: METH W4; A5; B8; C13.
LOCAL §2.5:
- On MST-E photos only 1.5% of images reach h* ≥ 55°.
- The MST reference swatches measure h* = 47–79°, non-monotonic across the scale.
- In the paper's own data: CFD is 72% "yellow", CelebA 34%, FFHQ 18%.

**K05. The dataset "skew" claims (Tables 1–2) have no reference distribution, and capture conditions are confounded with population.** Proposed: Major, possibly Critical.
The hue skew mostly reflects where 55° falls on a unimodal distribution (Fig. S6). Under controlled capture (CFD), the same instrument puts most faces on the yellow side.
Sources: A4 (Critical); METH W6; B8; C13.

**K06. The estimator design (5 clusters, top-3 brightest, left-edge Sturges mode, unstandardised [L, hue]) is unjustified and unablated, with skin-tone-dependent error.** Proposed: Major.
The choice is justified by an art book.
Sources: METH W16; A10; A11.
LOCAL §2.3: in well-lit images, the within-subject SD of h* is 6.6° for MST 1–3 and 16.2° for MST 7–10 (ρ = 0.69, p = 0.001). Compared with the pixel-mean hue, the estimator shifts MST 7–10 subjects about 14° toward "red".

**K07. Low-chroma ill-conditioning; chroma dropped.** Proposed: Major.
Per-pixel hue is unstable when C* is small, which applies to darker skin and low light. There is no chroma gating, and chroma is not a reported dimension.
Sources: METH W5; A9.
LOCAL §2.5: for the MST10 swatch, C* is about 5.8, and one unit of a* moves h* by about 9°.

**K08. The hue formula and range are inconsistent: arctan, not atan2.** Proposed: Minor.
Eq. 2 is written as arctan(b/a), and the text claims a 0–360° range. The released code uses np.arctan, giving a range of (−90°, 90°). Fig. S1 prints negative h*, and negative values fall into "red".
Sources: METH W18; A8; A13; B16; EIC W3.
LOCAL: 51/1304 MST-E images have h* < 0.

**K09. Construct drift.** Proposed: Major.
"Apparent" colour is defined as an image property, yet the paper concludes things about people, for example "classify people with lighter skin tones as more feminine". The Conclusion speaks of "constitutive complexity". The recommendation to balance datasets on apparent L*/h* risks balancing on lighting rather than on people.
Sources: A1; A16; C12.

**K10. The incremental value of hue over tone or ITA is never tested, and L* and h* are correlated in the data, contradicting the "orthogonal" framing.** Proposed: Major.
Sources: METH W7; A12; B15 (odds ratio 0.56–0.68 in the in-the-wild datasets); C10.
LOCAL: between-subject r(L*, h*) = 0.53 on MST-E.

**K11. Cropping audit: hue is confounded with ethnicity and with source dataset (CFD vs CFD-India); top/bottom position and cropper version are unreported.** Proposed: Major.
Strength to retain: the red and yellow groups have almost identical binary tone composition (61.7% vs 62.7% light), from Fig. 3 n's.
Sources: METH W8 and W21; B4; B11; C10.

**K12. Elo inference.** Proposed: Major.
- Ratings are order-dependent and unconverged.
- Faces play unequal numbers of games (about 43–87).
- Ratings are zero-sum dependent, yet t-tests treat them as independent.
- The "% preference" figures are model-implied, corresponding to Elo gaps of 75.7 and 57.9.
- The Bonferroni family is undefined.

Sources: METH W9; B5; B9; B10; C17; EIC W4.

**K13. Face verification (Table 3) gives no counts, CIs, or tests. Reconstructed counts show no difference is significant.** Proposed: Major, possibly Critical.
Sources: B1 (Critical); METH W10; C11.
LOCAL §1: the unique cell sizes are LR = 387, LY = 328, DR = 161, DY = 124. Every Fisher p is at least 0.19 for the marginal contrasts and at least 0.09 across all contrasts. The minimum detectable effect is about 4.4 pp.

**K14. ArcFace's Red/Yellow columns are swapped in Table 3.** Proposed: Major.
Exact reconstruction shows red = 521/548 = 95.07 and yellow = 431/452 = 95.35. Reported red = 95.36 is unattainable with n = 548. The swap reverses the hue direction for ArcFace and contradicts the caption's "all face verification models". FaceNet's LY value of 93.30 is unattainable; the correct value is 93.29.
Sources: B2; LOCAL §1 (independently derived by two agents).

**K15. Face verification design.** Proposed: Major.
- The rule assigning a pair to a skin group is undefined (negative pairs involve two people).
- The scikit-learn LFW loader defaults are unreported (believed to be grayscale and about 62×47; pending verification). Skin colour cannot be computed from grayscale.
- A single-threshold accuracy mixes false matches with false non-matches.

Sources: METH W11 and W17; A15; B3; B19; C11.

**K16. The causal edits are not shown to be skin-specific.** Proposed: Major, possibly Critical.
- InterFaceGAN conditional manipulation was not used.
- The directions are learned from whole-image classifiers trained on threshold labels.
- Entanglement with gender, makeup, lips, smile, or exposure would produce the same Table 4 patterns.
- Labels are assumed unchanged after editing.

Sources: METH W13; C1 (Critical); C4; C5; B6.

**K17. The "orthogonal" edit claim is contradicted by Fig. 4's own numbers.** Proposed: Major.
- The +red edit moves L* by +7.62 on one face, and +yellow moves it by +3.77.
- Only 3 faces are shown.
- The manipulation is checked with the same instrument that defined the directions.
- Edit magnitudes are unreported and asymmetric, with no dose-response.

Sources: METH W12 and W14; A12; B7; C2; C3.

**K18. Table 4 has no paired tests or CIs, over-reads small differences, and contains three internally inconsistent cells.** Proposed: Minor.
- Small differences are over-read: "male accuracy increases for all models" under +red includes AWS at +0.06 pp.
- The constant-female-share check shows f ≈ 0.631 everywhere except two places. AWS +dark "All" reads 98.27 but implies 98.43. FairFace +red/+yellow "All" values are swapped (96.97/97.16 vs implied 97.15/96.97).

Sources: METH W15; B13; B14; C7. The orchestrator verified the inconsistent cells by hand.

**K19. The generative-model comparison is not like for like, and "amplification" is only half true.** Proposed: Minor.
- P2 is less light-skewed than FFHQ (dark share 34.70 vs 33.74, p ≈ 0.04–0.06) and more red-skewed (yellow share 16.63 vs 18.12, p ≈ 3e-4).
- Masks differ: FFHQ uses dataset masks, which are themselves DeepLabV3 predictions, while the generated images need predicted masks.
- FFHQ-Ageing's "ground truth" masks are model predictions.

Sources: METH W20; B12; B17; A14; C13.

**K20. Reproducibility gaps.** Proposed: Minor.
Unreported: segmentation model details, edit strengths, generation seeds, LFW loader settings, commercial API versions and dates, cropper version, and the Elo game order.
Sources: METH W17 and W22; C9; C15; A14.

**K21. Structure.** Proposed: Minor (contract D2 = warn).
The method appears only in Supplement A.2, while background takes about 2 pages. The abstract omits the method and findings. The terminology drifts.
Sources: EIC W1 (Major), W5, W6, W7, W8.

**K22. No consolidated limitations or responsible-use discussion.** Proposed: Major for writing, Minor for method.
- Race-proxy risk: hue increases ethnic separability.
- Dual use of skin-colour editing directions.
- Non-consented web images sent to commercial APIs.
- Racialised vocabulary ("yellow" for Asian subjects) and "more feminine" framing.

Sources: EIC W2 and W9; C18; C19; C20; C21; A17.

**K23. Over-generalisation.** Proposed: Minor.
"Any camera", "any face pose", "datasets and models", "previously invisible", and "data collection to model deployment" all rest on two datasets, one cropper, three verifiers on LFW, and four classifiers.
Sources: A18; C12; EIC W10.

**K24. Minor numeric slips.** Proposed: Minor.
- Table 1(b) Red total reads 81.87; it should be 81.88, since the cells are exact at N = 70,000.
- Fig. S3 says "6 points"; see K03.
- FaceNet LY; see K14.

Sources: B18; LOCAL §3.

---

## Strengths to verify (merged)

- S-a. The construct is scoped explicitly to apparent colour, as seen by a model.
- S-b. Choosing L* + h* rather than ITA avoids the shared b* component; the coordinates have a principled CIELAB-cylindrical basis.
- S-c. Code is released, and the dataset scores for CelebAMask-HQ, FFHQ and CFD are released.
- S-d. Fig. 3 prints per-group n's, and the red and yellow groups have balanced binary tone composition.
- S-e. Tone × hue intersections are tested with Bonferroni correction.
- S-f. The edits are compared with reconstructed images rather than originals.
- S-g. The "pale" direction is used as a discriminant contrast.
- S-h. The contrast confound is examined (RMS contrast, Fig. S4).
- S-i. Results are split by F/M and S/NS.
- S-j. The CFD benchmark is consented and controlled-capture.
- S-k. Ethical framing of gender classification.
- S-l. Candid statement of the reconstruction limitation.
- S-m. Histograms beyond binary cuts (Fig. S6).

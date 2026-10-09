# Field Analysis Report

**Phase**: 0 (field_analyst_agent), ARS academic-paper-reviewer v3.23.0
**Mode**: `methodology-focus`. Active panel: Journal-Fit Reviewer (internal role `EIC`, Card #1) and Peer Reviewer 1 (Methodology, Card #2). Cards #3 and #4 are included as the agent definition requires, but they are **INACTIVE** in this mode.
**Sprint contract in force**: `reviewer/reviewer_methodology_focus/v2`. D1 `methodology_rigor` is mandatory and owned by `methodology` (Card #2). D2 `writing_and_structure` is normal priority and owned by `eic` (Card #1).
**Review target binding**: `criteria_binding_unavailable`. The author did not confirm a Review Target Context. Venue strings found in the manuscript are treated as data, not as a binding target: the arXiv identifier `2309.05148v2 [cs.CV]` in the page-1 margin, and "ICCV" inside reference entries [44], [80] and [81]. This report makes no venue-alignment claim and does not generate venue criteria.
**Manuscript-directed text scan**: none found. A full read of the extraction found no text addressed to reviewers, editors or automated agents. Nothing in it tries to set reviewer identity, leniency, the decision, or what to ignore. The manuscript also contains a code URL (`github.com/SonyResearch/apparent_skincolor`). It was not fetched and has not been verified.

---

## Source Caveat (read before reviewing)

- The review input is a **pypdf text extraction of a 15-page PDF**. Pages 1–9 are the main text through the Conclusion, pages 9–11 are References, and pages 12–15 are Supplementary Material A.1–A.4.
- **No figure graphics survived.** Only the captions and the in-figure numeric labels remain. The losses are:
  - Fig. 1: example faces.
  - Fig. 2: L* × h* scatter plots for CelebAMask-HQ and FFHQ.
  - **Fig. 3: Elo-score plots for the cropping study.** These are the only place where group-level Elo distributions, intersectional comparisons and any subgroup Ns would appear.
  - Fig. S2: pipeline illustration.
  - Fig. S5: CFD scatter plots by skin colour and by ethnicity.
  - Fig. S6: histograms.
- **Figures whose numeric labels survived**: Fig. 4 (L*/h* labels for 3 faces × 8 conditions), Fig. S1 (5 L*/h* pairs), Fig. S3 (8 L*/h* pairs) and Fig. S4 (5 L*/h* pairs). Some of the numbers below are derived from these labels. The mapping of labels to faces is inferred from extraction order.
- **Tables 1–4 survived as text** and were reconstructed below.
- **Equations are partially garbled.** In Eq. 1 the fraction layout was lost. In the Elo update the superscript is rendered as `10(Rj−Ri)/M`. Words are merged across line breaks in places, e.g. "thetrue", "ifj looses", "asa∗ andb∗".
- The caption of Fig. S2 is truncated ("…to get the f"). This may be an extraction artifact.
- **Panel rule**: if a claim depends on lost figure content, record it as *not verifiable from the extraction*. Do not record it as *absent from the manuscript*. Check typographic defects against the PDF before attributing them to the authors.

---

## Paper Basic Information
- **Title**: Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color
- **Authors (as printed)**: William Thong (Sony AI; corresponding), Przemyslaw Joniak (The University of Tokyo; work done as a Sony AI intern), Alice Xiang (Sony AI)
- **Abstract length**: about 140 words
- **Full text length**: about 10,900 extracted words in total:
  - Main text (pp. 1–9): about 6,500, including table cells and figure labels. Prose is about 5,500–6,000.
  - Supplement (A.1–A.4): about 2,100.
  - References: about 2,050.
- **Number of references**: 81, numbered [1]–[81]. Three are cited only in the supplement: [45] Lloyd/K-Means, [57] an artists' colour-and-light book, and [66] Sturges.

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Computer vision: algorithmic fairness and bias auditing of face-analysis datasets and models. The core contribution is a new measurement instrument used for fairness benchmarking. |
| Secondary Disciplines | (1) Colorimetry and colour science (CIELAB, individual typology angle, hue angle), including its dermatological and cosmetic uses. (2) Measurement science, i.e. how the construct "apparent skin colour" is operationalised and the validity and reliability of an automated instrument. (3) Generative modelling for counterfactual and causal evaluation (GAN inversion, latent-direction editing, diffusion and GAN sample audits). |
| Research Paradigm | Quantitative. Secondary analysis of public datasets and model outputs. The authors collected no new human-subjects data. |
| Methodology Type | Statistical Modelling / Machine Learning. It combines: (a) a proposed measurement instrument (pixel-level CIELAB extraction with clustering); (b) descriptive audits of dataset and generator distributions; (c) disaggregated benchmarking of models by subgroup, a comparative design; (d) an interventional, quasi-experimental study using synthetic counterfactual images. |
| Target Journal Tier | `criteria_binding_unavailable`. **No tier or venue is assigned.** Field-general observation only: this is a measurement-and-benchmark contribution within CV fairness, formatted as a ~9-page main text with a supplement. It should be held to the general CV-fairness peer-review bar for a new measurement instrument plus demonstration studies. That observation is about format only. It is not a venue claim. |
| Paper Maturity | Pre-submission (complete). The structure is complete (abstract, intro, background, method, three experiment families, conclusion, references, supplement), the citation format is consistent, the language is polished, and code is linked. Remaining surface issues are listed for Card #1: "Alahuf" vs ref [1] "Alaluf"; "identify" for "identity"; "ifj looses"; dataset naming switching between FFHQ and FFHQ-Ageing; a Sec. 3 cross-reference to "Figure S3" for method details; minor grammar. There is no dedicated Limitations section. |

---

## Paper Summary for the Panel (factual, non-evaluative)

**Claimed contributions** (§1):
1. A multidimensional apparent-skin-colour score for images. Perceptual lightness **L\*** measures skin *tone* and CIELAB hue angle **h\*** measures skin *hue*. The authors choose L* rather than ITA so that the two measures do not both depend on b*.
2. Showcases:
   - (i) Datasets and generative models are skewed toward light-red and under-represent dark-yellow skin.
   - (ii) Tone and hue biases appear in saliency cropping and face verification.
   - (iii) The skin-colour "causal effect" on gender and smile prediction, measured with latent-space counterfactuals.

**Construct scope stated by the authors**: the paper measures *apparent* skin colour (as depicted in the image and seen by a model), not *true/constitutive* skin colour (§1; A.1; A.2). A.1 lists factors that shift apparent colour: colour cast, illumination, low light, makeup and flushing.

### Component C0: Measurement instrument (§3, Supplement A.2, Fig. S2)
- **Definitions**:
  - ITA = arctan((L* − 50)/b*) × 180/π (Eq. 1). This is background only and is not used as the score.
  - h* = arctan(b*/a*) (Eq. 2). The text says h* ranges 0–360° and that interest is limited to 0–90° (a*, b* > 0).
  - Fig. S1 labels include negative h* values: −25.38, −14.70, −0.70 and −4.22.
- **Pipeline** (adapted from Merler et al. [48], Diversity in Faces §4.6):
  - (a) Input face image.
  - (b) Skin segmentation, either manual or from a model.
  - (c) Per-pixel conversion from sRGB to CIELAB, giving L* and h* per pixel.
  - (d) K-Means with K = 5 clusters. For each cluster, build a histogram with the bin count set by Sturges' rule, and take the histogram mode as the cluster value.
  - (e) Keep the **3 clusters with the highest L\*** to exclude facial hair and shadow. The authors motivate this with artists' five-value grouping [57].
  - (f) Average the cluster values, weighted by pixel count, to get image-level L* and h*.
- **Not stated in the extracted text**:
  - The sRGB→XYZ→CIELAB assumptions (reference white or illuminant, linearisation).
  - The feature space used for K-Means.
  - How h* is computed for pixels with near-zero chroma, and how values outside 0–90° are treated.
- **Binarisation thresholds**: L* = 60 (light/dark) and h* = 55° (red/yellow), taken from Ly et al. [46], a cutaneous-colorimetry methods paper.
- **Mask sources by study**:
  - C1: the masks provided with each dataset.
  - C3: DeepLabV3 [11] trained on CelebAMask-HQ, applied to CFD.
  - C2, C4 and C5: the extracted text does not say.
- **Validation reported**:
  - **Relighting robustness (Fig. S3)**:
    - Input: one individual, 8 images produced by the relighting network of Zhou et al. [81].
    - Text: L* varies by up to 6 points from the original, and h* is stable.
    - Surviving labels: L* ranges 59.41–71.34 (span 11.93) and h* ranges 57.08–59.12 (span 2.04).
    - Which label is the original cannot be recovered. *Derived:* if the first pair (66.63 / 59.12) is the original, the maximum |ΔL\*| is 7.22.
  - **Contrast check (A.2, Fig. S4)**:
    - Mean RMS contrast on the L* channel, computed over the §4.3 image sets: reconstructed 0.644, +dark 0.630, +light 0.652.
    - One example of a global contrast edit: +contrast L* 91.74 / h* 14.05; −contrast L* 51.10 / h* 56.56.
  - **Not reported in the extracted text**: comparison against reflectance or spectrophotometer measurements, against human Fitzpatrick or Monk annotations, a repeat-measurement (test-retest) study, or a population-level L*–h* correlation.
- **Statistical test**: none.

### Component C1: Dataset skin-colour distribution (§4.1, Table 1, Fig. 2, A.4 / Fig. S6)
- **Data**:
  - CelebAMask-HQ [43], **N = 30,000**, derived from CelebA (images crawled from social media).
  - FFHQ-Ageing [52], **N = 70,000**, derived from FFHQ. Tables and figures label it "FFHQ".
  - Both use the skin masks that ship with the dataset.
- **Output**: cell percentages after binarisation at L* 60 and h* 55°.

| % | CelebAMask-HQ Light | Dark | Total | FFHQ Light | Dark | Total |
|---|---|---|---|---|---|---|
| Red | 46.95 | 19.28 | 66.23 | 52.82 | 29.06 | 81.87 |
| Yellow | 27.48 | 6.29 | 33.77 | 13.44 | 4.68 | 18.12 |
| Total | 74.43 | 25.57 | 100 | 66.26 | 33.74 | 100 |

- **A.4**: 20-bin histograms, described as unimodal and bell-shaped. The text says alternative thresholds confirm the skew. The specific thresholds varied are not tabulated in the extraction.
- **Statistical test**: none (descriptive).

### Component C2: Generative-model output distribution (§4.1, Table 2)
- **Models**: StyleGAN3 [37] and the P2 diffusion model [13], both trained on FFHQ. **10,000 generated images per model.** The text does not say whether the authors trained the models or used released checkpoints. The skin-mask method for generated images is also not stated.

| % (L/D × R/Y) | L-R | D-R | L-Y | D-Y | Light total | Red total |
|---|---|---|---|---|---|---|
| StyleGAN3 | 53.05 | 28.71 | 13.46 | 4.78 | 66.51 | 81.76 |
| P2 | 53.29 | 30.08 | 12.01 | 4.62 | 65.30 | 83.37 |
| (FFHQ, for reference) | 52.82 | 29.06 | 13.44 | 4.68 | 66.26 | 81.87 |

- **Claim**: both generators reproduce FFHQ's skew, and P2 slightly amplifies it.
- *Derived difference, P2 − FFHQ*: red share +1.50 pp; light share −0.96 pp.
- **Statistical test**: none.

### Component C3: Saliency-based image cropping (§4.2.1, Fig. 3, A.3 / Fig. S5)
- **Model**: the Twitter saliency-cropping algorithm. The extracted text gives no version or source. The design is adapted from Birhane et al. [7] and Yee et al. [79].
- **Data**: Chicago Face Database [47] plus CFD-India [42], **N = 739 unique images**, controlled capture, informed consent stated.
  - Self-reported gender: 359 F, 380 M.
  - Self-reported ethnicity: 109 Asian, 197 Black, 142 Indian, 108 Latino, 183 White.
  - Masks: DeepLabV3 trained on CelebAMask-HQ.
- **Design**:
  - 10 gender × ethnicity groups give 45 distinct-group combinations, since C(10,2) = 45 excludes within-group pairs.
  - 500 sampled pairs per combination, **22,500 comparisons** in total.
  - Each pair is stacked vertically with white space between the faces, with aspect ratio preserved.
  - *Derived*: each group fills 9 × 500 = 4,500 appearance slots, so the number of games per image varies inversely with gender × ethnicity cell size. Those cell sizes are not reported.
  - The extracted text does not state whether top/bottom position was counterbalanced, or how many times the Elo procedure was run or reordered.
- **Outcome**: an Elo rating per image (M = 400, K = 16, initialised at 1400; sequential updates). The unit of analysis is 739 per-image Elo scores, grouped by binarised L* and h*.
- **Statistical tests and results**:
  - Light vs dark tone: independent t-test, p < 0.0001. The mean Elo corresponds to a "60.73% preference" for light.
  - Red vs yellow hue: p < 0.0001, a "58.25% preference" for red.
  - Intersectional tone × hue groups: pairwise independent t-tests with Bonferroni correction. All are significant at p < 0.01 except light-yellow vs dark-red.
  - How the percentages were derived from mean Elo is not stated. *Derived*, assuming the Elo logistic: about 76 and 58 rating points.
  - The extraction contains no skin-colour subgroup Ns, effect sizes or CIs. They may have been in the lost Fig. 3.
- **A.3 (Fig. S5, lost)**: describes CFD's distribution by self-reported ethnicity.
  - White vs Black separate on L* alone.
  - Black subjects are darker and more yellow than Indian subjects.
  - Asian subjects fall mostly on the yellow side.
  - Latino and White subjects have similar tone but more hue spread.
  - No test reported.

### Component C4: Face verification (§4.2.2, Table 3)
- **Data**: LFW [33] in the **scikit-learn pre-processed version**, test split, **1,000 pairs (500 positive / 500 negative)**.
- **Models**: ArcFace [18], FaceNet [62] and Dlib [40], run through the DeepFace repository.
- **Metric**: verification accuracy.
- **Not stated in the extracted text**: the skin-mask source for LFW; how a pair (two images, possibly of two people) is assigned to a skin-colour group; subgroup Ns; decision thresholds or loader options.

| Accuracy % | Overall | Light | Dark | Red | Yellow | L+R | L+Y | D+R | D+Y |
|---|---|---|---|---|---|---|---|---|---|
| ArcFace | 95.20 | 95.52 | 94.39 | 95.36 | 95.07 | 96.12 | 94.82 | 92.55 | 96.77 |
| FaceNet | 94.40 | 94.55 | 94.04 | 94.89 | 93.81 | 95.61 | 93.30 | 93.17 | 95.16 |
| Dlib | 94.20 | 94.41 | 93.68 | 94.71 | 93.58 | 94.83 | 93.90 | 94.41 | 92.74 |

- *Derived gaps (light − dark; red − yellow)*: ArcFace 1.13 / 0.29; FaceNet 0.51 / 1.08; Dlib 0.73 / 1.13 pp.
- **Statistical test**: none reported. No CIs.

### Component C5: Counterfactual "causal effect" on attribute prediction (§4.3, Fig. 4, Table 4, Fig. S4)
- **Data**: CelebAMask-HQ, **N = 30,000**. Ground truth is the binary CelebA gender and smiling labels, which the text says a professional company annotated.
- **Manipulation**: e4e encoder [68] with StyleGAN3 [37], following Alaluf et al. [1]. Latent directions come from InterFaceGAN [65]:
  - Train a classifier on CelebAMask-HQ for binary tone and binary hue. The labels are implied to come from the paper's own thresholded scores.
  - Sample **500,000** StyleGAN3 images and label them with that classifier.
  - Train two linear SVMs on the most confident positives and negatives to obtain directions D_tone and D_hue.
- **Edit sets**: +light, +dark, +red, +yellow, i.e. **4 × 30,000 edited images**. The baseline is the *reconstructed* image, not the original, to net out inversion error.
- **Not stated**: edit magnitude or step size, the confidence cut-off for the SVM training set, which StyleGAN3 checkpoint was used, and its training domain.
- **Models evaluated**:
  - Gender: AWS Rekognition, Microsoft Azure Face, Clarifai, FairFace model [36].
  - Smile: AWS and Azure.
  - The authors say they used the "latest available version" and give no access date.
- **Manipulation check**: qualitative. Fig. 4 shows labels for 3 faces. Derived Δ against the reconstructed image, for faces 1/2/3:

| Edit | ΔL* | Δh* |
|---|---|---|
| +light | +9.82 / +14.30 / +5.28 | −1.00 / −1.37 / −0.08 |
| +dark | −13.72 / −20.65 / −9.75 | −0.07 / +3.52 / +0.88 |
| +red | +2.17 / +7.62 / −0.81 | −10.00 / −12.87 / −13.80 |
| +yellow | −0.42 / +2.27 / +3.77 | +8.51 / +6.94 / +10.36 |
| +pale (CelebA attr.) | +7.64 / +16.05 / +8.45 | +1.11 / +7.36 / +3.51 |
| −pale | −7.01 / −16.88 / −10.75 | −3.22 / −8.60 / −4.26 |

  - Original → reconstructed: ΔL* = −5.37 / −1.08 / −2.04, Δh* = +4.04 / +1.21 / −3.11.
  - The text calls the tone and hue edits "orthogonal". No population-level ΔL*/Δh* distribution and no cosine between the two directions is reported.
- **Results, Table 4a: gender accuracy %** (F / M / All):

| Model | Reconstructed | +light | +dark | +red | +yellow |
|---|---|---|---|---|---|
| AWS | 99.67 / 94.82 / 97.88 | 99.84 / 90.66 / 96.45 | 98.84 / 97.73 / 98.27 | 99.69 / 94.88 / 97.92 | 99.63 / 94.56 / 97.76 |
| Azure | 99.78 / 95.80 / 98.31 | 99.91 / 92.59 / 97.22 | 99.11 / 97.72 / 98.60 | 99.75 / 96.01 / 98.37 | 99.78 / 95.45 / 98.18 |
| Clarifai | 95.31 / 85.94 / 91.85 | 96.04 / 80.14 / 90.18 | 93.04 / 92.20 / 92.73 | 94.72 / 86.52 / 91.70 | 96.02 / 84.53 / 91.79 |
| FairFace | 99.49 / 92.91 / 97.06 | 99.77 / 87.56 / 95.27 | 98.21 / 96.57 / 97.61 | 99.52 / 93.10 / 96.97 | 99.42 / 92.77 / 97.16 |

- **Results, Table 4b: smile accuracy %** (S / NS / All):

| Model | Reconstructed | +light | +dark | +red | +yellow |
|---|---|---|---|---|---|
| AWS | 92.80 / 93.66 / 93.26 | 94.22 / 91.58 / 92.82 | 88.80 / 96.02 / 92.63 | 96.88 / 86.38 / 91.32 | 87.97 / 96.70 / 92.60 |
| Azure | 97.29 / 80.84 / 88.57 | 98.13 / 76.36 / 86.60 | 95.59 / 86.11 / 90.57 | 99.00 / 69.76 / 83.51 | 95.18 / 87.22 / 90.97 |

- **Authors' interpretation**: lighter tone leads to more "female" predictions, so male accuracy drops (e.g. AWS male 94.82 → 90.66). Lighter tone or redder hue leads to more "smiling" predictions (e.g. Azure non-smiling 80.84 → 69.76 under +red).
- **Limitation the authors state**: reconstruction and manipulation suffer from spurious correlations (background and eye gaze change). The causal results depend on synthetic-data quality.
- **Statistical test**: none reported (no paired test, no CIs). Class counts (F/M, S/NS) are not reported.

### Ethics and data statements (as stated)
- Licences are given for CelebAMask-HQ (non-commercial research agreement), FFHQ-Ageing (CC BY-NC-SA 4.0) and CFD (non-commercial).
- CFD informed consent is stated.
- The authors disclaim gender classification as a task, citing harm to non-binary and transgender people, and report it for audit purposes only.
- There is no dedicated Limitations or Broader Impact section. Limitation statements appear in §4.3, A.1 and A.2.

---

## Recommended Target Journals (Top 3)

**Withheld: `criteria_binding_unavailable`.** No author-confirmed Review Target Context was supplied. Under the agent definition (Dimension 5) and the dispatch binding rule, this agent does not recommend, substitute or infer a venue, and does not generate venue criteria from memory. The arXiv identifier and the ICCV strings in references are observed data, not a target. The quality gate "recommended target journals match" is therefore intentionally not exercised. If the author confirms a target later, re-run Phase 0 against that context.

---

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer
**Status**: ACTIVE. Owns **D2 `writing_and_structure`** (normal priority).
**Binding**: `criteria_binding_unavailable`. Configured field-general. "Venue conventions" in D2 are read as general conventions for method-focused computer-vision papers, and no venue-fit claim is made.
**Identity Description**: A field-general senior handling editor and area-chair-level reviewer for computer-vision fairness and responsible-AI benchmarking papers. Has years of experience handling *measurement-and-audit* submissions that import instruments from other disciplines (colour science, dermatology, psychometrics) into CV. Particularly experienced with conference-format papers that put substantive method content in the supplement. Does not represent any specific venue.
**Review Focus**:
  1. **Do the headline claims match what the body delivers, in scope?**
     - Trace each headline claim to the section, table or figure that delivers it. Claims: hue "reveals additional biases" (Abstract); "measuring the causal effect" (§1 contribution iii; §4 opening summary); "previously invisible" biases and "more representative assessment" (§5).
     - Check whether the abstract and conclusion carry the qualifications the body states: the §4.3 reconstruction and spurious-correlation caveat, and the apparent-vs-true scope.
     - This is an exposition-consistency check. Whether the evidence suffices belongs to Card #2.
  2. **Can a main-text reader find the core instrument?**
     - The extraction algorithm and its validation live only in Supplement A.2 / Fig. S2 / Fig. S3. That covers segmentation, sRGB→CIELAB, K-Means with K = 5, Sturges bins, histogram mode, top-3-by-L* retention, and the relighting check.
     - §3 points readers to "Figure S3" for "details of the methodology".
     - Judge whether the paper's main contribution is specified well enough in the main text, e.g. as an algorithm box or a short main-text summary, and whether the threshold provenance (Ly et al. [46]) is explained where the thresholds are first used (§4.1 / Fig. 2).
  3. **Internal consistency and editorial accuracy.** Verify each against the PDF before attributing it to the authors.
     - "FFHQ-Ageing" (§4.1 text) vs "FFHQ" (Table 1, Fig. 2, Fig. S6, Table 2).
     - "Alahuf et al." (§4.3) vs ref [1] "Alaluf".
     - "identify" for "identity" (§4.2.2).
     - "ifj looses" (§4.2.1).
     - Eq. 2 written as arctan alongside the stated 0–360° range.
     - Fig. 2 orders the threshold labels "red vs. yellow", Fig. S5 "yellow vs. red".
     - Truncated Fig. S2 caption.
     - Minor grammar, e.g. "a representative scalar scores", "would then corresponds".
     - The term "transgendered" in the gender-classification disclaimer.
  4. **Where limitations and ethics statements are placed.**
     - There is no dedicated Limitations section. Limitations are spread across §4.3, A.1 and A.2. Licence and consent statements are spread across §4.1 and §4.2.1.
     - Assess whether readers can find them.
     - Assess whether the §5 recommendation (adopt the multidimensional measure "from data collection to model deployment") is stated together with its scope conditions.
  5. **Are tables and captions self-sufficient for a method-focused paper?**
     - Do Tables 1–4 and the Fig. 3 caption state Ns, thresholds and the test used, so that a reader can interpret, for example, a 0.29-pp gap (ArcFace red vs yellow) or the "60.73% preference"?
     - Only judge the presentation. Statistical adequacy belongs to Card #2.
     - Graphics were lost, so judge captions and text only.
  6. **Originality and significance framing, at big-picture level and field-general.**
     - Is the novelty claim worded precisely enough to distinguish the contribution? The claim: to the authors' knowledge the hue angle has not been used for CV fairness. It should be distinguished from (a) concurrent multi-category tone scales (Monk [51, 63]), (b) ITA-based CV fairness work ([36, 41, 48]), and (c) existing multidimensional cosmetic colour charts (de Rigal et al. [17]).
     - Literature completeness itself belongs to Card #3, which is inactive in this mode.
**Will particularly care about**: Whether a reader of the main paper can tell exactly what the new measure is, how it is computed, and what scope its "causal" and "previously invisible" claims carry. Whether those statements stay consistent from abstract to conclusion.
**Possible blind spots**:
- Will not audit colorimetric correctness, instrument validity, or the statistical support for the disparities. These belong to Card #2.
- Because Cards #3 and #4 are inactive in this mode, two areas get no dedicated reviewer: literature coverage, and sociotechnical implications such as hue labels acting as an ethnicity proxy and the colour terminology. Card #1 may touch them only through framing. The synthesizer should list them as *not reviewed*, not as *no issues*.

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1
**Status**: ACTIVE. Owns **D1 `methodology_rigor`** (mandatory).
**Binding**: `criteria_binding_unavailable`. Evaluates against the general peer-review bar for CV fairness and measurement work. No venue claim.
**Identity Description**: A measurement scientist working at the intersection of **applied colorimetry and image-based colour measurement** and **algorithmic-fairness evaluation statistics**.
- **Colour science**: CIE colorimetry and camera colour pipelines (sRGB encoding and linearisation, XYZ, CIELAB with its reference-white assumptions, hue-angle computation and its instability at low chroma). Has validated image-derived skin-colour estimates against spectrophotometric and colorimeter reference measurements.
- **Measurement theory**: psychometric and metrological validity and reliability frameworks for new instruments. This covers convergent and discriminant validity, test-retest and inter-capture reliability, measurement invariance across groups, and how measurement error propagates into binarised subgroup labels.
- **Evaluation statistics**: disaggregated evaluation with uncertainty (bootstrap and Wilson CIs, paired tests such as McNemar, multiple-comparison control, subgroup power). Also paired-comparison models (Elo / Bradley–Terry).
- **Causal evaluation**: causal inference with **generative-model counterfactuals**. This covers GAN inversion (e4e), InterFaceGAN-style linear directions, manipulation checks, attribute entanglement and off-manifold artifacts.
**Review Focus**:
  1. **Colorimetric specification and correctness of the instrument** (§3, A.2, Eq. 1–2):
     - The sRGB→CIELAB conversion assumptions are not stated: reference white or illuminant, gamma linearisation, and how uncalibrated, white-balanced, compressed in-the-wild images are handled.
     - Eq. 2 is written as arctan(b*/a*), whose range is (−90°, 90°), yet the text claims 0–360°. Was the quadrant-aware atan2 used?
     - Fig. S1 shows negative h* values. The paper restricts interest to 0–90°. How are such values, and low-chroma pixels where hue is ill-defined, handled in clustering, histograms, thresholds and averaging?
     - Is taking the mode of a histogram of a circular quantity well-defined here?
  2. **Free parameters of the pipeline, sensitivity, and differential bias** (A.2):
     - Free parameters: K = 5 clusters; keeping the top-3 clusters by L* (justified only by artists' value grouping [57]); Sturges bins; histogram mode; pixel-weighted averaging. The K-Means feature space is unstated.
     - Is there any ablation or sensitivity analysis?
     - Specifically: does discarding the 2 lowest-L* clusters shift L* upward *differentially* across tone groups, faces with facial hair, or poses? If so, Table 1–4 group assignments could be affected.
  3. **Validity and reliability evidence for the construct "apparent skin colour"**:
     - The only reliability evidence is synthetic relighting of **one individual (8 images, Fig. S3)**, and the relit images come from a neural network rather than real captures.
     - Reconcile the "up to 6 points" L* claim with the surviving labels. The span is 11.93, and if the first label is the original the maximum |ΔL\*| is 7.22. The figure was lost, so verify against the PDF.
     - Ask whether evidence appropriate to an apparent-colour construct was feasible and missing. Examples: consistency across multiple photos of the same identity (available in LFW); agreement with CFD's standardised captures; correlation with human Monk or Fitzpatrick ratings; error propagation from segmentation (DeepLabV3 trained on CelebAMask-HQ, transferred to CFD; unstated masks for LFW and generated images).
     - Population-level L*–h* correlation is not reported, yet the paper calls the two dimensions "orthogonal" and "complementary".
  4. **Binarisation thresholds and measurement-error propagation**:
     - L* = 60 and h* = 55° come from cutaneous colorimetry (Ly et al. [46]), which measures constitutive skin under controlled instruments. Here they are applied to apparent in-image colour.
     - How many images sit near the thresholds, and how does instrument noise (≥ 6 L* points under relighting) reclassify them?
     - Do the Table 1–4 conclusions hold under alternative cut-points or continuous analysis? A.4 states alternative thresholds "confirm" the result, but does not show which thresholds or what they changed.
     - The mask source differs between studies (dataset masks, DeepLabV3, unstated). Is the instrument therefore not the same instrument across studies?
  5. **Design and inference in the cropping benchmark** (§4.2.1, Fig. 3):
     - Elo is order-dependent with K = 16. Was it a single pass or averaged over permutations?
     - The number of games per image differs by gender × ethnicity cell size (each cell fills 4,500 slots).
     - Pairs are balanced on gender × ethnicity, not on skin colour, so tone and hue groups are confounded with ethnicity, gender and capture properties.
     - Top/bottom position counterbalancing is unstated.
     - The unit of analysis and independence assumption: 739 Elo scores that share games.
     - Are t-test assumptions met?
     - How was "60.73% / 58.25% preference" derived from mean Elo?
     - Subgroup Ns, effect sizes and CIs are not in the extracted text, though they may be in the lost Fig. 3.
     - How many intersectional comparisons does the Bonferroni family cover?
     - Would a Bradley–Terry or mixed-effects paired-comparison model be the more defensible estimator?
  6. **Face verification inference** (§4.2.2, Table 3):
     - Only **1,000 LFW test pairs** exist. How was each pair assigned to a skin-colour group: by both faces, one face, or same-group pairs only? Group Ns are unreported.
     - There are no CIs or tests, yet the text interprets gaps of 0.29–1.13 pp. Are these within sampling noise?
     - The D+Y cell is *highest* for ArcFace (96.77) and FaceNet (95.16), while the marginal narrative says light and red are favoured. How do the authors reconcile this?
     - Separate false-accept and false-reject rates are not reported.
     - DeepFace thresholds and detector/alignment defaults are unstated.
     - Check the loader settings, outside knowledge to verify: scikit-learn's `fetch_lfw_pairs` defaults to `color=False` (grayscale), `resize=0.5`, and a fixed central crop (roughly 62×47 px). Confirm that colour was enabled, and assess whether such low-resolution crops support skin segmentation and CIELAB estimation.
  7. **Identification in the counterfactual "causal effect" study** (§4.3, Fig. 4, Table 4):
     - The estimand is really "the effect of a fixed-magnitude InterFaceGAN latent edit". When does that equal "the causal effect of skin colour"?
     - The manipulation check is **3 qualitative faces**. In those, +red raises L* by 7.62 on face 2, +dark shifts h* by +3.52, and +yellow raises L* by up to 3.77. No population-level ΔL*/Δh* distribution or direction cosine is reported.
     - **Circularity**: the instrument defines the classifier labels that create the directions, and the same instrument then verifies that the edits worked.
     - Entanglement: do the tone and hue directions co-vary with femininity cues, makeup, age, lighting or expression? Such co-variation would offer an alternative explanation for the gender shift ("+light → more female") and the smile shift. A.2 shows global contrast also changes.
     - Unstated: edit magnitude, whether magnitude is matched across directions, the SVM confidence cut-off, and the StyleGAN3 checkpoint and training domain (CelebAMask-HQ images inverted into a generator trained elsewhere?).
     - Comparing against the reconstructed image controls for inversion error but not for artifacts the edit introduces.
     - The design is paired (same 30,000 images) but no paired test or CI is reported, and class Ns are absent.
     - Commercial API versions and access dates are unstated.
  8. **Descriptive audits of datasets and generators** (§4.1, Tables 1–2):
     - Is the "P2 slightly amplifying the bias" claim defensible? Derived: red share +1.50 pp, but light share −0.96 pp against FFHQ, based on 10,000 samples with no uncertainty reported.
     - The skin-mask method for generated images is unstated.
     - Are dataset-provided masks and model-predicted masks comparable?
     - Does measurement error, rather than sampling error, dominate the uncertainty in these large-N percentages?
  9. **Reproducibility affordances**:
     - Code is linked but was not verified.
     - Missing parameters: edit step sizes, SVM selection rule, Elo ordering and seeds, number of runs, DeepFace and LFW loader options, mask models for LFW and generated images, API versions and dates.
     - The Twitter cropping model has no source or version.
     - Can a third party regenerate Tables 1–4 from what is specified?
**Will particularly care about**: Whether (L*, h*), as this pipeline extracts it from uncalibrated in-the-wild images, is a *valid and reliable* measure of apparent skin colour. Whether the downstream disparities, many of them 1–2 pp or less and reported without uncertainty, and the "causal effect" conclusions survive instrument error, threshold sensitivity, subgroup sample sizes, and entanglement of the generative edits.
**Possible blind spots**:
- May hold an apparent-colour instrument to *constitutive* (spectrophotometric) standards. The paper explicitly scopes itself to apparent colour, so requests should be calibrated to evidence that is feasible for that construct.
- May underweight sociotechnical construct concerns (the meaning and terminology of "red/yellow" hue groupings, ethnicity proxying) and the paper's novelty relative to the literature. Cards #3 and #4 would cover these but are inactive, so the synthesizer should mark them as uncovered.

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2
**Status**: **INACTIVE in `methodology-focus` mode.** It is emitted per the agent definition. It is not dispatched and owns no contract dimension.
**Identity Description**: A senior researcher in fairness auditing of face-analysis systems and **skin-tone annotation for ML datasets**. Has worked on Fitzpatrick and Monk scale annotation reliability, auditing in the Gender Shades lineage, and causal benchmarking of bias in face analysis with synthetic counterfactuals.
**Review Focus**:
  1. Literature completeness on skin-colour measurement for ML. Examples: the Monk Skin Tone scale and annotation studies [51, 63]; expert/crowd/algorithm annotation comparisons [28]; scene-disambiguated skin-tone estimation [23]; Casual Conversations [31]; Diversity in Faces' ITA pipeline [48]. Also any later work on multi-dimensional or hue-aware skin-colour descriptors.
  2. Whether the contribution goes beyond Merler et al. [48] (pixel clustering with ITA) and beyond cosmetic multi-dimensional colour charts [17] in a way the field would recognise as new.
  3. Whether the downstream tasks are current and representative of deployed CV practice: Twitter cropping, LFW verification with ArcFace / FaceNet / Dlib, and CelebA gender and smile. Do the findings replicate or contradict prior disaggregated audits ([7], [79], [29], [4], [60])?
**Will particularly care about**: Whether "hue as a fairness axis" is positioned accurately against concurrent skin-tone-scale work, and whether the empirical showcases add knowledge beyond existing audits.
**Possible blind spots**: Measurement-theoretic and colorimetric detail (Card #2), and the normative and terminology questions (Card #4).

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3
**Status**: **INACTIVE in `methodology-focus` mode.** It is emitted per the agent definition. It is not dispatched and owns no contract dimension.
**Identity Description**: A social scientist of race, colourism and **skin-colour stratification measurement**, with experience building and validating observer-rated skin-colour palette instruments in survey research. Also has practical experience in responsible-AI data governance: dataset documentation and the regulation of sensitive-attribute proxies.
**Review Focus**:
  1. Do the "red/yellow" hue categories, and the A.3 ethnicity-level reading (Asian subjects "mostly in the yellow side"), risk reviving historically racialised colour terminology? Should neutral descriptors or continuous reporting be preferred?
  2. Does a second colour axis turn the measure into a more precise **ethnicity proxy**? The paper itself motivates tone as a race proxy (§1) given data-protection limits [22]. What governance or usage guidance should accompany the release?
  3. Practical adoption: how the measure would enter datasheets and model cards [25, 50] and dataset-collection specifications (§4.1 recommendation; §5). Also its limits for social-media-crawled data under non-commercial licences, and for non-face, human-centric tasks proposed in §5.
**Will particularly care about**: Whether the instrument's categories and recommended uses could cause representational harm or enable covert demographic inference, separately from whether the measure is technically valid.
**Possible blind spots**: Technical validity of the colour pipeline and of the statistical inference (Card #2).

---

## Review Strategy Recommendations
- **Mode coverage**:
  - Only D1 (Card #2) and D2 (Card #1) are scored under `reviewer/reviewer_methodology_focus/v2`.
  - The focus areas of Cards #3 and #4 (literature and novelty audit; sociotechnical, terminology and proxy-governance concerns) are **not reviewed** in this run. The fixed Devil's Advocate seat is not in the methodology-focus panel, per the SKILL.md mode table.
  - The synthesizer should report these as coverage gaps and not infer that no issues exist. The "red/yellow" terminology and proxy questions fall outside D1 and are listed under Card #2's blind spots.
- **Binding**: every active seat must disclose `criteria_binding_unavailable`. Card #1 reads D2's "venue conventions" as general conventions for method-focused computer-vision papers and makes no venue-alignment claim.
- **Treat the paper as an instrument plus demonstrations**:
  - Card #2 should judge D1 on two layers: (a) instrument specification, validity and reliability (C0), and (b) inferential rigor of each demonstration study (C1–C5).
  - Most quantitative claims are descriptive or have no uncertainty. Only C3 reports hypothesis tests. Card #2 should separate claims that are inferentially supported from claims that are only directional.
- **Apparent vs true colour**: both seats should judge against the paper's declared construct (apparent colour). A spectrophotometric ground truth is not a precondition. Validity evidence that is feasible for this construct is a legitimate request: same-identity consistency, agreement with controlled CFD captures, and human-rating correlation.
- **Division of labour on the supplement**:
  - Card #1 judges whether the instrument is *placed and specified readably* in the main text (D2).
  - Card #2 judges whether the specification is *complete and correct* wherever it appears (D1).
  - The same gap (e.g. unstated sRGB→CIELAB assumptions) should be scored once, in D1. D2 covers only how it is presented.
- **Lost figures**: Fig. 3 (cropping Elo distributions), Fig. 2 / S5 / S6 (distributions) and S2 (pipeline) cannot be checked. Findings that depend on them must say "not verifiable from extraction". Recovered labels from Fig. 4, S1, S3 and S4 (tabulated above) may be used, with the caveat that the label-to-face mapping was inferred.
- **Points where the two seats may diverge**:
  - Card #1 may see the paper as polished and complete (pre-submission maturity), while Card #2 may find load-bearing method details only in the supplement or missing entirely. The synthesizer should keep the two dimensions separate.
  - Card #2's strictest items concern whether the instrument is valid (focus 1, 3, 4) and whether the causal design is identified (focus 7). These are the dimensions most likely to decide D1.

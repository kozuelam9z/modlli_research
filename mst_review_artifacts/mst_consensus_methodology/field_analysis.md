# Field Analysis Report

**Run mode**: methodology-focus (active panel: Journal-Fit Reviewer [internal role EIC] + Peer Reviewer 1 [Methodology]). Cards #3 and #4 are emitted per the agent definition but are **inactive** in this mode.
**Review target binding**: `criteria_binding_unavailable`. No author-confirmed Review Target Context was supplied. Venue observations below are field-general only.
**Source caveat**: the manuscript is a text extraction of a 30-page PDF. Figures did not survive, only their captions. Several key numbers (per-region ICCs in Fig. 3, Spearman-Brown curves in Fig. 5, confusion matrices in Fig. 8, Open Images vs MST-E distributions in Fig. 6) are therefore not inspectable. Reviewers must state which claims they could and could not verify against the text.

## Paper Basic Information
- **Title**: Consensus and Subjectivity of Skin Tone Annotation for ML Fairness
- **Abstract length**: ~258 words (single paragraph plus a findings paragraph)
- **Full text length**: ~13,950 words in the extraction (main body to references ~6,000; references ~2,900; appendices A-L ~5,000)
- **Number of references**: 86 (numbered [1]-[86])
- **Observed venue strings (data, not a binding target)**: the footer reads "37th Conference on Neural Information Processing Systems (NeurIPS 2023) Track on Datasets and Benchmarks" and carries a DOI and proceedings page numbers. Appendix L states a prior rejection at FAccT 2023. Both are recorded as manuscript content. Neither is used for criteria binding.
- **Instruction-boundary check**: no imperative text aimed at reviewers or the panel was found (no directives about leniency, decision, reviewer identity or what to ignore). Appendix L ("Addressing previous reviews") is a persuasive author response to earlier reviewers. Treat each "we addressed X" statement in it as a claim to verify against the main text, not as a resolved concern.

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Machine-learning fairness / responsible computer vision, specifically **human annotation methodology for perceived demographic attributes** (dataset-and-benchmark contribution: MST-E dataset + annotation study) |
| Secondary Disciplines | Psychometrics / measurement of rater agreement (ordinal rating reliability, crowdsourcing design); colour science and visual perception (colour constancy, illumination, display conditions); sociology of colorism / cross-cultural social perception |
| Research Paradigm | Quantitative (with a small exploratory expert component; one pilot with dermatologists is described only qualitatively) |
| Methodology Type | Survey/annotation experiment with repeated ordinal ratings (inter-rater reliability study + criterion comparison against a single expert "oracle"); between-group comparison of annotator regions (Mann-Whitney U per image, MANOVA, a chi-square/V-type test on Open Images); reliability projection (Spearman-Brown); dataset release with data card. Secondary: a small pixel-based baseline (RGB nearest-swatch) in Appendix G |
| Target Journal Tier | `criteria_binding_unavailable`. Field-general observation: in polish, scope and documentation the manuscript sits at the level expected of a top-tier archival ML/fairness venue (Q1 / A*-conference equivalent). The self-declared NeurIPS 2023 D&B string is noted but not adopted as a target, and no venue-specific criteria are applied |
| Paper Maturity | **Pre-submission / final (published camera-ready)**. Rationale: complete IMRaD-style structure, consistent numbered citations, data card, maintenance plan, compensation disclosure, limitations/ethics section, and a response-to-prior-reviews appendix. Residual polish issues are mostly in reporting precision (unnamed test statistics, missing CIs, ICC form ambiguity) and data-card copy errors, not in structure |

### Paper summary for the panel (factual, no evaluation)
- **Dataset (MST-E)**: 19 TONL-sourced subjects spanning MST 1-10 (1-3 subjects per MST point; MST7 and MST10 have one subject each), 1,515 images and 31 videos shot within a 4-hour window per subject across poses, expressions, lighting and masks. One "intended/oracle" MST value per subject, set by Dr. Ellis Monk (the scale's creator and a co-author) after first-pass annotation by an author. Monk also chose one Golden image per subject. The authors curated a matching Challenging (worse lighting) image per subject.
- **Study 1 (experts)**: 5 photographers in India and 5 in the US (recruited via GLG). 50 images per session: 19 targets (18 analysed because one subject was dropped for a programming error) plus 31 distractors. Golden session first, Challenging session about 1 week later, in a fixed order. Analyses: two-way random single-score ICC; per-image Mann-Whitney U (36 tests, 3 significant at p<.05); % of medians within ±1 of the oracle (88.9% India, 83.4% US) and average median distance (0.78 / 0.84).
- **Study 2 (crowd)**: trained vendor annotators in India, Philippines, Brazil, Hungary and Ghana, 5 per region, 25 per image, on all of MST-E plus 86,809 faces from 41,471 Open Images photos. Analyses: one-way random single-score ICC (per subject 0.86-0.94, Golden 0.90-0.96, Challenging 0.82-0.95); MANOVA with region as the IV (Pillai = 1.97, p<.05); within-±1 = 94.7% (18/19 subjects); average median distance 0.78 (well and poorly lit); Spearman-Brown projection leading to a "10 annotators (2 × 5 regions)" recommendation; Open Images ICC 0.875-0.91, ICC-equality χ² = 0.26 (p = .99), region difference "V² = 0.0766, p<.05". Cost about $780k.
- **Headline claims**: (a) trained crowds and photographers annotate MST reliably; (b) annotators are, "with training", invariant to lighting; (c) region shapes annotation, yet a geographically diverse pool's median matches the creator's intent; (d) practitioner guidance; (e) dataset release.

## Recommended Target Journals (Top 3)
`criteria_binding_unavailable`. No author-confirmed target exists, so no specific journal or venue fit is asserted and no venue criteria are generated from model memory. The field-general venue *classes* this work belongs to are:
1. **Datasets-and-benchmarks tracks of major ML conferences**, for the MST-E dataset plus annotation-protocol contribution. Field-general expectations: dataset documentation, licensing coherence, accessibility, maintenance, and reproducibility of reported analyses from released artefacts.
2. **Sociotechnical fairness and accountability venues (conference or journal)**, for the subjectivity/perspectivism framing and the practitioner guidance. Field-general expectations: construct validity of the measured attribute, positionality of the ground truth, and normative argument.
3. **Human computation / crowdsourcing and CSCW-type venues**, for the replication-count and annotator-pool-composition findings. Field-general expectations: rater-population description, task design, quality control, and reliability methodology.

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer
**Contract ownership (methodology-focus contract)**: D2 `writing_and_structure`
**Identity Description**: Senior area chair / associate editor for dataset-and-benchmark and responsible-AI submissions at top-tier ML venues (field-general, not bound to a named venue). Has handled human-annotated demographic-attribute datasets (perceived gender, age, skin tone) and is fluent in data-card / datasheet documentation, dataset licensing and access policy, and consent for releasing identifiable people imagery. Has also adjudicated reviewer conflicts where a dataset's ground truth comes from an author.
**Review Focus**:
  1. **Contribution delineation versus prior skin-tone annotation work**: separate what is new (MST-specific, multi-region crowd at 25×, curated lighting-paired exemplar set, Open Images transfer) from what replicates the known FST result that crowd and expert land within about 1 point (Groh et al. [33,34]; Krishnapriya et al. [48]). Check that the abstract and Conclusion (a)-(e) claim no more than the evidence supports. In particular, "with training, can provide annotations invariant to lighting conditions" has no training manipulation, and "aligns with an expert ... even under challenging environmental conditions" rests on one Challenging image per subject.
  2. **Dataset-track hygiene and internal consistency of the release**: (i) license coherence: the images and annotations are declared "CC BY", yet the same text restricts use to research, model evaluation or annotator training and forbids model training. CC BY does not carry such field-of-use restrictions, and §3 lists "model evaluations" while Appendix I omits it. (ii) Data-card copy errors: "Data Subject(s): Data about image search queries"; a blank "Number of unique annotations" for the crowd workforce. (iii) Access requires a Google account, which the paper frames as a misuse mitigation; weigh this against open-access norms. (iv) Released crowd CSV fields (subject, image, region, annotation) carry no annotator ID or lighting/condition join. Expert annotations, Open Images annotations and analysis code are not stated as released, so reported ICC forms and rater-effect analyses cannot be reproduced from the artefacts.
  3. **Writing and structure (D2)**: the load-bearing quantities live only in figures (per-region ICCs, Spearman-Brown curves, confusion matrices). Statistical reporting omits ICC form (consistency vs absolute agreement), CIs, degrees of freedom, and the names of the tests behind "χ² = 0.26" and "V² = 0.0766". Small numeric inconsistencies (83.4% where 15/18 = 83.3%; "19 subjects" vs 18 analysed in Study 1) and a reversed MANOVA sentence ("subject annotations were a significantly high predictor of the region") need correcting. Scare-quoted "experts" and the shifting terms "oracle", "intended", "golden" and "ground truth" should be harmonised.
  4. **Governance and conflict of interest**: the criterion ("oracle") annotator is a co-author and the scale's creator, and the authors' institution maintains the scale. Check that this is disclosed where the accuracy claims are made, not only in Appendix L. Ethics: "guidance of our institution's ethics body" gives no approval identifier. Compensation disclosure (Appendix K) is unusually complete; credit it.
**Will particularly care about**: Whether the paper's two framings are reconciled at the level of claims a reader will act on. It argues skin tone is subjective and culturally situated, then scores annotators by distance to one person's labels and recommends a 10-rater protocol to practitioners.
**Possible blind spots**: Will not adjudicate whether ICC(1,1), MANOVA or the ±1 metric are statistically appropriate (deferred to R1). May over-weight dataset-track packaging (license, access, data card) relative to whether the annotation science holds. With figures missing from the extraction, may under-estimate how much evidence the figures actually carry.

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1 (Methodology)
**Contract ownership (methodology-focus contract)**: D1 `methodology_rigor` (mandatory; any block/warn drives the F1-F3 decision rules)
**Identity Description**: Quantitative psychometrician specialising in reliability and agreement for **ordinal perceptual ratings**: ICC forms (Shrout-Fleiss / McGraw-Wong), generalizability theory with crossed and nested facets, Krippendorff's α (ordinal metric), weighted κ and Gwet's AC2, and cumulative-link (ordinal) mixed models with crossed random effects for items and raters. Has designed multi-site crowdsourced labeling studies for subjective attributes, including rater-pool composition, qualification and gold-question QC, and replication-count planning via k-rater reliability (Wong & Paritosh [83]). Has working knowledge of colour-appearance measurement as it affects human colour judgments: display calibration and gamut, ambient viewing conditions, colour constancy and illuminant discounting, CIELAB / ΔE00.
**Review Focus**:
  1. **ICC specification, design fit, and inflation by stimulus design**.
     - Study 1 uses a "two-way random, single score ICC" without saying whether it is consistency or absolute agreement. Only absolute agreement speaks to annotators agreeing on the *same MST value*.
     - Study 2 uses one-way ICC(1,1) on the grounds that raters vary by image. But vendor annotators on monthly contracts form small, recurring teams, so the design is partially crossed and nested (raters within region). A crossed-random-effects / G-study decomposition (subject, image-within-subject, rater-within-region, region, residual) is the appropriate model.
     - "Per Subject" ICC is undefined: is it within a subject across its images (where the true target variance is near zero), or at the subject level after aggregation?
     - The Golden set has 19 targets deliberately spread one or two per MST point. That maximises between-target variance and mechanically inflates ICC relative to realistic distributions. This matters when comparing to Open Images, which is heavily light-skewed (Fig. 6).
     - Every ICC is reported as "significant, p<.05" against a null of zero, which is uninformative. Require CIs and interpretation against agreement benchmarks.
     - The ICC treats a 10-category ordinal scale as interval. Ask for an ordinal-metric α or polychoric/ordinal-model sensitivity check.
     - Skipped ("too hard / no skin") items create an unbalanced design whose handling is unstated.
  2. **Criterion validity against a single-expert oracle and the agreement metrics**.
     - The oracle is one rater with no reported test-retest reliability. Labels were proposed by an author first, then confirmed (an anchoring risk). One label per subject is applied to every image of that subject regardless of lighting, so "accuracy" conflates perception of the image with knowledge of the person.
     - The ±1 tolerance is imported from 6-point FST work [33,34]. Its meaning on a 10-point scale (3 of 10 categories accepted) and its chance baseline (e.g., a permutation or uniform-guess null, or an always-predict-middle baseline) are not given.
     - The unit of analysis is n = 18-19 subjects, so 94.7% = 18/19. "Average median distance" is an unsigned mean over medians that pool 25 ratings and, per subject, many images. Aggregation pulls medians toward the centre, and no CIs or bootstrap over subjects are reported.
     - No signed-bias analysis by MST level or by region is reported (Fig. 4 suggests systematic lightening at mid-scale), so "diverse pool matches intent" could depend on pool composition. There is no US crowd pool even though the scale was designed around ethnoracial variation in the Americas.
  3. **Inference on regional differences**.
     - Study 1 runs 36 per-image Mann-Whitney tests with n = 5 vs 5, heavy ties and no multiplicity control. Three hits at α = .05 is roughly what chance predicts: expected 1.8, and P(≥3 | null) ≈ 0.27. Yet these images are highlighted (Fig. 4) as "suggestive evidence".
     - Study 2's MANOVA is under-specified. What is a row, when raters differ per image? What are the DVs (19 subject-level annotations?), the df, and the assumption checks (multivariate normality on ordinal 1-10 data, independence)? The direction of inference is reversed in the text. The claim of "enough statistical power" comes without a power analysis. No effect size in MST units or post-hoc region contrasts are given.
     - On Open Images, "V² = 0.0766" is unnamed (presumably Cramér's V). With about 2.2M annotations any difference is "significant". The effect size is small and needs practical interpretation. The ICC-equality test (χ² = 0.26) is unnamed.
     - Region is confounded with vendor site, trainer and training materials, team, language, and display hardware, so "region as proxy for cultural context" is not identified.
     - The preferred analysis is a cumulative-link mixed model, MST ~ region × lighting × MST-level + (1|subject/image) + (1|rater), with region-specific thresholds.
  4. **Lighting-invariance and training claims: design confounds and leakage**.
     - In Study 1, condition is perfectly confounded with session and order (Golden always first, Challenging about 1 week later, no counterbalancing, no intra-rater test-retest on identical images).
     - "Challenging" is one author-curated image per subject with no quantified illumination (exposure, correlated colour temperature, luminance). The released CSV has a `lighting` field that could support a full-dataset lighting analysis but is not used.
     - Claim (b) "with training" has no untrained control and no pre/post comparison. Crowd training materials, qualification thresholds and in-production QC are not described.
     - Leakage risk: were MST-E images (the evaluation set) used to train these same annotators?
     - With 1,515 images of only 19 faces, mixing them into "a much larger set" may not prevent subject recognition. Recognition would let annotators propagate a remembered label across lighting conditions and inflate apparent invariance. Ask for an analysis of within-subject label stability versus annotator exposure order.
  5. **Replication-count recommendation (Spearman-Brown → "10 annotators")**.
     - Spearman-Brown assumes exchangeable, parallel raters. The paper's own MANOVA finding of systematic regional differences violates that, yet k is counted across regions.
     - The recommendation could be validated directly by subsampling the observed 25 ratings: bootstrap k ∈ {1..25} drawn with and without region stratification, measuring agreement of the k-median with the 25-median and with the oracle. That check is not done.
     - Also check the recommendation's dependence on these five specific regions, and its tension with the "use co-located annotators" advice.
  6. **Colour-measurement conditions of the human task and the pixel baseline**.
     - No control or report of display calibration, brightness or ambient viewing conditions for experts or crowd, which are known moderators of colour judgments across sites.
     - The swatch rendering in the task (MST spheres vs flat patches) is not specified.
     - The Appendix G baseline (mean RGB, L2 distance to sRGB swatches, no white balance) is perceptually non-uniform and illumination-naive. It supports "naive pixel methods fail" but not a broader claim against automated estimation. ΔE00 in CIELAB after illuminant estimation (cf. Feng et al. [25]) is the fair comparator.
  7. **Sampling and generalisation limits that bound the claims**.
     - 19 subjects, with single subjects at MST7 and MST10. Images are nested within subjects, so image-level tests are pseudo-replicated.
     - Five raters per region per item. Rater demographics are not reported (own-group effects are untestable).
     - Expert n = 5 per country.
     - Open Images has no oracle, so it can test reliability and regional difference but not validity. Yet the Discussion generalises the "matches creator's intent" conclusion to in-the-wild data.
**Will particularly care about**: Whether the headline "reliable and aligned with the expert" survives (i) the correct ICC form with CIs on a design not engineered to maximise between-target variance, (ii) a subject-level bootstrap and a chance baseline for the ±1 metric, and (iii) a rater-and-image-aware ordinal model in which region, lighting and their interaction are estimated with effect sizes in MST units rather than as bare p<.05 statements.
**Possible blind spots**: Will judge the oracle mainly as a single-rater reliability and validity problem and may under-weight the normative question of whose perception should count (left to the inactive R3 angle and to the Journal-Fit Reviewer's framing check). May demand psychometric apparatus (G-studies, ordinal mixed models) beyond dataset-track norms. The synthesizer should separate "fatal to claims" from "would strengthen". Cannot inspect the ICC values or confusion matrices that exist only in the missing figures.

### Reviewer Configuration Card #3 (inactive in methodology-focus mode)

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2 (Domain)
**Identity Description**: Computer-vision fairness researcher who builds and audits demographic-attribute annotations for disaggregated evaluation (FST/ITA/MST skin tone, perceived gender and age). Familiar with the crowd-vs-dermatologist FST literature, image-based skin-tone estimation, and data-perspectivist / annotator-modelling work in NLP and affective computing.
**Review Focus**:
  1. Literature completeness: measurement-modelling and construct-validity framing of fairness attributes; perspectivist and disagreement-preserving annotation; prior FST crowd/expert agreement studies and their tolerance conventions; image-based skin-tone estimation with illumination correction.
  2. Whether the 10-point MST choice is justified for downstream disaggregated evaluation (bin sparsity, merging conventions). Appendix L declares scale-length questions out of scope.
  3. Whether MST-E's stated secondary use as a model-evaluation set is sound with 19 identities and no training permission.
**Will particularly care about**: Whether the practitioner guidance is genuinely new relative to existing perspectivist annotation guidance, or a domain instantiation of it.
**Possible blind spots**: Accepts ML-community reliability conventions (ICC, ±1) without psychometric scrutiny. May not question the region-as-culture construct.

### Reviewer Configuration Card #4 (inactive in methodology-focus mode)

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3 (Cross-disciplinary / Practical)
**Identity Description**: Cultural sociologist of colorism and racial classification with comparative work across Latin America, South Asia, West Africa and Southeast Asia, using interviewer-rated skin-colour palettes in survey research (e.g., interviewer-effect literature in colour ratings).
**Review Focus**:
  1. Whether "annotator region" is theorised as a cultural mechanism (local colour categories, reference-group norms, colourism hierarchies) or merely observed as a site effect. What the observed directional shifts would mean sociologically.
  2. The normative status of the "creator's intent" as ground truth for a construct framed as socially perceived, and the implications for deploying region-matched versus globally mixed annotator pools.
  3. Interviewer-effects precedents in survey research on skin-colour ratings, as an independent evidentiary base for the regional-difference finding.
**Will particularly care about**: Whether the recommendation to aggregate across regions toward a single median erases exactly the perceptual variation the paper argues is real.
**Possible blind spots**: Will not engage with ICC/MANOVA mechanics or dataset-release logistics.

**Coverage note (highly cross-disciplinary paper)**: CV fairness is the core domain (R2). Psychometrics plus colour-measurement conditions are concentrated in R1 because R1 is the only active substantive seat in this mode. Sociology of colorism is the distinct R3 angle. The colour-science items were deliberately folded into R1 rather than R3 so they are not lost while R3 is inactive.

## Review Strategy Recommendations
- **Figures are missing; enforce verification honesty.** R1 and the Journal-Fit Reviewer should mark every claim that depends on Fig. 3, 5, 6 or 8 as "not verifiable from extraction" rather than inferring values. The text gives only ICC ranges, so per-region and per-condition comparisons cannot be audited.
- **The central tension to resolve**: the paper's subjectivity framing (regional mental models are real) against its validity framing (accuracy = distance to one co-author's labels, and a diverse median "matches intent"). R1 owns whether the evidence supports each claim. The Journal-Fit Reviewer owns whether the abstract, Conclusion and practitioner guidance state the tension honestly. They should not duplicate each other: R1 on estimation, the Journal-Fit Reviewer on claim wording and disclosure.
- **Likely D1 severity anchors for R1's scoring plan (suggestions, not verdicts)**:
  - Candidate *block*: lighting-invariance and "with training" claims resting on an order-confounded, single-image-per-subject design with possible training/evaluation leakage; regional-difference inference resting on an unspecified MANOVA and uncorrected per-image tests.
  - Candidate *warn*: ICC form/CI/ordinal-metric gaps; ±1 metric without chance baseline or subject-level uncertainty; Spearman-Brown under a violated exchangeability assumption.
  - Candidate *fatal*: none apparent from the text alone. The reliability and Open Images findings are large-sample and plausibly robust, and the dataset contribution stands independently of the inferential weaknesses.
- **D2 anchors for the Journal-Fit Reviewer**: unnamed tests and statistics, missing CIs and df, figure-only evidence, data-card copy errors and the license contradiction are *warn*-level writing/structure issues. None alone is structural.
- **Appendix L handling**: verify each "addressed" item. Dr. Monk's identity and role are now disclosed. The expert study is now labelled "exploratory", but it still drives a highlighted figure and the regional-difference narrative. Crowd annotations are released, but without rater IDs.
- **Complementarity**: the Journal-Fit Reviewer's licensing/access/reproducibility checks and R1's reproduction requests converge on one actionable ask. Release rater-ID-keyed annotations (expert and crowd, MST-E and Open Images), the lighting/condition join, and the analysis code. That single fix would let most of R1's alternative analyses be run by readers.

contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: block
trigger: "A central agreement, subjectivity, or group-difference claim rests on an analysis that is wrong but fixable"
block_class: repairable

### D2: writing_and_structure
score: not_assessed

## Review Body

Reviewer stance: quantitative psychometrician (reliability and agreement for ordinal perceptual ratings, multi-site crowdsourced labelling design, colour-appearance conditions of human judgement), per Card #2. Only D1 is scored; D2 belongs to the eic seat.

The paper makes five claims: (a) trained crowd annotators and photographers annotate MST reliably; (b) annotators are invariant to lighting "with training"; (c) annotator region shapes MST annotation, yet the median of a geographically diverse pool matches the scale creator's intent; (d) practitioners should use about 10 annotators (2 per region across 5 regions); (e) MST-E is released for annotator training and research. The data collection is substantial and well suited to the question. Every image receives 25 ratings, balanced 5 per region, so region is crossed with items. There is a criterion reference, a controlled multi-condition shoot, and an 86,809-face in-the-wild extension. These are real design assets, and most of my concerns can be repaired with the data the authors already hold.

D1 = block (repairable). Several central claims rest on analyses that are under-specified, mis-specified, or not designed to answer the question asked. Claim (c) rests on a MANOVA whose unit of observation, df, assumptions and effect size are not stated (W1), and its region effect is not identified as "cultural context" (W2). The "diverse pool matches intent" half of (c) is never compared against single-region pools, and the aggregation rule is never varied (W6). Claim (b) rests on an untested, order-confounded comparison and has no training contrast at all (W7, W8). Claim (d) projects Spearman-Brown under assumptions the paper's own regional finding violates (W9). The criterion validity of "aligns with an expert" depends on a single, non-blind reference rater (W4) and is assessed with a lenient metric that has no uncertainty attached (W5). These go beyond warn-level reporting gaps because the analyses as specified cannot carry the conclusions drawn from them. They do not reach my fatal trigger, for four reasons: there are repeated, overlapping annotations; items are fully crossed with regions; an ethics body is named; and no headline conclusion is contradicted by the paper's own numbers. Reanalysis of the existing 25-rating design, plus re-scoping where no reanalysis can help (the training and culture attributions), would answer most of what follows.

Verification limits. The extraction contains captions only for Figures 1-6 and 8-11. I could not inspect the per-region ICC values (Fig. 3), the Spearman-Brown curves (Fig. 5), the MST-E versus Open Images distributions (Fig. 6), the oracle-versus-median confusion matrices (Fig. 8) or the pixel-baseline outputs (Figs. 9-10). Every judgement below rests on the numbers printed in the text and in the Appendix E table. Where a claim is supported only by a missing figure, I say so.

Arithmetic receipts. These were computed from my own extraction. AR1 (India 88.9% = 32/36) and AR5 (94.7% = 18/19) are consistent. AR2 (US 83.4%) is a mismatch, reported in W14. I consider AR4 (US average median distance 0.84) conservative. GRIM reachability needs only integer item values and the analytic n. With five experts rating every image, both the medians and the oracle are integers, so a signed or absolute distance is still integer-valued. Then 0.84 is not of the form k/36 or k/18 (30/36 = 0.833, 31/36 = 0.861). I raise this only in prose, and adjudication should decide it. AR3, AR6 and AR7 are not computable because the paper does not state the analytic n or the distance convention. AR8-AR10 are not computable because the test statistics are unnamed or lack df; these are reporting defects in their own right (W1, W11). As a calibration aid for W5, I used the data-card subject distribution (2, 3, 2, 2, 2, 2, 1, 2, 2, 1 subjects at MST1-10). A uniform random guess would land within ±1 of the oracle for 28.4% of subjects on average, and the best constant guess (always MST2 or always MST3) for 36.8%. The reported 94.7% is therefore far above chance. The problem with the ±1 metric is resolution and uncertainty, not chance-level performance.

### S1: Dense, region-balanced replication design
**Evidence Anchor**: text: §6 Exploration of Crowdsourced Annotations, p. 7 "Each task was replicated 5 times in each region resulting in 25 annotations per image"
Every MST-E image is rated by 5 annotators in each of 5 regions. Region is therefore crossed with items rather than confounded with item sets, which is the design property a between-pool subjectivity comparison needs. Twenty-five ratings per image also allow empirical subsampling of replication counts (see W9).

### S2: Criterion comparison beyond inter-rater reliability
**Evidence Anchor**: text: §4 The Annotation Experiment, p. 5 "we have the unique opportunity to compare annotations from the annotators to his annotations"
Most annotation studies report only inter-rater reliability. Including an external reference and two agreement-with-reference metrics is a genuine methodological advance, even though the reference itself needs strengthening (W4, W5).

### S3: Controlled capture that isolates condition from true tone
**Evidence Anchor**: text: §3 The MST Scale and the MST-E Dataset, p. 4 "collected within a short timespan of 4 hours"
Each subject is photographed within one short session across poses, expressions, masks and lighting. Image-to-image variation within a subject can then be attributed to capture conditions rather than to changes in the person. The released `lighting`, `pose` and `mask` fields make this usable for analysis.

### S4: Complete reporting of the expert per-image tests
**Evidence Anchor**: table: Appendix E Figure 7(a)-(b), full per-subject Mann-Whitney U and p listing for both image sets
All 36 tests are reported, the non-significant ones included, which is what allows the multiplicity check in W13.

### S5: Image-level crowd annotations are released
**Evidence Anchor**: text: Appendix L Addressing previous reviews, p. 29 "We release the annotations with this paper."
Releasing the individual crowd labels with their region lets others recompute the one-way reliability and the regional distributions. W12 lists what is still missing for full reproduction.

### S6: Pilot-informed, construct-driven choice of expert population
**Evidence Anchor**: text: §5 Exploration with Experts, p. 6 "were more likely to attempt to assess skin tone beneath clothing which was not depicted"
The authors piloted dermatologists and photographers. They then chose photographers because that group's approach matched the target construct, perceived tone in the image. This is good construct-validity practice.

### S7: Consensus rule suited to ordinal labels
**Evidence Anchor**: text: §4 The Annotation Experiment, p. 5 "we use the median MST annotation from the responses"
The median is an appropriate central-tendency aggregator for a 10-level ordinal scale and is robust to single outlying raters. W6 asks only that the paper show conclusions are not sensitive to this choice.

### S8: Transparent compensation and cost reporting
**Evidence Anchor**: table: Appendix K annotator compensation, per-rater monthly pay and estimated hourly wage by region
Reporting rates by region and the total cost (about $780k) supports ethical evaluation and lets practitioners budget the replication counts the paper recommends.

### S9: Reliability tested on an in-the-wild sample at scale
**Evidence Anchor**: text: §6 Extension to In-the-Wild Annotations, p. 8 "In the 41,471 images, 86,809 faces"
Repeating the reliability analysis on a large, light-skewed, uncontrolled sample partly addresses the concern that the MST-E agreement figures are inflated by the stimulus design (W15).

### W1: The regional-difference MANOVA is under-specified and its assumptions are unaddressed
**Severity**: Major
**Evidence Anchor**: text: §6 Regional Differences in Annotation, p. 8 "with annotator region as the independent variable and MST annotations for each" and "we have enough statistical power to explicitly test the effect"
**Confidence**: 4 — multivariate and ordinal modelling of rater data; design details are absent from the text

Claim (c), and the regional half of the practitioner guidance, rest on one MANOVA reported as Pillai's trace = 1.97, p < 0.05.

The unit of observation is undefined. Raters are re-drawn per image, so no single rater rated every subject. It is unclear what a row is, what the DVs are (19 subject-level annotations? averaged over which images?), and what N is. No approximate F statistic or df are given, which is why AR8 is not computable. Without N and the number of DVs, a trace of 1.97 cannot be interpreted. Under the null hypothesis, Pillai's trace has expectation p·q/(N−1), which approaches its maximum when the number of DVs nears the error df. A large trace can therefore arise from a many-DV, few-row configuration alone.

The assumptions are also unaddressed. Multivariate normality on 10-level ordinal ratings is not discussed, nor is homogeneity of covariance matrices, nor independence: all regions rate the same images, and images are nested within 19 subjects. The text states the inference backwards, calling the annotations a "predictor of the region of the annotators". It asserts "enough statistical power" with no power analysis. It gives no effect size in MST units and no post-hoc contrasts, so a reader cannot tell which regions differ, in which direction, at which MST levels, or by how much. That information is exactly what a practitioner needs.

Remedy: fit a cumulative-link (ordinal) mixed model on the 25-rating data, for example MST ~ region × lighting × oracle-MST-level + (1|subject/image) + (1|rater), allowing region-specific thresholds if warranted. Report region contrasts as latent shifts and as predicted differences in MST units with CIs. At minimum, report per-region signed mean deviation from the oracle with subject-level bootstrap CIs, and state N, df and the approximate F for any retained MANOVA.

### W2: Region is not identified as "cultural context", and the rater sample behind each region is undocumented
**Severity**: Major
**Evidence Anchor**: text: §7 Discussion and §7 Limitations, pp. 9-10 "suggesting that regional cultural contexts" and "or our annotators, beyond general geographic region"
**Confidence**: 4 — multi-site crowdsourcing design; vendor-site details are not given in the paper

Research question (b) frames location as "a proxy for cultural context and lived experience". The Discussion and Conclusion (c) then attribute differences to culture. But each region is a single vendor site, and region is perfectly aliased with that site's trainers, team, language environment, display hardware and supervision. The number of distinct raters per region is never reported ("randomly selected from a broader pool of annotators"). If each regional pool is a handful of people, the "region effect" is indistinguishable from a few individuals' rater effects. The paper also collected no annotator attributes beyond region (own skin tone, ethnicity, age, gender), so the lived-experience mechanism it invokes, including own-group perception effects, cannot be tested. The expert comparison has the same structure: country is aliased with one GLG recruitment pool each.

Remedy: report distinct rater counts and ratings per rater by region. Include a rater random effect so the region effect is estimated against between-rater variance within region. Describe site, training and hardware differences. Re-scope the cultural-influence language to something like "annotator pools recruited in different regions differ systematically". Any causal cultural attribution needs new data, such as several sites or vendors per region, or measured annotator attributes.

### W3: ICC forms, design fit and inferential reporting are unspecified
**Severity**: Major
**Evidence Anchor**: text: §5 and §6 Inter-Rater Reliability, pp. 6-7 "so we use a two-way random, single score ICC where the subject and annotator are viewed" and "As the group of annotators was not consistent from image"
**Confidence**: 4 — ICC forms and G-theory; Fig. 3 values are not inspectable

Claim (a) rests on ICCs whose specification leaves the reliability claim open.

- **Study 1 form.** Study 1 uses a two-way random, single-score ICC without saying whether it is absolute agreement or consistency. Only absolute agreement shows that experts choose the same MST value. Consistency would credit raters who rank subjects alike but are offset by one or two categories, which is exactly the regional pattern Fig. 4 is said to show.
- **Study 2 form.** Study 2 uses a one-way ICC because raters vary across images. But vendor annotators on monthly contracts plausibly recur across many images, making the design partially crossed with raters nested in region. The one-way model folds systematic rater and region bias into error and hides the region facet the paper is about.
- **"Per Subject" ICC.** This is undefined. With subject as the random effect over all of a subject's images, image-to-image (lighting, pose) and rater variance are pooled as error; the paper should say so explicitly.
- **Inference.** Every ICC is described as significant at p < .05, a test against a null of zero that is uninformative at values of 0.8-0.96. No confidence intervals are given, and with 18-19 targets the CIs for single-rater ICCs are not narrow.
- **Measurement level.** The 10-level ordinal scale is treated as interval, with no sensitivity check.

Remedy: name the McGraw-Wong form used for each analysis (for example ICC(A,1)) and report 95% CIs in place of null-of-zero tests. Add Krippendorff's α with an ordinal metric. Alternatively, add a generalizability-theory variance decomposition (subject, image within subject, rater within region, region, residual). That would also give the standard error of measurement in MST units, which tells practitioners how far an individual label typically sits from the consensus.

### W4: The criterion standard is one non-blind rater, a co-author, who also selected the evaluation images
**Severity**: Major
**Evidence Anchor**: text: §3 The MST Scale and the MST-E Dataset, p. 4 "ﬁrst annotated by an author and sent to Dr. Monk for ﬁnal golden annotations" and "an image for each subject that best represents their skin tone"
**Confidence**: 4 — criterion-validity design; the oracle's internal process is described only briefly

The reference ("oracle") is a single person, the scale's creator and a co-author. He approved labels an author had already proposed, which is an anchoring risk rather than an independent rating. His reliability is not reported (no test-retest, no second expert), and no colorimetric measurement exists to triangulate.

The same expert also chose each subject's Golden image as the one that "best represents" the subject's tone. The evaluation image is therefore selected conditional on the reference label, which favours agreement on the Golden set. A single subject-level label is then applied to every image of that subject, including the Challenging ones. "Agreement" on poorly lit images therefore measures illuminant discounting toward a person-level tone. That is a defensible construct, but the paper should state it.

Because the reference's error is unknown and the same person both set the reference and picked the stimuli, the "aligns with an expert" and "matches the original intention" claims are bounded by unquantified reference error and by possible tuning to one person's judgement. The conflict of interest is not discussed.

Remedy: obtain blind MST labels from at least two further MST-trained raters, or Dr. Monk's blind re-rating of shuffled images including the Challenging set, and report the reference's reliability. Choose any Golden-style evaluation image by a rule that is independent of the reference label. State the illumination-discounting construct. Disclose the co-author role as a limitation. If new labels cannot be collected, re-scope the wording from accuracy to "agreement with the scale creator's labels".

### W5: The ±1 tolerance and "average median distance" are lenient, ambiguous and reported without uncertainty or direction
**Severity**: Major
**Evidence Anchor**: text: §5 Distance from Intended Annotations, p. 7 "was not above the 1-point guardrail established in previous research"
**Confidence**: 4 — agreement metrics for ordinal ratings; the Fig. 8 confusion matrices are missing

**The ±1 tolerance.** It is imported from 6-point FST work [33, 34]. On the 10-point MST it accepts 3 of 10 categories, so the paper motivates MST by its finer granularity but evaluates at roughly FST resolution.

**The 1-point guardrail.** In [33, 34] this was a criterion on the proportion of ratings within one point. Here it is reused as a threshold for a mean distance, and no justification is given.

**Average median distance.** The paper does not say whether it is signed or absolute. If it is absolute and n = 36, the expert figures imply a low exact-agreement rate. India's 0.78 corresponds to a distance sum of 28 over 36 images, and the four images outside ±1 contribute at least 8. At most 20 of the 32 within-tolerance medians can then be off by one category, so exact agreement is at least 12/36 (33%). It stays below one half unless the four misses average 3.5 or more categories off. On these figures, most expert consensus labels probably do not match the reference exactly. The text never reports exact agreement, weighted κ against the reference, or signed bias by MST level or region. Fig. 4 suggests directional differences at MST6.

**Units of analysis and uncertainty.** The headline figures rest on very few units, with images nested in subjects (18 subjects × 2 sets for experts; 19 subjects for the crowd). None carries a CI. A Clopper-Pearson 95% interval for 18/19 is about 0.74-1.00, and for 32/36 about 0.74-0.97. The per-subject crowd consensus is a median over hundreds to thousands of ratings, so it is stable by construction and tends to pull toward the centre of the scale.

Remedy:
- Report exact-agreement rates, weighted κ or ordinal α between consensus and reference, and signed mean deviation by MST level and by region.
- Give confusion matrices as tables in the text.
- Add subject-level bootstrap CIs.
- Define the distance metric.
- Present ±1 agreement next to the chance and constant baselines given in the opening remarks.

### W6: "A geographically diverse pool matches the creator's intent" is never compared with single-region pools, and aggregation is never varied
**Severity**: Major
**Evidence Anchor**: text: §8 Conclusion and §6 Distance from Intended Annotations, pp. 8-10 "However, when collecting annotations from a diverse geographical pool, annotators are able" and "the average median distance to oracle annotations to be less than 1 for every region"
**Confidence**: 4 — aggregation and annotator-pool design; per-region values exist only in missing figures

The paper's own text says each single-region pool already meets its alignment criterion (average median distance below 1 "for every region"). So nothing shown establishes that diversity, rather than simply more raters (25 global versus 5 regional), produces alignment. The two are confounded. The consensus rule is fixed at the median. There is no sensitivity analysis against the mean, the mode, trimmed estimators or an annotator-aware ordinal label model, and no account of the half-integer medians that skips can produce.

This matters because it underpins the second half of Conclusion (c) and the first practitioner recommendation ("Diversity of annotators is important").

Remedy, using existing data: draw size-matched pools (5 and 10 raters) from within one region and stratified across regions. Compare their exact, ±1 and signed deviation from the reference with bootstrap CIs. Report per-region alignment numbers in the text, and repeat the key result under at least one alternative aggregator.

### W7: The lighting-invariance evidence is untested, order-confounded and rests on one author-curated image per subject
**Severity**: Major
**Evidence Anchor**: text: §5 Exploration with Experts and §3, pp. 4-6 "annotated the Golden Images set and distractor images. Approximately one week later, participants" and "We curated a corresponding Challenging Images set which mirrored the"
**Confidence**: 4 — experimental design and colour-appearance measurement; Fig. 3 values are not inspectable

**Study 1.** Condition is perfectly confounded with session, practice and memory: the Golden set always comes first and the Challenging set about a week later, with no counterbalancing and no test-retest on identical images to separate occasion noise from the effect of condition. The expert ±1 and distance metrics are reported pooled per country, not per condition, so expert lighting invariance is never actually shown.

**The Challenging set.** It is one author-curated image per subject. The selection criteria and illumination (exposure, correlated colour temperature, luminance) are not quantified.

**Study 2.** The evidence is a pair of untested ICC ranges, 0.90-0.96 for Golden and 0.82-0.95 for Challenging, described as "comparatively lower". It also includes an identical average distance of 0.78 for "well lit and poorly lit images", whose annotator pool and n are unstated (AR6 and AR7 are not computable). Invariance is inferred from the absence of a tested difference, with no test, no CI and no equivalence margin.

The released CSV carries a `lighting` field for all 1,515 images, so a full-dataset lighting analysis was possible but is not reported. The Abstract's "even under challenging environmental conditions" outruns this evidence.

Remedy:
- Estimate the lighting (and pose and mask) effects within the mixed model of W1 across all images.
- Report the effect in MST units with a CI.
- Test equivalence against a pre-stated margin, for example ±0.5 MST.
- Report expert metrics per condition.
- Document how the Challenging images were selected and quantify their illumination.
- Acknowledge the Study 1 order confound, or counterbalance it in any new collection.

### W8: The "with training" claim has no comparison condition, and training content and possible MST-E leakage are undisclosed
**Severity**: Major
**Evidence Anchor**: text: §7 Discussion and Suggestions for Practitioners, p. 9 "annotators are able to learn to be invariant to environmental factors such as lighting"
**Confidence**: 4 — training-effect design; the training materials are not described anywhere in the text

Three passages make a causal claim about training: Conclusion (b) ("with training, can provide annotations invariant to lighting conditions"), the Discussion's "able to learn", and the data card's "Trains annotators to be invariant to lighting conditions". There is no untrained group, no pre/post measurement, and no variation in training. The training content, duration, qualification threshold and in-production quality control (gold questions, removals) are never described.

MST-E is both the evaluation set and the recommended training material. If any MST-E images or reference labels were used to train these same annotators, their agreement with the reference is contaminated.

Remedy: describe the training protocol and state whether MST-E images or labels were part of it. Remove the causal "with training" and "learn to" wording, or support it with a controlled comparison (randomised trained versus untrained raters, or pre/post on held-out images). Present contribution (e) as an intended use, not a demonstrated effect.

### W9: The "10 annotators (2 × 5 regions)" recommendation rests on Spearman-Brown assumptions the paper's own results violate
**Severity**: Major
**Evidence Anchor**: text: §6 Replications, p. 8 "use the Spearman-Brown prediction formula to determine inter-rater agreement"
**Confidence**: 4 — k-rater reliability and replication planning; the Fig. 5 curves are missing

Spearman-Brown assumes parallel, exchangeable raters. The paper's own regional finding says raters from different regions are not exchangeable, and k is counted across regions, with stratified sampling of 2 per region. The formula projects the reliability of the mean of k ratings, yet the consensus used is the median. The reliability level that "suffices" is not stated, and Fig. 5 is unavailable, so the step from projected curves to "one rater per region" and "two annotators per region" cannot be checked. With 25 observed ratings per image, the projection could have been validated directly but was not. The advice also sits uneasily with the separate recommendation to use co-located annotators.

Remedy: subsample k from 1 to 25 with and without regional stratification. Measure how well the k-rater median agrees with the 25-rater median and with the reference (exact and ±1, with CIs), by image condition. State the target threshold, and reconcile the result with the co-location advice.

### W10: Validity conclusions are extended to in-the-wild data that have no reference labels
**Severity**: Major
**Evidence Anchor**: text: §6 Extension to In-the-Wild Annotations and §7 Limitations, pp. 8-10 "likely translate to real-world scenarios commonly faced by ML practitioners" and "we believe our results will translate to other domains"
**Confidence**: 4 — external-validity reasoning; the Fig. 6 distribution is not inspectable

The Open Images analysis can speak to reliability (ICC) and to regional difference. It has no reference labels, so it cannot show that consensus "matches intent" outside MST-E. The paper nonetheless concludes that recommendations from the controlled studies "likely translate" and that "our results will translate to other domains". MST-E subjects are 19 curated exemplars spanning the scale, photographed in a controlled shoot. Open Images is light-skewed (Fig. 6) and contains small, occluded and low-quality faces, which is exactly where validity is most likely to degrade.

Remedy: restrict the transfer claim to reliability and the regional-difference pattern. Alternatively, collect reference labels (an expert panel, or self-report where ethical and available) on a stratified random Open Images subset and test validity transfer directly.

### W11: The in-the-wild tests are unnamed, ignore clustering, and treat non-significance as equivalence
**Severity**: Major
**Evidence Anchor**: text: §6 Extension to In-the-Wild Annotations, p. 8 "This suggests that crowdsource annotators are similarly consistent in MST" and "between annotation distributions between regions"
**Confidence**: 3 — test identity has to be inferred because the statistics are unnamed

**The ICC-equality test** ("χ2 = 0.26, p = 0.99") has no name and no df, which is why AR9 is not computable. Its non-significance is read as "similarly consistent", which treats absence of evidence as equivalence. ICCs from item populations with different between-target variance are also not directly comparable as measures of consistency (W15).

**The regional-difference statistic** ("V 2 = 0.0766") is unnamed: it could be Cramér's V, or V² with V ≈ 0.28. It also lacks df and a named test, which is why AR10 is not computable. It is computed on about 2.2 million annotations (86,809 faces × up to 25) that are clustered within faces, images and raters. A naive contingency test is pseudo-replicated and will flag almost any difference. The effect size, possibly small, is not interpreted, yet practitioner advice depends on its magnitude.

Remedy: name each test and report df and effect sizes with CIs. Use cluster-aware inference, such as the mixed model of W1, or face-level bootstrap or permutation. For equivalence of reliability, give a CI on the ICC difference against a stated margin. Report the regional distributions in MST units.

### W12: The released artefacts do not support reproduction of the reported analyses
**Severity**: Major
**Evidence Anchor**: absence: Appendix C data card and Appendix L — expected pseudonymous annotator IDs and skip or difficulty flags in the released crowd CSV, the expert and Open Images annotations, and analysis code; checked §3, §6, Appendix C data fields, Appendix H, Appendix I, Appendix J, Appendix L
**Confidence**: 4 — data-release practice for annotation studies; based on the data-card field list

The released crowd CSV has four fields: subject, image, region and annotation. It carries no rater identifier, order or timestamp, skip or difficulty flag, or body-part response. That rules out any rater-level re-analysis: the two-way or G-study models of W3, rater random effects (W1, W2), exposure-order checks (W16) and the paper's own MANOVA. The expert annotations and the 86,809-face Open Images annotations behind the in-the-wild claims are not released, and no analysis code is mentioned. The crowd data card's "Number of unique annotations" is blank.

Remedy: release pseudonymous rater IDs with order, flags and body-part fields; the expert labels; the Open Images MST labels keyed to Open Images IDs; and scripts that reproduce every reported statistic.

### W13: Study 1's three significant Mann-Whitney tests are what chance predicts
**Severity**: Minor
**Evidence Anchor**: table: Appendix E Figure 7(a) and 7(b), p. 25, rows S13 Golden (p 0.026888), S14 Golden (p 0.018119), S14 Challenging (p 0.048632)
**Confidence**: 5 — direct arithmetic on the printed p-values

Study 1 ran 36 tests (18 subjects × 2 sets), each with 5 versus 5 raters, heavy ties and no multiplicity control. Three fall below .05. Under a global null, the expected count is 1.8, and P(≥3) ≈ 0.27 (binomial, treating the tests as independent; S14 appears twice, so they are not fully independent). None survives Holm or Benjamini-Hochberg correction: the smallest p, 0.018, would need to be below about 0.0014. The Section 5 text ("suggestive evidence that geographic location affects skin tone annotation") and the Figure 4 caption treat this as evidence of a regional effect. It is minor because Study 2 carries the regional claim.

Remedy: report the expert comparison as inconclusive, with multiplicity-adjusted p-values. Alternatively, use one pooled ordinal model with a country effect across all 36 images.

### W14: The US within-±1 rate of 83.4% cannot arise from the stated expert design
**Severity**: Minor
**Evidence Anchor**: text: §5 Distance from Intended Annotations, p. 7 "83.4% in the United States"
**Confidence**: 3 — GRIM reachability; the denominator of 36 is inferred because the paper does not state it
**Arithmetic Receipt**: AR2

Eighteen subjects were analysed in each of two sets. With these 36 reference-labelled images, a proportion must be k/36: 30/36 = 83.3% and 31/36 = 86.1%. So 83.4% is unreachable under any conventional rounding, and also under n = 18 (15/18 = 83.3%). The companion India value (88.9% = 32/36) is reachable. As noted in the opening remarks, the US average distance of 0.84 appears equally unreachable for integer distances. The denominator, rounding or computation behind the US figures therefore differs from the described design, for example because of an unreported skipped rating or a rounding slip. No conclusion changes.

Remedy: state k/n for every agreement figure, per condition, and correct the value.

### W15: Curated exemplar subjects spanning the scale inflate ICC and confound ICC comparisons across item populations
**Severity**: Minor
**Evidence Anchor**: text: §3 The MST Scale and the MST-E Dataset, p. 4 "subjects from an initial pool of hundreds of models, 19 of whom were eventually photographed"
**Confidence**: 4 — ICC as a variance ratio; the subject-selection criteria are not described

The 19 subjects were selected to span MST 1-10 with 1-3 per point, which maximises between-target variance. Because ICC is the ratio of between-target to total variance, the MST-E values are high partly by design. The criteria used to pick the 30 candidates, and who judged their MST at that stage, are not stated. Comparing MST-E ICCs with Open Images ICCs, and the χ² equality test, sets ratios with different denominators side by side. The high Open Images ICC (0.875-0.91) on a light-skewed sample partly mitigates the concern for the reliability claim, which is why this is Minor.

Remedy: report the within-image SD or standard error of measurement in MST units for each item population next to the ICC, and describe how subjects were selected.

### W16: Repeated exposure to the same 19 faces may inflate within-subject consistency
**Severity**: Minor
**Evidence Anchor**: text: §6 Exploration of Crowdsourced Annotations, p. 7 "larger set of similar images to prevent face recall among annotators"
**Confidence**: 3 — rater-memory effects in repeated-stimulus designs; exposure counts are not reported

MST-E holds 1,515 images of only 19 people, rated by vendor annotators on monthly contracts. Interleaving them with other images does not prevent recognition. A rater who recognises a subject can carry a remembered label across lighting conditions, which would inflate per-subject ICC and apparent lighting invariance. Neither the size of the larger pool nor the MST-E share is reported.

Remedy: report how many MST-E images each rater saw. Analyse label stability against exposure order, which needs the rater IDs and timestamps requested in W12, and check whether first-exposure ratings alone reproduce the invariance result.

### W17: Missingness and collected auxiliary responses are not reported
**Severity**: Minor
**Evidence Anchor**: absence: §5, §6 and Appendix C — expected counts of skipped and difficulty-flagged annotations by region, MST level and lighting, their handling in the ICC and median, and results for expert ease ratings and body-part responses; checked §4, §5, §6, §7, Appendix C, Appendix D, Appendix F
**Confidence**: 4 — missing-data reporting standards; the data card confirms that skips occurred

Annotators could skip images or flag them as difficult, and the data card confirms that some images have fewer than 25 ratings. The text does not give the number of skips, their distribution by MST level, region or lighting, or how the one-way ICC (unequal k) and the median (even counts) handled them. If skips concentrate on darker tones in poor lighting, the invariance and alignment results are biased in a fairness-relevant direction. The experts' 5-point ease ratings, and the body-part responses collected in both studies, are never reported.

Remedy: add a missingness table and state the handling rule. Report difficulty and body-part results against MST level and lighting.

### W18: The expert-versus-crowd conclusion rests on small, non-comparable designs
**Severity**: Minor
**Evidence Anchor**: text: §4 The Annotation Experiment and §7, pp. 5-9 "is a qualitative survey with a group of" and "suggesting that subject matter experts are not necessarily"
**Confidence**: 4 — reliability comparison design

Study 1 is called a "qualitative survey" but is analysed with ICCs and hypothesis tests. It has 5 experts per country and 18 targets per session, and uses a different ICC form from Study 2 (two-way versus one-way), so expert and crowd reliabilities are not on a common scale. Even so, the Discussion infers that "subject matter experts are not necessarily needed", which is a comparative claim.

Remedy: compute one agreement statistic for 5 experts per country and 5 crowd raters per region on the same 36 Golden and Challenging images, with CIs. Temper the inference, and describe Study 1 as a small quantitative exploratory study.

### W19: Stimulus presentation and viewing conditions are under-specified
**Severity**: Minor
**Evidence Anchor**: absence: §4 to §6 and Appendix D — expected the swatch rendering shown to annotators, display device and calibration, ambient viewing conditions, thumbnail resolution, and the full instruction text; checked §3, §5, §6, Appendix C, Appendix D captions
**Confidence**: 4 — colour-appearance moderators of human colour judgement; the Appendix D screenshots are absent from the extraction

Section 3 says MST swatches exist as flat patches or as shaded spheres, but not which the annotators saw. Display type, brightness and calibration, ambient lighting, and the exact instruction wording are not reported. These moderate colour judgements, and plausibly differ between vendor sites, which feeds the confound in W2.

Remedy: report them, and if possible record device type per rating.

### W20: The suggestion to filter for well-lit images may bias fairness datasets
**Severity**: Minor
**Evidence Anchor**: text: §6 Replications, p. 8 "would suggest ﬁltering for images with good lighting conditions"
**Confidence**: 3 — selection-bias reasoning; no data in the paper bear on it directly

Lighting quality in in-the-wild images is unlikely to be independent of skin tone, since exposure and camera pipelines have historically under-served darker skin. Filtering to well-lit images to save annotation budget could under-sample darker-skinned subjects and bias exactly the representation measures these labels are meant to support.

Remedy: check on Open Images, for example using the difficulty flags, whether such filtering shifts the MST distribution, and add the caveat to the recommendation.

### W21: The pixel baseline is a weak comparator and is reported only in figures
**Severity**: Minor
**Evidence Anchor**: text: Appendix G Pixel-Based Skin Tone, p. 26 "the closest MST point based on the L2 distance in RGB space"
**Confidence**: 4 — colour measurement (CIELAB, ΔE00, illuminant estimation)

The baseline averages RGB values and takes the L2 distance to the MST swatches in device RGB, with no white balance or illuminant estimation. That metric is perceptually non-uniform and blind to illumination. Its results appear only in Figures 9-11, with no agreement figure in the text. It supports "naive pixel matching fails" but not the broader recommendation against automated estimation, especially since §2 cites an illumination-aware alternative [25].

Remedy: report exact and ±1 agreement with the reference. Add a fairer baseline, such as ΔE00 in CIELAB after illuminant estimation, or an ITA mapping. Narrow the claim accordingly.

### W22: Data-card counts and usage terms are internally inconsistent
**Severity**: Minor
**Evidence Anchor**: table: Appendix C data card, Distribution of human attributes, p. 22, Images row summing to 1512 and Videos row summing to 34
**Confidence**: 5 — direct summation of the printed table

The per-MST counts sum to 1,512 images and 34 videos, against the stated 1,515 and 31. The data card lists "Data about image search queries" as the data subject, which looks like a template remnant, and leaves the crowd "Number of unique annotations" empty. The usage terms conflict as well. Section 3 says images and annotations are "licensed under CC BY" while restricting use to research, model evaluation and annotator training, and forbidding model training; a CC BY licence does not allow those restrictions. Appendix I then omits model evaluation altogether.

Remedy: reconcile the counts, fix the data-card fields, and state one consistent licence and use policy.

### W23: Ethics determination and annotator consent are not documented
**Severity**: Minor
**Evidence Anchor**: text: §4 The Annotation Experiment, p. 5 "conducted under the guidance of our institution’s ethics body"
**Confidence**: 3 — human-subjects reporting norms; venue-specific requirements were not applied (criteria binding unavailable)

The paper documents subject consent. For annotators it gives no approval or exemption determination, no description of the consent process for the crowd annotators, whose regional identity is the object of analysis, and nothing for the experts beyond GLG's terms and conditions.

Remedy: state the ethics determination, the annotator consent procedure, and how annotator data are handled.

## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "88.9% in India and 83.4% in the United States"
reported_inputs: 88.9% in India; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: the paper defines the metric as the percentage of median MST annotations within 1-point of the oracle, i.e. a mean of per-image 0/1 indicators on [0,1], so 88.9% is transcribed as the proportion 0.889 (percent sign dropped, decimal point shifted two places, no rounding); n=36 is the paper-stated count of oracle-annotated expert images (19 subjects minus the 1 excluded per footnote 4, in both the Golden and Challenging sets; Appendix E Figure 7(a) and 7(b) each list 18 subjects); the paper reports one value per market with no per-set split and does not state the denominator explicitly; rounding rule not stated
derivation: an unweighted mean of N=36 integer responses on [0,1] must be an integer sum divided by 36; candidate sums range over [0,36]
derived_value_or_range: sum 32 gives 32/36 = 0.8889, which rounds to 0.889
comparison_rule: the reported mean 0.889 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: consistent
rounding_interval: 0.8885 <= mean <= 0.8895 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: achieving sum 32; adjacent sums 32/36 = 0.8889; 33/36 = 0.9167

### AR2
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "88.9% in India and 83.4% in the United States"
reported_inputs: 83.4% in the United States; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: the paper defines the metric as the percentage of median MST annotations within 1-point of the oracle, i.e. a mean of per-image 0/1 indicators on [0,1], so 83.4% is transcribed as the proportion 0.834 (percent sign dropped, decimal point shifted two places, no rounding); n=36 is the paper-stated count of oracle-annotated expert images (19 subjects minus the 1 excluded per footnote 4, in both the Golden and Challenging sets; Appendix E Figure 7(a) and 7(b) each list 18 subjects); the paper reports one value per market with no per-set split and does not state the denominator explicitly; rounding rule not stated
derivation: an unweighted mean of N=36 integer responses on [0,1] must be an integer sum divided by 36; candidate sums range over [0,36]
derived_value_or_range: no integer sum in [0,36] rounds to 0.834 at 3 decimals
comparison_rule: the reported mean 0.834 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: mismatch
finding_ref: W14
rounding_interval: 0.8335 <= mean <= 0.8345 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: 30/36 = 0.8333; 31/36 = 0.8611

### AR3
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "0.78 in India and 0.84 in the United States"
reported_inputs: 0.78 in India; computed across all images; five experts in photography in India; Each expert reviewed each image; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: items are per-image differences between the median of the 5 India experts' MST ratings (each expert rated each image, so the median is an MST integer) and the integer oracle MST value; n=36 oracle-annotated images (18 subjects after the footnote-4 exclusion, Golden and Challenging sets) with the denominator not stated explicitly; the paper does not state whether the difference is absolute or signed, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the response-scale support is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: scale_support_unknown

### AR4
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "0.78 in India and 0.84 in the United States"
reported_inputs: 0.84 in the United States; computed across all images; five experts in photography in the United States; Each expert reviewed each image; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: items are per-image differences between the median of the 5 US experts' MST ratings (each expert rated each image, so the median is an MST integer) and the integer oracle MST value; n=36 oracle-annotated images (18 subjects after the footnote-4 exclusion, Golden and Challenging sets) with the denominator not stated explicitly; the paper does not state whether the difference is absolute or signed, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the response-scale support is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: scale_support_unknown

### AR5
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "the consensus annotation agreed within 1 point for all but one subject (94.7%)"
reported_inputs: all but one subject (94.7%); Using the global pool; consisting of images from 19 subjects; annotations for the entire MST-E dataset
assumptions: per-subject 0/1 indicators of the global-pool Per Subject consensus being within 1 point of the oracle, on [0,1], so 94.7% is transcribed as the proportion 0.947 (percent sign dropped, decimal point shifted two places, no rounding); n=19 is the paper-stated MST-E subject count, all annotated by the crowdsourced pool with no exclusion stated for this study; rounding rule not stated
derivation: an unweighted mean of N=19 integer responses on [0,1] must be an integer sum divided by 19; candidate sums range over [0,19]
derived_value_or_range: sum 18 gives 18/19 = 0.9474, which rounds to 0.947
comparison_rule: the reported mean 0.947 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: consistent
rounding_interval: 0.9465 <= mean <= 0.9475 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: achieving sum 18; adjacent sums 17/19 = 0.8947; 18/19 = 0.9474

### AR6
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "The distance was 0.78 for both well lit and poorly lit images."
reported_inputs: The distance was 0.78 for both well lit and poorly lit images; computed across all images; Each task was replicated 5 times in each region resulting in 25 annotations per image; Some images were too hard to annotate and were skipped by some annotators
assumptions: the paper does not state which annotator pool (global or a region) this value refers to, nor whether well lit images means the 19-image Golden set or all well-lit MST-E images, so n is not stated; skipped annotations can leave fewer than 25 (or 5) ratings per image, so integer median granularity is not licensed, and the sign convention of the distance is not stated, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the item-specific analytic N is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: analytic_n_ambiguous

### AR7
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "The distance was 0.78 for both well lit and poorly lit images."
reported_inputs: The distance was 0.78 for both well lit and poorly lit images; computed across all images; Each task was replicated 5 times in each region resulting in 25 annotations per image; Some images were too hard to annotate and were skipped by some annotators
assumptions: the paper does not state which annotator pool (global or a region) this value refers to, nor whether poorly lit images means the 19-image Challenging set or all poorly lit MST-E images, so n is not stated; skipped annotations can leave fewer than 25 (or 5) ratings per image, so integer median granularity is not licensed, and the sign convention of the distance is not stated, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the item-specific analytic N is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: analytic_n_ambiguous

### AR8
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Regional Differences in Annotation, p. 8 "(Pillai’s trace = 1.97,p< 0.05)"
reported_inputs: Pillai’s trace = 1.97,p< 0.05; multivariate analysis of variance (MANOVA) with annotator region as the independent variable and MST annotations for each subject as the dependent variable
assumptions: the only statistic printed is Pillai's trace, which is not a t, z, F, or chi-square value; the paper reports neither the approximating F statistic nor its df, so test family, statistic, and df are not stated; no tail convention stated
derivation: stopped before derivation: the test family is not identifiable from the report
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: test_family_ambiguous
tail_convention: unstated

### AR9
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations, p. 8 "χ2 = 0.26, p = 0.99 > 0.05"
reported_inputs: χ2 = 0.26, p = 0.99 > 0.05; the intraclass correlation from the Open Images dataset has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset
assumptions: chi-square family as printed; the specific chi-square test used to compare the intraclass correlations is not named and its df is not reported; the paper states no tail convention
derivation: stopped before derivation: the degrees of freedom are not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: missing_reported_value
tail_convention: unstated

### AR10
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations, p. 8 "(V 2 = 0.0766,p < 0.05)"
reported_inputs: V 2 = 0.0766,p < 0.05; We also find significant differences between annotation distributions between regions
assumptions: the paper does not name the statistic printed as V 2 or the test that produced the p-value, so the test family is not stated; df not reported; no tail convention stated
derivation: stopped before derivation: the test family is not identifiable from the report
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: test_family_ambiguous
tail_convention: unstated

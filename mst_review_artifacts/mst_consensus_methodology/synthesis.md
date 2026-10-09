# Editorial Decision Package

Contract `reviewer/reviewer_methodology_focus/v2` · mode `reviewer_methodology_focus` · panel_size 2 (`eic`, `methodology`) · no Devil's Advocate seat in this mode.

Seat labels used below: **EIC** = Journal-Fit Reviewer seat (`contract_role: eic`, scores D2). **METH** = methodology seat (`contract_role: methodology`, scores D1; schema seat R1). Transport refs `R<n>` / `S<n>` are roadmap references, not reviewer labels and not ranks.

## Binding Check

This is an explicitly unbound run. Both contract seats disclose `criteria_binding_unavailable` in their Phase 1 cards (p1_eic.md, p1_methodology.md), and both Phase 2 cards restate it. No venue criteria were applied, and this package makes no venue-alignment claim. The contract defines two seats, so the requirement that every card carry the disclosure applies to those two.

## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

Current runtime boundary: this package is not upgraded from a candidate or prose-named profile. `PROFILE_MEASURED` remains unavailable until a closed profile artifact and replay validator bind the exact target fields to the actual completed-panel `execution_topology_sha256`.

## Sprint Contract Arithmetic (Steps 1-3)

### Step 1: Role-scoped scoring matrix

| Dimension | Priority | Eligible roles | eic seat | methodology seat | Assessed eligible seats | Audit verdict |
|---|---|---|---|---|---|---|
| D1 methodology_rigor | mandatory | methodology | not_assessed (ineligible, excluded) | block, `block_class: repairable`, no fatal declared | 1 of 1 | block |
| D2 writing_and_structure | normal | eic | warn | not_assessed (ineligible, excluded) | 1 of 1 | warn |

Every dimension has at least one assessed eligible seat, so no dimension is unassessed.

### Step 2: Failure-condition evaluation

| Condition | Severity | Quantifier | Expression (all parse in the closed vocabulary) | Evaluation | Fired | Action |
|---|---|---|---|---|---|---|
| F1 | 95 | any | `D1 has a fatal block` | The METH seat's block is `repairable` and it declared no fatal block | false | reject |
| F2 | 90 | any | `D1 scores 'block'` | METH = block (1 of 1 assessed seat) | true | major_revision |
| F3 | 70 | any | `D1 scores 'warn'` | Exact-score atom (`<Dn> scores '<score>'`, not the "or worse" form). METH = block, which is not warn | false | major_revision |
| F4 | 40 | any | `D2 scores 'warn' or worse` | EIC = warn (1 of 1 assessed seat) | true | minor_revision |
| F0 | 10 | all | `every dimension scores 'pass'` | D1 = block, D2 = warn | false | accept |

### Step 3: Precedence and emission

Two conditions fired: F2 (severity 90) and F4 (severity 40). F2 has the highest severity, so its action applies. This mode has no DA seat, so there are no DA CRITICAL IDs. The mechanical outcome is not accept, so no DA-versus-accept marker applies. The cross-model blind decision check was not run because `ARS_CROSS_MODEL` is unset.

dimension_verdicts: [D1=block, D2=warn]
fired_conditions: [F2, F4]
da_critical_adjudications: []
editorial_decision=major_revision

---

## Part 1: Editorial Decision Letter

Dear Author(s),

Thank you for submitting your manuscript, "Consensus and Subjectivity of Skin Tone Annotation for ML Fairness". It was reviewed under a methodology-focused sprint contract by two role-separated seats. The Journal-Fit Reviewer (EIC seat) scored writing and structure (D2), and the Methodology Reviewer scored methodology rigor (D1). No venue criteria were bound, so nothing below asserts fit to a particular venue. This mode does not include a review-panel provenance record, and no claim is made that the two seats are independent.

### Decision: Major Revision

### Consensus Analysis

**Counting basis.** The denominator is the two contract seats (panel_size 2), not the four-seat basis used in full mode, so the labels CONSENSUS-3 and CONSENSUS-4 cannot occur. Each sub-claim gets one label:

- **corroborated (2/2):** both seats raised it and neither disputes it.
- **single-seat (1/2):** one seat raised it. The other seat's silence is not opposition.
- **SPLIT:** one seat disputes whether the problem exists, or disputes its severity or remedy.

The 46 weaknesses (EIC W1-W23, METH W1-W23) decompose into 59 sub-claims (SC-1 to SC-59): 21 corroborated, 8 SPLIT and 30 single-seat (13 EIC, 17 METH). Severity and confidence come from the cards unchanged. Confidence values did not affect any count or resolution.

#### Points of Agreement

Both seats credit the same design and reporting strengths:

- controlled same-session capture across poses, expressions and lighting (EIC S6, METH S3)
- the in-the-wild extension to 86,809 Open Images faces (EIC S4, METH S9)
- full tabulation of all per-image expert tests (EIC S5, METH S4)
- region-level compensation disclosure (EIC S2, METH S8)
- release of the image-level crowd annotations with dataset documentation (EIC S3, METH S5)

Corroborated weaknesses, both rated Major unless marked otherwise:

- **R1 (SC-1 to SC-3):** The claims of lighting invariance and invariance "with training" go beyond the evidence. There is no training contrast, the Challenging set has one image per subject, and Open Images has no reference labels. Sources: EIC W1; METH W7, W8, W10.
- **R2 (SC-4 to SC-6):** The 10-rater, five-region recommendation has no stated reliability threshold. Spearman-Brown pools k across regions. Every single-region pool already falls below a distance of 1, so diversity is confounded with rater count. The recommendation is also in tension with the co-location advice. Sources: EIC W2; METH W6, W9.
- **R4 (SC-8, SC-9):** The construct should be defined once: a subject-level reference label, with imaging conditions discounted. "Accuracy", "quality" and "aligns with an expert" should become agreement with the scale creator's reference labels. Sources: EIC W3, W4; METH W4.
- **R5 (SC-10, SC-11):** The reference annotator is a co-author and the scale's creator, and he approved labels an author had proposed first. Neither point is disclosed where the accuracy claims are made, and the limitations section does not mention it. Sources: EIC W4; METH W4.
- **R6 (SC-12, SC-13):** The training protocol, whether MST-E was used in training, and the number of raters per region are not described. Sources: EIC W5; METH W8, W2.
- **R8 (SC-16 to SC-18):** Load-bearing values appear only in figures. ICC forms and confidence intervals are missing, and tests are named without their statistic or degrees of freedom. Sources: EIC W7; METH W1, W3, W5, W6, W11.
- **S2 (SC-21, Minor):** The US within-±1 rate of 83.4% cannot be produced by the stated design. Sources: EIC W9; METH W14 (receipt AR2).
- **S4, S5 (SC-23, SC-24, Minor):** Data-card counts and fields contain errors. Sources: EIC W10, W11; METH W22.
- **S8 (SC-27, Minor):** Study 1 is labelled a "qualitative survey" but analysed quantitatively. Sources: EIC W13; METH W18.
- **S11 (SC-30, Minor):** The body-region, difficulty and skip data that were collected are never reported. Sources: EIC W15; METH W17.
- **S13 (SC-32, Minor):** The ethics determination and the annotators' consent are not documented. Sources: EIC W17; METH W23.

**Shared verification limit.** Both seats state that Figures 3, 5, 6 and 8 and the Appendix D screenshots were missing from the extraction. Several findings note that a figure may hold a value the text lacks (EIC W2, W7; METH W3, W5, W6, W9). Pointing to a figure answers what the figure shows. It does not meet the corroborated request that load-bearing values appear in the text or in tables.

**Single-seat findings.** Thirty sub-claims rest on one seat's anchored evidence. They are retained at that seat's severity and are not treated as consensus. Each one appears in the roadmap with its source W-id.

#### Points of Disagreement

**How SPLITs were resolved.** In a two-seat panel the Journal-Fit Reviewer is itself one of the parties, so no seat can arbitrate neutrally. Every SPLIT is therefore resolved by arbitration principle 2 (expertise first), keyed to the contract's own dimension descriptions:

- D1 (METH) covers study design, data handling, statistical reporting and reproducibility affordances.
- D2 (EIC) covers organisation, clarity of exposition and venue conventions.

Evidence first is applied wherever a card supplies the evidence. No SPLIT is left unresolved. The authors may contest any resolution in the response letter.

1. **SC-14, verbatim task instructions (severity).** EIC W5 raises this as Major, inside its training-protocol bundle. METH W19 raises it as Minor, as a moderator of viewing conditions. Both seats ask for the same remedy.
   - **Editor's Resolution:** Minor, should_fix (S1). Instruction text is a reproducibility affordance, which falls under D1. The training-protocol content stays must_fix under R6 (corroborated Major).
2. **SC-15, licence and terms of use (severity).** EIC W6 rates this Major. METH W22 rates it Minor.
   - **Editor's Resolution:** Major, must_fix (R7). The licence and access statement is a venue-convention item in the EIC's D2 scoring plan. The METH scoring plan does not cover licensing.
3. **SC-20, the MANOVA sentence reverses the model (severity).** EIC W8 rates this Minor. METH W1 places it in a Major bundle.
   - **Editor's Resolution:** Major, must_fix (R10). Stating which way a statistical model runs is statistical reporting, which falls under D1. The EIC card limits itself to how statistics are worded.
4. **SC-34, transferring conclusions to Open Images (severity).** EIC W19 rates this Minor. METH W10 rates it Major.
   - **Editor's Resolution:** Major, must_fix (R11). Whether the design supports transferring validity claims falls under D1. The two remedies are compatible: both restrict the claim to reliability and to the pattern of regional differences.
5. **SC-35, the "similar" wording (remedy).** EIC W19's proposed replacement reads "reliability and regional differences were similar on Open Images". METH W11 says a non-significant χ² read as "similarly consistent" treats absence of evidence as equivalence.
   - **Editor's Resolution:** METH's remedy governs (R11). This is statistical inference under D1, and the EIC card defers judgements on the appropriateness of tests to METH. Similarity may be stated only with a confidence interval on the ICC difference against a stated margin. Otherwise, report that no difference was detected.
6. **SC-37, a ±1 tolerance on a 10-point scale (severity and remedy scope).** EIC W20 asks for one sentence (Minor). METH W5 holds that the metric is too lenient and imported from 6-point FST work (Major).
   - **Editor's Resolution:** Major, must_fix (R12). Whether an agreement metric is adequate falls under D1. The EIC's sentence is covered by the METH remedy.
7. **SC-41, contents of the released artefacts (severity and remedy).** EIC W23 and W15 rate this Minor and would accept "release, or state why omitted". METH W12 rates it Major and asks for release.
   - **Editor's Resolution:** Major, must_fix (R13), and the METH release remedy governs. This is a reproducibility affordance under D1, and EIC W23 explicitly defers the reproducibility bar to METH. The release-scope table (SC-40) remains an EIC single-seat Minor item (S18).
8. **SC-52, "suggestive evidence" of a regional effect in the expert study (existence).** METH W13 (Minor) reports that 3 of 36 tests fall below .05 when 1.8 are expected by chance, and none survives Holm or Benjamini-Hochberg correction. EIC S5 credits the "suggestive evidence" wording as well hedged.
   - **Editor's Resolution:** METH W13 governs, Minor, should_fix (S19). On evidence, the card supplies the arithmetic. On expertise, inference falls under D1, and the EIC card states it does not judge whether analyses are appropriate. The EIC's credit for tabulating all 36 tests stands, and METH S4 agrees.

**Not a disagreement.** EIC W16 says the dermatologist pilot is unreported. METH S6 calls the pilot-informed choice of photographers good construct-validity practice. METH does not say whether the pilot is reported, and EIC's alternative remedy (present the choice as a design rationale) is consistent with METH S6. This stays an EIC single-seat item (S12).

### Decision Rationale

Under a sprint contract the decision is mechanical (`editorial_decision_standards.md` §0). The no-contract recommendation matrix does not apply and cannot adjust a fired action.

**How the decision follows from the scores:**

- The methodology seat is the only eligible scorer of the mandatory D1. It scored `block` with `block_class: repairable`, so F2 fired (severity 90).
- The EIC seat is the only eligible scorer of D2. It scored `warn`, so F4 fired (severity 40).
- F1 did not fire. The methodology seat declared no fatal block and gave four reasons for staying below its fatal trigger: there are repeated, overlapping annotations; items are fully crossed with regions; an ethics body is named; and no headline conclusion is contradicted by the paper's own numbers.
- F3 did not fire. Its atom requires an exact score of warn, and D1 is block.
- F0 did not fire.
- Precedence selects F2, so the decision is Major Revision.

**What the two cards agree on.** Both seats find that the headline claims are stated more strongly than the analyses support. This covers lighting invariance, "with training", alignment driven by diversity, the 10-rater five-region protocol, and transfer to in-the-wild data. Both seats also treat the single, non-independent reference annotator as a limit on every alignment claim. The methodology block rests on analyses that are under-specified or mis-specified (METH W1-W9). The EIC warn rests on overclaiming wording and on load-bearing details that are missing, scattered or inconsistent (EIC W1-W7).

**What can be fixed with existing data.** Both seats credit real design assets: 25 region-balanced ratings per image, controlled capture, complete expert test tables, and a large in-the-wild extension. The methodology seat judges that reanalysing the existing data, plus re-scoping where reanalysis cannot help, would answer most of its concerns. Where a card proposes new data, it also offers re-scoping as an alternative. This applies to independent reference labels, reference labels on Open Images, and any causal attribution to culture. The revised manuscript returns for re-review.

### Blocking Issues (0-3, immutable source order)

**Selection rule.** These are must_fix items that both seats corroborate, where each seat names the parent weakness as a driver of its own score (the METH D1 block rationale and the EIC D2 warn rationale). They are taken in source order and capped at three. R5, R6 and R8 meet the same rule and are left out only because of the cap. Every must_fix item (R1-R23) blocks acceptance equally, and this table does not rank them.

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---|---|---|---|---|
| R1 | The claims of lighting invariance and invariance "with training" go beyond the evidence | EIC W1; METH W7, W8, W10 | `text: Abstract and §8(b) "aligns with an expert in the MST scale, even under challenging environmental conditions"; "with training, can provide annotations invariant to lighting conditions"` | R1 |
| R2 | The practitioner protocol (10 raters, 5 regions) cannot be traced to a stated rule; diversity is confounded with rater count | EIC W2; METH W6, W9 | `text: §6-§7 "to be less than 1 for every region and image condition"; "(10 ratings per image), particularly for challenging images"; "it may be wise to use annotators from the same region"` | R2 |
| R4 | The construct is undefined, and "accuracy/aligns with an expert" overstates agreement with a single reference annotator | EIC W3, W4; METH W4 | `text: §1 and §8(c) "have any effect on annotation quality?"; "annotators are able to provide annotations that match the original intention behind the MST scale"; Appendix A "true skin tone"` | R4 |

---

## Part 2: Revision Roadmap

> The `Sub-Claim(s)` column gives each item's sub-claim IDs and consensus label. Items follow the fixed schema source order: EIC W1-W23, then METH W1-W23, then sub-claim. `R<n>` and `S<n>` number the must_fix and should_fix items within that order. Severity, obligation and cost never affect the order. Where an item has two sources, the first-listed source supplies the primary evidence anchor. Corroborating sources and their confidence values are given alongside.
>
> The machine `revision-roadmap/1.0` core is **not emitted**. It requires `base_draft_sha256`, `block_manifest_sha256` and `proposed_targets` block IDs from a bound block manifest, and none is bound in this run. Targets are given here as section locators only.
>
> Obligation rule: an item is must_fix when its transported severity (or its resolved severity, for a SPLIT) is Major, and should_fix when it is Minor. No item is classed `consider`. Counts: must_fix 23, should_fix 26, consider 0, total 49.

### Required Revisions (Must Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Restate the lighting results as measured: medians on one poorly lit image per subject stayed within one point of the subject-level label. Drop "with training" and "learn to", including the data card's "Trains annotators…", unless a trained-versus-untrained or pre/post comparison is added. Reframe contribution (e) as an intended use. Do not use Open Images as evidence of alignment under poor lighting. | SC-1, SC-2, SC-3 (2/2) | major / major | `text: Abstract and §8(b) "aligns with an expert in the MST scale, even under challenging environmental conditions"` | EIC 4; METH 4 (W7, W8, W10) | EIC W1; METH W7, W8, W10 | must_fix | sentence: Abstract; §7; §8(b); contribution (e); data card intended use | claim_scope_unsupported → claim: Abstract/§8(b) lighting invariance "with training" |
| R2 | State the reliability threshold that defines "suffices" and the k needed to reach it per condition. Report a size-matched comparison of single-region and pooled raters, or justify five regions on other grounds. Say when the co-location advice overrides the diversity advice. | SC-4, SC-5, SC-6 (2/2) | major / major | `text: §6-§7 "to be less than 1 for every region and image condition"` | EIC 4; METH 4 | EIC W2; METH W6, W9 | must_fix | re_analysis: §6 Replications; §7 practitioner bullets | claim_scope_unsupported → claim: §7 "(10 ratings per image)" recommendation |
| R3 | Reconcile the framing of skin tone as subjective perception with the framing of accuracy against an oracle. Add a §7 paragraph on what regional disagreement means for downstream fairness metrics: aggregate the labels, or keep them per annotator or per region. | SC-7 (1/2, EIC) | major | `text: §1 and §8(c) "have any effect on annotation quality?"` | EIC 4 | EIC W3 | must_fix | section: §1 framing; new §7 paragraph | interpretive_ambiguity_remains → claim: title/§1 subjectivity framing vs §2/§8(c) accuracy framing |
| R4 | Define the measured construct once, early: perceived tone, with imaging conditions discounted, judged against one subject-level reference label. Replace "quality", "accuracy", "aligns with an expert" and "true skin tone" with agreement with the scale creator's reference labels. | SC-8, SC-9 (2/2) | major / major | `text: §1 and §8(c) "annotators are able to provide annotations that match the original intention behind the MST scale"; Appendix A "true skin tone"` | EIC 4; METH 4 | EIC W3, W4; METH W4 | must_fix | sentence: §1/§3 definition; wording throughout incl. Abstract | claim_scope_unsupported → claim: Abstract "aligns with an expert"; §8(c) |
| R5 | In §3 and §4, disclose that the reference annotator is a co-author and the scale's creator, and that an author proposed the labels first. Add a competing-interests statement and a limitations paragraph on depending on a single reference. | SC-10, SC-11 (2/2) | major / major | `text: §3 "reviewed and annotated using the MST scale by the authors as well as the MST creator, Dr. Ellis Monk"; "annotated by an author and sent to Dr. Monk"` | EIC 4; METH 4 | EIC W4; METH W4 | must_fix | section: §3; §4; §7 Limitations | reporting_requirement_unmet → section: §3; §7 Limitations |
| R6 | Add a protocol subsection, or an appendix with an in-text pointer, on crowd training. Cover the content and source images (state whether MST-E images or labels were used), the duration and the qualification criteria. Report the number of distinct raters per region and the ratings per rater. | SC-12, SC-13 (2/2) | major / major | `absence: §6 and Appendices C-D — expected crowd training content (incl. MST-E use), verbatim instructions, unique raters per region; checked Abstract, §4, §6, §7, §8, Appendices C, D, K, L` | EIC 4; METH 4 (W8, W2) | EIC W5; METH W8, W2 | must_fix | section: §6 crowd protocol | method_reproducibility_unresolved → section: §6 crowd protocol |
| R7 | Adopt one licence that matches the use restrictions, since CC BY permits no field-of-use limits. State the same permitted and prohibited uses, including model evaluation, in §3, Appendix I and the data card. Say whether the annotation CSV carries a separate licence. | SC-15 (SPLIT → major) | SPLIT: major (EIC) vs minor (METH) → major | `text: §3 "The images and annotations are licensed under CC BY."; "The images cannot be used to train machine learning models."` | EIC 5; METH 5 | EIC W6; METH W22 | must_fix | section: §3; Appendix I; Appendix C data card | editorial_conformance_unmet → dataset: MST-E licence and terms of use |
| R8 | Add a results table (region × condition × dataset) giving the ICC form, point estimate, 95% CI and n. Put the photographer ICC values, the per-region distances to the reference and the confusion matrices in text or tables. Name every test with its statistic, df and p: the Open Images ICC comparison, "V²" and the MANOVA approximate F. | SC-16, SC-17, SC-18 (2/2) | major / major | `text: §5-§6 "we use a two-way random, single score ICC"; "χ2 = 0.26"; "V 2 = 0.0766"` | EIC 3; METH 4 (W1, W3, W5, W6), 3 (W11) | EIC W7; METH W1, W3, W5, W6, W11 | must_fix | section: §5-§6 new results table | reporting_requirement_unmet → table: new reliability/agreement table |
| R9 | Relabel the Appendix E "Figure 7" listings as tables, and label the "Value" column as U. | SC-19 (1/2, EIC) | major | `text: §5-§6 "we use a two-way random, single score ICC"` | EIC 3 | EIC W7 | must_fix | sentence: Appendix E labels | reader_traceability_reduced → table: Appendix E |
| R10 | Restate the MANOVA result in the direction of the stated model (region → per-subject annotations), with the statistic, F(df1, df2) and p. | SC-20 (SPLIT → major) | SPLIT: minor (EIC) vs major (METH) → major | `text: §6 "high predictor of the region of the annotators"` | EIC 5; METH 4 | EIC W8; METH W1 | must_fix | sentence: §6 Regional Differences in Annotation | interpretive_ambiguity_remains → claim: §6 MANOVA result sentence |
| R11 | Limit the Open Images transfer claims to reliability and the pattern of regional differences, and remove or qualify "other domains". State that reliability is similar only with a CI on the ICC difference against a stated margin; otherwise report "no detected difference". Alternatively, collect reference labels on a stratified Open Images subset. | SC-34, SC-35 (SPLIT → major) | SPLIT: minor (EIC) vs major (METH W10, W11) → major | `text: §7 "they perform similarly on the in-the-wild subset of Open Images"; "we believe our results will translate to other domains"` | EIC 4; METH 4 (W10), 3 (W11) | EIC W19; METH W10, W11 | must_fix | re_analysis: §6 Open Images ICC comparison; §6-§7 transfer wording | claim_scope_unsupported → claim: §6 "likely translate to real-world scenarios"; §7 "other domains" |
| R12 | Address what a ±1 tolerance means on a 10-point scale, given that it comes from 6-point FST work. Report exact agreement alongside ±1, and show ±1 against chance and constant-guess baselines. | SC-37 (SPLIT → major) | SPLIT: minor (EIC) vs major (METH) → major | `text: §2 "expert and crowdsource annotators tend toward fairly similar annotations on the FST"` | EIC 4; METH 4 | EIC W20; METH W5 | must_fix | re_analysis: §5-§6 agreement metrics | claim_scope_unsupported → claim: §5-§6 "within 1 point" alignment claims |
| R13 | Release pseudonymous rater IDs in the crowd CSV, with order or timestamp, skip and difficulty flags and body-region fields. Also release the expert labels, the Open Images MST labels keyed to Open Images IDs, and code that reproduces every reported statistic. | SC-41 (SPLIT → major) | SPLIT: minor (EIC W23, W15) vs major (METH W12) → major | `text: Appendix L "We release the annotations with this paper."` | EIC 4; METH 4 | EIC W23, W15; METH W12 | must_fix | other (data_release): crowd CSV fields; expert and Open Images labels; analysis code | method_reproducibility_unresolved → dataset: released annotations and code |
| R14 | Specify the regional-difference analysis: the unit of observation, N, the dependent variables, and the approximate F with df. Address multivariate normality, homogeneity of covariance, and nesting (images within subjects, the same images rated by every region). Drop the power claim or support it. Report region contrasts and effect sizes in MST units, preferably from a cumulative-link mixed model with subject/image and rater random effects. | SC-42 (1/2, METH) | major | `text: §6 Regional Differences in Annotation, p. 8 "with annotator region as the independent variable and MST annotations for each"; "we have enough statistical power to explicitly test the effect"` | METH 4 | METH W1 | must_fix | re_analysis: §6 Regional Differences in Annotation | evidence_gap_remains → claim: Conclusion (c) regional effect |
| R15 | Narrow the "cultural context" and "lived experience" attributions to "annotator pools recruited in different regions differ systematically". Include a rater random effect, and describe how sites, training and hardware differ by region. Note that each country in the expert study is a single recruitment pool. A causal attribution to culture needs new data. | SC-43 (1/2, METH) | major | `text: §7 Discussion and §7 Limitations, pp. 9-10 "suggesting that regional cultural contexts"; "or our annotators, beyond general geographic region"` | METH 4 | METH W2 | must_fix | re_analysis: §6 region model; §1 RQ(b), §7, §8(c) wording | claim_scope_unsupported → claim: §7 "regional cultural contexts" |
| R16 | Name the ICC form for each analysis using the McGraw-Wong taxonomy, e.g. ICC(A,1). Justify the one-way model, given that raters recur and are nested in region. Define the "Per Subject" ICC and its error terms. Add an ordinal Krippendorff's α or a G-theory decomposition with the standard error of measurement in MST units. | SC-44 (1/2, METH) | major | `text: §5 and §6 Inter-Rater Reliability, pp. 6-7 "so we use a two-way random, single score ICC where the subject and annotator are viewed"; "As the group of annotators was not consistent from image"` | METH 4 | METH W3 | must_fix | re_analysis: §5-§6 reliability analyses | evidence_gap_remains → claim: reliability claim (a) |
| R17 | Measure the reliability of the reference labels: the scale creator re-rates shuffled images blind, or at least two further MST-trained raters label blind. Choose any Golden-style evaluation image by a rule that does not depend on the reference label. If new labels cannot be collected, re-scope as in R4. | SC-45 (1/2, METH) | major | `text: §3 The MST Scale and the MST-E Dataset, p. 4 "ﬁrst annotated by an author and sent to Dr. Monk for ﬁnal golden annotations"; "an image for each subject that best represents their skin tone"` | METH 4 | METH W4 | must_fix | new_data: §3 reference labels (re-scoping fallback in R4) | evidence_gap_remains → claim: Abstract "aligns with an expert" |
| R18 | Define "average median distance": signed or absolute, and its n. Stop applying the proportion-based 1-point guardrail to a mean. Report exact agreement, weighted κ or ordinal α against the reference, and signed deviation by MST level and region, with subject-level bootstrap CIs. | SC-46 (1/2, METH) | major | `text: §5 Distance from Intended Annotations, p. 7 "was not above the 1-point guardrail established in previous research"` | METH 4 | METH W5 | must_fix | re_analysis: §5-§6 agreement metrics | evidence_gap_remains → claim: §5-§6 distance and ±1 figures |
| R19 | Test whether the conclusions change under other aggregators: mean, mode, trimmed estimators, or an annotator-aware ordinal label model. State how the half-integer medians that skips can produce are handled. | SC-47 (1/2, METH) | major | `text: §8 Conclusion and §6 Distance from Intended Annotations, pp. 8-10 "However, when collecting annotations from a diverse geographical pool, annotators are able"` | METH 4 | METH W6 | must_fix | re_analysis: §4/§6 consensus rule | evidence_gap_remains → claim: Conclusion (c) |
| R20 | Estimate the effects of lighting, pose and mask across all 1,515 images in a mixed model, in MST units with CIs. Test equivalence against a margin stated in advance. Report expert metrics per condition. Acknowledge that Study 1 always showed the Golden set before the Challenging set. Document how the Challenging images were selected, and quantify their illumination. | SC-48 (1/2, METH) | major | `text: §5 Exploration with Experts and §3, pp. 4-6 "annotated the Golden Images set and distractor images. Approximately one week later, participants"` | METH 4 | METH W7 | must_fix | re_analysis: §5-§6 lighting analysis | evidence_gap_remains → claim: lighting invariance (Abstract; §8(b)) |
| R21 | Describe quality control during production: gold questions and rater removals. | SC-49 (1/2, METH) | major | `text: §7 Discussion and Suggestions for Practitioners, p. 9 "annotators are able to learn to be invariant to environmental factors such as lighting"` | METH 4 | METH W8 | must_fix | section: §6 crowd protocol | method_reproducibility_unresolved → section: §6 crowd protocol |
| R22 | Check the replication recommendation against the data. Subsample k = 1-25, with and without stratifying by region, and report how well the k-rater median agrees with the 25-rater median and with the reference (exact and ±1, with CIs) by condition. Address the fact that the Spearman-Brown projection is for a mean while the consensus uses a median. | SC-50 (1/2, METH) | major | `text: §6 Replications, p. 8 "use the Spearman-Brown prediction formula to determine inter-rater agreement"` | METH 4 | METH W9 | must_fix | re_analysis: §6 Replications | evidence_gap_remains → claim: §7 "10 ratings per image" |
| R23 | Use inference that accounts for clustering in the Open Images regional comparison: a mixed model, or face-level bootstrap or permutation. Report and interpret effect sizes in MST units. Note that ICCs from item populations with different between-target variance cannot be compared directly. | SC-51 (1/2, METH) | major | `text: §6 Extension to In-the-Wild Annotations, p. 8 "This suggests that crowdsource annotators are similarly consistent in MST"; "between annotation distributions between regions"` | METH 3 | METH W11 | must_fix | re_analysis: §6 Extension to In-the-Wild Annotations | evidence_gap_remains → claim: §6 Open Images regional differences |

### Suggested Revisions (Should Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Give the verbatim task instructions in the text or an appendix. | SC-14 (SPLIT → minor) | SPLIT: major (EIC W5) vs minor (METH W19) → minor | `absence: §6 and Appendices C-D — expected verbatim task instructions; checked Abstract, §4, §6, §7, §8, Appendices C, D, K, L` | EIC 4; METH 4 | EIC W5; METH W19 | should_fix | section: Appendix D instruction text | method_reproducibility_unresolved → section: Appendix D |
| S2 | Correct the US within-±1 figure and give k/n for every agreement percentage. | SC-21 (2/2) | minor / minor | `text: §5 "88.9% in India and 83.4% in the United States"` | EIC 5; METH 3 (AR2) | EIC W9; METH W14 | should_fix | sentence: §5 Distance from Intended Annotations | reporting_requirement_unmet → claim: §5 agreement percentages |
| S3 | State that 18 of the 19 subjects shown were analysed in the expert study, and which MST level lost a subject. | SC-22 (1/2, EIC) | minor | `text: §5 "19 from the MST-E Golden Images or Challenging"` | EIC 5 | EIC W9 | should_fix | sentence: §5 | reader_traceability_reduced → section: §5 |
| S4 | Reconcile the data card's per-MST counts (1512 images, 34 videos) with the stated totals (1515, 31), checking against the released CSV. | SC-23 (2/2) | minor / minor | `table: Appendix C, Distribution of human attributes (Images row sums to 1512, Videos row to 34, versus Data Snapshot 1515 and 31)` | EIC 4; METH 5 | EIC W10; METH W22 | should_fix | other (data_card): Appendix C distribution table | editorial_conformance_unmet → dataset: Appendix C data card |
| S5 | Fix the "Data about image search queries" data-subject field, and fill in the crowd "Number of unique annotations". | SC-24 (2/2) | minor / minor | `text: Appendix C "Data about image search queries"` | EIC 5; METH 5 | EIC W11; METH W22 | should_fix | other (data_card): Appendix C fields | editorial_conformance_unmet → dataset: Appendix C data card |
| S6 | Correct "Model Evalutation", and add the author pre-annotation step to the provenance line. | SC-25 (1/2, EIC) | minor | `text: Appendix C "Model Evalutation"` | EIC 5 | EIC W11 | should_fix | other (data_card): Appendix C fields | editorial_conformance_unmet → dataset: Appendix C data card |
| S7 | Add one sentence in §3 stating that every image of a subject is scored against that subject's single reference label. | SC-26 (1/2, EIC) | minor | `text: §3 and Appendix C "We refer to these annotations as the oracle or intended annotations for the images"; "was annotated with a single MST-E value"` | EIC 4 | EIC W12 | should_fix | sentence: §3 | interpretive_ambiguity_remains → section: §3 |
| S8 | Describe Study 1 as a small quantitative exploratory study rather than a "qualitative survey". | SC-27 (2/2) | minor / minor | `text: §4 and §2 "is a qualitative survey with a group of skin tone"` | EIC 5; METH 4 | EIC W13; METH W18 | should_fix | sentence: §4 | interpretive_ambiguity_remains → section: §4 |
| S9 | Add a terminology paragraph to §4 and use its terms consistently: photographer panel, reference annotation, Golden/Challenging set, lighting condition. | SC-28 (1/2, EIC) | minor | `text: §4 and §2 "compared to an expert ground truth assessment"` | EIC 5 | EIC W13 | should_fix | section: §4 terminology paragraph | reader_traceability_reduced → manuscript |
| S10 | Replace "non-subjective attributes such as gender identity" with a distinction between self-identified or reportable attributes and perceived attributes. | SC-29 (1/2, EIC) | minor | `text: §2 "non-subjective attributes such as gender identity and age"` | EIC 4 | EIC W14 | should_fix | sentence: §2 | interpretive_ambiguity_remains → section: §2 |
| S11 | Summarise body-region use and difficulty ratings (crowd and photographers) by condition, and report skip counts. | SC-30 (2/2) | minor / minor | `text: §6 "report which part of the body they primarily used to make the selection"; "skip the task if no skin was visible"` | EIC 5; METH 4 | EIC W15; METH W17 | should_fix | re_analysis: §5-§6 descriptive summaries | evidence_gap_remains → section: §5-§6 |
| S12 | Report the dermatologist pilot's n and procedure, or present the choice of photographers as a design rationale rather than a finding. | SC-31 (1/2, EIC) | minor | `text: §5 "During an initial pilot we found that different types of experts may"` | EIC 5 | EIC W16 | should_fix | sentence: §5 | evidence_gap_remains → claim: §5 photographers-over-dermatologists rationale |
| S13 | State the type and outcome or identifier of the ethics review, the consent procedure for crowd and expert annotators, and how annotator data are handled. | SC-32 (2/2) | minor / minor | `text: §4 "conducted under the guidance of our institution"` | EIC 4; METH 3 | EIC W17; METH W23 | should_fix | sentence: §4 | reporting_requirement_unmet → section: §4 |
| S14 | Replace "open-access" with an accurate description of access for each artefact, and justify gating access behind an account. | SC-33 (1/2, EIC) | minor | `text: §3 and §7 "the open-access MST-E dataset"; "do not allow for anonymous access to the image dataset"` | EIC 4 | EIC W18 | should_fix | sentence: §3; §7; Appendix H; data card | editorial_conformance_unmet → dataset: MST-E access terms |
| S15 | Add a contributions paragraph at the end of §1 that names each new element relative to [33, 34, 48], maps the research questions to sections, and points to where each is delivered. | SC-36 (1/2, EIC) | minor | `text: §2 "expert and crowdsource annotators tend toward fairly similar annotations on the FST"` | EIC 4 | EIC W20 | should_fix | section: §1 contributions paragraph | reader_traceability_reduced → section: §1 |
| S16 | Move the statement of the MST design scope (the Americas) from Appendix A.2 into §2 or §3, and discuss it alongside the regional results in §7. | SC-38 (1/2, EIC) | minor | `text: Appendix A.2 "to optimally capture ethnoracial diversity in skin tone across the Americas"` | EIC 4 | EIC W21 | should_fix | section: §2/§3; §7 | interpretive_ambiguity_remains → section: §7 regional discussion |
| S17 | Correct the Casual Conversations attribution in Appendix A.3, and check that [50] supports the sentence on crowd-expert agreement. | SC-39 (1/2, EIC) | minor | `text: Appendix A.3 "Liu et al. [51] released the Casual Conversations Dataset"` | EIC 3 | EIC W22 | should_fix | sentence: §2; Appendix A.3 | reader_traceability_reduced → section: §2; Appendix A.3 |
| S18 | Add a release-scope table listing each artefact as released or withheld, with the reason, and document how image names join to lighting conditions. | SC-40 (1/2, EIC) | minor | `text: Appendix L "We release the annotations with this paper."` | EIC 4 | EIC W23 | should_fix | section: Appendix C/J release-scope table | reader_traceability_reduced → dataset: MST-E release |
| S19 | Report the expert regional comparison as inconclusive, with multiplicity-adjusted p-values or one pooled ordinal model with a country effect. Revise "suggestive evidence" and the Figure 4 caption. | SC-52 (SPLIT → METH) | minor (METH W13); EIC S5 disputes | `table: Appendix E Figure 7(a) and 7(b), p. 25, rows S13 Golden (p 0.026888), S14 Golden (p 0.018119), S14 Challenging (p 0.048632)` | METH 5 | METH W13 (disputed by EIC S5) | should_fix | re_analysis: §5; Appendix E | claim_scope_unsupported → claim: §5 "suggestive evidence that geographic location affects skin tone annotation" |
| S20 | Report the within-image SD or standard error of measurement in MST units next to each ICC, for each item population. Describe how the subjects were selected. | SC-53 (1/2, METH) | minor | `text: §3 The MST Scale and the MST-E Dataset, p. 4 "subjects from an initial pool of hundreds of models, 19 of whom were eventually photographed"` | METH 4 | METH W15 | should_fix | re_analysis: §5-§6 reliability reporting; §3 selection description | interpretive_ambiguity_remains → claim: MST-E vs Open Images ICC comparison |
| S21 | Report how many MST-E images each rater saw and the share of MST-E in the larger interleaved pool. Analyse label stability by exposure order, and check whether first-exposure ratings alone reproduce the invariance result. This needs the rater IDs from R13. | SC-54 (1/2, METH) | minor | `text: §6 Exploration of Crowdsourced Annotations, p. 7 "larger set of similar images to prevent face recall among annotators"` | METH 3 | METH W16 | should_fix | re_analysis: §6 | evidence_gap_remains → claim: per-subject ICC and lighting invariance |
| S22 | Add a missingness table showing skipped and difficulty-flagged annotations by region, MST level and lighting. State how skips enter the one-way ICC and the median. | SC-55 (1/2, METH) | minor | `absence: §5, §6 and Appendix C — expected counts of skipped and difficulty-flagged annotations by region, MST level and lighting, and their handling in the ICC and median; checked §4, §5, §6, §7, Appendix C, Appendix D, Appendix F` | METH 4 | METH W17 | should_fix | section: §5-§6 missingness table | reporting_requirement_unmet → table: missingness |
| S23 | Compute one agreement statistic for the 5 experts per country and 5 crowd raters per region on the same 36 images, with CIs, or temper "subject matter experts are not necessarily needed". | SC-56 (1/2, METH) | minor | `text: §4 and §7, pp. 5-9 "suggesting that subject matter experts are not necessarily"` | METH 4 | METH W18 | should_fix | re_analysis: §5-§7 expert-crowd comparison | claim_scope_unsupported → claim: §7 expert-necessity inference |
| S24 | Report the swatch rendering (flat or shaded), display type, brightness and calibration, ambient viewing conditions and thumbnail resolution. If possible, record the device type for each rating. | SC-57 (1/2, METH) | minor | `absence: §4 to §6 and Appendix D — expected the swatch rendering shown to annotators, display device and calibration, ambient viewing conditions, thumbnail resolution; checked §3, §5, §6, Appendix C, Appendix D captions` | METH 4 | METH W19 | should_fix | section: §4-§6 protocol | method_reproducibility_unresolved → section: §4-§6 protocol |
| S25 | Check on Open Images whether filtering to well-lit images shifts the MST distribution, and add a caveat to the recommendation. | SC-58 (1/2, METH) | minor | `text: §6 Replications, p. 8 "would suggest ﬁltering for images with good lighting conditions"` | METH 3 | METH W20 | should_fix | re_analysis: §6 Open Images | claim_scope_unsupported → claim: §6 filtering recommendation |
| S26 | Report exact and ±1 agreement between the pixel baseline and the reference. Add a baseline that accounts for illumination, such as ΔE00 in CIELAB after illuminant estimation, or an ITA mapping. Narrow the claim against automated estimation. | SC-59 (1/2, METH) | minor | `text: Appendix G Pixel-Based Skin Tone, p. 26 "the closest MST point based on the L2 distance in RGB space"` | METH 4 | METH W21 | should_fix | re_analysis: Appendix G | claim_scope_unsupported → claim: recommendation against automated estimation |

### Source-Traceability Checklist

> This list keeps source order and does not suggest an order of work. Author triage is collected later in a separate sidecar.

- [ ] R1 — obligation `must_fix`: Restate lighting results as measured; drop "with training" (EIC W1; METH W7, W8, W10)
- [ ] R2 — obligation `must_fix`: Reliability threshold, single-region vs pooled comparison, co-location vs diversity (EIC W2; METH W6, W9)
- [ ] R3 — obligation `must_fix`: Reconcile the subjective framing with the accuracy framing; add downstream-metrics paragraph (EIC W3)
- [ ] R4 — obligation `must_fix`: Define the construct; reword as agreement with the reference labels (EIC W3, W4; METH W4)
- [ ] R5 — obligation `must_fix`: Disclose the reference annotator's role; add single-reference limitation (EIC W4; METH W4)
- [ ] R6 — obligation `must_fix`: Crowd training protocol, MST-E use, raters per region (EIC W5; METH W8, W2)
- [ ] S1 — obligation `should_fix`: Verbatim task instructions (EIC W5; METH W19)
- [ ] R7 — obligation `must_fix`: One consistent licence and use policy (EIC W6; METH W22)
- [ ] R8 — obligation `must_fix`: Results table with ICC form, CI and n; name every test (EIC W7; METH W1, W3, W5, W6, W11)
- [ ] R9 — obligation `must_fix`: Relabel Appendix E as tables with a U column (EIC W7)
- [ ] R10 — obligation `must_fix`: Restate the MANOVA result in the model's direction (EIC W8; METH W1)
- [ ] S2 — obligation `should_fix`: Correct 83.4% and give k/n (EIC W9; METH W14)
- [ ] S3 — obligation `should_fix`: 18 of 19 subjects analysed; MST level affected (EIC W9)
- [ ] S4 — obligation `should_fix`: Reconcile data-card counts (EIC W10; METH W22)
- [ ] S5 — obligation `should_fix`: Data-subject field and unique-annotations count (EIC W11; METH W22)
- [ ] S6 — obligation `should_fix`: Misspelling and provenance line (EIC W11)
- [ ] S7 — obligation `should_fix`: Per-subject reference label stated in §3 (EIC W12)
- [ ] S8 — obligation `should_fix`: Drop "qualitative survey" (EIC W13; METH W18)
- [ ] S9 — obligation `should_fix`: Terminology paragraph (EIC W13)
- [ ] S10 — obligation `should_fix`: Rephrase "non-subjective" gender identity (EIC W14)
- [ ] S11 — obligation `should_fix`: Report body-region, difficulty and skip data (EIC W15; METH W17)
- [ ] S12 — obligation `should_fix`: Report the pilot or reframe it as rationale (EIC W16)
- [ ] S13 — obligation `should_fix`: Ethics determination and annotator consent (EIC W17; METH W23)
- [ ] S14 — obligation `should_fix`: Accurate access description (EIC W18)
- [ ] R11 — obligation `must_fix`: Limit the Open Images transfer claim; no "similar" without an equivalence test (EIC W19; METH W10, W11)
- [ ] S15 — obligation `should_fix`: Contributions paragraph against prior FST work (EIC W20)
- [ ] R12 — obligation `must_fix`: ±1 tolerance on a 10-point scale; exact agreement and baselines (EIC W20; METH W5)
- [ ] S16 — obligation `should_fix`: Move MST design scope into the main text (EIC W21)
- [ ] S17 — obligation `should_fix`: Citation attributions (EIC W22)
- [ ] S18 — obligation `should_fix`: Release-scope table (EIC W23)
- [ ] R13 — obligation `must_fix`: Release rater IDs, auxiliary fields, expert and Open Images labels, code (EIC W23, W15; METH W12)
- [ ] R14 — obligation `must_fix`: Specify or replace the MANOVA (ordinal mixed model) (METH W1)
- [ ] R15 — obligation `must_fix`: Narrow the cultural attribution; rater random effect; site details (METH W2)
- [ ] R16 — obligation `must_fix`: ICC forms, one-way model justification, ordinal α or G-theory (METH W3)
- [ ] R17 — obligation `must_fix`: Reference-label reliability; independent selection of Golden images (METH W4)
- [ ] R18 — obligation `must_fix`: Define distance metric; exact agreement, κ/α, signed deviation, CIs (METH W5)
- [ ] R19 — obligation `must_fix`: Sensitivity to the aggregation rule (METH W6)
- [ ] R20 — obligation `must_fix`: Full-dataset lighting model, equivalence test, order confound, Challenging-set selection (METH W7)
- [ ] R21 — obligation `must_fix`: Quality control during production (METH W8)
- [ ] R22 — obligation `must_fix`: Validate replication counts by subsampling (METH W9)
- [ ] R23 — obligation `must_fix`: Clustering-aware Open Images tests; effect sizes (METH W11)
- [ ] S19 — obligation `should_fix`: Report the expert regional comparison as inconclusive with multiplicity control (METH W13)
- [ ] S20 — obligation `should_fix`: SEM next to ICC; subject selection (METH W15)
- [ ] S21 — obligation `should_fix`: Effects of repeated exposure (METH W16)
- [ ] S22 — obligation `should_fix`: Missingness table and handling rule (METH W17)
- [ ] S23 — obligation `should_fix`: Common expert-crowd agreement statistic, or temper the inference (METH W18)
- [ ] S24 — obligation `should_fix`: Viewing conditions and swatch rendering (METH W19)
- [ ] S25 — obligation `should_fix`: Bias from filtering to well-lit images (METH W20)
- [ ] S26 — obligation `should_fix`: Pixel baseline metrics and a fairer baseline (METH W21)

### Response Letter Template

Please respond to every item above, R1-R23 and S1-S26, using the format in `templates/revision_response_template.md`. For each item, quote the transport ref and source W-id(s), state what was changed or why it was declined, and give the revised location. You may contest any SPLIT resolution in Part 1 with new evidence or reasoning.


## Attachment: Acronym Check (advisory, #849)

### Acronym check (advisory; no reply needed)
Coverage: body (partial)
Not in this input: English abstract, Chinese abstract.
Not checked:
- Body, line 304: IRR (the initials before its parentheses do not spell it)
- Body, line 601: ICASSP (the initials before its parentheses do not spell it)

| Scope | Line | Rule | Acronym | Uses |
|---|---|---|---|---|
| Body | 3 | Not defined | PAGE | 30 |
| Body | 5 | Not defined | ML | 6 |
| Body | 33 | Not defined | AI | 9 |
| Body | 67 | Not defined | MST1 | 4 |
| Body | 68 | Not defined | MST2 | 7 |
| Body | 69 | Not defined | MST3 | 6 |
| Body | 70 | Not defined | MST4 | 5 |
| Body | 71 | Not defined | MST5 | 7 |
| Body | 72 | Not defined | MST6 | 5 |
| Body | 73 | Not defined | MST7 | 4 |
| Body | 74 | Not defined | MST8 | 5 |
| Body | 75 | Not defined | MST9 | 5 |
| Body | 76 | Not defined | MST10 | 3 |
| Body | 77 | Defined again | MST | 119 |
| Body | 120 | Not defined | LGBTQ | 3 |
| Body | 173 | Defined after first use | ITA | 10 |
| Body | 174 | Not defined | RGB | 5 |
| Body | 203 | Defined again | MST | 119 |
| Body | 204 | Defined again | MST | 119 |
| Body | 213 | Not defined | TONL3 | 1 |
| Body | 232 | Not defined | TONL | 11 |
| Body | 240 | Not defined | CO | 6 |
| Body | 241 | Not defined | ALL | 2 |
| Body | 241 | Not defined | RIGHTS | 2 |
| Body | 243 | Not defined | BY | 1 |
| Body | 243 | Not defined | CC | 1 |
| Body | 302 | Defined after first use | ICC | 14 |
| Body | 322 | Defined again | ICC | 14 |
| Body | 400 | Not defined | MANOV | 1 |
| Body | 455 | Not defined | MSTE | 1 |
| Body | 456 | Not defined | OI | 1 |
| Body | 483 | Not defined | UI | 1 |
| Body | 561 | Not defined | TA | 1 |
| Body | 567 | Not defined | AAAI | 5 |
| Body | 567 | Not defined | ACM | 12 |
| Body | 580 | Not defined | PMLR | 1 |
| Body | 591 | Not defined | AJ | 1 |
| Body | 600 | Not defined | IEEE | 11 |
| Body | 614 | Not defined | FJBJoD | 1 |
| Body | 619 | Not defined | FAccT | 2 |
| Body | 619 | Not defined | NY | 1 |
| Body | 628 | Not defined | JAMA | 1 |
| Body | 633 | Not defined | ECCV | 2 |
| Body | 641 | Not defined | CUTIS | 1 |
| Body | 641 | Not defined | NEW | 1 |
| Body | 642 | Not defined | YORK | 1 |
| Body | 652 | Not defined | CVF | 4 |
| Body | 689 | Not defined | CF | 1 |
| Body | 698 | Not defined | KS | 1 |
| Body | 705 | Not defined | GA | 1 |
| Body | 705 | Not defined | JC | 1 |
| Body | 705 | Not defined | JL | 1 |
| Body | 744 | Not defined | JB | 1 |
| Body | 744 | Not defined | SC | 1 |
| Body | 763 | Not defined | KIPS | 1 |
| Body | 763 | Not defined | PERROT | 1 |
| Body | 763 | Not defined | TRAN | 1 |
| Body | 831 | Not defined | CIE | 1 |
| Body | 848 | Defined again | FST | 20 |
| Body | 892 | Defined again | MST | 119 |
| Body | 921 | Not defined | MSCOCO | 1 |
| Body | 984 | Not defined | LLC | 1 |
| Body | 996 | Not defined | GB | 1 |
| Body | 1029 | Not defined | PXL | 5 |

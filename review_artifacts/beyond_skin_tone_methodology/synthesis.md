# Editorial Decision Package

## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

Current runtime boundary: this package is not upgraded from a candidate or prose-named profile. `PROFILE_MEASURED` remains unavailable until a closed profile artifact and replay validator bind the exact target fields to the actual completed-panel `execution_topology_sha256`. Both seats are also `NOT_CALIBRATED`.

## Run Scope and Provenance (reviewer_methodology_focus)

- **Contract**: `reviewer/reviewer_methodology_focus/v2` (baseline v3.20.0), `panel_size: 2`.
- **Seats used** (both passed Phase 2 conformance): `eic` = Journal-Fit Reviewer, the only eligible seat for D2 `writing_and_structure`; `methodology` = Peer Reviewer 1, the only eligible seat for D1 `methodology_rigor`. Peer Reviewers 2 and 3 were not dispatched in this mode. The mode has no Devil's Advocate seat, so there are no DA CRITICAL IDs to adjudicate.
- **Execution provenance**: both seats ran on the same model family (Claude, Anthropic). They are role-separated (different personas, dimension ownership and scoring plans), but that does not make them independent. Their errors may be correlated, and agreement between them should not be read as two independent confirmations. The `reviewer_full` provenance block (#540/#740) does not apply in this mode and is omitted. No binary or numeric independence claim is made.
- **Criteria binding**: this is an unbound run (`criteria_binding_unavailable`). The methodology card carries the literal disclosure token. The eic card discloses the unbound state in prose ("no target-criteria authority was supplied for this run"; "I make no venue-alignment claim") but does not carry the literal `criteria_binding_unavailable` token. This disclosure-format gap is recorded here for the orchestrator. Binding conformance is not a score, failure condition, severity or editorial verdict. This package makes no venue-alignment or venue-fit claim.
- **Cross-model decision check (#518)**: not run, because `ARS_CROSS_MODEL` is unset. The decision is single-model.
- **Manuscript-directed text**: neither card nor the Phase 0 scan reported any manuscript text addressed to reviewers, editors or agents, and none was seen during anchor checks.

## Sprint Contract Synthesis (mechanical)

### Step 1: Role-scoped scoring matrix (Schema 6 `criterion_judgements`, `judgement_scale: sprint_contract`)

| Dimension | Priority | Eligible roles | eic | methodology | Assessed eligible seats | Audit verdict |
|---|---|---|---|---|---|---|
| D1 `methodology_rigor` | mandatory | [methodology] | not_assessed (ineligible; excluded) | block, `block_class: repairable` | 1 | block |
| D2 `writing_and_structure` | normal | [eic] | warn | not_assessed (ineligible; excluded) | 1 | warn |

Ineligible `not_assessed` values are excluded from both numerator and denominator. Both dimensions have one assessed eligible seat, so no `[DIMENSION-UNASSESSED]` abort applies. No seat declared a fatal block.

### Step 2: Failure-condition evaluation

| Condition | Severity | Expression (pattern) | Quantifier | Per-dimension result | Fired |
|---|---|---|---|---|---|
| F1 | 95 | `D1 has a fatal block` (pattern 6) | any | D1: block is `repairable`, not fatal → false | false |
| F2 | 90 | `D1 scores 'block'` (pattern 4, exact) | any | D1: methodology = block → true | true |
| F3 | 70 | `D1 scores 'warn'` (pattern 4, exact) | any | D1: methodology = block, not warn → false | false |
| F4 | 40 | `D2 scores 'warn' or worse` (pattern 8) | any | D2: eic = warn → true | true |
| F0 | 10 | `every dimension scores 'pass'` (pattern 9) | all | D1 false, D2 false → every → false | false |

Every expression parsed against the recognised vocabulary, so there was no `[EXPRESSION-UNRECOGNISED]` abort.

### Step 3: Precedence, decision and audit emission

The fired conditions are F2 (severity 90, action major_revision) and F4 (severity 40, action minor_revision). F2 has the highest severity and is selected. Nothing is averaged, voted or softened. The decision is not Accept, so no DA-consistency marker applies.

```text
dimension_verdicts: [D1=block, D2=warn]
fired_conditions: [F2, F4]
da_critical_adjudications: []
editorial_decision=major_revision
```

---

## Part 1: Editorial Decision Letter

Dear Author(s),

Thank you for your manuscript "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color". No target venue was bound for this review, so this letter makes no venue-fit claim. The manuscript was reviewed in methodology-focus mode by two role-separated review seats: a Journal-Fit Reviewer, who scored writing and structure (D2), and a Methodology Reviewer, who scored methodological rigor (D1). Both seats ran on the same model family. The provenance section above explains why their agreement should not be treated as independent confirmation.

### Decision: Major Revision

### Consensus Analysis

The panel has two scoring seats, and each is eligible for only one dimension. Most findings are therefore raised by one seat, and that reflects how the panel is scoped, not disagreement. The denominator here is the two active seats. A 2-of-2 agreement is reported as a corroborated finding. No CONSENSUS-4 or CONSENSUS-3 label is assigned, because the seats those labels need were not dispatched.

#### Points of Agreement

- **Corroborated (2/2, no conflict), SC-3**: Eq. (2) defines h* as arctan(b*/a*) and states a 0–360° range, yet Figure S1 prints negative h* values. Both seats ask for an atan2 definition with an explicit range (EIC W3; Methodology W18).
- **Corroborated (2/2, no conflict), SC-8**: the Figure S2 caption, the only depiction of the extraction pipeline, is truncated at "to get the f" (EIC W8; Methodology Minor Issues item 4).
- **Corroborated (2/2, no conflict), SC-10**: copy-editing slips "identify", "Alahuf", "a increase", and the dated term "transgendered" in the Section 4.3 ethics passage (EIC W9; Methodology Minor Issues items 1, 2, 3, 6).
- **Shared strengths**: comparing edits against the reconstruction rather than the original image (EIC S4; Methodology S3); the public code release (EIC S6; Methodology S8); scoping the construct to apparent rather than constitutive colour (Methodology S1; EIC's D2 rationale).
- **Single-reviewer findings**: the other 32 sub-claims (9 EIC, 23 Methodology) were raised by one seat, with the other seat silent. Each is judged against its own anchored evidence in the roadmap below.

#### Points of Disagreement

Neither seat marked any sub-claim as `disputed`, so there is no SPLIT to arbitrate. Four places where the cards touch the same manuscript feature from different dimensions are recorded below. They are not disputes, but the author should read them together.

- **Limitations content (EIC W2 ↔ Methodology W4, W19, W2/W17)**: EIC says the threshold provenance, illumination sensitivity and segmenter dependence are not *disclosed*. The Methodology seat says they are not *justified or quantified*.
  - **Editor's Resolution**: these are distinct atomic claims: disclosure under D2, rigor under D1. Phase 0 already divided the labour this way: a gap is scored once in D1, and D2 covers only how it is presented. Both remedies are compatible. The new Limitations section (REV-02) should report what the D1 analyses (REV-14, REV-16, REV-31) find.
- **Elo preference percentages (EIC W4 ↔ Methodology W9)**: EIC finds the conversion from Elo to a percentage undefined (minor, exposition). The Methodology seat finds that the percentage is the mean Elo gap passed through the logistic, not an observed win rate, and that the estimator and tests are unsound (major, inference).
  - **Editor's Resolution**: the two claims are different, so the severities are not in conflict. Both remedies apply: state the formula (REV-04) and report observed win rates with intervals from a defensible estimator (REV-21).
- **"Previously invisible" framing (EIC W10 ↔ Methodology W7, W8)**: EIC asks for the framing to be scaled back, and its card says the evidence question belongs to the methodology seat. The Methodology seat asks for the incremental-value and confounding analyses.
  - **Editor's Resolution**: no conflict. Revise the framing now (REV-12), and settle the final wording after REV-19 and REV-20.
- **Figure 4 (EIC S5 ↔ Methodology W12)**: EIC credits the Figure 4 caption as clear exposition of independent control. The Methodology seat shows that Figure 4 row 2's own values contradict that independence (+red raises L* from 44.43 to 52.05; both values were confirmed in the extraction).
  - **Editor's Resolution**: no conflict. The strength concerns how clearly the figure presents its claim, not whether the claim is true. The substantive claim is handled under REV-24, and the caption should be revised to match the dataset-level manipulation check.

#### Coverage Gaps (not reviewed; this does not mean "no issues")

Methodology-focus mode did not dispatch the domain seat (R2), the cross-disciplinary seat (R3) or a Devil's Advocate. As Phase 0 recorded, three areas therefore received no dedicated review:

- literature completeness and novelty positioning, which EIC W6 touches only as exposition;
- sociotechnical questions, namely "red/yellow" terminology, ethnicity-proxy risk and governance of the released measure, which EIC W2 touches only as a responsible-use disclosure;
- an adversarial stress-test of the core claim.

#### Anchor Verification Notes

- Checked against the text extraction: the quoted text anchors on both cards match the manuscript, with only line-break differences. The cited numeric values also match: Figure 4 row 2 L* 44.43/52.05, Figure S3 L* 66.63/59.41 with "up to 6 points", Figure S1 h* −25.38, Table 2 83.37, and Table 3 ArcFace D+Y 96.77. Phase 0 notes that the extraction-order mapping of Figure S3 labels to panels is inferred.
- Not verifiable from the extraction: the Figure 3 per-box group sizes (461/278, 206/533, 127/334/79/199). The Methodology card cites them in S2, uses them to illustrate W4 ("533 of 739") and W6 (72% "yellow" on CFD), and mentions them in its arithmetic note. Phase 0 recorded that Figure 3 graphics were lost in extraction. These values only illustrate W4 and W6 and change no score. The authors should confirm them.
- The Figure S2 caption truncation (SC-8) may be an extraction artifact, as Phase 0 noted. EIC reports seeing it on the rendered pages. The authors should confirm against the PDF. If it is an artifact, REV-08 closes without a change.
- The Methodology seat flags two of its own points as resting on its own knowledge, not on the manuscript: whether relighting method [81] alters chroma (W3, Question 3) and the scikit-learn LFW loader defaults (W17). They are carried with that caveat.
- The Methodology seat filed a `no_recomputable_statistics` arithmetic attestation. It is a declaration and is transported unchanged.

### Decision Rationale

The decision follows mechanically from contract `reviewer/reviewer_methodology_focus/v2`:

- The Methodology seat, the only eligible scorer for the mandatory D1, scored D1 `block` and declared it repairable.
- The Journal-Fit seat, the only eligible scorer for D2, scored D2 `warn`.
- F2 (D1 scores 'block', severity 90) and F4 (D2 scores 'warn' or worse, severity 40) fired, and precedence selects F2: Major Revision.
- F1 did not fire because the block is repairable, not fatal. F3 needs D1 to be exactly 'warn'. F0 needs every dimension to pass.

The two cards also support this outcome on substance. The Methodology seat's central finding is that the L*/h* instrument is never validated:

- there is no external validity anchor (REV-13, the only Critical finding, which the card says justifies the block on its own);
- there is no reliability evidence (REV-14);
- the one robustness probe cannot move hue (REV-15).

Every audit in the paper is a statement made with this instrument, so these gaps carry into each audit. The audits also have inference gaps of their own:

- the cropping results are not adjusted for ethnicity, gender and source (REV-20);
- Elo ratings that depend on one another are tested as if independent (REV-21);
- the verification cells have no uncertainty and no defined assignment rule (REV-22, REV-23);
- off-target effects of the counterfactual edits are unquantified (REV-24, REV-25).

**Why not Reject.** The Methodology seat checked its fatal trigger explicitly and found it unmet. Converting segmented skin pixels to CIELAB defines an apparent-colour quantity, and every gap can be closed by reanalysing data the authors hold, adding controls and documentation, or adding a bounded validation sub-study. F1 did not fire, and this letter does not override it.

**Why not Minor Revision.** F2 fired, and the remedies need re-analysis and new validation evidence. The revised manuscript will be reviewed again.

The two Major D2 findings (REV-01, REV-02) also stand in the way of acceptance on their own and belong in the same revision.

### Blocking Issues (0–3, immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---------------|----------------|--------------------|-----------------|------------------------|
| R1 | The score-extraction procedure (the paper's method) appears only in the supplement, and the Section 3 pointer sends readers to the robustness figure instead | EIC | `text: Sec. 3, p. 4 "provide the details of the methodology and a robustness" ... "analysis to different illuminations in Figure S3"` | REV-01 |
| R2 | There is no consolidated limitations or responsible-use discussion for the proposed L*/h* measure | EIC | `absence: Sec. 5 Conclusion and any Limitations or Broader Impact section — expected a consolidated discussion of the proposed L*/h* measure's validity limits and misuse risks; checked Secs. 1-5, the Sec. 2 social-impact paragraph, the Sec. 4.3 reconstruction caveat, and Supplementary A.1-A.4` | REV-02 |
| R3 | The L*/h* scores have no external validity anchor | Methodology (R1 seat) | `absence: §3 and §A.2 — expected a convergent-validity comparison of image-derived L* and h* against an external reference (multi-rater perceptual ratings, instrument readings, or colour-target captures) with agreement statistics; checked §2, §3, §4.1–§4.3, §A.1–§A.4, Figures 2–4 and S1–S6, Tables 1–4` | REV-13 |

How these three were chosen: for each fired condition, I took the finding or findings that the owning seat itself names as the driver of its non-pass score. For F2 that is Methodology W1, which the card says "on its own" justifies the D1 block. For F4 it is EIC W1 and W2, the two Major findings named in EIC's warn rationale. The other twelve Major D1 findings (REV-14 to REV-25) are also must-fix and together also block acceptance. The limit of three is a presentation bound, not a ranking.

---

## Part 2: Revision Roadmap

> The `Sub-Claim(s)` column carries the Step 1b `sub_claim_id`. In this package SC-n and REV-n share the same number. Transport refs `R<n>` and `S<n>` are roadmap references, not ranks. The R1 seat label (Methodology Reviewer) is a different thing from transport ref R1. Rows follow the immutable source order (seat EIC, then R1; then finding ordinal; then sub-claim part). Severity, obligation and cost never affect the order. No block manifest was bound to this run, so `proposed_targets[]` block ids are not emitted. They must come from a bound manifest when `scripts/revision_roadmap.py` builds the closed `revision-roadmap/1.0` artifact. Author triage is not included here; it belongs to the separate author sidecar.
>
> Obligation rule: a sub-claim whose transported severity is critical or major is `must_fix`, because these are the findings that keep D1 at block or D2 at warn. A minor finding is `should_fix`. A non-finding-channel editorial note raised by one seat is `consider`. Counts: must_fix 15, should_fix 19, consider 1 (35 items in total).

### Required Revisions (Must Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | REV-01: Move a condensed score-extraction pipeline (segmentation, sRGB→CIELAB, K-Means k=5, Sturges histogram mode, top-3-by-L* retention, size-weighted average) into Sec. 3 and reference Fig. S2. Point to A.2 for the method and Fig. S3 for robustness. Trim the Fitzpatrick/ITA background in Secs. 2–3 | SC-1 | major | `text: Sec. 3, p. 4 "provide the details of the methodology and a robustness" ... "analysis to different illuminations in Figure S3"` | 4 — core expertise: structure of CV fairness measurement papers | EIC (W1) | must_fix | section: Secs. 2–3, Supp. A.2 / Fig. S2 | reader_traceability_reduced → section: Sec. 3 |
| R2 | REV-02: Add a Limitations and Responsible Use subsection. Cover illumination and makeup sensitivity (Figs. S1, S3), the provenance and fixedness of the L*=60 / h*=55° thresholds, segmenter dependence, face-only scope, and explicit guidance against inferring an individual's race or ethnicity from L*/h*. Qualify the Sec. 5 deployment recommendation | SC-2 | major | `absence: Sec. 5 Conclusion and any Limitations or Broader Impact section — expected a consolidated discussion of the proposed L*/h* measure's validity limits and misuse risks; checked Secs. 1-5, the Sec. 2 social-impact paragraph, the Sec. 4.3 reconstruction caveat, and Supplementary A.1-A.4` | 4 — core expertise: responsible-AI review norms for demographic measurement tools | EIC (W2) | must_fix | section: new subsection before or within Sec. 5 | claim_scope_unsupported → section: Sec. 5 Conclusion |
| R3 | REV-13: Add a convergent-validity sub-study. Tone: agreement between L* and existing image-level annotations ([63], [31]) as rank and ordinal agreement with CIs. Hue: a multi-rater perceptual study with rater composition, inter-rater agreement and agreement with h*. Where possible, ΔE00 against colour-target captures | SC-13 | critical | `absence: §3 and §A.2 — expected a convergent-validity comparison of image-derived L* and h* against an external reference (multi-rater perceptual ratings, instrument readings, or colour-target captures) with agreement statistics; checked §2, §3, §4.1–§4.3, §A.1–§A.4, Figures 2–4 and S1–S6, Tables 1–4` | 4 — core expertise: measurement validity and image colorimetry | R1 Methodology (W1) | must_fix | new_data: validation sub-study (tone check can reuse annotated corpora [63], [31]; hue requires a multi-rater study) | evidence_gap_remains → claim: validity of the L*/h* score (§3, §A.2) |
| R4 | REV-14: Report reliability, stratified by tone: within-identity ICC(2,1) and Bland–Altman limits (CelebAMask-HQ and LFW identities); agreement between ground-truth and DeepLabV3 masks; spread over at least 10 K-means seeds, k = 3–7 and alternative retention rules; compression and resolution | SC-14 | major | `absence: §A.2 Robustness — expected an agreement statistic (ICC or Bland–Altman limits with CIs) for L* and h* across repeated images of an identity, segmenters, K-means seeds, cluster settings, and compression levels; checked §3, §4.1, §4.2.1, §A.2, Figures S2–S3` | 5 — core expertise: reliability of automated measurement instruments | R1 Methodology (W2) | must_fix | re_analysis: existing CelebAMask-HQ, LFW and CFD images and masks | evidence_gap_remains → claim: group assignment at L*=60 / h*=55° |
| R5 | REV-15: Run a sensitivity analysis over illuminant chromaticity and white balance (e.g. 2700–6500 K plus green/magenta tint, via von Kries/CAT on linearised sRGB) on many tone-stratified subjects. Report ΔL*, Δh* and ΔE00. State whether [81] alters chroma, and qualify the "orthogonal" conclusion | SC-15 | major | `text: §A.2 "h∗ remains stable and robust to face relighting, which confirms that it provides complementary and"` | 4 — core expertise: illumination and white balance; the detail of [81] is from the reviewer's own knowledge and should be confirmed by the authors | R1 Methodology (W3) | must_fix | re_analysis: synthetic illuminant shifts on existing images, §A.2 | claim_scope_unsupported → claim: §A.2 hue robustness / "orthogonal" |
| R6 | REV-16: Re-run the audits on continuous scores, across a cut-point grid (L* 50–70, h* 45–65°) and with dataset-specific quantile bins. Justify applying instrument-colorimetry thresholds [46] to image-derived values, or drop the implied equivalence | SC-16 | major | `text: §4.1 "Threshold values are taken from Ly et al. [46]."` | 5 — core expertise: colorimetry and categorisation of continuous measures | R1 Methodology (W4) | must_fix | re_analysis: Tables 1–4, Figure 3 | interpretive_ambiguity_remains → table: Tables 1–4 and Figure 3 group contrasts |
| R7 | REV-17: Report per-image chroma C* by group. Apply a chroma floor, or propagate per-image h* uncertainty with a pixel bootstrap. Check the dark-yellow and dark-red results in a chroma-restricted subset | SC-17 | major | `text: §3 "focus on the measurement of L∗ for skin tone and h∗ for skin hue"` | 3 — core expertise: colorimetry; how large the effect is on these data is unknown | R1 Methodology (W5) | must_fix | re_analysis: §3 measure definition and §4 group results | evidence_gap_remains → claim: dark-yellow / dark-red findings |
| R8 | REV-18: Describe Table 1 as apparent-colour composition. Estimate how much h* variance comes from capture conditions (repeated identities; regression on illuminant, exposure and saturation proxies from non-skin regions). Report identity-level proportions alongside image-level ones | SC-18 | major | `text: §1 "skewed towards light-red skin color and under-represent dark-yellow skin color"; §A.3 "This is explained by the fact that images in CFD have been captured in a controlled setting"` | 4 — core expertise: image colour pipelines; the CFD contrast is suggestive rather than conclusive because the population mixes differ | R1 Methodology (W6) | must_fix | re_analysis: Table 1, §1, §4.1, §A.3 | claim_scope_unsupported → claim: §1 / §4.1 dataset skew and balancing recommendation |
| R9 | REV-19: For each audit, fit nested models on continuous scores (~L*; ~ITA; ~L*+h*; ~L*×h*) with cluster-robust inference and report the gain in fit with CIs. Report L*–h* and ITA–h* correlations for each dataset | SC-19 | major | `absence: §4.2–§4.3 — expected a comparison of (L*, h*) against ITA-only and L*-only groupings or covariates in explaining performance differences (e.g., nested models with a likelihood-ratio test or ΔR²); checked §3, §4.1–§4.3, §A.3–§A.4, Tables 1–4, Figure 3` | 4 — core expertise: incremental validity testing | R1 Methodology (W7) | must_fix | re_analysis: §4.2–§4.3 audits | claim_scope_unsupported → claim: central "beyond skin tone" contribution |
| R10 | REV-20: Model the cropping outcomes directly (Bradley–Terry or logistic on L* and h* differences, with ethnicity, gender, source and position covariates). Report hue effects within ethnic groups where the h* range allows | SC-20 | major | `text: §4.2.1 "The product of both gender and ethnicity label sets results in 10"` | 4 — core expertise: confounding in fairness audits | R1 Methodology (W8) | must_fix | re_analysis: §4.2.1, Figure 3 | claim_scope_unsupported → figure: Figure 3 hue effect |
| R11 | REV-21: Replace single-pass Elo with Bradley–Terry MLE (with SEs or a game bootstrap) or with Elo averaged over many random orders. Use permutation tests over group labels. Report observed between-group win rates with CIs, effect sizes and exact test statistics | SC-21 | major | `text: §4.2.1 "we set M = 400 andK = 16 and we initialize scores at 1400."` | 4 — core expertise: rating systems and pairwise-comparison models | R1 Methodology (W9) | must_fix | re_analysis: §4.2.1, Figure 3 | evidence_gap_remains → figure: Figure 3 inferential claims |
| R12 | REV-22: Report per-cell pair and identity counts with Wilson or identity-clustered bootstrap CIs. Test differences with identity-clustered logistic regression and correct for multiplicity across the model × cell family. Consider the full 6,000-pair LFW View 2 | SC-22 | major | `table: Table 3 — ArcFace D+Y 96.77 exceeds L+R 96.12 while marginals report Light 95.52 vs Dark 94.39 and Red 95.36 vs Yellow 95.07; no per-cell n, interval, or test` | 5 — core expertise: uncertainty in disaggregated metrics | R1 Methodology (W10) | must_fix | re_analysis: Table 3, §4.2.2 | reporting_requirement_unmet → table: Table 3 |
| R13 | REV-23: State the rule that assigns a verification pair to a tone or hue cell. Analyse genuine and impostor pairs separately, and report same-group and cross-group impostor pairs separately (NIST protocol [29]) | SC-23 | major | `text: §4.2.2 "which contains 1,000 test pairs (500 positives and 500 negatives)"` | 4 — core expertise: biometric fairness evaluation | R1 Methodology (W11) | must_fix | re_analysis: §4.2.2, Table 3 | interpretive_ambiguity_remains → table: Table 3 cell definition |
| R14 | REV-24: Over all 4 × 30,000 edits, report distributions of skin ΔL*, Δh*, ΔC* and ΔE00, and of non-skin change (background ΔE, global contrast). Re-estimate Table 4 conditional on, or matched on, the off-target change. Consider projecting each latent direction orthogonal to the other | SC-24 | major | `figure: Figure 4 row 2 — reconstructed L*=44.43 vs +red L*=52.05 (h* 70.19 to 57.32)` | 5 — figure values read directly; core expertise: manipulation checks for counterfactual edits | R1 Methodology (W12) | must_fix | re_analysis: §4.3, Table 4, Figure 4, Fig. S4 | claim_scope_unsupported → claim: §4.3 independence of tone and hue edits |
| R15 | REV-25: Condition the tone and hue directions on the gender, smile, age and makeup boundaries. Report off-target drift with identity similarity, independent attribute classifiers and human verification of a stratified sample. Add a sham edit, and optionally a mask-restricted colour-space edit | SC-25 | major | `text: §4.3 "SVMs, one for skin tone and one for skin hue, are finally trained on the most confident positive and negative"` | 4 — core expertise: generative counterfactuals for causal fairness evaluation | R1 Methodology (W13) | must_fix | new_data: re-generated conditional edits plus human verification of a stratified sample, §4.3 | claim_scope_unsupported → claim: §1 / §4.3 causal findings (lighter → more "female", redder → more "smiling") |

#### Required Item Details

**R1: Score-extraction procedure absent from the main text (REV-01)**
- **Problem**: The main text never says how one L* and h* value is obtained per image. Sec. 3 defers to "Figure S3", which is the relighting figure. The procedure appears only in Supp. A.2 and Fig. S2, while Secs. 2–3 spend roughly two pages on prior scales.
- **Source**: EIC W1 (Major, confidence 4).
- **Requirement**: Add a short numbered pipeline (cluster count, retention rule, aggregation formula) to Sec. 3, reference or promote Fig. S2, fix the pointer, and trim the background.
- **Acceptance criteria**: A reader of the main text alone can re-implement the per-image score, and the Sec. 3 pointer names A.2 for the method and Fig. S3 for robustness.

**R2: No consolidated limitations or responsible-use discussion (REV-02)**
- **Problem**: The measure's own limitations are scattered or absent, and the Conclusion recommends use "from data collection to model deployment" without stating any.
- **Source**: EIC W2 (Major, confidence 4).
- **Requirement**: Add a Limitations and Responsible Use subsection with the elements listed in the roadmap row, and qualify the Sec. 5 recommendation. Report what the D1 analyses (REV-14, REV-16, REV-31) actually find.
- **Acceptance criteria**: One subsection states illumination/makeup sensitivity, threshold provenance, segmenter dependence and face-only scope, gives explicit guidance against individual race or ethnicity inference, and Sec. 5 carries these scope conditions.

**R3: No external validity anchor (REV-13)**
- **Problem**: L*/h* are never compared against any independent reference for what they claim to measure. Being automatic is not evidence of validity.
- **Source**: Methodology W1 (Critical, confidence 4); the card states this alone justifies the D1 block.
- **Requirement**: Add the validation sub-study described in the roadmap row (tone agreement with existing annotations; multi-rater hue study; ΔE00 against colour targets where possible).
- **Acceptance criteria**: The manuscript reports convergent-validity agreement statistics with CIs for L* and for h* against named external references, including rater composition and inter-rater agreement for the hue study.

**R4: No reliability evidence (REV-14)**
- **Problem**: There is no agreement statistic across repeated images, segmenters, K-means seeds, cluster settings or compression, yet every group uses a hard cut.
- **Source**: Methodology W2 (Major, confidence 5).
- **Requirement**: Report the tone-stratified reliability analyses listed in the roadmap row.
- **Acceptance criteria**: Within-identity ICC(2,1) and Bland–Altman limits, mask-source agreement, and seed, k and retention-rule spread are reported for L* and h*, stratified by tone.

**R5: Robustness probe cannot test hue's main threat (REV-15)**
- **Problem**: The single-subject relighting probe varies luminance, not illuminant chromaticity or white balance. Even so, the text concludes that hue is stable and "orthogonal".
- **Source**: Methodology W3 (Major, confidence 4; the detail of [81] is the reviewer's own knowledge and needs author confirmation).
- **Requirement**: Run the multi-subject illuminant-chromaticity and white-balance sensitivity analysis, state whether [81] alters chroma, and qualify the conclusion.
- **Acceptance criteria**: Distributions of ΔL*, Δh* and ΔE00 under chromatic illuminant and white-balance shifts are reported for tone-stratified subjects, and the hue-robustness claim matches them.

**R6: Cut-points unjustified and untested for sensitivity (REV-16)**
- **Problem**: Thresholds taken from instrument colorimetry [46] are applied to display-referred pixels without argument, and the model audits are never re-run at other cut-points.
- **Source**: Methodology W4 (Major, confidence 5).
- **Requirement**: Report the audits on continuous scores, across a cut-point grid, and with quantile bins. Justify or drop the equivalence with [46].
- **Acceptance criteria**: Each audit conclusion is shown to hold, or is qualified, under continuous analysis and the threshold grid, and the commensurability of the thresholds is argued or the equivalence claim is removed.

**R7: Chroma omitted; hue ill-conditioned at low chroma (REV-17)**
- **Problem**: C* is dropped, and h* error scales roughly as σ/C*. Hue precision may be worst where the dark-yellow claims are made.
- **Source**: Methodology W5 (Major, confidence 3).
- **Requirement**: Report C* by group, apply a chroma floor or propagate h* uncertainty, and re-check the dark-hue results.
- **Acceptance criteria**: Per-group C* is reported, and the dark-yellow and dark-red results are shown under a chroma floor or with propagated per-image h* uncertainty.

**R8: Apparent image colour read as population composition (REV-18)**
- **Problem**: Dataset skew claims treat apparent colour (casts, lighting, makeup, processing) as the make-up of the people photographed, and counts are per image, not per identity.
- **Source**: Methodology W6 (Major, confidence 4).
- **Requirement**: Relabel Table 1 as apparent-colour composition, estimate the share of h* variance due to capture conditions, and add identity-level proportions.
- **Acceptance criteria**: Table 1 and §1/§4.1 describe apparent-colour composition, a capture-condition variance estimate is reported, and identity-level proportions appear alongside image-level ones.

**R9: Added value of (L*, h*) never tested (REV-19)**
- **Problem**: No audit compares the two-dimensional grouping with ITA or L* alone, so the central "beyond skin tone" claim is asserted, not measured.
- **Source**: Methodology W7 (Major, confidence 4).
- **Requirement**: Fit the nested models with cluster-robust inference and report the L*–h* and ITA–h* correlations.
- **Acceptance criteria**: For each audit, the gain in fit of the L*+h* (and interaction) models over L*-only and ITA-only models is reported with CIs, and per-dataset correlations are given.

**R10: Cropping disparities confounded with ethnicity, gender and source (REV-20)**
- **Problem**: Skin colour groups are strongly structured by ethnicity, CFD-India is confounded with one group, and the comparisons are unadjusted t-tests.
- **Source**: Methodology W8 (Major, confidence 4).
- **Requirement**: Model game outcomes with L*/h* differences plus ethnicity, gender, source and position covariates, and report hue effects within ethnic groups where possible.
- **Acceptance criteria**: The hue effect is reported conditional on ethnicity, gender, source dataset and position, with uncertainty.

**R11: Elo estimator and t-tests on dependent ratings (REV-21)**
- **Problem**: Single-pass Elo is order-dependent, game counts differ by cell, and the ratings are tested as independent. Results are given only as thresholds, and the "60.73%" figure is a logistic of a mean gap, not an observed win rate.
- **Source**: Methodology W9 (Major, confidence 4).
- **Requirement**: Use Bradley–Terry MLE or order-averaged Elo, with permutation tests over group labels and observed win rates with CIs.
- **Acceptance criteria**: Group comparisons rest on an order-invariant estimator with permutation-based inference, and report observed between-group win rates with CIs, effect sizes and exact test statistics.

**R12: Verification disparities without counts, intervals or tests (REV-22)**
- **Problem**: Table 3 gives no per-cell n, intervals or tests. The marginal gaps are 0.29–1.13 points, the intersectional cells contradict the marginal narrative, and LFW pairs are clustered by identity.
- **Source**: Methodology W10 (Major, confidence 5).
- **Requirement**: Report per-cell counts with CIs, test with identity-clustered models and multiplicity correction, and consider LFW View 2.
- **Acceptance criteria**: Table 3 reports per-cell pair and identity counts, CIs and multiplicity-corrected tests, and the directional text claims are consistent with them.

**R13: Pair-to-cell assignment rule undefined (REV-23)**
- **Problem**: A negative pair contains two people who may fall in different groups, and the paper does not say how such a pair is assigned to a cell.
- **Source**: Methodology W11 (Major, confidence 4); Question 1 on that card.
- **Requirement**: State the rule and analyse genuine and impostor pairs separately, splitting impostors into same-group and cross-group.
- **Acceptance criteria**: The assignment rule is stated, and false non-match and false match results are reported separately, with same-group and cross-group impostor pairs distinguished.

**R14: Hue edit moves lightness; no dataset-level manipulation check (REV-24)**
- **Problem**: Figure 4 row 2's +red edit raises L* by 7.62. The edits change global contrast, and the independence claim rests on three faces.
- **Source**: Methodology W12 (Major, confidence 5).
- **Requirement**: Report dataset-level on-target and off-target change distributions and re-estimate Table 4 conditional on, or matched on, off-target change.
- **Acceptance criteria**: Distributions of ΔL*, Δh*, ΔC*, ΔE00 and non-skin change over all edits are reported, and the Table 4 effects are re-estimated conditional on off-target change.

**R15: Edit directions not conditioned on predicted attributes (REV-25)**
- **Problem**: Unconditioned InterFaceGAN directions can carry gender-presentation or expression cues. That would produce the reported "lighter → female" and "redder → smiling" shifts with no skin colour effect at all.
- **Source**: Methodology W13 (Major, confidence 4).
- **Requirement**: Use conditional manipulation, report off-target drift (identity similarity, independent classifiers, human verification of a sample), and add a sham edit.
- **Acceptance criteria**: The causal findings are re-reported using attribute-conditioned directions, with off-target drift measures, human verification of a stratified sample, and a sham-edit control.

### Suggested Revisions (Should Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | REV-03: Define h* with atan2 wrapped to [0, 360) and state the range. Explain the negative h* values in Fig. S1, or report them consistently with the stated range | SC-3 | minor (EIC); minor (R1) | EIC: `equation: Eq. (2) h* = arctan(b*/a*) with stated 0-360 degree range, versus negative h* values printed under Figure S1 panels (a), (c), (d), (e)`; R1: `equation: Eq. (2) h∗ = arctan(b∗/a∗) with stated 0–360° range, versus negative h* values in Figure S1 (a), (c)–(e)` | EIC 4 — core expertise: colour-space notation in vision papers; R1 5 — core expertise: CIELCh computation | EIC (W3) + R1 Methodology (W18, first part) | should_fix | sentence: Eq. (2), Sec. 3 | interpretive_ambiguity_remains → section: Sec. 3, Eq. (2) |
| S2 | REV-04: Correct the Elo update indices and wording ("if j looses"). State the formula that maps a mean group Elo gap to the reported 60.73% / 58.25% preferences | SC-4 | minor | `text: Sec. 4.2.1, p. 6 "an average Elo score indicating a 58.25% preference"` | 4 — core expertise: pairwise-comparison benchmarks in CV | EIC (W4) | should_fix | sentence: Sec. 4.2.1 | method_reproducibility_unresolved → section: Sec. 4.2.1 |
| S3 | REV-05: Use one term per construct and define it once (e.g. "ethnicity (self-reported)", "FFHQ (with FFHQ-Ageing masks)", "skin color score"). Rename the overloaded symbol a | SC-5 | minor | `text: Sec. 4.2.1, p. 5 "We extend it to multiple race labels"` | 4 — core expertise: fairness terminology conventions | EIC (W5) | should_fix | section: Secs. 3–4, Tables 1–2, Fig. 2 | interpretive_ambiguity_remains → manuscript: terminology throughout |
| S4 | REV-06: Replace the citation lists with a comparative paragraph that positions the extractor against prior automatic skin-colour estimators (what each measures, how it aggregates pixels, how the proposal differs) | SC-6 | minor | `text: Sec. 2, p. 3 "identification in facial recognition [8, 35, 58], image cap"` | 3 — adjacent expertise: skin-tone estimation literature in vision | EIC (W6) | should_fix | section: Sec. 2 | reader_traceability_reduced → section: Sec. 2 |
| S5 | REV-07: Compress the abstract's background to one sentence. Add one sentence on the extraction pipeline and one on the headline findings | SC-7 | minor | `text: Abstract, p. 1 "In their seminal paper Gender Shades, Buolamwini"` | 4 — core expertise: abstract conventions at CV venues | EIC (W7) | should_fix | section: Abstract | reader_traceability_reduced → section: Abstract |
| S6 | REV-08: Restore the full Fig. S2 caption, after confirming against the PDF (Phase 0 noted the truncation may be an extraction artifact) | SC-8 | minor (EIC); minor [SEVERITY-SOURCE: letter-fallback] (R1) | EIC: `figure: Figure S2 caption, final sentence ends mid-word at "to get the f"`; R1: Minor Issues item 4 (non-finding channel, no typed anchor) | EIC 5 — directly visible on the rendered pages; R1 not stated (non-finding channel) | EIC (W8, first part) + R1 Methodology (Minor Issues 4) | should_fix | sentence: Fig. S2 caption | editorial_conformance_unmet → figure: Fig. S2 |
| S7 | REV-09: Define L+R, L+Y, D+R, D+Y and the meaning of bold in the Table 3 caption | SC-9 | minor | `figure: Figure S2 caption, final sentence ends mid-word at "to get the f"` (parent W8 anchor; the Table 3 locator is in the finding text) | 5 — directly visible on the rendered pages | EIC (W8, second part) | should_fix | sentence: Table 3 caption | reader_traceability_reduced → table: Table 3 |
| S8 | REV-10: Correct "identify" → "identity", "Alahuf" → "Alaluf", "a increase" → "an increase", and "transgendered" → "transgender" | SC-10 | minor (EIC); minor [SEVERITY-SOURCE: letter-fallback] (R1) | EIC: `text: Sec. 4.2.2, p. 6 "as they better verify the identify of light-skinned"`; R1: Minor Issues items 1, 2, 3, 6 (non-finding channel, no typed anchor) | EIC 5 — directly verifiable in the text; R1 not stated (non-finding channel) | EIC (W9, first part) + R1 Methodology (Minor Issues 1, 2, 3, 6) | should_fix | sentence: §4.2.2, §4.3 | editorial_conformance_unmet → manuscript: §4.2.2, §4.3 |
| S9 | REV-11: Fix the remaining slips: "if j looses", "would then corresponds", "a representative scalar scores", "have a darker skins", and the stray full stop in the Fig. S3 caption | SC-11 | minor | `text: Sec. 4.2.2, p. 6 "as they better verify the identify of light-skinned"` (parent W9 anchor) | 5 — directly verifiable in the text | EIC (W9, second part) | should_fix | sentence: §4.2.1, §4.3, Supp. A.2, Fig. S3 caption | editorial_conformance_unmet → manuscript: listed locations |
| S10 | REV-12: Replace "previously invisible" with "not captured by a tone-only scale" and limit the deployment recommendations to the settings evaluated. Final wording should follow REV-19 and REV-20 | SC-12 | minor | `text: Sec. 5, p. 9 "and computer vision models, previously invisible."` | 3 — writing-calibration judgement; the substantive evidence question belongs to the methodology seat | EIC (W10) | should_fix | sentence: Sec. 1, Sec. 5 | claim_scope_unsupported → claim: Sec. 5 "previously invisible" |
| S11 | REV-26: Report dataset-level ΔL* and Δh* for each edit direction. Evaluate several edit strengths for a dose–response curve per unit of L* or per degree of h* | SC-26 | minor | `text: §4.3 "we modify all images in the CelebAMask-HQ datasets"` | 4 — core expertise: manipulation checks | R1 Methodology (W14) | should_fix | re_analysis: §4.3, Table 4 | interpretive_ambiguity_remains → table: Table 4 cross-direction comparisons |
| S12 | REV-27: Report paired differences with identity-clustered bootstrap CIs and McNemar tests. Control the FDR across 4 models × 4 edits × 3 subsets | SC-27 | minor | `text: §4.3 "results in a increase in accuracy for all models"` | 5 — core expertise: paired inference | R1 Methodology (W15) | should_fix | re_analysis: Table 4 | reporting_requirement_unmet → table: Table 4 |
| S13 | REV-28: Ablate the top-3-brightest-cluster rule (all clusters, middle clusters only, specular masking). Report changes in scores and group assignment by tone | SC-28 | minor | `text: §A.2 "We cluster the face skin into five groups and keep the top-3 groups with the highest L∗"` | 3 — core expertise: reflectance models; effect size unknown | R1 Methodology (W16) | should_fix | re_analysis: §A.2 pipeline | evidence_gap_remains → section: §A.2 |
| S14 | REV-29: Add a per-dataset methods table: mask source, image resolution, sRGB→CIELAB settings (linearisation, reference white, library), K-means feature space and seed, mode tie-breaking, LFW loader parameters | SC-29 | minor | `absence: §3, §4.2.2, §4.3 and §A.2 — expected the colour-conversion assumptions, K-means feature space and seed, LFW loading parameters, and the skin-segmentation source for LFW, generated and edited images; checked §3, §4.1–§4.3, §A.2, Figures S2–S4, footnote 1` | 4 — core expertise: reproducibility of image pipelines; the scikit-learn defaults are from the reviewer's own knowledge | R1 Methodology (W17) | should_fix | section: new methods table in §3 or §A.2 | method_reproducibility_unresolved → section: §3 / §A.2 |
| S15 | REV-30: Report how many images have h* outside 0–90°, and flag or exclude them instead of binning negative hues (including green casts) as "red" | SC-30 | minor | `equation: Eq. (2) h∗ = arctan(b∗/a∗) with stated 0–360° range, versus negative h* values in Figure S1 (a), (c)–(e)` | 5 — core expertise: CIELCh computation | R1 Methodology (W18, second part) | should_fix | re_analysis: §4 group assignments | interpretive_ambiguity_remains → claim: red/yellow group membership |
| S16 | REV-31: Correct the "up to 6 points" statement (Fig. S3 shows 66.63 → 59.41, which crosses L*=60). Report the share of images within a few units of each cut-point | SC-31 | minor | `figure: Figure S3 — original L*=66.63 vs sixth relit panel L*=59.41` | 5 — values read directly from the figure | R1 Methodology (W19) | should_fix | re_analysis: Fig. S3 caption, §A.2, cut-point proximity counts | claim_scope_unsupported → figure: Fig. S3 |
| S17 | REV-32: Score real FFHQ images with the same predicted-mask pipeline used for the generated images, and report CIs for the differences before describing P2 as amplifying | SC-32 | minor | `table: Table 2(b) — P2 red-hue total 83.37 vs FFHQ 81.87 in Table 1(b), reported as amplification without an interval` | 4 — core expertise: measurement invariance | R1 Methodology (W20) | should_fix | re_analysis: Tables 1(b), 2(b) | claim_scope_unsupported → claim: §4.1 "slightly amplifying" |
| S18 | REV-33: Counterbalance or randomise top/bottom placement, or include position as a covariate. Name the cropper release and commit | SC-33 | minor | `text: §4.2.1 "both facial images vertically with a white space in"` | 4 — core expertise: audit design | R1 Methodology (W21) | should_fix | re_analysis: §4.2.1 | method_reproducibility_unresolved → section: §4.2.1 |
| S19 | REV-34: Report API versions, model identifiers and query dates for AWS, Azure and Clarifai, and archive the raw responses | SC-34 | minor | `text: §4.3 "we use their latest available version for attribute prediction"` | 5 — core expertise: reproducibility of audits | R1 Methodology (W22) | should_fix | sentence: §4.3 | method_reproducibility_unresolved → table: Table 4 |
| S20 | REV-35: Use the same hue-label order in the Fig. 2 and Fig. S5 captions | SC-35 | minor [SEVERITY-SOURCE: letter-fallback] | R1: Minor Issues item 5 (non-finding channel, no typed anchor) | not stated (non-finding channel) | R1 Methodology (Minor Issues 5) | consider | sentence: Fig. S5 caption | editorial_conformance_unmet → figure: Fig. S5 |

### Step 1b Sub-Claim Inventory (compact)

Findings raised by only one seat are carried as one sub-claim per finding. Splitting them further would not change any disposition, because every part would still be a single-reviewer finding. Findings with a counterpart on the other card are split at the point where the cards overlap. Every (sub-claim, seat) pair not listed below is `not-mentioned`, which means silence, not opposition. Neither seat took a `disputed` position on any sub-claim. Transported severity, typed anchor and confidence are given on each roadmap row above.

| sub_claim_id | parent_weakness | reviewer_id | position | evidence_pointer | severity | confidence |
|---|---|---|---|---|---|---|
| SC-3 | EIC W3 hue-angle definition | EIC | raised | p2_eic.md W3 (equation anchor, row S1) | minor | 4 |
| SC-3 | Methodology W18 hue formula/range (first part) | R1 | corroborated | p2_methodology.md W18 (equation anchor, row S1) | minor | 5 |
| SC-8 | EIC W8 captions (Fig. S2 truncation) | EIC | raised | p2_eic.md W8 (figure anchor, row S6) | minor | 5 |
| SC-8 | Methodology Minor Issues item 4 | R1 | corroborated | p2_methodology.md Minor Issues 4 | minor [SEVERITY-SOURCE: letter-fallback] | not stated |
| SC-10 | EIC W9 copy-editing (shared slips) | EIC | raised | p2_eic.md W9 (text anchor, row S8) | minor | 5 |
| SC-10 | Methodology Minor Issues items 1, 2, 3, 6 | R1 | corroborated | p2_methodology.md Minor Issues 1, 2, 3, 6 | minor [SEVERITY-SOURCE: letter-fallback] | not stated |
| SC-1, 2, 4, 5, 6, 7, 9, 11, 12 | EIC W1, W2, W4, W5, W6, W7, W8 (second part), W9 (second part), W10 | EIC | raised (R1: not-mentioned) | p2_eic.md, per roadmap row | per row | per row |
| SC-13 to SC-29, SC-30 to SC-35 | Methodology W1–W17, W18 (second part), W19–W22, Minor Issues 5 | R1 | raised (EIC: not-mentioned) | p2_methodology.md, per roadmap row | per row | per row |

Confidence values are self-reported scope disclosures. None was totalled, averaged or used to weight a finding.

### Source-Traceability Checklist

> This list is in immutable source order and does not suggest a work order. Author triage is collected later as a separate, explicit sidecar.

- [ ] R1 (REV-01) — obligation `must_fix`: bring the score-extraction pipeline into Sec. 3, fix the pointer, rebalance the background
- [ ] R2 (REV-02) — obligation `must_fix`: add a Limitations and Responsible Use subsection and qualify Sec. 5
- [ ] S1 (REV-03) — obligation `should_fix`: atan2 definition and range for h*; explain negative values
- [ ] S2 (REV-04) — obligation `should_fix`: fix the Elo exposition and state the conversion to a percentage
- [ ] S3 (REV-05) — obligation `should_fix`: unify terminology and notation
- [ ] S4 (REV-06) — obligation `should_fix`: position the extractor against prior automatic estimators
- [ ] S5 (REV-07) — obligation `should_fix`: rebalance the abstract
- [ ] S6 (REV-08) — obligation `should_fix`: restore the Fig. S2 caption (confirm against the PDF)
- [ ] S7 (REV-09) — obligation `should_fix`: define the Table 3 abbreviations and bold
- [ ] S8 (REV-10) — obligation `should_fix`: shared copy-edits, including "transgender"
- [ ] S9 (REV-11) — obligation `should_fix`: remaining proofreading slips
- [ ] S10 (REV-12) — obligation `should_fix`: scale back the "previously invisible" framing
- [ ] R3 (REV-13) — obligation `must_fix`: convergent-validity sub-study
- [ ] R4 (REV-14) — obligation `must_fix`: reliability evidence stratified by tone
- [ ] R5 (REV-15) — obligation `must_fix`: illuminant-chromaticity and white-balance sensitivity
- [ ] R6 (REV-16) — obligation `must_fix`: cut-point justification and sensitivity
- [ ] R7 (REV-17) — obligation `must_fix`: chroma reporting and low-chroma hue handling
- [ ] R8 (REV-18) — obligation `must_fix`: apparent-colour framing and capture-condition share of variance
- [ ] R9 (REV-19) — obligation `must_fix`: incremental value of (L*, h*) over ITA and L* alone
- [ ] R10 (REV-20) — obligation `must_fix`: adjust the cropping audit for ethnicity, gender, source and position
- [ ] R11 (REV-21) — obligation `must_fix`: order-invariant estimator and valid inference for cropping
- [ ] R12 (REV-22) — obligation `must_fix`: counts, CIs and tests for Table 3
- [ ] R13 (REV-23) — obligation `must_fix`: pair-assignment rule; genuine and impostor analyses
- [ ] R14 (REV-24) — obligation `must_fix`: dataset-level manipulation and off-target checks
- [ ] R15 (REV-25) — obligation `must_fix`: attribute-conditioned edits, drift measures, sham control
- [ ] S11 (REV-26) — obligation `should_fix`: edit dose and dose–response
- [ ] S12 (REV-27) — obligation `should_fix`: paired tests and FDR control for Table 4
- [ ] S13 (REV-28) — obligation `should_fix`: ablate the retention rule
- [ ] S14 (REV-29) — obligation `should_fix`: per-dataset methods table
- [ ] S15 (REV-30) — obligation `should_fix`: handling of out-of-range hues
- [ ] S16 (REV-31) — obligation `should_fix`: correct the Fig. S3 lightness range; cut-point proximity
- [ ] S17 (REV-32) — obligation `should_fix`: same-pipeline comparison for generator amplification
- [ ] S18 (REV-33) — obligation `should_fix`: placement counterbalancing; cropper version
- [ ] S19 (REV-34) — obligation `should_fix`: version and date the commercial endpoints
- [ ] S20 (REV-35) — obligation `consider`: consistent hue-label order in captions

### Response Letter Template

Please respond to every item above using the format in `templates/revision_response_template.md`, marking every change in the revised manuscript. Please also answer the Methodology Reviewer's five Questions for Authors directly. Each corresponds to an item above: Q1 → REV-23, Q2 → REV-29, Q3 → REV-15, Q4 → REV-33, Q5 → REV-30. Journal-supplied deadline: NOT PROVIDED. No deadline or work estimate is inferred.

We encourage you to consider the reviewers' comments carefully and to submit a substantially revised manuscript. The revised manuscript will undergo another round of review.

---

## Part 3: Reviewer Report Summary (Appendix)

### Journal-Fit Review Report Summary (seat `eic`, D2 `writing_and_structure`)
- Recommendation: no overall recommendation (sprint-contract cards score only their own dimension). D2 = warn, trigger "limitations are present but thin; or the length balance is off". Confidence: per finding only (range 3–5).
- Counts: 6 strengths, 10 weaknesses (2 Major, 8 Minor), 0 questions.
- Key Point: The argument is easy to follow and each promised contribution maps to a subsection. However, the method is hidden in the supplement, there is no consolidated limitations or responsible-use section, and notation and terminology defects add up.

### Reviewer 1 (Methodology) Summary (seat `methodology`, D1 `methodology_rigor`)
- Recommendation: no overall recommendation (sprint-contract cards score only their own dimension). D1 = block (repairable), trigger "a required analysis or control is missing and can be supplied by reanalysing data the authors already hold, adding controls, or documenting". Confidence: per finding only (range 3–5).
- Counts: 10 strengths, 22 weaknesses (1 Critical, 12 Major, 9 Minor), 5 questions, 6 non-finding minor issues; `no_recomputable_statistics` arithmetic attestation.
- Key Point: The instrument has no validity or reliability evidence, and the audits lack uncertainty, confounder adjustment and manipulation checks. Every gap is repairable without redesigning the audits.

### Reviewer 2 (Domain) Summary
- Not dispatched in `reviewer_methodology_focus` mode. Coverage gap: literature and novelty positioning.

### Reviewer 3 (Perspective) Summary
- Not dispatched in `reviewer_methodology_focus` mode. Coverage gap: sociotechnical, terminology and ethnicity-proxy concerns.

### Devil's Advocate Summary
- Recommendation: N/A. This mode has no DA seat, so there are no DA CRITICAL IDs.
- Key Challenge: none issued. No adversarial review was run.

## Attachment: Acronym Check (advisory, #849)

### Acronym check (advisory; no reply needed)
Coverage: body (partial)
Not in this input: English abstract, Chinese abstract.
Not checked:
- Body, line 251: CIE (the initials before its parentheses do not spell it)
- Body, line 258: CIELAB (the initials before its parentheses do not spell it)
- Body, line 944: CSCW (the initials before its parentheses do not spell it)

| Scope | Line | Rule | Acronym | Uses |
|---|---|---|---|---|
| Body | 2 | Not defined | PAGE | 15 |
| Body | 5 | Not defined | AI | 5 |
| Body | 52 | Not defined | HQ | 18 |
| Body | 75 | Not defined | CV | 1 |
| Body | 253 | Not defined | RGB | 2 |
| Body | 341 | Not defined | FFHQ | 13 |
| Body | 367 | Not defined | BY | 1 |
| Body | 367 | Not defined | NC | 1 |
| Body | 367 | Not defined | SA | 1 |
| Body | 404 | Not defined | GAN | 2 |
| Body | 546 | Defined after first use | LFW | 4 |
| Body | 627 | Not defined | GAN3 | 1 |
| Body | 674 | Not defined | SVM | 1 |
| Body | 682 | Not defined | AWS | 5 |
| Body | 689 | Not defined | NS | 6 |
| Body | 815 | Not defined | FAccT | 4 |
| Body | 821 | Not defined | ECCV | 4 |
| Body | 824 | Not defined | NPJ | 1 |
| Body | 830 | Not defined | WACV | 2 |
| Body | 845 | Not defined | KJ | 1 |
| Body | 845 | Not defined | SJ | 2 |
| Body | 845 | Not defined | YB | 1 |
| Body | 851 | Not defined | CVPR | 10 |
| Body | 869 | Not defined | IEEE | 3 |
| Body | 875 | Not defined | JAMA | 3 |
| Body | 891 | Not defined | ACM | 6 |
| Body | 931 | Not defined | AAAI | 1 |
| Body | 946 | Not defined | JMLR | 2 |
| Body | 949 | Not defined | CF | 1 |
| Body | 951 | Not defined | MICCAI | 1 |
| Body | 960 | Not defined | ICCV | 4 |
| Body | 1008 | Not defined | AIES | 2 |
| Body | 1014 | Not defined | SY | 1 |
| Body | 1038 | Not defined | GM | 1 |
| Body | 1040 | Not defined | BMVC | 1 |
| Body | 1051 | Not defined | MN | 1 |
| Body | 1060 | Not defined | TPAMI | 1 |

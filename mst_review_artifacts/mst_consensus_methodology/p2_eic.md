contract_role: eic

## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: writing_and_structure
score: warn
trigger: "abstract or introduction claims worded more strongly than the results sections support"

## Review Body

Reviewer identity: Journal-Fit Reviewer, configured as a senior area chair for dataset-and-benchmark and responsible-AI submissions at top-tier ML venues. No venue criteria are bound (`criteria_binding_unavailable`), so venue observations below are field-general. I score D2 (writing_and_structure) only. D1 (methodology_rigor) belongs to the methodology seat. Where a writing defect touches statistics or design, I flag only how it is reported or claimed, not whether the analysis is appropriate.

Verification scope. The extraction has captions but no figures. I could not inspect the per-region ICC values (Fig. 3), the Spearman-Brown curves (Fig. 5), the MST-E vs Open Images distributions (Fig. 6), the confusion matrices against the oracle (Fig. 8), the task interfaces (Appendix D), the Golden/Challenging image sets (Appendix B) or the pixel-baseline outputs (Figs. 9-11). Every judgement below is made against the text and the tables that survived (Appendix C distribution table, Appendix E per-image tests, Appendix K compensation). Where a figure might hold a number the text lacks, I say so and lower my Confidence.

Journal fit, originality, significance. The topic is timely and squarely in scope for a datasets-and-benchmarks or responsible-AI venue. MST is being adopted for fairness audits, and nothing yet documents how people actually annotate it. The new contributions are an MST-specific annotation study with a five-region crowd at 25 replications per image, a curated subject set with matched lighting conditions (MST-E), and a check of reliability transfer on 86,809 Open Images faces. The headline that crowd medians land within about one point of an expert replicates a known result for FST [33, 34, 48], and the paper does not say plainly how its result differs. Significance for practitioners is high if the recommendations hold, which is why the gap between claims and evidence matters more here than in a purely descriptive paper.

Structural coherence and the D2 score. The manuscript is organised and readable: research questions in §1, protocol in §3-§6, discussion and limitations in §7, and a full set of dataset-track appendices (data card, maintenance plan, author statement, format, compensation). I score D2 `warn`, not `block`. A reader can find the protocol, the construct is recoverable once the data card is read, a limitations and ethics section exists, and every documentation gap can be fixed by line edits and added paragraphs without restructuring. What drives the warn is that the abstract and conclusion state lighting invariance, training effects, alignment with "the original intention behind the MST scale", and the value of geographic diversity more strongly than §5-§6 support (W1-W3). Load-bearing numbers, protocol details and licence terms are missing, scattered across sections or inconsistent (W4-W7). I considered the block clause on headline claims with no matching results section, for the "with training" wording. I did not apply it, because lighting invariance does have a results basis (the Golden vs Challenging comparison) and the training wording reads as an overreach on that basis rather than a claim with no results at all.

The paper's central tension, and the one practitioners will act on, is that it argues skin tone perception is subjective and culturally situated, then grades annotators by distance to one person's labels and recommends a fixed 10-rater, five-region protocol. The revision should reconcile these two framings explicitly.

### S1: Clear motivating question and practitioner-oriented research questions
The introduction poses one operational question and three sub-questions (who can annotate, whether location matters, what practices to adopt) that map onto §5, §6 and §7. The reader always knows which question a section answers.
**Evidence Anchor**: text: §1 "What is the best method to systematically annotate skin tone to build datasets and benchmarks for fairness research?"

### S2: Unusually complete annotator compensation disclosure
Appendix K reports per-region monthly pay and estimated hourly wage for all five crowd regions, the honoraria cap for the photographers, and total spend (about $780k crowd, about $5k experts). This exceeds what most annotation papers disclose and lets readers weigh labour conditions against the regional findings.
**Evidence Anchor**: table: Appendix K, per-region compensation table (Per Rater/Mo and Estimated Hourly Wage for India, Philippines, Hungary, Ghana, Brazil)

### S3: Dataset-track documentation package is present
The release ships with a data-card-style description (Appendix C), a maintenance plan with an error-reporting path (Appendix H), an author responsibility statement (Appendix I) and a file-format description (Appendix J). The per-image crowd annotations with region labels are public. The structure matches what a datasets-and-benchmarks reader expects, though see W6, W10, W11 and W23 on its contents.
**Evidence Anchor**: dataset: MST-E release documentation (Appendices C, H, I, J)

### S4: Scale and ecological extension of the crowd study
Beyond the controlled set, the authors annotate a large in-the-wild sample with the same tool and regions. This is the right move for a paper whose audience annotates uncontrolled imagery, and it is a distinctive contribution relative to prior FST studies.
**Evidence Anchor**: text: §6 "In the 41,471 images, 86,809 faces were present to annotate."

### S5: Transparent, appropriately hedged reporting of the exploratory expert comparison
Every per-image regional test for the photographers is tabulated, not only the significant ones, and the main text calls the result "suggestive evidence". This is good calibration of language to a 5-vs-5 design.
**Evidence Anchor**: table: Appendix E, Figure 7(a)-(b), per-image Mann-Whitney results for the 18 analysed subjects

### S6: Thoughtful stimulus design for the dataset's stated purpose
Same-session capture of each subject, deliberate variation in pose, expression and lighting, and subjects chosen across ethnicities and genders so that annotators can separate tone from race. These are well-motivated design choices for an annotator-training resource, and they are stated in the main text.
**Evidence Anchor**: text: §3 "collected within a short timespan of 4 hours"

### S7: Limitations section engages with practical cost and misuse
The limitations and ethics discussion names the cost of the recommended replication level, suggests a cheaper imputation-based alternative, acknowledges the small subject count, and discusses misuse risk and privacy choices.
**Evidence Anchor**: text: §7 "This is a very large jump from the status quo of 3 annotators per image"

### S8: Candour about review history and the identity of the criterion annotator
Appendix L records the earlier rejection and names the scale creator as the criterion annotator, where an earlier version left him anonymous. I checked its "we addressed X" statements against the main text. Most hold (limitations section added, metric definitions in §4, annotations released). The exceptions are noted in W4 and W23.
**Evidence Anchor**: text: Appendix L "we highlight that Dr. Monk is the Monk Skin Tone scale expert"

### W1: Lighting-invariance and training claims in the abstract and conclusion exceed the evidence
The abstract says annotators align with the expert "even under challenging environmental conditions". Conclusion (b) says annotators "with training, can provide annotations invariant to lighting conditions". §7 says annotators "are able to learn to be invariant". Contribution (e) presents MST-E as a way to train annotators to be invariant. The evidence is narrower than that:
- There is no training manipulation, no untrained comparison group and no pre/post measure, so nothing supports "with training" or "learn".
- The lighting result rests on the Challenging set, which is one image per subject (19 images for the crowd, 18 for the photographers).
- The Challenging ICC range drops to 0.82 (from 0.90 on Golden), which the text itself calls "comparatively lower".
- Open Images has no oracle, so it cannot speak to alignment under poor lighting.

This matters because practitioners will read "invariant to lighting" as licence to annotate badly lit imagery without adjustment, while §6 itself advises filtering poorly lit images or adding raters. Remedy: rephrase to what was measured, along the lines of "medians on one poorly lit image per subject stayed within one point of the subject-level label". Drop "with training" and "learn" unless a training-versus-no-training comparison is added. Reframe contribution (e) as an intended use, not a demonstrated effect.
**Severity**: Major
**Evidence Anchor**: text: Abstract and §8(b) "aligns with an expert in the MST scale, even under challenging environmental conditions"; "with training, can provide annotations invariant to lighting conditions"
**Confidence**: 4 — editorial comparison of abstract and conclusion wording against the §5-§6 text; I could not inspect Fig. 3 or Fig. 8

### W2: Practitioner recommendations are not traceable to a stated decision rule, and parts of them pull against each other
The abstract's closing advice and the §7 bullets recommend at least two raters in at least five regions (10 ratings per image), especially for challenging images. Three problems:
1. The Spearman-Brown paragraph says one rater per region "likely suffices" and two is "beneficial" but never states the target reliability that defines "suffices". Fig. 5, which carries the curves, is not reproduced in text.
2. Spearman-Brown pools k across regions, so it cannot by itself justify requiring five distinct regions instead of ten raters from one region.
3. §6 reports that the average median distance to the oracle is below 1 "for every region", yet §7 and conclusion (c) present geographic diversity as what yields alignment with the scale's intent. The contrast that would support that inference (single-region vs pooled distance) is not reported.

Separately, the third §7 bullet advises using annotators co-located with the data, which pulls against the diversity bullets, and the tension is not reconciled. Readers who act on this guidance need to know which result supports which bullet. Remedy:
- State the reliability threshold and report the k needed to reach it per condition in a table.
- Either report the single-region vs pooled comparison or justify the five-region recommendation on other grounds, namely the regional variation itself, framed as a choice of perspective rather than as accuracy.
- Add one sentence saying when the co-location advice overrides the diversity advice.
**Severity**: Major
**Evidence Anchor**: text: §6-§7 "to be less than 1 for every region and image condition"; "(10 ratings per image), particularly for challenging images"; "it may be wise to use annotators from the same region"
**Confidence**: 4 — the claim-evidence trace is in the text; the threshold might be visible in Fig. 5, which I could not inspect

### W3: The "subjective perception" framing and the "accuracy against an oracle" framing are not reconciled
The introduction and title frame skin tone annotation as subjective, shaped by lived experience and region. Yet RQ (b) asks whether location affects annotation "quality", §2 speaks of "annotator accuracy compared to an expert ground truth assessment", conclusion (c) claims a diverse pool yields annotations that "match the original intention behind the MST scale", and Appendix A refers to a subject's "true skin tone". Under the paper's own framing, regional variation is a legitimate difference in perspective. Under the evaluation framing, it is deviation from a single correct answer. The headline results are interpretable, but readers cannot tell which reading the authors endorse, and the two readings lead to different practice. One reading says to aggregate to a median and treat dispersion as noise. The other says to keep per-annotator or per-region labels, as the paper's own §2 discussion of annotator-level modelling suggests. Remedy: define the construct once, early ("perceived skin tone of the depicted person, corrected for imaging conditions, as judged against the scale creator's reference labels"). Rename "quality"/"accuracy" to "agreement with the reference annotator" throughout. Add a paragraph in §7 on what regional disagreement means for downstream fairness metrics.
**Severity**: Major
**Evidence Anchor**: text: §1 and §8(c) "have any effect on annotation quality?"; "annotators are able to provide annotations that match the original intention behind the MST scale"; Appendix A "true skin tone"
**Confidence**: 4 — conceptual reading of the paper's own framing statements; no statistical judgement involved

### W4: The criterion annotator's relationship to the authors is not disclosed where the accuracy claims are made, and single-criterion dependence is absent from the limitations
§3 says the images were annotated "by the authors as well as the MST creator, Dr. Ellis Monk", which reads as if Dr. Monk were external, though he is a co-author. The same paragraph says the labels were "annotated by an author and sent to Dr. Monk" for approval, so the criterion labels originate inside the author team and are confirmed by the scale's creator, whose scale the authors' institution hosts. §4-§8 then use these labels as the yardstick for "alignment", "intended" and "accuracy". There is no competing-interests statement. The relationship becomes explicit only in Appendix L. The limitations paragraph covers subject count, expert sample size and the 1-point threshold, but not that every accuracy claim depends on one non-independent reference annotator. Remedy:
- Add a disclosure sentence in §3 and §4 stating that the reference annotator is a co-author and the scale's creator, and that an author pre-annotated the images.
- Add a limitations paragraph on single-reference dependence.
- Qualify "aligns with an expert" in the abstract as agreement with the scale creator's reference labels.

The methodology seat should judge whether an independent reference panel is needed.
**Severity**: Major
**Evidence Anchor**: text: §3 "reviewed and annotated using the MST scale by the authors as well as the MST creator, Dr. Ellis Monk"; "annotated by an author and sent to Dr. Monk"
**Confidence**: 4 — author list, §3, §7 and Appendix L read together; governance judgement within my remit

### W5: The crowd training protocol, task instructions and rater-pool size cannot be located
"Trained" crowd annotators are central to the abstract, §7 and conclusions (a), (b) and (e). Yet the manuscript never describes the training: what materials were used, whether MST-E images (the evaluation set) were among them, how long it took, and whether there was a qualification threshold. The only instruction artefacts are task screenshots in Appendix D, which did not survive extraction. The text gives no verbatim instructions. The number of unique raters per region, out of which five were "randomly selected" per image, is never given, and the data card's "Number of unique annotations" for the crowd is blank. Without these, the protocol cannot be reproduced and the "with training" claims (W1) cannot be interpreted. If training used MST-E, the evaluation on MST-E would also need caveating. The authors cite CrowdWorkSheets [20] but do not provide the equivalent documentation themselves. Remedy: add a protocol subsection, or an appendix with an in-text pointer, covering training content and source images, duration, qualification criteria, verbatim instructions, rater-pool size per region and skip counts.
**Severity**: Major
**Evidence Anchor**: absence: §6 Exploration of Crowdsourced Annotations and Appendices C-D — expected a description of crowd annotator training content (including whether MST-E images were used), verbatim task instructions, and the number of unique raters per region; checked Abstract, §4, §6, §7, §8, Appendices C, D, K and L
**Confidence**: 4 — full text searched; the Appendix D screenshots might show the instruction text, but the training procedure is not described anywhere

### W6: The licence and terms of use are internally inconsistent
§3 states that the images and annotations are "licensed under CC BY". The same passage, the image credit ("ALL RIGHTS RESERVED") and Appendix I restrict use to research and annotator training and forbid model training. CC BY carries no field-of-use restrictions, so the two statements cannot both govern the release. The allowed uses also differ by location:
- §3 permits "model evaluations".
- Appendix I omits model evaluation.
- The data card lists "Model Evaluation" as an intended use.
- §7 promotes MST-E for model evaluation.

For a dataset contribution, users must be able to tell lawful use from the paper, and the inconsistency also weakens the misuse mitigation claimed in §7. Remedy: settle on one licence that matches the TONL permission. That likely means a custom research licence or CC BY-NC-ND with an explicit no-training clause, not CC BY. Then state the identical permitted and prohibited uses in §3, Appendix I and the data card, and state separately whether the annotation CSV carries a different licence from the images.
**Severity**: Major
**Evidence Anchor**: text: §3 "The images and annotations are licensed under CC BY."; "The images cannot be used to train machine learning models."
**Confidence**: 5 — direct textual contradiction; CC BY terms are standard knowledge for dataset-track review

### W7: Load-bearing statistics are carried by figures or reported without identifying the statistic
For the photographers, the text never reports the ICC values themselves, only that Fig. 3(a) shows them to be significant. For the crowd, ranges are given, but per-region values, per-region oracle distances and the confusion matrices exist only in Figs. 3 and 8. No ICC is reported with a confidence interval. The ICC form (consistency vs absolute agreement) is not stated for either design. The test behind the Open Images ICC comparison and the statistic behind the regional-distribution comparison are unnamed. The MANOVA is reported without degrees of freedom or an approximate F. The Appendix E tables are labelled "Figure 7", and their "Value" column does not say it is U. A reader working from text and tables, as accessibility and archival use often require, cannot check the reliability claims. Remedy: add one results table (region × condition × dataset) giving ICC form, point estimate, 95% CI and n. Name each test with its statistic, df and p. Relabel Appendix E as tables with a "U" column. Whether these are the right tests is for the methodology seat.
**Severity**: Major
**Evidence Anchor**: text: §5-§6 "we use a two-way random, single score ICC"; "χ2 = 0.26"; "V 2 = 0.0766"
**Confidence**: 3 — Figs. 3, 5 and 8 may carry some of the missing values; the absent ICC form, CIs and test names are confirmed in text and captions

### W8: The MANOVA result sentence reverses the model
The MANOVA is specified with region as the independent variable and the per-subject annotations as dependent variables, but the result is reported as annotations being a "predictor of the region". This inverts the stated model and invites misreading as a classification result. Remedy: report it as "annotator region had a significant multivariate effect on per-subject MST annotations (Pillai's trace = 1.97, F(df1, df2) = ..., p = ...)".
**Severity**: Minor
**Evidence Anchor**: text: §6 "high predictor of the region of the annotators"
**Confidence**: 5 — direct reading of the stated model against the reported sentence

### W9: Small numeric inconsistencies in the expert study
With 18 analysed subjects, 15/18 = 83.3%, not 83.4% (88.9% = 16/18 is consistent). §5 says the photographers annotated "19" MST-E images per round. Footnote 4 excludes one subject, and Appendix E lists 18 (S16 absent), so 18 were analysed, and the MST1 category then has a single subject in the expert study. Remedy: correct the percentage, state 18 analysed of 19 shown, and note which MST level lost a subject.
**Severity**: Minor
**Evidence Anchor**: text: §5 "88.9% in India and 83.4% in the United States"; "19 from the MST-E Golden Images or Challenging"
**Confidence**: 5 — arithmetic check against Appendix E row count

### W10: The data card's attribute distribution does not reconcile with the dataset totals
The data card snapshot and §3 give 1515 images and 31 videos. The "Distribution of human attributes" table sums to 1512 images and 34 videos across MST 1-10 (subjects sum correctly to 19). Users who rely on the card for stratified evaluation need the per-level counts to match the files. Remedy: reconcile the counts against the released CSV and correct either the totals or the per-level rows. If three images carry no MST label, say so.
**Severity**: Minor
**Evidence Anchor**: table: Appendix C, Distribution of human attributes (Images row sums to 1512, Videos row to 34, versus Data Snapshot 1515 and 31)
**Confidence**: 4 — direct summation of the extracted table; an extraction artefact is possible but the numbers parse cleanly

### W11: Data card copy errors
"Data Subject(s)" reads "Data about image search queries", apparently carried over from another card. The subjects are photographed people. The crowd workforce's "Number of unique annotations" is blank. "Model Evalutation" is misspelled. The provenance line "Annotated by a human expert" omits the author pre-annotation step described in §3. Remedy: correct these fields and state the crowd annotation count (about 25 × 1515 minus skips).
**Severity**: Minor
**Evidence Anchor**: text: Appendix C "Data about image search queries"; "Model Evalutation"
**Confidence**: 5 — verbatim data card content

### W12: Whether the reference label applies per image or per subject is stated inconsistently
§3 calls the reference labels the "oracle or intended annotations for the images", implying per-image labels. The data card says each subject received a single value (19 unique annotations). The difference changes what the lighting result means. Against a subject-level label, it measures annotators' compensation for lighting. Against image-level labels, it measures agreement on the perceived tone of each image. The data card resolves this, but the main text should not leave it to the appendix. Remedy: one sentence in §3 stating that every image of a subject is scored against the subject's single reference label.
**Severity**: Minor
**Evidence Anchor**: text: §3 and Appendix C "We refer to these annotations as the oracle or intended annotations for the images"; "was annotated with a single MST-E value"
**Confidence**: 4 — reading of §3 against the data card

### W13: Unstable terminology for the study, the annotators and the reference
- The photographer study is called a "qualitative survey" but is analysed with ICC and Mann-Whitney tests.
- "Experts" is scare-quoted for the photographers in §4, unquoted as "subject matter experts" in §7, and used for Dr. Monk in the abstract.
- The reference labels are variously "oracle", "intended", "golden annotations" and "ground truth". "Golden" also names the one-image-per-subject Golden Images set, a different object.
- "Image quality" and "lighting conditions" are used interchangeably, as are "well lit/poorly lit" and Golden/Challenging.

Remedy: a short terminology paragraph in §4, then consistent use: "photographer panel", "reference annotation", "Golden/Challenging set", "lighting condition".
**Severity**: Minor
**Evidence Anchor**: text: §4 and §2 "is a qualitative survey with a group of skin tone"; "compared to an expert ground truth assessment"
**Confidence**: 5 — direct reading across sections

### W14: Gender identity is described as a "non-subjective" attribute
§2 contrasts "subjective attributes such as skin tone" with "non-subjective attributes such as gender identity and age". The intended distinction is self-reported versus third-party-perceived. Calling gender identity non-subjective will read as a category error to much of the fairness readership and distracts from the paper's point. Remedy: rephrase as "self-identified attributes (e.g., gender identity) and directly reportable attributes (e.g., age) versus perceived attributes".
**Severity**: Minor
**Evidence Anchor**: text: §2 "non-subjective attributes such as gender identity and age"
**Confidence**: 4 — field-norm judgement on terminology for this readership

### W15: Collected annotation metadata is never reported
Both studies collected which body region the rater used, and the photographers also rated difficulty on a 5-point scale. Crowd raters could flag difficulty and skip images. None of these are analysed, summarised or listed among the released CSV fields. They bear directly on the lighting claim (W1) and on skip-driven missingness. Remedy: summarise body-region use and difficulty by condition, report skip counts, and either release these fields or say why not.
**Severity**: Minor
**Evidence Anchor**: text: §6 "report which part of the body they primarily used to make the selection"; "skip the task if no skin was visible"
**Confidence**: 5 — collected variables are named in §5-§6 and absent from the results and the data card

### W16: An unreported pilot is used to justify a key design choice
The choice of photographers over dermatologists rests on a pilot in which dermatologists reportedly assessed skin beneath clothing. No sample size, procedure or data are given. Appendix L also cites this pilot as the answer to a prior reviewer's concern. Remedy: report the pilot's n and procedure in a sentence or footnote, or present the choice as a design rationale rather than a finding.
**Severity**: Minor
**Evidence Anchor**: text: §5 "During an initial pilot we found that different types of experts may"
**Confidence**: 5 — no pilot details appear anywhere in the text

### W17: The ethics review statement is not verifiable
"Under the guidance of our institution's ethics body" gives no approval or exemption identifier and does not say whether formal review occurred. Subject consent to release is stated. Annotator consent is covered only by GLG's terms and conditions for the photographers and is not stated for crowd workers. For work with human raters and a sensitive perceived attribute, this is expected documentation. Remedy: state the review type and its outcome or identifier, and how crowd annotators were informed and consented.
**Severity**: Minor
**Evidence Anchor**: text: §4 "conducted under the guidance of our institution"
**Confidence**: 4 — standard dataset-track ethics documentation expectation

### W18: "Open access" and account-gated access are described inconsistently
§3 calls MST-E "open-access", while §7, Appendix H and the data card require a Google account and present the lack of anonymous access as a misuse mitigation. The crowd annotation CSV, meanwhile, sits at a public storage URL. Readers need to know exactly what is gated, why, and whether an account requirement tied to one vendor is the right control. A signed research-use agreement is the more common dataset-track mechanism. Remedy: replace "open-access" with an accurate access description, state what each artefact requires, and justify the gating choice.
**Severity**: Minor
**Evidence Anchor**: text: §3 and §7 "the open-access MST-E dataset"; "do not allow for anonymous access to the image dataset"
**Confidence**: 4 — direct textual comparison; norms judgement within my remit

### W19: Generalisation statements about Open Images go beyond what was measured there
On Open Images the paper measures ICC and regional distribution differences only. There is no reference label, so there is no alignment or accuracy measure. Yet §7 says annotators "perform similarly" on Open Images and MST-E, §6 says the recommendations "likely translate to real-world scenarios", and the limitations paragraph says the results "will translate to other domains". "Other domains" is unsupported. The paper never defines which domains it means, and the extension stays within face imagery. Remedy: say "reliability and regional differences were similar on Open Images", and remove or qualify "other domains".
**Severity**: Minor
**Evidence Anchor**: text: §7 "they perform similarly on the in-the-wild subset of Open Images"; "we believe our results will translate to other domains"
**Confidence**: 4 — wording compared against the measures reported in §6

### W20: Contribution delineation against prior skin tone annotation work is implicit
The paper notes that crowd and expert FST annotations are known to agree closely [33, 48]. It then reports the analogous MST result without saying what is new: a finer 10-point scale, five regions at 25 replications, a lighting-paired set, and an in-the-wild transfer check. There is also no comment on what a ±1 tolerance means on a 10-point versus a 6-point scale. The only explicit contributions list is in the Conclusion, and the introduction's RQs are not mapped to the contributions. Remedy: add a short contributions paragraph at the end of §1 that names each new element against [33, 34, 48] and points to the section that delivers it, plus one sentence on the ±1 threshold across scale lengths.
**Severity**: Minor
**Evidence Anchor**: text: §2 "expert and crowdsource annotators tend toward fairly similar annotations on the FST"
**Confidence**: 4 — editorial originality assessment from the paper's own related-work framing

### W21: The scale's stated design scope sits only in an appendix and is not linked to the regional findings
Appendix A.2 says MST was designed to capture skin tone diversity across the Americas, and frames its suitability as a hypothesis. The main text presents MST's suitability as established and recruits raters in India, the Philippines, Hungary and Ghana. If the reference swatches were designed around an Americas frame, that bears directly on how to read the regional differences in §6. Remedy: move the design-scope sentence into §2 or §3 and discuss it in §7 alongside the regional results.
**Severity**: Minor
**Evidence Anchor**: text: Appendix A.2 "to optimally capture ethnoracial diversity in skin tone across the Americas"
**Confidence**: 4 — direct comparison of Appendix A.2 with §2

### W22: Citation attribution errors
§2 attributes the Casual Conversations dataset to Hazirbas et al. [38]. Appendix A.3 attributes it to Liu et al. [51], which by its title is the speech-transcription companion. Reference [50] is cited (with [33, 48]) for crowd-expert FST agreement, but its title concerns the absence of images of skin of colour in COVID-19 publications and does not suggest an agreement study. Remedy: correct the A.3 attribution, and check that [50] supports the agreement sentence or replace it.
**Severity**: Minor
**Evidence Anchor**: text: Appendix A.3 "Liu et al. [51] released the Casual Conversations Dataset"
**Confidence**: 3 — based on reference titles only; I did not consult the cited works

### W23: What is and is not released is not stated in one place
Appendix L says "We release the annotations", but only the MST-E crowd annotations are released. The released crowd CSV has subject, image, region and annotation only. It has no annotator identifier, no lighting or difficulty field (lighting needs an undocumented join on image name), and no body-region field. The photographer annotations, the 86,809-face Open Images annotations, the distractor set, the instructions and the analysis code are not mentioned as released or withheld. The data card describes the crowd file as "for replication purposes only", but the expert and Open Images results cannot be reproduced from the release. Remedy: add a release-scope table listing each artefact, released or withheld, and the reason. Add annotator IDs, or state why they are omitted, and document the image-to-lighting join. Whether the withheld items fall short of the field's reproducibility bar is for the methodology seat.
**Severity**: Minor
**Evidence Anchor**: text: Appendix L "We release the annotations with this paper."
**Confidence**: 4 — data card field lists and Appendices C, J and L read together

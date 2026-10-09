contract_role: eic
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: writing_and_structure
score: warn
trigger: "limitations are present but thin; or the length balance is off, for example background that dwarfs the method and evaluation sections"

The argument can be followed from start to finish. The contributions promised in the Introduction are each delivered by a dedicated subsection, and the experiments share a consistent Task/Method/Results scaffold. The exposition is uneven, though. The procedure that turns an image into the proposed L* and h* scores appears only in the appended supplement, while background on prior scales takes up a large share of the main text. The paper also has no consolidated limitations or responsible-use discussion for its own measure, and several notation, terminology and caption defects add friction for the reader.

## Review Body

Viewed from editorial oversight, this is a short, readable measurement paper whose central idea is easy to state: report CIELAB perceptual lightness L* as skin tone and hue angle h* as skin hue, and show that the hue axis surfaces dataset and model disparities that a tone-only scale does not. The Introduction states the contribution plainly and lists three uses: dataset skew, model disparities in cropping and verification, and causal manipulation for attribute prediction. Sections 4.1, 4.2 and 4.3 each deliver one of them, so readers never lose the thread. The experiment sections use a repeated Task/Method/Results layout, which suits a benchmark-style paper.

My D2 concerns fall into three groups. First, proportion and placement. Section 2 and the first half of Section 3 review the Fitzpatrick scale and ITA at length. The proposal itself, by contrast, is given in the main text only as two colour-space definitions plus a forward pointer, and the pointer names a robustness figure rather than the method section. Everything a reader needs to re-implement the per-image score is in Supplementary A.2: skin segmentation, per-pixel conversion, K-Means into five clusters, Sturges-binned histogram modes, keeping the three lightest clusters, and size-weighted averaging. Second, the paper offers a new demographic-adjacent measurement tool and closes by recommending it for use "from data collection to model deployment". Yet it has no section that gathers the measure's own limitations and misuse risks. The only self-limitation in the main text concerns the image-reconstruction step in Section 4.3. Third, a set of local defects. The stated range of the hue angle conflicts with the values the paper prints. The Elo exposition has an index error and an undefined conversion to a percentage. Terminology for labels, datasets and the measure itself drifts. One method caption is truncated. There are also copy-editing slips, including the dated term "transgendered" in an otherwise careful ethics passage.

Why warn and not block. My Phase 1 block trigger covers material needed to understand the main claim that exists only in supplementary files, and limitations or responsible-use discussion that is absent. Neither applies in full. The main text defines L* and h* and their thresholds well enough to understand and assess the headline claim, and the supplement is bound into the same document. Limitations and ethics content does exist, notably the gender-classification disclaimer, the reconstruction caveat and the apparent-versus-true-colour framing, but it is scattered and thin rather than missing. Why warn and not pass. The imbalance between background and method, the missing consolidated limitations, and the cumulative notation and terminology defects go beyond polish. They are the "uneven exposition" pattern my Phase 1 warn trigger names.

I make no venue-alignment claim, because no target-criteria authority was supplied for this run. I found no instruction-like content addressed to reviewers in the manuscript.

### S1: Explicit contribution statement that the body delivers one-for-one
The Introduction names one primary contribution and three demonstrations, (i) to (iii). Sections 4.1, 4.2 (4.2.1 and 4.2.2) and 4.3 map onto them directly, and the Section 4 preamble restates the mapping. A reader can check every promise against a specific subsection.
**Evidence Anchor**: `text: Sec. 1, p. 2 "Our main contribution is to demonstrate the relevance"`

### S2: Consistent Task / Method / Results scaffold across experiments
Every model experiment opens with a Task paragraph, follows with Method, and ends with Results. This lets readers who know the conventions of the cropping, verification and attribute-prediction literatures jump to the parts they need.
**Evidence Anchor**: `text: Sec. 4.2.1, p. 5 "Task. The saliency-based image cropping task produces a"`

### S3: Explicit ethical framing of the gender-classification experiment
The authors say outright that they report binary gender classification as an audit target, not as an endorsed task, and they cite the harms to non-binary people. This is the kind of responsible-use framing readers of fairness work expect.
**Evidence Anchor**: `text: Sec. 4.3, p. 8 "condone the gender classification task, as it causes harm to"`

### S4: Candid statement of the causal setup's dependence on reconstruction quality
The paper says that e4e/StyleGAN3 reconstruction alters non-target attributes. It explains the design choice that follows, which is to compare manipulated images with the reconstruction rather than with the original, so readers can read Table 4 correctly.
**Evidence Anchor**: `text: Sec. 4.3, p. 8 "A current limitation of this setup lies in the image"`

### S5: Qualitative figure that makes the two axes concrete
Figure 4 prints L* and h* beneath every face for the reconstructed, +light, +dark, +red and +yellow versions and for the CelebA "pale" direction. Its caption explains on its own terms why the proposed directions give independent control while "pale" does not. This is the clearest piece of exposition in the paper.
**Evidence Anchor**: `figure: Figure 4, panels (b)-(h) with per-face L* and h* annotations and self-contained caption`

### S6: Public code pointer in the main text
Section 4 links to a code repository. This partly offsets the brevity of the method description in the main text and fits the conventions of method-focused vision papers.
**Evidence Anchor**: `text: Sec. 4 preamble, p. 4 "Code can be found at"`

### W1: The score-extraction procedure, the paper's actual method, is only in the supplement, and the main-text pointer misdirects
**Problem**: The main text never says how a single L* and h* value is obtained for an image. It does not mention segmentation, clustering, histogram modes, the exclusion of the two darkest of five clusters, or size-weighted averaging. Section 3 ends by deferring to "Figure S3", which is a relighting robustness figure. The procedure itself is in Supplementary A.2 and Figure S2, and the main text references neither. Meanwhile Section 2 and the ITA material in Section 3 occupy roughly two pages on prior scales.
**Evidence Anchor**: `text: Sec. 3, p. 4 "provide the details of the methodology and a robustness" ... "analysis to different illuminations in Figure S3"`
**Why it matters**: The submission's contribution is a measurement tool. A reader of the main text cannot see the design choices, such as discarding low-L* clusters or taking the histogram mode, that shape every number in Tables 1 to 4. The proportion also inverts what readers of a method-focused paper expect, with more space on the scales being replaced than on the proposed measure.
**Suggestion**: Move a condensed version of A.2 into Section 3: a short numbered pipeline with the cluster count, the retention rule and the aggregation formula, and reference Figure S2 or move it into the main paper. Trim the Fitzpatrick and ITA history in Sections 2 and 3 to make room. Fix the pointer so it names Section A.2 for the method and Figure S3 for robustness.
**Severity**: Major
**Confidence**: 4 — core expertise: structure of CV fairness measurement papers

### W2: No consolidated limitations or responsible-use discussion for the proposed measure
**Problem**: The paper criticises the limitations of the Fitzpatrick scale and ITA at length but never gathers the limitations of its own L*/h* score. Several are visible in its own material: L* shifts by up to 6 points under relighting while the light/dark cut is at 60. The binary thresholds are taken from cutaneous colorimetry of constitutive skin colour, not apparent colour. Scores depend on a skin segmenter trained on CelebAMask-HQ. Supplementary A.3 frames the axes as separating ethnic groups, which raises the question of whether the measure could be misused as an automated ethnicity proxy. The Conclusion makes broad deployment recommendations and states no limitations at all.
**Evidence Anchor**: `absence: Sec. 5 Conclusion and any Limitations or Broader Impact section — expected a consolidated discussion of the proposed L*/h* measure's validity limits and misuse risks; checked Secs. 1-5, the Sec. 2 social-impact paragraph, the Sec. 4.3 reconstruction caveat, and Supplementary A.1-A.4`
**Why it matters**: The paper positions itself as a fairness tool that practitioners should adopt. Readers of fairness-oriented vision work expect the conditions under which the tool is unreliable, and the ways it should not be used, to be stated in one place. Without that, the closing recommendation reads as unqualified.
**Suggestion**: Add a dedicated Limitations and Responsible Use subsection, either before the Conclusion or merged into it. Cover sensitivity to illumination and makeup with reference to Figures S1 and S3, the provenance and fixedness of the 60 and 55 degree thresholds, segmentation dependence, scope limited to faces, and explicit guidance against using L*/h* to infer race or ethnicity of individuals.
**Severity**: Major
**Confidence**: 4 — core expertise: responsible-AI review norms for demographic measurement tools

### W3: Hue-angle definition conflicts with the values the paper reports
**Problem**: Eq. (2) defines h* as arctan(b*/a*) and states that it ranges from 0 to 360 degrees. A plain arctangent of a ratio cannot cover that range. The supplement also prints negative hue values for several faces in Figure S1. Readers cannot tell which convention (arctan, atan2, or a wrapped angle) produced the reported numbers.
**Evidence Anchor**: `equation: Eq. (2) h* = arctan(b*/a*) with stated 0-360 degree range, versus negative h* values printed under Figure S1 panels (a), (c), (d), (e)`
**Why it matters**: h* is one of the two quantities the paper introduces. Inconsistent notation for a core symbol undermines confidence, even though most analysed values sit in the first quadrant.
**Suggestion**: Define h* with atan2 and state its range explicitly. Then either explain negative values, as a* < 0 cases, or report them consistently with the stated range.
**Severity**: Minor
**Confidence**: 4 — core expertise: colour-space notation in vision papers

### W4: Elo exposition has an index error and an undefined conversion to a percentage preference
**Problem**: In Section 4.2.1 the text assigns the complementary probability p_j to image x_i instead of x_j, and says the update applies "if j looses". The Results then report "60.73%" and "58.25%" preferences derived from average Elo scores without saying how a group-average Elo difference was converted to a percentage.
**Evidence Anchor**: `text: Sec. 4.2.1, p. 6 "an average Elo score indicating a 58.25% preference"`
**Why it matters**: The cropping benchmark's headline numbers are expressed in this derived unit, and readers cannot reproduce or interpret them from the text.
**Suggestion**: Correct the indices and wording, and state explicitly the formula that maps the mean Elo gap between groups to a preference probability.
**Severity**: Minor
**Confidence**: 4 — core expertise: pairwise-comparison benchmarks in CV

### W5: Terminology and notation drift across labels, datasets and the measure itself
**Problem**: The cropping benchmark speaks of "race labels" and then describes the same CFD annotations as "self-reported ethnic labels". The 70,000-image dataset is called FFHQ-Ageing in the text but labelled FFHQ in Figure 2, Table 1 and Table 2. The proposed quantity is called a score, a scale and a measure interchangeably, and Section 4.2.1 says the authors "extract skin color scales". The symbol a means a race label in 4.2.1, a target attribute in 4.3, and the CIELAB a* component in Section 3.
**Evidence Anchor**: `text: Sec. 4.2.1, p. 5 "We extend it to multiple race labels"`
**Why it matters**: Precise terms for demographic constructs matter in fairness writing, and race and ethnicity are not interchangeable. Swapping dataset names hides whether the Table 2 comparison is against the same images as Table 1(b).
**Suggestion**: Choose one term for each construct and define it once (for example, "ethnicity (self-reported)", "FFHQ (with FFHQ-Ageing masks)", and "skin color score"). Rename the overloaded symbols.
**Severity**: Minor
**Confidence**: 4 — core expertise: fairness terminology conventions

### W6: Related work catalogues prior uses but does not position the proposal against other automatic skin-colour estimators
**Problem**: The "Applications in fairness assessment" and bias-mitigation paragraphs list tasks and methods by citation without contrast. The Monk Skin Tone scale gets one "concurrent" sentence. Prior automatic or algorithmic skin-tone estimators that the paper cites elsewhere, such as ITA-based pipelines and scene-disambiguated skin-tone estimation, are never compared with the proposed extraction. Only Merler et al. is discussed as a starting point.
**Evidence Anchor**: `text: Sec. 2, p. 3 "identification in facial recognition [8, 35, 58], image cap"`
**Why it matters**: Readers need to know what the proposed extractor does differently from existing automatic estimators, not only from Fitzpatrick annotation, in order to judge novelty and choose between tools.
**Suggestion**: Replace the citation lists with a short comparative paragraph. For each prior automatic estimator, say what dimension it measures, how it aggregates pixels, and how the proposal differs.
**Severity**: Minor
**Confidence**: 3 — adjacent expertise: skin-tone estimation literature in vision

### W7: Abstract spends its space on history and omits method and findings
**Problem**: About half of the abstract retells Gender Shades and the adoption of Fitzpatrick. It does not mention how scores are extracted from images, which three benchmarks are run, or any concrete finding beyond the statement that hue "reveals additional biases".
**Evidence Anchor**: `text: Abstract, p. 1 "In their seminal paper Gender Shades, Buolamwini"`
**Why it matters**: For method-focused vision venues the abstract is the main way readers triage a paper. As written, it undersells what the paper actually does.
**Suggestion**: Compress the background to one sentence. Add one sentence on the extraction pipeline and one on the headline dataset, cropping, verification and attribute-prediction findings.
**Severity**: Minor
**Confidence**: 4 — core expertise: abstract conventions at CV venues

### W8: Method-overview caption is truncated and table captions are not self-contained
**Problem**: The caption of Figure S2, the only figure that depicts the extraction pipeline, breaks off mid-word. Table 3 uses the column headers L+R, L+Y, D+R and D+Y and bold highlighting, and neither the caption nor the text defines them.
**Evidence Anchor**: `figure: Figure S2 caption, final sentence ends mid-word at "to get the f"`
**Why it matters**: Captions should be readable on their own. A broken caption on the method figure compounds the placement problem in W1.
**Suggestion**: Restore the full Figure S2 caption. Define the intersectional abbreviations and the meaning of bold in the Table 3 caption.
**Severity**: Minor
**Confidence**: 5 — directly visible on the rendered pages

### W9: Copy-editing errors, including a dated term in the ethics passage
**Problem**: There are several slips: "verify the identify" (identity); "Alahuf et al." for Alaluf; "results in a increase"; "if j looses"; "Any discrepancy would then corresponds"; "a representative scalar scores"; "have a darker skins"; and a stray full stop mid-sentence in the Figure S3 caption. The ethics passage in Section 4.3 uses "transgendered", which current style guidance replaces with "transgender".
**Evidence Anchor**: `text: Sec. 4.2.2, p. 6 "as they better verify the identify of light-skinned"`
**Why it matters**: Each slip is small, but together they signal a hurried revision. The terminology slip is notable in a paper whose ethics framing is otherwise careful.
**Suggestion**: Do a full proofreading pass, and replace "transgendered individuals" with "transgender individuals".
**Severity**: Minor
**Confidence**: 5 — directly verifiable in the text

### W10: Claim language in the Conclusion outruns what is shown
**Problem**: The Introduction and Conclusion describe the surfaced disparities as "previously invisible", and the Conclusion recommends the measure across the whole pipeline and for other human-centric tasks. The paper shows hue-split disparities. It does not show that those disparities are distinct from known ethnicity-linked effects, and Supplementary A.3 itself cites prior evidence of lower performance for Asian individuals.
**Evidence Anchor**: `text: Sec. 5, p. 9 "and computer vision models, previously invisible."`
**Why it matters**: Overstated framing invites pushback from readers in this area. It also clashes with the paper's own careful "first step" wording in the Conclusion.
**Suggestion**: Change the framing to "not captured by a tone-only scale" and limit deployment recommendations to the settings actually evaluated.
**Severity**: Minor
**Confidence**: 3 — writing-calibration judgement; the substantive evidence question belongs to the methodology seat

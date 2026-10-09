# V1 text-fidelity verification: K01–K12 and strengths S-a to S-g

**Paper:** Thong, Joniak & Xiang, "Beyond Skin Tone" (ICCV 2023; arXiv 2309.05148v2).
**Lens:** Does the paper actually say, omit or show what each issue claims? I checked the full manuscript, including §A.1–A.4 and every figure and table label, against the rendered pages p1, p4, p6, p7, p12, p13 and p14.
**Stance:** Adversarial. I tried to refute each issue, and I recomputed the LOCAL numbers where I could.

Severity bands are the canonical ones:
- Critical: alone invalidates a core claim.
- Major: materially weakens a core claim and needs substantial reanalysis or new data.
- Minor: clarity or rigour.

## Summary table

| ID | Verdict | Proposed | Corrected | One-line reason |
|---|---|---|---|---|
| K01 | PARTLY CONFIRMED | Major / poss. Critical | **Major** | The anchor is absent, but the construct is apparent colour, so colorimeter readings of the people are the wrong criterion. The tone anchor is partly supplied by LOCAL ρ = −0.76. Claims are unsupported, not refuted. |
| K02 | CONFIRMED | Major | **Major** | No agreement statistic of any kind. The LOCAL ICCs need stress-test caveats. |
| K03 | CONFIRMED | Major | **Major** | Fig. S3 is the DPR demo (one face, 7 achromatic SH lights). h\* is fixed by construction, and the printed L\* range contradicts "up to 6". |
| K04 | PARTLY CONFIRMED | Major | **Major** | "No sensitivity analysis" overstates: §A.4/Fig. S6 gives descriptive histograms for composition. There is none for the model audits. The paper's own §A.2 says [46] concerns constitutive cutaneous measurement. |
| K05 | PARTLY CONFIRMED | Major / poss. Critical | **Major** | The "red skew" vanishes a few degrees below 55° in the paper's own Fig. S6. Light skew and the Table 2 "reproduce" comparison survive. |
| K06 | PARTLY CONFIRMED | Major | **Major (provisional; Minor on paper text alone)** | There is a stated rationale (shadows and facial hair), so the estimator is not "unjustified". Code facts are mislabelled as paper facts. The LOCAL tone dependence needs caveats. |
| K07 | CONFIRMED (absence) / PARTLY (mechanism) | Major | **Minor** | L\*+h\* follows the cited precedent [17]. The paper's own §A.4 reports lower hue spread for dark tones. Tone-dependent noise is already counted in K02/K06. |
| K08 | PARTLY CONFIRMED | Minor | **Minor** | Eq. 2 vs the 0–360° range vs negative Fig. S1 values is confirmed. "Negatives fall into red" is not shown: Figs. 2 and S6 contain no negative h\*. |
| K09 | PARTLY CONFIRMED | Major | **Minor** | One quote is a misquote. The paper scopes "apparent" explicitly and repeatedly. Drift is confined to a few sentences, and its substantive consequence is K05's. |
| K10 | PARTLY CONFIRMED | Major | **Minor** | "Never tested" is false: Fig. 3c tests hue within tone. The "orthogonal" contradiction is overstated, and §A.4 itself reports tone–hue dependence. The ITA and continuous-L\* comparisons are genuinely absent. |
| K11 | CONFIRMED | Major | **Major** | Hue tracks ethnicity (Fig. S5b), and Indian = CFD-India. Position and cropper version are unreported. Balanced tone composition (S-d) is confirmed. |
| K12 | PARTLY CONFIRMED | Major | **Minor** | All reporting and inference points are confirmed. The direction and significance very likely survive a Bradley–Terry refit, because differential shrinkage biases toward the null. Order effects were modest in our own simulation. The real threat is K11. |

---

## K01: No external validity anchor for L\*/h\*

**Verdict: PARTLY CONFIRMED. Corrected severity: Major.** The missing anchor leaves claim (i) unsupported, not refuted. A known-groups check exists (Fig. S5b), and LOCAL gives tone some convergent validity.

**Anchors checked**

- §2 (p3): "These annotation limitations indicate the need for quantitative and more objective measures for skin color."
- §3 (p3): "deriving quantitative metrics enables more reliable skin color scores" and "this mitigates the subjectivity of the (self-)annotator as well as the inter-rater reliability".
- Nowhere in §3, §4 or §A.1–A.4 is L\*/h\* compared with human ratings, instrument readings or colour-target captures. **Absence confirmed.**
- The paper does contain a weak known-groups check: Fig. S5b (CFD self-reported ethnicity) and §A.3 ("Asian subjects, which are mostly in the yellow side…").

**Corrections**

1. The paper does not call automatic scores "objective" outright. It argues for "quantitative and **more** objective measures" and claims "more reliable" scores. Quote it that way.
2. The issue leads with colorimeter or spectrophotometer readings "of the same people". The paper explicitly disclaims the true or constitutive colour that such instruments measure (§1: "we are interested in characterizing apparent skin color rather than true skin color"). Criteria that fit the stated construct come first:
   - multi-rater perceptual ratings of the *images*;
   - captures that include a colour target;
   - agreement with existing image-level MST or Fitzpatrick labels.

   Instrument readings remain relevant only because the cut-points are borrowed from colorimetry (K04).
3. Acknowledge the Fig. S5b known-groups evidence as weak but genuine.
4. LOCAL ρ = −0.76 has caveats: n = 19 subjects, well-lit images only, cheek mask, and approximate landmark masks rather than DeepLabV3. The local h\* figure is weak (ρ = −0.43, p = 0.06), and the pixel-mean hue figure is null (ρ = 0.03). So there is still no evidence either way for hue.

---

## K02: No reliability evidence

**Verdict: CONFIRMED. Corrected severity: Major.**

**Anchors checked**

- §A.2 "Robustness": the only probe is "a series of images in which the illumination changes … for a given individual" (Fig. S3).
- No seed, k, top-n, segmenter, binning, compression or within-identity agreement statistic appears anywhere.
- The paper uses two mask sources and never compares them: dataset masks for CelebAMask-HQ and FFHQ (§4.1) and DeepLabV3 for CFD (§4.2.1).

**Corrections**

1. Change "no within-identity agreement" to: "no within-identity agreement statistic on real images. The only within-identity probe is the n = 1 synthetic relighting of Fig. S3 (see K03)."
2. Separate two demands.
   - **Instrument reliability** (seed, k, top-n, segmenter, binning, JPEG) is construct-neutral and clearly missing.
   - **Within-person agreement across lighting** is partly *construct-relevant* variation for an apparent-colour measure. The paper says "changes in perceptual lightness are expected" (Fig. S3 caption).

   The within-person demand bites hardest against two things: the paper's "h\* remains stable and robust" claim, and its person-level readings (K09).
3. LOCAL numbers reproduce from `mste_proc/analysis.json`:
   - h\* ICC = 0.286 [0.172, 0.401] across all images and 0.461 for well-lit images;
   - L\* ICC = 0.133 across all images and 0.502 for well-lit images;
   - within SD = 12.2° (all) and 11.8° (well-lit); between SD = 8.0° and 10.9°.
4. Add these caveats:
   - MST-E is a **stress test**. It has deliberately poorly lit images (572 of 1,304) and pose variation (558 side, 150 bottom, 431 facing, 165 frontal).
   - The images are Pixel "PORTRAIT"-mode JPEGs.
   - The masks are approximate, from Apple Vision landmarks.
   - The well-lit ICCs (about 0.46 for h\*, 0.50 for L\*) are the fair headline. The all-image ICCs (0.13 and 0.29) overstate the problem for curated datasets.
5. Add a finding that the issue omits. The *pixel-mean* hue ICC is also low (0.28 well-lit, cheeks). So much of the instability is in the images, not only in the estimator.
6. I confirmed "same day" from the filenames: all are PXL_20220922.

---

## K03: The Fig. S3 robustness test

**Verdict: CONFIRMED. Corrected severity: Major** for the evidential void on h\* robustness. The "6 points" misreport on its own would be Minor.

**Anchors checked (Fig. S3, rendered page 13)**

- The original is L\* = 66.63 / h\* = 59.12. The seven relit versions read:
  - L\* = 69.24, 69.66, 63.49, 70.48, 71.34, **59.41**, 64.58;
  - h\* = 57.08–59.08.
- The largest deviation is 66.63 − 59.41 = **−7.22**, against +4.71 on the upside. 59.41 is below 60, so this person crosses the cut-point under relighting alone. **Confirmed.**
- The caption and §A.2 both say "varies by up to 6 points" and "can differ from up to 6 points". Both are contradicted.
- §A.2 says "h∗ remains stable and robust to face relighting, which confirms that it provides complementary and orthogonal information about skin color than the skin tone". The quote is verbatim, and the non sequitur is confirmed.
- §3 overstates it further: "a robustness analysis to different illuminations in Figure S3". The analysis varies only direction and intensity (§A.2), not illuminant colour.
- Fig. S1(a) (p12) reads "Color cast L∗=37.10 h∗=−25.38". **Confirmed.**
- On the DPR mechanism, Fig. S3 is visibly the public DPR demo: the same portrait and 7 achromatic spherical-harmonics spheres. §A.2 says "samples coming from the work of Zhou et al. [81]". My independent recollection of the DPR demo is that it converts to OpenCV Lab, feeds only L to the network, writes the output into the L channel and converts back. That agrees with LOCAL §4. Per-pixel a\* and b\* are therefore fixed, apart from 8-bit and gamut-clipping effects. The 57.08–59.12° spread reflects which clusters the L-dependent top-3 selection keeps.

**Corrections**

1. "White light only" is accurate in effect: the SH lighting is achromatic and applied to luminance.
2. The paper never *claims* robustness to colour casts. §A.1 accepts that casts change apparent colour. State the critique as "the only test cannot fail for h\*", not "the paper claims chromatic robustness".
3. LOCAL §2.2 caveats: the "not ideal" and poorly-lit MST-E conditions are deliberately extreme, n = 15 golden/not-ideal pairs, and the masks are approximate. The per-person Δh\* range from −18.5° to +32° is real-lighting evidence against "h\* remains stable", with those caveats.

---

## K04: Thresholds borrowed from in-vivo colorimetry

**Verdict: PARTLY CONFIRMED. Corrected severity: Major.**

**Anchors checked**

- §4.1: "Threshold values are taken from Ly et al. [46]." No transfer argument appears anywhere. **Confirmed.**
- **Internal-inconsistency anchor the issue should add.** The paper itself says [46] concerns constitutive, instrument-based measurement:
  - §A.2: "Our objective differs from the cosmetics or dermatology fields, which requires an accurate assessment of constitutive skin color from cutaneous measurements [46]".
  - §2: "the usage of a spectrophotometer … remains the standard to provide the ground truth score of the true or constitutive skin color [46]".

  So the paper takes its apparent-colour cut-points from a source it describes as measuring a different construct.
- On sensitivity analysis, §A.4 says "we go beyond a simple binary thresholding … The different thresholds confirm the over-representation of light skin tones and red skin hues". Fig. S6 gives 20-bin histograms.

**Corrections**

1. "No sensitivity analysis" overstates the gap. There is a *descriptive* threshold-free view for dataset composition (Fig. S6). There is **no** sensitivity analysis for:
   - the model audits (Fig. 3, Table 3);
   - the labels used to learn the §4.3 edit directions.

   §A.4's "different thresholds confirm" is also contradicted by Fig. S6 itself (see K05).
2. Provenance remains **unresolved**. I could not access the full text of Ly et al. (JID 2020; the publisher returned 403).
   - 55° coincides exactly with the canonical **ITA** "very light / light" boundary (>55°, 41–55°, 28–41°, …; Chardon 1991 / Del Bino categories), which secondary sources attribute to this literature.
   - I found no source giving an L\* = 60 or h\* = 55° cut.
   - Treat "55° is an ITA cut-point transplanted to h\*" as plausible but unverified. If it is confirmed, K04 becomes sharper.
3. LOCAL corrections and caveats:
   - "Only 1.5% of MST-E images reach h\* ≥ 55°" should read **1.6% (21/1,304)** (recomputed).
   - "CFD is 72% yellow" is 533/739 from the Fig. 3 n's. That set is CFD plus CFD-India, scored with **DeepLabV3** masks rather than dataset masks.
   - The MST swatch h\* values (47–79°, MST10 C\* ≈ 5.8) are **not reproducible from any saved script**, so the source is undocumented.

     My recomputation from the commonly published MST hex codes (quoted from memory; sRGB D65) gives h\* ≈ 49–89° and MST10 C\* ≈ 3.8 (dh/da\* ≈ 14°/unit). That is also wide and non-monotonic, so the qualitative point stands. Cite the swatch source, or drop the exact numbers.

---

## K05: Dataset "skew" with no reference distribution; capture confounded with population

**Verdict: PARTLY CONFIRMED. Corrected severity: Major.**

- The tone half of claim (ii) has outside support: §4.1 says "as commonly hypothesized in the literature".
- The generator comparison in Table 2 uses FFHQ as its reference.
- The **hue-skew sub-claim is unsupported** and is close to Critical for that sub-claim alone.

**Anchors checked**

- Table 1 caption: "Images are skewed towards a light skin tone and a red skin hue while dark and yellow skin colors are underrepresented."
- §A.4: "distributions are unimodal with a bell curve shape."
- §A.3 (CFD): "the CFD dataset depicts less variation … explained by the fact that images in CFD have been captured in a controlled setting". The paper itself attributes distributional differences to capture.

**New fidelity finding that strengthens the issue**

Reading Fig. S6 by eye, the histograms are overlaid (light and dark are not stacked; the bar sums match Table 1's light and dark totals). The h\* medians sit at roughly **51–53° (CelebAMask-HQ)** and **46–48° (FFHQ)**.

- At a 50° cut, CelebAMask-HQ would be about 40–45% "red", a *yellow* majority.
- FFHQ is roughly balanced near 46°.

So the §A.4 claim that "the different thresholds confirm the over-representation of … red skin hues" is contradicted by the paper's own figure for cuts only a few degrees lower. These are approximate readings, ±2°. The released score files (`extract/results`, see S-c) would allow an exact check.

**Corrections**

1. "No reference distribution" is slightly overstated.
   - §4.1 implies an equal-cell-share target: "we recommend tracking both skin tone and skin hue … such that all subgroups are well balanced". That target inherits K04's arbitrary cut.
   - Table 2's "reproduce" claim has an explicit reference (FFHQ).

   Rephrase as: "no population or deployment reference. The implied equal-share target is defined only by the borrowed cut."
2. "The same instrument puts most CFD faces on the yellow side" is not quite the same instrument: CFD uses DeepLabV3 predicted masks, CelebA and FFHQ use dataset masks. Population mix also differs. Hedge to "the same estimator, with a different mask source and population".
3. Fig. S5b supports the capture confound visually: CFD White subjects straddle 55°, against an FFHQ that is 18% yellow overall.

---

## K06: Estimator design unjustified and unablated, with skin-tone-dependent error

**Verdict: PARTLY CONFIRMED. Corrected severity: Major, provisional.** On paper text alone this would be Minor, since it is an un-ablated heuristic. Major rests entirely on the LOCAL tone-dependence evidence.

**Anchors checked (§A.2)**

- "We cluster the face skin into five groups and keep the top-3 groups with the highest L∗ … inspired by how human artists would perform value grouping in five different groups when simplifying an image [57]". [57] is *Artists' Master Series: Color and Light*. **Art-book justification confirmed.**
- No ablation appears anywhere. **Confirmed.**

**Corrections**

1. "Unjustified" is too strong. The paper gives a functional rationale: "as some parts of the face can skew the results towards darker values (e.g., facial hair or shaded regions), we prefer to exclude some groups which yield a very low L∗", and "clustering can identify shaded areas of the face or facial hair". Say: "justified only heuristically, with no empirical check that the dropped clusters are shadows or hair".
2. "Left-edge Sturges mode" and "unstandardised [L, hue]" are **code facts, not paper text**. The paper says only "the mode of the histogram" and "a clustering algorithm, such as K-Means". Label them as coming from the released code.
3. LOCAL, recomputed from `scored_merged.csv` (well-lit):
   - Within-subject h\* SD by oracle MST is 6.7°, 8.2° and 16.2° for MST 1–3, 4–6 and 7–10, which matches. The groups contain 7, 6 and 6 subjects.
   - The **pixel-mean hue SD also roughly doubles** (4.4° → 8.7°). Part of the tone dependence is therefore in the images (low chroma or capture). The estimator roughly doubles it again. The issue attributes all of it to the estimator.
   - "Shifts MST 7–10 subjects about 14° toward red" is a **mean driven by two subjects**: subject_4 (−28°) and subject_12 (−37°). The other four range from −0.1° to −8.5°, and the median is about −8°. local_checks.md itself says the trend is ρ = −0.40, p = 0.09. The canonical text drops this caveat and must restore it.
   - The approximate-mask caveat applies throughout.

---

## K07: Low-chroma ill-conditioning; chroma dropped

**Verdict: CONFIRMED as an absence. The mechanism is PARTLY CONFIRMED. Corrected severity: Minor.**

**Anchors checked**

- The only use of "chroma" in the paper is the ITA aside (§3: "a perceptual lightness at value 50 corresponds to a maximum chroma").
- There is no C\* dimension and no chroma gate. **Confirmed.**

**Why I downgrade**

1. Dropping C\* follows the paper's cited precedent. §3 says "We take inspiration from de Rigal et al. [17], and focus on the measurement of L∗ for skin tone and h∗ for skin hue".
2. The paper's own data do not show inflated hue spread for dark images. §A.4 says "the hue angle has a lower spread for dark skin tones than light skin tones", and Fig. S6 bears this out visually.
3. The tone-dependent within-person noise that LOCAL finds is already counted in K02 and K06.
4. The magnitude in the paper's datasets is unknown.

**Corrections**

- The arithmetic (σ/C\*; dh/da\* = b\*/C\*² ≈ 9°/unit at C\* = 5.8) is correct.
- The swatch source caveat from K04 applies.
- "Applies to darker skin" should be hedged: plausible, and supported locally (pixel-mean SD doubling), but not visible in the paper's Fig. S6.

---

## K08: arctan vs atan2 and the stated range

**Verdict: PARTLY CONFIRMED. Corrected severity: Minor.** It could become Major if the excluded or negative fraction turns out non-trivial and tone-dependent. LOCAL finds negatives concentrated in MST 8–10.

**Anchors checked**

- Eq. 2: "h∗ = arctan (b∗/a∗) (2) where h∗ goes from 0 to 360◦ as a∗ and b∗ components are unbounded". **Confirmed.**
- Fig. S1 (CelebAMask-HQ) prints h\* = −25.38, −14.70, −0.70 and −4.22 (4 of 5 examples). **Confirmed.**

**Corrections**

1. "Negative values fall into red" is **not shown in the paper**. Figs. 2 and S6 (rendered p4 and p14) contain no negative h\*:
   - the Fig. 2 x-axis starts at about −4° with the data beginning near 0°;
   - the Fig. S6 histograms start at 0°.

   Yet Fig. S1 shows four negative CelebAMask-HQ images. Either such images were excluded or clipped before plotting and tabulating, or Fig. S1 used a different pipeline version. Rephrase as: "The handling of out-of-range h\* is undocumented. Under the stated 55° rule they would count as red unless silently excluded or clipped, and Figs. 2 and S6 suggest exclusion or clipping." That is itself an internal inconsistency worth reporting.
2. LOCAL 51/1,304 is recomputed and confirmed.

---

## K09: Construct drift

**Verdict: PARTLY CONFIRMED. Corrected severity: Minor.** The construct is scoped explicitly in §1, §A.1, §A.2 and the Fig. S3 caption. The drift sits in a handful of sentences and can be fixed by rewording. Its substantive consequence (balancing on capture conditions) is already K05.

**Anchors checked**

- Conclusion: "provide a comprehensive representation of its constitutive complexity". **Confirmed.** It is also in §1: "given the skin constitutive complexity".
- §4.1 recommendation: "we recommend tracking both skin tone and skin hue … such that all subgroups are well balanced". **Confirmed.**

**Corrections**

1. **Misquote.** The paper never says "classify people with lighter skin tones as more feminine". The verbatim options are:
   - §4 (p4): "classifiers tend to predict people with lighter skin tones as more feminine";
   - Table 4 caption: "models classify individuals as more feminine when their skin tone becomes lighter".
2. That example is weak in any case: it describes responses to image edits of the same people.
3. Better drift anchors are:
   - §1: datasets "under-represent dark-yellow skin color";
   - §A.3: "Black subjects having a darker and more yellow skin color than Indian subjects";
   - §A.3: "collecting data from White and Black subjects would be enough to cover the whole spectrum";
   - the in-vivo aging motivation in §1 ("Asian skin becomes darker and more yellow… [17]").

---

## K10: Incremental value of hue never tested; L\* and h\* correlated

**Verdict: PARTLY CONFIRMED. Corrected severity: Minor.**

**Anchors checked**

- §4.2.1 and Fig. 3c: "When performing independent t-tests with a Bonferroni correction, we find that all pairwise groups are statistically different (p <0.01), except for the light-yellow and dark-red". These are within-tone hue contrasts (LR vs LY, DR vs DY).
- §3: "Measuring L∗ instead of ITA avoids having correlated measures as both ITA and h∗ contain the b∗ component."
- §A.4: "the hue angle has a lower spread for dark skin tones than light skin tones … the yellow skin hue tends to have a larger skewness towards light skin tones than the red skin hue."

**Corrections**

1. "Never tested" is false. Fig. 3c tests hue *within* binary tone for the cropping audit, though that test is confounded by K11. What is genuinely absent:
   - any comparison with ITA;
   - adjustment for continuous L\* within the binary tone groups;
   - nested-model or ΔR² tests;
   - anything comparable for Table 3.
2. "Contradicting the orthogonal framing" is overstated. The paper's "orthogonal" statements concern edit directions (§4.3) and relighting (§A.2), not population independence. §3's "avoids correlated measures" refers to construction (the shared b\* term). §A.4 *itself* reports tone–hue dependence.

   Rephrase as: "the population association between L\* and h\* is never quantified, although it is computable from Table 1 and acknowledged qualitatively in §A.4. That makes incremental value an empirical question the paper does not answer."
3. Odds ratios recomputed from Tables 1–2 and the Fig. 3 n's:

   | Set | Type | Odds ratio |
   |---|---|---|
   | CelebAMask-HQ | in the wild | 0.557 |
   | FFHQ | in the wild | 0.633 |
   | StyleGAN3 | generated | 0.656 |
   | P2 | generated | 0.682 |
   | CFD | controlled | 0.958 |

   "0.56–0.68 in the in-the-wild datasets" mislabels the generated sets.
4. The LOCAL r(L\*, h\*) = 0.53 uses all images, poorly lit included; the well-lit figure is 0.42 (recomputed). Both rest on n = 19 subjects. The association is **estimator-induced**: pixel-mean hue has ρ = 0.03 with MST (LOCAL §2.4). It is evidence about the instrument, not about people, and should not be cited as a "data" correlation.

---

## K11: Cropping audit confounded with ethnicity and source; position and version unreported

**Verdict: CONFIRMED. Corrected severity: Major.**

**Anchors checked**

- §4.2.1: "we rely on Chicago Face Dataset (CFD) [47] and CFD-India [42], for a total of 739 unique facial images … 109 Asians, 197 Blacks, 142 Indians, 108 Latinos, 183 Whites". That gives 597 = CFD plus 142 = CFD-India, so Indian ethnicity is aliased with source. The 142 and 597 counts come from external knowledge of the datasets but are consistent with the paper's numbers.
- §4.2.1 then says "From CFD, we sample pairs". The source label is used loosely.
- "concatenate both facial images vertically with a white space in between and preserve their aspect ratio". There is no statement on randomising or counterbalancing top/bottom. **Confirmed unreported.**
- The cropper is identified only as "the saliency-based cropping algorithm of Twitter", with no version or commit. **Confirmed.**
- Fig. S5b (zoomed): Asians are mostly light-yellow, Black subjects mostly dark-yellow, the dark-red cell mostly Indian, and light-red mostly White and Latino. **Confirmed.**
- **Strength confirmed** from the Fig. 3 box labels: red = 127 L / 79 D (61.65% light) and yellow = 334 L / 199 D (62.66% light).

**Adversarial note to add**

The paper's own §A.3 motivates hue *because* it separates ethnic groups that tone collapses. A hue-group disparity that runs partly through ethnicity is therefore partly the paper's intended use. What the confound defeats is the *attribution*: "skin color preference of the Twitter cropping algorithm". The CFD-India source aliasing is an artefact pathway independent of that argument. Keep Major.

---

## K12: Elo inference

**Verdict: PARTLY CONFIRMED. Corrected severity: Minor.**

- The reporting and inference faults are real.
- B5's own simulation finds compression is greater for under-played groups. That biases group gaps toward the null, and order effects were modest (SD ≈ 10 Elo points per face).
- With n = 461/278 and 206/533, the direction and significance very likely survive a Bradley–Terry refit.
- The material threat to the cropping claim is K11. Rate this Major only when combined with K11, since the same covariate-adjusted Bradley–Terry model fixes both.

**Anchors checked**

- §4.2.1: "we set M = 400 and K = 16 and we initialize scores at 1400".
- Update rule: "R′i = Ri + K(Si − pi), and conversely for xj". This is zero-sum. **Confirmed.**
- "confirmed with a statistically significant independent t-test (p < 0.0001)". **Confirmed.**
- "an average Elo score indicating a 60.73% preference" and "58.25%". These are model-implied. The gaps 400·log10(p/(1−p)) = **75.7 and 57.9** check out.
- The design is 45 = C(10,2) cross-group combinations with no within-group games, so each group makes 9 × 500 = 4,500 appearances. **Confirmed.**

**Corrections**

1. "About 43–87 games" depends on the CFD gender × ethnicity split recalled by B5. The paper gives only the marginals (359 F / 380 M; 109/197/142/108/183). Ethnicity totals alone give roughly 46–83 (even split), and W9 says about 45–85. These are expected values under uniform within-group sampling, which the paper does not state.
2. "Order-dependent and unconverged" needs qualifying. Order dependence is real in principle but modest in our simulation. "Unconverged" rests on simulation with illustrative parameters.
3. "Bonferroni family undefined" should read "not stated; most naturally the 6 pairwise intersectional contrasts".
4. Whether the % figures transform the mean gap or average the pairwise probabilities is not stated. "Indicating" suggests the mean-gap transform.

---

## Strengths

| ID | Verdict | Anchor and caveat |
|---|---|---|
| S-a | **CONFIRMED** | §1 "The apparent skin color is the one depicted in images, and the one that a computer vision model would see"; §A.1 "we consider the 'apparent' skin color as this what computer vision models are seeing"; Fig. S3 caption. Caveat: drift in a few sentences (K09). |
| S-b | **CONFIRMED (with caveat)** | §3 "Measuring L∗ instead of ITA avoids having correlated measures as both ITA and h∗ contain the b∗ component." L\* and h_ab are CIELCh coordinates. The paper never uses the word "cylindrical", but the characterisation is fair. Caveats: Eq. 2 and the code use arctan, not atan2 (K08). "Avoids correlated measures" is by construction only; empirically L\* and h\* are associated (K10). |
| S-c | **CONFIRMED (partly from outside the manuscript)** | The manuscript states only "Code can be found at https://github.com/SonyResearch/apparent skincolor". The score release is **not stated in the paper**. I confirmed it from the repo README: "We also provide the results of this script in extract/results for the CelebAMask-HQ, FFHQ and CFD datasets". File contents unverified. The release would let K05 and K08 be checked exactly. |
| S-d | **CONFIRMED** | Fig. 3 prints n = 461/278, 206/533, and 334/199/127/79. Red is 61.65% light and yellow 62.66% light. |
| S-e | **CONFIRMED (with caveat)** | §4.2.1 "independent t-tests with a Bonferroni correction". Caveats: the family is not stated, and the t-tests run on dependent Elo ratings (K12). |
| S-f | **CONFIRMED** | §4.3 "we compare the performance of manipulated images with the reconstructed version rather than the original one in Table 4". Caveat: original-image accuracy is not reported. |
| S-g | **CONFIRMED (contrast weaker than claimed)** | §4.3 "The same does not hold when selecting the 'pale' attribute"; Fig. 4(g–h). The ±pale edits move h\* by 1.1–8.6°. The paper's own +red edit moves L\* by −0.8, **+7.62** and +2.17 across the three faces, and +yellow by −0.4, +2.3 and +3.8. So "pale" is less cleanly separated from the proposed edits than the text implies (see K17). |

---

## Cross-cutting fidelity notes for the merger

1. **§A.4 self-contradiction.** "The different thresholds confirm the over-representation of … red skin hues" is contradicted by Fig. S6. The h\* medians sit a few degrees below 55°, about 51–53° for CelebAMask-HQ and 46–48° for FFHQ. Add this to K05 and K04.
2. **§A.2 vs §4.1 on [46].** The paper itself says [46] concerns constitutive cutaneous measurement, which is a different construct from its own. Add this to K04.
3. **Figs. 2/S6 vs Fig. S1.** There are no negative h\* in the dataset plots, but four in the dataset examples. This points to undocumented exclusion or clipping. Add it to K08 and K20.
4. **LOCAL hygiene.** Four LOCAL numbers in the canonical list need caveats or corrections:
   - 1.5% should be 1.6%;
   - the K06 14° figure is driven by two subjects (median about 8°);
   - the K10 r = 0.53 is estimator-induced (n = 19, all images; 0.42 well-lit);
   - the MST swatch values have no saved source script.

   Every MST-E figure should carry the caveats: stress test with deliberately poor lighting and varied poses, approximate landmark masks, and n = 19 subjects.
5. I recomputed Table 1/2 odds ratios, the Fig. 3 composition, the Elo gaps, the MST-E ICCs, the negative-count, the ≥ 55° share and the well-lit SD-by-MST, and all match except where noted above.

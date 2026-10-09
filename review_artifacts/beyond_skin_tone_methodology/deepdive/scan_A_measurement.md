# Scan A: measurement and construct validity (colour science)

**Paper:** Thong, Joniak, Xiang, "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color" (arXiv 2309.05148v2)
**Perspective:** the instrument itself: the construct, the colour pipeline, the estimator, thresholds, and evidence for robustness, reliability and validity.
**Sources used:** the manuscript text and rendered pages p1, p4, p6, p7, p12, p13 and p14, plus the code facts the caller supplied (extract/predict.py).

**Quotes.** Quotes are verbatim from the pypdf extraction. I removed line-break hyphenation, and "∗" is written as "*".

**Page numbers.** Page numbers are PDF pages. The supplement starts on p12.

**Numerical checks.** I ran these myself in pure Python, with no files written. The sRGB(D65) to CIELAB conversion follows the skimage defaults (sRGB, D65, 2°). Small numerical differences from skimage are possible. The checks are labelled **[my computation]**.

**External knowledge.** Claims that rest on my own knowledge of other papers or code, which I could not check without web access, are labelled **[external, from memory]**.

## Summary

| ID | Title | Proposed severity | Conf. |
|---|---|---|---|
| A1 | Construct drift: "apparent" colour is defined as an image property, but conclusions are drawn about people and "constitutive" colour | Major | 5 |
| A2 | No reliability or validity evidence for the new instrument | Major (borderline Critical) | 5 |
| A3 | Apparent h* and L* in web images are dominated by capture and processing conditions, and the paper's own figures show it | Major | 4 |
| A4 | The "dataset skew" claims (Tables 1–2) have no reference distribution, so the hue skew mostly reflects where the cutpoint sits | **Critical** | 4 |
| A5 | The 60 / 55° thresholds come from in-vivo colorimetry and are applied to image-derived values in different units | Major | 4 |
| A6 | Dichotomisation at the cutpoints without propagating measurement error | Minor | 4 |
| A7 | The Fig. S3 robustness test cannot test h*: the relighting method fixes chroma by construction, and "up to 6 points" understates the printed values | Major | 4 |
| A8 | The hue computation uses `arctan`, not `atan2`: quadrants are conflated, the jump sits at the yellow pole, and Eq. 2 contradicts the code | Major | 5 (bug) / 3 (impact) |
| A9 | Per-pixel hue is ill-conditioned at low chroma; there is no chroma gating, and chroma is dropped as a dimension | Major | 4 |
| A10 | The cluster-and-top-3 estimator: unstandardised features, K=5/top-3 justified by an art book, no ablation, and a likely skin-tone-dependent bias | Major | 3 |
| A11 | The histogram-mode estimator: the code takes the left bin edge, and Sturges bins depend on range and resolution | Minor | 4 |
| A12 | The "orthogonal" and "independent" claims for L* and h* are overstated or circular | Major | 4 |
| A13 | Negative h* values in Fig. S1 contradict the definition and the axes of Fig. 2 and Fig. S6 | Minor | 4 |
| A14 | Masks: FFHQ-Aging's "ground truth" masks are model predictions, and the mask source is unreported for the generated and LFW images | Minor | 3 |
| A15 | The instrument is applied to the low-resolution scikit-learn LFW crops, and how a pair is assigned to a group is undefined | Minor | 3 |
| A16 | Recommending that datasets be balanced on apparent L*/h* invites balancing on lighting rather than on people | Major | 4 |
| A17 | Colorimetric inaccuracies and reifying labels ("red/yellow", "L*=50 is max chroma", 0–360° range) | Minor | 4 |
| A18 | Generality claims ("any camera", "any face pose") are not tested | Minor | 4 |

**Counts:** 1 Critical, 10 Major, 7 Minor.

---

## Findings

### A1. Construct drift: "apparent" colour is defined as an image property, but conclusions are drawn about people and "constitutive" colour
**Quoted text**
- p2: "we are interested in characterizing apparent skin color rather than true skin color"
- p2: "the true skin color characterizes the constitutive skin color without the influence of external factors such as illumination or color cast"
- p9 (Conclusion): "Measuring apparent skin color requires a multidimensional score to capture its variation and provide a comprehensive representation of its constitutive complexity."
- p2: "common image datasets are skewed towards light-red skin color and under-represent dark-yellow skin color"
- p4: "classifiers tend to predict people with lighter skin tones as more feminine, and people with redder skin hue as more smiley"
- p14: "with Black subjects having a darker and more yellow skin color than Indian subjects"
- p2, motivation: "when aging, Asian skin becomes darker and more yellow while Caucasian skin becomes darker and redder [17]"
- p3: "Colorimetry aims to represent faithfully the human perception of colors."
- p12: "Still, we consider the “apparent” skin color as this what computer vision models are seeing."

**Problem.** The paper carefully defines its construct as the colour of skin pixels in a given image. On p2 it defines "constitutive" colour as the true colour without illumination or colour cast. Yet it keeps moving from that construct to claims about people:
- The Conclusion describes apparent colour as representing "constitutive complexity".
- Datasets "under-represent dark-yellow skin color", which is a statement about the people in them.
- Ethnic groups "have" darker or yellower skin.
- The hue dimension is motivated by in-vivo, constitutive findings on aging skin [17] and by physiological harms (pulse oximetry, heart rate).

A second, separate slippage concerns perception. CIELAB is justified because it "reflects the human perception". But the construct is "what computer vision models are seeing", and models see pixel values, not percepts. If the target were human perception, CIELAB relative to the display's D65 white would be the wrong model. Human observers partly discount scene illuminant colour (colour constancy), so a perceptual measure would need a colour-appearance model with an estimated adapting white, such as CIECAM02/CAM16. If the target is model input, the perceptual justification is not needed. CIELAB is then only a convenient re-coordinatisation of sRGB, and "perceptual lightness" is a misnomer.

**Consequence.** All person-level readings are unsupported by the instrument as defined: the dataset under-representation of people, the ethnic-group hue profiles, and the recommendation to diversify data collection. The model-bias results (Fig. 3, Table 3) can only be read as "models perform differently on images whose skin pixels have these statistics". As A3 argues, those statistics carry illumination and processing as much as the person.

**Fix.**
- Pick one construct and keep to it.
  - **If image-level:** rewrite the person-level claims, for example "images in which skin pixels measure h* < 55° are over-represented". Remove "constitutive" from the Conclusion, and drop or reframe the in-vivo motivations.
  - **If person-level** (which the dataset-collection recommendation needs): validate it against colorimetry or self/expert report (see A2), and model capture conditions (see A3).
- If "perceptual" is kept, justify CIELAB over a colour-appearance model, or drop the perceptual framing.

**Severity: Major.** The conclusions most at risk are the dataset findings, the ethnicity analysis in A.3 and the recommendation. Repairing it needs either a substantial reframing or new person-level validation data.
**Confidence: 5**

---

### A2. No reliability or validity evidence for the new instrument
**Quoted text**
- p3: "deriving quantitative metrics enables more reliable skin color scores"
- p3: "this mitigates the subjectivity of the (self-)annotator as well as the inter-rater reliability"
- p4, criticising ITA: "the low correlation with expert annotations makes it less reliable [28]"
- p4: "We provide the details of the methodology and a robustness analysis to different illuminations in Figure S3."

**Problem.** The paper's main contribution is a measurement, but it reports none of the standard evidence a measurement needs:
- **(i) Test–retest reliability.** Does the same person get similar scores across different images? CelebAMask-HQ inherits CelebA identity labels, LFW has many identities with several images each, and CFD has several expressions per person. A within-identity intra-class correlation (ICC), or the within-identity variance relative to the between-identity variance, could be computed directly from the data already used.
- **(ii) Criterion validity against an instrument ground truth.** There is no comparison with spectrophotometer or colorimeter readings, or with photographs that include a colour reference target (a colour checker).
- **(iii) Convergent validity with human judgement.** There is no comparison with human ratings of perceived lightness or hue, nor with existing skin-tone labels such as Monk or Fitzpatrick annotations, despite the paper criticising ITA for exactly this ("low correlation with expert annotations").
- **(iv) Measurement uncertainty.** No measurement uncertainty is reported for any score.

The only robustness evidence is n=1 relit face (Fig. S3), which A7 shows cannot test h*. "More reliable" is asserted, not shown. Being automatic removes annotator variance but not instrument variance, and A3, A7 and A9 suggest the instrument variance from capture conditions is large.

**Consequence.** Without reliability and validity evidence, the reader cannot tell whether the h* groupings index skin or lighting and white balance. That leaves the core claim "the hue dimension reveals additional biases related to skin color" unsupported, along with every downstream group comparison.

**Fix.**
- Report a within-identity ICC for L* and h* on CelebA identities, LFW and CFD.
- Report the probability that the same identity gets the same binary label across its images.
- Validate against a dataset with paired colorimetry, or a dataset photographed with colour checkers.
- Report agreement with human perceived-colour ratings and with Monk-scale annotations where they exist.
- Report the per-image estimator variance, for example by bootstrapping the skin pixels.

**Severity: Major, borderline Critical.** This needs new analysis and probably new data. I did not mark it Critical only because missing evidence leaves the claims unsupported rather than refuted.
**Confidence: 5**

---

### A3. Apparent h* and L* in web images are dominated by capture and processing conditions, and the paper's own figures show it
**Quoted text**
- p12: "the “apparent” skin color can be affected by external factors in the scene environment or the camera setting (e.g., color cast, intensity and orientation of the illumination, low-light environment, etc)"
- p12–13: "the “apparent” skin color in images acquired from any camera, with varying acquisition parameters or lighting conditions"
- p14: "This is explained by the fact that images in CFD have been captured in a controlled setting, enabling fair comparisons among images."
- Fig. S1 (p12): "L*=37.10 h*=−25.38 (a) Color cast"
- Fig. S4 (p13): "L*=91.74 h*=14.05 (d) +contrast"

**Problem.** The pipeline assumes sRGB-encoded input with a D65 white (skimage defaults) and does no white balancing, colour constancy or exposure normalisation. It does not use any in-image reference (sclera, teeth, background neutrals) and records no capture covariates. In uncalibrated web images, the apparent hue and lightness of skin are strongly shaped by several factors:
- the illuminant's chromaticity, and auto white balance, which in face-dominated frames partly treats skin as the scene average
- the camera maker's preferred skin-colour rendering intents and tone curves
- auto-exposure: face-priority metering pulls faces toward mid-grey, which compresses L* differences between light and dark skin
- makeup, flash and retouching
- colour-profile handling: Adobe RGB or Display P3 images read as sRGB lose saturation
- for CelebAMask-HQ, the neural JPEG-artifact-removal and 4× super-resolution networks used to build CelebA-HQ **[external, from memory: Karras et al. 2018]**

The paper's own figures show these effects are as large as, or larger than, the between-group signal:
- **Fig. S1:** single CelebAMask-HQ images span h* from −25.4 to 45.4 because of cast, low light, makeup and flushing.
- **Fig. S4:** a global contrast change moves h* by 42° (55.96 to 14.05). A9 traces this to clipping plus the arctan artefact; either way it shows extreme sensitivity to tone-curve processing.
- **CFD versus web datasets (Fig. S5a against Fig. 2 and Fig. S6).** Under controlled capture, the 739 CFD faces from five self-reported ethnic groups span roughly 40–72° of h*. Visibly most of them sit above the 55° "yellow" line, and CFD's White subjects scatter on both sides of 55. In CelebAMask-HQ and FFHQ, the hue histograms peak near 45–50° and span about 0–85°.

So under uncontrolled capture, the spread across images is more than twice the spread across five ethnic groups under controlled capture, and the centre is shifted by roughly 8–12° (read off the figures). The shift is in the direction that produces the "red skew". Those numbers come from the paper's own figures; reading them as evidence that capture variance outweighs between-group variance is my inference.

**Consequence.**
- **(a)** The image groups labelled "red" and "yellow" in the model analyses (Fig. 3, Table 3) may partly index warm versus cool lighting, white balance, makeup or photographic style, all of which can affect models independently of skin.
- **(b)** The dataset "red skew" may be a property of how web portraits are photographed and processed (A4).
- **(c)** Cross-dataset comparisons (CFD against CelebA/FFHQ; FFHQ against generated images) mix capture regimes.

**Fix.**
- Quantify the variance in scores due to capture: within-identity spread (A2), and the spread of neutral references in the same image.
- Add a colour-constancy or white-balance normalisation arm (gray-world/edge-based, or sclera/teeth-referenced) and report how Tables 1–2 and Figs. 3/Table 3 change.
- Measure the hue of non-skin regions (background, hair, clothing) as a proxy for colour cast, and adjust for it or stratify by it.
- Report the dataset pipelines: colour-profile handling and resampling.

**Severity: Major.** It materially weakens every hue-based claim. Fixing it needs substantial reanalysis.
**Confidence: 4.** The camera-pipeline effects are well established. Their magnitude in these specific datasets is inferred from the paper's figures.

---

### A4. The "dataset skew" claims (Tables 1–2) have no reference distribution, so the hue skew mostly reflects where the cutpoint sits
**Quoted text**
- p4–5: "both datasets are skewed towards light skins. This paper enables to quantify such skin color bias. Measuring the hue angle further shows that both datasets are also skewed towards red skins."
- Table 1 caption (p5): "Images are skewed towards a light skin tone and a red skin hue while dark and yellow skin colors are underrepresented."
- p15: "distributions are unimodal with a bell curve shape. Individuals with a light skin tone and a red skin hue are over-represented with a much larger count."

**Problem.** "Skewed" and "under-represented" are comparative terms that need a reference distribution: a target population, a deployment population, or a balanced design over meaningful categories. The paper gives none. The implied reference is a 50/50 split at cutpoints imported from in-vivo colorimetry (A5). Fig. S6 shows both datasets' h* distributions are unimodal, with the mode below 55°. So the 66–82% "red" figure is mainly a statement about where 55° falls relative to the dataset median. A cutpoint at the median would report "balance", and one at 45° would report a "yellow skew".

The paper's own controlled-capture data cut the other way. On CFD (Fig. S5a), the same instrument puts most faces on the "yellow" side, including many of the White subjects (A3). So the measured "red skew" cannot be separated from capture conditions (A3) or from the arbitrary cutpoint (A5).

The light-tone skew has some independent support, from the literature and from the composition of the source datasets. The hue skew has none.

**Consequence.** Core claim (i) of the contributions ("skewed towards light-red ... under-represent dark-yellow") and the abstract's claim that hue "reveals additional biases ... in ... datasets" are not interpretable as stated. The generative-model results in Table 2 inherit the same problem: they show that the outputs match the training distribution, not that they reproduce a "bias".

**Fix.**
- Define the reference explicitly. Options:
  - a population distribution of constitutive colour from colorimetric surveys (this needs person-level validity, A1/A2)
  - the distribution of apparent colour in the intended deployment domain, measured with the same instrument
  - the CFD distribution as a controlled baseline
- Report divergence from that reference (KL or Wasserstein distance) with bootstrap CIs.
- Show the hue result is robust across a sweep of cutpoints, or replace the binary split with quantiles of the reference.
- Until then, restate the result descriptively: "the median apparent h* is X° (IQR ...)".

**Severity: Critical.** On its own, this leaves the dataset hue-skew claim, a headline contribution, uninterpretable. It reduces to cutpoint placement against the median.
**Confidence: 4**

---

### A5. The 60 / 55° thresholds come from in-vivo colorimetry and are applied to image-derived values in different units
**Quoted text**
- p4: "When L* is over 60, it corresponds to a light skin tone ... When h* is over 55°, it corresponds to a skin turning towards yellow ... Threshold values are taken from Ly et al. [46]."
- p5: "The different thresholds confirm the over-representation of light skin tones and red skin hues."

**Problem.** Ly et al. [46] review contact cutaneous colorimetry. In that setting, L* is computed from measured reflectance relative to a perfect diffuser, using instrument illuminant/observer conventions (often D65/10°), and specular reflection is typically excluded. Readings are taken at particular body sites in particular study populations. The manuscript does not state which population, body site, geometry or illuminant/observer the 60 and 55° values come from.

The image-derived quantities are not on the same scale:
- Image L* is relative to the display white (sRGB 255).
- It depends on exposure, tone curve and white balance.
- It includes specular reflection.
- It is computed as an upper-trimmed estimate (the top-3 of 5 clusters by L*, see A10), which pushes it upward relative to an average over the face.
- The code uses the 2° observer.

No calibration links the two scales. One example in the paper shows the gap. The Fig. S3 subject, whose face is visibly darker than the Fig. 4 row-1 subject, scores L*=66.63 ("light") in the original image. The light-skinned row-1 reconstruction scores 61.92.

Despite the p5 sentence, the paper never actually sweeps thresholds. Fig. S6 shows histograms coloured by the same binary split.

**Consequence.** The labels "light/dark" and "red/yellow" are cutpoints in uncalibrated instrument units. Every binary result inherits that arbitrariness: Tables 1–2, Fig. 3, Table 3, and the directions learned for Section 4.3. Both cutpoints sit within roughly 5–10 units of the dataset modes (Fig. S6), where small shifts move the most images.

**Fix.**
- State the provenance of the thresholds.
- Either calibrate image units to colorimetric units (paired photos and colorimetry, or colour-checker-referenced photos), or drop the claim that the cutpoints mean "light" or "yellow".
- Run a real threshold sweep (for example L* 50–70 and h* 45–65) for every binary result, or switch to continuous analyses.

**Severity: Major.** It materially weakens all the binary group results. Fixing it needs reanalysis, and calibration needs new data.
**Confidence: 4**

---

### A6. Dichotomisation at the cutpoints without propagating measurement error
**Quoted text**
- Table 1/2 (p5): percentages to two decimals, for example "46.95 19.28 66.23"
- p5: "we go beyond a simple binary thresholding for both L* and h*"

**Problem.** The paper splits continuous, noisy scores at cutpoints that sit close to the density modes. When there is measurement error, the share of images misclassified is largest exactly there. The only error evidence in the paper shows one face crossing the L*=60 line under relighting (Fig. S3: 59.41 against 66.63, see A7). If the error is differential (larger for low-chroma, underexposed or darker images: A9, A10), misclassification can manufacture or hide differences between intersectional cells such as dark-red versus dark-yellow (Fig. 3c, Table 3). Two-decimal percentages with no uncertainty imply a precision the instrument does not have.

**Consequence.** It weakens the precision and the intersectional contrasts. It may attenuate or distort group differences in the model analyses.

**Fix.**
- Use continuous regressions of the outcome on L* and h* (with an interaction term) in place of, or alongside, the 2×2 cells.
- Use probabilistic group membership from per-image score uncertainty, or exclude an uncertainty band around each cutpoint.
- Report CIs for the cell percentages.

**Severity: Minor.** The main damage is already counted in A4, A5 and A2. On its own this is a fixable analysis choice.
**Confidence: 4**

---

### A7. The Fig. S3 robustness test cannot test h*: the relighting method fixes chroma by construction, and "up to 6 points" understates the printed values
**Quoted text**
- Fig. S3 caption (p13): "the perceptual lightness L* varies by up to 6 points w.r.t. the original image. while the hue angle h* remains stable."
- p13: "Face relighting affects L*, which can differ from up to 6 points with respect to the original image. Interestingly, h* remains stable and robust to face relighting, which confirms that it provides complementary and orthogonal information about skin color than the skin tone."
- p13: "we rely on samples coming from the work of Zhou et al. [81] where a deep neural network produces different face relighting images"

**Problem.**
1. **The test is tautological for h*.** The figure matches the Deep Portrait Relighting (DPR) demo: one portrait, seven spherical-harmonic lights, shown as shaded spheres. **[External, from memory; confidence about 4.]** DPR converts the image to Lab, relights only the L channel, and copies the original a/b channels back before converting to RGB. So per-pixel a* and b*, and therefore hue, are held fixed by construction, apart from 8-bit and JPEG rounding and gamut clipping. The residual h* spread of 57.08–59.12° measures how much the top-3-by-L cluster selection shifts from one region of the face to another. It says nothing about h* robustness to illumination.
2. **The test leaves out the main threat to h*.** DPR models white light only. Changes in illuminant chromaticity and white balance, which drive h* in the wild (A3, Fig. S1a), are never tested.
3. **The printed numbers contradict the caption.**
   - The original L* is 66.63. The relit values run from 59.41 to 71.34.
   - The largest deviation is **7.22**, not "up to 6".
   - Across lightings the range is **11.93**, which is roughly comparable to one standard deviation of the between-image L* distribution in Fig. S6 (read by eye).
   - At 59.41, **the same person crosses the L*=60 light/dark cutpoint**.
4. **n = 1**, a single synthetic relighting model, and no statistics.
5. **The inference is invalid.** Stability of one variable while another changes does not show the two variables are "orthogonal" or "complementary" as measures of skin colour (see also A12). As a point in the authors' favour, CIELAB hue is in principle invariant to achromatic scaling of linear intensity in the cube-root region. **[My computation:** scaling linear RGB from L*=61 down to L*=33 leaves h exactly unchanged; drift appears only below L*≈15.**]** But that is a property of the colour space. It is not evidence about the instrument on real images.

**Consequence.**
- The paper's only robustness evidence for h* is void.
- The claim "h* remains stable and robust" is unsupported.
- The L* evidence actually shows the person-level instability of the light/dark label.

**Fix.**
- Test robustness with real multi-illuminant captures of the same subjects (for example light-stage or multi-illumination face datasets, or the same subjects photographed under different correlated colour temperatures (CCTs) and white-balance settings).
- Also use physically based relighting that changes illuminant colour.
- Report the per-subject SD of L* and h* across many subjects, and the label-flip rates at the cutpoints.
- Correct the caption to "up to 7.2 points (range 11.9)".
- State what DPR modifies.

**Severity: Major.** It invalidates the only robustness claim for h*. I stopped short of Critical because the headline results do not rest on S3 alone, but this reinforces A2.
**Confidence: 4.** The numbers are certain. The DPR mechanism is from memory.

---

### A8. The hue computation uses `arctan`, not `atan2`: quadrants are conflated, the jump sits at the yellow pole, and Eq. 2 contradicts the code
**Quoted text**
- p4: "h* = arctan (b*/a*) (2) where h* goes from 0 to 360° as a* and b* components are unbounded."
- p4: "we are mainly interested in angles between 0 and 90° (i.e., positive values of a* and b*)"

**Problem.** The code computes `degrees(arctan(b/(a+1e-8)))`, which has range (−90°, 90°). Compared with the CIE hue angle h_ab = atan2(b*, a*) on [0°, 360°):
- **Quadrant II** (a*<0, b*>0: greenish-yellow) maps to negative values. These are the *most yellow* pixels, and they are scored as "redder than red". **[My computation:** sRGB (255,255,200) gives a=−8.6, b=26.4, true h=108°, code value **−71.9°**. sRGB (140,150,120) gives true h=122°, code value −58°.**]**
- **Quadrant III** (a*<0, b*<0: bluish-cyan) maps into (0°, 90°), the *skin range*. **[My computation:** sRGB (120,130,140) gives a=−1.5, b=−6.6, true h=257° (blue), code value **77.3°**, so it is labelled "yellow".**]**
- **Quadrant IV** (magenta casts) maps to negative values. For these, the signed angle is actually equivalent to atan2's (−180°, 180°] convention, so it is benign.
- **The jump is at h=90°**, where a* crosses zero for b*>0. That is pure yellow, at the yellow end of the construct. As a* passes through zero, the hue jumps from +89° to −89°. With atan2 the jump would sit at 180° (green), far from skin.
- **Near-neutral pixels** get essentially arbitrary hues from floating-point residuals. **[My computation:** pure white and mid-grey give code h=−63° in my implementation.**]** Pixel-weighted averaging of cluster modes then combines values on either side of this jump linearly.

**A plausible artefact in the paper's own figure.** Raising contrast or gain on skin clips R and then G, which pushes pixels *toward yellow* (true h 97–108°). The code then reports them at about −72° to −83°. **[My computation:** skin (235,190,160) at 2× contrast gives true h=105.7°, code value −74.3°.**]** This matches Fig. S4:
- "+contrast" drops h* from 55.96 to 14.05, with L*=91.74, which is consistent with clipping.
- "−contrast", which does not clip, keeps h*=56.56.

With atan2, the +contrast face would read *more* yellow, not redder. The negative h* values in Fig. S1 show that pixels outside quadrant I occur in the dataset (A13).

**Consequence.**
- h* is wrong in direction for green-yellow and blue casts, and for clipped highlights (A10).
- The error is not random. It biases affected images toward "red", or for blue casts toward "yellow", which can feed the hue skew in A4 and corrupt group membership.
- Eq. 2 and the stated 0–360° range do not describe what was computed.

**Fix.**
- Use `atan2(b, a)`, and report hue on a declared circular range, for example (−180°, 180°].
- Gate on chroma (A9).
- Exclude clipped pixels (any channel ≥ 254 or ≤ 1).
- Recompute every table and figure, and report what fraction of pixels and images have a*≤0 or b*≤0.
- Correct Eq. 2 and its text.

**Severity: Major.** The bug is certain. Its effect on the aggregates is unknown but can go in either direction, and it is plainly visible in Fig. S4. Fixing it needs a full recomputation.
**Confidence: 5** that the bug exists and is mis-documented. **3** for the size of its effect on Tables 1–2.

---

### A9. Per-pixel hue is ill-conditioned at low chroma; there is no chroma gating, and chroma is dropped as a dimension
**Quoted text**
- p13: "We convert to the CIELAB space to extract the L* component, and further use the a* and b* components to compute the hue angle h*. This results in a point measurement of L* and h* for every skin pixel in the image."
- p4: "We take inspiration from de Rigal et al. [17], and focus on the measurement of L* for skin tone and h* for skin hue."

**Problem.** Hue is undefined at chroma C*=0, and its error grows roughly as σ_ab/C*. **[My computation:** with per-pixel noise σ_ab=1, hue SD is 2.9° at C*=20, 5.8° at C*=10, 13° at C*=5 and 33° at C*=3. With σ_ab=2, it is 13° at C*=10 and 39° at C*=5, and 9–27% of pixels wrap past the arctan jump at C*≤5.**]**

Several conditions push skin pixels to low chroma and high chroma noise:
- low light (Fig. S1c: L*=18.9, h*=−14.7)
- grey or cool casts
- specular highlights
- underexposed darker skin in mixed scenes
- JPEG 4:2:0 chroma subsampling and quantisation, which is spatially correlated and so barely reduced by a Gaussian blur with σ=1

The pipeline computes per-pixel hue and then takes histogram modes. That differs from colorimetric practice, where a* and b* are measured over an aperture and h is computed from the aggregated values. Hue computed from the mean (or median) a*, b* is well-conditioned. A mode of per-pixel hue is not.

Chroma C* is also left out of the "multidimensional" measure, although Weatherall & Coombs [75], whom the paper credits with proposing the hue angle for skin, used the full L*C*h* description. Without C*, an almost grey face and a saturated one with the same h* are treated as equal, and no reliability flag is possible.

**Consequence.** h* precision varies with capture conditions and, through exposure, plausibly with skin tone. That produces differential misclassification in the intersectional hue analyses (Fig. 3c, Table 3) and in the "dark-yellow" cells of Tables 1–2.

**Fix.**
- Compute h from the aggregated (trimmed-mean or median) a*, b* of the selected skin pixels.
- Exclude pixels with C* below a threshold, for example 5–8.
- Report C* as a third coordinate.
- Flag images with low median C*, and run sensitivity analyses that exclude them.

**Severity: Major.** It produces unquantified, plausibly differential error in the hue groups. Fixing it means recomputing everything.
**Confidence: 4**

---

### A10. The cluster-and-top-3 estimator: unstandardised features, K=5/top-3 justified by an art book, no ablation, and a likely skin-tone-dependent bias
**Quoted text**
- p13: "We cluster the face skin into five groups and keep the top-3 groups with the highest L* to compute the final L* and h* scalar scores for the image. Such approach is inspired by how human artists would perform value grouping in five different groups when simplifying an image [57]."
- p13: "Moreover, clustering can identify shaded areas of the face or facial hair, which we remove to avoid contaminating the final skin color scores."

**Problem.**
1. **Feature scaling is arbitrary.** K-means runs on raw [L*, hue°], so one lightness unit counts the same as one degree of hue. Which feature dominates the clustering depends on the image. In noisy or low-chroma images, hue variance (up to ±90°, A8/A9) dominates. The clusters then split mainly on hue, and "drop the 2 lowest-L* clusters" no longer removes shadows or beard as the paper claims. Euclidean distance in (L, h) also has no colorimetric meaning, whereas (L*, a*, b*) is the space designed for Euclidean colour difference.
2. **The justification is not methodological.** K=5 and top-3 are justified by a painting book [57]. There is no ablation over K, the number of clusters kept, or feature scaling, and no check that the dropped clusters are actually shadows or hair.
3. **Bright-pixel selection keeps specular highlights.** Highlights are bright, low-chroma pixels coloured by the illuminant (dichromatic reflection), and nothing removes them. Fresnel surface reflectance is similar across skin types while diffuse reflectance is much lower for darker skin. So highlights make up a larger share of the brightest clusters on darker faces, and push L* up and h* toward the illuminant, or toward noise. That is a skin-tone-dependent error.
4. **Upper trimming scales with lightness.** Multiplicative shading k changes L* by about (L*+16)(k^{1/3}−1), so for the same lighting, lighter faces spread more in absolute L*. Taking the upper clusters therefore inflates L* more for lighter faces, stretching the scale between tone groups, and moves it further from in-vivo units (A5).
5. **Selection instability is already visible.** The 2° h* spread in Fig. S3 (A7) is attributable to which clusters are selected.

**Consequence.** The location estimator's bias depends on skin tone, lighting contrast and chroma noise, in unknown amounts. The binary group assignments and the cross-dataset comparisons inherit those biases.

**Fix.**
- Cluster on standardised features, or in (L*, a*, b*), or on L* alone for shadow exclusion.
- Remove highlights explicitly (clipped or high-L*/low-C* pixels).
- Ablate K, the number of clusters kept, and the scaling, and report how Tables 1–2 and the group labels change. Report the label-flip rate.
- Validate cluster removal against annotated shadow and beard regions.
- Compare with simple robust baselines, such as the median a*, b*, L* over masked skin.

**Severity: Major.** The estimator's design choices are untested and their bias may depend on skin tone, which matters for a fairness instrument. Settling it needs systematic reanalysis.
**Confidence: 3.** The mechanisms are sound. Their size in these data is unmeasured.

---

### A11. The histogram-mode estimator: the code takes the left bin edge, and Sturges bins depend on range and resolution
**Quoted text**
- p13: "For every cluster, we compute a histogram of distribution and set the number of bins with the Sturges formula [66]. The mode of the histogram is then used to assign a scalar value for each considered skin color score."
- p13: "we average the scalar values of every group normalized by their pixel size."

**Problem.**
- **Downward bias.** The code returns the *left edge* of the modal bin, not the bin centre or a density mode. That biases each estimate downward by roughly half a bin width, toward "dark" and "red".
- **Range-dependent bin width.** Sturges' rule fixes the bin count at ⌈log₂n⌉+1, so the bin width is the cluster's range divided by about 12–17. The width, and therefore the bias, depends on the most extreme pixel in the cluster's Voronoi cell, and on how many pixels there are, which depends on image resolution and face size.
- **Simulation.** **[My computation, histogram stage only, without clustering:** with a Gaussian hue cluster of SD 4–8° and n=2,000–20,000, the bias is −1.0° to −2.0°. When 0.5–2% of pixels are spread across ±90°, the bin width grows to about 11–14° and the bias reaches about −6° to −8°. Clustering bounds each cluster's range, so the effective outlier range is smaller in the real pipeline.**]**
- **Mixed-up coordinates.** Modes of L* and h* are taken separately from their marginals, so the final (L*, h*) pair need not correspond to any actual pixel colour.
- **Linear averaging of angles** is unsafe given the arctan jump (A8).
- **Paper–code mismatch.** Several choices are not in the paper: "mode" versus left edge, the Gaussian σ=1 pre-smoothing, the raw unstandardised features, and K-means' fixed random_state.

**Consequence.** There is a small, systematic and image-dependent bias toward "dark" and "red", which compounds A4. The results also depend on resolution across datasets (A15).

**Fix.**
- Use bin centres, or better a kernel-density mode or a robust location estimate (median or Hodges–Lehmann).
- Use fixed-width bins in colour units, not a bin count from Sturges' rule.
- Average angles circularly, or average a*, b* (A9).
- Document every implementation choice.

**Severity: Minor.** Bias of 1–2 units in clean cases. It does not on its own overturn any claim.
**Confidence: 4** for the mechanism. **3** for the size of the effect.

---

### A12. The "orthogonal" and "independent" claims for L* and h* are overstated or circular
**Quoted text**
- p8: "Modifying the image in one direction does not affect the skin color score in the other direction, making them orthogonal."
- Fig. 4 caption (p7): "our proposal (c-f) is better for measuring the multidimensional causal effect of skin color as we have an independent control over L* and h*."
- p13: "which confirms that it provides complementary and orthogonal information about skin color than the skin tone"
- p7: "we first train a classifier on CelebAMask-HQ [43] to predict the skin tone (light vs. dark) and skin hue (red vs. yellow)."

**Problem.** "Orthogonal" is used in three different senses, and none of them is established:
- **(a) Separate coordinates.** L* and h_ab are separate coordinates of CIELAB's cylindrical LCh form. That is true by definition and is not an empirical finding.
- **(b) Statistical independence across people or images.** This is never reported: there is no correlation and no mutual-information estimate. The in-vivo literature and the paper's own CFD figure (Fig. S5: Black subjects "darker and more yellow") suggest L* and h* are correlated in populations. The Fig. 2 scatter is visibly not a product distribution.
- **(c) Disentangled manipulation.** The claim rests on three images in Fig. 4, and the printed values partly contradict it:
  - The tone directions keep |Δh| ≤ 3.5° (row 2 +dark: 70.19 to 73.71).
  - The hue directions change L* by up to **+7.62** (row 2 +red: 44.43 to 52.05). That is more than half the size of the +light effect in the same row (+14.30), and larger than the +light effect in row 3 (+5.28).
  - The "pale" comparison is not a clear contrast either: −pale moves row-2 h* by −8.6°, against −12.9° for +red.
- **Circularity.** The directions are learned from labels produced by the instrument's own cutpoints and then checked with the same instrument.
- **Global colour.** Given A3, a "hue" direction learned from apparent h* in web images may partly encode global white balance or illuminant colour, not skin. The paper does not measure the colour of non-skin regions. By eye, at the rendered resolution, I cannot tell either way.

Aggregate ΔL* and Δh* over all 4×30,000 manipulated images were available to the authors but are not reported. They did report an aggregate RMS-contrast diagnostic.

**Consequence.**
- The causal attributions in Table 4 assume the hue and tone directions are separable and specific to skin: "redder → more smiley", "lighter → more feminine". With up to 7.6 L* units of cross-talk, part of the hue effect may be a lightness effect, or a global colour-cast effect.
- The S3 "orthogonality" inference is invalid (A7).

**Fix.**
- Report the mean and SD of ΔL* and Δh* for each direction over all manipulated images.
- Report Δ(non-skin colour) (background, hair, sclera) to check that the edits are specific to skin.
- Report the Spearman correlation and mutual information between L* and h* in each dataset.
- Replace "orthogonal" with what was actually measured.
- Consider directions that are explicitly orthogonalised against the other attribute and against global white balance.

**Severity: Major.** It materially weakens the independent-control premise of the causal benchmark. Needs reanalysis.
**Confidence: 4**

---

### A13. Negative h* values in Fig. S1 contradict the definition and the axes of Fig. 2 and Fig. S6
**Quoted text**
- Fig. S1 (p12): "L*=37.10 h*=−25.38 (a) Color cast", "L*=18.93 h*=−14.70 (c) Low-light", "L*=46.40 h*=−0.70 (d) Makeup", "L*=81.29 h*=−4.22 (e) Face flushing"
- p4: "h* goes from 0 to 360°"

**Problem.**
- **Contradiction with the definition.** Four of the five illustrated CelebAMask-HQ images have negative h*, which Eq. 2 says cannot happen. The values come from the arctan implementation (A8).
- **Contradiction with the figures.** The Fig. 2 scatter axes and the Fig. S6 hue histograms appear to start at about 0°. With matplotlib's default margins, a minimum of −25 would show as an axis extending to about −30.
- **Unanswered questions.** It is unclear whether images with negative h* were excluded, clipped, or counted as "red" in Table 1, and whether Fig. S1 used a different version of the pipeline.
- **Ambiguous meaning.** A negative value is ambiguous in meaning: it could be a magenta cast (quadrant IV) or a green-yellow cast (quadrant II), which are opposite meanings.

**Consequence.** The handling of these images is undocumented and may shift the "red" share in Tables 1–2. It is also a visible internal inconsistency.

**Fix.**
- Report how many images have h* < 0 or h* > 90 in each dataset, and how they were handled.
- Make the figure axes match the data.
- Recompute with atan2 (A8).

**Severity: Minor.** It is a consistency and reporting gap. The substantive issue is A8.
**Confidence: 4.** I read the axis limits by eye from the rendered figures.

---

### A14. Masks: FFHQ-Aging's "ground truth" masks are model predictions, and the mask source is unreported for the generated and LFW images
**Quoted text**
- p4: "Both datasets provide ground truth segmentation masks of the skin, which we use to extract skin color scores."
- p5: "We extract the skin masks with DeepLabV3 [11], trained on CelebAMask-HQ [43] as done in FFHQ-Ageing [52]."

**Problem.**
- **"Ground truth" is a misdescription.** The second sentence implies that FFHQ-Aging's masks were themselves produced by DeepLabV3 trained on CelebAMask-HQ, which matches my recollection. **[External, from memory.]** So they are model predictions, not ground truth.
- **Unreported mask sources.** The paper does not say how masks were obtained for the 2×10,000 generated images (Table 2) or for LFW (Table 3).
- **Possible tone-dependent segmentation error.** The segmentation model was trained on a dataset the paper itself shows to be predominantly light-skinned (Table 1a). There is no breakdown of segmentation quality by skin group, so errors that differ by group cannot be ruled out: missed skin, or included beard, hairline or shadow.
- **Boundary bleed from smoothing.** The code applies a Gaussian blur with σ=1 to the whole image *before* masking. Boundary skin pixels therefore mix with lips (red), brows and hair (dark) and background. That pushes h* toward red at lip borders, and its weight grows as image resolution falls.

**Consequence.** It adds instrument noise that may differ by group. Cross-dataset comparisons may mix mask sources: CelebA uses human masks, while FFHQ, CFD, the generated images and LFW use predicted ones.

**Fix.**
- Describe FFHQ-Aging's masks accurately.
- State the mask source for every dataset.
- Report segmentation IoU by tone and hue group on CelebAMask-HQ held-out data.
- Erode the masks, or apply the mask before smoothing.
- Check how sensitive the scores are to the mask source by scoring CelebAMask-HQ with both ground-truth and DeepLabV3 masks.

**Severity: Minor.** Mostly accuracy and reporting. The likely effect is modest for high-resolution frontal images.
**Confidence: 3**

---

### A15. The instrument is applied to the low-resolution scikit-learn LFW crops, and how a pair is assigned to a group is undefined
**Quoted text**
- p6: "We rely on the pre-processed version of LFW available in scikit-learn [54]"

**Problem.**
- **Tiny, possibly greyscale crops.** By default, scikit-learn's `fetch_lfw_pairs` returns tight central crops downsampled to about 62×47 pixels, in greyscale unless `color=True`. **[External, from memory.]**
- **Few skin pixels.** Applied to roughly a thousand skin pixels from heavily JPEG-compressed news photos, five clusters, Sturges bins (about 10–11) and per-pixel hue (A9) become much noisier.
- **Domain shift for the mask model.** The DeepLabV3 model was trained on 512-pixel full-head images.
- **Undefined pair assignment.** The paper never says how a *pair* is assigned to a skin group. Negative pairs contain two different people who may fall in different groups.

**Consequence.** The Table 3 group labels may be unreliable. With subgroup accuracy differences of about 0.3–1.1 points, label noise matters.

**Fix.**
- State the resolution, colour setting and mask source.
- Score faces at native 250×250 resolution.
- Define the pair-to-group rule (for example, require both images in the same group), and report the reliability of the labels across each identity's images (A2).

**Severity: Minor.** It affects one experiment's labels. The main concern sits with another scanner's perspective.
**Confidence: 3**

---

### A16. Recommending that datasets be balanced on apparent L*/h* invites balancing on lighting rather than on people
**Quoted text**
- p5: "In future dataset collections, we recommend tracking both skin tone and skin hue for skin color scores, such that all subgroups are well balanced, which in turn makes the dataset more diverse."
- p9: "we recommend the usage of a multidimensional skin color measure as a fairness tool to assess the computer vision pipeline, from data collection to model deployment."

**Problem.** The instrument measures apparent colour, which depends heavily on capture conditions (A3, A7). Balancing a collection on it can therefore be satisfied by changing exposure, white balance, lighting colour or filters, without adding any demographic diversity. A set of only light-skinned subjects shot under warm and cool, bright and dim conditions can fill all four cells. A balancing procedure could even select for extreme casts and underexposure to fill "dark-yellow" cells. This is Goodhart's law applied to an unvalidated proxy.

The cutpoints themselves are arbitrary (A5), so "well balanced" would mean balanced on uncalibrated half-planes. The claim "which in turn makes the dataset more diverse" does not follow, because diversity of apparent colour is not diversity of people.

**Consequence.** The paper's main practical recommendation could produce datasets that look balanced but are not, and so create false assurance in fairness audits.

**Fix.**
- Recommend tracking apparent colour *together with* capture covariates and person-level attributes (self-reported or colorimetric), with an explicit warning against balancing on apparent colour alone.
- Balance on person-level measures, and use apparent colour as an audit dimension for test-time robustness.
- Report what the recommendation does under simulated capture variation.

**Severity: Major.** It materially weakens a headline recommendation in the abstract and Conclusion. A safe version needs person-level validation (A2).
**Confidence: 4**

---

### A17. Colorimetric inaccuracies and reifying labels ("red/yellow", "L*=50 is max chroma", 0–360° range)
**Quoted text**
- p3: "where a perceptual lightness at value 50 corresponds to a maximum chroma"
- p4: "h* goes from 0 to 360° as a* and b* components are unbounded"
- p1 (Abstract): "we introduce the hue angle ranging from red to yellow"
- p14: "Asian subjects, which are mostly in the yellow side of skin hue"

**Problem.**
- **Maximum chroma.** Maximum chroma does not occur at L*=50 in general. It depends on hue and gamut: sRGB yellows peak near L*≈97 and reds near L*≈54. The 50 in ITA is a convention.
- **The 0–360° range** follows from h being an angle, not from a* and b* being unbounded.
- **The "red" and "yellow" labels.** In CIELAB, h_ab=0° is the +a* axis (magenta-red), and unique red sits at roughly 20–25°. Skin hues of about 40–70° are perceptually orange throughout. So "red" and "yellow" are names for two halves of a narrow orange band, and they are easily misread as perceptual categories.
- **Racialised wording.** Applying "yellow" to Asian subjects (p14) echoes a racialised slur. In a fairness paper this deserves neutral wording, such as "higher/lower hue angle".
- **Notation.** CIE notation is h_ab, not h*.

**Consequence.** These are about accuracy and communication. They contribute to the reification described in A1.

**Fix.**
- Correct the statements.
- Use "lower/higher hue angle" (or "more reddish/more yellowish") as relative descriptors.
- Report h_ab with its colour-space conventions.

**Severity: Minor.** Clarity and accuracy only.
**Confidence: 4**

---

### A18. Generality claims ("any camera", "any face pose") are not tested
**Quoted text**
- p4: "generalize their method to handle any scalar scoring value, any face pose and facial variation"
- p13: "This better deals with atypical facial poses, as clustering can handle faces that are unaligned or from the side"
- p12–13: "images acquired from any camera, with varying acquisition parameters or lighting conditions"

**Problem.** The paper offers no experiment on pose, camera or acquisition variation. Its only robustness test is one frontal face under white-light relighting (A7). Profile faces change the visible skin area and the shading geometry, so the top-3 selection keeps different regions.

**Consequence.** The claims overstate the evidence. They are not load-bearing for the headline results.

**Fix.** Either test on multi-pose and multi-camera captures of the same identities (for example the yaw-binned data in Multi-PIE), or soften the wording to "does not require landmarks".

**Severity: Minor.**
**Confidence: 4**

---

## Strengths of the measurement approach (with anchors)

1. **The paper states its construct and limits openly.** It explicitly separates apparent from true or constitutive colour (p2). It also discusses and shows external factors (A.1, Fig. S1). Many fairness papers leave this implicit. The problem (A1) is staying consistent with the distinction, not stating it.
2. **It uses standard, interpretable colorimetric quantities.** L* and h_ab are the cylindrical (LCh) coordinates of CIELAB, with a long history in skin colorimetry ([75], [17]). Choosing L* plus h* over ITA, which mixes L* and b*, is principled (p4). For sRGB-encoded content, the sRGB→CIELAB transform with a D65 white (skimage defaults) is the correct nominal conversion, and it is a defensible operationalisation of "colour as displayed".
3. **Hue has real potential to resist exposure changes.** CIELAB h_ab is invariant to achromatic scaling of linear intensity in the cube-root region. **[My computation:** h is unchanged from L*=61 to L*=33 and drifts only below L*≈15.**]** So h* can in principle complement L* when exposure varies. The paper does not state this argument and its S3 test does not demonstrate it (A7), but the design choice is sound.
4. **It is continuous, automatic and open.** The measure is continuous and annotation-free, so it avoids rater-dependence (p3), and the code is released (p4). The measurement is therefore reproducible and open to the audits proposed above.
5. **The aggregation intent is reasonable.** Excluding shadows and facial hair, and avoiding landmarks so non-frontal faces can be handled, are sensible goals (p13), even though the implementation needs work (A10).
6. **It shows some distributional transparency.** It shows full 2D scatters (Fig. 2, Fig. S5) and per-dimension histograms (Fig. S6), not only the 2×2 tables. That lets readers see the cutpoint-placement issue for themselves (A4).
7. **The controlled-capture analysis gives weak convergent evidence.** On CFD (Fig. S5b), self-reported groups separate in ways qualitatively consistent with the in-vivo literature the paper cites ([17]: Asian skin more yellow). That is modest evidence that h* carries person-related signal when capture is controlled.
8. **It compares manipulations against reconstructions.** Section 4.3 compares manipulated images with reconstructions rather than originals, and reports side-effects on contrast (Fig. S4 and the RMS contrast analysis). Those are good diagnostic habits that could be extended to ΔL*, Δh* and the colour of non-skin regions (A12).

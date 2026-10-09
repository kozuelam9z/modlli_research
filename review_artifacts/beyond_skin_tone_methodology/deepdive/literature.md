# Literature and provenance check: Thong, Joniak & Xiang, "Beyond Skin Tone" (ICCV 2023, arXiv 2309.05148)

Checked 2026-10-08. Read-only web checks; nothing logged into. All web content was treated as data. Paper text comes from arXiv HTML v2 (https://arxiv.org/html/2309.05148v2). The CVF PDF returned 403.

| Q | Topic | Verdict |
|---|---|---|
| Q1 | L*=60 / h*=55° thresholds "taken from Ly et al. [46]" | **NOT VERIFIED** (likely misattribution; 55° matches an ITA class boundary, not a hue cut-off) |
| Q2 | DPR relights only L of Lab and keeps a/b | **VERIFIED** (repository code), so the paper's hue-robustness check is close to circular |
| Q3 | sklearn `fetch_lfw_pairs` defaults; test = 1000 pairs (500/500) | **VERIFIED**, but the authors' code overrides the defaults (`color=True, resize=1`) |
| Q4 | Follow-up literature on validity/reliability | Summarised below. No independent validation of image-derived h* against instruments found; several papers report illumination/device sensitivity |
| Q5 | Sony patent | **VERIFIED**: granted US 12,675,913 B2 (7 Jul 2026) |
| Q6 | CFD-INDIA uses the same protocol as CFD | **PARTLY VERIFIED** ("followed closely", same output size and white background). Same camera/lighting **NOT VERIFIED**. Documented manual skin-tone colour corrections in CFD-INDIA |
| Q7 | InterFaceGAN conditional manipulation; e4e+StyleGAN3 entanglement | Mechanism **VERIFIED**. Thong et al. do **not** use it (no projection described), and InterFaceGAN says the trick fails in StyleGAN W space. Entanglement evidence is indirect |
| Q8 | Venue / open reviews | **VERIFIED** ICCV 2023 main conference. No public ICCV reviews, but an earlier version has **public NeurIPS 2022 D&B OpenReview reviews** |

---

## Q1. Threshold provenance (L* = 60, h* = 55°)

**What the paper says.** Section 4.1 says L* over 60 means light and h* over 55° means "turning towards yellow". It ends with: "Threshold values are taken from Ly et al. [46]." Ref [46] is Ly, Dyer, Feig, Chien, Del Bino, *J Invest Dermatol* 140(1):3–12, 2020 (https://arxiv.org/html/2309.05148v2). The code README restates both cut-offs with no derivation (https://github.com/SonyResearch/apparent_skincolor).

**Access to Ly et al.**
- Europe PMC: PMID 31864431, not in PMC, "subscription required" (https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1016/j.jid.2019.11.003&format=json&resultType=core).
- Unpaywall/Semantic Scholar mark it BRONZE (free on the publisher site). However, jidonline.org and sciencedirect.com returned 403 or a bot-verification page, which I did not try to get past.
- **I could not read the full text, so I cannot say what numbers Ly et al. actually print.**

**Circumstantial evidence**
1. The numeric skin-colour cut-offs that secondary sources attribute to Ly et al. (together with Chardon 1991, Del Bino 2006, and Del Bino & Bernerd 2013) are the **ITA classes**: very light >55°, light 41–55°, intermediate 28–41°, tan 10–28°, brown −30–10°, dark ≤−30° (skinoptics docs: https://skinoptics.readthedocs.io/en/latest/07_colors.html).
   - ITA is computed from L* and b*, not from hue. So "55°" is an angle on the L*–b* plane.
   - **The 55° value matches the ITA very-light/light boundary. No source I found gives a 55° hue-angle cut-off.**
2. No source I found attributes an L* = 60 cut-off to Ly et al.
   - Downstream papers attribute "L≤60 and h≤55" to Thong et al. themselves, e.g. Fairness-Aware Grouping, ECAI 2025 (https://arxiv.org/html/2507.11247).
   - Other works use different L* cut-offs, e.g. TrustSkin uses 37/67 (https://arxiv.org/html/2505.20637).
3. In the NeurIPS 2022 rebuttal (see Q8), the authors justify *choosing* L* and h* ("well-documented and commonly used"). As far as I could read, they do not justify the numeric cut-offs.

**Typical measured skin hue angles (instrument data)**

| Source | Hue angle (h_ab) finding | Notes |
|---|---|---|
| Wang, Luo, Wang, Xiao, Pointer 2017, *Color Res Appl* 42:764 (accepted MS, https://eprints.whiterose.ac.uk/id/eprint/116965/) | Face averages about 56°, limbs about 70°. Female forehead 58.5°, cheeks 53–56° | Group means (Table 4) depend strongly on measurement geometry. TSR: Caucasian 60.0, Chinese 61.6, South Asian 59.2, Dark 51.0. d:8°: 62.0 / 64.7 / 61.8 / 56.1. 45°:0°: about 77–78° |
| Cook et al. 2024, arXiv 2410.21005 (calibrated colorimeter on faces) | Hue range across their population "about 45 degrees" | Lower (pinker) hue affected ratings much like higher L* |
| Everett et al. 2012, *Clin Nurs Res* (PMC3465481) | From Table 1 a*/b* means (my calculation): forearm/upper arm Asian 66/65°, Black 65/64°, White 68/66° | Arm sites, not face |

What this means for the measure (my synthesis, not a claim from any source):
- **h* = 55° sits near the centre of the facial hue distribution.** It works as a median split rather than an established physiological "red vs yellow" boundary.
- Measured hue moves by about 5–15° with body site and instrument geometry.
- In instrument data the darkest group has the **lowest** (redder) mean hue. Thong et al. report Black subjects in CFD as "darker and more yellow", which is worth flagging as a possible image-pipeline effect.

**Not accessed:** de Rigal et al. 2007, Del Bino & Bernerd 2013 (*Br J Dermatol* 169 Suppl 3:33–40), and Weatherall & Coombs 1992 (*J Invest Dermatol*). I found no open full text, so I make no claims about their exact hue values.

## Q2. DPR (Zhou, Hadap, Sunkavalli, Jacobs, ICCV 2019): L-only relighting

**Repository code** (https://raw.githubusercontent.com/zhhoper/DPR/master/testNetwork_demo_512.py):
- `Lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)` → `inputL = Lab[:,:,0]` → network → `Lab[:,:,0] = outputImg` → `cv2.COLOR_LAB2BGR`.
- Only the L channel is replaced. The a/b channels are carried through unchanged.

**Paper text:** the CVF PDF returned 403, and the abstract does not mention Lab. A secondary source supports L-only input: the IPOL reproduction by Bammey 2022 (https://www.ipol.im/pub/art/2022/429/) says the network takes the luminance of a colour photo.

**Implication for Thong et al., Appendix A.2:**
- The paper says L* shifts "up to 6 points" while h* "remains stable and robust to face relighting".
- With DPR, per-pixel a*/b* are unchanged by construction. The only h* changes can come from 8-bit/gamut clipping on Lab→BGR and from the K-means/top-3-L* clusters picking different pixels.
- **So the "hue is robust to illumination" evidence is close to tautological. It does not test real illuminant-colour or camera white-balance changes.**
- Figure S3 values as rendered in arXiv HTML: L* runs 59.41–71.34 against an original of 66.63. 66.63 − 59.41 = 7.2, which is slightly more than the "up to 6" stated in the text. h* runs 57.08–59.12.
- In the NeurIPS 2022 rebuttal the authors concede that the hue "can be influenced by an external color cast" (see Q8).

## Q3. scikit-learn `fetch_lfw_pairs`

**Defaults** (https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_lfw_pairs.html; source https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/_lfw.py):
- `subset='train'`, `funneled=True`, `resize=0.5`, `color=False`, `slice_=(slice(70,195), slice(78,172))`.
- The crop is 125×94. At resize 0.5 that gives **62×47**.
- Pixels are float32 scaled to [0,1]. With `color=False`, the channels are **averaged to grey** (`face.mean(axis=2)`). Docs example: `pairs.shape == (2200, 2, 62, 47)`.

**Test subset:**
- `'test'` maps to `pairsDevTest.txt`.
- LFW tech report (Huang et al.): the test set has 500 matched and 500 mismatched pairs, so **1000 pairs**. The training set has 1100 + 1100. (Read from the umass.edu PDF, https://people.cs.umass.edu/~elm/papers/lfw.pdf.)

**What the authors actually ran** (https://raw.githubusercontent.com/SonyResearch/apparent_skincolor/main/face-verification/lfw.py):
- They call `fetch_lfw_pairs(subset='test', color=True, resize=1)`. So the images are **RGB, 125×94, funneled, cropped to the default slice, floats in [0,1]**. They are not grayscale.
- The arrays go straight into `DeepFace.verify(...)` with no rescaling to 0–255 and no RGB→BGR swap.
- Unverified concern for the reviewer: DeepFace conventionally expects OpenCV-style BGR 0–255 input. Check whether this affects the reported accuracies.

**Reproducibility gap:**
- The repo has **no LFW skin-colour scores**. `extract/results` holds only CFD, CelebA and FFHQ (https://api.github.com/repos/SonyResearch/apparent_skincolor/git/trees/main?recursive=1).
- The paper does not say how skin was segmented on these 125×94 LFW crops.

## Q4. Follow-up literature (2023–2026) relevant to validity and reliability

Semantic Scholar lists 33 citing works (https://api.semanticscholar.org/graph/v1/paper/arXiv:2309.05148/citations). The relevant ones, in order of relevance:

### Reliability of image-derived colour

- **Cook, Howard, Rabbitt, Shuggi, Sirotin, Tipton, Vemury 2024** (arXiv 2410.21005; published 2025, *ACM J Responsible Computing*, doi 10.1145/3730409)
  - They measured faces with a calibrated colorimeter. They say colour in images can "vary substantially depending on the capture camera" and environment.
  - Human scale ratings were barely sensitive to hue: one FST/CST/MST step equalled about 52°/35°/32° of hue, against a population hue range of about 45°.
  - Rating consistency (ICC) varied by capture device.
  - They cite Thong et al. only for the idea that "some research has also considered skin hue".
- **Howard, Sirotin, Tipton, Vemury 2021**, *IEEE T-BIOM* 3(4) (arXiv 2106.11240) — background, pre-dates the paper
  - For the same subject, image-derived face lightness varied by "more than a 2-fold difference" across images.
  - Correlation with the colorimeter was ρ = 0.45 when only the environment was controlled, 0.78 with device and time controlled, and 0.92 with a single device plus grey-background correction.
  - Only L* was analysed; there is no hue/a*/b* analysis (https://ar5iv.arxiv.org/html/2106.11240).
  - **This directly limits uncalibrated in-the-wild L* (and, by extension, h*) estimates such as CelebA, FFHQ and LFW.**
- **Alipour, Burke, Courtney 2026**, "Limitations of ITA for Skin Type Estimation Under Uncontrolled Imaging Conditions", *Skin Res Technol* (doi 10.1111/srt.70374; PMC13459198)
  - Fixed-threshold ITA on 920 healthy-skin patches from PAD-UFES-20 reached 22.9% accuracy, against a 51.3% majority baseline.
  - They attribute errors to lighting. Their Table 1 lists Thong et al. as an "ITA & Hue angle" method that does **not** consider light variation and has no dermatologist-FST validation.
- **Fournier-Montgieux et al.**, "Fairness-Aware Grouping for Continuous Sensitive Variables", ECAI 2025 (arXiv 2507.11247)
  - They use Thong's 2D partition (L≤60, h≤55) as a baseline.
  - They state that pixel-based estimates "may be noisy as it depends on lightning conditions", and use a proprietary device-approximating estimator instead.
- **TrustSkin**, FG 2025 (arXiv 2505.20637)
  - They adopt L* + hue, citing Thong, because ITA is "sensitive to illumination".
  - They report no quantitative consistency test.
  - Aggregate disparity was actually lower with ITA (F1 gap 0.050 vs 0.080).
  - Their L* bins are 37/67, not 60.
- **Bernat, Bromberg, Sinefeld, Arad 2026**, "Unifying the spectrum…", *J Biomed Opt* 31(9) (PMC13621389)
  - Uses 15,256 spectral reflectances (ISSA). They treat CIE-h as undertone and note ITA ignores a* variation.
  - They cite Thong et al. as having evaluated undertone "on uncalibrated images 'in the wild'", contrasting this with spectral data.
- **Benčević et al. 2025/2026** (arXiv 2504.04494; arXiv 2602.10265), dermatoscopic images
  - Patch-based colour estimates show lighting-dependent bias.
  - Pixel averaging is substantially worse than colorimeter-supervised learning for ITA.
  - Hue was not evaluated.

### Applications and uses

- **FHIBE** (Xiang et al., *Nature* 2025, doi 10.1038/s41586-025-09716-2; PMC12675298)
  - Skin colour is **self-reported** (natural and apparent) on 6 Fitzpatrick-style levels (data card: https://fairnessbenchmark.ai.sony/data-card).
  - It cites Thong et al. only in passing, as ref 57.
  - **FHIBE does not use the image-derived L*/h* measure.**
- Wilson, Ghosh, Caliskan, AIES (arXiv 2508.17465)
  - Report SD-XL skin tones as 13.53% darker and 23.76% "less red", with perceptual colour metrics.
  - The method details were not checked.
- Kabbani et al., BIOSIG 2024; AI-Face (CVPR 2025); VariFace; PhysFlow (BMVC 2024); Fairness-is-in-the-Details (ECML-PKDD 2025)
  - These cite or use skin-tone grouping.
  - None that I checked validates h* against a ground truth.

### Pre-publication critique

The NeurIPS 2022 reviews (Q8) raised: no ground truth, no comparison with other skin metrics, only four groups, unclear cluster aggregation, and possible confounding by facial features.

**Not found:** any independent study that measures the *test–retest or cross-camera stability of image-derived h** against a colorimeter.

## Q5. Patent

**US 12,675,913 B2**, "Systems and methods for determining and using a multidimensional measure of apparent skin color". Read by OCR of the USPTO full-text PDF (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12675913).

Bibliographic data:
- Applicant/assignee: Sony Group Corporation.
- Inventors: William Eric Thong, Przemyslaw Kamil Joniak, Alice Xiang.
- Application 18/333,729, filed 13 Jun 2023. Provisional 63/366,981, filed 24 Jun 2022.
- Prior publication US 2023/0419549 A1 (28 Dec 2023).
- **Granted, date of patent 7 Jul 2026**, with 475 days of term adjustment and 18 claims.
- Prosecution per Google Patents (https://patents.google.com/patent/US20230419549A1/en): non-final action Nov 2025, notice of allowance 6 Mar 2026.

Independent claims:
- **Claim 1:** segment skin pixels → extract L*, a*, b* → cluster → histogram → scalar L* and h* per cluster from the histogram mode.
- **Claim 7:** dataset bias by counting images above or below a "first/second predetermined threshold" for L* and h*. **The claims give no numeric 60/55.**
- **Claim 13:** model bias based on L* and/or h*.

Dependent claims cover:
- 5 clusters with the top-3 by L* retained (claims 4, 9, 18).
- Sturges bins.
- A learned skin segmenter.
- Excluding clusters below a minimum L* (claims 3, 8, 17). This step is **not** in the released `predict.py`.
- GAN plus diffusion-generated images (claim 12).
- Face cropping (claim 14), face verification (claim 15), and attribute manipulation via changing tone/hue (claim 16).

The method is patented and the released code is Apache-2.0. The reviewer may want to disclose that.

## Q6. CFD vs CFD-INDIA capture protocol

**Original CFD** (Ma, Correll, Wittenbrink 2015, *Behav Res Methods* 47:1122; https://www.wittenbrink.org/research/pdf/mcw15.pdf):
- Subjects were seated at a fixed distance from a digital camera (model not named in the text extracted).
- "Participants sat in front of a white cloth backdrop." Three photo lamps: two on the front and one hair lamp.
- Raw images were 3008×2000. They were resized so a 796×435 template fit the core facial features, then cropped to **2444×1718**.
- Images were then "equated for color temperature" and placed on a plain white background.

**CFD-INDIA** (Lakshmi, Wittenbrink, Correll, Ma 2021, *Front Psychol* 12:627678; https://www.frontiersin.org/articles/10.3389/fpsyg.2021.627678/full):
- Recruited and photographed in Delhi. The setup "followed closely the procedures used for the existing CFD image set". Camera, lighting and backdrop are not specified.
- RAW files were corrected for uniform colour temperature and exposure "matching the existing CFD materials".
- **"Where necessary, additional corrections were made to reach a realistic skin tone."**
- Same 796×435 template. Exported as **2444×1718 JPEG** with an inserted white background.
- Grooming was not enforced. Religious and cultural markers were retained or produced in two versions.

**Bearing on the measure:** CFD and CFD-INDIA L*/h* reflect **post-processed** colour, after colour-temperature/exposure equalisation and, for India, manual skin-tone correction. Indian-vs-other comparisons in the paper therefore mix capture-site differences with editorial colour decisions.

## Q7. InterFaceGAN conditional manipulation; e4e + StyleGAN3

**Conditional manipulation (verified):**
- Shen et al. CVPR 2020 (https://ar5iv.labs.arxiv.org/html/1907.10786) project the primal normal as n1 − (n1ᵀn2)n2 so that editing attribute 1 leaves attribute 2 unchanged. With multiple conditions, the primal direction is projected onto the orthogonal complement.
- The code `project_boundary` does the same: "Projects the primal boundary onto condition boundaries." (https://raw.githubusercontent.com/genforce/interfacegan/master/utils/manipulator.py)

**Caveats from InterFaceGAN itself:**
- It assumes linear separability (SVM accuracy 75–90%) and supports decorrelation mostly with qualitative figures.
- For StyleGAN (Sec. 3.4): "This trick, however, cannot be applied to W space."

**What Thong et al. actually did:**
- Two linear SVMs (tone, hue), trained on classifier-labelled StyleGAN3 samples, with e4e inversion following Alaluf et al. The edited set is CelebAMask-HQ, 4×30k images.
- **The words "conditional" and "project" do not appear.** The repo ships only `lum_skin_boundary.npy` and `hue_skin_boundary.npy`, with no condition boundaries for other attributes.
- Orthogonality is claimed empirically from example images (Fig. 4), not enforced.
- They acknowledge the methods "struggle with spurious correlations". They also say this means attributes are not preserved, and that edits change global contrast (0.630/0.652 vs 0.644).

**Entanglement evidence (indirect):**
- Alaluf et al. 2022 (arXiv 2201.13433), the pipeline Thong follows: StyleGAN3 W/W+ "are more entangled than their StyleGAN2 counterparts".
- I found **no published study that specifically quantifies skin-tone/hue entanglement for e4e + StyleGAN3**. General GAN-editing surveys report that skin colour is entangled with race and hair attributes.

## Q8. Venue and peer review

**Venue:**
- ICCV 2023 main conference proceedings, pp. 4903–4913, doi 10.1109/ICCV51070.2023.00452 (https://mlanthology.org/iccv/2023/thong2023iccv-beyond/).
- The CVF open-access path is `content/ICCV2023/` (main), not workshops.
- The arXiv comment says "Accepted at the International Conference on Computer Vision (ICCV) 2023". v1 was posted 10 Sep 2023 and v2 on 3 Oct 2023.

**ICCV reviews:** ICCV 2023 reviewed through CMT with confidential reviews (https://iccv2023.thecvf.com/reviewer.guidelines-362000-2-16-20.php). I found no public ICCV reviews.

**Earlier public reviews:** an earlier version, **"More Than Skin-Deep: Towards a Multidimensional Measure of Skin Color"** by the same three authors, was submitted to **NeurIPS 2022 Datasets & Benchmarks**. It has public reviews on OpenReview at https://openreview.net/forum?id=iJAwfSj6i8L. I read it through the OpenReview search API; the forum page itself hit a bot challenge, which I did not bypass.

Reviews retrieved, with ratings and confidences:

| Reviewer | Rating | Confidence |
|---|---|---|
| zT3x | 6 | 4 |
| RqxP | 6 | 4 |
| YGai | 5 | 4 |
| t2qw | 6 | 2 |
| JoQS | 6 | 4 |

Not retrieved:
- The oUuH review text.
- The decision. Later publication at ICCV suggests it was not published at NeurIPS D&B 2022 (inference).
- The API search output may mix forum attributions for JoQS and YGai, so verify on the forum page.

Key reviewer points:
- Limited novelty: a combination of two known metrics.
- No ground truth and no comparison with other skin metrics.
- Only four groups.
- Unclear merging of clusters.
- Bias could come from facial features other than skin.
- The gender task is dubious.

Key author concessions:
- There is "no consensus at the moment on what constitutes a ground truth".
- Hue "can be influenced by an external color cast".

---

## Incidental code observations

Source: https://github.com/SonyResearch/apparent_skincolor, `extract/predict.py`, read via raw.githubusercontent.

- Hue is `np.degrees(np.arctan(b/(a+eps)))`, i.e. `arctan`, not `arctan2`. Values are folded into (−90°, 90°), which matters for colour-cast or low-chroma pixels; for example, Fig. S1 shows h* = −25.38.
- `mode = bins[hist.argmax()]` returns the **left edge** of the modal Sturges bin, a systematic downward bias of up to one bin width.
- `rgb2lab` uses the skimage default (D65). A Gaussian blur with σ=1 is applied before conversion. Clustering is KMeans with k=5, keeping the top 3 clusters by luminance, weighted by pixel count.
- There is no minimum-L* cluster filter, although the patent claims one.

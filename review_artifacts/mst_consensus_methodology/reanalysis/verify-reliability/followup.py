# Follow-up checks on points where the analyst's numbers/interpretation could hinge on a choice.
import json, itertools, math
from pathlib import Path
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

OUT = Path(__file__).resolve().parent
d = pd.read_csv(OUT.parent / "annotations_clean.csv"); d["y"] = d.mst_annot.astype(int)
R = {}
rng = np.random.default_rng(777)


def icc1(groups):  # list of arrays
    n = np.array([len(g) for g in groups]); s = np.array([g.sum() for g in groups]); q = np.array([(g ** 2).sum() for g in groups])
    N, a = n.sum(), len(n)
    msb = ((s ** 2 / n).sum() - s.sum() ** 2 / N) / (a - 1); msw = (q.sum() - (s ** 2 / n).sum()) / (N - a)
    k0 = (N - (n ** 2).sum() / N) / (a - 1)
    return (msb - msw) / (msb + (k0 - 1) * msw)


g = d.sort_values(["image", "pos_in_image"]).groupby("image")
img = pd.DataFrame({"vals": g.y.apply(lambda v: np.array(v)), "subject": g.subject.first(), "oracle": g.oracle.first(),
                    "light": g.lighting.first(), "golden": g.is_golden.first(), "chall": g.is_challenging.first()})
five = img[img.vals.apply(len) == 5]
X = np.stack(five.vals.values)

# 1. empirical 2-rater partitions: file order vs value-sorted order vs random order
def parts(M):
    out = []
    for A in itertools.combinations(range(5), 2):
        for Bc in itertools.combinations([i for i in range(5) if i not in A], 2):
            if A < Bc:
                out.append(icc1(list(np.column_stack([M[:, A].mean(1), M[:, Bc].mean(1)]))))
    return out
Xs = np.sort(X, 1); Xr = np.array([rng.permutation(r) for r in X])
for nm, M in [("file_order", X), ("value_sorted", Xs), ("random_order", Xr)]:
    p = parts(M); R[f"sb_emp2_{nm}"] = dict(mean=float(np.mean(p)), min=float(min(p)), max=float(max(p)))
print("partitions", {k: v for k, v in R.items()})

# 2. SB raters needed; challenging on 5-rating images only; several thresholds
sb_need = lambda rho, r: rho * (1 - r) / (r * (1 - rho))
sb = lambda k, r: k * r / (1 + (k - 1) * r)
r = {"all5": icc1(list(five.vals)), "golden": icc1(list(img.vals[img.golden])),
     "chall_all19": icc1(list(img.vals[img.chall])), "chall_5only18": icc1(list(five.vals[five.chall]))}
R["sb"] = {nm: dict(r1=v, **{f"need_{t}": sb_need(t, v) for t in (0.9, 0.95, 0.98)},
                    **{f"sb_k{k}": sb(k, v) for k in (1, 2, 3, 5, 10)}) for nm, v in r.items()}
# paper's lowest reported regional values, for context
R["sb"]["paper_low_chall_0.82"] = {f"sb_k{k}": sb(k, 0.82) for k in (5, 10)}
print(json.dumps(R["sb"], indent=0))

# 3. lighting effect within subject (fixed effect in the nested LMM; paired subject means)
dl = d[d.lighting.isin(["well_lit", "poorly_lit"])].copy(); dl["poor"] = (dl.lighting == "poorly_lit").astype(int)
fit = smf.mixedlm("y ~ poor", dl, groups="subject", re_formula="1", vc_formula={"image": "0 + C(image)"}).fit(reml=True)
pm = dl.groupby(["subject", "poor"]).y.mean().unstack()
diff = (pm[1] - pm[0]).values
bt = [rng.choice(diff, len(diff)).mean() for _ in range(2000)]
R["lighting"] = dict(lmm_poor_coef=float(fit.params["poor"]), lmm_poor_se=float(fit.bse["poor"]),
                     lmm_var_image=float(fit.vcomp[0]), n_subjects_both=int(len(diff)),
                     paired_mean_diff=float(diff.mean()), paired_boot=[float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))],
                     n_subj_poor_higher=int((diff > 0).sum()),
                     icc_well=icc1(list(img.vals[img.light == "well_lit"])), icc_poor=icc1(list(img.vals[img.light == "poorly_lit"])))
print("lighting", R["lighting"])

# 4. paired Golden vs Challenging difference (one image each per subject)
def w1(vals):
    tot = hit = 0
    for v in vals:
        for a, b in itertools.combinations(v, 2):
            tot += 1; hit += abs(a - b) <= 1
    return hit / tot
G = img[img.golden].set_index("subject").vals; C = img[img.chall].set_index("subject").vals
subs = sorted(G.index)
dw, di = [], []
for _ in range(2000):
    sel = rng.choice(subs, len(subs))
    dw.append(w1(G[sel]) - w1(C[sel])); di.append(icc1(list(G[sel])) - icc1(list(C[sel])))
R["golden_vs_chall"] = dict(w1_diff=w1(G) - w1(C), w1_diff_boot=[float(np.percentile(dw, 2.5)), float(np.percentile(dw, 97.5))],
                            icc_diff=icc1(list(G)) - icc1(list(C)), icc_diff_boot=[float(np.percentile(di, 2.5)), float(np.percentile(di, 97.5))])
print("golden vs chall", R["golden_vs_chall"])

# 5. "agreed within 1 point for all but one subject": alternative consensus definitions (this region)
med = img.vals.apply(np.median)
R["subject_within1_variants"] = dict(
    pooled_all_annotations=float(np.mean([abs(np.median(np.concatenate(list(img.vals[img.subject == s]))) - img.oracle[img.subject == s].iloc[0]) <= 1 for s in subs])),
    golden_image_median=float(np.mean(np.abs(med[img.golden] - img.oracle[img.golden]) <= 1)),
    challenging_image_median=float(np.mean(np.abs(med[img.chall] - img.oracle[img.chall]) <= 1)),
    median_of_image_medians=float(np.mean([abs(np.median(med[img.subject == s]) - img.oracle[img.subject == s].iloc[0]) <= 1 for s in subs])),
    per_subject_majority_of_images=float(np.mean([np.mean(np.abs(med[img.subject == s] - img.oracle[img.subject == s].iloc[0]) <= 1) > .5 for s in subs])))
print("subject within1 variants", R["subject_within1_variants"])

(OUT / "followup.json").write_text(json.dumps(R, indent=1, default=float))

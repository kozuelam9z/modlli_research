"""Independent verification of condition-effects (lighting/pose/mask) on MST-E Ghana crowd annotations.
Written from scratch; does not read the analyst's scripts or results.
Run: venv/bin/python -I verify.py
"""
import json, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent
DATA = OUT.parent / "annotations_clean.csv"
SEED = 987654  # deliberately different from analyst's
B = 4000
rng = np.random.default_rng(SEED)
R = {}

d = pd.read_csv(DATA)
assert len(d) == 7395 and d.image.nunique() == 1482 and d.subject.nunique() == 19
assert (d.err == d.mst_annot - d.oracle).all()
d["sid"] = d.subject.str.replace("subject_", "").astype(int)
d["poorly"] = (d.lighting == "poorly_lit").astype(float)
d["absErr"] = d.err.abs()

# image-level table
img = d.groupby("image").agg(sid=("sid", "first"), oracle=("oracle", "first"), lighting=("lighting", "first"),
                             pose=("pose", "first"), mask=("mask", "first"), golden=("is_golden", "first"),
                             chall=("is_challenging", "first"), conflict=("meta_conflict", "first"),
                             n=("mst_annot", "size"), mean=("mst_annot", "mean"), med=("mst_annot", "median"),
                             mabs=("absErr", "mean")).reset_index()
img["serr"] = img["mean"] - img.oracle            # image mean signed error
img["mederr"] = img.med - img.oracle               # per-image median signed error
img["medabs"] = img.mederr.abs()
img["portrait"] = img.image.str.contains("PORTRAIT")
SUBJ = sorted(img.sid.unique())
ORA = img.groupby("sid").oracle.first()
R["n"] = dict(annotations=len(d), images=len(img), subjects=len(SUBJ),
              lighting_counts=img.lighting.value_counts(dropna=False).to_dict(),
              pose_counts=img.pose.value_counts(dropna=False).to_dict(),
              mask_counts=img["mask"].value_counts(dropna=False).to_dict())

LIT = img[img.lighting.isin(["well_lit", "poorly_lit"])].copy()
dL = d[d.lighting.isin(["well_lit", "poorly_lit"])].copy()
R["n"]["lighting_analysis"] = dict(images=len(LIT), annotations=len(dL),
                                   poorly_imgs=int((LIT.lighting == "poorly_lit").sum()),
                                   well_imgs=int((LIT.lighting == "well_lit").sum()),
                                   poorly_ann=int((dL.lighting == "poorly_lit").sum()),
                                   well_ann=int((dL.lighting == "well_lit").sum()))


def boot_mean(x, b=B, seed=None, level=95):
    x = np.asarray(x, float)
    g = np.random.default_rng(SEED if seed is None else seed)
    idx = g.integers(0, len(x), (b, len(x)))
    m = x[idx].mean(1)
    a = (100 - level) / 2
    return [float(np.percentile(m, a)), float(np.percentile(m, 100 - a))]


def summarize(c, name):
    c = pd.Series(c).dropna()
    t = stats.ttest_1samp(c, 0)
    w = stats.wilcoxon(c) if (c != 0).sum() > 0 else None
    return dict(name=name, mean=float(c.mean()), ci95=boot_mean(c.values), ci90=boot_mean(c.values, level=90),
                n_subj=int(len(c)), n_pos=int((c > 0).sum()), n_neg=int((c < 0).sum()), n_zero=int((c == 0).sum()),
                t_p=float(t.pvalue), wilcoxon_p=float(w.pvalue) if w else None,
                per_subject={int(k): round(float(v), 4) for k, v in c.items()})


def contrast(df, col, cond_col, a, b_, agg="mean"):
    """per-subject mean(col | cond==a) - mean(col | cond==b_)"""
    g = df.groupby(["sid", cond_col])[col].mean().unstack()
    return (g[a] - g[b_]).dropna()


def tost(c, m):
    c = np.asarray(c, float); n = len(c); se = c.std(ddof=1) / np.sqrt(n); mu = c.mean()
    p1 = 1 - stats.t.cdf((mu + m) / se, n - 1)   # H0 mu <= -m
    p2 = stats.t.cdf((mu - m) / se, n - 1)       # H0 mu >= +m
    return float(max(p1, p2))


# ---------- (a) lighting contrasts ----------
LA = {}
c_sign = contrast(LIT, "serr", "lighting", "poorly_lit", "well_lit")
LA["signed_imagemean"] = summarize(c_sign, "signed, image-mean metric")
c_sign_ann = contrast(dL, "err", "lighting", "poorly_lit", "well_lit")
LA["signed_annweighted"] = summarize(c_sign_ann, "signed, annotation-weighted")
c_abs = contrast(dL, "absErr", "lighting", "poorly_lit", "well_lit")
LA["abs_annotation"] = summarize(c_abs, "abs err, annotation-level mean")
c_abs_img = contrast(LIT, "mabs", "lighting", "poorly_lit", "well_lit")
LA["abs_imagemean"] = summarize(c_abs_img, "abs err, image-mean of annotation abs err")
c_med_s = contrast(LIT, "mederr", "lighting", "poorly_lit", "well_lit")
LA["median_signed"] = summarize(c_med_s, "per-image median signed")
c_med_a = contrast(LIT, "medabs", "lighting", "poorly_lit", "well_lit")
LA["median_abs"] = summarize(c_med_a, "per-image |median-oracle|")
# within-subject Welch tests on image-mean signed error
welch = {}
for s in SUBJ:
    x = LIT[(LIT.sid == s) & (LIT.lighting == "poorly_lit")].serr; y = LIT[(LIT.sid == s) & (LIT.lighting == "well_lit")].serr
    welch[int(s)] = float(stats.ttest_ind(x, y, equal_var=False).pvalue)
LA["n_subjects_welch_p_lt_05"] = int(sum(p < .05 for p in welch.values()))
R["lighting_contrasts"] = LA

# ---------- (b) TOST ----------
R["tost"] = {k: {f"m{m}": tost(c, m) for m in (0.25, 0.5)} for k, c in
             dict(signed=c_sign, abs_ann=c_abs, median_abs=c_med_a, median_signed=c_med_s).items()}
R["tost"]["signed_boot90"] = LA["signed_imagemean"]["ci90"]

# ---------- paper-style unsigned vs signed by lighting ----------
def pooled_stats(frame):
    out = {}
    for L in ["well_lit", "poorly_lit"]:
        f = frame[frame.lighting == L]
        out[L] = dict(abs=float(f.medabs.mean()), signed=float(f.mederr.mean()), n=int(len(f)))
    out["diff_abs"] = out["poorly_lit"]["abs"] - out["well_lit"]["abs"]
    out["diff_signed"] = out["poorly_lit"]["signed"] - out["well_lit"]["signed"]
    return out

PS = pooled_stats(LIT)
# subject-cluster bootstrap of pooled stats
groups = {s: LIT[LIT.sid == s] for s in SUBJ}
g = np.random.default_rng(SEED + 1)
bs = []
for _ in range(B):
    samp = pd.concat([groups[s] for s in g.choice(SUBJ, len(SUBJ))])
    p = pooled_stats(samp)
    bs.append([p["well_lit"]["abs"], p["poorly_lit"]["abs"], p["diff_abs"], p["well_lit"]["signed"], p["poorly_lit"]["signed"], p["diff_signed"]])
bs = np.array(bs)
PS["ci95"] = dict(zip(["well_abs", "poorly_abs", "diff_abs", "well_signed", "poorly_signed", "diff_signed"],
                      [[float(np.percentile(bs[:, i], 2.5)), float(np.percentile(bs[:, i], 97.5))] for i in range(6)]))
# subject-balanced
sb = LIT.groupby(["sid", "lighting"])[["medabs", "mederr"]].mean().unstack()
PS["subject_balanced"] = dict(abs_well=float(sb["medabs"]["well_lit"].mean()), abs_poorly=float(sb["medabs"]["poorly_lit"].mean()),
                              signed_well=float(sb["mederr"]["well_lit"].mean()), signed_poorly=float(sb["mederr"]["poorly_lit"].mean()))
# variant: per-subject consensus = median of ALL annotations of that subject in a lighting cell
sc = dL.groupby(["sid", "lighting"]).mst_annot.median().unstack().sub(ORA, axis=0)
PS["subject_consensus_median"] = dict(abs_well=float(sc.well_lit.abs().mean()), abs_poorly=float(sc.poorly_lit.abs().mean()),
                                      signed_well=float(sc.well_lit.mean()), signed_poorly=float(sc.poorly_lit.mean()),
                                      within1_well=float((sc.well_lit.abs() <= 1).mean()), within1_poorly=float((sc.poorly_lit.abs() <= 1).mean()))
# variant: median of the per-image distance (instead of mean)
PS["median_of_image_abs"] = {L: float(LIT[LIT.lighting == L].medabs.median()) for L in ["well_lit", "poorly_lit"]}
# image within-1
PS["within1_image"] = {L: float((LIT[LIT.lighting == L].medabs <= 1).mean()) for L in ["well_lit", "poorly_lit"]}
R["paper_style_distance"] = PS

# ---------- mechanism ----------
well_bias = LIT[LIT.lighting == "well_lit"].groupby("sid").serr.mean()
rho = stats.spearmanr(well_bias.loc[c_abs.index], c_abs)
posb = well_bias[well_bias > 0].index; negb = well_bias[well_bias < 0].index
R["mechanism"] = dict(spearman_rho=float(rho.statistic), p=float(rho.pvalue),
                      n_pos=int(len(posb)), n_neg=int(len(negb)),
                      pos_oracles=sorted(ORA[posb].tolist()), neg_oracles=sorted(ORA[negb].tolist()),
                      abs_change_pos=float(c_abs[posb].mean()), ci_pos=boot_mean(c_abs[posb].values, seed=SEED + 2),
                      abs_change_neg=float(c_abs[negb].mean()), ci_neg=boot_mean(c_abs[negb].values, seed=SEED + 3),
                      well_bias_per_subject={int(k): round(float(v), 3) for k, v in well_bias.items()},
                      )
# arithmetic check: |err| change predicted purely by shifting each subject's well-lit annotations by its own signed contrast
wl = dL[dL.lighting == "well_lit"]
pred = pd.Series({s: float((wl[wl.sid == s].err + c_sign_ann[s]).abs().mean() - wl[wl.sid == s].absErr.mean()) for s in c_abs.index})
R["mechanism"]["pred_abs_change_from_uniform_shift"] = {int(k): round(v, 3) for k, v in pred.items()}
R["mechanism"]["pred_vs_obs_pearson"] = float(np.corrcoef(pred, c_abs[pred.index])[0, 1])
R["mechanism"]["pred_mean"] = float(pred.mean()); R["mechanism"]["obs_mean"] = float(c_abs.mean())
R["mechanism"]["pred_light"] = float(pred[lvl_tmp := (ORA[pred.index] <= 3)].mean()); R["mechanism"]["pred_middark"] = float(pred[~lvl_tmp].mean())

# ---------- (d) oracle level ----------
lvl = pd.cut(ORA, [0, 3, 6, 10], labels=["light", "mid", "dark"])
OL = {}
for nm, c in dict(signed=c_sign, abs=c_abs).items():
    o = {}
    for k, L in enumerate(["light", "mid", "dark"]):
        v = c[lvl[c.index] == L]
        o[L] = dict(mean=float(v.mean()), ci=boot_mean(v.values, seed=SEED + 10 + k), n=int(len(v)))
    vl = c[lvl[c.index] == "light"].values; vd = c[lvl[c.index] == "dark"].values
    g1 = np.random.default_rng(SEED + 20); g2 = np.random.default_rng(SEED + 21)
    dd = vl[g1.integers(0, len(vl), (B, len(vl)))].mean(1) - vd[g2.integers(0, len(vd), (B, len(vd)))].mean(1)
    o["light_minus_dark"] = float(vl.mean() - vd.mean()); o["lmd_ci"] = [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]
    o["kruskal_p"] = float(stats.kruskal(*[c[lvl[c.index] == L] for L in ["light", "mid", "dark"]]).pvalue)
    sp = stats.spearmanr(ORA[c.index], c); o["spearman_oracle"] = [float(sp.statistic), float(sp.pvalue)]
    OL[nm] = o
R["oracle_level"] = OL

# ---------- (e) golden vs challenging ----------
gold = img[img.golden].set_index("sid"); ch = img[img.chall].set_index("sid")
GC = {}
for stat_ in ["med", "mean", "medabs"]:
    c = (ch[stat_] - gold[stat_])
    GC[stat_] = summarize(c, f"challenging minus golden, {stat_}")
GC["tost_mean_0.5"] = tost(ch["mean"] - gold["mean"], 0.5)
GC["tost_med_0.5"] = tost(ch["med"] - gold["med"], 0.5)
GC["same_pose"] = int((ch.pose == gold.pose).sum()); GC["diff_mask"] = int((ch["mask"] != gold["mask"]).sum())
GC["gold_lighting"] = gold.lighting.value_counts(dropna=False).to_dict(); GC["chall_lighting"] = ch.lighting.value_counts(dropna=False).to_dict()
GC["gold_signed_mederr"] = float(gold.mederr.mean()); GC["chall_signed_mederr"] = float(ch.mederr.mean())
GC["gold_abs"] = float(gold.medabs.mean()); GC["chall_abs"] = float(ch.medabs.mean())
GC["gold_within1"] = float((gold.medabs <= 1).mean()); GC["chall_within1"] = float((ch.medabs <= 1).mean())
GC["n_ann"] = dict(gold=gold.n.value_counts().to_dict(), chall=ch.n.value_counts().to_dict())
GC["pairs"] = {int(s): dict(oracle=int(gold.oracle[s]), gpose=str(gold.pose[s]), cpose=str(ch.pose[s]), glit=str(gold.lighting[s]),
                            clit=str(ch.lighting[s]), gmed=float(gold.med[s]), cmed=float(ch.med[s])) for s in SUBJ}
R["golden_challenging"] = GC

# ---------- (f) mask & pose contrasts ----------
MK = {}
LITm = LIT.dropna(subset=["mask"]).copy(); LITm["mk"] = LITm["mask"].map({1.0: "m", 0.0: "u"})
MK["signed_all"] = summarize(contrast(LITm, "serr", "mk", "m", "u"), "mask minus unmasked, signed")
MK["signed_well"] = summarize(contrast(LITm[LITm.lighting == "well_lit"], "serr", "mk", "m", "u"), "mask, well-lit only")
MK["signed_poorly"] = summarize(contrast(LITm[LITm.lighting == "poorly_lit"], "serr", "mk", "m", "u"), "mask, poorly-lit only")
dLm = dL.dropna(subset=["mask"]).copy(); dLm["mk"] = dLm["mask"].map({1.0: "m", 0.0: "u"})
MK["abs_ann"] = summarize(contrast(dLm, "absErr", "mk", "m", "u"), "mask abs change")
with_mask = LITm[LITm["mask"] == 1].sid.unique()
MK["n_images_in_mask_subjects"] = LITm[LITm.sid.isin(with_mask)]["mk"].value_counts().to_dict()
MK["subjects_without_mask"] = sorted(int(s) for s in set(SUBJ) - set(with_mask))
MK["lighting_x_mask"] = pd.crosstab(LITm.lighting, LITm["mask"]).to_dict()
R["mask"] = MK
PO = {}
for q in ["bottom", "frontal", "side"]:
    c = contrast(LIT, "serr", "pose", q, "facing_camera")
    PO[q] = summarize(c, f"{q} minus facing_camera"); PO[q]["tost_0.25"] = tost(c, 0.25)
    PO[q]["abs_change"] = float(contrast(dL, "absErr", "pose", q, "facing_camera").mean())
R["pose"] = PO

# ---------- robustness ----------
def sign_c(frame):
    return contrast(frame, "serr", "lighting", "poorly_lit", "well_lit")
def abs_c(frame):
    dd = dL[dL.image.isin(frame.image)]
    return contrast(dd, "absErr", "lighting", "poorly_lit", "well_lit")
RB = {}
for nm, f in dict(unmasked=LIT[LIT["mask"] == 0], five_ann=LIT[LIT.n == 5], no_conflict=LIT[~LIT.conflict],
                  no_gold_chall=LIT[~LIT.golden & ~LIT.chall], portrait_only=LIT[LIT.portrait], nonportrait_only=LIT[~LIT.portrait]).items():
    c = sign_c(f); RB[nm] = dict(signed=float(c.mean()), ci=boot_mean(c.values), n_subj=int(len(c)), abs=float(abs_c(f).mean()))
RB["portrait_by_lighting"] = pd.crosstab(LIT.lighting, LIT.portrait).to_dict()
R["robustness"] = RB

# ---------- (c) models ----------
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

dM = dL.dropna(subset=["mask", "pose"]).copy()
for q in ["bottom", "frontal", "side"]:
    dM[f"p_{q}"] = (dM.pose == q).astype(float)
dM["mask"] = dM["mask"].astype(float)
R["n"]["model_rows"] = dict(annotations=len(dM), images=int(dM.image.nunique()), subjects=int(dM.sid.nunique()))
XC = ["poorly", "p_bottom", "p_frontal", "p_side", "mask"]

# OLS with subject FE
ols = smf.ols("err ~ C(sid) + " + " + ".join(XC), dM).fit()
M = {"ols_fe": {k: float(ols.params[k]) for k in XC}}

# Mixed models
t0 = time.time()
lmm = smf.mixedlm("err ~ " + " + ".join(XC), dM, groups="sid", re_formula="1",
                  vc_formula={"image": "0 + C(image)"}).fit(reml=True, method="powell", maxiter=5000)
ci = lmm.conf_int()
M["lmm_ri_vc"] = {k: dict(coef=float(lmm.params[k]), ci=[float(ci.loc[k, 0]), float(ci.loc[k, 1])]) for k in XC}
M["lmm_ri_vc"]["var_subject"] = float(lmm.cov_re.iloc[0, 0]); M["lmm_ri_vc"]["var_image"] = float(lmm.vcomp[0]); M["lmm_ri_vc"]["var_resid"] = float(lmm.scale)
M["lmm_ri_vc"]["secs"] = time.time() - t0; M["lmm_ri_vc"]["converged"] = bool(lmm.converged)
print("lmm vc done", time.time() - t0, flush=True)
lmm_rs = smf.mixedlm("err ~ " + " + ".join(XC), dM, groups="sid", re_formula="1 + poorly").fit(reml=True)
ci = lmm_rs.conf_int()
M["lmm_rslope"] = dict(coef=float(lmm_rs.params["poorly"]), ci=[float(ci.loc["poorly", 0]), float(ci.loc["poorly", 1])],
                       slope_sd=float(np.sqrt(lmm_rs.cov_re.iloc[1, 1])), mask=float(lmm_rs.params["mask"]), converged=bool(lmm_rs.converged))
lmm_rs2 = smf.mixedlm("err ~ " + " + ".join(XC), dM, groups="sid", re_formula="1 + poorly",
                       vc_formula={"image": "0 + C(image)"}).fit(reml=True, method="powell", maxiter=5000)
ci = lmm_rs2.conf_int()
M["lmm_rslope_vc"] = dict(coef=float(lmm_rs2.params["poorly"]), ci=[float(ci.loc["poorly", 0]), float(ci.loc["poorly", 1])],
                          slope_sd=float(np.sqrt(lmm_rs2.cov_re.iloc[1, 1])), converged=bool(lmm_rs2.converged))
# interaction with oracle (centered)
dM["orc"] = dM.oracle - dM.oracle.mean()
lmm_int = smf.mixedlm("err ~ poorly*orc + p_bottom + p_frontal + p_side + mask", dM, groups="sid", re_formula="1",
                      vc_formula={"image": "0 + C(image)"}).fit(reml=True, method="powell", maxiter=5000)
ci = lmm_int.conf_int()
M["lmm_interaction"] = dict(coef=float(lmm_int.params["poorly:orc"]), ci=[float(ci.loc["poorly:orc", 0]), float(ci.loc["poorly:orc", 1])],
                            p=float(lmm_int.pvalues["poorly:orc"]), converged=bool(lmm_int.converged))
print("lmm all done", flush=True)

# Ordinal logit (full-data fit); bootstrap lives in boot_models.py
sys.path.insert(0, str(OUT))
from boot_models import fit_ord
o_full = fit_ord(dM, dM.sid)
M["ordinal"] = o_full
M["ordinal"]["coef_over_spacing"] = o_full["beta"]["poorly"] / o_full["spacing"]
bp = OUT / "boot_results.json"
M["boot"] = json.load(open(bp)) if bp.exists() else "run boot_models.py first"
R["models"] = M
json.dump(R, open(OUT / "verify_results.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print(json.dumps(R, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))

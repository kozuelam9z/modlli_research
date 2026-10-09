# Independent recomputation of MST-E single-region reliability numbers.
# Run: venv/bin/python -I verify.py
import json, itertools, math, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

OUT = Path(__file__).resolve().parent
S = OUT.parent.parent
d = pd.read_csv(S / "reanalysis" / "annotations_clean.csv")
SEED = 777
B = 2000
R = {}

# ---------- basic structure ----------
d["y"] = d["mst_annot"].astype(int)
img = d.groupby("image").agg(subject=("subject", "first"), oracle=("oracle", "first"),
                             lighting=("lighting", "first"), golden=("is_golden", "first"),
                             chall=("is_challenging", "first"), n=("y", "size"),
                             s=("y", "sum"), q=("y", lambda v: (v ** 2).sum()),
                             med=("y", "median"), vals=("y", lambda v: sorted(v)))
img = img.reset_index()
subs = sorted(img.subject.unique())
R["n"] = dict(annotations=len(d), images=len(img), subjects=len(subs),
              imgs_with_5=int((img.n == 5).sum()), imgs_with_4=int((img.n == 4).sum()))


# ---------- ICC(1) from group sufficient stats ----------
def icc1(n, s, q, alpha=0.05):
    n, s, q = map(np.asarray, (n, s, q))
    N, a = n.sum(), len(n)
    ssb = (s ** 2 / n).sum() - s.sum() ** 2 / N
    ssw = q.sum() - (s ** 2 / n).sum()
    msb, msw = ssb / (a - 1), ssw / (N - a)
    k0 = (N - (n ** 2).sum() / N) / (a - 1)
    F = msb / msw
    df1, df2 = a - 1, N - a
    r1 = (msb - msw) / (msb + (k0 - 1) * msw)
    rk = 1 - 1 / F
    FL = F / stats.f.ppf(1 - alpha / 2, df1, df2)
    FU = F * stats.f.ppf(1 - alpha / 2, df2, df1)
    return dict(icc1=r1, icc1k=rk, k0=k0, F=F, df1=int(df1), df2=int(df2),
                p=float(stats.f.sf(F, df1, df2)), mw_lo=(FL - 1) / (FL + k0 - 1),
                mw_hi=(FU - 1) / (FU + k0 - 1), msb=msb, msw=msw)


def icc_df(frame, target):
    g = frame.groupby(target)["y"]
    return icc1(g.size().values, g.sum().values, g.apply(lambda v: (v ** 2).sum()).values)


def boot_subjects(fn, sub_list, seed=SEED, B=B):
    """fn(list_of_subject_ids_with_duplicates) -> scalar; duplicates are distinct clusters."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(B):
        out.append(fn(list(rng.choice(sub_list, len(sub_list), replace=True))))
    out = np.array(out, float)
    return [float(np.nanpercentile(out, 2.5)), float(np.nanpercentile(out, 97.5))]


# image-level stat arrays grouped by subject for fast bootstrap
by_sub = {s: img[img.subject == s] for s in subs}


def icc_images_of(sel, mask_col=None):
    parts = [by_sub[s] if mask_col is None else by_sub[s][by_sub[s][mask_col]] for s in sel]
    t = pd.concat(parts)
    return icc1(t.n.values, t.s.values, t.q.values)["icc1"]


def show(name, r):
    print(f"{name}: " + ", ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in r.items()))


# (a) Golden / Challenging / all images
for nm, col in [("golden", "golden"), ("challenging", "chall")]:
    t = img[img[col]]
    r = icc1(t.n.values, t.s.values, t.q.values)
    r["boot"] = boot_subjects(lambda sel: icc_images_of(sel, col), subs)
    r["n_images"], r["n_ann"] = len(t), int(t.n.sum())
    R[f"icc_{nm}"] = r; show(nm, r)

r = icc1(img.n.values, img.s.values, img.q.values)
r["boot"] = boot_subjects(lambda sel: icc_images_of(sel), subs)
R["icc_i_all_images"] = r; show("def i", r)

# pingouin cross-check on golden
import pingouin as pg
gd = d[d.is_golden].copy(); gd["slot"] = gd.pos_in_image
pgi = pg.intraclass_corr(gd, targets="image", raters="slot", ratings="y"); print(pgi.iloc[:, :3]); pgi = pgi.set_index(pgi.columns[0])
R["pingouin_golden_ICC1"] = float(pgi.iloc[0]["ICC"]); print("pingouin golden ICC1", R["pingouin_golden_ICC1"])

# (ii-a) subjects as targets, all annotations replicates
sub_stats = d.groupby("subject")["y"].agg(n="size", s="sum", q=lambda v: (v ** 2).sum())
r = icc_df(d, "subject")
r["boot"] = boot_subjects(lambda sel: icc1(sub_stats.loc[sel].n.values, sub_stats.loc[sel].s.values,
                                           sub_stats.loc[sel].q.values)["icc1"], subs)
R["icc_iia_subject_all_ann"] = r; show("def ii-a", r)
# (ii-b) image means as replicates; (ii-c) image medians
img["mean"] = img.s / img.n
for nm, col in [("iib_img_means", "mean"), ("iic_img_medians", "med")]:
    t = img.assign(y=img[col])
    r = icc_df(t, "subject")
    R[f"icc_{nm}"] = r; show(nm, r)

# (iii) within each subject across images
per = {}
for s in subs:
    t = by_sub[s]
    per[s] = icc1(t.n.values, t.s.values, t.q.values)
vals = np.array([per[s]["icc1"] for s in subs])
R["icc_iii_within_subject"] = dict(median=float(np.median(vals)), mean=float(vals.mean()),
                                   min=float(vals.min()), max=float(vals.max()),
                                   n_p_lt_05=int(sum(per[s]["p"] < .05 for s in subs)),
                                   boot_median=boot_subjects(lambda sel: np.median([per[x]["icc1"] for x in sel]), subs),
                                   boot_mean=boot_subjects(lambda sel: np.mean([per[x]["icc1"] for x in sel]), subs),
                                   per_subject={s: round(per[s]["icc1"], 4) for s in subs})
show("def iii", {k: v for k, v in R["icc_iii_within_subject"].items() if k != "per_subject"})


# ---------- (b) pairwise agreement, alpha, quadratic kappa ----------
def counts(v):
    c = np.zeros(10); np.add.at(c, np.asarray(v) - 1, 1); return c


img["cnt"] = img.vals.apply(counts)
V = np.arange(1, 11)
D = np.abs(V[:, None] - V[None, :])


def pmat(c):  # unordered within-image pairs by value
    return (np.outer(c, c) - np.diag(c)) / 2


def omat(c):  # Krippendorff coincidences
    return (np.outer(c, c) - np.diag(c)) / (c.sum() - 1)


img["P"] = img.cnt.apply(pmat); img["O"] = img.cnt.apply(omat)


def agg(t):
    return dict(P=np.sum(list(t.P), axis=0), O=np.sum(list(t.O), axis=0), C=np.sum(list(t.cnt), axis=0))


def pair_stats(a):
    P = a["P"]; tot = P.sum()
    return dict(n_pairs=tot, exact=np.trace(P) / tot, within1=P[D <= 1].sum() / tot, mad=(P * D).sum() / tot,
                po_w=(P * (1 - D ** 2 / 81)).sum() / tot)


def alpha_from(a, metric):
    O = a["O"]; nc = O.sum(1); n = nc.sum()
    if metric == "nominal":
        dl = (D > 0).astype(float)
    elif metric == "interval":
        dl = D.astype(float) ** 2
    else:
        dl = np.array([[(nc[min(i, j):max(i, j) + 1].sum() - (nc[i] + nc[j]) / 2) ** 2 for j in range(10)] for i in range(10)])
    return 1 - (O * dl).sum() / n / ((np.outer(nc, nc) * dl).sum() / (n * (n - 1)))


def qkappa(a):
    ps = pair_stats(a); p = a["C"] / a["C"].sum()
    mu = (p * V).sum(); var = (p * (V - mu) ** 2).sum(); pe = 1 - 2 * var / 81
    return dict(po_w=ps["po_w"], pe_w=pe, kappa=(ps["po_w"] - pe) / (1 - pe))


AG = {s: agg(img[img.subject == s]) for s in subs}
sumag = lambda sel: {k: np.sum([AG[x][k] for x in sel], axis=0) for k in ("P", "O", "C")}

allrows = agg(img)
ps = pair_stats(allrows)
for key in ["exact", "within1", "mad"]:
    ps[f"boot_{key}"] = boot_subjects(lambda sel, key=key: pair_stats(sumag(sel))[key], subs)
R["pairwise_all"] = ps; show("pairwise all", {k: v for k, v in ps.items()})
for nm, m in [("golden", img.golden), ("challenging", img.chall), ("well_lit", img.lighting == "well_lit"),
              ("poorly_lit", img.lighting == "poorly_lit")]:
    R[f"pairwise_{nm}"] = pair_stats(agg(img[m])); show(f"pairwise {nm}", R[f"pairwise_{nm}"])

import krippendorff
rel = np.full((5, len(img)), np.nan)
for j, v in enumerate(img.vals):
    rel[:len(v), j] = v
R["alpha"] = {}
for met in ["ordinal", "interval", "nominal"]:
    mine = alpha_from(allrows, met)
    pkg = krippendorff.alpha(reliability_data=rel, level_of_measurement=met, value_domain=list(range(1, 11)))
    bt = boot_subjects(lambda sel, met=met: alpha_from(sumag(sel), met), subs)
    R["alpha"][met] = dict(mine=mine, package=float(pkg), boot=bt)
    for nm, m in [("golden", img.golden), ("challenging", img.chall)]:
        R["alpha"][met][nm] = alpha_from(agg(img[m]), met)
print("alpha", R["alpha"])
qk = qkappa(allrows)
qk["boot_kappa"] = boot_subjects(lambda sel: qkappa(sumag(sel))["kappa"], subs)
R["quadratic_kappa"] = qk; print("qkappa", qk)

# within-image order check (is pos_in_image random?)
p_nondec = [math.prod(math.factorial(int(x)) for x in c) / math.factorial(int(c.sum())) for c in img.cnt]
obs_nondec = np.mean([all(a <= b for a, b in zip(v, v[1:])) for v in
                      d.sort_values(["image", "pos_in_image"]).groupby("image").y.apply(list)])
R["order_check"] = dict(observed_nondecreasing_share=float(obs_nondec), expected_if_random=float(np.mean(p_nondec)),
                        slot_means={int(k): float(v) for k, v in d.groupby("pos_in_image").y.mean().items()})
print("order", R["order_check"])

# ---------- (c) variance decomposition ----------
import statsmodels.formula.api as smf
md = smf.mixedlm("y ~ 1", d, groups="subject", re_formula="1", vc_formula={"image": "0 + C(image)"})
fit = md.fit(reml=True)
vs, vi, ve = float(fit.cov_re.iloc[0, 0]), float(fit.vcomp[0]), float(fit.scale)
tot = vs + vi + ve
R["lmm"] = dict(converged=bool(fit.converged), var_subject=vs, var_image=vi, var_resid=ve,
                share_subject=vs / tot, share_image=vi / tot, share_resid=ve / tot,
                err_sd=math.sqrt(ve), img_sd=math.sqrt(vi))
print("lmm", R["lmm"])


def nested_anova(sel):
    # sel: subjects (duplicates allowed); returns (va, vb, ve)
    parts = [by_sub[s] for s in sel]
    n_ij = np.concatenate([p.n.values for p in parts]); s_ij = np.concatenate([p.s.values for p in parts])
    q_ij = np.concatenate([p.q.values for p in parts])
    n_i = np.array([p.n.sum() for p in parts]); s_i = np.array([p.s.sum() for p in parts])
    a, Bn, N = len(parts), len(n_ij), n_ij.sum()
    sse = q_ij.sum() - (s_ij ** 2 / n_ij).sum()
    ssb = (s_ij ** 2 / n_ij).sum() - (s_i ** 2 / n_i).sum()
    ssa = (s_i ** 2 / n_i).sum() - s_i.sum() ** 2 / N
    mse, msb, msa = sse / (N - Bn), ssb / (Bn - a), ssa / (a - 1)
    sum_i = sum((p.n.values ** 2).sum() / p.n.sum() for p in parts)
    c1 = (N - sum_i) / (Bn - a)
    c2 = (sum_i - (n_ij ** 2).sum() / N) / (a - 1)
    c3 = (N - (n_i ** 2).sum() / N) / (a - 1)
    ve_ = mse; vb_ = (msb - mse) / c1; va_ = (msa - mse - c2 * vb_) / c3
    return va_, vb_, ve_


va, vb, ve2 = nested_anova(subs); t2 = va + vb + ve2
R["anova_moments"] = dict(var_subject=va, var_image=vb, var_resid=ve2, share_subject=va / t2,
                          share_image=vb / t2, share_resid=ve2 / t2, err_sd=math.sqrt(ve2))
for i, nm in enumerate(["share_subject", "share_image", "share_resid"]):
    R["anova_moments"][f"boot_{nm}"] = boot_subjects(lambda sel, i=i: (lambda v: v[i] / sum(v))(nested_anova(sel)), subs)
R["anova_moments"]["boot_err_sd"] = boot_subjects(lambda sel: math.sqrt(nested_anova(sel)[2]), subs)
print("anova", R["anova_moments"])

# ---------- (d) spread dependence ----------
bands = {"light_1_3": (1, 3), "mid_4_7": (4, 7), "dark_8_10": (8, 10)}
R["bands"] = {}
for nm, (lo, hi) in bands.items():
    t = img[(img.oracle >= lo) & (img.oracle <= hi)]
    bs = sorted(t.subject.unique())
    r = icc1(t.n.values, t.s.values, t.q.values)
    within_sd = math.sqrt(r["msw"]); sd_means = float(t["mean"].std(ddof=1))
    R["bands"][nm] = dict(icc1=r["icc1"], n_subjects=len(bs), n_images=len(t), within_sd=within_sd,
                          sd_image_means=sd_means, boot=boot_subjects(lambda sel: icc_images_of(sel), bs))
R["sd_image_means_all"] = float(img["mean"].std(ddof=1))
print("bands", R["bands"], R["sd_image_means_all"])

rng = np.random.default_rng(SEED)
R["golden_like"] = {}
for nm, (lo, hi), filt in [("all", (1, 10), None), ("win_3_5", (3, 5), None), ("win_8_10", (8, 10), None),
                           ("well_lit_only", (1, 10), "well_lit"), ("poorly_lit_only", (1, 10), "poorly_lit")]:
    pool = img[(img.oracle >= lo) & (img.oracle <= hi)]
    if filt: pool = pool[pool.lighting == filt]
    groups = [g for _, g in pool.groupby("subject")]
    res = []
    for _ in range(2000):
        pick = pd.concat([g.iloc[[rng.integers(len(g))]] for g in groups])
        res.append(icc1(pick.n.values, pick.s.values, pick.q.values)["icc1"])
    R["golden_like"][nm] = dict(n_subjects=len(groups), median=float(np.median(res)),
                                p2_5=float(np.percentile(res, 2.5)), p97_5=float(np.percentile(res, 97.5)))
print("golden-like", R["golden_like"])

# ---------- (e) k-rater analysis ----------
five = img[img.n == 5].reset_index(drop=True)
X = np.array([np.array(v) for v in d[d.image.isin(five.image)].sort_values(["image", "pos_in_image"])
              .groupby("image").y.apply(list).loc[five.image]])
orc = five.oracle.values
med5 = np.median(X, axis=1)


def lower_upper_mid(sub):  # sorted rows; returns lower and upper middle order stats
    k = sub.shape[1]; srt = np.sort(sub, axis=1)
    return srt[:, (k - 1) // 2], srt[:, k // 2]


def agree(m, ref):
    diff = m - ref
    return np.vstack([np.abs(diff) < 1e-9, np.abs(diff) <= 1 + 1e-9, np.abs(diff), diff])  # exact, w1, abs, signed


def krater(mask):
    out = {}
    Xm, om, m5 = X[mask], orc[mask], med5[mask]
    for k in range(1, 6):
        acc = {v: [] for v in ["raw", "rand_os", "rand_round"]}
        acc5 = {v: [] for v in ["raw", "rand_os"]}
        hold = {v: [] for v in ["raw", "rand_os"]}
        for comb in itertools.combinations(range(5), k):
            sub = Xm[:, comb]
            raw = np.median(sub, axis=1)
            lo, hi = lower_upper_mid(sub)
            acc["raw"].append(agree(raw, om))
            acc["rand_os"].append((agree(lo, om) + agree(hi, om)) / 2)       # random pick of a middle order stat
            acc["rand_round"].append((agree(np.floor(raw), om) + agree(np.ceil(raw), om)) / 2)  # round .5 at random
            acc5["raw"].append(agree(raw, m5)); acc5["rand_os"].append((agree(lo, m5) + agree(hi, m5)) / 2)
            if k < 5:
                rest = [i for i in range(5) if i not in comb]
                ho = Xm[:, rest]; hraw = np.median(ho, axis=1); hlo, hhi = lower_upper_mid(ho)
                hold["raw"].append(agree(raw, hraw))
                hold["rand_os"].append((agree(lo, hlo) + agree(lo, hhi) + agree(hi, hlo) + agree(hi, hhi)) / 4)
        rec = {}
        for nm, dd in [("oracle", acc), ("vs_med5", acc5), ("vs_heldout", hold)]:
            for v, lst in dd.items():
                if not lst: continue
                a = np.mean(lst, axis=0).mean(axis=1)  # avg over subsets then over images
                rec[f"{nm}_{v}"] = dict(exact=a[0], within1=a[1], mae=a[2], signed=a[3])
        out[k] = rec
    return out


masks = {"all": np.ones(len(five), bool), "golden": five.golden.values, "challenging": five.chall.values,
         "well_lit": (five.lighting == "well_lit").values, "poorly_lit": (five.lighting == "poorly_lit").values}
R["krater"] = {nm: dict(n_images=int(m.sum()), n_subjects=int(five.subject[m].nunique()), res=krater(m))
               for nm, m in masks.items()}
for nm in masks:
    kr = R["krater"][nm]["res"]
    print(nm, R["krater"][nm]["n_images"], {k: (round(kr[k]["oracle_raw"]["within1"], 3), round(kr[k]["oracle_rand_os"]["within1"], 3),
                                                  round(kr[k]["oracle_raw"]["mae"], 3)) for k in kr})
    print("  vs5/heldout k=1", {k: round(v, 3) for k, v in kr[1]["vs_med5_raw"].items()},
          {k: round(v, 3) for k, v in kr[1]["vs_heldout_raw"].items()}, {k: round(v, 3) for k, v in kr[1]["vs_heldout_rand_os"].items()})

# subject-clustered bootstrap for k=1,3,5 within-1/MAE vs oracle (all images)
f_sub = five.subject.values


def kr_boot_stat(k, which):
    per_img = np.mean([agree(np.median(X[:, c], axis=1), orc)[which] for c in itertools.combinations(range(5), k)], axis=0)
    idx = {s: np.where(f_sub == s)[0] for s in subs}
    return boot_subjects(lambda sel: per_img[np.concatenate([idx[x] for x in sel])].mean(), subs)


R["krater_boot"] = {f"k{k}_{nm}": kr_boot_stat(k, w) for k in (1, 3, 5) for nm, w in [("within1", 1), ("mae", 2)]}
print("krater boot", R["krater_boot"])

# Spearman-Brown
r1 = icc1(five.n.values, five.s.values, five.q.values)["icc1"]
sb = lambda k, r: k * r / (1 + (k - 1) * r)
need = lambda rho, r: rho * (1 - r) / (r * (1 - rho))
emp = []
for A in itertools.combinations(range(5), 2):
    for Bc in itertools.combinations([i for i in range(5) if i not in A], 2):
        if A < Bc:
            m = np.column_stack([X[:, A].mean(1), X[:, Bc].mean(1)])
            emp.append(icc1(np.full(len(m), 2), m.sum(1), (m ** 2).sum(1))["icc1"])
rg = icc1(img[img.golden].n.values, img[img.golden].s.values, img[img.golden].q.values)["icc1"]
rc = icc1(img[img.chall].n.values, img[img.chall].s.values, img[img.chall].q.values)["icc1"]
R["spearman_brown"] = dict(r1_five=r1, sb2=sb(2, r1), sb5=sb(5, r1), emp2_mean=float(np.mean(emp)),
                           emp2_min=float(min(emp)), emp2_max=float(max(emp)), n_partitions=len(emp),
                           need95_all=need(.95, r1), need95_golden=need(.95, rg), need95_chall=need(.95, rc),
                           need90_all=need(.9, r1), need90_golden=need(.9, rg), need90_chall=need(.9, rc))
print("SB", R["spearman_brown"])

# subject-level consensus vs oracle with k raters/image
rng = np.random.default_rng(SEED)
sub_imgs = {s: [np.array(v) for v in img.vals[img.subject == s]] for s in subs}
sub_or = img.groupby("subject").oracle.first()
R["subject_consensus"] = {}
for k in range(1, 6):
    w1, ex, mae, w1m = [], [], [], []
    for _ in range(500):
        hits, exs, aes, hm = [], [], [], []
        for s in subs:
            picks = [rng.choice(v, min(k, len(v)), replace=False) for v in sub_imgs[s]]
            cons = np.median(np.concatenate(picks))
            mm = np.median([np.median(p) for p in picks])
            e = cons - sub_or[s]
            hits.append(abs(e) <= 1); exs.append(e == 0); aes.append(abs(e)); hm.append(abs(mm - sub_or[s]) <= 1)
        w1.append(np.mean(hits)); ex.append(np.mean(exs)); mae.append(np.mean(aes)); w1m.append(np.mean(hm))
    R["subject_consensus"][k] = dict(within1=float(np.mean(w1)), w1_p2_5=float(np.percentile(w1, 2.5)),
                                     w1_p97_5=float(np.percentile(w1, 97.5)), exact=float(np.mean(ex)),
                                     mae=float(np.mean(mae)), within1_med_of_meds=float(np.mean(w1m)))
print("subject consensus", R["subject_consensus"])
full = d.groupby("subject").y.median()
R["subject_full_median"] = {s: dict(oracle=int(sub_or[s]), median=float(full[s])) for s in subs}
R["subject_full_within1"] = float(np.mean([abs(full[s] - sub_or[s]) <= 1 for s in subs]))
R["subject_full_exact"] = int(sum(full[s] == sub_or[s] for s in subs))
print({s: (int(sub_or[s]), float(full[s])) for s in subs}, R["subject_full_within1"], R["subject_full_exact"])

# average median distance (image-level, all available ratings)
img["dev"] = img.med - img.oracle
R["median_distance"] = {}
for nm, m in [("all", np.ones(len(img), bool)), ("well_lit", img.lighting == "well_lit"),
              ("poorly_lit", img.lighting == "poorly_lit"), ("golden", img.golden), ("challenging", img.chall)]:
    t = img[m]
    R["median_distance"][nm] = dict(n=int(len(t)), abs=float(t.dev.abs().mean()), signed=float(t.dev.mean()),
                                    within1=float((t.dev.abs() <= 1).mean()),
                                    abs_subject_weighted=float(t.groupby("subject").dev.apply(lambda v: v.abs().mean()).mean()))
print("median distance", R["median_distance"])

(OUT / "results.json").write_text(json.dumps(R, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
print("saved")

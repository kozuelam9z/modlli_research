"""V2 stress test of the local MST-E evidence (K02, K03, K06, K07, K10).
Reads existing scored_merged.csv + scores_cheeks.csv; no re-scoring."""
import sys
import numpy as np, pandas as pd
from scipy import stats

SP = "/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/aa16d469-2438-4934-be22-436934f5e296/scratchpad"
df = pd.read_csv(SP + "/mste_proc/scored_merged.csv")
ck = pd.read_csv(SP + "/mste_proc/scores_cheeks.csv")
df = df.merge(ck.drop(columns=["subject"]), on="file", how="left")
df["est_shift"] = df.h_full - df.hmean_full  # estimator minus pixel-mean hue
df["est_shift_ck"] = df.h_ck - df.hmean_ck


def icc1(d, col):
    d = d.dropna(subset=[col])
    g = d.groupby("subject")[col]
    k = g.size(); k = k[k >= 2]; d = d[d.subject.isin(k.index)]; g = d.groupby("subject")[col]
    n = len(k); N = k.sum(); grand = d[col].mean()
    msb = (k * (g.mean() - grand) ** 2).sum() / (n - 1)
    msw = ((d[col] - d.subject.map(g.mean())) ** 2).sum() / (N - n)
    k0 = (N - (k ** 2).sum() / N) / (n - 1)
    return (msb - msw) / (msb + (k0 - 1) * msw), np.sqrt(msw), g.mean().std(), len(d), n


def boot(d, col, B=1000, seed=0):
    rng = np.random.default_rng(seed); subs = d.subject.unique(); gs = dict(tuple(d.groupby("subject"))); v = []
    for _ in range(B):
        pick = rng.choice(subs, len(subs))
        v.append(icc1(pd.concat([gs[p].assign(subject=f"{p}_{i}") for i, p in enumerate(pick)]), col)[0])
    return np.percentile(v, [2.5, 97.5])


wl = df[df.lighting == "well_lit"]
front = wl[wl.pose.isin(["facing_camera", "frontal"])]
subsets = {"all": df, "well_lit": wl, "well_lit_frontal": front,
           "well_lit_frontal_noneg": front[front.h_full >= 0]}
print("== ICC(1) [subjects as targets]; cols: icc, within_sd, between_sd_means, n_img, n_subj ==")
for name, d in subsets.items():
    for col in ["L_full", "h_full", "L_ck", "h_ck", "Lmean_full", "hmean_full", "hmean_ck"]:
        r = icc1(d, col)
        ci = boot(d, col, B=500) if col in ("h_full", "L_full", "h_ck") else (np.nan, np.nan)
        print(f"{name:24s} {col:11s} icc={r[0]:.2f} [{ci[0]:.2f},{ci[1]:.2f}] wSD={r[1]:.1f} bSD={r[2]:.1f} n={r[3]} s={r[4]}")

# leave-two-out on the noisiest dark subjects
drop2 = ["subject_12", "subject_4"]
for name, d in (("well_lit", wl), ("well_lit_frontal", front)):
    for col in ("h_full", "h_ck", "L_full"):
        r = icc1(d[~d.subject.isin(drop2)], col)
        print(f"drop {drop2} {name} {col}: icc={r[0]:.2f} wSD={r[1]:.1f} bSD={r[2]:.1f}")
    r = icc1(d[d.oracle <= 7], "h_full"); print(f"{name} MST<=7 only h_full icc={r[0]:.2f} wSD={r[1]:.1f} bSD={r[2]:.1f}")

print("\n== within-subject SD by oracle MST (per subject) ==")
for name, d in (("all", df), ("well_lit", wl), ("well_lit_frontal", front)):
    per = d.groupby("subject").agg(oracle=("oracle", "first"), n=("file", "size"),
                                   sd_est=("h_full", "std"), sd_mean=("hmean_full", "std"),
                                   sd_est_ck=("h_ck", "std"), sd_mean_ck=("hmean_ck", "std"),
                                   shift=("est_shift", "mean"), shift_ck=("est_shift_ck", "mean"),
                                   hm=("h_full", "mean"), hmm=("hmean_full", "mean"), hck=("h_ck", "mean"), hmck=("hmean_ck", "mean"),
                                   Lm=("L_full", "mean"), Lck=("L_ck", "mean"))
    per["grp"] = pd.cut(per.oracle, [0, 3, 6, 10], labels=["1-3", "4-6", "7-10"])
    print(f"-- {name}")
    print(per.groupby("grp", observed=True)[["sd_est", "sd_mean", "sd_est_ck", "sd_mean_ck", "shift", "shift_ck"]].mean().round(1).to_string())
    for c in ("sd_est", "sd_mean", "sd_est_ck", "sd_mean_ck", "shift", "shift_ck", "hm", "hmm", "hck", "hmck", "Lm", "Lck"):
        rho, p = stats.spearmanr(per.oracle, per[c])
        # jackknife range and drop-2-most-extreme
        jk = [stats.spearmanr(per.drop(s).oracle, per.drop(s)[c])[0] for s in per.index]
        p2 = per.drop([s for s in drop2 if s in per.index])
        rho2, pp2 = stats.spearmanr(p2.oracle, p2[c])
        print(f"   rho(oracle,{c:10s})={rho:+.2f} p={p:.3f}  jackknife[{min(jk):+.2f},{max(jk):+.2f}]  drop2: {rho2:+.2f} p={pp2:.3f}")
    if name == "well_lit":
        print(per.sort_values("oracle")[["oracle", "n", "sd_est", "sd_mean", "sd_est_ck", "sd_mean_ck", "shift", "shift_ck", "hm", "hmm"]].round(1).to_string())

print("\n== between-subject r(L,h) ==")
for name, d in (("all", df), ("well_lit", wl), ("well_lit_frontal", front)):
    sm = d.groupby("subject")[["L_full", "h_full", "L_ck", "h_ck", "hmean_full", "Lmean_full"]].mean()
    print(name, "paper full r=%.2f p=%.3f" % stats.pearsonr(sm.L_full, sm.h_full),
          "| cheeks r=%.2f p=%.3f" % stats.pearsonr(sm.L_ck, sm.h_ck),
          "| pixel-mean r=%.2f p=%.3f" % stats.pearsonr(sm.Lmean_full, sm.hmean_full))

print("\n== share h>=55 ==")
for name, d in subsets.items():
    print(name, "paper:", round((d.h_full >= 55).mean(), 3), "cheeks:", round((d.h_ck >= 55).mean(), 3), "pixmean:", round((d.hmean_full >= 55).mean(), 3),
          "L>=60:", round((d.L_full >= 60).mean(), 3))

print("\n== lighting shift (paired subject means, facing/frontal pose only) ==")
fr = df[df.pose.isin(["facing_camera", "frontal"])]
pm = fr.groupby(["subject", "lighting"])[["L_full", "h_full", "hmean_full", "h_ck"]].mean().unstack()
for c in ("L_full", "h_full", "hmean_full", "h_ck"):
    dl = (pm[(c, "poorly_lit")] - pm[(c, "well_lit")]).dropna()
    print(c, "mean=%.1f sd=%.1f min=%.1f max=%.1f n=%d p=%.3f" % (dl.mean(), dl.std(), dl.min(), dl.max(), len(dl), stats.ttest_1samp(dl, 0).pvalue))

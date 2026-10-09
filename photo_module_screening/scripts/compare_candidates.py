"""Screen candidate estimators on MST-E against the proxy-testable criteria
(A2 reliability, A3 tone-group consistency, A5 abstention, lighting shift, tone validity)."""
import sys, json
import numpy as np, pandas as pd
from scipy import stats

SP = sys.argv[1]
base = pd.read_csv(SP + "/mste_proc/scored_merged.csv")
meta = base[["file", "lighting", "mask", "oracle", "pose"]]
ck = pd.read_csv(SP + "/mste_proc/scores_cheeks.csv")[["file", "L_ck", "h_ck"]]
cand = pd.read_csv(SP + "/mste_proc/candidates.csv")
df = cand.merge(meta, on="file").merge(ck, on="file", how="left").merge(base[["file", "L_full", "h_full"]], on="file")
df = df[df["mask"].astype(str) == "0"].copy()
signed = lambda h: np.where(h > 180, h - 360, h)  # skin hue sits in 0-90: put the cut at 180
for c in ("C1", "C2", "C3", "C4"):
    df[f"{c}_h"] = signed(df[f"{c}_h"])
CANDS = {  # name: (L col, C col or None, h col, extra availability gate col)
    "C0 Thong 全脸": ("L_full", None, "h_full", None),
    "C0 Thong 脸颊": ("L_ck", None, "h_ck", None),
    "C1 中位数": ("C1_L", "C1_C", "C1_h", None),
    "C2 稳健+彩度门控": ("C2_L", "C2_C", "C2_h", None),
    "C3 C2+灰度世界白平衡": ("C3_L", "C3_C", "C3_h", None),
    "C4 C2+背景白参照": ("C4_L", "C4_C", "C4_h", "gate4"),
}
grp = lambda m: "MST1-3" if m <= 3 else ("MST4-6" if m <= 6 else "MST7-10")
df["grp"] = df.oracle.map(grp)


def icc1(d, col):
    d = d.dropna(subset=[col]); g = d.groupby("subject")[col]
    k = g.size(); k = k[k >= 2]; d = d[d.subject.isin(k.index)]; g = d.groupby("subject")[col]
    n, N = len(k), k.sum(); gm = d[col].mean()
    msb = (k * (g.mean() - gm) ** 2).sum() / (n - 1)
    msw = ((d[col] - d.subject.map(g.mean())) ** 2).sum() / (N - n)
    k0 = (N - (k ** 2).sum() / N) / (n - 1)
    sb2 = max((msb - msw) / k0, 0)
    return (msb - msw) / (msb + (k0 - 1) * msw), np.sqrt(msw), np.sqrt(sb2)


def boot(d, col, B=1000, seed=0):
    rng = np.random.default_rng(seed); subs = d.subject.unique(); gs = dict(tuple(d.groupby("subject"))); v = []
    for _ in range(B):
        pick = rng.choice(subs, len(subs))
        v.append(icc1(pd.concat([gs[p].assign(subject=f"{p}_{i}") for i, p in enumerate(pick)]), col)[0])
    return np.percentile(v, [2.5, 97.5])


rows = []
for name, (Lc, Cc, hc, g4) in CANDS.items():
    for gated in (False, True):
        d = df.copy()
        if gated:
            d = d[d.gate.isna()]
            if g4: d = d[d[g4].isna()]
        d = d.dropna(subset=[Lc, hc])
        wl = d[d.lighting == "well_lit"]
        r = {"候选": name, "门控": "是" if gated else "否"}
        for lab, col in (("L", Lc), ("C", Cc), ("h", hc)):
            if col is None:
                r[f"ICC_{lab}"] = r[f"比_{lab}"] = "—"; continue
            icc, sw, sb = icc1(wl, col)
            lo, hi = boot(wl, col)
            r[f"ICC_{lab}"] = f"{icc:.2f} [{lo:.2f},{hi:.2f}]"
            r[f"比_{lab}"] = f"{sw / sb:.2f}" if sb > 0 else "inf"  # sigma_e / sigma_b, target <= 0.5
        sd = wl.groupby("subject").agg(sd=(hc, "std"), grp=("grp", "first"), o=("oracle", "first"))
        gsd = sd.groupby("grp").sd.mean()
        r["h人内SD 1-3/4-6/7-10"] = "/".join(f"{gsd.get(k, np.nan):.1f}" for k in ("MST1-3", "MST4-6", "MST7-10"))
        r["组间比"] = f"{gsd.max() / gsd.min():.2f}"
        r["ρ(人内SD,MST)"] = f"{stats.spearmanr(sd.o, sd.sd).statistic:.2f}"
        pm = d.groupby(["subject", "lighting"])[[Lc, hc]].mean().unstack()
        r["光照|ΔL|中位"] = f"{(pm[(Lc, 'poorly_lit')] - pm[(Lc, 'well_lit')]).abs().median():.1f}"
        r["光照|Δh|中位"] = f"{(pm[(hc, 'poorly_lit')] - pm[(hc, 'well_lit')]).abs().median():.1f}"
        sm = wl.groupby("subject").agg(L=(Lc, "mean"), o=("oracle", "first"))
        r["ρ(L,MST)"] = f"{stats.spearmanr(sm.o, sm.L).statistic:.2f}"
        n_all = (df["mask"].astype(str) == "0").sum()
        r["保留率 良光/差光"] = f"{len(wl) / (df.lighting == 'well_lit').sum():.0%}/{len(d[d.lighting == 'poorly_lit']) / (df.lighting == 'poorly_lit').sum():.0%}"
        keep = d.groupby("grp").size() / df.groupby("grp").size()
        r["保留率 按组"] = "/".join(f"{keep.get(k, 0):.0%}" for k in ("MST1-3", "MST4-6", "MST7-10"))
        r["h人间SD"] = f"{wl.groupby('subject')[hc].mean().std():.1f}"
        rows.append(r)
out = pd.DataFrame(rows)
out.to_csv(SP + "/mste_proc/candidate_comparison.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(out.to_string(index=False))

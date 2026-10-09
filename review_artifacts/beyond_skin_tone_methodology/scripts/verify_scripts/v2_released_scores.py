"""Analyse the authors' released per-image scores (CFD, CelebA, FFHQ) in memory; writes nothing.
Checks: Table 1 reproduction, threshold sweeps (K04/K05), L-h association (K10), negative/out-of-range hue (K08),
CFD hue by ethnicity and position confound in the cropping design (K11), CFD/CFD-India source."""
import io, itertools as it, urllib.request
import numpy as np, pandas as pd
from scipy import stats

BASE = "https://raw.githubusercontent.com/SonyResearch/apparent_skincolor/main/"
get = lambda p: pd.read_csv(io.BytesIO(urllib.request.urlopen(BASE + p).read()), index_col=0)
S = {k: get(f"extract/results/{k}.csv") for k in ("CFD", "CelebA", "FFHQ")}
meta = get("cropping/cfd_meta.csv")

print("== reproduce Table 1 / CFD 2x2 (L>=60 light, h>=55 yellow) ==")
for k, d in S.items():
    L, h = d.lum, d.hue
    t = pd.crosstab(np.where(h >= 55, "Y", "R"), np.where(L >= 60, "Light", "Dark"), normalize=True) * 100
    print(k, len(d), "\n", t.round(2).to_string())
    print(f"  h<0: {(h < 0).mean() * 100:.2f}%  h>90: {(h > 90).mean() * 100:.2f}%  |h-55|<3: {(abs(h - 55) < 3).mean() * 100:.1f}%  |L-60|<3: {(abs(L - 60) < 3).mean() * 100:.1f}%")
    print(f"  median h={h.median():.1f} IQR=[{h.quantile(.25):.1f},{h.quantile(.75):.1f}]  median L={L.median():.1f}")
    print(f"  Spearman(L,h)={stats.spearmanr(L, h)[0]:+.3f}  Pearson={stats.pearsonr(L, h)[0]:+.3f}")
    sweep = {c: round((h >= c).mean() * 100, 1) for c in (40, 45, 50, 55, 60, 65)}
    print("  %yellow at h cut:", sweep)
    sweepL = {c: round((L >= c).mean() * 100, 1) for c in (50, 55, 60, 65, 70)}
    print("  %light at L cut:", sweepL)
    print("  hue_std (within-image pixel spread of selected clusters) median:", round(d.hue_std.median(), 2))

print("\n== CFD: hue by self-reported ethnicity ==")
c = S["CFD"].join(meta[["EthnicitySelf", "GenderSelf"]], how="inner")
print("merged", len(c))
print(c.groupby("EthnicitySelf")[["lum", "hue"]].agg(["mean", "std", "count"]).round(1).to_string())
c["src"] = np.where(c.EthnicitySelf == "I", "CFD-India", "CFD")
c["tone"] = np.where(c.lum >= 60, "L", "D"); c["hueg"] = np.where(c.hue >= 55, "Y", "R")
print(pd.crosstab([c.tone, c.hueg], c.EthnicitySelf, margins=True).to_string())
# variance of hue explained by ethnicity
m = stats.f_oneway(*[g.hue.values for _, g in c.groupby("EthnicitySelf")])
eta2 = 1 - ((c.hue - c.groupby("EthnicitySelf").hue.transform("mean")) ** 2).sum() / ((c.hue - c.hue.mean()) ** 2).sum()
print(f"ANOVA hue~ethnicity F={m.statistic:.1f} p={m.pvalue:.1e} eta2={eta2:.2f}")

print("\n== cropping design: top-position share by group (from released generate.py logic) ==")
prod = list(it.product(["W", "B", "A", "I", "L"], ["F", "M"])); comb = list(it.combinations(prod, 2))
topn = {g: 0 for g in prod}
for a, b in comb:
    topn[a] += 1
c["top_share"] = [topn[(e, g)] / 9 for e, g in zip(c.EthnicitySelf, c.GenderSelf)]
c["games"] = c.groupby(["EthnicitySelf", "GenderSelf"]).lum.transform(lambda s: 4500 / len(s))
for col in ("tone", "hueg"):
    print(col, c.groupby(col)[["top_share", "games"]].mean().round(3).to_string())
c["cell"] = c.tone + c.hueg
print(c.groupby("cell")[["top_share", "games"]].mean().round(3).to_string())
print("n by cell:", c.cell.value_counts().to_dict())

"""Reconstruct Table 3 cell counts from the unique cell sizes LR=387, LY=328,
DR=161, DY=124 (N=1000 pairs) and test every reported percentage."""
from fractions import Fraction as F
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint
n = {"LR": 387, "LY": 328, "DR": 161, "DY": 124}
T = {"ArcFace": [95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77],
     "FaceNet": [94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16],
     "Dlib":    [94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74]}
COLS = ["overall", "light", "dark", "red", "yellow", "LR", "LY", "DR", "DY"]
def rnd(k, m): return float(round(F(100 * k, m), 2))
for m, v in T.items():
    k = {}
    for c in ("LR", "LY", "DR", "DY"):
        r = v[COLS.index(c)]
        cands = [x for x in range(n[c] + 1) if abs(F(100 * x, n[c]) - F(str(r))) <= F(1, 200)]
        best = cands[0] if cands else min(range(n[c] + 1), key=lambda x: abs(100 * x / n[c] - r))
        k[c] = best
        if not cands:
            print(f"{m} {c}: reported {r} unreachable with n={n[c]}; nearest {best}/{n[c]}={100*best/n[c]:.4f}")
    agg = {"overall": (sum(k.values()), 1000), "light": (k["LR"] + k["LY"], 715), "dark": (k["DR"] + k["DY"], 285),
           "red": (k["LR"] + k["DR"], 548), "yellow": (k["LY"] + k["DY"], 452)}
    for c, (kk, nn) in agg.items():
        rep = v[COLS.index(c)]
        flag = "OK" if rnd(kk, nn) == rep else f"MISMATCH (reported {rep})"
        print(f"{m:8s} {c:8s} {kk}/{nn} = {100*kk/nn:.3f}  {flag}")
    for a, b in (("light", "dark"), ("red", "yellow")):
        (ka, na), (kb, nb) = agg[a], agg[b]
        p = fisher_exact([[ka, na - ka], [kb, nb - kb]]).pvalue
        ca = proportion_confint(ka, na, method="wilson"); cb = proportion_confint(kb, nb, method="wilson")
        print(f"   {a} vs {b}: {100*ka/na:.2f} [{100*ca[0]:.1f},{100*ca[1]:.1f}] vs {100*kb/nb:.2f} [{100*cb[0]:.1f},{100*cb[1]:.1f}]  diff={100*(ka/na-kb/nb):+.2f}pp Fisher p={p:.3f}")
    ks = sorted(((k[c] / n[c], c) for c in n)); lo, hi = ks[0][1], ks[-1][1]
    p = fisher_exact([[k[hi], n[hi] - k[hi]], [k[lo], n[lo] - k[lo]]]).pvalue
    print(f"   largest intersectional gap {hi} vs {lo}: Fisher p={p:.3f}")

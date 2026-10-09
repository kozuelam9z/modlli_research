"""V4 independent re-derivation of Table 3 (LFW) cell sizes, swap check, tests, power.
Run: venv/bin/python v4_table3.py"""
import math
from scipy.stats import fisher_exact, norm
from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

T3 = {"ArcFace": (95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77),
      "FaceNet": (94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16),
      "Dlib":    (94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74)}
TOL = 0.005 + 1e-9
def ks(n, a): return [k for k in range(n + 1) if abs(100 * k / n - a) <= TOL] if n > 0 else []

def search(model, N, use_hue_margins=True, use_cells=True):
    """All (nL, nR, nLR) with every printed value attainable and counts additive."""
    tot, aL, aD, aR, aY, aLR, aLY, aDR, aDY = T3[model]
    out = []
    for kt in ks(N, tot):
        tone = [(nL, kL) for nL in range(1, N) for kL in ks(nL, aL) if (kt - kL) in ks(N - nL, aD)]
        hue = [(nR, kR) for nR in range(1, N) for kR in ks(nR, aR) if (kt - kR) in ks(N - nR, aY)] if use_hue_margins else None
        if not use_cells:
            out += [(N, t, hue) for t in tone]; continue
        nRs = sorted({h[0] for h in hue}) if use_hue_margins else range(1, N)
        for nL, kL in tone:
            for nR in nRs:
                for nLR in range(max(1, nL + nR - N + 1), min(nL, nR)):
                    nLY, nDR, nDY = nL - nLR, nR - nLR, N - nL - nR + nLR
                    if min(nLY, nDR, nDY) <= 0: continue
                    for kLR in ks(nLR, aLR):
                        for kLY in ks(nLY, aLY):
                            if kLR + kLY != kL: continue
                            for kDR in ks(nDR, aDR):
                                kDY = kt - kL - kDR
                                if kDY not in ks(nDY, aDY): continue
                                kR = kLR + kDR
                                if use_hue_margins and (kR not in ks(nR, aR) or (kt - kR) not in ks(N - nR, aY)): continue
                                out.append((N, nL, nR, nLR, nLY, nDR, nDY, kLR, kLY, kDR, kDY))
    return out

print("== Full joint search at N=1000 (tone margins + hue margins + 4 cells + additivity) ==")
for m in T3:
    s = search(m, 1000)
    print(m, "solutions:", len(s), s[:3])
print("\n== ArcFace without its printed hue margins (cells + tone only), N=1000 ==")
s = search("ArcFace", 1000, use_hue_margins=False)
cfg = sorted({x[1:7] for x in s}); print("cell-size configs:", cfg[:5], "n=", len(cfg))
for x in s[:3]:
    N, nL, nR, nLR, nLY, nDR, nDY, kLR, kLY, kDR, kDY = x
    print(f"  implied red={100*(kLR+kDR)/nR:.2f} yellow={100*(kLY+kDY)/(N-nR):.2f}")
print("\n== Strongest rebuttal: ArcFace evaluated on N<1000 (detection drop)? full joint search ==")
for N in range(990, 1000):
    s = search("ArcFace", N)
    if s: print("N", N, "feasible:", s[:2])
print("(no output above => no N in 990..999 reproduces all nine ArcFace values)")

print("\n== FaceNet L+Y=93.30 attainable at n=328? ", ks(328, 93.30), " 306/328 =", round(100*306/328, 4))

C = {"ArcFace": dict(L=(683,715),D=(269,285),R=(521,548),Y=(431,452),LR=(372,387),LY=(311,328),DR=(149,161),DY=(120,124)),
     "FaceNet": dict(L=(676,715),D=(268,285),R=(520,548),Y=(424,452),LR=(370,387),LY=(306,328),DR=(150,161),DY=(118,124)),
     "Dlib":    dict(L=(675,715),D=(267,285),R=(519,548),Y=(423,452),LR=(367,387),LY=(308,328),DR=(152,161),DY=(115,124))}
print("\n== Fisher exact / Newcombe CI on recovered counts (pairs as units) ==")
pmin = 1
for m, c in C.items():
    for a, b in (("L","D"),("R","Y"),("LR","LY"),("DR","DY"),("LR","DR"),("LY","DY"),("LR","DY"),("LY","DR")):
        (k1,n1),(k2,n2) = c[a], c[b]
        p = fisher_exact([[k1,n1-k1],[k2,n2-k2]])[1]; pmin = min(pmin, p)
        lo, hi = confint_proportions_2indep(k1,n1,k2,n2,method="newcomb")
        print(f"{m:8s} {a:2s}-{b:2s} diff={100*(k1/n1-k2/n2):+5.2f}pp CI[{100*lo:+.2f},{100*hi:+.2f}] p={p:.3f}")
print("min p over 24 contrasts:", round(pmin, 3))

print("\n== Sensitivity: if images (2 per pair) were the units (naive doubling, ignores within-pair dependence) ==")
for m, c in C.items():
    for a, b in (("L","D"),("R","Y")):
        (k1,n1),(k2,n2) = c[a], c[b]
        print(m, a, b, "p(doubled)=", round(fisher_exact([[2*k1,2*(n1-k1)],[2*k2,2*(n2-k2)]])[1], 3))

print("\n== Minimum detectable difference (two-sided alpha=.05, power=.80), baseline p=0.95 ==")
pw = NormalIndPower()
def mdd(n1, n2, p_hi=0.95):
    for d in [x/1000 for x in range(1, 300)]:
        es = proportion_effectsize(p_hi, p_hi - d)
        if pw.power(es, nobs1=n1, alpha=0.05, ratio=n2/n1) >= 0.8: return d
for lab, n1, n2 in (("Light/Dark", 715, 285), ("Red/Yellow", 548, 452), ("LR/DY", 387, 124), ("DR/DY", 161, 124)):
    print(f"{lab}: MDD = {100*mdd(n1,n2):.1f} pp  (Wald approx {100*2.8*math.sqrt(.05*.95/n1+.06*.94/n2):.1f})")
print("n per group (equal) for 80% power to detect 95% vs 94%:",
      math.ceil(pw.solve_power(proportion_effectsize(.95,.94), alpha=.05, power=.8)))
print("Observed-gap power: ArcFace tone (95.52 vs 94.39):",
      round(pw.power(proportion_effectsize(.9552,.9439), nobs1=715, alpha=.05, ratio=285/715), 3))

print("\n== FaceNet with L+Y relaxed to 93.29 (rounding-slip hypothesis) ==")
T3["FaceNet"] = (94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.29, 93.17, 95.16)
print("FaceNet solutions:", search("FaceNet", 1000))
print("\n== Tone split alone (any N=1000 nL with margins attainable) per model ==")
for m in T3:
    s = search(m, 1000, use_hue_margins=False, use_cells=False)
    print(m, sorted({x[1][0] for x in s}))

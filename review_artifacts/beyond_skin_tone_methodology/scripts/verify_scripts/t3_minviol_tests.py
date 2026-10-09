"""V3: (a) shared cell sizes at N=1000: for every (nLR,nLY,nDR,nDY) with nL=715 AND for every nL,
minimum number of printed Table-3 values that cannot be reproduced (choosing k per model freely);
(b) ArcFace no-swap vs swap residuals at the recovered sizes; (c) Fisher/Wilson/MDE.
Run with the venv python (scipy, statsmodels)."""
from fractions import Fraction as F
from itertools import product
T = {"ArcFace": [95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77],
     "FaceNet": [94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16],
     "Dlib":    [94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74]}
TOL = 0.005 + 1e-9  # float check; exact Fraction check below for reported residuals
ok = lambda k, n, r: n > 0 and abs(100 * k / n - r) <= TOL


def viol(n4, v):
    """min violations over k choices (each cell k within +-2 of nearest)."""
    nLR, nLY, nDR, nDY = n4
    best = 99
    cands = []
    for n, r in zip(n4, v[5:]):
        k0 = int(r * n / 100)
        cands.append([k for k in (k0, k0 + 1) if 0 <= k <= n])  # floor/ceil: covers any attainable k
    for kLR, kLY, kDR, kDY in product(*cands):
        bad = (not ok(kLR + kLY + kDR + kDY, 1000, v[0])) + (not ok(kLR + kLY, nLR + nLY, v[1])) \
            + (not ok(kDR + kDY, nDR + nDY, v[2])) + (not ok(kLR + kDR, nLR + nDR, v[3])) \
            + (not ok(kLY + kDY, nLY + nDY, v[4])) + (not ok(kLR, nLR, v[5])) + (not ok(kLY, nLY, v[6])) \
            + (not ok(kDR, nDR, v[7])) + (not ok(kDY, nDY, v[8]))
        best = min(best, bad)
        if best == 0:
            break
    return best


# (a1) tone split: which nL make Light, Dark, Overall jointly reproducible for all 3 models?
tone = []
for nL in range(1, 1000):
    good = True
    for v in T.values():
        kt = round(v[0] * 10)
        if not any(ok(kL, nL, v[1]) and ok(kt - kL, 1000 - nL, v[2]) for kL in range(nL + 1)):
            good = False
            break
    if good:
        tone.append(nL)
print("(a1) nL consistent for all 3 models (N=1000):", tone)
# hue split alone, ignoring ArcFace hue
hue = []
for nR in range(1, 1000):
    if all(any(ok(kR, nR, v[3]) and ok(round(v[0] * 10) - kR, 1000 - nR, v[4]) for kR in range(nR + 1))
           for m, v in T.items() if m != "ArcFace"):
        hue.append(nR)
print("(a1) nR consistent for FaceNet+Dlib (N=1000):", hue)

# (a2) nL=715 fixed, scan all cell tuples; total violations across 3 models
res = []
for nLR in range(1, 715):
    for nDR in range(1, 285):
        n4 = (nLR, 715 - nLR, nDR, 285 - nDR)
        tv = 0
        for v in T.values():
            tv += viol(n4, v)
            if tv > 4:
                break
        if tv <= 4:
            res.append((tv, n4))
res.sort()
print("(a2) nL=715: tuples with <=4 total violations:", res[:10])

# (b) residuals at recovered sizes
n4 = (387, 328, 161, 124)
for m, v in T.items():
    ks = [round(r * n / 100) for n, r in zip(n4, v[5:])]
    R, Y = F(100 * (ks[0] + ks[2]), 548), F(100 * (ks[1] + ks[3]), 452)
    print(f"(b) {m}: k={ks} -> red {float(R):.4f} yellow {float(Y):.4f}; printed R {v[3]} Y {v[4]};"
          f" cell checks {[ok(k, n, r) for k, n, r in zip(ks, n4, v[5:])]}")
print("(b) ArcFace attainable red(n=548) near 95.36:", [round(100 * k / 548, 3) for k in (522, 523)],
      " yellow(n=452) near 95.07:", [round(100 * k / 452, 3) for k in (429, 430)],
      " yellow(n=452) near 95.36:", [round(100 * k / 452, 3) for k in (431, 432)])

# (c) inference with recovered counts (ArcFace hue swap-corrected)
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint
from itertools import combinations
cells = {}
for m, v in T.items():
    ks = [round(r * n / 100) for n, r in zip(n4, v[5:])]
    c = dict(zip(["LR", "LY", "DR", "DY"], zip(ks, n4)))
    c["L"] = (ks[0] + ks[1], 715); c["D"] = (ks[2] + ks[3], 285)
    c["R"] = (ks[0] + ks[2], 548); c["Y"] = (ks[1] + ks[3], 452)
    cells[m] = c
allp = []
for m, c in cells.items():
    for a, b in [("L", "D"), ("R", "Y")] + list(combinations(["LR", "LY", "DR", "DY"], 2)):
        (k1, n1), (k2, n2) = c[a], c[b]
        p = fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1]
        allp.append((round(p, 3), m, a, b, round(100 * (k1 / n1 - k2 / n2), 2)))
        if a in "LR" and len(a) == 1:
            w1, w2 = proportion_confint(k1, n1, method="wilson"), proportion_confint(k2, n2, method="wilson")
            print(f"(c) {m} {a} {100*k1/n1:.2f} [{100*w1[0]:.1f},{100*w1[1]:.1f}] vs {b} {100*k2/n2:.2f} "
                  f"[{100*w2[0]:.1f},{100*w2[1]:.1f}] diff {100*(k1/n1-k2/n2):+.2f}pp Fisher p={p:.3f}")
allp.sort()
print("(c) smallest p over 24 contrasts:", allp[:4])
print("(c) min marginal p:", min(x for x in allp if len(x[2]) == 1))
z = 1.959964 + 0.841621
for a, b, n1, n2 in (("L", "D", 715, 285), ("R", "Y", 548, 452)):
    p = 0.945
    print(f"(c) MDE {a} vs {b} (p~{p}, 80% power, a=.05): {100*z*(p*(1-p)*(1/n1+1/n2))**0.5:.2f} pp")

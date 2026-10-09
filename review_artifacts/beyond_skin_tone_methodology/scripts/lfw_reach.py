"""Reachability check for Table 3 (LFW face verification): which subgroup sizes n
make every reported 2-decimal accuracy an attainable k/n, and do the subgroups
partition the 1,000 test pairs (or 2,000 images) with correct-count totals
matching the Overall column? Exact rational arithmetic; a value is 'reachable'
if some integer k gives 100*k/n inside the half-width-0.005 rounding interval."""
from fractions import Fraction as F

T = {  # model: overall, light, dark, red, yellow, LR, LY, DR, DY
    "ArcFace": [95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77],
    "FaceNet": [94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16],
    "Dlib":    [94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74],
}
COLS = ["overall", "light", "dark", "red", "yellow", "LR", "LY", "DR", "DY"]


def ks(r, n):
    lo, hi = F(str(r)) - F(1, 200), F(str(r)) + F(1, 200)
    return [k for k in range(n + 1) if lo <= F(100 * k, n) <= hi]


def feasible(col, N):
    out = {}
    for n in range(1, N + 1):
        per = [ks(T[m][COLS.index(col)], n) for m in T]
        if all(per):
            out[n] = per
    return out


for N in (1000, 2000):
    print(f"=== total units N={N}")
    tot = {m: ks(T[m][0], N) for m in T}
    print("overall correct counts:", tot)
    for a, b in (("light", "dark"), ("red", "yellow")):
        fa, fb = feasible(a, N), feasible(b, N)
        sols = []
        for na, pa in fa.items():
            nb = N - na
            if nb not in fb:
                continue
            ok = all(any(ka + kb in tot[m] for ka in pa[i] for kb in fb[nb][i]) for i, m in enumerate(T))
            if ok:
                sols.append((na, nb))
        print(f"{a}/{b}: {len(sols)} feasible splits;", sols[:12], "..." if len(sols) > 12 else "")
    for c in ("LR", "LY", "DR", "DY"):
        fc = feasible(c, N)
        print(c, "smallest feasible n:", sorted(fc)[:10])

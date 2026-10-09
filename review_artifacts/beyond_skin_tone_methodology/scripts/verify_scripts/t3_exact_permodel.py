"""V3 independent check of Table 3 (re-transcribed from pg_p6.png).
Per model, with NO cross-model constraint and NO fixed N: find every cell-size tuple
(nLR,nLY,nDR,nDY), N=sum<=NMAX, and integer correct counts such that all 9 printed values
are reproduced. Tests the 'model-specific denominator' alternative to the ArcFace swap.
mode 'round': |100k/n - r| <= 0.005 ; mode 'trunc': r <= 100k/n < r+0.01 (truncation)."""
import sys
from fractions import Fraction as F
T = {"ArcFace": [95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77],
     "FaceNet": [94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16],
     "Dlib":    [94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74]}
C = ["all", "L", "D", "R", "Y", "LR", "LY", "DR", "DY"]
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
MODE = sys.argv[2] if len(sys.argv) > 2 else "round"
SWAP = len(sys.argv) > 3 and sys.argv[3] == "swap"


def ok(k, n, r):
    x, r = F(100 * k, n), F(str(r))
    return abs(x - r) <= F(1, 200) if MODE == "round" else r <= x < r + F(1, 100)


def feas(r):
    out = []
    for n in range(1, NMAX + 1):
        k0 = int(r * n / 100)
        out += [(n, k) for k in (k0 - 1, k0, k0 + 1, k0 + 2) if 0 <= k <= n and ok(k, n, r)]
    return out


for m, v in T.items():
    v = dict(zip(C, v))
    if SWAP and m == "ArcFace":
        v["R"], v["Y"] = v["Y"], v["R"]
    f = {c: feas(v[c]) for c in ("LR", "LY", "DR", "DY")}
    light = [(a, b) for a in f["LR"] for b in f["LY"] if a[0] + b[0] < NMAX and ok(a[1] + b[1], a[0] + b[0], v["L"])]
    dark = [(a, b) for a in f["DR"] for b in f["DY"] if a[0] + b[0] < NMAX and ok(a[1] + b[1], a[0] + b[0], v["D"])]
    sols = set()
    for (lr, ly) in light:
        for (dr, dy) in dark:
            N = lr[0] + ly[0] + dr[0] + dy[0]
            if N > NMAX:
                continue
            if not ok(lr[1] + dr[1], lr[0] + dr[0], v["R"]):
                continue
            if not ok(ly[1] + dy[1], ly[0] + dy[0], v["Y"]):
                continue
            if not ok(lr[1] + ly[1] + dr[1] + dy[1], N, v["all"]):
                continue
            sols.add((N, lr[0], ly[0], dr[0], dy[0]))
    sols = sorted(sols)
    print(f"{m} mode={MODE} swap={SWAP} NMAX={NMAX}: {len(sols)} exact cell-size solutions;",
          "N range", (sols[0][0], sols[-1][0]) if sols else None)
    near = [s for s in sols if s[0] >= 900]
    print("   solutions with N>=900:", near[:15], "..." if len(near) > 15 else "")

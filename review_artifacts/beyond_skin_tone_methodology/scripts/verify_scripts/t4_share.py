"""V3: Table 4 constant-share check with interval arithmetic (each printed value +-0.005).
share = (All - Neg)/(Pos - Neg) must be identical across columns (same 30,000 images, labels fixed)."""
from itertools import product
cols = ["recon", "+light", "+dark", "+red", "+yellow"]
G = {"AWS": [(99.67, 94.82, 97.88), (99.84, 90.66, 96.45), (98.84, 97.73, 98.27), (99.69, 94.88, 97.92), (99.63, 94.56, 97.76)],
     "Azure": [(99.78, 95.80, 98.31), (99.91, 92.59, 97.22), (99.11, 97.72, 98.60), (99.75, 96.01, 98.37), (99.78, 95.45, 98.18)],
     "Clarifai": [(95.31, 85.94, 91.85), (96.04, 80.14, 90.18), (93.04, 92.20, 92.73), (94.72, 86.52, 91.70), (96.02, 84.53, 91.79)],
     "FairFace": [(99.49, 92.91, 97.06), (99.77, 87.56, 95.27), (98.21, 96.57, 97.61), (99.52, 93.10, 96.97), (99.42, 92.77, 97.16)]}
S = {"AWS": [(92.80, 93.66, 93.26), (94.22, 91.58, 92.82), (88.80, 96.02, 92.63), (96.88, 86.38, 91.32), (87.97, 96.70, 92.60)],
     "Azure": [(97.29, 80.84, 88.57), (98.13, 76.36, 86.60), (95.59, 86.11, 90.57), (99.00, 69.76, 83.51), (95.18, 87.22, 90.97)]}


def iv(p, n, a):
    vals = [(A - N) / (P - N) for P, N, A in product(*[(x - .005, x + .005) for x in (p, n, a)])]
    return min(vals), max(vals)


for name, T in (("gender: female share", G), ("smile: smiling share", S)):
    print("==", name)
    lo_all, hi_all = 0, 1
    for m, rows in T.items():
        line = []
        for c, (p, n, a) in zip(cols, rows):
            lo, hi = iv(p, n, a)
            line.append(f"{c} {(a-n)/(p-n):.4f}[{lo:.3f},{hi:.3f}]")
            if not (name.startswith("gender") and (m, c) in {("AWS", "+dark"), ("FairFace", "+red"), ("FairFace", "+yellow")}):
                lo_all, hi_all = max(lo_all, lo), min(hi_all, hi)
        print(m, "; ".join(line))
    print(f"common share interval (excluding flagged cells): [{lo_all:.4f}, {hi_all:.4f}]")
    if name.startswith("gender"):
        f0, f1 = lo_all, hi_all
        imp = lambda p, n: (f0 * p + (1 - f0) * n, f1 * p + (1 - f1) * n)
        print("AWS +dark implied All:", ["%.3f" % x for x in imp(98.84, 97.73)], "printed 98.27;",
              "M needed if F,All right: %.2f-%.2f" % ((98.27 - f1 * 98.84) / (1 - f1), (98.27 - f0 * 98.84) / (1 - f0)),
              "F needed if M,All right: %.2f-%.2f" % ((98.27 - (1 - f0) * 97.73) / f0, (98.27 - (1 - f1) * 97.73) / f1))
        r, y = imp(99.52, 93.10), imp(99.42, 92.77)
        print("FairFace +red implied All:", ["%.3f" % x for x in r], "printed 96.97 | +yellow implied:", ["%.3f" % x for x in y], "printed 97.16")
        print("  alt (F/M pairs swapped between +red,+yellow): +red(99.42,92.77)->", ["%.3f" % x for x in y],
              "vs printed 96.97; +yellow(99.52,93.10)->", ["%.3f" % x for x in r], "vs printed 97.16")
        print("  FairFace male recon 92.91: +red M printed 93.10 (up); under F/M-swap alt +red M = 92.77 (down)")

"""Exact tests on Table 3 using integer counts recovered by table3_cells.py. Run: python table3_tests.py"""
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import confint_proportions_2indep
C = {  # (k, n) per group; ArcFace hue uses swap-corrected margins (red 521/548, yellow 431/452)
 "ArcFace": dict(L=(683, 715), D=(269, 285), R=(521, 548), Y=(431, 452), LR=(372, 387), LY=(311, 328), DR=(149, 161), DY=(120, 124)),
 "FaceNet": dict(L=(676, 715), D=(268, 285), R=(520, 548), Y=(424, 452), LR=(370, 387), LY=(306, 328), DR=(150, 161), DY=(118, 124)),
 "Dlib":    dict(L=(675, 715), D=(267, 285), R=(519, 548), Y=(423, 452), LR=(367, 387), LY=(308, 328), DR=(152, 161), DY=(115, 124))}
for m, c in C.items():
    assert sum(c[g][0] for g in ("LR", "LY", "DR", "DY")) == c["L"][0] + c["D"][0]
    for a, b in (("L", "D"), ("R", "Y"), ("LR", "DY"), ("DR", "DY"), ("LR", "DR"), ("LY", "DY")):
        (k1, n1), (k2, n2) = c[a], c[b]
        p = fisher_exact([[k1, n1-k1], [k2, n2-k2]])[1]
        lo, hi = confint_proportions_2indep(k1, n1, k2, n2, method="newcomb")
        print(f"{m:8s} {a:2s} {100*k1/n1:6.2f} vs {b:2s} {100*k2/n2:6.2f}: diff={100*(k1/n1-k2/n2):+5.2f}pp 95%CI=[{100*lo:+.2f},{100*hi:+.2f}] Fisher p={p:.2f}")

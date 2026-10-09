"""Empirical multi-shot aggregation on MST-E (well-lit, gated): for each subject draw two
disjoint sets of m images, average each, and compute ICC(1) between the two set-means
across subjects (repeated random draws). Compares with the Spearman-Brown projection."""
import sys
import numpy as np, pandas as pd
sys.argv = ["x", sys.argv[1]]
exec(open(__file__.replace("aggregate_shots.py", "compare_candidates.py")).read().split("rows = []")[0])
wl = df[(df.lighting == "well_lit") & df.gate.isna()]
rng = np.random.default_rng(1)


def icc_two(a, b):  # ICC(1) for two measurements per subject
    x = np.c_[a, b]; n = len(x); gm = x.mean()
    msb = 2 * ((x.mean(1) - gm) ** 2).sum() / (n - 1); msw = ((x - x.mean(1, keepdims=True)) ** 2).sum() / n
    return (msb - msw) / (msb + msw)


for name, col in (("C0 Thong 全脸 h", "h_full"), ("C2 h", "C2_h"), ("C2 L", "C2_L"), ("C2 C", "C2_C"), ("C4 L", "C4_L"), ("C4 C", "C4_C")):
    d = wl.dropna(subset=[col]); d = d[d.gate4.isna()] if col.startswith("C4") else d
    groups = [g[col].to_numpy() for _, g in d.groupby("subject")]
    base = icc1(d, col)[0]
    out = []
    for m in (1, 3, 5, 8):
        vals = []
        for _ in range(300):
            a, b = [], []
            for v in groups:
                if len(v) < 2 * m: continue
                p = rng.permutation(v); a.append(p[:m].mean()); b.append(p[m:2 * m].mean())
            vals.append(icc_two(np.array(a), np.array(b)))
        sb = m * base / (1 + (m - 1) * base)
        out.append(f"m={m}: 实测 {np.median(vals):.2f} [{np.percentile(vals, 5):.2f},{np.percentile(vals, 95):.2f}] / S-B {sb:.2f}")
    need = 4 * (1 - base) / base
    print(f"{name:16s} 单张ICC {base:.2f} | " + " | ".join(out) + f" | S-B 达0.8需 {need:.1f} 张")

"""V3: Table 2 vs Table 1(b) two-proportion z-tests (gen n=10,000 vs FFHQ n=70,000) and Table 1(b) margin check."""
from math import sqrt
from scipy.stats import norm, chisquare
ffhq = dict(LR=52.82, DR=29.06, LY=13.44, DY=4.68)
gen = {"StyleGAN3": dict(LR=53.05, DR=28.71, LY=13.46, DY=4.78), "P2": dict(LR=53.29, DR=30.08, LY=12.01, DY=4.62)}
agg = lambda d: dict(red=d["LR"] + d["DR"], yellow=d["LY"] + d["DY"], light=d["LR"] + d["LY"], dark=d["DR"] + d["DY"], **d)


def z2(p1, n1, p2, n2):
    p = (p1 * n1 + p2 * n2) / (n1 + n2)
    z = (p1 - p2) / sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return z, 2 * norm.sf(abs(z))


F = agg(ffhq)
for m, d in gen.items():
    G = agg(d)
    for k in ("light", "dark", "red", "yellow", "LR", "DY"):
        z, p = z2(G[k] / 100, 10000, F[k] / 100, 70000)
        print(f"{m:9s} {k:6s} gen {G[k]:.2f} vs FFHQ {F[k]:.2f}: diff {G[k]-F[k]:+.2f}pp z={z:+.2f} p={p:.2g}")
    obs = [d[c] * 100 for c in ("LR", "DR", "LY", "DY")]
    exp = [ffhq[c] * 100 for c in ("LR", "DR", "LY", "DY")]
    print(f"{m}: 4-cell GOF vs FFHQ shares p={chisquare(obs, exp).pvalue:.2g} (FFHQ treated as fixed)")
print("Table 1(b) cell sums: red", round(52.82 + 29.06, 2), "yellow", round(13.44 + 4.68, 2),
      "| printed red 81.87 + yellow 18.12 =", round(81.87 + 18.12, 2), "(complementary shares must round to sum 100.00 +-0.01 and cannot both round down)")

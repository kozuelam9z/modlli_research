"""V4: P2/StyleGAN3 vs FFHQ tests (K19) and Table 1(b) integer feasibility (K24). Run: venv/bin/python v4_tables12.py"""
import math, itertools
from scipy.stats import norm, chisquare
FFHQ = dict(LR=52.82, DR=29.06, LY=13.44, DY=4.68, R=81.87, Y=18.12, L=66.26, D=33.74)
GEN = {"StyleGAN3": dict(LR=53.05, DR=28.71, LY=13.46, DY=4.78, R=81.76, Y=18.24, L=66.51, D=33.49),
       "P2":        dict(LR=53.29, DR=30.08, LY=12.01, DY=4.62, R=83.37, Y=16.63, L=65.30, D=34.70)}
nG, nF = 10000, 70000
print("== Generated (n=10k) vs FFHQ: one-sample z (FFHQ as fixed reference) and two-sample pooled z ==")
for g, t in GEN.items():
    for c in ("D", "Y", "LR", "DY"):
        p, p0 = t[c]/100, FFHQ[c]/100
        z1 = (p - p0)/math.sqrt(p0*(1-p0)/nG)
        pp = (p*nG + p0*nF)/(nG+nF); z2 = (p - p0)/math.sqrt(pp*(1-pp)*(1/nG+1/nF))
        print(f"{g:9s} {c:2s} {100*p:6.2f} vs {100*p0:6.2f} diff={100*(p-p0):+5.2f}pp  one-sample z={z1:+5.2f} p={2*norm.sf(abs(z1)):.1e}  two-sample z={z2:+5.2f} p={2*norm.sf(abs(z2)):.1e}")
    obs = [t[c]*nG/100 for c in ("LR","DR","LY","DY")]; exp = [FFHQ[c]*nG/100 for c in ("LR","DR","LY","DY")]
    exp = [e*sum(obs)/sum(exp) for e in exp]
    print(f"{g}: 4-cell GOF chi2 p = {chisquare(obs, exp).pvalue:.2g}")
print("Approx. 'one-sample' 95% half-width at n=10k for p~0.34 and p~0.17:",
      round(196*math.sqrt(.34*.66/1e4), 2), round(196*math.sqrt(.17*.83/1e4), 2), "pp")

print("\n== Table 1(b): integer counts at N=70,000 are NOT unique (0.01% = 7 images) ==")
N = 70000
rng = lambda a: [k for k in range(int((a-0.005)*N/100)-2, int((a+0.005)*N/100)+3) if abs(100*k/N - a) <= 0.005+1e-12]
R = {c: rng(FFHQ[c]) for c in ("LR","DR","LY","DY")}
for c, v in R.items(): print(c, FFHQ[c], "->", v[0], "...", v[-1], f"({len(v)} candidates)")
ok_cells = [x for x in itertools.product(*R.values()) if sum(x) == N]
print("cell 4-tuples summing to 70,000:", len(ok_cells))
red_ok = [x for x in ok_cells if abs(100*(x[0]+x[1])/N - 81.87) <= 0.005]
yel_ok = [x for x in ok_cells if abs(100*(x[2]+x[3])/N - 18.12) <= 0.005]
both = [x for x in red_ok if x in set(yel_ok)]
print("...of which Red margin rounds to 81.87:", len(red_ok), "; Yellow rounds to 18.12:", len(yel_ok), "; BOTH:", len(both))
print("Red 81.87 and Yellow 18.12 jointly attainable with a full partition of 70,000?", bool(both),
      "-> one margin is mis-rounded (or some images unscored); 81.88 is NOT uniquely the 'correct' value")

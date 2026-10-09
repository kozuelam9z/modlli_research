"""V4: Table 4 internal-consistency, single-shift (probit) model of F/M and S/NS changes,
L*-leakage arithmetic for the +red smile effect, McNemar bounds. Run: venv/bin/python v4_table4.py"""
import math
from scipy.stats import norm, binomtest
conds = ["recon", "+light", "+dark", "+red", "+yellow"]
G = {  # (F, M, All) per condition
 "AWS":      [(99.67,94.82,97.88),(99.84,90.66,96.45),(98.84,97.73,98.27),(99.69,94.88,97.92),(99.63,94.56,97.76)],
 "Azure":    [(99.78,95.80,98.31),(99.91,92.59,97.22),(99.11,97.72,98.60),(99.75,96.01,98.37),(99.78,95.45,98.18)],
 "Clarifai": [(95.31,85.94,91.85),(96.04,80.14,90.18),(93.04,92.20,92.73),(94.72,86.52,91.70),(96.02,84.53,91.79)],
 "FairFace": [(99.49,92.91,97.06),(99.77,87.56,95.27),(98.21,96.57,97.61),(99.52,93.10,96.97),(99.42,92.77,97.16)]}
S = {  # (S, NS, All)
 "AWS":   [(92.80,93.66,93.26),(94.22,91.58,92.82),(88.80,96.02,92.63),(96.88,86.38,91.32),(87.97,96.70,92.60)],
 "Azure": [(97.29,80.84,88.57),(98.13,76.36,86.60),(95.59,86.11,90.57),(99.00,69.76,83.51),(95.18,87.22,90.97)]}

def w_int(F, M, A, e=0.005):
    vals = [(a - m) / (f - m) for f in (F-e, F+e) for m in (M-e, M+e) for a in (A-e, A+e)]
    return min(vals), max(vals)
print("== Implied positive-class share w=(All-neg)/(pos-neg), rounding interval ==")
for tab, nm in ((G, "female"), (S, "smiling")):
    for m, rows in tab.items():
        print(f"{nm:8s} {m:9s}", "  ".join(f"{c}:[{w_int(*r)[0]:.3f},{w_int(*r)[1]:.3f}]" for c, r in zip(conds, rows)))
wF = 0.6313
print("\nExpected 'All' at w=0.6313: AWS +dark", round(wF*98.84+(1-wF)*97.73, 2), "(printed 98.27);",
      "FairFace +red", round(wF*99.52+(1-wF)*93.10, 2), "(printed 96.97);",
      "FairFace +yellow", round(wF*99.42+(1-wF)*92.77, 2), "(printed 97.16)")
# Strongest rebuttal: per-condition detection failures change denominators. What female drop share would give w=0.486 (AWS +dark)?
nF, nM = 0.6313*30000, 0.3687*30000
x = nF - 0.486/(1-0.486)*nM
print(f"AWS +dark: to get w=0.486 by dropping females only, need to drop {x:.0f} of {nF:.0f} female images ({100*x/nF:.0f}%)")
print("FairFace +yellow printed All (97.16) EXCEEDS the w-weighted mean (96.97): failures-counted-as-errors can only LOWER All -> swap remains most parsimonious")

print("\n== Equal-variance probit single-shift model: does ONE decision shift explain both classes? ==")
print("delta_pos = z(acc_pos') - z(acc_pos);  delta_neg = z(acc_neg) - z(acc_neg')  (both >0 = shift toward positive class)")
for tab, (pos, neg) in ((G, ("F","M")), (S, ("S","NS"))):
    for m, rows in tab.items():
        P0, N0, _ = rows[0]
        for c, (P1, N1, _) in zip(conds[1:], rows[1:]):
            dp = norm.ppf(P1/100) - norm.ppf(P0/100); dn = norm.ppf(N0/100) - norm.ppf(N1/100)
            d = dn  # predict positive-class accuracy from shift estimated on the (non-ceiling) negative class
            pred = 100*norm.cdf(norm.ppf(P0/100) + d)
            print(f"{m:9s} {c:8s} shift(from {neg})={dn:+.3f}  shift(from {pos})={dp:+.3f}  predicted {pos}={pred:6.2f} observed {pos}={P1:6.2f}")

print("\n== Can L* leakage of the hue edit explain the +red smile effect? (paper's own numbers) ==")
dL_light = (9.82+14.30+5.28)/3; dL_dark = (-13.72-20.65-9.75)/3; dL_red = (2.17+7.62-0.81)/3; dL_yel = (-0.42+2.27+3.77)/3
print(f"mean dL*: +light {dL_light:.2f}, +dark {dL_dark:.2f}, +red {dL_red:.2f} (max 7.62), +yellow {dL_yel:.2f}")
for m in S:
    NS0 = S[m][0][1]; sl_light = (S[m][1][1]-NS0)/dL_light; sl_dark = (S[m][2][1]-NS0)/dL_dark
    obs = S[m][3][1]-NS0
    print(f"{m}: NS slope per +1 L* = {sl_light:.3f} (light) / {sl_dark:.3f} (dark); leakage-predicted dNS(+red) = "
          f"{sl_light*dL_red:+.2f} (mean leak) to {sl_light*7.62:+.2f} (max leak); observed {obs:+.2f}")
for m in G:
    M0 = G[m][0][1]; sl = (G[m][1][1]-M0)/dL_light
    print(f"{m}: male-acc slope per +1 L* = {sl:.3f}; leakage-predicted dM(+red)={sl*dL_red:+.2f}, observed {G[m][3][1]-M0:+.2f}; "
          f"dM(+yellow) predicted {sl*dL_yel:+.2f}, observed {G[m][4][1]-M0:+.2f}")

print("\n== '+red increases male accuracy for all models': size in images and McNemar bounds ==")
nM = round(0.3687*30000)
for m in G:
    d = G[m][3][1]-G[m][0][1]; net = round(d/100*nM)
    # exact McNemar p if discordant b+c = D with b-c = net
    Ds = [D + ((D - net) % 2) for D in (net, 50, 100, 200, 400, 800) if D >= net]
    ps = {D: binomtest((D + net)//2, D, 0.5).pvalue for D in Ds}
    print(f"{m:9s} +{d:.2f}pp ~ net {net} of {nM} males; McNemar p by discordant count D:",
          {D: round(p, 3) for D, p in ps.items()})
print("Sign test on 4/4 models positive under H0 (independent, p=.5): two-sided p =", 2*0.5**4)

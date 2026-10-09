"""Perspective-B arithmetic checks for Thong et al. (apparent skin color). Run: python checks_B.py"""
import math, itertools
import numpy as np
from scipy import stats

def h(t): print("\n=== " + t + " ===")

# ---------- Tables 1-2: margins ----------
h("Tables 1-2 margin consistency")
T = {  # LR, DR, LY, DY, red, yellow, light, dark, N
 "CelebAMask-HQ": (46.95, 19.28, 27.48, 6.29, 66.23, 33.77, 74.43, 25.57, 30000),
 "FFHQ":          (52.82, 29.06, 13.44, 4.68, 81.87, 18.12, 66.26, 33.74, 70000),
 "StyleGAN3":     (53.05, 28.71, 13.46, 4.78, 81.76, 18.24, 66.51, 33.49, 10000),
 "P2":            (53.29, 30.08, 12.01, 4.62, 83.37, 16.63, 65.30, 34.70, 10000),
}
for k, (LR, DR, LY, DY, R, Y, L, D, N) in T.items():
    print(k, "red=%.2f(rep %.2f) yel=%.2f(rep %.2f) light=%.2f(rep %.2f) dark=%.2f(rep %.2f) R+Y=%.2f cells=%.2f counts=%s"
          % (LR+DR, R, LY+DY, Y, LR+LY, L, DR+DY, D, R+Y, LR+DR+LY+DY, [round(c*N/100, 2) for c in (LR, DR, LY, DY)]))
# FFHQ: can red=81.87 and yellow=18.12 both be correctly rounded from complementary shares?
print("FFHQ red in [81.865,81.875) & yellow in [18.115,18.125) -> sum in [99.98,100.00): complementary shares impossible")

h("Generative vs FFHQ: two-proportion z (and one-sample vs FFHQ treated as fixed)")
def z2(p1, n1, p2, n2):
    p = (p1*n1 + p2*n2)/(n1+n2); se = math.sqrt(p*(1-p)*(1/n1+1/n2)); z = (p1-p2)/se
    return z, 2*stats.norm.sf(abs(z))
def z1(p1, n1, p0):
    se = math.sqrt(p0*(1-p0)/n1); z = (p1-p0)/se; return z, 2*stats.norm.sf(abs(z))
F = T["FFHQ"]
for g in ("StyleGAN3", "P2"):
    G = T[g]
    for name, i in (("red", 4), ("dark", 7), ("dark-yellow", 3), ("light-red", 0)):
        zz, pp = z2(G[i]/100, 10000, F[i]/100, 70000); zo, po = z1(G[i]/100, 10000, F[i]/100)
        d = G[i]-F[i]; se = math.sqrt(G[i]/100*(1-G[i]/100)/10000)*100
        print(f"{g:9s} {name:11s} gen={G[i]:.2f} ffhq={F[i]:.2f} diff={d:+.2f}pp 95%CI(one-sample)=[{d-1.96*se:+.2f},{d+1.96*se:+.2f}] z2={zz:+.2f} p={pp:.2g} | z1={zo:+.2f} p={po:.2g}")
    # 4-cell chi-square goodness of fit vs FFHQ cell shares
    obs = np.array([G[0], G[1], G[2], G[3]])*100; exp = np.array([F[0], F[1], F[2], F[3]])/100*10000
    print(f"{g}: chi2 GOF 4 cells vs FFHQ = {stats.chisquare(obs, exp*obs.sum()/exp.sum())}")

h("Tone x hue association (odds ratio, chi2 independence)")
for k, (LR, DR, LY, DY, *_ , N) in T.items():
    tab = np.array([[LR, DR], [LY, DY]])*N/100
    OR = (LR*DY)/(DR*LY); exp_DY = (DR+DY)*(LY+DY)/100
    print(f"{k}: OR(odds red: light vs dark)={OR:.3f}  DY obs={DY:.2f}% vs independence {exp_DY:.2f}%  chi2 p={stats.chi2_contingency(tab)[1]:.2g}")
cfd = np.array([[127, 79], [334, 199]])  # rows red/yellow, cols light/dark (Fig 3c n's)
print("CFD (Fig 3c n's) OR=", (127*199)/(79*334), " chi2 p=", stats.chi2_contingency(cfd)[1])
print("CFD share light in red=%.3f, in yellow=%.3f" % (127/206, 334/533))

# ---------- Elo -> % preference ----------
h("Elo gap implied by reported % preference (M=400)")
for p in (0.6073, 0.5825):
    d = 400*math.log10(p/(1-p)); print(f"p={p}: delta={d:.1f} Elo pts")
# Zero-sum: group means implied if overall mean is 1400
for (n1, n2, d, lab) in ((461, 278, 400*math.log10(.6073/.3927), "light/dark"), (206, 533, 400*math.log10(.5825/.4175), "red/yellow")):
    m1 = 1400 + n2/(n1+n2)*d; m2 = 1400 - n1/(n1+n2)*d
    print(f"{lab}: implied means {m1:.1f} / {m2:.1f}")
# Jensen: mean logistic over heterogeneous ratings vs logistic of mean gap
for sd in (100, 150, 200):
    rng = np.random.default_rng(0); D = rng.normal(400*math.log10(.6073/.3927), math.sqrt(2)*sd, 10**6)
    print(f"within-group SD={sd}: E[P(light beats dark)] over random light-dark pairs = {np.mean(1/(1+10**(-D/400))):.4f} vs logistic(mean gap)=0.6073")

# rough t from boxplot (medians, IQR/1.35 as SD) for the intersectional Bonferroni claim
h("Rough intersectional t-tests read off Fig 3c (medians; SD from IQR/1.349)")
grp = {"LR": (1477, 1348, 1618, 127), "LY": (1405, 1262, 1568, 334), "DR": (1412, 1287, 1508, 79), "DY": (1312, 1220, 1443, 199)}
for a, b in itertools.combinations(grp, 2):
    ma, qa1, qa3, na = grp[a]; mb, qb1, qb3, nb = grp[b]
    sa, sb = (qa3-qa1)/1.349, (qb3-qb1)/1.349
    t, p = stats.ttest_ind_from_stats(ma, sa, na, mb, sb, nb, equal_var=False)
    print(f"{a} vs {b}: diff={ma-mb:+d}  t={t:+.2f}  p={p:.2g}  bonf6={min(1, 6*p):.2g}")

# ---------- CFD games per face ----------
h("Games per face under 45 combos x 500 (each group plays 9x500 = 4500 appearances)")
# CFD per-gender counts recalled from CFD documentation (consistent with paper totals 359F/380M, 109/197/142/108/183)
g = {"AsianF": 57, "AsianM": 52, "BlackF": 104, "BlackM": 93, "LatinoF": 56, "LatinoM": 52,
     "WhiteF": 90, "WhiteM": 93, "IndianF": 52, "IndianM": 90}
assert sum(g.values()) == 739
for k, n in g.items(): print(f"{k:8s} n={n:3d} games/face={4500/n:5.1f}")
print("total appearances", 45*500*2, "mean games/face", 45000/739)

# ---------- Table 3 integer feasibility ----------
h("Table 3: integer feasibility of subgroup accuracies with 1,000 pairs")
T3 = {"ArcFace": (95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77),
      "FaceNet": (94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16),
      "Dlib":    (94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74)}
tol = 0.005 + 1e-9
def ok(k, n, acc): return n > 0 and abs(100*k/n - acc) <= tol
def feasible_split(N, ktot, a1, a2):
    out = set()
    for n1 in range(1, N):
        n2 = N - n1
        for k1 in range(max(0, ktot-n2), min(n1, ktot)+1):
            if ok(k1, n1, a1) and ok(ktot-k1, n2, a2): out.add(n1)
    return out
for N in (1000,):
    for lab, (i1, i2) in (("tone (n_light)", (1, 2)), ("hue (n_red)", (3, 4))):
        sets = {}
        for m, v in T3.items():
            ktot = round(v[0]*N/100); sets[m] = feasible_split(N, ktot, v[i1], v[i2])
            print(f"N={N} {lab} {m}: ktot={ktot}, feasible n = {sorted(sets[m])[:12]}{'...' if len(sets[m])>12 else ''} (count {len(sets[m])})")
        print("  common across models:", sorted(set.intersection(*sets.values())))
# implied weights (continuous)
for m, v in T3.items():
    print(m, "w_light=%.3f w_red=%.3f" % ((v[0]-v[2])/(v[1]-v[2]), (v[0]-v[4])/(v[3]-v[4])))
# CI for light-dark gap at n_light~710
h("Table 3: CIs for subgroup gaps (assuming n_light~710, n_red~545, 1,000 pairs)")
for m, v in T3.items():
    for lab, a1, a2, n1 in (("tone", v[1], v[2], 710), ("hue", v[3], v[4], 545)):
        p1, p2 = a1/100, a2/100; n2 = 1000-n1
        se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2); d = p1-p2
        print(f"{m:8s} {lab}: gap={100*d:+.2f}pp 95%CI=[{100*(d-1.96*se):+.2f},{100*(d+1.96*se):+.2f}] z={d/se:.2f} p={2*stats.norm.sf(abs(d/se)):.2f}  (gap in pairs of smaller group={d*min(n1,n2):.1f})")
print("FaceNet vs Dlib tone gap difference = %.2fpp ~ %.1f pairs of the dark group" % ((94.41-93.68)-(94.55-94.04), ((94.41-93.68)-(94.55-94.04))/100*290))

# ---------- Table 4 consistency (F/M -> All) ----------
h("Table 4a: implied female share w = (All-M)/(F-M) with rounding intervals")
T4a = {"AWS":      [(99.67, 94.82, 97.88), (99.84, 90.66, 96.45), (98.84, 97.73, 98.27), (99.69, 94.88, 97.92), (99.63, 94.56, 97.76)],
       "Azure":    [(99.78, 95.80, 98.31), (99.91, 92.59, 97.22), (99.11, 97.72, 98.60), (99.75, 96.01, 98.37), (99.78, 95.45, 98.18)],
       "Clarifai": [(95.31, 85.94, 91.85), (96.04, 80.14, 90.18), (93.04, 92.20, 92.73), (94.72, 86.52, 91.70), (96.02, 84.53, 91.79)],
       "FairFace": [(99.49, 92.91, 97.06), (99.77, 87.56, 95.27), (98.21, 96.57, 97.61), (99.52, 93.10, 96.97), (99.42, 92.77, 97.16)]}
cols = ["recon", "+light", "+dark", "+red", "+yellow"]
def w_int(F, M, A, e=0.005):
    vals = [(a-m)/(f-m) for f in (F-e, F+e) for m in (M-e, M+e) for a in (A-e, A+e)]
    return min(vals), max(vals)
W = 0.631
for m, rows in T4a.items():
    for c, (F_, M_, A_) in zip(cols, rows):
        lo, hi = w_int(F_, M_, A_); flag = "" if lo <= W <= hi else "  <-- INCONSISTENT"
        print(f"{m:8s} {c:7s} w=[{lo:.3f},{hi:.3f}] expected All at w={W}: {W*F_+(1-W)*M_:.2f} (rep {A_}){flag}")
print("FairFace swap test: +red All if computed = %.2f, +yellow All = %.2f (reported 96.97 / 97.16)" %
      (W*99.52+(1-W)*93.10, W*99.42+(1-W)*92.77))
print("AWS +dark: All implied by F,M = %.2f (rep 98.27); M implied by All,F = %.2f; F implied by All,M = %.2f" %
      (W*98.84+(1-W)*97.73, (98.27-W*98.84)/(1-W), (98.27-(1-W)*97.73)/W))

h("Table 4b: implied smiling share")
T4b = {"AWS": [(92.80, 93.66, 93.26), (94.22, 91.58, 92.82), (88.80, 96.02, 92.63), (96.88, 86.38, 91.32), (87.97, 96.70, 92.60)],
       "Azure": [(97.29, 80.84, 88.57), (98.13, 76.36, 86.60), (95.59, 86.11, 90.57), (99.00, 69.76, 83.51), (95.18, 87.22, 90.97)]}
for m, rows in T4b.items():
    for c, (S, NS, A) in zip(cols, rows):
        lo, hi = w_int(S, NS, A); print(f"{m:6s} {c:7s} w_smile=[{lo:.3f},{hi:.3f}]")

h("Table 4a: smallest male-accuracy changes called 'increase for all models' (+red vs recon)")
nM = round(30000*(1-W))
for m, rows in T4a.items():
    d = rows[3][1]-rows[0][1]; print(f"{m:8s} male +red - recon = {d:+.2f}pp ~ {d/100*nM:+.0f} of ~{nM} male images (net)")

h("Fig 4 off-target shifts relative to reconstructed (3 example faces)")
rec = [(61.92, 46.76), (44.43, 70.19), (72.15, 55.96)]
man = {"+light": [(71.74, 45.76), (58.73, 68.82), (77.43, 55.88)], "+dark": [(48.20, 46.69), (23.78, 73.71), (62.40, 56.84)],
       "+red": [(64.09, 36.76), (52.05, 57.32), (71.34, 42.16)], "+yellow": [(61.50, 55.27), (46.70, 77.13), (75.92, 66.32)],
       "+pale": [(69.56, 47.87), (60.48, 77.55), (80.60, 59.47)], "-pale": [(54.91, 43.54), (27.55, 61.59), (61.40, 51.70)]}
for k, v in man.items():
    print(f"{k:7s} dL*={[round(a[0]-b[0], 2) for a, b in zip(v, rec)]}  dh*={[round(a[1]-b[1], 2) for a, b in zip(v, rec)]}")

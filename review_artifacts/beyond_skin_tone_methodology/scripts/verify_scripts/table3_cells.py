"""Table 3 intersectional integer feasibility. Run: python table3_cells.py"""
T3 = {"ArcFace": (95.20, 95.52, 94.39, 95.36, 95.07, 96.12, 94.82, 92.55, 96.77),
      "FaceNet": (94.40, 94.55, 94.04, 94.89, 93.81, 95.61, 93.30, 93.17, 95.16),
      "Dlib":    (94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74)}
tol = 0.005 + 1e-9
ks = lambda n, a: [k for k in range(n+1) if abs(100*k/n - a) <= tol] if n > 0 else []

# 1) ArcFace hue: any N (pairs evaluated) in 900..1000 and n_red giving all three of overall/red/yellow?
sol = []
for N in range(900, 1001):
    for kt in ks(N, 95.20):
        for nr in range(1, N):
            for kr in ks(nr, 95.36):
                if (N-nr) and abs(100*(kt-kr)/(N-nr) - 95.07) <= tol: sol.append((N, nr, kt, kr))
print("ArcFace hue feasible (N, n_red, k_tot, k_red), N in 900..1000:", sol[:10], "count", len(sol))
print("ArcFace with n_red=548, n_yel=452: red acc options", [round(100*k/548, 2) for k in (522, 523)], "yellow options", [round(100*k/452, 2) for k in (429, 430)])

# 2) intersectional cells with n_L=715, n_R=548, N=1000; free n_LR
for m, v in T3.items():
    tot, aL, aD, aR, aY, aLR, aLY, aDR, aDY = v
    ok = []
    for nLR in range(263, 549):
        nLY, nDR, nDY = 715-nLR, 548-nLR, nLR-263
        if min(nLY, nDR, nDY) <= 0: continue
        for kLR in ks(nLR, aLR):
            for kLY in ks(nLY, aLY):
                for kDR in ks(nDR, aDR):
                    for kDY in ks(nDY, aDY):
                        kL, kD, kR, kY = kLR+kLY, kDR+kDY, kLR+kDR, kLY+kDY
                        if (kL+kD == round(tot*10) and abs(100*kL/715-aL) <= tol and abs(100*kD/285-aD) <= tol):
                            hue_ok = abs(100*kR/548-aR) <= tol and abs(100*kY/452-aY) <= tol
                            ok.append((nLR, nLY, nDR, nDY, hue_ok))
    print(m, "feasible cell sizes (nLR,nLY,nDR,nDY,hue-margins-consistent):", sorted(set(ok))[:8], "count", len(set(ok)))

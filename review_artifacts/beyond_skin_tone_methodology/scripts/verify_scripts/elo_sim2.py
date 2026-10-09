"""Elo shrinkage vs games per face, high-heterogeneity regime (Elo SD ~ paper's boxplots). Run: python elo_sim2.py"""
import numpy as np
rng = np.random.default_rng(2)
sizes = {"AsF": 57, "AsM": 52, "BlF": 104, "BlM": 93, "LaF": 56, "LaM": 52, "WhF": 90, "WhM": 93, "InF": 52, "InM": 90}
grp = np.concatenate([[g]*n for g, n in sizes.items()]); N = len(grp); G = list(sizes)
idx = {g: np.where(grp == g)[0] for g in G}
combos = [(a, b) for i, a in enumerate(G) for b in G[i+1:]]
for tau in (600, 1000):
    theta = rng.normal(0, tau, N)  # no group effects at all
    games = np.array([(i, j) for a, b in combos for i, j in zip(rng.choice(idx[a], 500), rng.choice(idx[b], 500))])
    win = rng.random(len(games)) < 1/(1+10**(-(theta[games[:, 0]]-theta[games[:, 1]])/400))
    R = np.full(N, 1400.)
    for g in rng.permutation(len(games)):
        i, j = games[g]; pi = 1/(1+10**((R[j]-R[i])/400)); s = float(win[g]); R[i] += 16*(s-pi); R[j] -= 16*(s-pi)
    ng = np.bincount(games.ravel(), minlength=N)
    few, many = ng < 55, ng > 75
    b_few = np.polyfit(theta[few], R[few], 1)[0]; b_many = np.polyfit(theta[many], R[many], 1)[0]
    print(f"tau={tau}: Elo SD all={R.std():.0f}; SD few-games(<55, n={few.sum()})={R[few].std():.0f}, many-games(>75, n={many.sum()})={R[many].std():.0f}; "
          f"slope Elo~true: few={b_few:.2f}, many={b_many:.2f}; Elo range {R.min():.0f}-{R.max():.0f}")

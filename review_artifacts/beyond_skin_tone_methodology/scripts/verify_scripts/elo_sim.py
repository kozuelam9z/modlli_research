"""Elo design simulation mimicking the paper's cropping benchmark (739 faces, 10 gender x ethnicity groups,
45 cross-group combos x 500 games, K=16, M=400, init 1400). Run: python elo_sim.py"""
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
sizes = {"AsF": 57, "AsM": 52, "BlF": 104, "BlM": 93, "LaF": 56, "LaM": 52, "WhF": 90, "WhM": 93, "InF": 52, "InM": 90}
p_light = {"As": .9, "Bl": .1, "La": .9, "Wh": .9, "In": .4}
grp = np.concatenate([[g]*n for g, n in sizes.items()]); N = len(grp); G = list(sizes)
idx = {g: np.where(grp == g)[0] for g in G}
combos = [(a, b) for i, a in enumerate(G) for b in G[i+1:]]
assert len(combos) == 45 and N == 739

def run(beta, tau, order="shuffle", reps=1):
    light = np.array([rng.random() < p_light[g[:2]] for g in grp])
    theta = beta*light + rng.normal(0, tau, N)            # true strengths in Elo units
    games = []
    for a, b in combos:
        i = rng.choice(idx[a], 500); j = rng.choice(idx[b], 500)
        top = rng.random(500) < .5                          # position irrelevant here
        games += list(zip(i, j))
    games = np.array(games)
    p = 1/(1+10**(-(theta[games[:, 0]]-theta[games[:, 1]])/400))
    win = rng.random(len(games)) < p                       # True: first wins
    out = []
    for r in range(reps):
        o = np.arange(len(games)) if order == "sorted" else rng.permutation(len(games))
        R = np.full(N, 1400.)
        for g in o:
            i, j = games[g]; pi = 1/(1+10**((R[j]-R[i])/400)); s = 1. if win[g] else 0.
            R[i] += 16*(s-pi); R[j] -= 16*(s-pi)
        out.append(R.copy())
    R = np.array(out)
    gap = R[:, light].mean(1) - R[:, ~light].mean(1)
    implied = 1/(1+10**(-gap/400))
    cross = light[games[:, 0]] != light[games[:, 1]]
    lw = np.where(light[games[:, 0]], win, ~win)[cross]
    true_cross = np.mean(1/(1+10**(-(theta[light][:, None]-theta[~light][None, :])/400)))
    t = stats.ttest_ind(R[0, light], R[0, ~light])
    ngames = np.bincount(games.ravel(), minlength=N)
    return dict(true_gap=theta[light].mean()-theta[~light].mean(), elo_gap=gap.mean(), elo_implied=implied.mean(),
                empirical_cross_winrate=lw.mean(), true_avg_cross_prob=true_cross, t=t.statistic, p=t.pvalue,
                sd_elo=R[0].std(), sd_over_orders=R.std(0).mean() if reps > 1 else np.nan,
                corr_true_elo=np.corrcoef(theta, R[0])[0, 1],
                corr_true_elo_fewgames=np.corrcoef(theta[ngames < 55], R[0][ngames < 55])[0, 1],
                corr_true_elo_manygames=np.corrcoef(theta[ngames > 75], R[0][ngames > 75])[0, 1])

for beta, tau in ((90, 150), (90, 300)):
    r = run(beta, tau, "shuffle", reps=20)
    print(f"beta={beta} tau={tau} shuffled x20:", {k: round(float(v), 3) for k, v in r.items()})
r = run(90, 300, "sorted"); print("beta=90 tau=300 combo-sorted order:", {k: round(float(v), 3) for k, v in r.items()})
# null: no tone effect but ethnicity effect (e.g. model prefers White/Latino/Asian faces for non-skin reasons)
def run_eth(eth_eff, tau):
    global p_light
    return run(0, tau)
eth = {"As": 0, "Bl": -60, "La": 40, "Wh": 60, "In": 0}
light = None
# confounding demo: strength depends on ethnicity only; test 'light vs dark' via Elo
res = []
for s in range(200):
    lt = np.array([rng.random() < p_light[g[:2]] for g in grp])
    theta = np.array([eth[g[:2]] for g in grp]) + rng.normal(0, 150, N)
    res.append(theta[lt].mean() - theta[~lt].mean())
print("ethnicity-only model (no skin-colour effect): mean light-dark true gap =", round(np.mean(res), 1), "Elo pts")

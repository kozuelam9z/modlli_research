"""Is within-image order a cyclic rotation of the sorted values? And does structured order bias the position-based split-half?"""
import os, json, itertools, numpy as np, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
cl = pd.read_csv(os.path.join(OUT, '..', 'annotations_clean.csv'))
def is_rot_sorted(v):
    v = list(v); n = len(v)
    return any(all(v[(s + i) % n] <= v[(s + i + 1) % n] for i in range(n - 1)) for s in range(n))
def is_rot_rev(v):
    return is_rot_sorted(list(v)[::-1])
rng = np.random.default_rng(0)
obs = []; exp = []; obs_r = []; exp_r = []
for _, v in cl.groupby('image').mst_annot:
    v = v.values
    if len(set(v)) < 3:   # need >=3 distinct values for the test to be informative
        continue
    obs.append(is_rot_sorted(v)); obs_r.append(is_rot_rev(v))
    exp.append(np.mean([is_rot_sorted(rng.permutation(v)) for _ in range(200)]))
    exp_r.append(np.mean([is_rot_rev(rng.permutation(v)) for _ in range(200)]))
R = dict(n_images_3plus_distinct=len(obs), rot_sorted_obs=float(np.mean(obs)), rot_sorted_exp_random=float(np.mean(exp)),
         rot_desc_obs=float(np.mean(obs_r)), rot_desc_exp_random=float(np.mean(exp_r)))
# split-half: fixed positions vs random within-image permutations (golden / challenging)
gc = {nm: {s: g.mst_annot.values for s, g in cl[cl[col]].groupby('subject')} for nm, col in [('golden', 'is_golden'), ('chal', 'is_challenging')]}
def sh(d, k, perm=False):
    S = [s for s in d if len(d[s]) == 5]
    rs = []
    for A in itertools.combinations(range(5), k):
        rest = [j for j in range(5) if j not in A]
        for Bc in itertools.combinations(rest, k):
            if A < Bc:
                a = [d[s][list(A)].mean() for s in S]; b = [d[s][list(Bc)].mean() for s in S]
                rs.append(np.corrcoef(a, b)[0, 1])
    return float(np.mean(rs))
for nm, d in gc.items():
    for k in [1, 2]:
        fixed = sh(d, k)
        rnd = np.mean([sh({s: rng.permutation(v) for s, v in d.items()}, k) for _ in range(300)])
        R[f'splithalf_{nm}_k{k}'] = dict(fixed_positions=fixed, random_order_mean=float(rnd))
json.dump(R, open(os.path.join(OUT, 'order2.json'), 'w'), indent=1)
print(json.dumps(R, indent=1))

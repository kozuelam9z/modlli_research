"""Ordinal-logit + OLS-FE subject-cluster bootstrap (spawn-safe: light top level). Run: venv/bin/python -I boot_models.py [B]"""
import json, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel
warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent
SEED = 987654
d = pd.read_csv(OUT.parent / "annotations_clean.csv")
d["sid"] = d.subject.str.replace("subject_", "").astype(int)
d["poorly"] = (d.lighting == "poorly_lit").astype(float)
dM = d[d.lighting.isin(["well_lit", "poorly_lit"])].dropna(subset=["mask", "pose"]).copy()
for q in ["bottom", "frontal", "side"]:
    dM[f"p_{q}"] = (dM.pose == q).astype(float)
dM["mask"] = dM["mask"].astype(float)
XC = ["poorly", "p_bottom", "p_frontal", "p_side", "mask"]
SUBJ = sorted(dM.sid.unique())
def fit_ord(frame, clusters):
    sd = pd.get_dummies(clusters, prefix="s", drop_first=True).astype(float)
    sd.index = frame.index
    X = pd.concat([sd, frame[XC]], axis=1)
    y = pd.Categorical(frame.mst_annot, categories=range(1, 11), ordered=True)
    # drop unobserved categories (OrderedModel needs observed levels)
    y = y.remove_unused_categories()
    m = OrderedModel(y, X, distr="logit")
    r = m.fit(method="bfgs", disp=False, maxiter=2000)
    k = len(y.categories) - 1
    beta = r.params[X.columns]
    th = m.transform_threshold_params(r.params.values[-k:])  # cutpoints incl -inf, inf
    levels = np.array(y.categories, float)
    def EY(Xm):
        eta = Xm.values @ beta.values
        cdf = 1 / (1 + np.exp(-(th[None, :] - eta[:, None])))
        p = np.diff(cdf, axis=1)
        return (p * levels[None, :]).sum(1).mean()
    ame = {}
    for v in XC:
        X1 = X.copy(); X0 = X.copy(); X1[v] = 1.0; X0[v] = 0.0
        if v.startswith("p_"):
            for o in ["p_bottom", "p_frontal", "p_side"]:
                X1[o] = 0.0; X0[o] = 0.0
            X1[v] = 1.0
        ame[v] = EY(X1) - EY(X0)
    spacing = float(np.mean(np.diff(th[1:-1])))
    return dict(beta={v: float(beta[v]) for v in XC}, ame=ame, spacing=spacing, conv=bool(r.mle_retvals.get("converged", True)))

bySubj = {s: dM[dM.sid == s] for s in SUBJ}

def one_boot(seed):
    g = np.random.default_rng(seed)
    pick = g.choice(SUBJ, len(SUBJ))
    parts = []
    for j, s in enumerate(pick):
        p = bySubj[s].copy(); p["clu"] = j; parts.append(p)
    f = pd.concat(parts, ignore_index=True)
    # OLS FE via within-cluster demeaning
    W = f[XC + ["err"]] - f.groupby("clu")[XC + ["err"]].transform("mean")
    b_ols = np.linalg.lstsq(W[XC].values, W["err"].values, rcond=None)[0]
    try:
        o = fit_ord(f, f.clu)
        ordv = [o["beta"][v] for v in XC] + [o["ame"][v] for v in XC] + [float(o["conv"])]
    except Exception:
        ordv = [np.nan] * (2 * len(XC) + 1)
    return list(b_ols) + ordv


if __name__ == "__main__":
    import multiprocessing as mp
    BOOT = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    t0 = time.time()
    with mp.get_context("spawn").Pool(8) as pool:
        res = np.array(pool.map(one_boot, [SEED * 1000 + b for b in range(BOOT)], chunksize=10))
    print("boot secs", time.time() - t0, flush=True)
    k = len(XC)
    def pc(a, lo=2.5, hi=97.5):
        a = a[~np.isnan(a)]; return [float(np.percentile(a, lo)), float(np.percentile(a, hi))]
    M = dict(B=BOOT, ols_fe_bootCI={v: pc(res[:, i]) for i, v in enumerate(XC)}, ols_fe_boot90_poorly=pc(res[:, 0], 5, 95),
             ordinal_beta_bootCI={v: pc(res[:, k + i]) for i, v in enumerate(XC)},
             ordinal_ame_bootCI={v: pc(res[:, 2 * k + i]) for i, v in enumerate(XC)},
             ordinal_ame90_poorly=pc(res[:, 2 * k], 5, 95), ordinal_beta90_poorly=pc(res[:, k], 5, 95),
             ordinal_converged=int(np.nansum(res[:, 3 * k])), n_failed=int(np.isnan(res[:, k]).sum()))
    json.dump(M, open(OUT / "boot_results.json", "w"), indent=1)
    print(json.dumps(M, indent=1))

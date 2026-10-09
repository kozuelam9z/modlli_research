"""Re-score MST-E (full landmark mask) with estimator variants:
seed reliability (same image), n_init=1, atan2 hue, chroma diagnostics,
and hue-of-aggregated-(a,b) over the top-3 clusters."""
import json, sys, csv
import numpy as np, pandas as pd
from PIL import Image
from multiprocessing import Pool
from scipy.ndimage import gaussian_filter
from sklearn.cluster import KMeans

SP = "/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/aa16d469-2438-4934-be22-436934f5e296/scratchpad"
sys.path.insert(0, SP + "/scripts")
from skincolor import face_mask, rgb2lab, mode_left_edge  # reuse replication helpers

keep = set(pd.read_csv(SP + "/mste_proc/scored_merged.csv").file)
d = [r for r in json.load(open(SP + "/mste_proc/landmarks.json")) if r.get("faces") and r["file"] in keep]


def est(L, hue, a, b, seed, n_init, k=5, topk=3):
    lab_ = KMeans(n_clusters=k, random_state=seed, n_init=n_init).fit_predict(np.c_[L, hue])
    lum, hh, n, ids = [], [], [], []
    for c in range(k):
        s = lab_ == c
        if s.sum() < 2:
            continue
        lum.append(mode_left_edge(L[s])); hh.append(mode_left_edge(hue[s])); n.append(s.sum()); ids.append(c)
    lum, hh, n = map(np.array, (lum, hh, n))
    idx = np.argsort(lum)[::-1][:topk]
    sel = np.isin(lab_, np.array(ids)[idx])
    agg = float(np.degrees(np.arctan2(b[sel].mean(), a[sel].mean())))  # hue of mean (a,b) in top-3 clusters
    Csel = float(np.median(np.hypot(a[sel], b[sel])))
    return float(np.average(lum[idx], weights=n[idx])), float(np.average(hh[idx], weights=n[idx])), agg, Csel


def work(r):
    f = max(r["faces"], key=lambda f: f["bbox"][2] * f["bbox"][3])
    m = face_mask(r["w"], r["h"], f, forehead=True)
    if m is None or m.sum() < 500:
        return None
    im = np.asarray(Image.open(SP + "/mste_proc/img/" + r["out"]).convert("RGB")).astype(float) / 255
    sm = gaussian_filter(im, sigma=(1, 1, 0), truncate=4, mode="nearest")
    lab = rgb2lab(sm[m]); L, a, b = lab.T
    h_tan = np.degrees(np.arctan(b / (a + 1e-8)))
    h_at2 = np.degrees(np.arctan2(b, a))
    C = np.hypot(a, b)
    out = {"file": r["file"], "C_med": float(np.median(C)), "frac_a_le0": float((a <= 0).mean()), "frac_C_lt5": float((C < 5).mean())}
    for tag, seed, ninit, hue in (("s1", 1, 10, h_tan), ("s2", 2, 10, h_tan), ("ni1", 2021, 1, h_tan), ("at2", 2021, 10, h_at2)):
        Lx, hx, agg, Cs = est(L, hue, a, b, seed, ninit)
        out.update({f"L_{tag}": Lx, f"h_{tag}": hx})
        if tag == "at2":
            out.update({"h_agg_top3": agg, "C_top3": Cs})
    return out


if __name__ == "__main__":
    with Pool(14) as p:
        res = [x for x in p.map(work, d, chunksize=4) if x]
    print("rescored", len(res))
    from scipy import stats

    def icc1(d, col):  # same one-way ICC(1) as v2_mste_stress.py
        d = d.dropna(subset=[col]); g = d.groupby("subject")[col]; k = g.size(); n = len(k); N = k.sum()
        msb = (k * (g.mean() - d[col].mean()) ** 2).sum() / (n - 1)
        msw = ((d[col] - d.subject.map(g.mean())) ** 2).sum() / (N - n)
        k0 = (N - (k ** 2).sum() / N) / (n - 1)
        return (msb - msw) / (msb + (k0 - 1) * msw), np.sqrt(msw), g.mean().std()
    base = pd.read_csv(SP + "/mste_proc/scored_merged.csv")
    df = base.merge(pd.DataFrame(res), on="file")
    wl = df[df.lighting == "well_lit"]; fr = wl[wl.pose.isin(["facing_camera", "frontal"])]
    print("\n######## RESCORE RESULTS ########")
    # 1. same-image estimator reliability (seed / n_init)
    for c in ("s1", "s2", "ni1"):
        dh = (df[f"h_{c}"] - df.h_full).abs(); dL = (df[f"L_{c}"] - df.L_full).abs()
        flip = ((df[f"h_{c}"] >= 55) != (df.h_full >= 55)).mean(); flipL = ((df[f"L_{c}"] >= 60) != (df.L_full >= 60)).mean()
        print(f"{c} vs seed2021: |dh| median={dh.median():.2f} p95={dh.quantile(.95):.2f} max={dh.max():.1f}; |dL| median={dL.median():.2f} p95={dL.quantile(.95):.2f}; "
              f"hue-cat flip={flip:.3f} tone-cat flip={flipL:.3f}; r_h={df[f'h_{c}'].corr(df.h_full):.3f}")
    # 2. atan2 vs arctan
    diff = df.h_at2 - df.h_full
    print(f"atan2-arctan: images differing>1deg={(diff.abs() > 1).mean():.3f}, mean diff={diff.mean():.2f}, max={diff.max():.1f}; frac_a<=0 median={df.frac_a_le0.median():.4f} p95={df.frac_a_le0.quantile(.95):.3f}")
    print(f"h>=55 share: arctan={(df.h_full >= 55).mean():.3f} atan2={(df.h_at2 >= 55).mean():.3f}; h<0 arctan={(df.h_full < 0).sum()} atan2={(df.h_at2 < 0).sum()}")
    # 3. chroma by MST and relation to hue instability
    per = wl.groupby("subject").agg(oracle=("oracle", "first"), C_med=("C_med", "mean"), C_top3=("C_top3", "mean"),
                                    fCl5=("frac_C_lt5", "mean"), sd_tan=("h_full", "std"), sd_at2=("h_at2", "std"),
                                    sd_agg=("h_agg_top3", "std"), sh_tan=("h_full", "mean"), sh_at2=("h_at2", "mean"),
                                    sh_agg=("h_agg_top3", "mean"), hmean=("hmean_full", "mean"))
    per["grp"] = pd.cut(per.oracle, [0, 3, 6, 10], labels=["1-3", "4-6", "7-10"])
    print(per.groupby("grp", observed=True)[["C_med", "C_top3", "fCl5", "sd_tan", "sd_at2", "sd_agg", "sh_tan", "sh_at2", "sh_agg", "hmean"]].mean().round(2).to_string())
    print(per.sort_values("oracle").round(1).to_string())
    for c in ("C_med", "C_top3", "sd_tan", "sd_at2", "sd_agg", "sh_tan", "sh_at2", "sh_agg"):
        print(f"rho(oracle,{c})=%.2f p=%.3f" % stats.spearmanr(per.oracle, per[c]))
    for name, d in (("well_lit", wl), ("well_lit_frontal", fr), ("all", df)):
        for col in ("h_full", "h_at2", "h_agg_top3"):
            r = icc1(d, col); print(f"ICC {name} {col}: {r[0]:.2f} wSD={r[1]:.1f} bSD={r[2]:.1f}")
    # 4. low-chroma gating: does dropping low-C images restore reliability?
    q = wl.C_top3.quantile(.25)
    r = icc1(wl[wl.C_top3 > q], "h_full"); print(f"ICC well_lit, C_top3>{q:.1f} (top 75%): h_full {r[0]:.2f} wSD={r[1]:.1f}")
    print("corr(|h_full-hmean|, C_top3) within well-lit: rho=%.2f p=%.2g" % stats.spearmanr((wl.h_full - wl.hmean_full).abs(), wl.C_top3))

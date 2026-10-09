"""Supplementary checks: details-CSV row reconciliation, first-run count fit, mixture-vs-beta run order,
lighting-missing labels, golden id check, Fisher CI. Writes supplement.json."""
import os, json, math, itertools
from collections import Counter
import numpy as np, pandas as pd
from scipy import stats, optimize

OUT = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/connielam/Documents/Github/modlli_research/data"; MSTE = f"{DATA}/mst-e_data"
R = {}
raw = pd.read_csv(f"{DATA}/mste_annotations.csv", dtype=str, keep_default_na=False)
raw["mst"] = raw.annotation.str[3:].astype(int)
det = pd.read_csv(f"{MSTE}/mst-e_image_details.csv", dtype=str, keep_default_na=False)
det["id"] = det.image_ID.str.strip()
R["details_rows_by_ext"] = det.id.str.extract(r"\.(\w+)$")[0].fillna("none").value_counts().to_dict()
R["details_rows_total"] = len(det)
R["details_unique_ids_by_ext"] = det.drop_duplicates("id").id.str.extract(r"\.(\w+)$")[0].fillna("none").value_counts().to_dict()
gc = pd.read_csv(f"{MSTE}/golden_and_adversarial_mst-e_image_ids.csv", dtype=str, keep_default_na=False)
R["golden_183259162"] = gc[gc.golden_image_id.str.contains("183259162")].values.tolist()
dd = det.drop_duplicates("id").set_index("id")
light = raw.image.map(dd.lighting)
bad = raw[light.isna() | (light == "video")]
R["labels_with_missing_or_video_lighting"] = [len(bad), bad.image.nunique()]

# folder map
fmap = {f: d for d in os.listdir(MSTE) if d.startswith("subject_") for f in os.listdir(f"{MSTE}/{d}")}
raw["s"] = raw.image.map(fmap)
oracle = det[det.subject_name.str.startswith("subject_")].groupby("subject_name").MST.first().astype(int).to_dict()

groups = [(g.mst.tolist(), g.s.iloc[0]) for _, g in raw.groupby("image", sort=False)]
runs_all = []
for labs, s in groups:
    r = [(k, len(list(g))) for k, g in itertools.groupby(labs)]
    if len(r) > 1: runs_all.append((r, s, len(labs)))

# 1) first-run count vs beta=0 expectation, by count pattern
tab = {}
for r, s, n in runs_all:
    pat = tuple(sorted([c for _, c in r], reverse=True))
    first = r[0][1]
    t = tab.setdefault(pat, {"n": 0, "obs": Counter(), "exp": Counter()})
    t["n"] += 1; t["obs"][first] += 1
    for c in pat: t["exp"][c] += c / n  # P(group first) = c/n, summed over groups with that count
chi = 0; df = 0; rows = []
for pat, t in sorted(tab.items()):
    cats = sorted(set(pat))
    if len(cats) < 2: continue
    o = np.array([t["obs"][c] for c in cats], float); e = np.array([t["exp"][c] for c in cats])
    chi += ((o - e) ** 2 / e).sum(); df += len(cats) - 1
    rows.append({"pattern": pat, "n": t["n"], "obs": dict(zip(cats, o.tolist())), "exp": dict(zip(cats, e.round(2).tolist()))})
R["first_run_count_fit"] = {"chi2": chi, "df": df, "p": float(stats.chi2.sf(chi, df)), "rows": rows}

# 2) run-order models: PL-beta vs mixture (pi: runs sorted ascending by value; else first-appearance beta=0)
def seq_prob(c):  # beta=0 PL prob of observed order
    p = 1.0
    for i in range(len(c) - 1): p *= c[i] / sum(c[i:])
    return p
def asc_prob_under_fa(c, v):
    o = np.argsort(v); return seq_prob([c[i] for i in o])
data = []
for r, s, n in runs_all:
    v = np.array([k for k, _ in r], float); c = [cc for _, cc in r]
    data.append((seq_prob(c), all(np.diff(v) > 0), v - v.mean(), np.array(c, float), s))
def nll_mix(pi):
    return -sum(math.log(pi * a + (1 - pi) * p0) for p0, a, *_ in data)
rm = optimize.minimize_scalar(nll_mix, bounds=(1e-6, 1 - 1e-6), method="bounded")
def nll_beta(b):
    t = 0
    for _, _, v, c, _ in data:
        w = np.log(c) - b * v
        for i in range(len(c) - 1): t -= w[i] - np.logaddexp.reduce(w[i:])
    return t
rb = optimize.minimize_scalar(nll_beta, bounds=(-5, 5), method="bounded")
# mixture where the sorted component is descending too (control)
def nll_mixd(pi):
    return -sum(math.log(pi * float(all(np.diff(v) < 0)) + (1 - pi) * p0) for p0, _, v, *_ in data)
rd = optimize.minimize_scalar(nll_mixd, bounds=(1e-6, 1 - 1e-6), method="bounded")
R["run_order_models"] = {"nll_beta0": nll_beta(0.0), "nll_beta": rb.fun, "beta": rb.x,
                         "nll_mix_asc": rm.fun, "pi_asc": rm.x, "nll_mix_desc": rd.fun, "pi_desc": rd.x}
# per-subject ascending excess
per = {}
for p0, a, v, c, s in data:
    d = per.setdefault(s, [0, 0.0, 0, 0.0, 0])
    d[0] += a; d[1] += asc_prob_under_fa(list(c), v); d[2] += all(np.diff(v) < 0)
    d[3] += asc_prob_under_fa(list(c), -v); d[4] += 1
R["per_subject_asc_obs_exp_desc_obs_exp_n"] = {s: [d[0], round(d[1], 1), d[2], round(d[3], 1), d[4], oracle[s]] for s, d in sorted(per.items())}

# 3) Fisher exact OR CI (4-label vs poorly lit), Woolf approx with 0.5 correction
a, b, c, d = 4, 598, 11, 869
lor = math.log((a + .5) * (d + .5) / ((b + .5) * (c + .5))); se = math.sqrt(sum(1 / (x + .5) for x in (a, b, c, d)))
R["fisher_or_ci_woolf"] = [math.exp(lor - 1.96 * se), math.exp(lor + 1.96 * se)]

# 4) subject-level consensus: exact / off-by-one / signed, for pooled-median rule
sp = raw.groupby("s").mst.median()
diff = {s: float(sp[s] - oracle[s]) for s in sp.index}
R["subject_pooled_median_signed_diff"] = diff
R["subject_pooled_exact"] = sum(v == 0 for v in diff.values())
R["subject_pooled_mean_abs"] = float(np.mean([abs(v) for v in diff.values()]))
R["subject_pooled_mean_signed"] = float(np.mean(list(diff.values())))
# mean label error overall and per-subject mean (unweighted)
raw["err"] = raw.mst - raw.s.map(oracle)
R["mean_err_annotation_weighted"] = float(raw.err.mean())
R["mean_err_subject_unweighted"] = float(raw.groupby("s").err.mean().mean())

def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(conv(R), open(f"{OUT}/supplement.json", "w"), indent=1)
for k, v in conv(R).items(): print(k, ":", json.dumps(v)[:1500])

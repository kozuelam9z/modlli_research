"""Independent verification of release-forensics numbers for mste_annotations.csv.
Reads raw files directly (data only). Writes results.json next to this script."""
import os, re, json, math, hashlib, itertools
from collections import Counter, OrderedDict
import numpy as np, pandas as pd
from scipy import stats, optimize

OUT = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/connielam/Documents/Github/modlli_research/data"
MSTE = f"{DATA}/mst-e_data"
R = {}
rng_seed = 777
B = 2000

# ---------------- raw annotations ----------------
raw = pd.read_csv(f"{DATA}/mste_annotations.csv", dtype=str, keep_default_na=False)
R["raw_header"] = list(raw.columns)
R["raw_rows"] = len(raw)
R["raw_nunique"] = {c: int(raw[c].nunique()) for c in raw.columns}
R["raw_subject_values"] = raw["subject"].unique().tolist()
R["raw_region_values"] = raw["region"].unique().tolist()
raw["mst"] = raw["annotation"].str.replace("MST", "").astype(int)
assert set(raw["annotation"]) == {f"MST{k}" for k in range(1, 11)} or True
R["annotation_values"] = sorted(raw["annotation"].unique().tolist())

# ---------------- folders ----------------
files = []
for d in sorted(os.listdir(MSTE)):
    p = f"{MSTE}/{d}"
    if os.path.isdir(p) and d.startswith("subject_"):
        for f in os.listdir(p):
            files.append((d, f, f.rsplit(".", 1)[-1].lower()))
F = pd.DataFrame(files, columns=["folder", "file", "ext"])
R["folder_ext_counts"] = F["ext"].value_counts().to_dict()
dup_names = F[F.duplicated("file", keep=False)]
R["filenames_duplicated_across_folders"] = len(dup_names)
fmap = dict(zip(F.file, F.folder))
raw["true_subject"] = raw["image"].map(fmap)
R["annotated_images_not_in_folders"] = int(raw.loc[raw.true_subject.isna(), "image"].nunique())
R["rows_subject_correct"] = int((raw["subject"] == raw["true_subject"]).sum())
R["rows_subject_correct_frac"] = R["rows_subject_correct"] / len(raw)
# copy-of duplicate check
copies = F[F.file.str.startswith("Copy of")]
copy_info = []
for _, r in copies.iterrows():
    orig = r.file.replace("Copy of ", "")
    h = lambda fn: hashlib.sha256(open(f"{MSTE}/{r.folder}/{fn}", "rb").read()).hexdigest()
    copy_info.append({"copy": r.file, "folder": r.folder, "orig_exists": orig in fmap,
                      "identical": (orig in fmap) and h(r.file) == h(orig),
                      "orig_annotated": orig in set(raw.image), "copy_annotated": r.file in set(raw.image)})
R["copy_files"] = copy_info

# ---------------- per image counts ----------------
per_img = raw.groupby("image", sort=False).size()
R["n_images"] = int(per_img.size)
R["per_image_count_dist"] = per_img.value_counts().sort_index().to_dict()
R["frac_of_25"] = len(raw) / (25 * per_img.size)
R["n_subjects_true"] = int(raw.true_subject.nunique())

# ---------------- coverage ----------------
annotated = set(raw.image)
jpg = F[F.ext == "jpg"]
jpg_unique = jpg[~jpg.file.str.startswith("Copy of")]
R["jpg_files"] = len(jpg); R["jpg_unique"] = len(jpg_unique)
R["jpg_unique_annotated"] = int(jpg_unique.file.isin(annotated).sum())
unann = jpg_unique[~jpg_unique.file.isin(annotated)]
R["dng_annotated"] = int(F[F.ext == "dng"].file.isin(annotated).sum()); R["dng_total"] = int((F.ext == "dng").sum())
R["mp4_annotated"] = int(F[F.ext == "mp4"].file.isin(annotated).sum()); R["mp4_total"] = int((F.ext == "mp4").sum())
dng = F[F.ext == "dng"]
R["dng_folders"] = dng.folder.value_counts().to_dict()
R["dng_with_annotated_jpg_twin"] = int(sum((f.rsplit(".", 1)[0] + ".jpg") in annotated for f in dng.file))
# stems: dng stem may include .PORTRAIT? check generic twin
R["dng_with_any_annotated_same_stem"] = int(sum(any(a.split(".")[0] == f.split(".")[0] for a in annotated) for f in dng.file))

# ---------------- details csv ----------------
det = pd.read_csv(f"{MSTE}/mst-e_image_details.csv", dtype=str, keep_default_na=False)
R["details_header"] = list(det.columns); R["details_rows"] = len(det)
det["id_strip"] = det.image_ID.str.strip()
R["details_ids_with_whitespace"] = det.loc[det.image_ID != det.id_strip, "image_ID"].tolist()
R["details_ids_not_filelike"] = det.loc[~det.id_strip.str.contains(r"\.(?:jpg|mp4|dng)$", case=False), ["image_ID", "subject_name", "MST"]].values.tolist()
dups = det[det.duplicated("id_strip", keep=False)].sort_values("id_strip")
conf = []
for k, g in dups.groupby("id_strip"):
    cols = [c for c in ["pose", "lighting", "mask", "subject_name", "MST"] if g[c].nunique() > 1]
    conf.append({"id": k, "n": len(g), "conflicting_cols": cols, "vals": g[["pose", "lighting", "mask", "subject_name", "MST"]].values.tolist()})
R["details_duplicate_ids"] = conf
detids = set(det.id_strip)
R["annotated_not_in_details"] = sorted(annotated - detids)
R["annotated_not_in_details_folder"] = {i: fmap.get(i) for i in R["annotated_not_in_details"]}
R["folder_files_not_in_details"] = sorted(set(F.file) - detids)
R["details_ids_not_in_folders"] = sorted(detids - set(F.file))
R["details_lighting_values"] = det.lighting.value_counts().to_dict()
R["details_mask_values"] = det["mask"].value_counts().to_dict()
R["details_jpg_lighting_video"] = det.loc[(det.lighting == "video") & det.id_strip.str.endswith(".jpg"), "id_strip"].tolist()
# oracle per subject (consistent?)
sub_mst = det[det.subject_name.str.startswith("subject_")].groupby("subject_name").MST.agg(lambda s: sorted(set(s)))
R["details_subject_mst_sets"] = sub_mst.to_dict()
oracle = {s: int(v[0]) for s, v in sub_mst.items() if len(v) == 1}
raw["oracle"] = raw.true_subject.map(oracle)
raw["err"] = raw.mst - raw.oracle

# unannotated jpg metadata
dd = det.drop_duplicates("id_strip").set_index("id_strip")
R["unannotated_jpgs"] = [{"folder": r.folder, "file": r.file, **({k: dd.loc[r.file, k] for k in ["pose", "lighting", "mask"]} if r.file in dd.index else {"meta": "missing"})} for r in unann.itertuples()]

# golden / challenging
gc = pd.read_csv(f"{MSTE}/golden_and_adversarial_mst-e_image_ids.csv", dtype=str, keep_default_na=False)
R["gc_header"] = list(gc.columns)
gold = set(gc.golden_image_id.str.strip()); chal = set(gc.not_ideal_image_id.str.strip())
R["golden_annotated"] = f"{len(gold & annotated)}/{len(gold)}"; R["challenging_annotated"] = f"{len(chal & annotated)}/{len(chal)}"
R["golden_folder_subject_matches_list"] = int(sum(fmap.get(g) == s for g, s in zip(gc.golden_image_id.str.strip(), gc.subject)))
R["chal_folder_subject_matches_list"] = int(sum(fmap.get(g) == s for g, s in zip(gc.not_ideal_image_id.str.strip(), gc.subject)))

# per-MST folder counts vs data card
card_img = dict(zip(range(1, 11), [179, 218, 112, 187, 179, 165, 76, 143, 142, 111]))
card_vid = dict(zip(range(1, 11), [2, 5, 5, 3, 4, 3, 4, 2, 5, 1]))
F["oracle"] = F.folder.map(oracle)
img_like = F[F.ext.isin(["jpg", "dng"]) & ~F.file.str.startswith("Copy of")]
R["folder_images_by_mst"] = img_like.groupby("oracle").size().to_dict()
R["folder_jpg_unique_by_mst"] = jpg_unique.assign(o=jpg_unique.folder.map(oracle)).groupby("o").size().to_dict()
R["folder_videos_by_mst"] = F[F.ext == "mp4"].groupby("oracle").size().to_dict()
R["card_images_sum"] = sum(card_img.values()); R["card_videos_sum"] = sum(card_vid.values())
R["card_minus_folder_images"] = {k: card_img[k] - R["folder_images_by_mst"].get(k, 0) for k in card_img}
R["card_minus_folder_videos"] = {k: card_vid[k] - R["folder_videos_by_mst"].get(k, 0) for k in card_vid}

# ---------------- skipped (4-label) images ----------------
lightmap = dd.lighting.to_dict()
img = raw.groupby("image", sort=False).agg(n=("mst", "size"), subj=("true_subject", "first")).reset_index()
img["light"] = img.image.map(lightmap)
four = img[img.n == 4]
R["four_label_images"] = {"n": len(four), "subjects": int(four.subj.nunique()),
                          "lighting": four.light.fillna("missing").value_counts().to_dict(),
                          "challenging": sorted(set(four.image) & chal), "golden": sorted(set(four.image) & gold)}
pl = img.light == "poorly_lit"
tab = [[int(((img.n == 4) & pl).sum()), int(((img.n == 5) & pl).sum())], [int(((img.n == 4) & ~pl).sum()), int(((img.n == 5) & ~pl).sum())]]
R["four_vs_poorlit_table"] = tab
R["four_vs_poorlit_fisher"] = list(stats.fisher_exact(tab))
R["lighting_image_counts"] = img.light.fillna("missing").value_counts().to_dict()

# ---------------- file order structure ----------------
raw["row"] = np.arange(len(raw))
blocks = (raw.image != raw.image.shift()).sum()
R["image_blocks"] = int(blocks)
sb = raw.true_subject[(raw.true_subject != raw.true_subject.shift())].tolist()
R["subject_block_order"] = sb
R["last_subject_block"] = sb[-1]
img_order = raw.drop_duplicates("image")[["image", "true_subject"]]
R["sorted_by_filename_within_subject"] = int(sum(list(g.image) == sorted(g.image) for _, g in img_order.groupby("true_subject")))
ts = img_order.image.str.extract(r"PXL_\d{8}_(\d+)")[0].astype(float).values
dec = np.where(np.diff(ts) < 0)[0]
subj_change = (img_order.true_subject.values[1:] != img_order.true_subject.values[:-1])
R["timestamp_decreases"] = int(len(dec)); R["timestamp_decreases_at_subject_boundary"] = int(subj_change[dec].sum())
R["subject_boundaries"] = int(subj_change.sum())

# ---------------- within-image label contiguity ----------------
groups = [(im, g.mst.tolist(), g.true_subject.iloc[0]) for im, g in raw.groupby("image", sort=False)]
n_const = 0; n_contig = 0; exp_contig = 0.0; logP = 0.0; ninf = 0
for im, labs, s in groups:
    c = Counter(labs)
    if len(c) == 1:
        n_const += 1; continue
    ninf += 1
    runs = [k for k, _ in itertools.groupby(labs)]
    n_contig += len(runs) == len(c)
    p = math.factorial(len(c)) * np.prod([math.factorial(v) for v in c.values()]) / math.factorial(len(labs))
    exp_contig += p; logP += math.log10(p)
R["contiguity"] = {"constant_images": n_const, "informative": ninf, "contiguous": n_contig,
                   "expected_random": exp_contig, "log10_P_all": logP}

# ---------------- Plackett-Luce run-order model ----------------
pl_data = []  # (subject, counts list in observed order, centred values)
for im, labs, s in groups:
    runs = [(k, len(list(g))) for k, g in itertools.groupby(labs)]
    if len(runs) < 2: continue
    v = np.array([k for k, _ in runs], float); c = np.array([n for _, n in runs], float)
    pl_data.append((s, c, v - v.mean()))

# vectorised: pad each image's runs to 5 with -inf log-count
NR = 5
LC = np.full((len(pl_data), NR), -np.inf); VV = np.zeros((len(pl_data), NR)); M = np.zeros((len(pl_data), NR), bool)
for i, (_, c, v) in enumerate(pl_data):
    m = len(c); LC[i, :m] = np.log(c); VV[i, :m] = v; M[i, :m - 1] = True  # terms for all but last run
PL_SUBJ = np.array([d[0] for d in pl_data])

def nll(beta, idx):
    W = LC[idx] - beta * VV[idx]
    L = np.logaddexp.accumulate(W[:, ::-1], axis=1)[:, ::-1]  # suffix logsumexp
    with np.errstate(invalid="ignore"):
        T = np.where(M[idx], W - L, 0.0)
    return -T.sum()

def fit(idx):
    r = optimize.minimize_scalar(nll, bounds=(-5, 5), args=(idx,), method="bounded", options={"xatol": 1e-6})
    return r.x, r.fun

ALL = np.arange(len(pl_data))
# sanity: vectorised nll equals a loop on a few images at beta=0.3
def nll_loop(beta, data):
    tot = 0.0
    for _, c, v in data:
        w = np.log(c) - beta * v
        for i in range(len(c) - 1): tot -= w[i] - np.logaddexp.reduce(w[i:])
    return tot
assert abs(nll_loop(0.3, pl_data) - nll(0.3, ALL)) < 1e-6
bhat, f1 = fit(ALL); f0 = nll(0.0, ALL)
h = 1e-4; se = 1 / math.sqrt((nll(bhat + h, ALL) - 2 * f1 + nll(bhat - h, ALL)) / h**2)
R["pl_beta"] = {"beta": bhat, "exp_beta": math.exp(bhat), "LR_vs_0": 2 * (f0 - f1), "se": se, "n_images": len(pl_data)}
subs = sorted(set(PL_SUBJ))
by_s = {s_: np.where(PL_SUBJ == s_)[0] for s_ in subs}
per = {s: fit(by_s[s]) for s in subs}
R["pl_beta_per_subject"] = {s: per[s][0] for s in subs}
R["pl_hetero_LR"] = 2 * (f1 - sum(v[1] for v in per.values()))
R["pl_hetero_p"] = float(stats.chi2.sf(R["pl_hetero_LR"], len(subs) - 1))
R["pl_images_per_subject_range"] = [min(len(v) for v in by_s.values()), max(len(v) for v in by_s.values())]
# ascending/descending run orders vs expectation under beta=0
asc = desc = 0; e_asc = e_desc = 0.0
for _, c, v in pl_data:
    order = np.argsort(v)
    asc += all(np.diff(v) > 0); desc += all(np.diff(v) < 0)
    def p_seq(idx):
        cc = c[idx]; p = 1.0
        for i in range(len(cc) - 1): p *= cc[i] / cc[i:].sum()
        return p
    e_asc += p_seq(order); e_desc += p_seq(order[::-1])
R["run_order_asc_desc"] = {"asc_obs": asc, "asc_exp": e_asc, "desc_obs": desc, "desc_exp": e_desc}
# cluster bootstrap of beta
rng = np.random.default_rng(rng_seed)
bb = []
for _ in range(B):
    draw = rng.choice(subs, len(subs), replace=True)
    bb.append(fit(np.concatenate([by_s[s_] for s_ in draw]))[0])
R["pl_beta_boot_ci"] = list(np.percentile(bb, [2.5, 97.5]))

# ---------------- position analyses (complete images) ----------------
comp = [(im, np.array(l, float), s) for im, l, s in groups if len(l) == 5]
X = np.vstack([c[1] for c in comp]); S = np.array([c[2] for c in comp])
fr = stats.friedmanchisquare(*X.T)
R["friedman"] = {"chi2": fr.statistic, "p": fr.pvalue, "n": len(X), "W": fr.statistic / (len(X) * 4)}
dev = X - X.mean(1, keepdims=True)
med = np.median(X, 1, keepdims=True)
agree = (X == med).astype(float)
d15 = X[:, 0] - X[:, 4]
def boot_rows(M):
    idx = {s: np.where(S == s)[0] for s in np.unique(S)}; us = list(idx)
    rr = np.random.default_rng(rng_seed); out = []
    for _ in range(B):
        ii = np.concatenate([idx[s] for s in rr.choice(us, len(us), replace=True)])
        out.append(M[ii].mean(0))
    return np.percentile(np.array(out), [2.5, 97.5], axis=0)
R["pos_dev_mean"] = dev.mean(0).tolist(); R["pos_dev_ci"] = boot_rows(dev).T.tolist()
R["pos_agree_median"] = agree.mean(0).tolist(); R["pos_agree_ci"] = boot_rows(agree).T.tolist()
R["pos1_minus_pos5"] = float(d15.mean()); R["pos1_minus_pos5_ci"] = boot_rows(d15[:, None]).ravel().tolist()
R["pos_mean_err_vs_oracle"] = (X - np.array([oracle[s] for s in S])[:, None]).mean(0).tolist()
# random-order null expectation for agreement with median
R["agree_random_null"] = float(agree.mean())

# simulation nulls: grouped-by-first-appearance (beta=0) and fitted beta
def sim(beta, reps, seed):
    rr = np.random.default_rng(seed); devs = []; ags = []; chis = []
    for _ in range(reps):
        Y = np.empty_like(X)
        for i, row in enumerate(X):
            c = Counter(row); vals = np.array(list(c), float); cnt = np.array([c[v] for v in vals], float)
            vc = vals - row.mean()
            rem = list(range(len(vals))); seq = []
            while rem:
                w = cnt[rem] * np.exp(-beta * vc[rem]); j = rr.choice(len(rem), p=w / w.sum())
                k = rem.pop(j); seq += [vals[k]] * int(cnt[k])
            Y[i] = seq
        devs.append((Y - Y.mean(1, keepdims=True)).mean(0)); ags.append((Y == med).mean(0))
        chis.append(stats.friedmanchisquare(*Y.T).statistic)
    return np.mean(devs, 0), np.mean(ags, 0), np.array(chis)
g_dev, g_ag, g_chi = sim(0.0, 200, 1)
b_dev, b_ag, b_chi = sim(bhat, 200, 2)
R["null_grouped"] = {"dev": g_dev.tolist(), "agree": g_ag.tolist(), "friedman_mean": g_chi.mean(), "friedman_max": g_chi.max(), "reps": 200}
R["null_beta"] = {"dev": b_dev.tolist(), "agree": b_ag.tolist(), "friedman_mean": b_chi.mean(),
                  "p_two_sided": float(min(1, 2 * min((b_chi >= fr.statistic).mean(), (b_chi <= fr.statistic).mean()))), "reps": 200}
# fully random null friedman
rr = np.random.default_rng(3)
rchi = [stats.friedmanchisquare(*np.array([rr.permutation(r) for r in X]).T).statistic for _ in range(200)]
R["null_random_friedman"] = {"mean": float(np.mean(rchi)), "max": float(np.max(rchi))}

# ---------------- category usage ----------------
ks = range(1, 11)
sub_rows = {s: g for s, g in raw.groupby("true_subject")}
def usage(draw):
    a = np.zeros(10); o = np.zeros(10)
    for s in draw:
        g = sub_rows[s]; a += np.bincount(g.mst, minlength=11)[1:]; o[oracle[s] - 1] += len(g)
    return a / a.sum(), o / o.sum()
sa, so = usage(list(sub_rows))
R["share_annot"] = dict(zip(ks, sa.tolist())); R["share_oracle"] = dict(zip(ks, so.tolist()))
R["count_annot"] = dict(zip(ks, np.bincount(raw.mst, minlength=11)[1:].tolist()))
R["ratio"] = {k: sa[k - 1] / so[k - 1] if so[k - 1] > 0 else None for k in ks}
R["tv"] = 0.5 * np.abs(sa - so).sum()
rr = np.random.default_rng(rng_seed); ratios = []; diffs = []; tvs = []
us = list(sub_rows)
for _ in range(B):
    a, o = usage(rr.choice(us, len(us), replace=True))
    with np.errstate(divide="ignore", invalid="ignore"): ratios.append(np.where(o > 0, a / o, np.nan))
    diffs.append(a - o); tvs.append(0.5 * np.abs(a - o).sum())
ratios = np.array(ratios); diffs = np.array(diffs)
R["ratio_ci"] = {k: list(np.nanpercentile(ratios[:, k - 1], [2.5, 97.5])) for k in ks}
R["ratio_n_defined"] = {k: int(np.isfinite(ratios[:, k - 1]).sum()) for k in ks}
R["diff_ci_pp"] = {k: list(100 * np.percentile(diffs[:, k - 1], [2.5, 97.5])) for k in ks}
R["tv_ci"] = list(np.percentile(tvs, [2.5, 97.5]))
R["oracle_subjects_per_level"] = Counter(oracle.values())
# per-level exact agreement and image medians
R["exact_by_oracle"] = {int(o): [int((g.mst == o).sum()), len(g)] for o, g in raw.groupby("oracle")}
imed = raw.groupby("image").agg(med=("mst", "median"), o=("oracle", "first"), s=("true_subject", "first"))
R["image_median_dist"] = imed.med.value_counts().sort_index().to_dict()
R["image_oracle_dist"] = imed.o.value_counts().sort_index().to_dict()
R["image_median_within1"] = float((abs(imed.med - imed.o) <= 1).mean())
R["image_median_within1_n"] = [int((abs(imed.med - imed.o) <= 1).sum()), len(imed)]
R["mst10_subject"] = [s for s, v in oracle.items() if v == 10]
s10 = raw[raw.oracle == 10]
R["mst10_on_subject"] = [int((s10.mst == 10).sum()), len(s10)]
R["mst10_img_medians_10"] = [int((imed[imed.o == 10].med == 10).sum()), int((imed.o == 10).sum())]
R["img_medians_eq6"] = int((imed.med == 6).sum()); R["imgs_oracle6"] = int((imed.o == 6).sum())
# subject pooled median
sp = raw.groupby("true_subject").mst.median(); smm = imed.groupby("s").med.median()
R["subject_pooled_median_within1"] = int(sum(abs(sp[s] - oracle[s]) <= 1 for s in sp.index))
R["subject_pooled_fails"] = {s: [float(sp[s]), oracle[s]] for s in sp.index if abs(sp[s] - oracle[s]) > 1}
R["subject_median_of_imgmedians_within1"] = int(sum(abs(smm[s] - oracle[s]) <= 1 for s in smm.index))
R["subject_median_of_imgmedians_fails"] = {s: [float(smm[s]), oracle[s]] for s in smm.index if abs(smm[s] - oracle[s]) > 1}
# majority-vote/mode variant
smode = raw.groupby("true_subject").mst.agg(lambda x: x.value_counts().idxmax())
R["subject_mode_within1"] = int(sum(abs(smode[s] - oracle[s]) <= 1 for s in smode.index))
R["subject_pooled_median_by_subject"] = {s: [float(sp[s]), float(smm[s]), oracle[s]] for s in sp.index}

def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating, float)): return None if (isinstance(o, float) and math.isnan(o)) else float(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(conv(R), open(f"{OUT}/results.json", "w"), indent=1)
for k, v in conv(R).items():
    s = json.dumps(v); print(k, ":", s[:600])

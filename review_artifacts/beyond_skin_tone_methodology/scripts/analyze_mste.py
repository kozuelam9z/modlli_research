import sys, csv, json
import numpy as np, pandas as pd
from scipy import stats

SP, D = sys.argv[1], sys.argv[2]
s = pd.read_csv(SP + "/mste_proc/scores.csv")
meta = pd.read_csv(D + "/mst-e_image_details.csv").drop_duplicates("image_ID")
gold = pd.read_csv(D + "/golden_and_adversarial_mst-e_image_ids.csv")
ann = pd.read_csv(D.rsplit("/", 1)[0] + "/mste_annotations.csv")
ann["mst"] = ann.annotation.str.replace("MST", "").astype(int)
crowd = ann.groupby("image").mst.median().rename("crowd_median")

df = s.merge(meta, left_on="file", right_on="image_ID", how="left")
oracle = meta.dropna(subset=["MST"]).groupby("subject_name").MST.agg(lambda x: x.mode()[0])
df["oracle"] = df.subject.map(oracle).astype(float)
df = df.merge(crowd, left_on="file", right_index=True, how="left")
out = {}
out["n_scored"] = len(df)
out["n_meta_missing"] = int(df.lighting.isna().sum())
df = df[(df["mask"].astype(str) == "0")]  # exclude face-mask images
out["n_nomask"] = len(df)


def icc1(d, col):  # one-way random, single measure; subjects as targets
    g = d.groupby("subject")[col]
    k = g.size(); n = len(k); N = k.sum()
    grand = d[col].mean()
    msb = (k * (g.mean() - grand) ** 2).sum() / (n - 1)
    msw = ((d[col] - d.subject.map(g.mean())) ** 2).sum() / (N - n)
    k0 = (N - (k ** 2).sum() / N) / (n - 1)
    return (msb - msw) / (msb + (k0 - 1) * msw), np.sqrt(msw), d.groupby("subject")[col].mean().std()


def boot_icc(d, col, B=2000, seed=0):
    rng = np.random.default_rng(seed); subs = d.subject.unique(); vals = []
    gs = {k: v for k, v in d.groupby("subject")}
    for _ in range(B):
        pick = rng.choice(subs, len(subs), replace=True)
        bd = pd.concat([gs[p].assign(subject=f"{p}_{i}") for i, p in enumerate(pick)])
        vals.append(icc1(bd, col)[0])
    return np.percentile(vals, [2.5, 97.5])


for tag in ("full", "nofh"):
    for col in (f"L_{tag}", f"h_{tag}"):
        for sub, dd in (("all", df), ("well_lit", df[df.lighting == "well_lit"]), ("poorly_lit", df[df.lighting == "poorly_lit"])):
            r, wsd, bsd = icc1(dd, col)
            out[f"icc_{col}_{sub}"] = dict(icc=round(r, 3), within_sd=round(wsd, 2), between_sd_of_means=round(bsd, 2), n_img=len(dd))
        out[f"icc_{col}_all"]["boot95"] = [round(x, 3) for x in boot_icc(df, col)]

# threshold instability (paper thresholds L*=60, h*=55)
df["light"] = df.L_full >= 60; df["yellow"] = df.h_full >= 55
per = df.groupby("subject").agg(n=("file", "size"), oracle=("oracle", "first"), L_mean=("L_full", "mean"), L_sd=("L_full", "std"),
                                L_min=("L_full", "min"), L_max=("L_full", "max"), h_mean=("h_full", "mean"), h_sd=("h_full", "std"),
                                h_min=("h_full", "min"), h_max=("h_full", "max"), p_light=("light", "mean"), p_yellow=("yellow", "mean"))
per = per.sort_values("oracle")
out["per_subject"] = per.round(2).reset_index().to_dict(orient="records")
maj_l = per.p_light.apply(lambda p: max(p, 1 - p)); maj_y = per.p_yellow.apply(lambda p: max(p, 1 - p))
out["tone_flip"] = dict(subjects_with_both_categories=int(((per.p_light > 0) & (per.p_light < 1)).sum()),
                        subjects_minority_ge_10pct=int(((per.p_light >= .1) & (per.p_light <= .9)).sum()),
                        image_disagree_with_subject_majority=round(float((1 - maj_l).mul(per.n).sum() / per.n.sum()), 3))
out["hue_flip"] = dict(subjects_with_both_categories=int(((per.p_yellow > 0) & (per.p_yellow < 1)).sum()),
                       subjects_minority_ge_10pct=int(((per.p_yellow >= .1) & (per.p_yellow <= .9)).sum()),
                       image_disagree_with_subject_majority=round(float((1 - maj_y).mul(per.n).sum() / per.n.sum()), 3))
# 4-cell category per image vs subject's modal cell
df["cell"] = df.light.map({True: "L", False: "D"}) + df.yellow.map({True: "Y", False: "R"})
modal = df.groupby("subject").cell.agg(lambda x: x.mode()[0])
out["cell_disagree_with_subject_mode"] = round(float((df.cell != df.subject.map(modal)).mean()), 3)

# lighting effect within subject (paired subject means)
pm = df.groupby(["subject", "lighting"])[["L_full", "h_full"]].mean().unstack()
for c in ("L_full", "h_full"):
    dlt = (pm[(c, "poorly_lit")] - pm[(c, "well_lit")]).dropna()
    t = stats.ttest_1samp(dlt, 0)
    out[f"lighting_shift_{c}"] = dict(mean=round(dlt.mean(), 2), sd=round(dlt.std(), 2), min=round(dlt.min(), 2), max=round(dlt.max(), 2), n=len(dlt), p=float(t.pvalue))

# golden vs not-ideal pair
g = gold.melt(id_vars="subject", var_name="kind", value_name="file").merge(df[["file", "L_full", "h_full", "cell"]], on="file", how="left")
gw = g.pivot(index="subject", columns="kind", values=["L_full", "h_full", "cell"])
out["golden_pairs_scored"] = int(gw[("L_full", "golden_image_id")].notna().sum() if ("L_full", "golden_image_id") in gw else 0)
gw2 = gw.dropna()
if len(gw2):
    dL = gw2[("L_full", "not_ideal_image_id")].astype(float) - gw2[("L_full", "golden_image_id")].astype(float)
    dh = gw2[("h_full", "not_ideal_image_id")].astype(float) - gw2[("h_full", "golden_image_id")].astype(float)
    out["golden_vs_notideal"] = dict(n=len(gw2), dL_mean=round(dL.mean(), 2), dL_absmax=round(dL.abs().max(), 2), dh_mean=round(dh.mean(), 2),
                                     dh_absmean=round(dh.abs().mean(), 2), dh_absmax=round(dh.abs().max(), 2),
                                     cell_changed=int((gw2[("cell", "not_ideal_image_id")] != gw2[("cell", "golden_image_id")]).sum()))

# L-h relationships
sm = df.groupby("subject")[["L_full", "h_full", "oracle"]].mean()
out["between_subject_corr_L_h"] = [round(x, 3) for x in stats.pearsonr(sm.L_full, sm.h_full)]
dw = df.assign(Lc=df.L_full - df.subject.map(sm.L_full), hc=df.h_full - df.subject.map(sm.h_full))
out["within_subject_corr_L_h"] = [round(x, 3) for x in stats.pearsonr(dw.Lc, dw.hc)]
out["spearman_oracle_vs_subjectmean_L"] = [round(x, 3) for x in stats.spearmanr(sm.oracle, sm.L_full)]
out["spearman_oracle_vs_subjectmean_h"] = [round(x, 3) for x in stats.spearmanr(sm.oracle, sm.h_full)]
# partial: does h add to L in predicting oracle (OLS on 19 subjects)
import statsmodels.api as smod
X = smod.add_constant(sm[["L_full", "h_full"]]); fit = smod.OLS(sm.oracle, X).fit()
out["ols_oracle_on_L_h"] = dict(coef={k: round(v, 3) for k, v in fit.params.items()}, p={k: round(v, 4) for k, v in fit.pvalues.items()}, r2=round(fit.rsquared, 3),
                                r2_L_only=round(smod.OLS(sm.oracle, smod.add_constant(sm[["L_full"]])).fit().rsquared, 3))
# image level: crowd median vs image L within subject (does apparent L track crowd label?)
cc = dw.dropna(subset=["crowd_median"])
cc = cc.assign(cm=cc.crowd_median - cc.subject.map(cc.groupby("subject").crowd_median.mean()))
out["within_subject_corr_crowdMST_vs_L"] = [round(x, 3) for x in stats.spearmanr(cc.cm, cc.Lc)]
out["within_subject_corr_crowdMST_vs_h"] = [round(x, 3) for x in stats.spearmanr(cc.cm, cc.hc)]
# variance decomposition share: within/total
for c in ("L_full", "h_full"):
    tot = df[c].var(); within = dw[{"L_full": "Lc", "h_full": "hc"}[c]].var()
    out[f"within_share_{c}"] = round(within / tot, 3)
# negative / out-of-range hue
out["hue_lt_0"] = int((df.h_full < 0).sum()); out["hue_range"] = [round(df.h_full.min(), 2), round(df.h_full.max(), 2)]
# mask-variant agreement
out["variant_corr_L"] = round(df[["L_full", "L_nofh"]].corr().iloc[0, 1], 3)
out["variant_corr_h"] = round(df[["h_full", "h_nofh"]].corr().iloc[0, 1], 3)
out["variant_cell_agree"] = round(float(((df.L_nofh >= 60) == df.light).mul((df.h_nofh >= 55) == df.yellow).mean()), 3)
# mode-based vs mean-based hue
out["corr_hmode_vs_hmean"] = round(df[["h_full", "hmean_full"]].corr().iloc[0, 1], 3)
json.dump(out, open(SP + "/mste_proc/analysis.json", "w"), indent=1, default=float)
df.to_csv(SP + "/mste_proc/scored_merged.csv", index=False)
print(json.dumps({k: v for k, v in out.items() if k != "per_subject"}, indent=1, default=float))
print(per.round(1).to_string())

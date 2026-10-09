"""Check MixedLM variance components / convergence with alternative optimizers. Run: venv/bin/python -I lmm_check.py"""
import json, warnings
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.formula.api as smf
warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent
d = pd.read_csv(OUT.parent / "annotations_clean.csv")
d["sid"] = d.subject.str.replace("subject_", "").astype(int)
d = d[d.lighting.isin(["well_lit", "poorly_lit"])].dropna(subset=["mask", "pose"]).copy()
d["poorly"] = (d.lighting == "poorly_lit").astype(float)
for q in ["bottom", "frontal", "side"]:
    d[f"p_{q}"] = (d.pose == q).astype(float)
d["orc"] = d.oracle - d.oracle.mean()
F = "err ~ poorly + p_bottom + p_frontal + p_side + mask"
out = {"var_of_subject_mean_err": float(d.groupby("sid").err.mean().var(ddof=1))}
for meth in ["powell", "nm", "lbfgs", "bfgs"]:
    for nm, f in [("main", F), ("interaction", F.replace("poorly +", "poorly*orc +"))]:
        try:
            r = smf.mixedlm(f, d, groups="sid", re_formula="1", vc_formula={"image": "0 + C(image)"}).fit(reml=True, method=meth, maxiter=5000)
            key = "poorly" if nm == "main" else "poorly:orc"
            out[f"{nm}_{meth}"] = dict(coef=float(r.params[key]), ci=[float(x) for x in r.conf_int().loc[key]], var_subj=float(r.cov_re.iloc[0, 0]),
                                       var_img=float(r.vcomp[0]), resid=float(r.scale), llf=float(r.llf), converged=bool(r.converged))
        except Exception as e:
            out[f"{nm}_{meth}"] = str(e)
# random intercept only (no image vc) for reference
r = smf.mixedlm(F, d, groups="sid").fit(reml=True)
out["ri_only"] = dict(coef=float(r.params["poorly"]), var_subj=float(r.cov_re.iloc[0, 0]), converged=bool(r.converged))
json.dump(out, open(OUT / "lmm_check.json", "w"), indent=1)
print(json.dumps(out, indent=1))

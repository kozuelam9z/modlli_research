"""Lighting / pose / mask effects on MST-E crowd annotations (released file = ONE region, labelled Ghana).

Run: venv/bin/python -I condition_effects.py   -> writes results.json next to this file.
Units: subjects (19) are the independent units; images nested in subjects; annotations nested in images.
All CIs: subject-cluster percentile bootstrap, fixed seed.
"""
import json, os, sys, time, warnings
from multiprocessing import Pool
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'annotations_clean.csv')
SEED = 20231008
B = 4000          # simple bootstraps
B_ORD = int(os.environ.get('B_ORD', 2000))     # ordinal-model bootstrap (each resample = one OrderedModel fit)
POSE_REF = 'facing_camera'
POSES = ['bottom', 'frontal', 'side']          # contrasts vs POSE_REF
METRICS = ['signed_mean_err_img', 'signed_mean_err_ann', 'mean_abs_err_ann', 'signed_median_err', 'abs_median_err']
warnings.filterwarnings('ignore')


def load():
    d = pd.read_csv(DATA)
    d['abs_err'] = d.err.abs()
    img = d.groupby('image').agg(
        subject=('subject', 'first'), oracle=('oracle', 'first'), pose=('pose', 'first'),
        lighting=('lighting', 'first'), mask=('mask', 'first'), is_golden=('is_golden', 'first'),
        is_challenging=('is_challenging', 'first'), meta_conflict=('meta_conflict', 'first'),
        n=('mst_annot', 'size'), mean_annot=('mst_annot', 'mean'), med_annot=('mst_annot', 'median'),
        sum_err=('err', 'sum'), sum_abs=('abs_err', 'sum')).reset_index()
    img['mean_err'] = img.mean_annot - img.oracle
    img['mean_abs_err'] = img.sum_abs / img.n
    img['med_err'] = img.med_annot - img.oracle          # numpy median: mean of middle two for the 15 4-annotation images
    img['abs_med_err'] = img.med_err.abs()
    return d, img


def cell(x):
    return dict(n_img=int(len(x)), n_ann=int(x.n.sum()),
                signed_mean_err_img=x.mean_err.mean(), signed_mean_err_ann=x.sum_err.sum() / x.n.sum(),
                mean_abs_err_ann=x.sum_abs.sum() / x.n.sum(), signed_median_err=x.med_err.mean(),
                abs_median_err=x.abs_med_err.mean())


def contrast(img, a, b):
    """Per-subject contrast: images with boolean mask a minus images with mask b (within subject)."""
    rows = []
    for s, g in img.groupby('subject'):
        A, Bb = g[a.loc[g.index]], g[b.loc[g.index]]
        if len(A) == 0 or len(Bb) == 0:
            continue
        ca, cb = cell(A), cell(Bb)
        r = dict(subject=s, oracle=int(g.oracle.iloc[0]), n_img_a=ca['n_img'], n_img_b=cb['n_img'],
                 n_ann_a=ca['n_ann'], n_ann_b=cb['n_ann'])
        for m in METRICS:
            r[m + '_a'], r[m + '_b'], r['d_' + m] = ca[m], cb[m], ca[m] - cb[m]
        # within-subject Welch test, images as units (image mean error)
        if len(A) > 1 and len(Bb) > 1:
            r['welch_p_img_mean_err'] = stats.ttest_ind(A.mean_err, Bb.mean_err, equal_var=False).pvalue
        rows.append(r)
    return pd.DataFrame(rows).sort_values('oracle', kind='stable').reset_index(drop=True)


def boot_mean(x, rng, b=B):
    x = np.asarray(x, float)
    return x[rng.integers(0, len(x), (b, len(x)))].mean(1)


def summarize(x, rng):
    x = np.asarray(x, float)
    bs = boot_mean(x, rng)
    out = dict(n_subjects=len(x), mean=x.mean(), sd=x.std(ddof=1), median=float(np.median(x)),
               ci95=list(np.percentile(bs, [2.5, 97.5])), ci90=list(np.percentile(bs, [5, 95])),
               t_p=stats.ttest_1samp(x, 0).pvalue, n_pos=int((x > 0).sum()), n_neg=int((x < 0).sum()),
               n_zero=int((x == 0).sum()))
    out['wilcoxon_p'] = stats.wilcoxon(x).pvalue if (x != 0).sum() >= 1 else None
    return out


def tost(x, rng, margins=(0.25, 0.5)):
    x = np.asarray(x, float)
    n, mu, se = len(x), x.mean(), x.std(ddof=1) / np.sqrt(len(x))
    bs = boot_mean(x, rng)
    lo, hi = np.percentile(bs, [5, 95])
    res = {}
    for m in margins:
        p_low = 1 - stats.t.cdf((mu + m) / se, n - 1)   # H0: mu <= -m
        p_up = stats.t.cdf((mu - m) / se, n - 1)        # H0: mu >= +m
        res[f'pm{m}'] = dict(p_lower=p_low, p_upper=p_up, p_tost=max(p_low, p_up),
                             equivalent_t=bool(max(p_low, p_up) < 0.05),
                             boot90=[lo, hi], equivalent_boot=bool(-m < lo and hi < m))
    return res


def pooled(img, cond, levels, num, den, rng):
    """Image-pooled (NOT subject-balanced) group means sum(num)/sum(den) per level, subject-cluster bootstrap."""
    subs = sorted(img.subject.unique())
    N = np.array([[img[(img.subject == s) & cond(l)][num].sum() for l in levels] for s in subs], float)
    D = np.array([[img[(img.subject == s) & cond(l)][den].sum() for l in levels] for s in subs], float)
    idx = rng.integers(0, len(subs), (B, len(subs)))
    bm = N[idx].sum(1) / D[idx].sum(1)
    est = N.sum(0) / D.sum(0)
    out = {l: dict(value=est[i], ci95=list(np.percentile(bm[:, i], [2.5, 97.5])), n_img=int(D[:, i].sum()) if den == 'one' else None)
           for i, l in enumerate(levels)}
    if len(levels) == 2:
        dd = bm[:, 0] - bm[:, 1]
        out[f'diff_{levels[0]}_minus_{levels[1]}'] = dict(value=est[0] - est[1], ci95=list(np.percentile(dd, [2.5, 97.5])),
                                                          ci90=list(np.percentile(dd, [5, 95])))
    return out


# ---------------- model data ----------------
def model_frame(d):
    m = d[d.lighting.isin(['well_lit', 'poorly_lit']) & d.pose.isin([POSE_REF] + POSES) & d['mask'].notna()].copy()
    m['poorly'] = (m.lighting == 'poorly_lit').astype(float)
    for p in POSES:
        m['pose_' + p] = (m.pose == p).astype(float)
    m['mask'] = m['mask'].astype(float)
    return m.reset_index(drop=True)


COVS = ['poorly'] + ['pose_' + p for p in POSES] + ['mask']


def ordinal_fit(m, cluster):
    from statsmodels.miscmodels.ordinal_model import OrderedModel
    fe = pd.get_dummies(cluster, prefix='S', drop_first=True).astype(float)
    X = pd.concat([m[COVS].reset_index(drop=True), fe.reset_index(drop=True)], axis=1)
    y = m.mst_annot.values
    levels = np.unique(y)
    mod = OrderedModel(y, X, distr='logit')
    r = mod.fit(method='bfgs', maxiter=5000, disp=False)
    p = r.params
    E = lambda Xc: (mod.predict(p.values, exog=Xc.values) @ levels).mean()
    out = {c: p[c] for c in COVS}
    def setx(**kw):
        Xc = X.copy()
        for k, v in kw.items():
            Xc[k] = v
        return Xc
    out['ame_poorly'] = E(setx(poorly=1.0)) - E(setx(poorly=0.0))
    out['ame_mask'] = E(setx(mask=1.0)) - E(setx(mask=0.0))
    base = setx(**{'pose_' + q: 0.0 for q in POSES})
    for q in POSES:
        out['ame_pose_' + q] = E(setx(**{('pose_' + z): (1.0 if z == q else 0.0) for z in POSES})) - E(base)
    thr = mod.transform_threshold_params(p.values)[1:-1]
    out['mean_threshold_spacing'] = float(np.diff(thr).mean())
    out['converged'] = bool(r.mle_retvals.get('converged', True))
    return out


_M = None


def _init(m):
    global _M
    _M = m


def _ord_boot(b):
    rng = np.random.default_rng([SEED, 7, b])
    subs = np.array(sorted(_M.subject.unique()))
    pick = rng.choice(subs, len(subs), replace=True)
    parts = [_M[_M.subject == s].assign(cl=f'c{i}') for i, s in enumerate(pick)]
    mb = pd.concat(parts, ignore_index=True)
    try:
        return ordinal_fit(mb, mb.cl)
    except Exception as e:  # report failures, never silently drop
        return dict(error=str(e))


def ols_fe_boot(m, rng):
    """err ~ subject FE + COVS via within-subject demeaning; cluster bootstrap (duplicated subjects demean identically)."""
    blocks = {}
    for s, g in m.groupby('subject'):
        Xg = g[COVS].values - g[COVS].values.mean(0)
        yg = g.err.values - g.err.values.mean()
        blocks[s] = (Xg.T @ Xg, Xg.T @ yg)
    subs = sorted(blocks)
    XtX = np.array([blocks[s][0] for s in subs]); Xty = np.array([blocks[s][1] for s in subs])
    est = np.linalg.solve(XtX.sum(0), Xty.sum(0))
    idx = rng.integers(0, len(subs), (B, len(subs)))
    bs = np.array([np.linalg.solve(XtX[i].sum(0), Xty[i].sum(0)) for i in idx])
    return {c: dict(coef=est[k], ci95=list(np.percentile(bs[:, k], [2.5, 97.5])), ci90=list(np.percentile(bs[:, k], [5, 95])))
            for k, c in enumerate(COVS)}


def lmm(m, formula, vc=True, re_formula=None):
    import statsmodels.formula.api as smf
    kw = dict(groups='subject')
    if vc:
        kw['vc_formula'] = {'image': '0 + C(image)'}
    # statsmodels drops the group random intercept when vc_formula is given without re_formula -> force it
    kw['re_formula'] = re_formula or '1'
    md = smf.mixedlm(formula, m, **kw)
    r = md.fit(reml=True, method=['lbfgs', 'bfgs', 'nm'])
    ci95 = r.conf_int(0.05); ci90 = r.conf_int(0.10)
    fe = {k: dict(coef=r.fe_params[k], se=r.bse_fe[k], p=r.pvalues[k], ci95=list(ci95.loc[k]), ci90=list(ci90.loc[k]))
          for k in r.fe_params.index}
    out = dict(formula=formula, image_vc=vc, re_formula=kw['re_formula'], converged=bool(r.converged), fixed=fe,
               subject_re_cov=r.cov_re.values.tolist(), scale_resid_var=r.scale)
    if vc:
        out['image_vc_var'] = float(r.vcomp[0])
    return out


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, pd.DataFrame):
        return jsonable(o.to_dict('records'))
    if isinstance(o, (np.floating, float)):
        return None if np.isnan(o) else round(float(o), 6)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    d, img = load()
    R = dict(meta=dict(seed=SEED, B=B, B_ordinal=B_ORD, pose_reference=POSE_REF,
                       n_annotations=len(d), n_images=len(img), n_subjects=img.subject.nunique(),
                       region='single released region labelled Ghana; 4-5 annotations per image',
                       metric_defs={
                           'signed_mean_err_img': 'mean over images of (mean annotation - oracle)',
                           'signed_mean_err_ann': 'mean over annotations of (annotation - oracle)',
                           'mean_abs_err_ann': 'mean over annotations of |annotation - oracle|',
                           'signed_median_err': 'mean over images of (median annotation - oracle)',
                           'abs_median_err': 'mean over images of |median annotation - oracle| (paper-style "median distance")'},
                       contrast_def='per subject: metric over images in condition A minus metric over images in condition B; '
                                    'headline = unweighted mean over subjects having both conditions'))
    WL, PL = img.lighting.eq('well_lit'), img.lighting.eq('poorly_lit')
    R['meta']['n_img_lighting'] = img.lighting.fillna('NA').value_counts().to_dict()

    # ---------- (a) lighting paired contrast ----------
    def block(a, b, sub=None):
        I = img if sub is None else img[sub]
        c = contrast(I, a.loc[I.index], b.loc[I.index])
        return c, {m: summarize(c['d_' + m], rng) for m in METRICS}
    cL, sL = block(PL, WL)
    R['a_lighting'] = dict(definition='poorly_lit minus well_lit', summary=sL, per_subject=cL,
                           n_img_poorly=int(PL.sum()), n_img_well=int(WL.sum()),
                           n_subjects_welch_p_lt_05=int((cL.welch_p_img_mean_err < 0.05).sum()))
    # subject-balanced condition levels (mean over 19 subjects of the per-subject condition value)
    R['a_lighting']['subject_balanced_levels'] = {
        f'{m}_{lab}': dict(mean=cL[f'{m}_{s}'].mean(), ci95=list(np.percentile(boot_mean(cL[f'{m}_{s}'], rng), [2.5, 97.5])))
        for m in ['signed_median_err', 'abs_median_err', 'signed_mean_err_ann', 'mean_abs_err_ann'] for s, lab in [('a', 'poorly'), ('b', 'well')]}
    # sensitivities
    sens = {}
    for name, sub in {'unmasked_only': img['mask'].eq(0), 'five_annotation_images_only': img.n.eq(5),
                      'exclude_meta_conflict': ~img.meta_conflict,
                      'exclude_golden_and_challenging': ~(img.is_golden | img.is_challenging)}.items():
        c, s = block(PL, WL, sub)
        sens[name] = {m: dict(mean=s[m]['mean'], ci95=s[m]['ci95'], n_subjects=s[m]['n_subjects']) for m in
                      ['signed_mean_err_img', 'mean_abs_err_ann', 'signed_median_err', 'abs_median_err']}
    R['a_lighting']['sensitivity'] = sens

    # paper-style pooled statistic (image-weighted across subjects) + signed counterpart
    img['one'] = 1.0
    lev = ['poorly_lit', 'well_lit']
    cond = lambda l: img.lighting.eq(l)
    R['a_lighting']['pooled_image_weighted'] = {
        'abs_median_err': pooled(img, cond, lev, 'abs_med_err', 'one', rng),
        'signed_median_err': pooled(img, cond, lev, 'med_err', 'one', rng),
        'mean_abs_err_ann': pooled(img, cond, lev, 'sum_abs', 'n', rng),
        'signed_mean_err_ann': pooled(img, cond, lev, 'sum_err', 'n', rng),
        'pct_images_median_within1': pooled(img.assign(w1=(img.abs_med_err <= 1).astype(float)), cond, lev, 'w1', 'one', rng)}

    # ---------- (b) TOST ----------
    R['b_tost_lighting'] = {m: tost(cL['d_' + m], rng) for m in METRICS}

    # ---------- (c) models ----------
    m = model_frame(d)
    R['c_models'] = dict(n_annotations=len(m), n_images=m.image.nunique(), n_subjects=m.subject.nunique(),
                         covariates=COVS, pose_reference=POSE_REF)
    R['c_models']['ols_subject_fe_err'] = ols_fe_boot(m, rng)
    import statsmodels.formula.api as smf   # self-check: within estimator == dummy-variable OLS; CR1 cluster SE for reference
    ols = smf.ols('err ~ C(subject) + ' + ' + '.join(COVS), m).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(m.subject)[0]})
    assert np.allclose([ols.params[c] for c in COVS], [R['c_models']['ols_subject_fe_err'][c]['coef'] for c in COVS])
    for c in COVS:
        R['c_models']['ols_subject_fe_err'][c]['cr1_cluster_se'] = ols.bse[c]
    t1 = time.time()
    full = ordinal_fit(m, m.subject)
    print('ordinal full fit', round(time.time() - t1, 1), 's', flush=True)
    with Pool(max(1, (os.cpu_count() or 2) - 2), initializer=_init, initargs=(m,)) as pool:
        boots = pool.map(_ord_boot, range(B_ORD), chunksize=10)
    ok = [b for b in boots if 'error' not in b]
    keys = COVS + ['ame_poorly', 'ame_mask'] + ['ame_pose_' + q for q in POSES]
    bd = pd.DataFrame(ok)
    ordres = {k: dict(est=full[k], ci95=list(np.percentile(bd[k], [2.5, 97.5])), ci90=list(np.percentile(bd[k], [5, 95])))
              for k in keys}
    ordres['mean_threshold_spacing'] = full['mean_threshold_spacing']
    ordres['coef_over_spacing_MST_units'] = {c: full[c] / full['mean_threshold_spacing'] for c in COVS}
    ordres['n_boot_ok'] = len(ok); ordres['n_boot_failed'] = len(boots) - len(ok)
    ordres['n_boot_nonconverged'] = int((~bd.converged).sum())
    ordres['full_converged'] = full['converged']
    ordres['note'] = 'logit OrderedModel: mst_annot ~ subject FE + poorly + pose dummies (ref facing_camera) + mask; ' \
                     'coef in log-odds (positive = darker); ame_* = average marginal effect on E[MST] (MST units)'
    R['c_models']['ordinal_logit'] = ordres
    f = 'err ~ poorly + pose_bottom + pose_frontal + pose_side + mask'
    lm = {}
    for name, kw in {'ri_subject_plus_image_vc': dict(vc=True), 'ri_subject_only': dict(vc=False),
                     'ri_plus_random_slope_poorly': dict(vc=False, re_formula='~poorly')}.items():
        try:
            lm[name] = lmm(m, f, **kw)
        except Exception as e:
            lm[name] = dict(error=str(e))
    R['c_models']['lmm_err'] = lm
    # equivalence (90% CI inside +-margin == TOST at alpha .05) for the lighting effect, per estimator
    ci90s = {'subject_contrast_boot': list(np.percentile(boot_mean(cL.d_signed_mean_err_img, rng), [5, 95])),
             'ols_fe_boot': R['c_models']['ols_subject_fe_err']['poorly']['ci90'],
             'ordinal_ame_boot': ordres['ame_poorly']['ci90']}
    ci90s.update({f'lmm_{k}_wald': v['fixed']['poorly']['ci90'] for k, v in lm.items() if 'fixed' in v})
    R['c_models']['lighting_equivalence_by_estimator'] = {
        k: dict(ci90=v, **{f'equiv_pm{mg}': bool(-mg < v[0] and v[1] < mg) for mg in (0.25, 0.5)}, excludes_zero=bool(v[0] > 0 or v[1] < 0))
        for k, v in ci90s.items()}
    print('models done', round(time.time() - t0, 1), 's', flush=True)

    # ---------- (d) lighting effect by oracle level ----------
    lvl = lambda o: 'light_1to3' if o <= 3 else ('mid_4to6' if o <= 6 else 'dark_7to10')
    cL['level'] = cL.oracle.map(lvl)
    dres = {}
    for met in ['signed_mean_err_img', 'mean_abs_err_ann', 'signed_median_err', 'abs_median_err']:
        g = {L: cL.loc[cL.level == L, 'd_' + met].values for L in ['light_1to3', 'mid_4to6', 'dark_7to10']}
        bsg = {L: boot_mean(v, rng) for L, v in g.items()}   # stratified (within-level) subject bootstrap
        r = {L: dict(n_subjects=len(v), mean=v.mean(), ci95=list(np.percentile(bsg[L], [2.5, 97.5])),
                     subjects=cL.loc[cL.level == L, 'subject'].tolist()) for L, v in g.items()}
        dd = bsg['light_1to3'] - bsg['dark_7to10']
        r['light_minus_dark'] = dict(value=g['light_1to3'].mean() - g['dark_7to10'].mean(), ci95=list(np.percentile(dd, [2.5, 97.5])))
        r['kruskal_p'] = stats.kruskal(*g.values()).pvalue
        rho = stats.spearmanr(cL.oracle, cL['d_' + met])
        r['spearman_vs_oracle'] = dict(rho=rho.statistic, p=rho.pvalue)
        sl = stats.linregress(cL.oracle, cL['d_' + met])
        idx = rng.integers(0, len(cL), (B, len(cL)))
        X, Y = cL.oracle.values[idx], cL['d_' + met].values[idx]
        bsl = ((X - X.mean(1, keepdims=True)) * (Y - Y.mean(1, keepdims=True))).sum(1) / ((X - X.mean(1, keepdims=True)) ** 2).sum(1)
        r['ols_slope_per_MST_of_oracle'] = dict(slope=sl.slope, ci95=list(np.nanpercentile(bsl, [2.5, 97.5])), p=sl.pvalue)
        dres[met] = r
    m['oracle_c'] = m.oracle - m.oracle.mean()
    try:
        dres['lmm_interaction'] = lmm(m, 'err ~ poorly * oracle_c + pose_bottom + pose_frontal + pose_side + mask', vc=True)
    except Exception as e:
        dres['lmm_interaction'] = dict(error=str(e))
    dres['note'] = 'floor/ceiling: oracle 1 subjects cannot err below 0 and oracle 10 cannot err above 0'
    R['d_lighting_by_oracle_level'] = dres

    # ---------- (e) golden vs challenging ----------
    G = img[img.is_golden].set_index('subject'); C = img[img.is_challenging].set_index('subject')
    rows = []
    for s in sorted(G.index, key=lambda z: int(z.split('_')[1])):
        g, c = G.loc[s], C.loc[s]
        rows.append(dict(subject=s, oracle=int(g.oracle), gold_median=g.med_annot, chal_median=c.med_annot,
                         gold_mean=g.mean_annot, chal_mean=c.mean_annot, n_gold=int(g.n), n_chal=int(c.n),
                         d_median=c.med_annot - g.med_annot, d_mean=c.mean_annot - g.mean_annot,
                         d_abs_median_err=abs(c.med_err) - abs(g.med_err), d_mean_abs_err=c.mean_abs_err - g.mean_abs_err,
                         gold_pose=g.pose, chal_pose=c.pose, gold_light=g.lighting, chal_light=c.lighting,
                         gold_mask=g['mask'], chal_mask=c['mask'], same_pose=bool(g.pose == c.pose)))
    E = pd.DataFrame(rows)
    R['e_golden_vs_challenging'] = dict(
        definition='challenging minus golden, per subject (one image each); oracle identical so signed diff = diff in annotation',
        per_subject=E, n_same_pose=int(E.same_pose.sum()), n_pairs=len(E),
        summary={k: summarize(E[k], rng) for k in ['d_median', 'd_mean', 'd_abs_median_err', 'd_mean_abs_err']},
        abs_median_err_gold=E.eval('abs(gold_median-oracle)').mean(), abs_median_err_chal=E.eval('abs(chal_median-oracle)').mean(),
        signed_median_err_gold=E.eval('gold_median-oracle').mean(), signed_median_err_chal=E.eval('chal_median-oracle').mean(),
        pct_within1_gold=float((E.eval('abs(gold_median-oracle)') <= 1).mean()), pct_within1_chal=float((E.eval('abs(chal_median-oracle)') <= 1).mean()),
        tost=tost(E.d_mean, rng))

    # ---------- (f) pose and mask ----------
    fres = {}
    REF = img.pose.eq(POSE_REF)
    for q in POSES:
        c, s = block(img.pose.eq(q), REF)
        fres[f'pose_{q}_minus_{POSE_REF}'] = dict(summary=s, tost_signed=tost(c.d_signed_mean_err_img, rng),
                                                   per_subject=c[['subject', 'oracle', 'n_img_a', 'n_img_b', 'd_signed_mean_err_img', 'd_mean_abs_err_ann', 'd_signed_median_err', 'd_abs_median_err']])
    for name, sub in {'all_lighting': None, 'well_lit_only': WL, 'poorly_lit_only': PL}.items():
        c, s = block(img['mask'].eq(1), img['mask'].eq(0), sub)
        fres[f'mask_minus_nomask_{name}'] = dict(summary=s, tost_signed=tost(c.d_signed_mean_err_img, rng),
                                                 per_subject=c[['subject', 'oracle', 'n_img_a', 'n_img_b', 'd_signed_mean_err_img', 'd_mean_abs_err_ann', 'd_signed_median_err', 'd_abs_median_err']])
    imv = img[img.lighting.isin(lev)]
    fres['confounding'] = dict(mask_by_lighting=pd.crosstab(imv['mask'], imv.lighting).to_dict(),
                               pose_by_lighting=pd.crosstab(imv.pose, imv.lighting).to_dict())
    R['f_pose_mask'] = fres

    # ---------- signed shift hiding under equal unsigned distance ----------
    hid = dict(
        n_subjects_signed_shift_gt_0p25=int((cL.d_signed_mean_err_img > 0.25).sum()),
        n_subjects_signed_shift_lt_m0p25=int((cL.d_signed_mean_err_img < -0.25).sum()),
        mean_abs_subject_signed_shift=float(cL.d_signed_mean_err_img.abs().mean()),
        mean_subject_signed_shift=float(cL.d_signed_mean_err_img.mean()))
    # Mechanism: a common darker shift lowers |err| where well-lit bias is negative and raises it where positive.
    bias = cL.signed_mean_err_img_b   # well-lit signed bias (image-mean metric)
    for name, sel in {'well_lit_bias_pos': bias > 0, 'well_lit_bias_neg': bias < 0}.items():
        sub = cL[sel]
        hid[name] = dict(n_subjects=int(len(sub)), subjects=sub.subject.tolist(), oracles=sub.oracle.tolist(),
                         **{k: dict(mean=sub[k].mean(), ci95=list(np.percentile(boot_mean(sub[k], rng), [2.5, 97.5])))
                            for k in ['d_signed_mean_err_img', 'd_mean_abs_err_ann', 'd_signed_median_err', 'd_abs_median_err']})
    rs = stats.spearmanr(bias, cL.d_mean_abs_err_ann)
    hid['spearman_wellbias_vs_d_abs'] = dict(rho=rs.statistic, p=rs.pvalue, n_subjects=len(cL))
    hid['definition'] = ('well_lit bias = per-subject mean over well_lit images of (image mean annotation - oracle); '
                         'groups split by its sign; d_* = poorly_lit minus well_lit per-subject contrasts from (a)')
    R['hiding'] = hid

    R['meta']['runtime_s'] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, 'results.json'), 'w') as fh:
        json.dump(jsonable(R), fh, indent=1)
    print('done', R['meta']['runtime_s'])


if __name__ == '__main__':
    main()

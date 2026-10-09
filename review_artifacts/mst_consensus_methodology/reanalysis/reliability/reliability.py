"""Inter-rater reliability reanalysis of the released MST-E crowd annotations (single region, labelled Ghana).
Run: venv/bin/python -I reliability.py   -> writes results.json next to this file.
All bootstrap CIs: subject-clustered (19 subjects resampled with replacement; duplicated subjects treated as
distinct clusters), B=2000, percentile 2.5/97.5, seed fixed. pos_in_image is NOT a rater identity.
"""
import json, itertools, os, warnings, zlib
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'annotations_clean.csv')
B = 2000
SEED = 20231008
CATS = np.arange(1, 11)

d = pd.read_csv(DATA)
subjects = sorted(d.subject.unique(), key=lambda s: int(s.split('_')[1]))
SIDX = {s: i for i, s in enumerate(subjects)}
NS = len(subjects)
assert NS == 19 and d.image.nunique() == 1482 and len(d) == 7395

# ---------- image-level table ----------
cnt = pd.crosstab(d.image, d.mst_annot).reindex(columns=CATS, fill_value=0)
img = d.groupby('image').agg(subject=('subject', 'first'), oracle=('oracle', 'first'), lighting=('lighting', 'first'),
                             golden=('is_golden', 'first'), chall=('is_challenging', 'first')).loc[cnt.index].reset_index()
CNT = cnt.values.astype(float)                      # n_img x 10 counts
n = CNT.sum(1); s = CNT @ CATS; ss = CNT @ CATS ** 2
img['n'] = n; img['mean'] = s / n
img['si'] = img.subject.map(SIDX).values
SI = img.si.values
band = np.select([img.oracle <= 3, img.oracle <= 7], ['light', 'mid'], 'dark')
img['band'] = band

MASKS = {
    'all_images': np.ones(len(img), bool),
    'golden': img.golden.values,
    'challenging': img.chall.values,
    'well_lit': (img.lighting == 'well_lit').values,
    'poorly_lit': (img.lighting == 'poorly_lit').values,
    'light_oracle_1_3': band == 'light',
    'mid_oracle_4_7': band == 'mid',
    'dark_oracle_8_10': band == 'dark',
}


def boot_w(subj_present, seed_tag):
    """B x NS subject weights: multinomial resampling of the subjects present in a subset."""
    rng = np.random.default_rng([SEED, zlib.crc32(seed_tag.encode())])
    pres = np.flatnonzero(subj_present)
    W = np.zeros((B, NS))
    W[:, pres] = rng.multinomial(len(pres), np.ones(len(pres)) / len(pres), size=B)
    return W


def boot_w_for(mask, tag):
    present = np.zeros(NS, bool); present[np.unique(SI[mask])] = True
    return boot_w(present, tag)


def ci(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]


# ---------- one-way ICC from sufficient statistics (unbalanced-safe, k0) ----------
def icc_oneway(nn, sm, sq, w=None):
    """targets with nn ratings, sum sm, sum of squares sq. w: (R x targets) replicate weights. Returns dict of arrays."""
    w = np.ones((1, len(nn))) if w is None else np.atleast_2d(w)
    a = w.sum(1); N = w @ nn
    gm = (w @ sm) / N
    SSB = w @ (sm ** 2 / nn) - N * gm ** 2
    SSW = w @ (sq - sm ** 2 / nn)
    dfb = a - 1; dfw = N - a
    MSB = SSB / dfb; MSW = SSW / dfw
    k0 = (N - (w @ nn ** 2) / N) / dfb
    with np.errstate(invalid='ignore', divide='ignore'):
        icc1 = (MSB - MSW) / (MSB + (k0 - 1) * MSW)
        icck = (MSB - MSW) / MSB
    return dict(icc1=icc1, icck=icck, MSB=MSB, MSW=MSW, k0=k0, dfb=dfb, dfw=dfw, a=a, N=N)


def mcgraw_wong(r, alpha=0.05):
    F0 = r['MSB'][0] / r['MSW'][0]; dfb = r['dfb'][0]; dfw = r['dfw'][0]; k = r['k0'][0]
    FL = F0 / stats.f.ppf(1 - alpha / 2, dfb, dfw)
    FU = F0 * stats.f.ppf(1 - alpha / 2, dfw, dfb)
    return dict(F=float(F0), df1=float(dfb), df2=float(dfw), p=float(stats.f.sf(F0, dfb, dfw)),
                icc1_ci=[float((FL - 1) / (FL + k - 1)), float((FU - 1) / (FU + k - 1))],
                icck_ci=[float(1 - 1 / FL), float(1 - 1 / FU)])


def sb(r1, k):
    return k * r1 / (1 + (k - 1) * r1)


def icc_images(mask, tag, boot=True):
    """targets = images in mask; subject-clustered bootstrap."""
    r = icc_oneway(n[mask], s[mask], ss[mask])
    out = dict(n_subjects=int(len(np.unique(SI[mask]))), n_images=int(mask.sum()), n_annotations=int(n[mask].sum()),
               k0=float(r['k0'][0]), icc1=float(r['icc1'][0]), icc1_k0=float(r['icck'][0]),
               icc1_k5_SB=float(sb(r['icc1'][0], 5)), **mcgraw_wong(r),
               sd_between_image_means=float(np.std(img['mean'].values[mask], ddof=1)),
               within_image_sd_pooled=float(np.sqrt(r['MSW'][0])))
    if boot:
        W = boot_w_for(mask, tag)[:, SI[mask]]
        rb = icc_oneway(n[mask], s[mask], ss[mask], W)
        out['icc1_boot_ci'] = ci(rb['icc1']); out['icc1_k0_boot_ci'] = ci(rb['icck'])
    return out


R = {}
# ================= (a) ICC(1) =================
A = {}
for k in ['golden', 'challenging', 'well_lit', 'poorly_lit', 'all_images']:
    A[k] = icc_images(MASKS[k], 'icc_' + k)
A['per_subject_i_targets_all_images'] = A['all_images']

# (ii) targets = subjects
subj_ann = d.groupby('subject').mst_annot.agg(['size', 'sum', lambda x: (x ** 2).sum()]).loc[subjects].values.astype(float)
img_means = img.groupby('subject')['mean'].agg(['size', 'sum', lambda x: (x ** 2).sum()]).loc[subjects].values
img['median'] = d.groupby('image').mst_annot.median().loc[img.image].values
img_meds = img.groupby('subject')['median'].agg(['size', 'sum', lambda x: (x ** 2).sum()]).loc[subjects].values
Wsub = boot_w(np.ones(NS, bool), 'subjects')
for name, arr, desc in [
        ('per_subject_ii_a_annotations_as_replicates', subj_ann,
         'targets=19 subjects; replicates = every individual annotation of every image of that subject (n per subject 190-552)'),
        ('per_subject_ii_b_image_means_as_replicates', img_means,
         'targets=19 subjects; replicates = per-image mean rating (38-111 images per subject)'),
        ('per_subject_ii_c_image_medians_as_replicates', img_meds,
         'targets=19 subjects; replicates = per-image median rating')]:
    r = icc_oneway(arr[:, 0], arr[:, 1], arr[:, 2])
    rb = icc_oneway(arr[:, 0], arr[:, 1], arr[:, 2], Wsub)
    A[name] = dict(definition=desc, n_subjects=NS, n_replicates_total=int(arr[:, 0].sum()), k0=float(r['k0'][0]),
                   icc1=float(r['icc1'][0]), icc1_k0=float(r['icck'][0]), icc1_k5_SB=float(sb(r['icc1'][0], 5)),
                   **mcgraw_wong(r), icc1_boot_ci=ci(rb['icc1']))

# (iii) within each subject: targets = that subject's images
per = []
for si, sub in enumerate(subjects):
    m = SI == si
    r = icc_oneway(n[m], s[m], ss[m])
    mw = mcgraw_wong(r)
    per.append(dict(subject=sub, oracle=int(img.oracle[m].iloc[0]), n_images=int(m.sum()), icc1=float(r['icc1'][0]),
                    icc1_ci=mw['icc1_ci'], icc1_k0=float(r['icck'][0]), p=mw['p'],
                    sd_image_means=float(np.std(img['mean'][m], ddof=1)), within_image_sd=float(np.sqrt(r['MSW'][0]))))
iii = np.array([p['icc1'] for p in per])
iiik = np.array([p['icc1_k0'] for p in per])
bmean = Wsub @ iii / NS
bmed = [np.median(np.repeat(iii, w.astype(int))) for w in Wsub]
A['per_subject_iii_within_subject'] = dict(
    definition='ICC(1) computed separately within each subject with targets = that subject\'s images',
    per_subject=per, mean_icc1=float(iii.mean()), mean_icc1_boot_ci=ci(bmean), median_icc1=float(np.median(iii)),
    median_icc1_boot_ci=ci(bmed), min_icc1=float(iii.min()), max_icc1=float(iii.max()),
    n_subjects_p_lt_05=int(sum(p['p'] < .05 for p in per)), median_icc1_k0=float(np.median(iiik)),
    min_icc1_k0=float(iiik.min()), max_icc1_k0=float(iiik.max()))
A['paper_ranges'] = dict(per_subject=[0.86, 0.94], golden=[0.90, 0.96], challenging=[0.82, 0.95],
                         note='paper ranges are across 5 regions + global pool (25 ratings/image); here 1 region, <=5 ratings/image')
R['a_icc'] = A

# cross-check against pingouin on balanced data
try:
    import pingouin as pg
    chk = {}
    for k in ['golden', 'all_images']:
        ims = set(img.image[MASKS[k] & (n == 5)])
        dd = d[d.image.isin(ims)]
        t = pg.intraclass_corr(dd, targets='image', raters='pos_in_image', ratings='mst_annot').set_index('Type')
        mine = icc_oneway(n[MASKS[k] & (n == 5)], s[MASKS[k] & (n == 5)], ss[MASKS[k] & (n == 5)])
        assert abs(t.loc['ICC(1,1)', 'ICC'] - mine['icc1'][0]) < 1e-9, (k, t.loc['ICC(1,1)', 'ICC'], mine['icc1'][0])
        assert abs(t.loc['ICC(1,k)', 'ICC'] - mine['icck'][0]) < 1e-9
        chk[k + '_balanced_5'] = dict(pingouin_ICC1=float(t.loc['ICC(1,1)', 'ICC']), pingouin_CI=list(map(float, t.loc['ICC(1,1)', 'CI95'])),
                                      mine=float(mine['icc1'][0]), mine_CI=mcgraw_wong(mine)['icc1_ci'])
    R['crosscheck_pingouin'] = chk
except ImportError:
    pass

# ================= (b) agreement metrics =================
pairs = n * (n - 1) / 2
exact_p = (CNT * (CNT - 1) / 2).sum(1)
adj_p = (CNT[:, :-1] * CNT[:, 1:]).sum(1)
within1_p = exact_p + adj_p
absdiff_sum = sum(CNT[:, i] * CNT[:, j] * (j - i) for i in range(10) for j in range(i + 1, 10))
sqdiff_sum = n * ss - s ** 2                     # sum over unordered pairs of (x-y)^2

# Krippendorff coincidence matrix per image -> per subject
O_img = (CNT[:, :, None] * CNT[:, None, :] - CNT[:, :, None] * np.eye(10)[None]) / (n - 1)[:, None, None]


def kalpha(O, metric):
    nc = O.sum(1); N = nc.sum()
    if metric == 'interval':
        D2 = (CATS[:, None] - CATS[None, :]) ** 2.0
    elif metric == 'nominal':
        D2 = 1 - np.eye(10)
    else:  # ordinal
        cum = np.cumsum(nc); idx = np.arange(10)
        lo = np.minimum.outer(idx, idx); hi = np.maximum.outer(idx, idx)
        D2 = (cum[hi] - cum[lo] + nc[lo] - (nc[:, None] + nc[None, :]) / 2) ** 2
    Do = (O * D2).sum() / N
    De = (np.outer(nc, nc) * D2).sum() / (N * (N - 1))
    return 1 - Do / De


def agreement(mask, tag):
    W = boot_w_for(mask, 'agr_' + tag)
    def by_subj(v):
        out = np.zeros(NS); np.add.at(out, SI[mask], v[mask]); return out
    P, E, W1, AD, SQ = map(by_subj, [pairs, exact_p, within1_p, absdiff_sum, sqdiff_sum])
    Csub = np.zeros((NS, 10)); np.add.at(Csub, SI[mask], CNT[mask])
    Osub = np.zeros((NS, 10, 10)); np.add.at(Osub, SI[mask], O_img[mask])

    def stat(w):
        p = w @ P
        marg = w @ Csub; pm = marg / marg.sum()
        var_p = pm @ CATS ** 2 - (pm @ CATS) ** 2
        po_q = 1 - (w @ SQ) / p / 81
        pe_q = 1 - 2 * var_p / 81
        O = np.tensordot(w, Osub, 1)
        return dict(pair_exact=(w @ E) / p, pair_within1=(w @ W1) / p, pair_mean_abs_diff=(w @ AD) / p,
                    pair_mean_sq_diff=(w @ SQ) / p,
                    chance_exact=pm @ pm, chance_within1=float(pm @ pm + 2 * (pm[:-1] @ pm[1:])),
                    quad_weighted_agreement_Po=po_q, quad_weighted_chance_Pe=pe_q,
                    quad_weighted_kappa_fleiss_type=(po_q - pe_q) / (1 - pe_q),
                    kripp_alpha_ordinal=kalpha(O, 'ordinal'), kripp_alpha_interval=kalpha(O, 'interval'),
                    kripp_alpha_nominal=kalpha(O, 'nominal'))
    pt = stat(np.ones(NS) * (np.isin(np.arange(NS), SI[mask])))
    bs = [stat(w) for w in W]
    out = dict(n_subjects=int(len(np.unique(SI[mask]))), n_images=int(mask.sum()), n_pairs=int(pairs[mask].sum()))
    for key in pt:
        out[key] = float(pt[key]); out[key + '_boot_ci'] = ci([b[key] for b in bs])
    out['image_weighted_exact'] = float(np.mean(exact_p[mask] / pairs[mask]))
    out['image_weighted_within1'] = float(np.mean(within1_p[mask] / pairs[mask]))
    return out


Bres = {k: agreement(m, k) for k, m in MASKS.items()}
# pseudo-rater Cohen quadratic kappa over position slots (positions are NOT persons; shown only as a variant)
from sklearn.metrics import cohen_kappa_score
piv = d.pivot(index='image', columns='pos_in_image', values='mst_annot').loc[img.image]
for k in ['all_images', 'golden', 'challenging']:
    kk = []
    for i, j in itertools.combinations(range(1, 6), 2):
        sub = piv[MASKS[k]][[i, j]].dropna()
        kk.append(cohen_kappa_score(sub[i], sub[j], weights='quadratic', labels=CATS))
    Bres[k]['pseudo_slot_pair_cohen_quadratic_kappa_mean'] = float(np.mean(kk))
    Bres[k]['pseudo_slot_pair_cohen_quadratic_kappa_range'] = [float(min(kk)), float(max(kk))]
# cross-check alpha against krippendorff package
import krippendorff
rel = piv.T.values.astype(float)
for met in ['ordinal', 'interval', 'nominal']:
    pk = krippendorff.alpha(reliability_data=rel, level_of_measurement=met, value_domain=list(CATS))
    assert abs(pk - Bres['all_images']['kripp_alpha_' + met]) < 1e-6, (met, pk)
R['b_agreement'] = Bres

# ================= (c) variance decomposition =================
# (c1) linear mixed model, REML: subject and image(subject) random intercepts
import statsmodels.formula.api as smf
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    md = smf.mixedlm('mst_annot ~ 1', d, groups='subject', re_formula='1', vc_formula={'image': '0 + C(image)'})
    fit = md.fit(reml=True, method=['lbfgs'])
v_subj = float(fit.cov_re.iloc[0, 0]); v_img = float(fit.vcomp[0]); v_res = float(fit.scale)
tot = v_subj + v_img + v_res
Cc = dict(lmm_reml=dict(var_subject=v_subj, var_image_within_subject=v_img, var_residual_within_image=v_res,
                        share_subject=v_subj / tot, share_image=v_img / tot, share_residual=v_res / tot,
                        single_rater_error_sd=np.sqrt(v_res), sd_single_rating_about_subject_mean=np.sqrt(v_img + v_res),
                        sd_true_image_about_subject=np.sqrt(v_img), converged=bool(fit.converged),
                        implied_icc_image_target=(v_subj + v_img) / tot, implied_icc_subject_target_single_rating=v_subj / tot,
                        implied_icc_within_subject_images=v_img / (v_img + v_res)))

# (c2) unbalanced nested ANOVA (method of moments) with subject-clustered bootstrap
img['ssw'] = ss - s ** 2 / n
g = img.groupby('si')
nsub = g.n.sum().values; bsub = g.size().values.astype(float)
ybar_s = (g.apply(lambda x: (x.n * x['mean']).sum(), include_groups=False) / g.n.sum()).values
SSE_s = g.ssw.sum().values; dfE_s = nsub - bsub
SSB_s = g.apply(lambda x: (x.n * (x['mean'] - (x.n * x['mean']).sum() / x.n.sum()) ** 2).sum(), include_groups=False).values
n2_s = g.apply(lambda x: (x.n ** 2).sum(), include_groups=False).values


def nested_moments(w):
    w = np.atleast_2d(w)
    N = w @ nsub
    MSE = (w @ SSE_s) / (w @ dfE_s)
    dfB = w @ (bsub - 1); MSB = (w @ SSB_s) / dfB
    gm = (w @ (nsub * ybar_s)) / N
    dfA = w.sum(1) - 1; MSA = (w @ (nsub * ybar_s ** 2) - N * gm ** 2) / dfA
    k1 = (N - w @ (n2_s / nsub)) / dfB
    k2 = (w @ (n2_s / nsub) - (w @ n2_s) / N) / dfA
    k3 = (N - (w @ nsub ** 2) / N) / dfA
    ve = MSE; vb = (MSB - MSE) / k1; va = (MSA - ve - k2 * vb) / k3
    t = va + vb + ve
    return dict(var_subject=va, var_image_within_subject=vb, var_residual_within_image=ve,
                share_subject=va / t, share_image=vb / t, share_residual=ve / t, single_rater_error_sd=np.sqrt(ve))


pt = nested_moments(np.ones(NS)); bs = nested_moments(Wsub)
Cc['anova_moments'] = {k: float(pt[k][0]) for k in pt}
Cc['anova_moments_boot_ci'] = {k: ci(bs[k]) for k in bs}
Cc['n'] = '19 subjects / 1482 images / 7395 annotations'
Cc['note'] = ('No annotator IDs: the within-image residual mixes rater leniency (main effect), rater x image interaction '
              'and pure error; it cannot be split. Image(subject) variance = true between-image change in perceived tone '
              '(lighting/pose) as seen through the crowd.')
R['c_variance'] = Cc

# ================= (d) dependence of ICC on target spread =================
Dd = {'within_band_all_images': {k: icc_images(MASKS[k], 'band_' + k) for k in ['light_oracle_1_3', 'mid_oracle_4_7', 'dark_oracle_8_10']}}
Dd['golden_within_band'] = {}
Dd['challenging_within_band'] = {}
for b in ['light', 'mid', 'dark']:
    for setname, base in [('golden_within_band', 'golden'), ('challenging_within_band', 'challenging')]:
        m = MASKS[base] & (band == b)
        Dd[setname][b] = icc_images(m, f'{setname}_{b}', boot=True)

# Golden-like random draws: one random image per subject, from a pool; optionally restricted oracle window.
rng = np.random.default_rng(SEED + 1)
NDRAW = 2000
pool_masks = {'any_image': np.ones(len(img), bool), 'well_lit_only': MASKS['well_lit'], 'poorly_lit_only': MASKS['poorly_lit']}
windows = {'all_19_subjects': (1, 10), 'light_1_3': (1, 3), 'mid_4_7': (4, 7), 'dark_8_10': (8, 10)}
windows.update({f'window_{lo}_{lo + 2}': (lo, lo + 2) for lo in range(1, 9)})
GL = {}
for pname, pm in pool_masks.items():
    # draw indicator matrix NDRAW x n_img with one image per subject
    Wd = np.zeros((NDRAW, len(img)))
    for si in range(NS):
        cand = np.flatnonzero(pm & (SI == si))
        Wd[np.arange(NDRAW), rng.choice(cand, NDRAW)] = 1
    for wname, (lo, hi) in windows.items():
        keep = ((img.oracle >= lo) & (img.oracle <= hi)).values
        nsj = len(np.unique(SI[keep]))
        if nsj < 3:
            continue
        r = icc_oneway(n, s, ss, Wd * keep)
        m_ = img['mean'].values
        sdm = np.array([np.std(m_[(w * keep) > 0], ddof=1) for w in Wd[:200]])
        GL[f'{pname}|{wname}'] = dict(n_subjects=nsj, oracle_window=[lo, hi], icc1_median=float(np.median(r['icc1'])),
                                      icc1_draw_2p5_97p5=ci(r['icc1']),
                                      within_image_sd_median=float(np.median(np.sqrt(r['MSW']))),
                                      sd_image_means_median_first200=float(np.median(sdm)))
Dd['golden_like_random_draws'] = GL
Dd['note'] = ('golden_like_random_draws: 2000 draws of one random image per subject (subjects within the oracle window), '
              'interval = 2.5/97.5 percentiles over draws (Monte Carlo spread of the design, not a sampling CI).')
R['d_spread'] = Dd

# ================= (e) empirical k-rater analysis vs Spearman-Brown =================
five = n == 5
X = np.sort(piv.values[five].astype(float), axis=1)           # 1467 x 5 (order within image irrelevant)
orc = img.oracle.values[five].astype(float)
si5 = SI[five]
med5 = np.median(X, axis=1)
metric_names = ['vs5_exact', 'vs5_within1', 'vs5_mae', 'vs5_exact_randtie', 'vs5_within1_randtie',
                'heldout_exact', 'heldout_within1', 'heldout_mae',
                'oracle_exact', 'oracle_within1', 'oracle_mae', 'oracle_exact_randtie', 'oracle_within1_randtie',
                'oracle_signed']
per_img = {}
for k in range(1, 6):
    acc = {m: np.zeros(len(X)) for m in metric_names}
    combos = list(itertools.combinations(range(5), k))
    for cmb in combos:
        sub = np.sort(X[:, cmb], axis=1)
        med = np.median(sub, axis=1); lo = sub[:, (k - 1) // 2]; hi = sub[:, k // 2]
        for ref, pre in [(med5, 'vs5'), (orc, 'oracle')]:
            acc[pre + '_exact'] += (med == ref)
            acc[pre + '_within1'] += (np.abs(med - ref) <= 1)
            acc[pre + '_mae'] += np.abs(med - ref)
            acc[pre + '_exact_randtie'] += 0.5 * ((lo == ref).astype(float) + (hi == ref))
            acc[pre + '_within1_randtie'] += 0.5 * ((np.abs(lo - ref) <= 1).astype(float) + (np.abs(hi - ref) <= 1))
        acc['oracle_signed'] += med - orc
        if k < 5:
            rest = [j for j in range(5) if j not in cmb]
            hmed = np.median(X[:, rest], axis=1)
            acc['heldout_exact'] += (med == hmed); acc['heldout_within1'] += (np.abs(med - hmed) <= 1)
            acc['heldout_mae'] += np.abs(med - hmed)
    per_img[k] = {m: v / len(combos) for m, v in acc.items()}

e_masks = {key: MASKS[key][five] for key in ['all_images', 'golden', 'challenging', 'well_lit', 'poorly_lit']}
E = {}
for sname, m in e_masks.items():
    W = boot_w_for(MASKS[sname] & five, 'e_' + sname)
    cnt_s = np.bincount(si5[m], minlength=NS).astype(float)
    pres = cnt_s > 0
    rows = {}
    for k in range(1, 6):
        row = {}
        for mt in metric_names:
            if k == 5 and mt.startswith(('heldout', 'vs5')):
                continue
            v = per_img[k][mt]
            sums = np.bincount(si5[m], weights=v[m], minlength=NS)
            row[mt] = float(sums.sum() / cnt_s.sum())
            row[mt + '_boot_ci'] = ci((W @ sums) / (W @ cnt_s))
            if mt.startswith('oracle'):
                smean = np.where(pres, sums / np.maximum(cnt_s, 1), 0)
                row[mt + '_subject_weighted'] = float(smean[pres].mean())
        rows[f'k={k}'] = row
    # Spearman-Brown from the subset's ICC(1) (images as targets, 5-rating images)
    r = icc_oneway(n[MASKS[sname] & five], s[MASKS[sname] & five], ss[MASKS[sname] & five])
    r1 = float(r['icc1'][0])
    # empirical reliability of k-rater mean for k=1,2: one-way ICC(1) on two disjoint k-subsets, averaged over partitions
    emp = {}
    for k in (1, 2):
        vals = []
        for A_ in itertools.combinations(range(5), k):
            for B_ in itertools.combinations([j for j in range(5) if j not in A_], k):
                if A_ < B_:
                    a_ = X[m][:, A_].mean(1); b_ = X[m][:, B_].mean(1)
                    pair = np.c_[a_, b_]
                    rr = icc_oneway(np.full(len(pair), 2.), pair.sum(1), (pair ** 2).sum(1))
                    vals.append(float(rr['icc1'][0]))
        emp[f'k={k}'] = dict(mean_icc1_two_disjoint_k_means=float(np.mean(vals)), n_partitions=len(vals),
                             min=float(min(vals)), max=float(max(vals)))
    E[sname] = dict(n_subjects=int(pres.sum()), n_images=int(m.sum()), by_k=rows,
                    spearman_brown=dict(icc1_single=r1, **{f'k={k}': float(sb(r1, k)) for k in (1, 2, 3, 4, 5, 10, 25)},
                                        k_needed_for_0p80=float(0.8 * (1 - r1) / (r1 * 0.2)),
                                        k_needed_for_0p90=float(0.9 * (1 - r1) / (r1 * 0.1)),
                                        k_needed_for_0p95=float(0.95 * (1 - r1) / (r1 * 0.05))),
                    empirical_k_rater_reliability=emp)

# subject-level consensus from k raters per image across all of the subject's images, vs oracle
rngs = np.random.default_rng(SEED + 2)
NSIM = 500
Xall = piv.values.astype(float)                                   # 1482 x 5 with NaN for 4-rating images
oracle_s = img.groupby('si').oracle.first().values.astype(float)
SUBJ = {}
for k in range(1, 6):
    w1, mae, ex, w1m = [], [], [], []
    for _ in range(NSIM if k < 5 else 1):
        keys = rngs.random(Xall.shape); keys[np.isnan(Xall)] = np.inf
        order = np.argsort(keys, 1)[:, :k]
        sel = np.take_along_axis(Xall, order, 1)
        cons = np.array([np.nanmedian(sel[SI == si]) for si in range(NS)])               # pooled median
        imed = np.nanmedian(sel, 1)
        cons2 = np.array([np.median(imed[SI == si]) for si in range(NS)])                # median of image medians
        dv = np.abs(cons - oracle_s)
        w1.append((dv <= 1).mean()); mae.append(dv.mean()); ex.append((dv == 0).mean())
        w1m.append((np.abs(cons2 - oracle_s) <= 1).mean())
    SUBJ[f'k={k}'] = dict(pooled_median_within1_mean=float(np.mean(w1)), pooled_median_within1_mc_2p5_97p5=ci(w1),
                          pooled_median_mae_mean=float(np.mean(mae)), pooled_median_mae_mc_2p5_97p5=ci(mae),
                          pooled_median_exact_mean=float(np.mean(ex)),
                          median_of_image_medians_within1_mean=float(np.mean(w1m)), n_sims=len(w1))
E['subject_level_consensus_vs_oracle'] = dict(
    definition=('for each of 19 subjects, take k random raters per image (all images of the subject; 4-rating images '
                'contribute min(k,4)); consensus = median of all selected ratings (pooled) or median of image medians; '
                'compare with oracle. Intervals = Monte Carlo 2.5/97.5 over 500 rater draws (not a sampling CI; n=19 subjects).'),
    by_k=SUBJ,
    full_data_per_subject=[dict(subject=sub, oracle=int(oracle_s[si]), pooled_median_all=float(np.median(d.mst_annot[d.subject == sub])),
                                mean_all=float(d.mst_annot[d.subject == sub].mean())) for si, sub in enumerate(subjects)])
E['note'] = ('Only the 1467 images with 5 ratings are used (15 four-rating images dropped; this removes 1 Challenging image -> '
             'Challenging n=18). vs5 compares the k-rater median with the 5-rater median that CONTAINS those k raters '
             '(inflated by overlap); heldout compares with the median of the other 5-k raters (disjoint). Even-k medians can be '
             'x.5: "raw" uses np.median; heldout for k=2 and k=3 are the same comparisons (2 vs other 3);  "randtie" = expected value when the tie is broken at random (mean of lower/upper median).')
R['e_k_raters'] = E

R['meta'] = dict(data=DATA, n='19 subjects / 1482 images (1467x5 + 15x4 ratings) / 7395 annotations, one region (labelled Ghana)',
                 bootstrap=f'subject-clustered, B={B}, percentile, seed={SEED}', bands='light: oracle 1-3 (7 subj); mid: 4-7 (7 subj); dark: 8-10 (5 subj)')


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        if not np.isfinite(o):
            return None
        return float(f'{float(o):.4g}') if 0 < abs(o) < 1e-3 else round(float(o), 5)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


with open(os.path.join(HERE, 'results.json'), 'w') as f:
    json.dump(clean(R), f, indent=1)
print('wrote results.json')

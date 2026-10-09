"""Agreement of MST-E crowd annotations (released file = one region, labelled Ghana) with the oracle (Dr. Monk).

Run: <venv>/bin/python -I oracle_agreement.py   -> writes results.json next to this script.
All CIs: subject-clustered percentile bootstrap, B resamples of the 19 subjects with replacement,
one shared resample matrix (so differences between conditions are paired), fixed seed.
"""
import json
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from scipy import stats

S = Path('/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/'
         '258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad')
OUT = Path(__file__).resolve().parent
B, SEED = 4000, 20231008

d = pd.read_csv(S / 'reanalysis/annotations_clean.csv')
assert len(d) == 7395 and d.image.nunique() == 1482 and d.subject.nunique() == 19
assert (d.groupby('subject').oracle.nunique() == 1).all()

SUBJ = sorted(d.subject.unique(), key=lambda s: int(s.split('_')[1]))
SIDX = {s: i for i, s in enumerate(SUBJ)}
NS = len(SUBJ)
rng = np.random.default_rng(SEED)
BOOT = np.stack([np.bincount(rng.integers(0, NS, NS), minlength=NS) for _ in range(B)]).astype(float)
MET = ['exact', 'within1', 'abs', 'signed']


def r(x, k=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), k)


def ci(a):
    return [r(np.nanpercentile(a, 2.5)), r(np.nanpercentile(a, 97.5))]


def unit_metrics(pred, oracle):
    e = np.asarray(pred, float) - np.asarray(oracle, float)
    return np.c_[e == 0, np.abs(e) <= 1, np.abs(e), e].astype(float)


def summ(subj, M, names=MET):
    """Image(unit)-weighted and subject-weighted means of the columns of M, with clustered-bootstrap CIs.
    Returns (json dict, dict of bootstrap arrays for paired differences)."""
    s = np.array([SIDX[x] for x in subj])
    n = np.bincount(s, minlength=NS).astype(float)
    sums = np.stack([np.bincount(s, M[:, j], minlength=NS) for j in range(M.shape[1])], 1)
    pres = n > 0
    means = np.divide(sums, n[:, None], out=np.zeros_like(sums), where=pres[:, None])

    def stat(C):
        Cp = C * pres
        return (C @ sums) / (C @ n)[:, None], (Cp @ means) / Cp.sum(1)[:, None]

    pi, ps = stat(np.ones((1, NS)))
    bi, bs = stat(BOOT)
    res = {'n_units': int(n.sum()), 'n_subjects': int(pres.sum())}
    for j, nm in enumerate(names):
        res[nm] = {'unit_weighted': r(pi[0, j]), 'unit_weighted_ci95': ci(bi[:, j]),
                   'subject_weighted': r(ps[0, j]), 'subject_weighted_ci95': ci(bs[:, j])}
    return res, {'unit': bi, 'subj': bs, 'pt_unit': pi[0], 'pt_subj': ps[0]}


def diff(b1, b2, names=MET):
    out = {}
    for j, nm in enumerate(names):
        out[nm] = {w: {'point': r(b1['pt_' + w][j] - b2['pt_' + w][j]), 'ci95': ci(b1[w][:, j] - b2[w][:, j])}
                   for w in ('unit', 'subj')}
    return out


# ---------------------------------------------------------------- per-image medians
g = d.groupby('image')
img = g.agg(subject=('subject', 'first'), oracle=('oracle', 'first'), lighting=('lighting', 'first'),
            golden=('is_golden', 'first'), chall=('is_challenging', 'first'), pose=('pose', 'first'),
            mask=('mask', 'first'), n=('mst_annot', 'size'), med_mid=('mst_annot', 'median'))
img['med_lo'] = g.mst_annot.apply(lambda x: np.sort(x.values)[(len(x) - 1) // 2])  # lower median
img['med_hi'] = g.mst_annot.apply(lambda x: np.sort(x.values)[len(x) // 2])        # upper median
img['med_absdev'] = g.err.apply(lambda x: np.median(np.abs(x.values)))  # alt reading: median of |a-o|
img = img.reset_index()
n_half = int((img.med_mid % 1 != 0).sum())
VARIANTS = {
    'mid': ('med_mid', img.index),        # average of middle two for 4-rating images (can be x.5)
    'low': ('med_lo', img.index),
    'high': ('med_hi', img.index),
    'drop4': ('med_mid', img.index[img.n == 5]),
}

pmf = d.mst_annot.value_counts(normalize=True).reindex(range(1, 11), fill_value=0).values
F = np.cumsum(pmf)
cdf_med5 = sum(comb(5, j) * F ** j * (1 - F) ** (5 - j) for j in range(3, 6))
pmf_med5 = np.diff(np.r_[0, cdf_med5])
K = np.arange(1, 11)


def expected_metrics(q, oracle):
    o = np.asarray(oracle)[:, None]
    e = K[None, :] - o
    return np.c_[(q * (e == 0)).sum(1), (q * (np.abs(e) <= 1)).sum(1), (q * np.abs(e)).sum(1), (q * e).sum(1)]


def baselines(subj, oracle, chance_q):
    out = {'uniform_1_10': summ(subj, expected_metrics(np.full(10, .1), oracle))[0],
           'marginal_chance': summ(subj, expected_metrics(chance_q, oracle))[0]}
    o = np.asarray(oracle, float)
    cmae = {c: np.abs(c - o).mean() for c in K}
    cw1 = {c: (np.abs(c - o) <= 1).mean() for c in K}
    best_mae, best_w1 = min(cmae, key=cmae.get), max(cw1, key=cw1.get)
    out['best_constant_by_MAE'] = {'c': int(best_mae), **summ(subj, unit_metrics(np.full(len(o), best_mae), o))[0]}
    out['best_constant_by_within1'] = {'c': int(best_w1), **summ(subj, unit_metrics(np.full(len(o), best_w1), o))[0]}
    out['constant_scan_unit_weighted'] = {int(c): {'MAE': r(cmae[c]), 'within1': r(cw1[c])} for c in K}
    return out


R = {'meta': {'B': B, 'seed': SEED, 'n_annotations': len(d), 'n_images': len(img), 'n_subjects': NS,
              'n_images_4_ratings': int((img.n == 4).sum()), 'n_images_half_median_mid': n_half,
              'annotation_pmf_1_10': [r(x) for x in pmf], 'median_of_5_marginal_pmf_1_10': [r(x) for x in pmf_med5]}}

# (a) all images, every even-median variant
R['a_image_median_all'] = {}
for v, (col, idx) in VARIANTS.items():
    sub = img.loc[idx]
    R['a_image_median_all'][v] = summ(sub.subject, unit_metrics(sub[col], sub.oracle))[0]
R['a_baselines_image_level'] = baselines(img.subject, img.oracle, pmf_med5)
R['a_baselines_image_level']['note'] = ('marginal_chance here = median of 5 iid draws from the pooled annotation pmf '
                                        '(ignores the image); uniform = one uniform draw on 1..10; best constants '
                                        'chosen in-sample (optimistic), CIs ignore the selection')

# (b) conditions (main variant 'mid'; also 'low'/'high' where 4-rating images enter)
conds = {
    'golden': img.golden, 'challenging': img.chall,
    'well_lit': img.lighting == 'well_lit', 'poorly_lit': img.lighting == 'poorly_lit',
    'mask_1': img['mask'] == 1, 'mask_0': img['mask'] == 0,
    **{f'pose_{p}': img.pose == p for p in ['facing_camera', 'side', 'bottom', 'frontal']},
}
R['b_conditions'], bootc = {}, {}
for c, m in conds.items():
    sub = img[m]
    R['b_conditions'][c] = {}
    for v in ('mid', 'low', 'high'):
        res, bb = summ(sub.subject, unit_metrics(sub[VARIANTS[v][0]], sub.oracle))
        R['b_conditions'][c][v] = res
        if v == 'mid':
            bootc[c] = bb
    R['b_conditions'][c]['n_4rating_images'] = int((sub.n == 4).sum())
R['b_conditions']['golden']['baselines'] = baselines(img[img.golden].subject, img[img.golden].oracle, pmf_med5)
R['b_conditions']['challenging']['baselines'] = baselines(img[img.chall].subject, img[img.chall].oracle, pmf_med5)
R['ab_alt_definition_median_of_abs_dev'] = {
    'definition': 'per image median over raters of |annotation - oracle| (midpoint for 4 ratings), then averaged',
    **{c: {k: v for k, v in summ(sub.subject, unit_metrics(sub.med_absdev, 0 * sub.med_absdev))[0].items()
           if k in ('n_units', 'n_subjects', 'abs')}
       for c, sub in {'all': img, **{c: img[conds[c]] for c in ('golden', 'challenging', 'well_lit', 'poorly_lit')}}.items()}}
R['b_diff_well_minus_poorly_lit_mid'] = diff(bootc['well_lit'], bootc['poorly_lit'])
R['b_diff_golden_minus_challenging_mid'] = diff(bootc['golden'], bootc['challenging'])
R['b_conditions']['max_abs_distance_any_condition_mid'] = r(max(
    R['b_conditions'][c]['mid']['abs']['unit_weighted'] for c in conds))
# golden vs challenging per subject (one image each) for the record
gc = img[img.golden | img.chall][['subject', 'oracle', 'golden', 'med_mid', 'lighting']]
R['b_golden_challenging_per_subject'] = {
    s: {'oracle': int(x.oracle.iloc[0]),
        'golden_median': r(x[x.golden].med_mid.iloc[0]), 'challenging_median': r(x[~x.golden].med_mid.iloc[0])}
    for s, x in gc.groupby('subject')}

# (c) per-subject consensus
ps = d.groupby('subject').agg(oracle=('oracle', 'first'), n_ann=('mst_annot', 'size'), n_img=('image', 'nunique'),
                              pooled_median=('mst_annot', 'median'), mean=('mst_annot', 'mean'))
ps['median_of_image_medians'] = img.groupby('subject').med_mid.median()
ps['median_of_image_medians_low'] = img.groupby('subject').med_lo.median()
ps['pct_images_median_within1'] = img.assign(w=(img.med_mid - img.oracle).abs() <= 1).groupby('subject').w.mean()
ps['image_level_MAD'] = img.assign(a=(img.med_mid - img.oracle).abs()).groupby('subject').a.mean()
ps = ps.loc[SUBJ]
# within-subject stability of the pooled median: resample the subject's images (with all their annotations)
rng2 = np.random.default_rng(SEED + 1)
stab, okmat = {}, []
for s in SUBJ:
    vals = [x.values for _, x in d[d.subject == s].groupby('image').mst_annot]
    o = ps.loc[s, 'oracle']
    meds = np.array([np.median(np.concatenate([vals[i] for i in rng2.integers(0, len(vals), len(vals))]))
                     for _ in range(2000)])
    okmat.append(np.abs(meds - o) <= 1)
    stab[s] = {'P_within1': r((np.abs(meds - o) <= 1).mean()),
               'pooled_median_resample_values': {str(k): int(v) for k, v in zip(*np.unique(meds, return_counts=True))}}
cnt = np.sum(okmat, 0)  # subjects within 1 per joint replicate (subjects resampled independently)
R['c_within_image_resample_count_within1_of_19'] = {int(k): r(v / len(cnt)) for k, v in zip(*np.unique(cnt, return_counts=True))}
R['c_per_subject_table'] = {s: {**{k: (r(v) if isinstance(v, float) else int(v)) for k, v in ps.loc[s].items()},
                                'within_image_resample_stability': stab[s]} for s in SUBJ}
R['c_subject_consensus'] = {}
for col in ['pooled_median', 'median_of_image_medians', 'median_of_image_medians_low', 'mean']:
    e = ps[col] - ps.oracle
    k1, k0 = int((e.abs() <= 1).sum()), int((e == 0).sum())
    R['c_subject_consensus'][col] = {
        'n_within1_of_19': k1, 'pct_within1': r(100 * k1 / NS, 2),
        'within1_clopper_pearson95': [r(x) for x in stats.binomtest(k1, NS).proportion_ci(method='exact')],
        'n_exact_of_19': k0,
        'failing_subjects': {s: r(e[s]) for s in e.index[e.abs() > 1]},
        'summary': summ(ps.index, unit_metrics(ps[col], ps.oracle))[0],
    }
R['c_subject_baselines'] = baselines(ps.index, ps.oracle, pmf)
R['c_subject_baselines']['note'] = 'subject-level chance uses one draw from pooled annotation pmf'

# (d) single annotation
R['d_single_annotation'], bsingle = summ(d.subject, unit_metrics(d.mst_annot, d.oracle))
R['d_baselines'] = baselines(d.subject, d.oracle, pmf)
R['d_diff_median_minus_single'] = diff(summ(img.subject, unit_metrics(img.med_mid, img.oracle))[1], bsingle)

# (e) signed bias by oracle level
lvl = {}
for o in range(1, 11):
    a, im_ = d[d.oracle == o], img[img.oracle == o]
    if not len(a):
        continue
    lvl[o] = {'subjects': sorted(a.subject.unique(), key=lambda s: int(s.split('_')[1])),
              'n_images': len(im_), 'n_annotations': len(a),
              'single_mean_signed': r(a.err.mean()), 'single_within1': r((a.err.abs() <= 1).mean()),
              'image_median_mean_signed_mid': r((im_.med_mid - o).mean()),
              'subject_pooled_median_minus_oracle': {s: r(ps.loc[s, 'pooled_median'] - o) for s in a.subject.unique()},
              'annotation_counts_1_10': a.mst_annot.value_counts().reindex(range(1, 11), fill_value=0).tolist()}
R['e_by_oracle_level'] = lvl
bands = {'light_1_3': (1, 3), 'medium_4_7': (4, 7), 'dark_8_10': (8, 10)}
R['e_bands'] = {}
for b, (lo, hi) in bands.items():
    a, im_ = d[d.oracle.between(lo, hi)], img[img.oracle.between(lo, hi)]
    R['e_bands'][b] = {'single': summ(a.subject, unit_metrics(a.mst_annot, a.oracle))[0]['signed'] | {
        'n_annotations': len(a), 'n_subjects': int(a.subject.nunique())},
        'image_median_mid': summ(im_.subject, unit_metrics(im_.med_mid, im_.oracle))[0]['signed'] | {'n_images': len(im_)}}


x = ps.oracle.values.astype(float)
reg = {}
for nm, y in {'subject_mean_annotation': ps['mean'].values, 'subject_pooled_median': ps.pooled_median.values,
              'subject_mean_of_image_medians': img.groupby('subject').med_mid.mean().loc[SUBJ].values}.items():
    sl = np.polyfit(x, y, 1)
    bs = np.array([np.polyfit(x, y, 1, w=np.sqrt(c))[0] if (c > 0).sum() > 2 else np.nan for c in BOOT])
    mid = (x >= 2) & (x <= 9)
    reg[nm] = {'ols_slope_on_oracle': r(sl[0]), 'slope_ci95': ci(bs), 'intercept': r(sl[1]),
               'predicted_at_oracle': {o: r(sl[1] + sl[0] * o) for o in (1, 5.5, 10)},
               'crossover_oracle_where_pred_equals_oracle': r(sl[1] / (1 - sl[0])),
               'slope_excluding_oracle_1_and_10': r(np.polyfit(x[mid], y[mid], 1)[0]),
               'spearman_signed_err_vs_oracle': [r(v) for v in stats.spearmanr(x, y - x)],
               'n_subjects': NS}
R['e_regression_subject_level'] = reg
R['e_category_use'] = {'annotated_share_1_10': [r(x) for x in pmf],
                       'oracle_implied_share_1_10 (share of annotations whose oracle is k)':
                           d.oracle.value_counts(normalize=True).reindex(range(1, 11), fill_value=0).round(4).tolist()}
R['e_confusion_oracle_rows_annot_cols'] =pd.crosstab(d.oracle, d.mst_annot).reindex(
    columns=range(1, 11), fill_value=0).to_dict(orient='index')

# (f) perceptual units: CIEDE2000 between MST orb colours
def srgb_to_lab(rgb):
    c = np.asarray(rgb, float) / 255
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])  # IEC 61966-2-1
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])  # D65 white
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.c_[116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])]


def de2000(lab1, lab2):
    """CIEDE2000 (kL=kC=kH=1), Sharma, Wu & Dalal (2005) formulation, vectorised."""
    L1, a1, b1 = np.asarray(lab1, float).T
    L2, a2, b2 = np.asarray(lab2, float).T
    Cb = (np.hypot(a1, b1) + np.hypot(a2, b2)) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1, C2 = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1, h2 = np.degrees(np.arctan2(b1, a1p)) % 360, np.degrees(np.arctan2(b2, a2p)) % 360
    z = C1 * C2 == 0
    dh = h2 - h1
    dh = np.where(z, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dH = 2 * np.sqrt(C1 * C2) * np.sin(np.radians(dh / 2))
    Lb, Cbp = (L1 + L2) / 2, (C1 + C2) / 2
    hb = np.where(z, h1 + h2, np.where(np.abs(h1 - h2) <= 180, (h1 + h2) / 2,
                                       np.where(h1 + h2 < 360, (h1 + h2 + 360) / 2, (h1 + h2 - 360) / 2)))
    T = (1 - 0.17 * np.cos(np.radians(hb - 30)) + 0.24 * np.cos(np.radians(2 * hb))
         + 0.32 * np.cos(np.radians(3 * hb + 6)) - 0.20 * np.cos(np.radians(4 * hb - 63)))
    dth = 30 * np.exp(-((hb - 275) / 25) ** 2)
    RC = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7))
    SL = 1 + 0.015 * (Lb - 50) ** 2 / np.sqrt(20 + (Lb - 50) ** 2)
    SC, SH = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    RT = -np.sin(np.radians(2 * dth)) * RC
    tL, tC, tH = (L2 - L1) / SL, (C2 - C1) / SC, dH / SH
    return np.sqrt(tL ** 2 + tC ** 2 + tH ** 2 + RT * tC * tH)


# self-check against Sharma et al. (2005) test pairs 1, 7, 9, 11, 13, 15, 16, 17
_p1 = [(50, 2.6772, -79.7751), (50, 0, 0), (50, 2.49, -0.001), (50, 2.49, -0.001), (50, -0.001, 2.49),
       (50, -0.001, 2.49), (50, 2.5, 0), (50, 2.5, 0)]
_p2 = [(50, 0, -82.7485), (50, -1, 2), (50, -2.49, 0.0009), (50, -2.49, 0.0011), (50, 0.0009, -2.49),
       (50, 0.0011, -2.49), (50, 0, -2.5), (73, 25, -18)]
_exp = [2.0425, 2.3669, 7.1792, 7.2195, 4.8045, 4.7461, 4.3065, 27.1492]
assert np.allclose(de2000(_p1, _p2), _exp, atol=1e-4), de2000(_p1, _p2)

orb_rgb = []
for k in K:
    a = np.array(Image.open(S / f'data_untrusted/orbs/MST_{k}.png').convert('RGBA'))
    px = a[a[..., 3] == 255][:, :3]
    orb_rgb.append(np.median(px, 0))
orb_rgb = np.array(orb_rgb)
PUBLISHED_HEX = 'f6ede4 f3e7db f7ead0 eadaba d7bd96 a07e56 825c43 604134 3a312a 292420'.split()
pub_rgb = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in PUBLISHED_HEX])

R['f_perceptual'] = {'method': 'orb colour = per-channel median sRGB of pixels with alpha==255; sRGB->XYZ '
                               '(IEC 61966-2-1 matrix) -> CIELAB with D65 white (0.95047,1,1.08883); '
                               'CIEDE2000 kL=kC=kH=1 (Sharma 2005), verified on 8 Sharma test pairs to 1e-4. '
                               'dL* = L*(annotated orb) - L*(oracle orb): positive = annotated LIGHTER.'}
for src, rgb in {'orb_png_median': orb_rgb, 'published_mst_hex': pub_rgb}.items():
    lab = srgb_to_lab(rgb)
    DE = de2000(np.repeat(lab, 10, 0), np.tile(lab, (10, 1))).reshape(10, 10)
    Ls = lab[:, 0]
    out = {'rgb': rgb.round(1).tolist(), 'lab': lab.round(2).tolist(),
           'adjacent_step_dE00': [r(DE[i, i + 1], 2) for i in range(9)],
           'dE00_matrix': DE.round(2).tolist()}

    def pm(pred, oracle, subj):
        pred, oracle = np.asarray(pred, int), np.asarray(oracle, int)
        M = np.c_[DE[pred - 1, oracle - 1], Ls[pred - 1] - Ls[oracle - 1]]
        return summ(subj, M, ['dE00', 'dL_star'])[0]

    out['single_annotation'] = pm(d.mst_annot, d.oracle, d.subject)
    for v in ('low', 'high', 'drop4'):
        col, idx = VARIANTS[v]
        sub = img.loc[idx]
        out[f'image_median_{v}'] = pm(sub[col], sub.oracle, sub.subject)
    for c in ('golden', 'challenging', 'well_lit', 'poorly_lit'):
        sub = img[conds[c]]
        out[f'image_median_low_{c}'] = pm(sub.med_lo, sub.oracle, sub.subject)
    out['subject_pooled_median'] = pm(ps.pooled_median, ps.oracle, ps.index)
    out['subject_14_pooled_median_vs_oracle_dE00'] = r(DE[int(ps.loc['subject_14', 'pooled_median']) - 1,
                                                           int(ps.loc['subject_14', 'oracle']) - 1], 2)
    out['uniform_chance_single_dE00_unit_weighted'] = r(np.mean([DE[:, o - 1].mean() for o in d.oracle]), 3)
    out['marginal_chance_single_dE00_unit_weighted'] = r(np.mean([pmf @ DE[:, o - 1] for o in d.oracle]), 3)
    R['f_perceptual'][src] = out

# cross-check the bootstrap-matrix aggregation against plain pandas
_e = (img.med_mid - img.oracle).abs()
assert R['a_image_median_all']['mid']['abs']['unit_weighted'] == r(_e.mean())
assert R['a_image_median_all']['mid']['abs']['subject_weighted'] == r(_e.groupby(img.subject).mean().mean())
assert (img.med_lo <= img.med_mid).all() and (img.med_mid <= img.med_hi).all()

(OUT / 'results.json').write_text(json.dumps(R, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))
print('wrote', OUT / 'results.json')

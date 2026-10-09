"""Independent recomputation of oracle-agreement numbers (MST-E, Ghana crowd annotations).
Run: venv/bin/python -I verify.py   -> writes results.json next to this file."""
import json, os, sys
import numpy as np, pandas as pd
from scipy import stats
from PIL import Image

S = '/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad'
D = '/Users/connielam/Documents/Github/modlli_research/data'
OUT = os.path.join(S, 'reanalysis/verify-oracle-agreement')
SEED, B = 777, 4000
R = {}

df = pd.read_csv(os.path.join(S, 'reanalysis/annotations_clean.csv'))

# ---------- 0. independent sanity check of cleaned table against raw files ----------
raw = pd.read_csv(os.path.join(D, 'mste_annotations.csv'))
det = pd.read_csv(os.path.join(D, 'mst-e_data/mst-e_image_details.csv'))
gold = pd.read_csv(os.path.join(D, 'mst-e_data/golden_and_adversarial_mst-e_image_ids.csv'))
sub_or = det.groupby('subject_name')['MST'].agg(lambda x: sorted(set(x)))
assert all(len(v) == 1 for v in sub_or), 'oracle not constant within subject'
sub_or = sub_or.map(lambda v: v[0])
img_sub = det.groupby('image_ID')['subject_name'].agg(lambda x: sorted(set(x)))
R['sanity'] = {
    'raw_rows': len(raw), 'clean_rows': len(df),
    'raw_subject_unique': raw['subject'].unique().tolist(), 'raw_region_unique': raw['region'].unique().tolist(),
    'raw_images_in_details': int(raw['image'].isin(det['image_ID']).sum()),
    'images_with_multiple_subjects_in_details': int((img_sub.map(len) > 1).sum()),
}
m = raw['image'].map(lambda i: img_sub[i][0] if i in img_sub.index else None)
assert (raw['annotation'].str.replace('MST', '').astype(int).values == df['mst_annot'].values).all()
R['sanity']['subject_match_where_details_present'] = float((m[m.notna()].values == df.loc[m.notna(), 'subject'].values).mean())
R['sanity']['oracle_match'] = float((df['subject'].map(sub_or) == df['oracle']).mean())
R['sanity']['golden_match'] = bool(set(df.loc[df.is_golden, 'image']) == set(gold.golden_image_id))
R['sanity']['challenging_match'] = bool(set(df.loc[df.is_challenging, 'image']) == set(gold.not_ideal_image_id))

# ---------- per-image table ----------
subs = sorted(df.subject.unique(), key=lambda s: int(s.split('_')[1]))
sidx = {s: i for i, s in enumerate(subs)}
g = df.groupby('image')
im = pd.DataFrame({
    'subject': g.subject.first(), 'oracle': g.oracle.first(), 'n': g.size(),
    'med': g.mst_annot.median(),
    'lo': g.mst_annot.apply(lambda x: np.sort(x.values)[(len(x) - 1) // 2]),
    'hi': g.mst_annot.apply(lambda x: np.sort(x.values)[len(x) // 2]),
    'medabs': g.err.apply(lambda x: np.median(np.abs(x))),
    'lighting': g.lighting.first(), 'gold': g.is_golden.first(), 'chal': g.is_challenging.first(),
    'pose': g.pose.first(), 'mask': g['mask'].first(),
})
im['si'] = im.subject.map(sidx)
R['n'] = {'annotations': len(df), 'images': len(im), 'subjects': len(subs),
          'images_by_n': im.n.value_counts().to_dict(), 'xpoint5_medians': int((im.med % 1 != 0).sum()),
          'lighting_counts': im.lighting.fillna('MISSING').value_counts().to_dict()}

rng = np.random.default_rng(SEED)
BOOT = rng.multinomial(19, [1 / 19] * 19, size=B)  # B x 19 counts, shared across all metrics (paired)


def boot(values, si, weight='image'):
    """values per unit, si subject index. Returns point, CI for image(unit)-weighted or subject-weighted mean."""
    values = np.asarray(values, float); si = np.asarray(si)
    ssum = np.bincount(si, values, 19); scnt = np.bincount(si, minlength=19).astype(float)
    if weight == 'image':
        pt = values.mean()
        bs = (BOOT @ ssum) / (BOOT @ scnt)
    else:
        present = scnt > 0
        smean = np.where(present, ssum / np.maximum(scnt, 1), 0)
        pt = smean[present].mean()
        bs = (BOOT @ (smean * present)) / (BOOT @ present.astype(float))
    return [round(float(pt), 4), [round(float(np.nanpercentile(bs, 2.5)), 4), round(float(np.nanpercentile(bs, 97.5)), 4)]]


def metrics(med, orc, si, w='image'):
    e = np.asarray(med, float) - np.asarray(orc, float)
    return {'exact': boot(e == 0, si, w), 'within1': boot(np.abs(e) <= 1, si, w),
            'abs': boot(np.abs(e), si, w), 'signed': boot(e, si, w), 'n_units': int(len(e)),
            'n_subjects': int(len(set(np.asarray(si))))}


# ---------- (a) image median ----------
A = {}
for var in ['med', 'lo', 'hi']:
    A[var] = {w: metrics(im[var], im.oracle, im.si, w) for w in ['image', 'subject']}
d5 = im[im.n == 5]
A['drop4'] = {w: metrics(d5.med, d5.oracle, d5.si, w) for w in ['image', 'subject']}
A['alt_median_abs_err'] = boot(im.medabs, im.si)
R['a_image_median'] = A

# baselines
orc = im.oracle.values
pmf = df.mst_annot.value_counts(normalize=True).reindex(range(1, 11), fill_value=0).values
F = np.cumsum(pmf)
from math import comb
FM = np.array([sum(comb(5, j) * F[k] ** j * (1 - F[k]) ** (5 - j) for j in range(3, 6)) for k in range(10)])
pm_med = np.diff(np.r_[0, FM])
ks = np.arange(1, 11)
def exp_metrics(p):
    ex = np.array([p[ks == o].sum() for o in orc]); w1 = np.array([p[np.abs(ks - o) <= 1].sum() for o in orc])
    ab = np.array([(p * np.abs(ks - o)).sum() for o in orc])
    return {'exact': boot(ex, im.si), 'within1': boot(w1, im.si), 'abs': boot(ab, im.si)}
const = {}
for c in ks:
    p = (ks == c).astype(float); const[int(c)] = exp_metrics(p)
best_c_w1 = max(const, key=lambda c: const[c]['within1'][0]); best_c_abs = min(const, key=lambda c: const[c]['abs'][0])
R['baselines'] = {'best_const_within1': [best_c_w1, const[best_c_w1]], 'best_const_abs': [best_c_abs, const[best_c_abs]],
                  'marginal_median_of_5': exp_metrics(pm_med), 'marginal_single': exp_metrics(pmf),
                  'uniform': exp_metrics(np.full(10, .1))}

# ---------- (b) subsets ----------
Bsub = {}
for name, mask in [('golden', im.gold), ('challenging', im.chal), ('well_lit', im.lighting == 'well_lit'),
                   ('poorly_lit', im.lighting == 'poorly_lit')]:
    x = im[mask.astype(bool)]
    Bsub[name] = {v: metrics(x[v], x.oracle, x.si) for v in ['med', 'lo', 'hi']}
    Bsub[name]['subject_weighted_med'] = metrics(x.med, x.oracle, x.si, 'subject')
    Bsub[name]['alt_median_abs_err'] = boot(x.medabs, x.si)
    Bsub[name]['n4'] = int((x.n == 4).sum())
for name in ['golden', 'challenging']:
    x = im[im[name[:4] if name == 'golden' else 'chal'].astype(bool)].copy()
    x['e'] = x.med - x.oracle
    Bsub[name]['failures'] = x.loc[x.e.abs() > 1, ['subject', 'oracle', 'med', 'lo', 'hi', 'n', 'lighting']].reset_index().to_dict('records')
Bsub['challenging']['lighting'] = im[im.chal].lighting.value_counts().to_dict()
# paired well - poorly difference
def strat_diff(col):
    w = im.lighting == 'well_lit'; p = im.lighting == 'poorly_lit'
    def sums(mask, v):
        return np.bincount(im.si[mask], v[mask], 19), np.bincount(im.si[mask], minlength=19).astype(float)
    out = {}
    for lab, v in [('abs', np.abs(im[col] - im.oracle)), ('signed', im[col] - im.oracle)]:
        v = v.values; sw, cw = sums(w.values, v); sp, cp = sums(p.values, v)
        pt = sw.sum() / cw.sum() - sp.sum() / cp.sum()
        bs = (BOOT @ sw) / (BOOT @ cw) - (BOOT @ sp) / (BOOT @ cp)
        out[lab] = [round(pt, 4), [round(np.percentile(bs, 2.5), 4), round(np.percentile(bs, 97.5), 4)]]
    return out
Bsub['well_minus_poorly'] = strat_diff('med')
# golden - challenging signed (paired, one image each)
gs = im[im.gold].set_index('subject'); cs = im[im.chal].set_index('subject')
dd = (gs.med - gs.oracle) - (cs.med - cs.oracle).reindex(gs.index)
Bsub['golden_minus_challenging_signed'] = boot(dd.values, gs.index.map(sidx))
Bsub['per_subject_lighting_both'] = int(im[im.lighting == 'well_lit'].subject.nunique()), int(im[im.lighting == 'poorly_lit'].subject.nunique())
# other conditions
Bsub['by_pose_abs'] = {k: boot(np.abs(x.med - x.oracle), x.si) for k, x in im.groupby('pose')}
Bsub['by_mask_abs'] = {str(k): boot(np.abs(x.med - x.oracle), x.si) for k, x in im.groupby('mask')}
R['b_subsets'] = Bsub

# ---------- (c) per-subject consensus ----------
sc = pd.DataFrame({'oracle': df.groupby('subject').oracle.first(),
                   'pooled_median': df.groupby('subject').mst_annot.median(),
                   'median_of_img_medians': im.groupby('subject').med.median(),
                   'median_of_img_medians_lo': im.groupby('subject').lo.median(),
                   'mean': df.groupby('subject').mst_annot.mean(),
                   'n_ann': df.groupby('subject').size(), 'n_img': im.groupby('subject').size()}).loc[subs]
C = {'table': sc.reset_index().to_dict('records')}
for col in ['pooled_median', 'median_of_img_medians', 'median_of_img_medians_lo', 'mean']:
    e = sc[col] - sc.oracle
    C[col] = {'within1': int((e.abs() <= 1).sum()), 'exact': int((e == 0).sum()),
              'fail': e[e.abs() > 1].round(3).to_dict(), 'mad': round(float(e.abs().mean()), 4)}
k = C['pooled_median']['within1']
C['clopper_pearson'] = [round(x * 100, 2) for x in stats.binomtest(k, 19).proportion_ci(method='exact')]
# within-subject image resampling of pooled median
rng2 = np.random.default_rng(SEED + 1)
ann_by_img = {i: x.values for i, x in g.mst_annot}
cnts = []; stay = {s: 0 for s in subs}
NR = 2000
imgs_by_sub = {s: im.index[im.subject == s].values for s in subs}
for r in range(NR):
    ok = 0
    for s in subs:
        ims = rng2.choice(imgs_by_sub[s], len(imgs_by_sub[s]), replace=True)
        cons = np.median(np.concatenate([ann_by_img[i] for i in ims]))
        w = abs(cons - sc.oracle[s]) <= 1; ok += w; stay[s] += w
    cnts.append(ok)
cnts = np.array(cnts)
C['image_resample'] = {'P_count': {int(v): round(float((cnts == v).mean()), 4) for v in np.unique(cnts)},
                       'P_stay_within1_lowest': {s: round(stay[s] / NR, 4) for s in sorted(stay, key=stay.get)[:4]}}
R['c_subject_consensus'] = C

# ---------- (d) single annotation ----------
e = df.err.values; si_a = df.subject.map(sidx).values
D_ = {w: {'exact': boot(e == 0, si_a, w), 'within1': boot(np.abs(e) <= 1, si_a, w), 'mae': boot(np.abs(e), si_a, w),
          'signed': boot(e, si_a, w)} for w in ['image', 'subject']}
# gain median - single, paired over same subject resamples
def gain(fi, fa):
    s1 = np.bincount(im.si, fi, 19); c1 = np.bincount(im.si, minlength=19)
    s2 = np.bincount(si_a, fa, 19); c2 = np.bincount(si_a, minlength=19)
    pt = fi.mean() - fa.mean(); bs = (BOOT @ s1) / (BOOT @ c1) - (BOOT @ s2) / (BOOT @ c2)
    return [round(pt, 4), [round(np.percentile(bs, 2.5), 4), round(np.percentile(bs, 97.5), 4)]]
ei = (im.med - im.oracle).values
D_['gain'] = {'within1': gain((np.abs(ei) <= 1).astype(float), (np.abs(e) <= 1).astype(float)),
              'abs': gain(np.abs(ei), np.abs(e).astype(float)), 'exact': gain((ei == 0).astype(float), (e == 0).astype(float))}
R['d_single'] = D_

# ---------- (e) bias by oracle level ----------
E = {}
E['by_level'] = {int(k): {'n_subj': int(x.subject.nunique()), 'n_ann': len(x), 'mean_err': round(x.err.mean(), 3)}
                 for k, x in df.groupby('oracle')}
y = sc['mean'].values; xo = sc.oracle.values.astype(float)
sl = stats.linregress(xo, y)
E['ols_mean_on_oracle'] = {'slope': round(sl.slope, 4), 'intercept': round(sl.intercept, 4),
                           'crosses_identity': round(sl.intercept / (1 - sl.slope), 3)}
bs = []
for c in BOOT:
    sel = np.repeat(np.arange(19), c)
    if np.ptp(xo[sel]) == 0: continue
    bs.append(np.polyfit(xo[sel], y[sel], 1)[0])
E['ols_mean_on_oracle']['slope_ci'] = [round(np.percentile(bs, 2.5), 4), round(np.percentile(bs, 97.5), 4)]
mid = (xo > 1) & (xo < 10)
E['ols_mean_on_oracle']['slope_excl_1_10'] = round(stats.linregress(xo[mid], y[mid]).slope, 4)
sl2 = stats.linregress(xo, sc.pooled_median.values)
E['ols_pooled_median_on_oracle'] = round(sl2.slope, 4)
rho = stats.spearmanr(xo, y - xo)
E['spearman_oracle_vs_subject_mean_err'] = [round(rho.statistic, 4), round(rho.pvalue, 5)]
E['bands'] = {}
for lab, lo_, hi_ in [('light', 1, 3), ('medium', 4, 7), ('dark', 8, 10)]:
    msk = (df.oracle >= lo_) & (df.oracle <= hi_)
    v = np.where(msk, df.err, 0.).astype(float); c = msk.astype(float).values
    sv = np.bincount(si_a, v, 19); scn = np.bincount(si_a, c, 19)
    bsb = (BOOT @ sv) / np.where(BOOT @ scn > 0, BOOT @ scn, np.nan)
    E['bands'][lab] = {'mean_err': round(df.err[msk].mean(), 3), 'ci': [round(np.nanpercentile(bsb, 2.5), 3), round(np.nanpercentile(bsb, 97.5), 3)],
                       'n_ann': int(msk.sum()), 'n_subj': int(df.subject[msk].nunique())}
share_a = df.mst_annot.value_counts(normalize=True).reindex(ks, fill_value=0)
share_o = df.oracle.value_counts(normalize=True).reindex(ks, fill_value=0)
E['category_share_annot_vs_oracle_pct'] = {int(k): [round(100 * share_a[k], 2), round(100 * share_o[k], 2)] for k in ks}
o6 = df[df.oracle == 6].mst_annot.value_counts().sort_index().to_dict()
E['oracle6_annotation_counts'] = {int(k): int(v) for k, v in o6.items()}
E['pooled_median_offset_by_subject'] = (sc.pooled_median - sc.oracle).to_dict()
R['e_bias'] = E

# ---------- (f) CIEDE2000 ----------
def ciede2000(L1, a1, b1, L2, a2, b2):
    L1, a1, b1, L2, a2, b2 = map(lambda z: np.asarray(z, float), (L1, a1, b1, L2, a2, b2))
    C1 = np.hypot(a1, b1); C2 = np.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360; h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    h1p = np.where((a1p == 0) & (b1 == 0), 0, h1p); h2p = np.where((a2p == 0) & (b2 == 0), 0, h2p)
    dLp = L2 - L1; dCp = C2p - C1p
    dh = h2p - h1p
    dh = np.where(C1p * C2p == 0, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lbp = (L1 + L2) / 2; Cbp = (C1p + C2p) / 2
    hs = h1p + h2p
    hbp = np.where(C1p * C2p == 0, hs, np.where(np.abs(h1p - h2p) <= 180, hs / 2, np.where(hs < 360, (hs + 360) / 2, (hs - 360) / 2)))
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dth = 30 * np.exp(-((hbp - 275) / 25) ** 2)
    RC = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    SL = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2); SC = 1 + 0.045 * Cbp; SH = 1 + 0.015 * Cbp * T
    RT = -np.sin(np.radians(2 * dth)) * RC
    return np.sqrt((dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2 + RT * (dCp / SC) * (dHp / SH))

SHARMA = [((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425), ((50, 3.1571, -77.2803), (50, 0, -82.7485), 2.8615),
          ((50, 0, 0), (50, -1, 2), 2.3669), ((50, 2.5, 0), (73, 25, -18), 27.1492), ((50, 2.5, 0), (61, -5, 29), 22.8977),
          ((50, 2.5, 0), (56, -27, -3), 31.9030), ((50, 2.5, 0), (58, 24, 15), 19.4535),
          ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
          ((63.0109, -31.0961, -5.8663), (62.8187, -29.7946, -4.0864), 1.2630),
          ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082)]
for p, q, ref in SHARMA:
    assert abs(ciede2000(*p, *q) - ref) < 1e-4, (p, q, ciede2000(*p, *q), ref)

def srgb_to_lab(rgb):
    c = np.asarray(rgb, float) / 255
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)

orb_rgb = {}
for k in ks:
    a = np.array(Image.open(os.path.join(S, f'data_untrusted/orbs/MST_{k}.png')).convert('RGBA'))
    px = a[a[..., 3] == 255][:, :3]
    orb_rgb[int(k)] = np.median(px, axis=0)
LAB = np.array([srgb_to_lab(orb_rgb[k]) for k in ks])  # index k-1
# cross-check with colour-science
try:
    import colour
    xyz_c = colour.sRGB_to_XYZ(np.array([orb_rgb[k] for k in ks]) / 255)
    lab_c = colour.XYZ_to_Lab(xyz_c, colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'])
    de_c = colour.delta_E(lab_c[:-1], lab_c[1:], method='CIE 2000')
    xcheck = {'max_lab_diff_vs_colour': float(np.abs(lab_c - LAB).max()),
              'adjacent_dE_colour': np.round(de_c, 3).tolist()}
except Exception as ex:
    xcheck = {'error': repr(ex)}
HEX = ['f6ede4', 'f3e7db', 'f7ead0', 'eadaba', 'd7bd96', 'a07e56', '825c43', '604134', '3a312a', '292420']
LABH = np.array([srgb_to_lab([int(h[i:i + 2], 16) for i in (0, 2, 4)]) for h in HEX])

def de(cat1, cat2, lab=LAB):
    c1 = np.asarray(cat1).astype(int) - 1; c2 = np.asarray(cat2).astype(int) - 1
    return ciede2000(*lab[c1].T, *lab[c2].T)
Fo = {'orb_rgb_median': {k: v.tolist() for k, v in orb_rgb.items()}, 'orb_lab': np.round(LAB, 2).tolist(),
      'colour_science_crosscheck': xcheck,
      'adjacent_dE_orb': np.round(de(ks[:-1], ks[1:]), 3).tolist(),
      'adjacent_dE_hex': np.round(de(ks[:-1], ks[1:], LABH), 3).tolist()}
for nm, lab in [('orb', LAB), ('hex', LABH)]:
    Fo[nm] = {
        'single': boot(de(df.mst_annot, df.oracle, lab), si_a), 'single_subjw': boot(de(df.mst_annot, df.oracle, lab), si_a, 'subject'),
        'img_median_lo': boot(de(im.lo, im.oracle, lab), im.si), 'img_median_hi': boot(de(im.hi, im.oracle, lab), im.si),
        'subject_pooled_median': round(float(de(np.floor(sc.pooled_median), sc.oracle, lab).mean()), 4),
        'subject_pooled_median_xpoint5': int((sc.pooled_median % 1 != 0).sum()),
        'uniform': round(float(np.mean([np.mean(de(np.full(10, o), ks, lab)) for o in df.oracle.values[::1]])), 4),
        'marginal': round(float(np.mean([np.sum(pmf * de(np.full(10, o), ks, lab)) for o in df.oracle.values])), 4),
        'subject14_consensus': round(float(de([4], [6], lab)[0]), 3),
        'dL_img_lo_lighter_pos': boot(lab[im.lo.astype(int).values - 1, 0] - lab[im.oracle.values - 1, 0], im.si),
        'dL_img_lo_lighter_pos_subjw': boot(lab[im.lo.astype(int).values - 1, 0] - lab[im.oracle.values - 1, 0], im.si, 'subject'),
        'dL_single': boot(lab[df.mst_annot.values - 1, 0] - lab[df.oracle.values - 1, 0], si_a),
    }
    for lt in ['well_lit', 'poorly_lit']:
        x = im[im.lighting == lt]
        Fo[nm][f'dL_{lt}'] = boot(lab[x.lo.astype(int).values - 1, 0] - lab[x.oracle.values - 1, 0], x.si)
# subject-level consensus dE (orb) per subject pooled median: report whether any pooled median is x.5
R['f_ciede2000'] = Fo

def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, pd.Timestamp): return str(o)
    return o
json.dump(conv(R), open(os.path.join(OUT, 'results.json'), 'w'), indent=1, default=str)
print('ok')

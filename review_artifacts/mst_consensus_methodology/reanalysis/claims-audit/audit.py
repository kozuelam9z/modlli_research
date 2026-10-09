"""MST-E claims audit on the single released crowd region (labelled Ghana).
Run: venv/bin/python -I audit.py  -> writes results.json next to this file."""
import json, os, itertools
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
S = '/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad'
D = '/Users/connielam/Documents/Github/modlli_research/data'
SEED, B = 20231008, 4000
rng = np.random.default_rng(SEED)

df = pd.read_csv(S + '/reanalysis/annotations_clean.csv')
SUBJ = sorted(df.subject.unique(), key=lambda s: int(s.split('_')[1]))
NS = len(SUBJ); assert NS == 19
IDX = rng.integers(0, NS, size=(B, NS))  # one shared subject-resample matrix for all stats
R = {}

def ci(draws):
    draws = np.asarray(draws, float); draws = draws[np.isfinite(draws)]
    return [round(float(np.percentile(draws, 2.5)), 4), round(float(np.percentile(draws, 97.5)), 4)]

# ---------------- per-image table ----------------
def lo_med(a): a = np.sort(a); return a[(len(a) - 1) // 2]
def hi_med(a): a = np.sort(a); return a[len(a) // 2]
rows = []
for im, g in df.groupby('image', sort=False):
    x = g.mst_annot.to_numpy(); o = g.oracle.iloc[0]
    rows.append(dict(image=im, subject=g.subject.iloc[0], oracle=o, lighting=g.lighting.iloc[0],
                     golden=bool(g.is_golden.iloc[0]), chal=bool(g.is_challenging.iloc[0]), n=len(x),
                     x=x, med=np.median(x), med_lo=lo_med(x), med_hi=hi_med(x),
                     medabs=np.median(np.abs(x - o))))
img = pd.DataFrame(rows)
img['sidx'] = img.subject.map({s: i for i, s in enumerate(SUBJ)})
for v in ['med', 'med_lo', 'med_hi']:
    img[f'abs_{v}'] = (img[v] - img.oracle).abs()
    img[f'sgn_{v}'] = img[v] - img.oracle
    img[f'w1_{v}'] = (img[f'abs_{v}'] <= 1).astype(float)
CONDS = {'golden': img.golden, 'challenging': img.chal, 'all_images': img.n > 0,
         'well_lit': img.lighting == 'well_lit', 'poorly_lit': img.lighting == 'poorly_lit'}

# ---------------- ICC(1) via additive per-subject sufficient stats ----------------
def icc_from(m, N, T, Q, Rr, Ssq):
    m, N, T, Q, Rr, Ssq = map(lambda a: np.asarray(a, float), (m, N, T, Q, Rr, Ssq))
    msb = (Rr - T**2 / N) / (m - 1); msw = (Q - Rr) / (N - m)
    k0 = (N - Ssq / N) / (m - 1)
    return (msb - msw) / (msb + (k0 - 1) * msw), msb / msw, (msb - msw) / msb, k0, m - 1, N - m

def stats_images(mask):
    """targets = images; per-subject additive stats (m,N,T,Q,R,S)."""
    st = np.zeros((NS, 6))
    for _, r in img[mask].iterrows():
        x = r.x.astype(float); st[r.sidx] += [1, len(x), x.sum(), (x**2).sum(), x.sum()**2 / len(x), len(x)**2]
    return st

def stats_subject_targets(mask=None):
    """targets = subjects; every annotation of every image of the subject is a replicate."""
    st = np.zeros((NS, 6)); d = df if mask is None else df[mask]
    for s, g in d.groupby('subject'):
        x = g.mst_annot.to_numpy(float); i = SUBJ.index(s)
        st[i] = [1, len(x), x.sum(), (x**2).sum(), x.sum()**2 / len(x), len(x)**2]
    return st

def icc_report(st, label, nlev):
    tot = st.sum(0); icc, F, icck, k0, d1, d2 = icc_from(*tot)
    bs = st[IDX].sum(1)  # (B,6)
    bicc, _, bicck, *_ = icc_from(*bs.T)
    keep = st[:, 0] > 0
    sb = {k: float(k * icc / (1 + (k - 1) * icc)) for k in (1, 2, 3, 5, 10)}
    sb_ci = {k: ci(k * bicc / (1 + (k - 1) * bicc)) for k in (1, 2, 3, 5, 10)}
    return dict(label=label, n=nlev, icc1=round(float(icc), 4), icc1_ci95_boot=ci(bicc),
                F=round(float(F), 3), df=[int(d1), int(d2)], p=float(stats.f.sf(F, d1, d2)),
                icc1k_avg=round(float(icck), 4), icc1k_ci95_boot=ci(bicck), k0=round(float(k0), 3),
                spearman_brown={k: round(v, 4) for k, v in sb.items()}, spearman_brown_ci=sb_ci,
                n_subjects=int(keep.sum()))

ICC = {}
for c in ['golden', 'challenging']:
    ICC[c] = icc_report(stats_images(CONDS[c]), f'{c}: targets=19 images (1/subject), raters=annotations',
                        f'19 subjects / 19 images / {int(img[CONDS[c]].n.sum())} annotations')
    m5 = CONDS[c] & (img.n == 5)
    ICC[c + '_drop4'] = icc_report(stats_images(m5), f'{c}, only images with 5 annotations',
                                   f'{int(m5.sum())} images / {int(img[m5].n.sum())} annotations')
ICC['per_subject_A_subject_targets'] = icc_report(stats_subject_targets(),
    'Per Subject variant A (primary): targets=19 subjects, replicates=all annotations of all images of that subject',
    f'19 subjects / 1482 images / {len(df)} annotations')
ICC['per_subject_B_all_images'] = icc_report(stats_images(CONDS['all_images']),
    'Per Subject variant B: targets=all 1482 images (full MST-E), raters=annotations', '19 subjects / 1482 images / 7395 annotations')
for c in ['well_lit', 'poorly_lit']:
    ICC[c + '_images'] = icc_report(stats_images(CONDS[c]), f'targets={c} images', f'{int(CONDS[c].sum())} images')
# variant D: 5 pseudo-raters = mean over the subject's images of the k-th row (position is NOT a person)
pos = df.groupby(['subject', 'pos_in_image']).mst_annot.mean().unstack()
stD = np.zeros((NS, 6))
for i, s in enumerate(SUBJ):
    x = pos.loc[s].to_numpy(float); stD[i] = [1, 5, x.sum(), (x**2).sum(), x.sum()**2 / 5, 25]
ICC['per_subject_D_position_means'] = icc_report(stD, 'Per Subject variant D: targets=subjects, 5 pseudo-raters = per-position mean across images', '19 subjects x 5 position-means')
# variant C: ICC computed separately within each subject (targets = that subject's images)
within = {}
for i, s in enumerate(SUBJ):
    st = stats_images(img.subject == s)[i]
    within[s] = round(float(icc_from(*st)[0]), 4)
ICC['per_subject_C_within_subject'] = dict(label='Per Subject variant C: ICC(1) within each subject, targets=its images',
    values=within, min=min(within.values()), max=max(within.values()), median=float(np.median(list(within.values()))))
# cross-check own estimator against pingouin on the balanced golden set
try:
    import pingouin as pg
    gimg = img[CONDS['golden'] & (img.n == 5)]
    long = pd.DataFrame([(r.image, j, v) for _, r in gimg.iterrows() for j, v in enumerate(r.x)], columns=['t', 'r', 'y'])
    pgr = pg.intraclass_corr(long, targets='t', raters='r', ratings='y').set_index('Type')
    ICC['pingouin_check_golden_drop4'] = dict(ICC1=float(pgr.loc['ICC(1,1)', 'ICC']), CI95=list(map(float, pgr.loc['ICC(1,1)', 'CI95'])),
                                              pval=float(pgr.loc['ICC(1,1)', 'pval']))
except Exception as e:
    ICC['pingouin_check_golden_drop4'] = str(e)
# paper ranges (5 regions + global pool): a region's value must lie inside the min..max range (rounding to 2 dp)
PAPER = {'golden': (0.90, 0.96), 'challenging': (0.82, 0.95), 'per_subject_A_subject_targets': (0.86, 0.94),
         'per_subject_B_all_images': (0.86, 0.94), 'per_subject_D_position_means': (0.86, 0.94)}
for k, (a, b) in PAPER.items():
    ICC[k]['paper_range'] = [a, b]; ICC[k]['inside_paper_range_2dp'] = bool(a - 0.005 <= ICC[k]['icc1'] < b + 0.005)
# paired (same subject resample) golden - challenging ICC difference
sg, sc = stats_images(CONDS['golden']), stats_images(CONDS['challenging'])
dg = icc_from(*sg[IDX].sum(1).T)[0] - icc_from(*sc[IDX].sum(1).T)[0]
ICC['golden_minus_challenging'] = dict(diff=round(ICC['golden']['icc1'] - ICC['challenging']['icc1'], 4), ci95_boot=ci(dg),
                                       boot_share_le0=round(float((dg <= 0).mean()), 4))
R['icc'] = ICC

# ---------------- distance to oracle ----------------
def ratio_boot(vals, mask):
    """image-weighted mean over images in mask; subject-clustered bootstrap."""
    sums = np.bincount(img.sidx[mask], weights=vals[mask], minlength=NS)
    cnts = np.bincount(img.sidx[mask], minlength=NS).astype(float)
    pt = sums.sum() / cnts.sum(); bs = sums[IDX].sum(1) / cnts[IDX].sum(1)
    return round(float(pt), 4), ci(bs)

DIST = {}
for c, mask in CONDS.items():
    mask = mask.to_numpy()
    out = dict(n_images=int(mask.sum()), n_subjects=int(img[mask].subject.nunique()), n_annotations=int(img[mask].n.sum()))
    for v in ['med', 'med_lo', 'med_hi']:
        for met in ['abs', 'sgn', 'w1']:
            out[f'{met}_{v}'], out[f'{met}_{v}_ci'] = ratio_boot(img[f'{met}_{v}'].to_numpy(float), mask)
    out['median_abs_err_per_image'], out['median_abs_err_per_image_ci'] = ratio_boot(img.medabs.to_numpy(float), mask)
    out['max_abs_med'] = float(img[mask].abs_med.max())
    out['n_images_outside_1'] = int((img[mask].abs_med > 1).sum())
    # subject-weighted variant (each subject's mean over its images, then mean over subjects)
    sm = img[mask].groupby('sidx').abs_med.mean().reindex(range(NS))
    ok = sm.notna().to_numpy(); smv = sm.to_numpy()
    out['abs_med_subject_weighted'] = round(float(np.nanmean(smv)), 4)
    out['abs_med_subject_weighted_ci'] = ci(np.nanmean(smv[IDX], axis=1))
    DIST[c] = out
# Per Subject consensus (one value per subject vs its oracle)
orc = img.groupby('subject').oracle.first().reindex(SUBJ).to_numpy(float)
pooled = df.groupby('subject').mst_annot.median().reindex(SUBJ).to_numpy(float)
medmed = img.groupby('subject').med.median().reindex(SUBJ).to_numpy(float)
PS = {}
for name, v in [('pooled_median_all_annotations', pooled), ('median_of_image_medians', medmed)]:
    a = np.abs(v - orc); sg = v - orc; w = (a <= 1).astype(float)
    PS[name] = dict(n='19 subjects', abs=round(float(a.mean()), 4), abs_ci=ci(a[IDX].mean(1)),
                    sgn=round(float(sg.mean()), 4), sgn_ci=ci(sg[IDX].mean(1)),
                    within1=round(float(w.mean()), 4), within1_count=int(w.sum()),
                    within1_clopper_pearson=[round(float(x), 4) for x in stats.binomtest(int(w.sum()), NS).proportion_ci()],
                    exact_match=int((a == 0).sum()), max_abs=float(a.max()),
                    per_subject={s: [float(v[i]), float(orc[i])] for i, s in enumerate(SUBJ)})
DIST['per_subject'] = PS
# share of subject-bootstrap draws with average median distance >= 1 (guardrail)
for c, mask in CONDS.items():
    mask = mask.to_numpy(); v = img.abs_med.to_numpy(float)
    sums = np.bincount(img.sidx[mask], weights=v[mask], minlength=NS); cnts = np.bincount(img.sidx[mask], minlength=NS)
    DIST[c]['boot_share_abs_med_ge1'] = round(float((sums[IDX].sum(1) / cnts[IDX].sum(1) >= 1).mean()), 4)
a = np.abs(pooled - orc); DIST['per_subject']['boot_share_abs_ge1'] = round(float((a[IDX].mean(1) >= 1).mean()), 4)
DIST['per_subject']['abs_dist_counts'] = {int(k): int(v) for k, v in zip(*np.unique(a, return_counts=True))}
# scale compression: slope of consensus on oracle (1 = no compression)
def slope(x, y): return np.polyfit(x, y, 1)[0]
bsl = [slope(orc[i], pooled[i]) for i in IDX if len(np.unique(orc[i])) > 1]
io, im_, isx = img.oracle.to_numpy(float), img.med.to_numpy(float), img.sidx.to_numpy()
rows_by = [np.where(isx == s)[0] for s in range(NS)]
bsl_img = []
for i in IDX:
    r = np.concatenate([rows_by[s] for s in i])
    if len(np.unique(io[r])) > 1: bsl_img.append(slope(io[r], im_[r]))
lo, hi = orc <= 3, orc >= 8
DIST['scale_compression'] = dict(
    subject_slope_pooled_median_on_oracle=round(float(slope(orc, pooled)), 4), subject_slope_ci95=ci(bsl), n='19 subjects',
    image_slope_median_on_oracle=round(float(slope(io, im_)), 4), image_slope_ci95=ci(bsl_img), n_img='1482 images / 19 subjects',
    mean_signed_subjects_oracle_le3=round(float((pooled - orc)[lo].mean()), 4), n_le3=int(lo.sum()),
    mean_signed_subjects_oracle_ge8=round(float((pooled - orc)[hi].mean()), 4), n_ge8=int(hi.sum()))
R['distance'] = DIST

# confusion matrices oracle x median (Fig 8 analogue for this region)
def conf(o, m):
    t = pd.crosstab(pd.Series(o, name='oracle'), pd.Series(m, name='median'))
    return {int(k): {str(c): int(t.loc[k, c]) for c in t.columns if t.loc[k, c]} for k in t.index}
R['confusion'] = {'golden': conf(img[img.golden].oracle, img[img.golden].med),
                  'challenging': conf(img[img.chal].oracle, img[img.chal].med),
                  'per_subject_pooled': conf(orc.astype(int), pooled)}

# ---------------- k-rater subsets (exact enumeration) ----------------
def subset_metrics(r, k):
    combos = list(itertools.combinations(r.x, k)); meds = np.array([np.median(c) for c in combos])
    full = r.med
    return (np.abs(meds - r.oracle).mean(), (np.abs(meds - r.oracle) <= 1).mean(),
            (meds == full).mean(), (np.abs(meds - full) <= 1).mean())
KR = {}
for c in ['golden', 'challenging', 'all_images', 'well_lit', 'poorly_lit']:
    mask = CONDS[c].to_numpy(); out = {}
    per_k = {}
    for k in (1, 2, 3, 5):
        m = mask & (img.n >= k).to_numpy() if k < 5 else mask & (img.n == 5).to_numpy()
        M = np.array([subset_metrics(r, k) if (mm and r.n >= k) else (np.nan,) * 4 for mm, (_, r) in zip(m, img.iterrows())])
        per_k[k] = (M, m)
        res = {}
        for j, nm in enumerate(['abs_err', 'within1_oracle', 'exact_agree_fullpanel', 'within1_fullpanel']):
            vals = np.nan_to_num(M[:, j])
            res[nm], res[nm + '_ci'] = ratio_boot(vals, m)
        res['n_images'] = int(m.sum())
        out[f'k{k}'] = res
    # paired difference k=1 minus full panel (all available annotations), on the same images
    m = mask
    M1 = np.array([subset_metrics(r, 1) if mm else (np.nan,) * 4 for mm, (_, r) in zip(m, img.iterrows())])
    d_abs = np.nan_to_num(M1[:, 0] - img.abs_med.to_numpy())
    d_w1 = np.nan_to_num(M1[:, 1] - img.w1_med.to_numpy())
    out['full_panel_abs_err'] = ratio_boot(img.abs_med.to_numpy(float), m)
    out['full_panel_within1'] = ratio_boot(img.w1_med.to_numpy(float), m)
    out['diff_abs_k1_minus_full'] = ratio_boot(d_abs, m)
    out['diff_within1_k1_minus_full'] = ratio_boot(d_w1, m)
    M2 = np.array([subset_metrics(r, 2) if mm else (np.nan,) * 4 for mm, (_, r) in zip(m, img.iterrows())])
    out['diff_abs_k1_minus_k2'] = ratio_boot(np.nan_to_num(M1[:, 0] - M2[:, 0]), m)
    out['diff_within1_k2_minus_k1'] = ratio_boot(np.nan_to_num(M2[:, 1] - M1[:, 1]), m)
    KR[c] = out

# empirical split-half reliability of k-rater means vs Spearman-Brown (5-annotation images only)
def split_corr(mask, k):
    X = np.stack(img[mask & (img.n == 5)].x.to_numpy()).astype(float)
    sid = img[mask & (img.n == 5)].sidx.to_numpy()
    splits = [(a, b) for a in itertools.combinations(range(5), k) for b in itertools.combinations(range(5), k)
              if not set(a) & set(b) and a < b]
    def f(rows):
        return np.nanmean([np.corrcoef(X[rows][:, list(a)].mean(1), X[rows][:, list(b)].mean(1))[0, 1] for a, b in splits])
    allrows = np.arange(len(X)); pt = f(allrows)
    bs = []
    by = {s: np.where(sid == s)[0] for s in range(NS)}
    for b in range(B):
        rows = np.concatenate([by[s] for s in IDX[b]])
        bs.append(f(rows) if len(np.unique(X[rows].mean(1))) > 1 else np.nan)
    return round(float(pt), 4), ci(bs), len(splits), int(len(X))
SPLIT = {}
for c in ['golden', 'challenging', 'all_images']:
    for k in (1, 2):
        pt, cc, ns_, ni = split_corr(CONDS[c].to_numpy(), k)
        SPLIT[f'{c}_k{k}'] = dict(r=pt, ci95=cc, n_splits=ns_, n_images=ni,
                                  sb_pred_from_icc=ICC['per_subject_B_all_images' if c == 'all_images' else c]['spearman_brown'][k])
KR['split_half_empirical'] = SPLIT
R['k_raters'] = KR

# ---------------- lighting invariance (paired by subject) ----------------
LI = {}
for nm, (ma, mb) in {'poorly_minus_well_lit': (CONDS['poorly_lit'], CONDS['well_lit']),
                     'challenging_minus_golden': (CONDS['challenging'], CONDS['golden'])}.items():
    out = {}
    for met in ['abs_med', 'sgn_med', 'w1_med']:
        a = img[ma].groupby('sidx')[met].mean().reindex(range(NS)); b = img[mb].groupby('sidx')[met].mean().reindex(range(NS))
        d = (a - b).to_numpy(); ok = np.isfinite(d)
        out[met] = dict(mean_diff=round(float(np.nanmean(d)), 4), ci95=ci(np.nanmean(d[IDX], 1)),
                        n_subjects=int(ok.sum()),
                        wilcoxon_p=float(stats.wilcoxon(d[ok]).pvalue) if np.any(d[ok] != 0) else 1.0,
                        a_mean=round(float(np.nanmean(a)), 4), b_mean=round(float(np.nanmean(b)), 4))
    LI[nm] = out
# single-annotation level
for lv in ['well_lit', 'poorly_lit']:
    e = df[df.lighting == lv].err
    LI[f'single_annotation_{lv}'] = dict(n=int(len(e)), mean_abs=round(float(e.abs().mean()), 4), mean_signed=round(float(e.mean()), 4),
                                         within1=round(float((e.abs() <= 1).mean()), 4))
R['lighting'] = LI

# ---------------- data-card / structure checks ----------------
raw = pd.read_csv(D + '/mste_annotations.csv')
det = pd.read_csv(D + '/mst-e_data/mst-e_image_details.csv')
gold = pd.read_csv(D + '/mst-e_data/golden_and_adversarial_mst-e_image_ids.csv')
files = []
for s in SUBJ:
    for f in os.listdir(f'{D}/mst-e_data/{s}'):
        files.append((s, f, f.rsplit('.', 1)[-1].lower()))
files = pd.DataFrame(files, columns=['subject', 'file', 'ext'])
stills = files[files.ext.isin(['jpg', 'dng'])]
unann = stills[~stills.file.isin(df.image)]
cnt = img.n.value_counts().to_dict()
four = img[img.n == 4]
ct = pd.crosstab(img.lighting.isin(['poorly_lit']), img.n == 4)
DC = dict(
    raw_rows=int(len(raw)), raw_columns=list(raw.columns), raw_regions=raw.region.unique().tolist(),
    raw_subject_values=raw.subject.unique().tolist(), n_images=int(raw.image.nunique()),
    annotations_per_image_counts={int(k): int(v) for k, v in cnt.items()},
    expected_rows_if_25_per_image=int(25 * raw.image.nunique()), observed_fraction_of_25=round(len(raw) / (25 * raw.image.nunique()), 4),
    annotation_values=sorted(raw.annotation.unique().tolist(), key=lambda s: int(s[3:])),
    folder_files_by_ext=files.ext.value_counts().to_dict(),
    stills_in_folders=int(len(stills)), stills_not_annotated=int(len(unann)),
    stills_not_annotated_by_ext=unann.ext.value_counts().to_dict(),
    jpg_not_annotated=unann[unann.ext == 'jpg'][['subject', 'file']].values.tolist(),
    annotated_not_in_details_csv=sorted(set(df.image) - set(det.image_ID)),
    images_with_4=dict(n=int(len(four)), by_lighting=four.lighting.value_counts(dropna=False).to_dict(),
                       by_subject=four.subject.value_counts().to_dict(), includes_challenging=four[four.chal].image.tolist(),
                       includes_golden=four[four.golden].image.tolist(),
                       fisher_poorly_vs_other=float(stats.fisher_exact(ct.values)[1]),
                       rate_poorly=round(float(four.lighting.eq('poorly_lit').sum() / img.lighting.eq('poorly_lit').sum()), 4),
                       rate_well=round(float(four.lighting.eq('well_lit').sum() / img.lighting.eq('well_lit').sum()), 4)),
    golden_lighting=img[img.golden].lighting.value_counts(dropna=False).to_dict(),
    challenging_lighting=img[img.chal].lighting.value_counts(dropna=False).to_dict(),
    golden_csv_columns=list(gold.columns), details_csv_columns=list(det.columns),
    details_mask_values=det['mask'].astype(str).unique().tolist(), details_pose_values=det.pose.unique().tolist(),
    oracle_constant_within_subject=bool((det.groupby('subject_name').MST.nunique() == 1).all()),
    oracle_levels_present=sorted(det.MST.unique().tolist()),
    datacard_images_per_MST=[179, 218, 112, 187, 179, 165, 76, 143, 142, 111], datacard_images_sum=1512,
    datacard_videos_per_MST=[2, 5, 5, 3, 4, 3, 4, 2, 5, 1], datacard_videos_sum=34,
    annotated_images_per_MST=img.groupby('oracle').size().reindex(range(1, 11)).tolist(),
    folder_stills_per_MST=stills.subject.map(det.groupby('subject_name').MST.first()).value_counts().reindex(range(1, 11)).tolist(),
    folder_mp4_per_MST=files[files.ext == 'mp4'].subject.map(det.groupby('subject_name').MST.first()).value_counts().reindex(range(1, 11)).fillna(0).astype(int).tolist(),
    annotation_distribution={int(k): int(v) for k, v in df.mst_annot.value_counts().sort_index().items()},
    overall_single_annotation=dict(mean_abs_err=round(float(df.err.abs().mean()), 4), mean_signed=round(float(df.err.mean()), 4),
                                   within1=round(float((df.err.abs() <= 1).mean()), 4)),
)
assert sum(DC['datacard_images_per_MST']) == 1512 and sum(DC['datacard_videos_per_MST']) == 34
R['datacard'] = DC
R['meta'] = dict(seed=SEED, bootstrap_resamples=B, bootstrap='subject-clustered: resample 19 subjects with replacement, keep all their images',
                 levels='19 subjects / 1482 images / 7395 annotations; 1 region (Ghana)')

json.dump(R, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('ok')

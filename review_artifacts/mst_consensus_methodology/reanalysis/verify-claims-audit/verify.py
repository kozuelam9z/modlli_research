"""Independent verification of the claims-audit numbers. Built from the RAW files; the
orchestrator's cleaned table is only used as a cross-check of subject/oracle/lighting joins."""
import os, sys, json, itertools
import numpy as np, pandas as pd
from scipy import stats

D = '/Users/connielam/Documents/Github/modlli_research/data'
OUT = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(OUT, '..', 'annotations_clean.csv')
B = 4000
SEED = 7
R = {}

# ---------------- raw load ----------------
raw = pd.read_csv(f'{D}/mste_annotations.csv', dtype=str)
det = pd.read_csv(f'{D}/mst-e_data/mst-e_image_details.csv', dtype=str)
gc = pd.read_csv(f'{D}/mst-e_data/golden_and_adversarial_mst-e_image_ids.csv', dtype=str)
R_ws = {'details_cells_with_whitespace': int(det.apply(lambda c: c.str.strip() != c).sum().sum()), 'ids_cells_with_whitespace': int(gc.apply(lambda c: c.str.strip() != c).sum().sum())}
det = det.apply(lambda c: c.str.strip()); gc = gc.apply(lambda c: c.str.strip()); raw = raw.apply(lambda c: c.str.strip())
R['whitespace'] = R_ws
R['raw'] = dict(rows=len(raw), cols=list(raw.columns), subject_unique=raw.subject.unique().tolist(),
                region_unique=raw.region.unique().tolist(), n_images=raw.image.nunique(),
                annotation_counts=raw.annotation.value_counts().to_dict())
cnt = raw.groupby('image').size()
R['raw']['per_image_counts'] = cnt.value_counts().to_dict()
R['raw']['share_of_25x'] = len(raw) / (25 * raw.image.nunique())

# image -> folder
folder_of = {}
still = {}
for s in sorted(os.listdir(f'{D}/mst-e_data')):
    p = f'{D}/mst-e_data/{s}'
    if not (os.path.isdir(p) and s.startswith('subject_')):
        continue
    for f in os.listdir(p):
        folder_of.setdefault(f, []).append(s)
        if f.lower().endswith(('.jpg', '.jpeg', '.dng', '.png')):
            still[(s, f)] = 1
amb = [f for f, v in folder_of.items() if len(v) > 1]
raw['subject'] = raw.image.map(lambda f: folder_of.get(f, [None])[0])
R['join'] = dict(unmapped=int(raw.subject.isna().sum()), ambiguous_filenames=len(amb),
                 n_subjects=raw.subject.nunique())
assert raw.subject.notna().all()

# oracle per subject
o = det.groupby('subject_name').MST.nunique()
R['join']['oracle_const_within_subject'] = bool((o == 1).all())
oracle = det.groupby('subject_name').MST.first().astype(int)
raw['oracle'] = raw.subject.map(oracle)
raw['x'] = raw.annotation.str.replace('MST', '').astype(int)
raw['err'] = raw.x - raw.oracle
R['join']['oracle_level_counts'] = oracle.value_counts().sort_index().to_dict()

# lighting from details; flag dups/conflicts
dd = det.groupby('image_ID')
conf = [k for k, g in dd if g[['pose', 'lighting', 'mask', 'subject_name', 'MST']].drop_duplicates().shape[0] > 1]
light_conf = [k for k, g in dd if g.lighting.nunique() > 1]
light = dd.lighting.first()
raw['lighting'] = raw.image.map(light)
R['join']['meta_conflict_ids'] = conf
R['join']['lighting_conflict_ids'] = light_conf
R['join']['images_missing_meta'] = sorted(set(raw.image) - set(det.image_ID))
# details subject vs folder
ds = dd.subject_name.first()
mm = raw.image.map(ds)
R['join']['details_subject_mismatch_rows'] = int(((mm != raw.subject) & mm.notna()).sum())

golden = set(gc.golden_image_id); chal = set(gc.not_ideal_image_id)
raw['golden'] = raw.image.isin(golden); raw['chal'] = raw.image.isin(chal)
R['join']['golden_found'] = int(raw[raw.golden].image.nunique()); R['join']['chal_found'] = int(raw[raw.chal].image.nunique())
R['join']['golden_lighting'] = raw[raw.golden].drop_duplicates('image').lighting.fillna('MISSING').value_counts().to_dict()
R['join']['chal_lighting'] = raw[raw.chal].drop_duplicates('image').lighting.fillna('MISSING').value_counts().to_dict()
R['join']['image_lighting'] = raw.drop_duplicates('image').lighting.fillna('MISSING').value_counts().to_dict()

# cross-check vs orchestrator table
cl = pd.read_csv(CLEAN)
R['join']['clean_rows'] = len(cl)
R['join']['clean_subject_agree'] = bool((cl.subject.values == raw.subject.values).all() and (cl.image.values == raw.image.values).all())
R['join']['clean_oracle_agree'] = bool((cl.oracle.values == raw.oracle.values).all())
R['join']['clean_lighting_disagree_rows'] = int((cl.lighting.fillna('NA').values != raw.lighting.fillna('NA').values).sum())

# coverage of still files
ann_imgs = set(raw.image)
unann = [(s, f) for (s, f) in still if f not in ann_imgs]
R['coverage'] = dict(still_files=len(still), annotated=len(still) - len(unann), unannotated=len(unann),
                     unann_dng=sum(f.lower().endswith('.dng') for s, f in unann),
                     unann_by_subject=pd.Series([s for s, f in unann]).value_counts().to_dict(),
                     mp4=sum(1 for f in folder_of if f.lower().endswith('.mp4')),
                     annotated_not_in_folders=len(ann_imgs - {f for s, f in still}))

# ---------------- per-image table ----------------
img = raw.groupby('image').agg(subject=('subject', 'first'), oracle=('oracle', 'first'), n=('x', 'size'),
                                med=('x', 'median'), lighting=('lighting', 'first'),
                                golden=('golden', 'first'), chal=('chal', 'first')).reset_index()
img['lo'] = raw.groupby('image').x.apply(lambda v: np.sort(v.values)[(len(v) - 1) // 2]).values
img['hi'] = raw.groupby('image').x.apply(lambda v: np.sort(v.values)[len(v) // 2]).values
img['medabs'] = raw.assign(a=raw.err.abs()).groupby('image').a.median().values
subs = sorted(img.subject.unique())

# 4-annotation images
four = img[img.n == 4]
R['four'] = dict(n=len(four), lighting=four.lighting.fillna('MISSING').value_counts().to_dict(),
                 golden=int(four.golden.sum()), chal=int(four.chal.sum()),
                 chal_subject=four[four.chal].subject.tolist())
wl = img[img.lighting == 'well_lit']; pl = img[img.lighting == 'poorly_lit']
t = [[(pl.n == 4).sum(), (pl.n == 5).sum()], [(img.n == 4).sum() - (pl.n == 4).sum(), (img.n == 5).sum() - (pl.n == 5).sum()]]
R['four']['rate_poor'] = float((pl.n == 4).mean()); R['four']['rate_well'] = float((wl.n == 4).mean())
R['four']['fisher_poor_vs_other_p'] = float(stats.fisher_exact(t)[1])


# ---------------- ICC(1) ----------------
def icc1(groups):
    """one-way random single-score ICC for unbalanced groups (list of arrays). Returns icc, F, df1, df2, p"""
    groups = [np.asarray(g, float) for g in groups]
    n = len(groups); ni = np.array([len(g) for g in groups]); N = ni.sum()
    gm = np.concatenate(groups).mean()
    ssb = sum(len(g) * (g.mean() - gm) ** 2 for g in groups); ssw = sum(((g - g.mean()) ** 2).sum() for g in groups)
    msb = ssb / (n - 1); msw = ssw / (N - n)
    k0 = (N - (ni ** 2).sum() / N) / (n - 1)
    F = msb / msw
    return (msb - msw) / (msb + (k0 - 1) * msw), F, n - 1, N - n, stats.f.sf(F, n - 1, N - n), k0


# sanity check against pingouin on balanced golden
gx = {s: raw[(raw.subject == s) & raw.golden].x.values for s in subs}
cx = {s: raw[(raw.subject == s) & raw.chal].x.values for s in subs}
sx = {s: raw[raw.subject == s].x.values for s in subs}
try:
    import pingouin as pg
    long = pd.DataFrame([(s, j, v) for s in subs for j, v in enumerate(gx[s])], columns=['t', 'r', 'v'])
    pgr = pg.intraclass_corr(long, 't', 'r', 'v').set_index('Type'); R['pingouin_golden_icc1'] = pgr.loc['ICC1'].astype(str).to_dict()
except Exception as e:
    R['pingouin_golden_icc1'] = str(e)

rng = np.random.default_rng(SEED)
BS = [rng.choice(subs, len(subs), replace=True) for _ in range(B)]


def ci(vals):
    v = np.asarray(vals, float)
    return [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]


def icc_block(d):
    pt = icc1([d[s] for s in subs])
    bs = [icc1([d[s] for s in b])[0] for b in BS]
    return dict(icc=pt[0], F=pt[1], df1=pt[2], df2=pt[3], p=pt[4], k0=pt[5], ci=ci(bs)), np.array(bs)

icc = {}
icc['golden'], bg = icc_block(gx)
icc['chal'], bc = icc_block(cx)
cx5 = {s: v for s, v in cx.items()}
icc['chal_drop4'] = dict(icc=icc1([v for v in cx.values() if len(v) == 5])[0])
icc['golden_minus_chal'] = dict(diff=icc['golden']['icc'] - icc['chal']['icc'], ci=ci(bg - bc), share_le0=float(np.mean(bg - bc <= 0)))
icc['persubj_A'], bA = icc_block(sx)
# B: targets = images; bootstrap by subject (all images of the drawn subjects)
imgs_of = {s: [raw[raw.image == i].x.values for i in img[img.subject == s].image] for s in subs}
ptB = icc1([g for s in subs for g in imgs_of[s]])
bB = [icc1([g for s in b for g in imgs_of[s]])[0] for b in BS[:1000]]
icc['persubj_B'] = dict(icc=ptB[0], F=ptB[1], df1=ptB[2], df2=ptB[3], k0=ptB[5], ci_1000=ci(bB))
# C: within-subject ICC (targets = images of that subject)
cvals = {s: icc1(imgs_of[s])[0] for s in subs}
icc['persubj_C'] = dict(min=min(cvals.values()), max=max(cvals.values()), median=float(np.median(list(cvals.values()))))
# D: per subject, mean of annotations at each pos -> 5 pseudo-raters; ICC1 across subjects
cl['pos'] = cl.pos_in_image
pm = cl.groupby(['subject', 'pos']).mst_annot.mean().unstack()
icc['persubj_D'] = dict(icc=icc1([pm.loc[s].dropna().values for s in subs])[0])
# lighting ICC (images as targets)
for L in ['well_lit', 'poorly_lit']:
    icc[f'images_{L}'] = icc1([raw[raw.image == i].x.values for i in img[img.lighting == L].image])[0]
R['icc'] = icc

# ---------------- distances ----------------
def boot_img_mean(df, col):
    """image-weighted mean over images in df, subject-clustered bootstrap"""
    by = {s: df[df.subject == s][col].values for s in subs}
    pt = df[col].mean()
    bs = []
    for b in BS:
        v = np.concatenate([by[s] for s in b])
        bs.append(v.mean() if len(v) else np.nan)
    bs = np.array(bs)
    return dict(value=float(pt), ci=ci(bs), share_ge1=float(np.nanmean(bs >= 1)), n_images=int(len(df)))

img['absd'] = (img.med - img.oracle).abs(); img['sgn'] = img.med - img.oracle
img['absd_lo'] = (img.lo - img.oracle).abs(); img['absd_hi'] = (img.hi - img.oracle).abs()
conds = {'golden': img[img.golden], 'chal': img[img.chal], 'all': img,
         'well_lit': img[img.lighting == 'well_lit'], 'poorly_lit': img[img.lighting == 'poorly_lit'],
         'well_lit_noconflict': img[(img.lighting == 'well_lit') & ~img.image.isin(conf)],
         'poorly_lit_noconflict': img[(img.lighting == 'poorly_lit') & ~img.image.isin(conf)]}
dist = {}
for k, df in conds.items():
    dist[k] = dict(abs=boot_img_mean(df, 'absd'), signed=boot_img_mean(df, 'sgn'),
                   medabs=boot_img_mean(df, 'medabs'), abs_lo=float(df.absd_lo.mean()), abs_hi=float(df.absd_hi.mean()),
                   within1=float((df.absd <= 1).mean()), within1_hi=float((df.absd_hi <= 1).mean()),
                   within1_lo=float((df.absd_lo <= 1).mean()), n_off_gt1=int((df.absd > 1).sum()),
                   max_abs=float(df.absd.max()))
    # subject-weighted variant (mean over subjects of the subject's image-mean)
    sw = df.groupby('subject').absd.mean(); dist[k]['abs_subject_weighted'] = float(sw.mean())
    dist[k]['signed_subject_weighted'] = float(df.groupby('subject').sgn.mean().mean())
    dist[k]['within1_ci'] = boot_img_mean(df.assign(w=(df.absd <= 1).astype(float)), 'w')['ci']

# per subject
ps = raw.groupby('subject').agg(oracle=('oracle', 'first'), pooled=('x', 'median')).reindex(subs)
ps['med_of_med'] = img.groupby('subject').med.median().reindex(subs)
ps['absd'] = (ps.pooled - ps.oracle).abs(); ps['sgn'] = ps.pooled - ps.oracle
ps['absd_mm'] = (ps.med_of_med - ps.oracle).abs()
bsp = [ps.loc[b].absd.mean() for b in BS]; bss = [ps.loc[b].sgn.mean() for b in BS]
dist['per_subject'] = dict(abs=dict(value=float(ps.absd.mean()), ci=ci(bsp), share_ge1=float(np.mean(np.array(bsp) >= 1))),
                           signed=dict(value=float(ps.sgn.mean()), ci=ci(bss)),
                           abs_med_of_med=float(ps.absd_mm.mean()),
                           within1=int((ps.absd <= 1).sum()), within1_mm=int((ps.absd_mm <= 1).sum()),
                           exact=int((ps.absd == 0).sum()), off1=int((ps.absd == 1).sum()), off2plus=int((ps.absd >= 2).sum()),
                           misses=ps[ps.absd > 1][['oracle', 'pooled']].reset_index().to_dict('records'),
                           cp_ci=[float(x) for x in stats.binomtest(int((ps.absd <= 1).sum()), 19).proportion_ci(method='exact')],
                           pairs=ps[['oracle', 'pooled', 'med_of_med']].reset_index().to_dict('records'))
R['dist'] = dist

# ---------------- paired lighting / golden-chal shifts ----------------
def paired(a, b, col):
    """per-subject mean(col) over a-images minus over b-images"""
    d = (a.groupby('subject')[col].mean() - b.groupby('subject')[col].mean()).reindex(subs)
    bs = [d.loc[s].mean() for s in BS]
    return dict(mean=float(d.mean()), ci=ci(bs), wilcoxon_p=float(stats.wilcoxon(d.dropna()).pvalue), n=int(d.notna().sum()))
pls = {}
for col in ['sgn', 'absd']:
    pls[f'poor_minus_well_{col}'] = paired(conds['poorly_lit'], conds['well_lit'], col)
    pls[f'chal_minus_golden_{col}'] = paired(conds['chal'], conds['golden'], col)
R['paired'] = pls
# single annotations signed by lighting
R['single_signed_by_light'] = raw.groupby('lighting').err.mean().to_dict()
R['single_overall'] = dict(within1=float((raw.err.abs() <= 1).mean()), mean_abs=float(raw.err.abs().mean()))

# ---------------- k-rater enumeration ----------------
def krater(df_imgs, k):
    vals = []
    for i in df_imgs.image:
        x = raw[raw.image == i].x.values; o = raw[raw.image == i].oracle.iloc[0]
        kk = min(k, len(x))
        sub = [np.median(c) for c in itertools.combinations(x, kk)]
        vals.append((np.mean([abs(m - o) for m in sub]), np.mean([abs(m - o) <= 1 for m in sub])))
    return np.array(vals)

kr = {}
for name, df in [('golden', conds['golden']), ('chal', conds['chal']), ('all', img)]:
    r = {}
    per = {k: krater(df, k) for k in [1, 2, 3, 5]}
    for k in per:
        r[f'k{k}_abs'] = float(per[k][:, 0].mean()); r[f'k{k}_within1'] = float(per[k][:, 1].mean())
    sidx = df.subject.values
    for lab, a, b in [('diff_1_vs_full', 1, 5), ('gain_1_to_2', 1, 2)]:
        d = per[a][:, 0] - per[b][:, 0]
        byS = {s: d[sidx == s] for s in subs}
        bs = [np.concatenate([byS[s] for s in bb]).mean() for bb in BS]
        r[lab] = dict(value=float(d.mean()), ci=ci(bs))
    # single vs consensus
    ag = []
    for i in df.image:
        x = raw[raw.image == i].x.values; m = np.median(x)
        ag.append(((x == m).mean(), (np.abs(x - m) <= 1).mean()))
    ag = np.array(ag)
    r['single_vs_consensus_exact'] = float(ag[:, 0].mean()); r['single_vs_consensus_within1'] = float(ag[:, 1].mean())
    byS = {s: ag[sidx == s, 0] for s in subs}
    r['single_vs_consensus_exact_ci'] = ci([np.concatenate([byS[s] for s in bb]).mean() for bb in BS])
    kr[name] = r
R['krater'] = kr

# ---------------- Spearman-Brown + split half ----------------
sb = lambda r, k: k * r / (1 + (k - 1) * r)
R['sb'] = {nm: {f'k{k}': sb(icc[nm]['icc'], k) for k in [1, 2, 5, 10]} for nm in ['golden', 'chal', 'persubj_A']}
R['sb']['chal_k2_ci'] = ci([sb(v, 2) for v in bc])
R['sb']['golden_k1_ci'] = icc['golden']['ci']

def splithalf(d, k):
    S = [s for s in subs if len(d[s]) == 5]
    rs = []
    for A in itertools.combinations(range(5), k):
        rest = [j for j in range(5) if j not in A]
        for Bc in itertools.combinations(rest, k):
            if A < Bc:
                a = [d[s][list(A)].mean() for s in S]; b = [d[s][list(Bc)].mean() for s in S]
                rs.append(np.corrcoef(a, b)[0, 1])
    return float(np.mean(rs)), len(rs), len(S)
R['splithalf'] = {f'{nm}_k{k}': splithalf(d, k) for nm, d in [('golden', gx), ('chal', cx)] for k in [1, 2]}

# ---------------- slope ----------------
sl = np.polyfit(ps.oracle, ps.pooled, 1)[0]
bsl = [np.polyfit(ps.loc[b].oracle, ps.loc[b].pooled, 1)[0] if ps.loc[b].oracle.nunique() > 1 else np.nan for b in BS]
isl = np.polyfit(img.oracle, img.med, 1)[0]
ib = []
for b in BS[:2000]:
    dd2 = pd.concat([img[img.subject == s] for s in b])
    ib.append(np.polyfit(dd2.oracle, dd2.med, 1)[0] if dd2.oracle.nunique() > 1 else np.nan)
R['slope'] = dict(subject=float(sl), subject_ci=ci(bsl), image=float(isl), image_ci_2000=ci(ib),
                  low_mean_signed=float(ps[ps.oracle <= 3].sgn.mean()), n_low=int((ps.oracle <= 3).sum()),
                  high_mean_signed=float(ps[ps.oracle >= 8].sgn.mean()), n_high=int((ps.oracle >= 8).sum()))

json.dump(R, open(os.path.join(OUT, 'results.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps(R, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))

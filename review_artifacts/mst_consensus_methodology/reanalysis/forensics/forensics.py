"""MST-E crowd-annotation release forensics & coverage.
Run: venv/bin/python -I forensics.py   -> writes results.json next to this script.
Reads data files as data only."""
import json, os, re, glob, hashlib, itertools
from collections import Counter
from math import factorial
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
S = '/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad'
D = '/Users/connielam/Documents/Github/modlli_research/data'
SEED, B = 20231208, 2000
R = {}

a = pd.read_csv(f'{S}/reanalysis/annotations_clean.csv')
raw = pd.read_csv(f'{D}/mste_annotations.csv', dtype=str)
det = pd.read_csv(f'{D}/mst-e_data/mst-e_image_details.csv', dtype=str)
gc = pd.read_csv(f'{D}/mst-e_data/golden_and_adversarial_mst-e_image_ids.csv', dtype=str)
assert len(a) == len(raw) and (a.image.values == raw.image.values).all()
assert (a.mst_annot.values == raw.annotation.str[3:].astype(int).values).all()

# ---------------------------------------------------------------- (1) release defects
r1 = {}
r1['raw_columns'] = list(raw.columns)
r1['raw_rows'] = len(raw)
r1['raw_nunique'] = raw.nunique().to_dict()
r1['raw_subject_values'] = raw.subject.value_counts().to_dict()
r1['raw_region_values'] = raw.region.value_counts().to_dict()
r1['annotation_format_ok'] = bool(raw.annotation.str.fullmatch(r'MST([1-9]|10)').all())
r1['n_missing_cells'] = int(raw.isna().sum().sum())
per_img = a.groupby('image').size()
r1['annotations_per_image'] = {int(k): int(v) for k, v in per_img.value_counts().items()}
r1['n_images_annotated'] = int(per_img.size)
r1['n_true_subjects'] = int(a.subject.nunique())
r1['rows_where_subject_csv_correct'] = int((a.subject_csv == a.subject).sum())
r1['pct_rows_subject_csv_correct'] = round(100 * (a.subject_csv == a.subject).mean(), 2)
exp25 = 25 * per_img.size
r1['expected_rows_if_25_per_image_on_annotated_images'] = int(exp25)
r1['released_fraction_of_25_per_image'] = round(len(a) / exp25, 4)
r1['expected_rows_if_25_per_image_on_1515_images'] = 25 * 1515
# file order
img = a.drop_duplicates('image')[['image', 'subject', 'oracle', 'lighting', 'pose', 'is_golden', 'is_challenging', 'meta_missing']].reset_index(drop=True)
subj_order = img.subject.drop_duplicates().tolist()
r1['file_order'] = {
    'image_blocks_contiguous': int(((a.image != a.image.shift()).cumsum()).max()) == per_img.size,
    'subject_block_count': int((img.subject != img.subject.shift()).sum()),
    'subject_order_in_file': subj_order,
    'subject_order_is_lexicographic': subj_order == sorted(subj_order),
    'last_subject_block_in_file': subj_order[-1],
    'constant_subject_csv_equals_last_subject_block': bool(raw.subject.iloc[0] == subj_order[-1]),
    'subjects_with_images_sorted_by_filename(=capture timestamp)': int(img.groupby('subject').image.apply(lambda s: s.tolist() == sorted(s)).sum()),
}
# folder inventory
files = [(os.path.basename(s), f) for s in sorted(glob.glob(f'{D}/mst-e_data/subject_*')) for f in os.listdir(s)]
fl = pd.DataFrame(files, columns=['folder', 'file'])
fl['ext'] = fl.file.str.extract(r'\.(\w+)$')[0].str.lower()
fl['annotated'] = fl.file.isin(set(a.image))
r1['folder_files_total'] = len(fl)
r1['folder_filenames_unique'] = bool(fl.file.is_unique)
r1['folder_by_ext'] = fl.groupby('ext').annotated.agg(n='size', annotated='sum').astype(int).to_dict('index')
dupcopy = []
for _, row in fl[fl.file.str.startswith('Copy of')].iterrows():
    orig = row.file.replace('Copy of ', '')
    h = [hashlib.sha256(open(f'{D}/mst-e_data/{row.folder}/{x}', 'rb').read()).hexdigest() for x in (row.file, orig)]
    dupcopy.append({'file': row.file, 'folder': row.folder, 'byte_identical_to': orig if h[0] == h[1] else None,
                    'original_annotated': bool(orig in set(a.image))})
r1['copy_of_duplicates'] = dupcopy
det['id_clean'] = det.image_ID.str.strip()
detinfo = det.drop_duplicates('id_clean').set_index('id_clean')
un = fl[(fl.ext == 'jpg') & ~fl.annotated & ~fl.file.str.startswith('Copy of')].copy()
un['pose'] = un.file.map(detinfo.pose); un['lighting'] = un.file.map(detinfo.lighting); un['mask'] = un.file.map(detinfo['mask'])
r1['unannotated_unique_jpgs'] = un[['folder', 'file', 'pose', 'lighting', 'mask']].to_dict('records')
r1['n_unannotated_unique_jpgs'] = len(un)
r1['n_unique_jpgs_in_folders'] = int(((fl.ext == 'jpg') & ~fl.file.str.startswith('Copy of')).sum())
r1['dng_by_folder'] = fl[fl.ext == 'dng'].folder.value_counts().to_dict()
r1['mp4_total'] = int((fl.ext == 'mp4').sum())
stem = fl.file.str.replace(r'(\.PORTRAIT)?\.\w+$', '', regex=True)
jstems = set(stem[fl.ext == 'jpg'])
r1['dng_with_same_stem_jpg'] = int(stem[fl.ext == 'dng'].isin(jstems).sum())
r1['dng_twins_annotated_jpg'] = int(fl[(fl.ext == 'jpg') & stem.isin(set(stem[fl.ext == 'dng']))].annotated.sum())
r1['paper_claims'] = {'images': 1515, 'videos': 31}
r1['image_files_jpg_unique_plus_dng'] = r1['n_unique_jpgs_in_folders'] + int((fl.ext == 'dng').sum())
# data-card distribution vs folders
oracle_by_subject = det.groupby('subject_name').MST.agg(lambda s: s.astype(int).unique().tolist())
assert all(len(v) == 1 for v in oracle_by_subject)
orc = {k: v[0] for k, v in oracle_by_subject.items()}
fl['oracle'] = fl.folder.map(orc)
card_images = dict(zip(range(1, 11), [179, 218, 112, 187, 179, 165, 76, 143, 142, 111]))
card_videos = dict(zip(range(1, 11), [2, 5, 5, 3, 4, 3, 4, 2, 5, 1]))
card_subjects = dict(zip(range(1, 11), [2, 3, 2, 2, 2, 2, 1, 2, 2, 1]))
tab = pd.DataFrame({
    'card_subjects': card_subjects, 'subjects': pd.Series(orc).value_counts(),
    'card_images': card_images,
    'folder_jpg_unique_plus_dng': fl[(fl.ext != 'mp4') & ~fl.file.str.startswith('Copy of')].groupby('oracle').size(),
    'annotated_images': img.groupby('oracle').size(),
    'card_videos': card_videos, 'folder_mp4': fl[fl.ext == 'mp4'].groupby('oracle').size()}).fillna(0).astype(int)
r1['per_mst_level_inventory'] = tab.to_dict('index')
r1['per_mst_level_inventory_totals'] = tab.sum().to_dict()
# details CSV defects
r1['details_csv'] = {
    'rows': len(det), 'columns': list(det.columns[:-1]),
    'ids_with_trailing_or_leading_whitespace': det.image_ID[det.image_ID != det.id_clean].tolist(),
    'non_filename_ids': det[~det.id_clean.str.contains(r'\.')].drop(columns='id_clean').to_dict('records'),
    'duplicated_ids': {k: g.drop(columns=['id_clean']).to_dict('records') for k, g in det[det.id_clean.duplicated(keep=False)].groupby('id_clean')},
    'folder_files_missing_from_details': sorted(set(fl.file) - set(det.id_clean)),
    'annotated_images_missing_from_details': sorted(set(a.image) - set(det.id_clean)),
    'jpgs_with_lighting_video': det[(det.lighting == 'video') & det.id_clean.str.endswith('.jpg')].drop(columns='id_clean').to_dict('records'),
    'mask_values': det['mask'].value_counts().to_dict(),
    'lighting_values': det.lighting.value_counts().to_dict(),
    'pose_values': det.pose.value_counts().to_dict(),
    'data_card_header_mismatches': {'details: image_ID vs card: image_name': 'image_ID' in det.columns,
                                    'golden csv: not_ideal_image_id vs card: challenge_image_id': 'not_ideal_image_id' in gc.columns},
}
# golden / challenging
gc_ok = []
for _, row in gc.iterrows():
    for col, kind in (('golden_image_id', 'golden'), ('not_ideal_image_id', 'challenging')):
        f = row[col].strip()
        hit = fl[fl.file == f]
        gc_ok.append({'subject': row.subject, 'kind': kind, 'image': f, 'in_folder': hit.folder.tolist(),
                      'folder_matches_subject': hit.folder.tolist() == [row.subject],
                      'annotated': f in set(a.image), 'n_annot': int(per_img.get(f, 0)), 'in_details': f in set(det.id_clean)})
r1['golden_challenging_check'] = {
    'n': len(gc_ok), 'all_annotated': all(x['annotated'] for x in gc_ok),
    'all_folder_match': all(x['folder_matches_subject'] for x in gc_ok),
    'not_in_details': [x for x in gc_ok if not x['in_details']],
    'with_4_annotations': [x for x in gc_ok if x['n_annot'] == 4]}
# 3 conflicting-metadata IDs and 2 missing as used in the clean table
r1['clean_table_meta_conflict_images'] = sorted(a[a.meta_conflict].image.unique())
r1['clean_table_meta_missing_images'] = a[a.meta_missing].drop_duplicates('image')[['image', 'subject', 'oracle', 'is_golden', 'is_challenging']].to_dict('records')
# skipped annotations
four = img[img.image.map(per_img) == 4]
r1['images_with_4_annotations'] = four[['image', 'subject', 'oracle', 'lighting', 'pose', 'is_golden', 'is_challenging']].to_dict('records')
r1['four_by_subject'] = four.subject.value_counts().to_dict()
r1['four_by_lighting'] = four.lighting.value_counts(dropna=False).to_dict()
pl = img.lighting.eq('poorly_lit').values; f4 = (img.image.map(per_img) == 4).values
ct = np.array([[(pl & f4).sum(), (pl & ~f4).sum()], [(~pl & f4).sum(), (~pl & ~f4).sum()]])
odds, p = stats.fisher_exact(ct)
r1['four_vs_lighting_fisher'] = {'poorly_lit_4/total': f"{ct[0,0]}/{ct[0].sum()}", 'other_4/total': f"{ct[1,0]}/{ct[1].sum()}",
                                 'odds_ratio': round(odds, 3), 'p': float(p),
                                 'note': 'image-level test, images not independent within subject; descriptive only'}
R['part1_release_defects'] = r1

# ---------------------------------------------------------------- (2) position structure
r2 = {}
seqs = a.groupby('image', sort=False).mst_annot.apply(list)
nc = seqs[seqs.apply(lambda v: len(set(v)) > 1)]
def contiguous(v):
    runs = [k for k, _ in itertools.groupby(v)]
    return len(runs) == len(set(runs))
def p_contig_random(v):  # exact, uniform over distinct arrangements of the multiset
    perms = set(itertools.permutations(v))
    return sum(contiguous(p) for p in perms) / len(perms)
obs_c = int(nc.apply(contiguous).sum()); exp_c = float(nc.apply(p_contig_random).sum())
# exact Poisson-binomial lower tail is overkill; obs==n so P = prod p_i
p_all = float(np.exp(np.sum(np.log(nc.apply(p_contig_random)))))
r2['identical_labels_contiguous_within_image'] = {
    'n_nonconstant_images': len(nc), 'observed': obs_c, 'expected_under_random_order': round(exp_c, 1),
    'log10_P_all_contiguous_under_random_order': round(float(np.sum(np.log10(nc.apply(p_contig_random)))), 1),
    'n_constant_images': int(len(seqs) - len(nc))}
# first-appearance (M1) model of run order: P(run order sigma)=prod_k c_{sigma_k}/sum_{j>=k} c_{sigma_j}
def run_order(v):
    return [k for k, _ in itertools.groupby(v)]
def m1_prob(counts_in_order):
    p, rem = 1.0, sum(counts_in_order)
    for c in counts_in_order:
        p *= c / rem; rem -= c
    return p
gof = {}
asc_obs = asc_exp = desc_obs = desc_exp = 0
for v in nc:
    cnt = Counter(v); ro = run_order(v)
    typ = tuple(sorted(cnt.values(), reverse=True))
    cats = Counter()
    for perm in itertools.permutations(cnt):
        cats[tuple(cnt[x] for x in perm)] += m1_prob([cnt[x] for x in perm])
    d = gof.setdefault(typ, {})
    for k, pr in cats.items():
        d.setdefault(k, [0, 0.0])[1] += pr
    d.setdefault(tuple(cnt[x] for x in ro), [0, 0.0])[0] += 1
    asc_obs += ro == sorted(ro); desc_obs += ro == sorted(ro, reverse=True)
    asc_exp += m1_prob([cnt[x] for x in sorted(cnt)]); desc_exp += m1_prob([cnt[x] for x in sorted(cnt, reverse=True)])
cells = [(t, k, o, e) for t, d in gof.items() for k, (o, e) in d.items()]
big = [c for c in cells if c[3] >= 5]
chi2 = sum((o - e) ** 2 / e for _, _, o, e in big)
dfree = len(big) - len({c[0] for c in big})
r2['run_order_first_appearance_model'] = {
    'description': 'M1: rows of an image are grouped by label, groups ordered by first appearance of that label in a uniformly random underlying order (equivalently size-biased order by count). Cells = (multiset count type, counts in run order).',
    'cells': [{'type': str(t), 'counts_in_run_order': str(k), 'observed': o, 'expected_M1': round(e, 1)} for t, k, o, e in sorted(cells)],
    'pearson_chi2_cells_exp_ge5': round(chi2, 2), 'df': dfree, 'p': float(stats.chi2.sf(chi2, dfree)),
    'runs_in_ascending_value_order': {'observed': int(asc_obs), 'expected_M1': round(asc_exp, 1)},
    'runs_in_descending_value_order': {'observed': int(desc_obs), 'expected_M1': round(desc_exp, 1)},
    'binomial_two_sided_p_ascending_vs_M1_approx': float(stats.binomtest(int(asc_obs), len(nc), asc_exp / len(nc)).pvalue),
}
# position statistics on complete (5-annotation) images
full = a[a.image.map(per_img) == 5].sort_values(['row_in_file'])
X = full.mst_annot.values.reshape(-1, 5)
Y = full.oracle.values.reshape(-1, 5)[:, 0]
subj = full.subject.values.reshape(-1, 5)[:, 0]
assert (full.pos_in_image.values.reshape(-1, 5) == np.arange(1, 6)).all()
n_img = X.shape[0]
subj_codes, subj_idx = np.unique(subj, return_inverse=True)
med = np.median(X, axis=1)
def pos_stats(Xp):
    dev = Xp - Xp.mean(1, keepdims=True)
    return dev.mean(0)
def friedman_vec(Xp, tiecorr):
    rk = stats.rankdata(Xp, axis=1)
    Rj = rk.sum(0); n, k = Xp.shape
    return (12 / (n * k * (k + 1)) * (Rj ** 2).sum() - 3 * n * (k + 1)) / tiecorr
def inter_ss(Xp):  # position x subject interaction on within-image deviations
    dev = Xp - Xp.mean(1, keepdims=True)
    ss = 0.0
    glob_ = dev.mean(0)
    for s in range(len(subj_codes)):
        m = subj_idx == s
        ss += m.sum() * ((dev[m].mean(0) - glob_) ** 2).sum()
    return ss
rk = stats.rankdata(X, axis=1)
tiecorr = 1 - sum(((np.unique(r, return_counts=True)[1] ** 3) - np.unique(r, return_counts=True)[1]).sum() for r in X) / (n_img * 5 * (25 - 1))
fr_obs = friedman_vec(X, tiecorr)
fr_scipy = stats.friedmanchisquare(*X.T)
assert abs(fr_obs - fr_scipy.statistic) < 1e-6
def m1_shuffle(Xm, rng):
    P = rng.permuted(Xm, axis=1)
    first = (P[:, :, None] == P[:, None, :]).argmax(2)
    order = np.argsort(first, axis=1, kind='stable')
    return np.take_along_axis(P, order, 1)
rng = np.random.default_rng(SEED)
obs_dev = pos_stats(X); obs_maxdev = np.abs(obs_dev).max(); obs_int = inter_ss(X)
obs_agree = (X == med[:, None]).mean(0)
null = {'random_order': [], 'M1_grouped': []}
for b in range(B):
    for name, Xs in (('random_order', rng.permuted(X, axis=1)), ('M1_grouped', m1_shuffle(X, rng))):
        dv = pos_stats(Xs)
        null[name].append((friedman_vec(Xs, tiecorr), np.abs(dv).max(), inter_ss(Xs), *dv, *(Xs == med[:, None]).mean(0)))
nulls = {k: np.array(v) for k, v in null.items()}
def ptail(arr, obs):
    return float((1 + (arr >= obs - 1e-12).sum()) / (len(arr) + 1))
r2['position_tests_complete_images'] = {
    'n_images': int(n_img), 'n_subjects': int(len(subj_codes)), 'n_annotations': int(X.size),
    'friedman_chi2': round(float(fr_scipy.statistic), 2), 'friedman_df': 4, 'friedman_p_asymptotic': float(fr_scipy.pvalue),
    'kendalls_W': round(float(fr_scipy.statistic) / (n_img * 4), 4),
    'max_abs_position_mean_deviation_from_image_mean': round(float(obs_maxdev), 4),
    'position_x_subject_interaction_SS': round(float(obs_int), 3),
    'permutation_p': {name: {'friedman': ptail(nl[:, 0], fr_obs), 'max_abs_pos_dev': ptail(nl[:, 1], obs_maxdev),
                             'pos_x_subject_SS': ptail(nl[:, 2], obs_int)} for name, nl in nulls.items()},
    'null_means': {name: {'friedman': round(float(nl[:, 0].mean()), 2), 'max_abs_pos_dev': round(float(nl[:, 1].mean()), 4),
                          'pos_x_subject_SS': round(float(nl[:, 2].mean()), 3),
                          'pos_mean_dev': [round(float(x), 4) for x in nl[:, 3:8].mean(0)],
                          'pos_exact_agree_with_median': [round(float(x), 4) for x in nl[:, 8:13].mean(0)]} for name, nl in nulls.items()},
    'null_note': f'{B} replicates each; random_order = within-image shuffle (exchangeable raters, arbitrary row order); M1_grouped = shuffle then group identical labels by first appearance (matches the observed row-construction). p = (1+#null>=obs)/(B+1).'}
# per-position descriptives with subject-cluster bootstrap
err = X - Y[:, None]
loo_med = np.array([[np.median(np.delete(r, j)) for j in range(5)] for r in X])
per_s = lambda M: np.array([M[subj_idx == s].sum(0) for s in range(len(subj_codes))])  # (19,5)
n_s = np.bincount(subj_idx)
W = np.random.default_rng(SEED + 1).multinomial(len(subj_codes), np.ones(len(subj_codes)) / len(subj_codes), size=B)
def boot_ci(sums):  # ratio estimator of means with subject weights
    est = (W @ sums) / (W @ n_s)[:, None]
    return np.percentile(est, [2.5, 97.5], axis=0)
dev = X - X.mean(1, keepdims=True)
others = (X.sum(1, keepdims=True) - X) / 4
contrast = X - others
metrics = {'mean_signed_error_vs_oracle': err, 'mean_abs_error_vs_oracle': np.abs(err),
           'mean_deviation_from_image_mean': dev, 'contrast_pos_minus_mean_of_other4': contrast,
           'exact_agree_with_image_median(5)': (X == med[:, None]).astype(float),
           'within1_of_image_median(5)': (np.abs(X - med[:, None]) <= 1).astype(float),
           'exact_agree_with_LOO_median(other4)': (X == loo_med).astype(float),
           'within1_of_LOO_median(other4)': (np.abs(X - loo_med) <= 1).astype(float)}
pos_tab = {}
for name, M in metrics.items():
    sums = per_s(M); ci = boot_ci(sums)
    pos_tab[name] = [{'pos': j + 1, 'est': round(float(M[:, j].mean()), 4), 'ci95': [round(float(ci[0, j]), 4), round(float(ci[1, j]), 4)]} for j in range(5)]
r2['per_position_complete_images'] = pos_tab
# pos 1 vs pos 5 contrast, cluster bootstrap
d15 = X[:, 0] - X[:, 4]
sums = np.array([d15[subj_idx == s].sum() for s in range(len(subj_codes))])
est = (W @ sums) / (W @ n_s)
r2['pos1_minus_pos5'] = {'est': round(float(d15.mean()), 4), 'ci95': [round(float(x), 4) for x in np.percentile(est, [2.5, 97.5])],
                         'M1_null_expectation': round(float(nulls['M1_grouped'][:, 3].mean() - nulls['M1_grouped'][:, 7].mean()), 4)}
# --- value-biased first-appearance model (M1-beta): group order is Plackett-Luce with weight c_g*exp(-beta*v_g)
# (exponential race on individual labels with rate exp(-beta*label)); beta=0 is M1; beta>0: darker label groups appear later.
nc_img = nc.index.to_numpy()
nc_subj = np.searchsorted(subj_codes, a.drop_duplicates('image').set_index('image').subject.loc[nc_img].values)
Vm = np.zeros((len(nc), 5)); Cm = np.zeros((len(nc), 5)); Mk = np.zeros((len(nc), 5), bool)
for i, v in enumerate(nc):
    cnt = Counter(v); ro = run_order(v)
    Vm[i, :len(ro)] = ro; Cm[i, :len(ro)] = [cnt[x] for x in ro]; Mk[i, :len(ro)] = True
Vc = Vm - np.where(Mk, Vm, 0).sum(1, keepdims=True) / Mk.sum(1, keepdims=True)  # centre per image (cancels in PL)
def pl_ll_img(beta):
    w = np.where(Mk, Cm * np.exp(-beta * Vc), 0.0)
    den = np.cumsum(w[:, ::-1], 1)[:, ::-1]
    return np.where(Mk, np.log(np.where(Mk, w, 1)) - np.log(np.where(Mk, den, 1)), 0).sum(1)
from scipy.optimize import minimize_scalar
def fit_beta(wts):
    return minimize_scalar(lambda b: -(wts * pl_ll_img(b)).sum(), bounds=(-3, 3), method='bounded', options={'xatol': 1e-6}).x
one = np.ones(len(nc))
beta_hat = fit_beta(one)
ll1, ll0 = pl_ll_img(beta_hat).sum(), pl_ll_img(0.0).sum()
h = 1e-4; info = -(pl_ll_img(beta_hat + h).sum() - 2 * ll1 + pl_ll_img(beta_hat - h).sum()) / h ** 2
beta_bs = np.array([fit_beta(W[b][nc_subj]) for b in range(B)])
per_subj_beta, ll_sep = {}, 0.0
for s in range(len(subj_codes)):
    m = (nc_subj == s).astype(float)
    bs_ = fit_beta(m); per_subj_beta[subj_codes[s]] = {'beta': round(float(bs_), 3), 'n_nonconstant_images': int(m.sum())}
    ll_sep += (m * pl_ll_img(bs_)).sum()
lr_het = 2 * (ll_sep - ll1)
r2['value_biased_first_appearance_model'] = {
    'beta_hat_per_MST_step': round(float(beta_hat), 4), 'se_model': round(float(1 / np.sqrt(info)), 4),
    'ci95_subject_cluster_bootstrap': [round(float(x), 4) for x in np.percentile(beta_bs, [2.5, 97.5])],
    'exp_beta': round(float(np.exp(beta_hat)), 3),
    'LR_vs_M1_beta0': round(float(2 * (ll1 - ll0)), 2), 'LR_p_df1': float(stats.chi2.sf(2 * (ll1 - ll0), 1)),
    'per_subject_beta': per_subj_beta,
    'LR_heterogeneity_19_vs_1_beta': round(float(lr_het), 2), 'LR_het_df': len(subj_codes) - 1,
    'LR_het_p': float(stats.chi2.sf(lr_het, len(subj_codes) - 1)),
    'n_nonconstant_images': int(len(nc)),
    'interpretation': 'odds that a label group appears earlier are multiplied by exp(-beta) per MST step darker, beyond its count'}
def mb_shuffle(Xm, rng, beta):
    keys = rng.exponential(size=Xm.shape) / np.exp(-beta * (Xm - Xm.mean(1, keepdims=True)))
    P = np.take_along_axis(Xm, np.argsort(keys, 1), 1)
    first = (P[:, :, None] == P[:, None, :]).argmax(2)
    return np.take_along_axis(P, np.argsort(first, axis=1, kind='stable'), 1)
rngb = np.random.default_rng(SEED + 2)
nb = []
for b in range(B):
    Xs = mb_shuffle(X, rngb, beta_hat); dv = pos_stats(Xs)
    nb.append((friedman_vec(Xs, tiecorr), np.abs(dv).max(), inter_ss(Xs), *dv, *(Xs == med[:, None]).mean(0)))
nb = np.array(nb)
r2['position_tests_complete_images']['M1_beta_fitted_null'] = {
    'friedman_mean': round(float(nb[:, 0].mean()), 2), 'friedman_p_two_sided': float(min(1, 2 * min(ptail(nb[:, 0], fr_obs), ptail(-nb[:, 0], -fr_obs)))),
    'pos_mean_dev_mean': [round(float(x), 4) for x in nb[:, 3:8].mean(0)],
    'pos_mean_dev_null_95range': [[round(float(x), 4) for x in np.percentile(nb[:, 3 + j], [2.5, 97.5])] for j in range(5)],
    'pos_exact_agree_with_median_mean': [round(float(x), 4) for x in nb[:, 8:13].mean(0)],
    'pos_x_subject_SS_mean': round(float(nb[:, 2].mean()), 3), 'pos_x_subject_SS_p_upper': ptail(nb[:, 2], obs_int),
    'note': 'simulated with common beta_hat (estimated on all images incl. these), so this is a goodness-of-fit check, not an independent test'}
# position x oracle-level descriptive (would expose a fixed region order whose bias depends on skin tone)
po = pd.DataFrame(dev, columns=[f'pos{j+1}' for j in range(5)]); po['oracle'] = Y
r2['mean_deviation_from_image_mean_by_oracle_level'] = po.groupby('oracle').mean().round(3).to_dict('index')
R['part2_position_structure'] = r2

# ---------------------------------------------------------------- (3) category usage
r3 = {}
lv = np.arange(1, 11)
an_s = np.array([[((a.subject == s) & (a.mst_annot == k)).sum() for k in lv] for s in subj_codes])
or_s = np.array([[((a.subject == s) & (a.oracle == k)).sum() for k in lv] for s in subj_codes])
def shares(Wt, M):
    tot = Wt @ M
    return tot / tot.sum(-1, keepdims=True)
sh_a, sh_o = an_s.sum(0) / an_s.sum(), or_s.sum(0) / or_s.sum()
bs_a, bs_o = shares(W, an_s), shares(W, or_s)
diff_ci = np.percentile(bs_a - bs_o, [2.5, 97.5], axis=0)
ratio_ci = np.nanpercentile(bs_a / np.where(bs_o == 0, np.nan, bs_o), [2.5, 97.5], axis=0)
usage = []
for i, k in enumerate(lv):
    usage.append({'MST': int(k), 'n_annotations_with_label': int(an_s[:, i].sum()), 'share_annot': round(float(sh_a[i]), 4),
                  'n_annotations_whose_oracle_is_level': int(or_s[:, i].sum()), 'share_oracle': round(float(sh_o[i]), 4),
                  'diff_pp': round(100 * float(sh_a[i] - sh_o[i]), 2), 'diff_pp_ci95': [round(100 * float(x), 2) for x in diff_ci[:, i]],
                  'ratio': round(float(sh_a[i] / sh_o[i]), 3), 'ratio_ci95': [round(float(x), 3) for x in ratio_ci[:, i]],
                  'n_subjects_with_oracle': int((pd.Series(orc).values == k).sum())})
r3['annotation_level_usage_vs_oracle'] = usage
r3['tv_distance_annot_vs_oracle'] = round(0.5 * float(np.abs(sh_a - sh_o).sum()), 4)
r3['tv_distance_ci95'] = [round(float(x), 4) for x in np.percentile(0.5 * np.abs(bs_a - bs_o).sum(1), [2.5, 97.5])]
# image-level median consensus usage
imgmed = a.groupby('image').agg(med=('mst_annot', 'median'), oracle=('oracle', 'first'), subject=('subject', 'first'))
r3['image_median_distribution'] = {str(k): int(v) for k, v in imgmed.med.value_counts().sort_index().items()}
r3['image_oracle_distribution'] = {int(k): int(v) for k, v in imgmed.oracle.value_counts().sort_index().items()}
r3['n_image_medians_noninteger(4-annotation images)'] = int((imgmed.med % 1 != 0).sum())
# confusion
cm = pd.crosstab(a.oracle, a.mst_annot)
r3['confusion_oracle_rows_annot_cols_counts'] = {int(k): {int(c): int(v) for c, v in row.items()} for k, row in cm.iterrows()}
lvl = a.groupby('oracle').agg(n_subj=('subject', 'nunique'), n_img=('image', 'nunique'), n_ann=('err', 'size'),
                             mean_signed_err=('err', 'mean'), pct_exact=('err', lambda e: 100 * (e == 0).mean()),
                             pct_within1=('err', lambda e: 100 * (e.abs() <= 1).mean()),
                             pct_label_equals_oracle_level_used=('err', lambda e: 100 * (e == 0).mean()))
r3['per_oracle_level_annotation_level'] = lvl.drop(columns='pct_label_equals_oracle_level_used').round(3).to_dict('index')
# global-pool-like check available in this file: per-subject median over all its annotations within 1 of oracle
sm = a.groupby('subject').agg(med=('mst_annot', 'median'), oracle=('oracle', 'first'))
sm['within1'] = (sm.med - sm.oracle).abs() <= 1
r3['subject_pooled_median_within1'] = {'k': int(sm.within1.sum()), 'n_subjects': len(sm), 'pct': round(100 * sm.within1.mean(), 1),
                                       'subjects_failing': sm[~sm.within1].reset_index().to_dict('records'),
                                       'definition': 'median of all crowd labels of a subject in this file (all its images pooled) vs oracle; NOT the paper global 25-label pool'}
imgmed['med_within1'] = (imgmed.med - imgmed.oracle).abs() <= 1
sm2 = imgmed.groupby('subject').agg(med_of_img_meds=('med', 'median'), oracle=('oracle', 'first'), pct_img_within1=('med_within1', 'mean'))
r3['subject_median_of_image_medians_within1'] = {'k': int(((sm2.med_of_img_meds - sm2.oracle).abs() <= 1).sum()), 'n_subjects': len(sm2),
    'failing': sm2[(sm2.med_of_img_meds - sm2.oracle).abs() > 1].reset_index().to_dict('records')}
r3['image_median_within1_pct_all_images'] = round(100 * float(imgmed.med_within1.mean()), 2)
r3['ratio_ci_note'] = 'ratio CI computed over bootstrap draws with nonzero oracle share only; for MST7 and MST10 (1 subject each) it is conditional on that subject being drawn'
r3['bootstrap_draws_with_nonzero_oracle_share'] = {int(k): int((bs_o[:, i] > 0).sum()) for i, k in enumerate(lv)}
R['part3_category_usage'] = r3

R['meta'] = {'seed': SEED, 'bootstrap_B': B, 'bootstrap': 'subject-cluster (19 subjects resampled with replacement; all images/annotations of a drawn subject included; ratio-of-sums estimator); percentile CI'}
with open(os.path.join(HERE, 'results.json'), 'w') as f:
    json.dump(R, f, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps(R, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))[:60000])

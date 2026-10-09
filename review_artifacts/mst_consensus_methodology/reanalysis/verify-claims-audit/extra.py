"""Extra skeptic checks: position (row-order) structure, compression beyond floor/ceiling."""
import sys, json, os, numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
OUT = os.path.dirname(os.path.abspath(__file__))
cl = pd.read_csv(os.path.join(OUT, '..', 'annotations_clean.csv'))
R = {}
# contiguity of image rows in file
blocks = (cl.image != cl.image.shift()).sum()
R['image_blocks_in_file'] = int(blocks); R['n_images'] = int(cl.image.nunique())
# within-image sortedness
srt = cl.groupby('image').mst_annot.apply(lambda v: (np.all(np.diff(v.values) >= 0), np.all(np.diff(v.values) <= 0)))
R['share_images_sorted_asc'] = float(np.mean([a for a, b in srt])); R['share_sorted_desc'] = float(np.mean([b for a, b in srt]))
# expected share sorted asc under random order with ties: simulate
rng = np.random.default_rng(1)
sim = cl.groupby('image').mst_annot.apply(lambda v: np.mean([np.all(np.diff(rng.permutation(v.values)) >= 0) for _ in range(20)]))
R['expected_sorted_asc_random'] = float(sim.mean())
# position effect: two-way additive with image fixed effect, pos as factor (5-annotation images only)
c5 = cl[cl.groupby('image').image.transform('size') == 5]
R['pos_means_err'] = c5.groupby('pos_in_image').err.mean().round(4).to_dict()
wide = c5.pivot(index='image', columns='pos_in_image', values='mst_annot')
R['friedman_pos'] = [float(x) for x in stats.friedmanchisquare(*[wide[c] for c in wide.columns])]
# pos x subject interaction: within each subject, does pos-mean differ by subject? Test via OLS anova
m = smf.ols('mst_annot ~ C(image) + C(pos_in_image) + C(pos_in_image):C(subject)', data=c5).fit()
import statsmodels.api as sm
a = sm.stats.anova_lm(m, typ=1)
R['anova_pos'] = a.loc[['C(pos_in_image)', 'C(pos_in_image):C(subject)'], ['df', 'F', 'PR(>F)']].to_dict('index')
# within-image SD distribution vs what 5 raters of 1 region vs 5 regions might give: just report
R['within_image_sd_mean'] = float(c5.groupby('image').mst_annot.std(ddof=1).mean())
R['within_image_range_dist'] = (c5.groupby('image').mst_annot.agg(lambda v: v.max() - v.min())).value_counts().sort_index().to_dict()
# compression beyond floor/ceiling: drop oracle 1 and 10 subjects
ps = cl.groupby('subject').agg(oracle=('oracle', 'first'), med=('mst_annot', 'median'))
mid = ps[(ps.oracle > 1) & (ps.oracle < 10)]
R['slope_subject_mid'] = float(np.polyfit(mid.oracle, mid.med, 1)[0]); R['n_mid'] = len(mid)
mid2 = ps[(ps.oracle > 2) & (ps.oracle < 9)]
R['slope_subject_3to8'] = float(np.polyfit(mid2.oracle, mid2.med, 1)[0]); R['n_3to8'] = len(mid2)
# subject-level mean annotation slope (continuous, avoids integer median)
ps['mean'] = cl.groupby('subject').mst_annot.mean()
R['slope_subject_mean'] = float(np.polyfit(ps.oracle, ps['mean'], 1)[0])
R['spearman_oracle_med'] = float(stats.spearmanr(ps.oracle, ps.med)[0])
# poorly vs well signed shift: Bonferroni over 6
R['bonf'] = {'poor_well_signed': min(1, 0.025821685791015625 * 6), 'chal_golden_signed': min(1, 0.007629172386487835 * 6)}
json.dump(R, open(os.path.join(OUT, 'extra.json'), 'w'), indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
# reverse regression (oracle on consensus) and per-MST image counts vs data card table
R['reverse_slope_oracle_on_med'] = float(np.polyfit(ps.med, ps.oracle, 1)[0])
R['annotated_images_per_oracle'] = cl.drop_duplicates('image').groupby('oracle').size().to_dict()
R['card_table_images'] = {1: 179, 2: 218, 3: 112, 4: 187, 5: 179, 6: 165, 7: 76, 8: 143, 9: 142, 10: 111}
R['card_table_sum'] = sum(R['card_table_images'].values())
json.dump(R, open(os.path.join(OUT, 'extra.json'), 'w'), indent=1, default=str)
print({k: R[k] for k in ['reverse_slope_oracle_on_med', 'annotated_images_per_oracle', 'card_table_sum']})

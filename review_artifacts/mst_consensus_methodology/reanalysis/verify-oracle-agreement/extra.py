"""Extra checks challenging analyst interpretations. Appends to results_extra.json."""
import json, os
import numpy as np, pandas as pd

S = '/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad'
OUT = os.path.join(S, 'reanalysis/verify-oracle-agreement')
df = pd.read_csv(os.path.join(S, 'reanalysis/annotations_clean.csv'))
g = df.groupby('image')
im = pd.DataFrame({'subject': g.subject.first(), 'oracle': g.oracle.first(), 'med': g.mst_annot.median(),
                   'lighting': g.lighting.first(), 'pose': g.pose.first(), 'n': g.size()})
im['e'] = im.med - im.oracle
subs = sorted(df.subject.unique(), key=lambda s: int(s.split('_')[1])); sidx = {s: i for i, s in enumerate(subs)}
im['si'] = im.subject.map(sidx); df['si'] = df.subject.map(sidx)
X = {}

# 1. per-subject consensus within lighting stratum -> mean |cons - oracle| over 19 subjects (lighting variant for 0.78)
for lt in ['well_lit', 'poorly_lit']:
    d = df[df.lighting == lt]
    pooled = d.groupby('subject').mst_annot.median(); orc = d.groupby('subject').oracle.first()
    mom = im[im.lighting == lt].groupby('subject').med.median()
    X[f'subject_consensus_{lt}'] = {'pooled_abs_mean': round(float((pooled - orc).abs().mean()), 4),
                                    'mom_abs_mean': round(float((mom - orc).abs().mean()), 4),
                                    'pooled_within1': int(((pooled - orc).abs() <= 1).sum()), 'n_subj': int(len(orc))}

# 2. image-level failure (|m-o|>1) by oracle level and by subject
X['img_fail_rate_by_oracle'] = im.groupby('oracle').apply(lambda x: [int((x.e.abs() > 1).sum()), len(x)]).to_dict()
X['img_fail_share_in_4_6'] = round(float(im[(im.e.abs() > 1)].oracle.between(4, 6).mean()), 4)
X['img_share_in_4_6'] = round(float(im.oracle.between(4, 6).mean()), 4)
X['img_fail_by_subject'] = im.groupby('subject').apply(lambda x: round(float((x.e.abs() > 1).mean()), 3)).sort_values(ascending=False).head(6).to_dict()

# 3. oracle-6 annotation distribution per subject (is the bimodality between-subject?)
X['oracle6_by_subject'] = {s: x.mst_annot.value_counts().sort_index().to_dict() for s, x in df[df.oracle == 6].groupby('subject')}

# 4. subject-weighted signed well-poorly difference (paired subject bootstrap)
rng = np.random.default_rng(777); BOOT = rng.multinomial(19, [1 / 19] * 19, size=4000)
def smean(mask):
    x = im[mask]; return x.groupby('si').e.mean().reindex(range(19)).values
w, p = smean(im.lighting == 'well_lit'), smean(im.lighting == 'poorly_lit')
d = w - p
X['subjw_signed_well_minus_poorly'] = [round(float(d.mean()), 4), [round(float(np.percentile(BOOT @ d / 19, q)), 4) for q in (2.5, 97.5)]]
X['subjects_with_well_lit_more_negative'] = int((d < 0).sum())

# 5. 'video' pose/lighting images
X['video_images'] = im[(im.pose == 'video') | (im.lighting == 'video')][['subject', 'oracle', 'med', 'n', 'lighting', 'pose']].reset_index().to_dict('records')

# 6. hex swatch L* monotonicity
def L(h):
    c = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    Y = lin @ np.array([0.2126729, 0.7151522, 0.0721750])
    return 116 * np.cbrt(Y) - 16 if Y > (6 / 29) ** 3 else 903.3 * Y
HEX = ['f6ede4', 'f3e7db', 'f7ead0', 'eadaba', 'd7bd96', 'a07e56', '825c43', '604134', '3a312a', '292420']
X['hex_Lstar'] = [round(float(L(h)), 2) for h in HEX]

# 7. within-subject image resampling with median-of-image-medians consensus (sensitivity of P(18/19))
rng2 = np.random.default_rng(778); cnt = []; stay6 = 0
meds = {s: im.med[im.subject == s].values for s in subs}; orc = im.groupby('subject').oracle.first()
for r in range(2000):
    ok = 0
    for s in subs:
        c = np.median(rng2.choice(meds[s], len(meds[s])))
        w_ = abs(c - orc[s]) <= 1; ok += w_
        if s == 'subject_6': stay6 += w_
    cnt.append(ok)
cnt = np.array(cnt)
X['resample_mom'] = {'P': {int(v): round(float((cnt == v).mean()), 4) for v in np.unique(cnt)}, 'subject_6_stay': stay6 / 2000}

# 8. Signed bias per stratum with CI: is well-lit itself significantly lighter?
X['note'] = 'see results.json b_subsets.well_lit.med.signed for CI'
json.dump(X, open(os.path.join(OUT, 'results_extra.json'), 'w'), indent=1, default=str)
print(json.dumps(X, indent=1, default=str))

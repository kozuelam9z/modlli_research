"""Characterise within-image row order of the released file."""
import os, json, numpy as np, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
cl = pd.read_csv(os.path.join(OUT, '..', 'annotations_clean.csv'))
def kind(v):
    d = np.diff(v)
    if np.all(d == 0): return 'const'
    if np.all(d >= 0): return 'asc'
    if np.all(d <= 0): return 'desc'
    return 'mixed'
g = cl.groupby('image', sort=False)
k = g.mst_annot.apply(lambda v: kind(v.values))
first_row = g.row_in_file.min()
df = pd.DataFrame({'kind': k, 'row': first_row, 'subject': g.subject.first(), 'n': g.size(), 'range': g.mst_annot.agg(lambda v: v.max()-v.min())}).sort_values('row')
R = {'kind_counts': df.kind.value_counts().to_dict()}
# expected under random order, non-const images
rng = np.random.default_rng(0)
exp = {'asc': 0, 'desc': 0, 'mixed': 0, 'const': 0}
for _, v in g.mst_annot:
    for _ in range(50):
        exp[kind(rng.permutation(v.values))] += 1 / 50
R['kind_expected_random'] = {a: round(b, 1) for a, b in exp.items()}
R['kind_by_subject'] = pd.crosstab(df.subject, df.kind).to_dict('index')
# by file decile
df['dec'] = pd.qcut(df.row, 10, labels=False)
R['kind_by_file_decile'] = pd.crosstab(df.dec, df.kind).to_dict('index')
# run lengths of kind along file
runs = (df.kind != df.kind.shift()).cumsum()
R['n_runs'] = int(runs.nunique())
# rank pattern frequencies among images with 5 distinct-ish values: argsort pattern
pat = g.mst_annot.apply(lambda v: ''.join(map(str, np.argsort(np.argsort(v.values, kind='stable'), kind='stable'))) if len(v) == 5 else None).dropna()
R['top_rank_patterns'] = pat.value_counts().head(12).to_dict()
# first 40 images: show values
R['first_images'] = [list(v.values) for _, v in list(g.mst_annot)[:30]]
json.dump(R, open(os.path.join(OUT, 'order.json'), 'w'), indent=1, default=str)
print(json.dumps(R, indent=0, default=str)[:6000])

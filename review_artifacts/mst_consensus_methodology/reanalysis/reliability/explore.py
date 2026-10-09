import pandas as pd, numpy as np
d=pd.read_csv('/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad/reanalysis/annotations_clean.csv')
print(d.dtypes)
g=d.groupby('subject').agg(oracle=('oracle','first'),n_img=('image','nunique'),n=('mst_annot','size'),mean=('mst_annot','mean'),sd=('mst_annot','std'),nor=('oracle','nunique'))
print(g.sort_values('oracle'))
print(d.groupby('image').size().value_counts())
print(d.lighting.value_counts(dropna=False))
print(d.drop_duplicates('image').lighting.value_counts(dropna=False))
print(d[d.is_golden].groupby('subject').image.nunique().sum(), d[d.is_challenging].groupby('subject').image.nunique().sum())
print(d[d.is_golden|d.is_challenging].groupby(['image']).agg(g=('is_golden','first'),c=('is_challenging','first'),n=('mst_annot','size'),light=('lighting','first')).value_counts(['g','c','n','light']))
print(d.mst_annot.value_counts().sort_index())
print(d.groupby('image').image.first().duplicated().sum(), d.image.nunique())
# are image names unique across subjects?
print(d.groupby('image').subject.nunique().max())

import pandas as pd
d=pd.read_csv('/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad/reanalysis/annotations_clean.csv')
im=d.drop_duplicates('image')
print(im[im.is_golden].lighting.value_counts(dropna=False))
print(im[im.is_challenging].lighting.value_counts(dropna=False))
print(pd.crosstab(im.subject, im.lighting.fillna('NA')))
print(d[d.is_golden|d.is_challenging].groupby('image').agg(subj=('subject','first'),g=('is_golden','first'),o=('oracle','first'),r=('mst_annot',lambda x:sorted(x))).sort_values(['g','o']).to_string())

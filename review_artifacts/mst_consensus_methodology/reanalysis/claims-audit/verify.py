"""Independent check: clean table == raw file row-for-row; subject recovered == folder holding the image file; oracle == details MST."""
import os, pandas as pd
S = '/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/258e1bf5-b292-418f-9e28-a4893dc6037a/scratchpad'
D = '/Users/connielam/Documents/Github/modlli_research/data'
raw = pd.read_csv(D + '/mste_annotations.csv'); cl = pd.read_csv(S + '/reanalysis/annotations_clean.csv').sort_values('row_in_file')
assert len(raw) == len(cl) == 7395
assert (raw.image.to_numpy() == cl.image.to_numpy()).all() and (raw.annotation.to_numpy() == cl.annotation.to_numpy()).all()
assert (cl.mst_annot == cl.annotation.str[3:].astype(int)).all()
loc = {}
for s in os.listdir(D + '/mst-e_data'):
    if s.startswith('subject_'):
        for f in os.listdir(f'{D}/mst-e_data/{s}'): loc.setdefault(f, set()).add(s)
dup = {f: v for f, v in loc.items() if len(v) > 1}
fold = cl.image.map(lambda f: next(iter(loc[f])) if f in loc and len(loc[f]) == 1 else None)
print('files in >1 folder:', len(dup), '| annotated images not found in any folder:', int(fold.isna().sum()))
print('subject mismatches vs folder:', int((fold != cl.subject).sum()))
det = pd.read_csv(D + '/mst-e_data/mst-e_image_details.csv')
om = det.groupby('subject_name').MST.first()
print('oracle mismatches:', int((cl.subject.map(om) != cl.oracle).sum()))
# images contiguous in file?
blocks = (cl.image != cl.image.shift()).sum(); print('contiguous image blocks:', int(blocks), 'unique images:', cl.image.nunique())

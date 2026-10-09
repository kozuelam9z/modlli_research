# Is pos_in_image structured (non-exchangeable)? Bears on whether 'Ghana'/5 raters per image is a safe reading.
import json, math
from pathlib import Path
import numpy as np, pandas as pd
OUT = Path(__file__).resolve().parent
d = pd.read_csv(OUT.parent / "annotations_clean.csv")
rng = np.random.default_rng(777)
# contiguity of image rows in file
contig = d.groupby("image").row_in_file.agg(lambda r: r.max() - r.min() + 1 == len(r)).mean()
f = d[d.groupby("image").image.transform("size") == 5]
W = f.pivot(index="image", columns="pos_in_image", values="mst_annot")
dev = W.sub(W.mean(1), axis=0)                      # within-image deviation by slot
sub = f.drop_duplicates("image").set_index("image").loc[W.index, ["subject", "oracle"]]
slot_dev = dev.mean()
subs = sub.subject.unique()
idx = {s: np.where(sub.subject.values == s)[0] for s in subs}
bt = np.array([dev.values[np.concatenate([idx[x] for x in rng.choice(subs, len(subs))])].mean(0) for _ in range(2000)])
band = pd.cut(sub.oracle, [0, 3, 7, 10], labels=["light", "mid", "dark"])
by_band = dev.groupby(band.values).mean()
# share of images whose slot sequence is monotone vs expectation under random order
seq = W.values
nondec = np.mean([np.all(np.diff(r) >= 0) for r in seq]); noninc = np.mean([np.all(np.diff(r) <= 0) for r in seq])
exp = np.mean([math.prod(math.factorial(c) for c in np.unique(r, return_counts=True)[1]) / 120 for r in seq])
res = dict(rows_contiguous_share=float(contig), slot_mean_dev=slot_dev.round(3).to_dict(),
           slot_dev_boot_lo=dict(zip(range(1, 6), np.percentile(bt, 2.5, 0).round(3))),
           slot_dev_boot_hi=dict(zip(range(1, 6), np.percentile(bt, 97.5, 0).round(3))),
           slot_dev_by_band={k: v.round(3).to_dict() for k, v in by_band.iterrows()},
           nondecreasing=float(nondec), nonincreasing=float(noninc), expected_each_if_random=float(exp))
print(json.dumps(res, indent=1, default=str))
(OUT / "slotcheck.json").write_text(json.dumps(res, indent=1, default=str))

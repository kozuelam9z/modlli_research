"""Build the canonical cleaned annotation table for the MST-E reanalysis."""
import sys, os, numpy as np, pandas as pd
ANN, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
a = pd.read_csv(ANN)
a["row_in_file"] = np.arange(len(a))
a["pos_in_image"] = a.groupby("image").cumcount() + 1
a["mst_annot"] = a.annotation.str.replace("MST", "").astype(int)
a = a.rename(columns={"subject": "subject_csv", "region": "region_csv"})
m = pd.read_csv(f"{DATA}/mst-e_image_details.csv")
m["image_ID"] = m.image_ID.str.strip()
dup = m[m.image_ID.duplicated(keep=False)].groupby("image_ID").agg(lambda s: "|".join(map(str, sorted(set(s)))))
m1 = m.drop_duplicates("image_ID").set_index("image_ID")
# folder listing gives ground-truth subject for every file
folder = {}
for sd in os.listdir(DATA):
    if sd.startswith("subject_") and os.path.isdir(f"{DATA}/{sd}"):
        for f in os.listdir(f"{DATA}/{sd}"): folder.setdefault(f, set()).add(sd)
a["subject_folder"] = a.image.map(lambda x: "|".join(sorted(folder.get(x, {"MISSING"}))))
a["subject_details"] = a.image.map(m1.subject_name)
a["subject"] = a.subject_details.fillna(a.subject_folder)
oracle = m.groupby("subject_name").MST.first()
a["oracle"] = a.subject.map(oracle)
for c in ["pose", "lighting", "mask"]: a[c] = a.image.map(m1[c])
a["meta_missing"] = a.subject_details.isna()
a["meta_conflict"] = a.image.isin(dup.index)
g = pd.read_csv(f"{DATA}/golden_and_adversarial_mst-e_image_ids.csv")
a["is_golden"] = a.image.isin(g.golden_image_id)
a["is_challenging"] = a.image.isin(g.not_ideal_image_id)
a["err"] = a.mst_annot - a.oracle
a.to_csv(f"{OUT}/annotations_clean.csv", index=False)
print("rows", len(a), "images", a.image.nunique())
print("subject_folder ambiguous/missing:", (a.subject_folder.str.contains(r"\|") | (a.subject_folder=="MISSING")).sum())
print("details vs folder subject disagreements:", ((a.subject_details.notna()) & (a.subject_details != a.subject_folder)).sum())
print("meta missing images:", a[a.meta_missing].image.unique().tolist(), a[a.meta_missing].subject.unique().tolist())
print("conflicting-metadata images annotated:", a[a.meta_conflict].image.unique().tolist())
print("golden imgs annotated:", a[a.is_golden].image.nunique(), "challenging:", a[a.is_challenging].image.nunique())
print("images/subject:", a.groupby("subject").image.nunique().to_dict())
print("lighting:", a.drop_duplicates("image").lighting.value_counts(dropna=False).to_dict())
print("ext of annotated:", a.image.str.extract(r"\.([A-Za-z0-9]+)\s*$")[0].str.lower().value_counts().to_dict())
na = sorted(set(m.image_ID) - set(a.image))
print("not annotated:", len(na), pd.Series(na).str.extract(r"\.([A-Za-z0-9 ]+)$")[0].str.strip().str.lower().value_counts().to_dict(), [x for x in na if not x.lower().endswith(("mp4","dng"))])
print("4-annotation images:", a.groupby("image").size().pipe(lambda s: s[s==4]).index.map(lambda x: (x, a[a.image==x].subject.iloc[0], a[a.image==x].lighting.iloc[0])).tolist())

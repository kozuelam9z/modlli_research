import os, itertools, numpy as np, pandas as pd
DATA="/Users/connielam/Documents/Github/modlli_research/data"; MSTE=f"{DATA}/mst-e_data"
raw=pd.read_csv(f"{DATA}/mste_annotations.csv",dtype=str); raw["mst"]=raw.annotation.str[3:].astype(int)
fmap={f:d for d in os.listdir(MSTE) if d.startswith("subject_") for f in os.listdir(f"{MSTE}/{d}")}
raw["s"]=raw.image.map(fmap)
det=pd.read_csv(f"{MSTE}/mst-e_image_details.csv",dtype=str,keep_default_na=False)
nm=det[~det.image_ID.str.strip().str.endswith(".mp4")]
print("details non-mp4 rows by MST:", nm.MST.astype(int).value_counts().sort_index().to_dict(), "sum", len(nm))
for S in ["subject_7","subject_1","subject_3"]:
    hi_first=0; e_hi_first=0; n2=0; dsum=[]
    for im,g in raw[raw.s==S].groupby("image",sort=False):
        r=[(k,len(list(x))) for k,x in itertools.groupby(g.mst)]
        if len(r)!=2: continue
        n2+=1; (v1,c1),(v2,c2)=r
        hi_first+= v1>v2; e_hi_first+= (c1 if v1>v2 else c2)/(c1+c2)
        dsum.append((v1-v2))
    print(S,"2-run imgs",n2,"higher-first obs",hi_first,"exp",round(e_hi_first,1))

"""PL run-order beta split by number of runs (2 vs >=3), overall and for a few subjects."""
import os, itertools, json, numpy as np, pandas as pd
from scipy import optimize
DATA="/Users/connielam/Documents/Github/modlli_research/data"; MSTE=f"{DATA}/mst-e_data"
raw=pd.read_csv(f"{DATA}/mste_annotations.csv",dtype=str); raw["mst"]=raw.annotation.str[3:].astype(int)
fmap={f:d for d in os.listdir(MSTE) if d.startswith("subject_") for f in os.listdir(f"{MSTE}/{d}")}
raw["s"]=raw.image.map(fmap)
D=[]
for im,g in raw.groupby("image",sort=False):
    r=[(k,len(list(x))) for k,x in itertools.groupby(g.mst)]
    if len(r)<2: continue
    v=np.array([k for k,_ in r],float); D.append((g.s.iloc[0],np.array([c for _,c in r],float),v-v.mean()))
def nll(b,d):
    t=0
    for _,c,v in d:
        w=np.log(c)-b*v
        for i in range(len(c)-1): t-=w[i]-np.logaddexp.reduce(w[i:])
    return t
fit=lambda d: optimize.minimize_scalar(nll,bounds=(-5,5),args=(d,),method="bounded").x if d else None
out={}
for name,sel in [("all",lambda x:True),("2runs",lambda x:len(x[1])==2),("3plus",lambda x:len(x[1])>=3)]:
    out[name]={"n":sum(map(sel,D)),"beta":fit([x for x in D if sel(x)])}
for S in ["subject_7","subject_1","subject_8","subject_3"]:
    out[S]={k:fit([x for x in D if x[0]==S and f(x)]) for k,f in [("2runs",lambda x:len(x[1])==2),("3plus",lambda x:len(x[1])>=3)]}
print(json.dumps(out,indent=1)); json.dump(out,open("beta_by_runs.json","w"),indent=1)

"""Check whether mask/pose minor differences come from including the 2 'video'-lit images. Run: venv/bin/python -I minor_check.py"""
from pathlib import Path
import pandas as pd
OUT = Path(__file__).resolve().parent
d = pd.read_csv(OUT.parent / "annotations_clean.csv")
img = d.groupby("image").agg(s=("subject", "first"), o=("oracle", "first"), L=("lighting", "first"), p=("pose", "first"),
                             m=("mask", "first"), a=("mst_annot", "mean")).reset_index()
img["e"] = img.a - img.o
print(img[img.L.isin(["video"]) | img.L.isna()][["image", "s", "L", "p", "m"]])
def c(f, col, a, b):
    g = f.groupby(["s", col]).e.mean().unstack(); return (g[a] - g[b]).dropna()
f = img.dropna(subset=["m"]).copy(); f["mk"] = f.m.map({1.0: "m", 0.0: "u"})
x = c(f, "mk", "m", "u"); print("mask incl video", round(x.mean(), 4), len(x), f[f.s.isin(x.index)].mk.value_counts().to_dict())
for q in ["bottom", "frontal", "side"]:
    print(q, "incl video", round(c(img, "p", q, "facing_camera").mean(), 4))

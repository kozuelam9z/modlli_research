import json, sys, csv
import numpy as np
from PIL import Image
from multiprocessing import Pool
from skincolor import cheek_mask, score
SP = sys.argv[1]
d = json.load(open(SP + "/mste_proc/landmarks.json"))
def work(r):
    if not r.get("faces"): return None
    f = max(r["faces"], key=lambda f: f["bbox"][2] * f["bbox"][3])
    m = cheek_mask(r["w"], r["h"], f)
    if m is None or m.sum() < 300: return None
    im = np.asarray(Image.open(SP + "/mste_proc/img/" + r["out"]).convert("RGB"))
    L, h, Lm, hm, n = score(im, m)
    return {"subject": r["subject"], "file": r["file"], "L_ck": L, "h_ck": h, "Lmean_ck": Lm, "hmean_ck": hm, "npix_ck": n}
if __name__ == "__main__":
    with Pool(8) as p:
        res = [x for x in p.map(work, d, chunksize=8) if x]
    with open(SP + "/mste_proc/scores_cheeks.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
    print("scored", len(res))

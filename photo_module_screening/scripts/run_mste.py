import json, sys, csv
import numpy as np
from PIL import Image
from multiprocessing import Pool
from skincolor import face_mask, score

SP = sys.argv[1]
d = json.load(open(SP + "/mste_proc/landmarks.json"))


def work(r):
    if not r.get("faces"):
        return None
    f = max(r["faces"], key=lambda f: f["bbox"][2] * f["bbox"][3])
    im = np.asarray(Image.open(SP + "/mste_proc/img/" + r["out"]).convert("RGB"))
    out = {"subject": r["subject"], "file": r["file"], "yaw": f.get("yaw"), "face_w": f["bbox"][2]}
    for tag, fh in (("full", True), ("nofh", False)):
        m = face_mask(r["w"], r["h"], f, forehead=fh)
        if m is None or m.sum() < 500:
            return None
        L, h, Lmean, hmean, n = score(im, m)
        out.update({f"L_{tag}": L, f"h_{tag}": h, f"Lmean_{tag}": Lmean, f"hmean_{tag}": hmean, f"npix_{tag}": n})
    return out


if __name__ == "__main__":
    with Pool(8) as p:
        res = [x for x in p.map(work, d, chunksize=8) if x]
    keys = list(res[0].keys())
    with open(SP + "/mste_proc/scores.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(res)
    print("scored", len(res))

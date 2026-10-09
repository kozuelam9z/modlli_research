"""Candidate skin-colour estimators for the Modlii photo-module screen (MST-E).

C1  cheek ROI, plain median Lab
C2  cheek ROI, L* 10-90 pct trim + chroma gate (drop C* < P25), median Lab
C3  C2 after shades-of-grey (p=6) white balance on non-face pixels (chromatic only)
C4  C2 after background white-reference (top corners) WB + exposure normalisation
(C0 = Thong et al. estimator, already scored in scored_merged.csv / scores_cheeks.csv)
Every candidate returns L*, C*, h* (atan2, [0,360)) or an abstain reason.
"""
import json, sys, csv
import numpy as np
from PIL import Image
from multiprocessing import Pool
from skincolor import rgb2lab, cheek_mask

M_Y = np.array([0.212671, 0.715160, 0.072169])  # sRGB -> Y


def lin(s): return np.where(s > 0.04045, ((s + 0.055) / 1.055) ** 2.4, s / 12.92)
def enc(l): return np.where(l > 0.0031308, 1.055 * np.abs(l) ** (1 / 2.4) - 0.055, 12.92 * l)


def lch(lab):
    L, a, b = np.median(lab[:, 0]), np.median(lab[:, 1]), np.median(lab[:, 2])
    return float(L), float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)


def robust(lab):
    lab = lab[np.isfinite(lab).all(1)]  # WB with a zero illuminant channel yields inf/nan
    if len(lab) < 150:
        return lab[:0]
    lo, hi = np.percentile(lab[:, 0], [10, 90])
    k = lab[(lab[:, 0] >= lo) & (lab[:, 0] <= hi)]
    C = np.hypot(k[:, 1], k[:, 2])
    return k[C >= np.percentile(C, 25)]


def wb(linimg, e, target_y=None):
    """Diagonal (von Kries) correction for illuminant estimate e (linear RGB).
    Chromatic only (neutral luminance kept) unless target_y is given."""
    e = np.asarray(e, float)
    e = e / (e @ M_Y) if target_y is None else e / target_y
    return linimg / e


def shades_of_grey(linimg, keep, p=6):
    px = linimg[keep]
    return np.mean(px ** p, axis=0) ** (1 / p)


def gates(srgb_roi, lab_roi):
    if len(lab_roi) < 300: return "roi_small"
    if np.mean((srgb_roi >= 0.98).any(1) | (srgb_roi <= 0.02).any(1)) > 0.25: return "clipped"
    if np.median(lab_roi[:, 0]) < 10: return "too_dark"
    return None


def work(args):
    SP, r = args
    if not r.get("faces"): return None
    f = max(r["faces"], key=lambda f: f["bbox"][2] * f["bbox"][3])
    m = cheek_mask(r["w"], r["h"], f)
    if m is None: return None
    img = np.asarray(Image.open(SP + "/mste_proc/img/" + r["out"]).convert("RGB")).astype(float) / 255
    L_img = lin(img)
    out = {"subject": r["subject"], "file": r["file"]}
    roi = img[m]; lab = rgb2lab(roi)
    out["gate"] = gates(roi, lab) or ""
    if len(lab) < 300:  # too few ROI pixels: nothing to estimate
        out["gate4"] = "roi_small"
        return out
    out["C1"] = lch(lab)
    rb = robust(lab)
    out["C2"] = lch(rb) if len(rb) >= 150 else None
    # non-face pixels: outside an expanded face box
    x, y, w, h = f["bbox"]; H, W = img.shape[:2]
    nonface = np.ones((H, W), bool)
    nonface[max(0, int(y - .6 * h)):int(y + 1.4 * h), max(0, int(x - .4 * w)):int(x + 1.4 * w)] = False
    e3 = shades_of_grey(L_img, nonface)
    lab3 = rgb2lab(enc(wb(L_img, e3))[m])
    rb3 = robust(lab3); out["C3"] = lch(rb3) if len(rb3) >= 150 else None
    # background reference: top corners, outside the face box
    cw, ch = int(.15 * W), int(.12 * H)
    corner = np.zeros((H, W), bool); corner[:ch, :cw] = True; corner[:ch, -cw:] = True
    corner &= nonface
    Yc = L_img[corner] @ M_Y
    if corner.sum() < 500 or np.median(Yc) < 0.05 or np.std(Yc) / max(np.mean(Yc), 1e-6) > 0.5:
        out["C4"] = None; out["gate4"] = "no_reference"
    else:
        lab4 = rgb2lab(enc(wb(L_img, np.median(L_img[corner], axis=0), target_y=0.8))[m])
        rb4 = robust(lab4); out["C4"] = lch(rb4) if len(rb4) >= 150 else None; out["gate4"] = ""
    return out


def selftest():
    # a neutral patch under a reddish illuminant becomes neutral and keeps luminance
    e = np.array([1.3, 1.0, 0.6]); patch = 0.4 * e
    fixed = wb(patch[None], e)[0]
    assert np.allclose(fixed / fixed[0], 1) and abs(fixed @ M_Y - patch @ M_Y) < 1e-9
    assert abs(lch(np.array([[50., -1., 1.]]))[2] - 135) < 1e-9  # quadrant II, atan2
    assert np.allclose(enc(lin(np.linspace(0, 1, 11))), np.linspace(0, 1, 11))
    print("selftest ok")


if __name__ == "__main__":
    SP = sys.argv[1]
    selftest()
    d = json.load(open(SP + "/mste_proc/landmarks.json"))
    with Pool(8) as p:
        res = [x for x in p.map(work, [(SP, r) for r in d], chunksize=8) if x]
    rows = []
    for x in res:
        row = {"subject": x["subject"], "file": x["file"], "gate": x["gate"], "gate4": x.get("gate4", "")}
        for c in ("C1", "C2", "C3", "C4"):
            v = x.get(c) or (np.nan, np.nan, np.nan)
            row.update({f"{c}_L": v[0], f"{c}_C": v[1], f"{c}_h": v[2]})
        rows.append(row)
    with open(SP + "/mste_proc/candidates.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("rows", len(rows))

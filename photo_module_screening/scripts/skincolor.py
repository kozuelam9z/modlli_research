"""Replication of SonyResearch/apparent_skincolor extract/predict.py (as documented
via its source: gaussian sigma=1 truncate=4 -> skimage rgb2lab (D65/2deg) ->
hue = degrees(arctan(b/(a+1e-8))) -> KMeans(5, random_state=2021) on raw [L, hue]
-> per-cluster histogram mode (bins='sturges', left edge) -> top-3 clusters by
mode L, pixel-count-weighted average). Mask comes from Apple Vision landmarks
(approximation of a CelebAMask-HQ 'skin' mask)."""
import numpy as np
from scipy.ndimage import gaussian_filter, binary_erosion
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans

WHITE_D65 = np.array([0.95047, 1.0, 1.08883])
M = np.array([[0.412453, 0.357580, 0.180423],
              [0.212671, 0.715160, 0.072169],
              [0.019334, 0.119193, 0.950227]])


def rgb2lab(rgb):  # rgb float in [0,1], (..., 3); same constants as skimage
    c = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    xyz = c @ M.T / WHITE_D65
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)


def mode_left_edge(x):
    hist, edges = np.histogram(x, bins="sturges")
    return edges[hist.argmax()]


def score(img_u8, mask, k=5, topk=3, hue_fn="arctan"):
    img = img_u8.astype(np.float64) / 255.0
    sm = gaussian_filter(img, sigma=(1, 1, 0), truncate=4, mode="nearest")
    lab = rgb2lab(sm[mask])
    L, a, b = lab[:, 0], lab[:, 1], lab[:, 2]
    if hue_fn == "arctan":
        hue = np.degrees(np.arctan(b / (a + 1e-8)))
    else:  # full-circle variant
        hue = np.degrees(np.arctan2(b, a))
    X = np.vstack([L, hue]).T
    lab_ = KMeans(n_clusters=k, random_state=2021, n_init=10).fit_predict(X)
    lum, hh, n = [], [], []
    for c in range(k):
        s = lab_ == c
        if s.sum() < 2:
            continue
        lum.append(mode_left_edge(L[s])); hh.append(mode_left_edge(hue[s])); n.append(s.sum())
    lum, hh, n = map(np.array, (lum, hh, n))
    idx = np.argsort(lum)[::-1][:topk]
    return (float(np.average(lum[idx], weights=n[idx])), float(np.average(hh[idx], weights=n[idx])),
            float(np.mean(L)), float(np.degrees(np.arctan2(np.mean(b), np.mean(a)))), int(mask.sum()))


def face_mask(w, h, f, forehead=True, erode_frac=0.03):
    """Skin polygon: hull of jaw contour + (optionally raised) brows, minus eyes,
    brows, lips and nose, then eroded."""
    contour = np.array(f.get("faceContour") or [])
    lb, rb = np.array(f.get("leftEyebrow") or []), np.array(f.get("rightEyebrow") or [])
    le, re_ = np.array(f.get("leftEye") or []), np.array(f.get("rightEye") or [])
    if len(contour) < 5 or len(lb) == 0 or len(rb) == 0 or len(le) == 0 or len(re_) == 0:
        return None
    brows = np.vstack([lb, rb])
    pts = [contour, brows]
    if forehead:
        eye_y = np.vstack([le, re_])[:, 1].mean()
        lift = 0.8 * (eye_y - brows[:, 1].mean())
        pts.append(brows - np.array([0, lift]))
    allp = np.vstack(pts)
    from scipy.spatial import ConvexHull
    hull = allp[ConvexHull(allp).vertices]
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.polygon([tuple(p) for p in hull], fill=1)
    face_w = np.ptp(contour[:, 0])
    pad = max(2, int(0.025 * face_w))
    for key in ("leftEye", "rightEye", "leftEyebrow", "rightEyebrow", "outerLips", "nose"):
        p = np.array(f.get(key) or [])
        if len(p) < 3:
            continue
        if key == "nose":  # nose region: hull of nose outline
            ph = p[ConvexHull(p).vertices]
            d.polygon([tuple(q) for q in ph], fill=0)
        else:
            c = p.mean(0)
            ph = c + (p - c) * 1.35  # dilate around centroid
            try:
                ph = ph[ConvexHull(ph).vertices]
            except Exception:
                pass
            d.polygon([tuple(q) for q in ph], fill=0)
            d.line([tuple(q) for q in np.vstack([ph, ph[:1]])], fill=0, width=pad)
    mask = np.asarray(m, dtype=bool)
    it = max(1, int(erode_frac * face_w))
    mask = binary_erosion(mask, iterations=it)
    return mask


def cheek_mask(w, h, f):
    """Merler-style cheek patches: below each eye, lateral to the nose, above the
    mouth line, inside the jaw contour hull."""
    from scipy.spatial import ConvexHull
    contour = np.array(f.get("faceContour") or []); nose = np.array(f.get("nose") or [])
    le, re_ = np.array(f.get("leftEye") or []), np.array(f.get("rightEye") or [])
    lips = np.array(f.get("outerLips") or [])
    if min(len(contour), len(nose), len(le), len(re_), len(lips)) < 3:
        return None
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    eye_bot = max(le[:, 1].max(), re_[:, 1].max())
    mouth_y = lips[:, 1].mean()
    y0 = eye_bot + 0.25 * (mouth_y - eye_bot); y1 = mouth_y
    nx0, nx1 = nose[:, 0].min(), nose[:, 0].max()
    for eye in (le, re_):
        ex = eye[:, 0].mean()
        if ex < nx0:
            xa = ex - 0.6 * (nx0 - ex) - 0.15 * np.ptp(contour[:, 0]); xb = nx0 - 0.1 * (nx0 - ex)
        else:
            xa = nx1 + 0.1 * (ex - nx1); xb = ex + 0.6 * (ex - nx1) + 0.15 * np.ptp(contour[:, 0])
        if xb > xa and y1 > y0: d.rectangle([xa, y0, xb, y1], fill=1)
    hull = Image.new("L", (w, h), 0)
    ImageDraw.Draw(hull).polygon([tuple(p) for p in contour[ConvexHull(contour).vertices]], fill=1)
    mask = np.asarray(m, dtype=bool) & binary_erosion(np.asarray(hull, dtype=bool), iterations=max(1, int(0.04 * np.ptp(contour[:, 0]))))
    return mask

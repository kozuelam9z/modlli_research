"""L*, a*, b*, h* (atan2), ITA of the official MST orb PNGs (median of opaque pixels)."""
import sys, numpy as np
from PIL import Image
from skincolor import rgb2lab
D = sys.argv[1]
for i in range(1, 11):
    im = np.asarray(Image.open(f"{D}/MST_{i}.png").convert("RGBA")).astype(float) / 255
    L, a, b = np.median(rgb2lab(im[im[..., 3] > 0.99][:, :3]), 0)
    C = np.hypot(a, b)
    print(f"MST{i}: L*={L:.1f} a*={a:.1f} b*={b:.1f} C*={C:.1f} h*={np.degrees(np.arctan2(b, a)):.1f} "
          f"ITA={np.degrees(np.arctan((L - 50) / b)):.1f} dh/da={np.degrees(b / C**2):.1f}deg/unit")

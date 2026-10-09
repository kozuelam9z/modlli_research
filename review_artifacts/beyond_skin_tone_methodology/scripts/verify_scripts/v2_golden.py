"""Golden vs not-ideal pairs: are the 4-cell changes tone or hue flips? Also Fig.4 deltas and Elo t approximations."""
import pandas as pd, numpy as np
SP = "/private/tmp/claude-501/-Users-connielam-Documents-Github-modlli-research/aa16d469-2438-4934-be22-436934f5e296/scratchpad"
df = pd.read_csv(SP + "/mste_proc/scored_merged.csv")
g = pd.read_csv("/Users/connielam/Documents/Github/modlli_research/data/mst-e_data/golden_and_adversarial_mst-e_image_ids.csv")
m = g.merge(df[["file", "L_full", "h_full", "hmean_full", "lighting", "pose"]].add_suffix("_g"), left_on="golden_image_id", right_on="file_g") \
     .merge(df[["file", "L_full", "h_full", "hmean_full", "lighting", "pose"]].add_suffix("_n"), left_on="not_ideal_image_id", right_on="file_n")
m["tone_flip"] = (m.L_full_g >= 60) != (m.L_full_n >= 60); m["hue_flip"] = (m.h_full_g >= 55) != (m.h_full_n >= 55)
m["dh"] = m.h_full_n - m.h_full_g; m["dh_mean"] = m.hmean_full_n - m.hmean_full_g
print(m[["subject", "lighting_g", "lighting_n", "pose_g", "pose_n", "L_full_g", "L_full_n", "h_full_g", "h_full_n", "dh", "dh_mean", "tone_flip", "hue_flip"]].round(1).to_string())
print("n", len(m), "tone flips", m.tone_flip.sum(), "hue flips", m.hue_flip.sum(), "|dh| mean", m.dh.abs().mean().round(1), "|dh_pixmean| mean", m.dh_mean.abs().mean().round(1))
# Fig 4 deltas vs reconstructed (L, h) for 3 faces
rec = [(61.92, 46.76), (44.43, 70.19), (72.15, 55.96)]
edits = {"+light": [(71.74, 45.76), (58.73, 68.82), (77.43, 55.88)], "+dark": [(48.20, 46.69), (23.78, 73.71), (62.40, 56.84)],
         "+red": [(64.09, 36.76), (52.05, 57.32), (71.34, 42.16)], "+yellow": [(61.50, 55.27), (46.70, 77.13), (75.92, 66.32)],
         "+pale": [(69.56, 47.87), (60.48, 77.55), (80.60, 59.47)], "-pale": [(54.91, 43.54), (27.55, 61.59), (61.40, 51.70)]}
for k, v in edits.items():
    print(k, [(round(L - r[0], 2), round(h - r[1], 2)) for (L, h), r in zip(v, rec)])
# Elo: implied gaps and rough t under assumed rating SD
for p in (0.6073, 0.5825):
    print("pref", p, "gap", round(400 * np.log10(p / (1 - p)), 1))
for sd in (100, 130, 160):
    for nm, gap, n1, n2 in (("tone", 75.7, 461, 278), ("hue", 57.9, 206, 533)):
        se = sd * np.sqrt(1 / n1 + 1 / n2); print(f"SD={sd} {nm}: t~{gap / se:.1f}; with design effect 2: t~{gap / se / np.sqrt(2):.1f}")
print("games/face range:", round(4500 / 104, 1), "-", round(4500 / 52, 1))
print("red light share", round(127 / 206, 4), "yellow light share", round(334 / 533, 4), "CFD yellow", round(533 / 739, 4))
for nm, LR, LY, DR, DY in (("CelebA", 46.95, 27.48, 19.28, 6.29), ("FFHQ", 52.82, 13.44, 29.06, 4.68), ("CFD", 127, 334, 79, 199)):
    print(nm, "OR(red | light vs dark)=", round((LR / LY) / (DR / DY), 3))

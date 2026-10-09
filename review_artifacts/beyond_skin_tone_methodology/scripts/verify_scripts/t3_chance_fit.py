"""V3: how often does a RANDOM 9-tuple (Dlib row jittered by U(-0.5,0.5) pp, 2 dp) admit an exact
N<=1000 partition fit? Calibrates how informative Dlib's unique exact fit is."""
import random
TOL = 0.005 + 1e-9
ok = lambda k, n, r: abs(100 * k / n - r) <= TOL


def feas(r, NMAX=1000):
    out = []
    for n in range(1, NMAX + 1):
        k0 = int(r * n / 100)
        out += [(n, k) for k in (k0, k0 + 1) if k <= n and ok(k, n, r)]
    return out


def nsol(v, NMAX=1000):
    f = [feas(r) for r in v[5:]]
    light = [(a, b) for a in f[0] for b in f[1] if a[0] + b[0] < NMAX and ok(a[1] + b[1], a[0] + b[0], v[1])]
    dark = [(a, b) for a in f[2] for b in f[3] if a[0] + b[0] < NMAX and ok(a[1] + b[1], a[0] + b[0], v[2])]
    s = 0
    for lr, ly in light:
        for dr, dy in dark:
            N = lr[0] + ly[0] + dr[0] + dy[0]
            if N <= NMAX and ok(lr[1] + dr[1], lr[0] + dr[0], v[3]) and ok(ly[1] + dy[1], ly[0] + dy[0], v[4]) \
                    and ok(lr[1] + ly[1] + dr[1] + dy[1], N, v[0]):
                s += 1
    return s


random.seed(1)
base = [94.20, 94.41, 93.68, 94.71, 93.58, 94.83, 93.90, 94.41, 92.74]
trials, hits, hits900 = 400, 0, 0
for _ in range(trials):
    v = [round(x + random.uniform(-0.5, 0.5), 2) for x in base]
    hits += nsol(v) > 0
print(f"random jittered rows with ANY exact partition fit (N<=1000): {hits}/{trials}")
print("Dlib actual:", nsol(base))

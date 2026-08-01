"""fig1 — the manuscript's curve figure (paper/figures/curve.pdf).

VISUALIZATION ONLY: no new outcome quantities. The bootstrap band is obtained by
deterministically REPLAYING the protocol's seeded bootstrap (same generator
numpy.random.default_rng(20261001), same draw order, same grids and fitting
procedure via exp4_protocol's own functions), storing full parameter vectors per
resample to evaluate the curve across ages. Verification printed: the refit
primary parameters must match the reported execution values, and the band at
ages 25/50/75 must match the reported bootstrap CIs.

Run: python experiments/fig1_curve.py   (replays 1000 bootstrap fits; ~30 min)
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))

import exp4_protocol as e4

OUT_DIR = ROOT / 'paper' / 'figures'
NPZ = ROOT / 'results' / 'bootstrap_curve_params.npz'

# Reported execution values (results/exp4_protocol_output.txt) for verification:
REPORTED = dict(b0=-2.4230, b1=0.2794, b2=0.0933,
                ci25=(0.0460, 0.1181), ci50=(0.0497, 0.1042),
                ci75=(0.1472, 0.2677))


def replay_bootstrap(age, e, n, B=1000, seed=20261001):
    """Exact replay of e4.bootstrap's draw sequence, storing full params."""
    rng = np.random.default_rng(seed)
    grids = (e4.B0_B, e4.B1_B, e4.B2_B, e4.LK_B)
    params = []
    for b in range(B):
        idx = rng.integers(0, len(age), size=len(age))
        fit = e4.fit_model(age[idx], e[idx], n[idx], const=False,
                           grids=grids, starts=3)
        if fit is not None:
            params.append(fit.x)
        if (b + 1) % 100 == 0:
            print(f'  replay {b + 1}/{B}')
    return np.array(params)


def main():
    pids, age, e, n, _tr = e4.clean()

    fit = e4.fit_model(age, e, n, const=False, report_name='primary')
    b0, b1, b2, _lk = fit.x
    ok = (abs(b0 - REPORTED['b0']) < 1e-3 and abs(b1 - REPORTED['b1']) < 1e-3
          and abs(b2 - REPORTED['b2']) < 1e-3)
    print(f'primary refit: b0={b0:.4f} b1={b1:.4f} b2={b2:.4f} '
          f'-> matches reported: {ok}')
    if not ok:
        raise SystemExit('refit does not match reported execution values')

    if NPZ.exists():
        params = np.load(NPZ)['params']
        print(f'loaded cached bootstrap params ({len(params)})')
    else:
        params = replay_bootstrap(age, e, n)
        NPZ.parent.mkdir(exist_ok=True)
        np.savez_compressed(NPZ, params=params)
        print(f'saved {len(params)} resample parameter vectors -> {NPZ}')

    ages = np.arange(20, 86.01, 0.5)
    curves = np.array([e4.curve_alpha(ages, p[0], p[1], p[2]) for p in params])
    lo = np.percentile(curves, 2.5, axis=0)
    hi = np.percentile(curves, 97.5, axis=0)

    for a, (rlo, rhi) in ((25, REPORTED['ci25']), (50, REPORTED['ci50']),
                          (75, REPORTED['ci75'])):
        j = int(np.argmin(np.abs(ages - a)))
        print(f'band at {a}: [{lo[j]:.4f}, {hi[j]:.4f}] '
              f'(reported CI [{rlo:.4f}, {rhi:.4f}])')

    # observed decile points (exp3 construction: sorted by age, chunks of 26)
    order = np.argsort(age)
    xs, ys = [], []
    for s in range(0, len(order), 26):
        chunk = order[s:s + 26]
        if len(chunk) < 5:
            continue
        xs.append(float(age[chunk].mean()))
        ys.append(float(e[chunk].sum() / n[chunk].sum()))

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    BLUE = '#2A6F97'
    INK = '#333333'
    MUTED = '#8A8A8A'

    plt.rcParams.update({'font.size': 9, 'axes.linewidth': 0.8,
                         'xtick.color': INK, 'ytick.color': INK})
    fig, ax = plt.subplots(figsize=(5.0, 3.4))

    ax.fill_between(ages, lo, hi, color=BLUE, alpha=0.16, linewidth=0,
                    label='95% bootstrap band')
    curve = e4.curve_alpha(ages, b0, b1, b2)
    ax.plot(ages, curve, color=BLUE, linewidth=2.0,
            label=r'fitted $\alpha(\mathrm{age})$')
    ax.plot(xs, ys, 'o', markersize=5.5, markerfacecolor='white',
            markeredgecolor=INK, markeredgewidth=1.1,
            label='observed decile rates')

    ax.axvline(38.0, color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
    ax.annotate('age 38', xy=(38.8, 0.012), color=MUTED, fontsize=8)

    ax.set_xlabel('Age (years)', color=INK)
    ax.set_ylabel(r'Egocentric weight $\alpha$', color=INK)
    ax.set_xlim(19, 87)
    ax.set_ylim(0, 0.42)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', color='#DDDDDD', linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc='upper left', fontsize=8)

    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / 'curve.pdf')
    fig.savefig(OUT_DIR / 'curve.png', dpi=200)
    print(f'wrote {OUT_DIR / "curve.pdf"} and .png preview')


if __name__ == '__main__':
    main()

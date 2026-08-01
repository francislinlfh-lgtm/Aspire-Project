"""exp3 — robustness battery for the exploratory exp2 result (STUDY_1A.md).

Runs BEFORE any EF-mediation analysis and before the confirmatory freeze.
Sections:
  A. kappa grid extended below the old floor (down to 1) — does the slope CI move?
  B. Continuous age: decile table + posterior predictive checks by age band.
  C. Trial-split stability: 20 seeded random within-participant 6/6 splits
     (context for the single +9.85 parity split; NOT a generalization claim).
  D. Participant-level cross-validation: 5-fold x 10 repeats — the
     generalization-to-people test.
  E. Influence diagnostics: targeted leave-one-out (top-20 error counts + 5
     random) — max slope perturbation.
  F. IQ-exclusion sensitivity: cutoffs none / 70 / 75 / 80.

All alpha statements remain conditional on the response rule (matching); under
argmax+lapse every alpha reads as epsilon = 2*alpha (exact relabeling).
Run: python experiments/exp3_robustness.py   (several minutes; prints progress)
"""
import math
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))

import exp2_bradford_fit as e2

SEED = 20260803
KNEE = e2.KNEE

# fine grids (section A) — kappa extended well below the old floor of 4
A_FINE = [0.005 + 0.005 * i for i in range(100)]
S_FINE = [0.00025 * i for i in range(33)]
K_FINE = [1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 128, 256, 1024]

# coarse grids for repeated fits (sections C, D, E, F)
A_CO = [0.005 + 0.01 * i for i in range(50)]
S_CO = [0.0005 * i for i in range(17)]
K_CO = [1, 2, 4, 8, 16, 32, 64, 256]


def fit(stats, age_model, ag, sg, kg):
    slopes = sg if age_model else [0.0]
    best = (-1e18, None)
    for ay in ag:
        for s in slopes:
            for k in kg:
                ll = e2.loglik(stats, ay, s, k)
                if ll > best[0]:
                    best = (ll, (ay, s, k))
    return best


def section_a(stats):
    print('\n=== A. kappa grid extended (floor 4 -> 1) ===')
    ll0, (a0, _s, k0) = fit(stats, False, A_FINE, S_FINE, K_FINE)
    ll1, (ay, s1, k1) = fit(stats, True, A_FINE, S_FINE, K_FINE)
    print(f'flat: alpha={a0:.3f} kappa={k0}  logL={ll0:.2f}')
    print(f'age : alpha_young={ay:.3f} slope={s1:.5f} kappa={k1}  logL={ll1:.2f}')
    print(f'dAIC (age-flat): {(6 - 2 * ll1) - (4 - 2 * ll0):.2f}')
    lo, hi = None, None
    for s in S_FINE:
        ll = max(e2.loglik(stats, a, s, k) for a in A_FINE for k in K_FINE)
        if ll >= ll1 - 1.92:
            lo = s if lo is None else lo
            hi = s
    print(f'slope profile 95% CI with extended kappa: [{lo:.5f}, {hi:.5f}]')
    return ay, s1, k1


def section_b(P, ay, s1, k1):
    print('\n=== B. continuous age + posterior predictive checks ===')
    people = sorted(P.values(), key=lambda p: p['age'])
    dec = max(1, len(people) // 10)
    print('age-decile observed vs model-predicted egocentric rate:')
    for i in range(0, len(people), dec):
        chunk = people[i:i + dec]
        obs_e = sum(p['L'][0] for p in chunk)
        obs_n = sum(p['L'][1] for p in chunk)
        pred = sum(e2.alpha_of_age(p['age'], ay, s1) * p['L'][1]
                   for p in chunk) / obs_n
        ages = (chunk[0]['age'], chunk[-1]['age'])
        print(f'  ages {ages[0]:>2}-{ages[1]:>2}: obs {100 * obs_e / obs_n:5.2f}%'
              f'   pred {100 * pred:5.2f}%   (n={len(chunk)})')
    print('PPC — distribution of per-participant error counts, by age band:')
    for lo_a, hi_a in ((20, 37), (38, 59), (60, 86)):
        band = [p for p in people if lo_a <= p['age'] <= hi_a]
        obs = Counter(min(p['L'][0], 3) for p in band)
        pred = [0.0] * 4
        for p in band:
            mu = e2.alpha_of_age(p['age'], ay, s1)
            a, b = mu * k1, (1 - mu) * k1
            n = p['L'][1]
            for e in range(n + 1):
                lp = (e2.betabinom_logpmf(e, n, a, b)
                      + math.lgamma(n + 1) - math.lgamma(e + 1)
                      - math.lgamma(n - e + 1))
                pred[min(e, 3)] += math.exp(lp)
        print(f'  {lo_a}-{hi_a}: e-count 0/1/2/3+  obs '
              f'{[obs.get(i, 0) for i in range(4)]}  pred '
              f'{[round(x, 1) for x in pred]}')


def section_c(rows, P, rng):
    print('\n=== C. trial-split stability (20 random 6/6 splits) ===')
    per_trials = {}
    for r in rows:
        if r['Participant'] in P and r['CONDITION'] == 'Listener':
            per_trials.setdefault(r['Participant'], []).append(
                int(r['EgocentricErrors']))
    deltas = []
    for i in range(20):
        cal, hold = Counter(), Counter()
        for pid, es in per_trials.items():
            idx = list(range(len(es)))
            rng.shuffle(idx)
            half = len(idx) // 2
            age = P[pid]['age']
            ce = sum(es[j] for j in idx[:half])
            he = sum(es[j] for j in idx[half:])
            cal[(age, ce, half)] += 1
            hold[(age, he, len(idx) - half)] += 1
        _l0, (ca, _s, ck) = fit(cal, False, A_CO, S_CO, K_CO)
        _l1, (cay, cs, ck1) = fit(cal, True, A_CO, S_CO, K_CO)
        d = (e2.loglik(hold, cay, cs, ck1) - e2.loglik(hold, ca, 0.0, ck))
        deltas.append(d)
        if (i + 1) % 5 == 0:
            print(f'  ...{i + 1}/20 splits done')
    m = sum(deltas) / len(deltas)
    print(f'held-out delta (age - flat): mean {m:+.2f}, min {min(deltas):+.2f}, '
          f'max {max(deltas):+.2f}, positive in {sum(d > 0 for d in deltas)}/20')


def section_d(P, rng):
    print('\n=== D. participant-level cross-validation (5-fold x 10 repeats) ===')
    pids = sorted(P)
    totals, wins = [], 0
    for rep in range(10):
        order = pids[:]
        rng.shuffle(order)
        folds = [order[i::5] for i in range(5)]
        total = 0.0
        for f in folds:
            test = set(f)
            tr = Counter((P[p]['age'], P[p]['L'][0], P[p]['L'][1])
                         for p in pids if p not in test)
            te = Counter((P[p]['age'], P[p]['L'][0], P[p]['L'][1])
                         for p in test)
            _l0, (ca, _s, ck) = fit(tr, False, A_CO, S_CO, K_CO)
            _l1, (cay, cs, ck1) = fit(tr, True, A_CO, S_CO, K_CO)
            total += (e2.loglik(te, cay, cs, ck1) - e2.loglik(te, ca, 0.0, ck))
        totals.append(total)
        wins += total > 0
        print(f'  repeat {rep + 1}/10: held-out participants delta {total:+.2f}')
    m = sum(totals) / len(totals)
    print(f'generalization-to-people: mean delta {m:+.2f} '
          f'({m / len(pids):+.4f} per participant), age model wins {wins}/10 repeats')


def section_e(P):
    print('\n=== E. influence diagnostics (targeted leave-one-out) ===')
    stats_all = e2.suff(P)
    _ll, (ay, s_full, k) = fit(stats_all, True, A_CO, S_CO, K_CO)
    ranked = sorted(P, key=lambda p: -P[p]['L'][0])
    rng = random.Random(SEED + 5)
    candidates = ranked[:20] + rng.sample(ranked[20:], 5)
    worst = (0.0, None)
    for pid in candidates:
        sub = {q: P[q] for q in P if q != pid}
        _l, (_a, s_i, _k) = fit(e2.suff(sub), True, A_CO, S_CO, K_CO)
        d = abs(s_i - s_full)
        if d > worst[0]:
            worst = (d, pid)
    print(f'full-sample slope (coarse): {s_full:.5f}; max |slope change| from '
          f'removing any candidate: {worst[0]:.5f} (participant {worst[1]})')


def section_f(rows):
    print('\n=== F. IQ-exclusion sensitivity ===')
    demo = e2.load_demographics()
    for cutoff in (None, 70, 75, 80):
        e2.IQ_EXCLUSION = cutoff if cutoff is not None else -1
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            P = e2.build_participants(rows, demo)
        stats = e2.suff(P)
        _l1, (ay, s1, k1) = fit(stats, True, A_CO, S_CO, K_CO)
        print(f'  cutoff {str(cutoff):>4}: N={len(P):3d}  '
              f'alpha_young={ay:.3f}  slope={s1:.5f}  kappa={k1}')
    e2.IQ_EXCLUSION = 70


def main():
    print('exp3 robustness battery | seed', SEED)
    rows = e2.load_rows()
    P = e2.build_participants(rows, e2.load_demographics())
    stats = e2.suff(P)
    ay, s1, k1 = section_a(stats)
    section_b(P, ay, s1, k1)
    section_c(rows, P, random.Random(SEED))
    section_d(P, random.Random(SEED + 1))
    section_e(P)
    section_f(rows)
    print('\nDone. All alpha statements conditional on the response rule '
          '(epsilon = 2*alpha under argmax+lapse).')


if __name__ == '__main__':
    main()

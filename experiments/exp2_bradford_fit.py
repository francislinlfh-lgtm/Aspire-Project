"""exp2 — cleaning pipeline and first real fit: Bradford et al. (2023), OSF 2epsu.

*** EXPLORATORY ANALYSIS — not the pre-registered confirmatory fit. ***
Cleaning rules follow DATASET_NOTES.md; the model is P-MIX(alpha), the
choice-level projection of Heller et al. (2016) Eq. 2 (MODEL_AUDIT §1.3), with a
Beta-Binomial hierarchy over participants. All alpha conclusions are conditional
on the response rule (IDENTIFIABILITY: matching ≡ argmax+lapse at choice level).

Data files (gitignored, not redistributed): data/DirectorTask_RawBehaviouralData.csv
and data/DirectorTask_Demographics.csv from https://osf.io/2epsu/ (Bradford,
Brunsdon & Ferguson, 2023; open-data statement in the paper).

Run: python experiments/exp2_bradford_fit.py
"""
import csv
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'DirectorTask_RawBehaviouralData.csv'
DEMO = ROOT / 'data' / 'DirectorTask_Demographics.csv'

KNEE = 38
IQ_EXCLUSION = 70          # conventional 2-SD criterion; reconstruction attempt
ALPHA_GRID = [0.005 + 0.005 * i for i in range(100)]        # 0.005 .. 0.50
SLOPE_GRID = [0.00025 * i for i in range(33)]               # 0 .. 0.008
KAPPA_GRID = [4, 8, 16, 32, 64, 128, 256, 1024]


# ---------- loading and cleaning ----------

def load_rows():
    with open(RAW, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    n0 = len(rows)
    seen, deduped = set(), []
    for r in rows:
        key = tuple(sorted(r.items()))
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    print(f'rows: {n0} -> {len(deduped)} after exact-duplicate removal '
          f'({n0 - len(deduped)} removed; expected 48 from participants '
          f'28225/64185 per DATASET_NOTES)')
    return deduped


def load_demographics():
    with open(DEMO, encoding='utf-8-sig', newline='') as fh:
        return {r['PID']: r for r in csv.DictReader(fh)}


def build_participants(rows, demo):
    """-> dict pid -> {age, listener:(e, n), shared:(e, n)} with sample notes."""
    per = {}
    for r in rows:
        p = per.setdefault(r['Participant'], {'age': int(r['Age']),
                                              'L': [0, 0], 'S': [0, 0]})
        side = 'L' if r['CONDITION'] == 'Listener' else 'S'
        p[side][1] += 1
        p[side][0] += int(r['EgocentricErrors'])
    ids = set(per)
    dem_ids = set(demo)
    print(f'participants in behavioral data: {len(ids)}; in demographics: '
          f'{len(dem_ids)}; overlap: {len(ids & dem_ids)}')
    missing_dem = sorted(ids - dem_ids)
    if missing_dem:
        print(f'behavioral ids missing from demographics (excluded): {missing_dem}')
    low_iq = sorted(p for p in (ids & dem_ids)
                    if demo[p].get('FSIQ4', '').strip().isdigit()
                    and int(demo[p]['FSIQ4']) < IQ_EXCLUSION)
    print(f'FSIQ4 < {IQ_EXCLUSION} among overlap: {len(low_iq)} {low_iq}')
    keep = (ids & dem_ids) - set(low_iq)
    print(f'analysis sample: {len(keep)} (paper analyzed 264; deviations reported '
          f'as-is, not hidden)')
    return {p: per[p] for p in keep}


# ---------- descriptive anchors (DATASET_NOTES: reproduce before fitting) ----------

def descriptives(P):
    egos = [e / n for (e, n) in (p['L'] for p in P.values()) if n]
    mean_pct = 100 * sum(egos) / len(egos)
    pooled_e = sum(p['L'][0] for p in P.values())
    pooled_n = sum(p['L'][1] for p in P.values())
    shared_e = sum(p['S'][0] for p in P.values())
    print(f'\nmean per-participant egocentric rate (Listener): {mean_pct:.2f}% '
          f'(paper: 10.23%)')
    print(f'pooled: {pooled_e}/{pooled_n} = {100 * pooled_e / pooled_n:.2f}%')
    print(f'Shared-condition egocentric rows in sample: {shared_e} '
          f'(authors\' coding convention, kept)')
    n_counts = Counter(p['L'][1] for p in P.values())
    print(f'Listener trials per participant: {dict(sorted(n_counts.items()))}')
    print('\nage-band egocentric rates (pooled):')
    for lo, hi in ((20, 37), (38, 59), (60, 86)):
        es = sum(p['L'][0] for p in P.values() if lo <= p['age'] <= hi)
        ns = sum(p['L'][1] for p in P.values() if lo <= p['age'] <= hi)
        ppl = sum(1 for p in P.values() if lo <= p['age'] <= hi)
        if ns:
            print(f'  {lo}-{hi}: {100 * es / ns:5.2f}%  ({ppl} participants)')


# ---------- Beta-Binomial fitting ----------

def betabinom_logpmf(k, n, a, b):
    return (math.lgamma(k + a) + math.lgamma(n - k + b) - math.lgamma(n + a + b)
            - math.lgamma(a) - math.lgamma(b) + math.lgamma(a + b))


def alpha_of_age(age, alpha_young, slope):
    return min(0.95, alpha_young + slope * max(0, age - KNEE))


def loglik(stats, alpha_young, slope, kappa):
    """stats: Counter over (age, e, n)."""
    ll = 0.0
    for (age, e, n), cnt in stats.items():
        mu = alpha_of_age(age, alpha_young, slope)
        a, b = mu * kappa, (1 - mu) * kappa
        ll += cnt * betabinom_logpmf(e, n, a, b)
    return ll


def suff(P, which='L'):
    return Counter((p['age'], p[which][0], p[which][1]) for p in P.values()
                   if p[which][1] > 0)


def fit(stats, age_model):
    slopes = SLOPE_GRID if age_model else [0.0]
    best = (-1e18, None)
    for ay in ALPHA_GRID:
        for s in slopes:
            for k in KAPPA_GRID:
                ll = loglik(stats, ay, s, k)
                if ll > best[0]:
                    best = (ll, (ay, s, k))
    return best


def profile_ci_slope(stats, best_ll):
    lo, hi = None, None
    for s in SLOPE_GRID:
        ll = max(loglik(stats, ay, s, k)
                 for ay in ALPHA_GRID for k in KAPPA_GRID)
        if ll >= best_ll - 1.92:
            if lo is None:
                lo = s
            hi = s
    return lo, hi


def main():
    print('exp2 — Bradford et al. (2023) cleaning + first fit  '
          '[EXPLORATORY; alpha convention]')
    if not RAW.exists():
        sys.exit('data files missing — see module docstring for provenance')
    rows = load_rows()
    P = build_participants(rows, load_demographics())
    descriptives(P)

    stats = suff(P)
    ll0, (a0, _s0, k0) = fit(stats, age_model=False)
    ll1, (ay, s1, k1) = fit(stats, age_model=True)
    aic0, aic1 = 4 - 2 * ll0, 6 - 2 * ll1
    print(f'\nM0 flat:  alpha={a0:.3f} kappa={k0}  logL={ll0:.2f}  AIC={aic0:.2f}')
    print(f'M1 age :  alpha_young={ay:.3f} slope={s1:.5f}/yr kappa={k1}  '
          f'logL={ll1:.2f}  AIC={aic1:.2f}')
    print(f'dAIC (age - flat): {aic1 - aic0:.2f}  '
          f'({"age model preferred" if aic1 < aic0 - 2 else "no preference"})')
    lo, hi = profile_ci_slope(stats, ll1)
    print(f'slope profile 95% CI: [{lo:.5f}, {hi:.5f}] per year')
    print(f'fitted alpha(age): 20 -> {alpha_of_age(20, ay, s1):.3f} | '
          f'38 -> {alpha_of_age(38, ay, s1):.3f} | '
          f'60 -> {alpha_of_age(60, ay, s1):.3f} | '
          f'86 -> {alpha_of_age(86, ay, s1):.3f}')

    impossible = sum(1 for p in P.values() if 0 < p['L'][0] < p['L'][1])
    print(f'\nboundary models: P-EGO and P-CG each assign zero probability to '
          f'{impossible} of {len(P)} participants (intermediate error counts) — '
          f'both rejected outright, as expected (H-1A.3)')

    # held-out validation: within-participant parity split of Listener trials
    calib, hold = {}, {}
    for pid, p in P.items():
        pass  # placeholder replaced below by trial-level split
    # trial-level split needs raw rows:
    per_trials = {}
    for r in rows:
        if r['Participant'] in P and r['CONDITION'] == 'Listener':
            per_trials.setdefault(r['Participant'], []).append(
                (int(r['trial_number']), int(r['EgocentricErrors'])))
    calib_stats, hold_stats = Counter(), Counter()
    for pid, trials in per_trials.items():
        trials.sort()
        age = P[pid]['age']
        ce = sum(e for i, (_t, e) in enumerate(trials) if i % 2 == 0)
        cn = sum(1 for i in range(len(trials)) if i % 2 == 0)
        he = sum(e for i, (_t, e) in enumerate(trials) if i % 2 == 1)
        hn = len(trials) - cn
        calib_stats[(age, ce, cn)] += 1
        hold_stats[(age, he, hn)] += 1
    cll0, (ca0, _cs, ck0) = fit(calib_stats, age_model=False)
    cll1, (cay, cs1, ck1) = fit(calib_stats, age_model=True)
    h0 = loglik(hold_stats, ca0, 0.0, ck0)
    h1 = loglik(hold_stats, cay, cs1, ck1)
    print(f'\nheld-out (fit on odd-position trials, evaluate on even):')
    print(f'  flat model held-out logL: {h0:.2f}')
    print(f'  age  model held-out logL: {h1:.2f}  '
          f'(delta {h1 - h0:+.2f}; positive favors the age model out of sample)')

    print('\nCAVEATS: exploratory, not pre-registered; alpha conditional on the '
          'response rule; P-MIX is a choice-level projection of Heller Eq. 2; '
          'OtherError trials counted as non-egocentric (paper-consistent); '
          'knee fixed at 38; IQ exclusion reconstructed at FSIQ4<70.')


if __name__ == '__main__':
    main()

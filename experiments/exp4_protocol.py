"""exp4 — implementation of the Frozen Analysis Protocol (PREREGISTRATION.md,
frozen e09d306, amended a8de96b + Addendum 2). Section references in comments
map code to protocol clauses.

Modes:
  --synthetic   validation on synthetic data with KNOWN parameters (§4.4).
                Repeatable; touches no real data.
  --execute     THE single outcome-bearing execution on the real dataset (§14).
                Output reported whole, regardless of result.

Libraries (recorded per §4): numpy, scipy — versions printed at runtime.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, gammaln

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'DirectorTask_RawBehaviouralData.csv'
DEMO = ROOT / 'data' / 'DirectorTask_Demographics.csv'

# ---- §4 stage-1 grids (primary) ----
B0_G = np.arange(-5.0, -0.4 + 1e-9, 0.2)          # 24
B1_G = np.arange(-0.5, 1.0 + 1e-9, 0.1)           # 16
B2_G = np.arange(-0.5, 0.5 + 1e-9, 0.1)           # 11
LK_G = np.arange(-1.0, 11.0 + 1e-9, 0.5)          # 25
# ---- §8 bootstrap grid (Addendum 2 exact steps) ----
B0_B = np.arange(-5.0, -0.4 + 1e-9, 0.4)          # 12
B1_B = np.arange(-0.5, 1.0 + 1e-9, 0.2)           # 8
B2_B = np.arange(-0.5, 0.5 + 1e-9, 0.2)           # 6
LK_B = np.arange(-1.0, 11.0 + 1e-9, 1.0)          # 13
# ---- S1 grid (Addendum 2 exact steps) ----
B0_S1 = np.arange(-5.0, -0.4 + 1e-9, 0.1)
B1_S1 = np.arange(-0.5, 1.0 + 1e-9, 0.05)
B2_S1 = np.arange(-0.5, 0.5 + 1e-9, 0.05)
LK_S1 = np.arange(-1.0, 11.0 + 1e-9, 0.25)

BOUNDS = [(-7.0, 0.0), (-1.0, 1.5), (-1.0, 1.0), (-1.5, 11.5)]   # §4.2
BOUNDS_C = [(-7.0, 0.0), (-1.5, 11.5)]


def halt(msg):
    print('PROTOCOL HALT (§1.4):', msg)
    raise SystemExit(1)


# ---------------- §1 cleaning ----------------

def clean(iq_cutoff=70, expect=True):
    with open(RAW, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    seen, dedup, dup_pids = set(), [], set()
    for r in rows:
        key = tuple(sorted(r.items()))
        if key in seen:
            dup_pids.add(r['Participant'])
        else:
            seen.add(key)
            dedup.append(r)
    removed = len(rows) - len(dedup)
    if expect and (removed != 48 or dup_pids != {'28225', '64185'}):
        halt(f'duplicate expectation failed: removed={removed}, pids={dup_pids}')

    with open(DEMO, encoding='utf-8-sig', newline='') as fh:
        demo = {r['PID']: r for r in csv.DictReader(fh)}
    ids = {r['Participant'] for r in dedup}
    missing = ids - set(demo)
    low_iq = {p for p in ids & set(demo)
              if demo[p].get('FSIQ4', '').strip().isdigit()
              and int(demo[p]['FSIQ4']) < iq_cutoff}
    if expect and missing != {'30145'}:
        halt(f'missing-demographics expectation failed: {missing}')
    if expect and low_iq != {'24255'}:
        halt(f'low-IQ expectation failed: {low_iq}')
    keep = ids - missing - low_iq

    per = {}
    trial_rows = []
    for r in dedup:
        pid = r['Participant']
        if pid not in keep or r['CONDITION'] != 'Listener':
            continue
        p = per.setdefault(pid, {'age': int(r['Age']), 'e': 0, 'n': 0})
        p['e'] += int(r['EgocentricErrors'])
        p['n'] += 1
        trial_rows.append((pid, int(r['trial_number']), int(r['EgocentricErrors'])))
    if expect and len(per) != 264:
        halt(f'N expectation failed: {len(per)}')
    if expect and any(p['n'] != 12 for p in per.values()):
        halt('trials-per-participant expectation failed')
    pids = sorted(per)
    age = np.array([per[p]['age'] for p in pids])
    e = np.array([per[p]['e'] for p in pids])
    n = np.array([per[p]['n'] for p in pids])
    return pids, age, e, n, trial_rows


# ---------------- §3 model ----------------

def z_of(age):
    return (age - 53.0) / 10.0


def curve_alpha(age, b0, b1, b2):
    z = z_of(np.asarray(age, dtype=float))
    return expit(b0 + b1 * z + b2 * z * z)


def _bb_ll(mu, k, e, n):
    a = mu * k
    b = (1.0 - mu) * k
    return (gammaln(e + a) + gammaln(n - e + b) - gammaln(n + a + b)
            - gammaln(a) - gammaln(b) + gammaln(a + b))


def negll_primary(params, age, e, n):
    b0, b1, b2, lk = params
    mu = curve_alpha(age, b0, b1, b2)
    return -float(np.sum(_bb_ll(np.clip(mu, 1e-9, 1 - 1e-9), 2.0 ** lk, e, n)))


def negll_const(params, age, e, n):
    b0, lk = params
    mu = np.full(len(age), float(expit(b0)))
    return -float(np.sum(_bb_ll(mu, 2.0 ** lk, e, n)))


# ---------------- §4 estimator ----------------

def _grid_top(age, e, n, grids, const=False, top=5, chunk=8192):
    if const:
        combos = np.array(np.meshgrid(grids[0], grids[1],
                                      indexing='ij')).reshape(2, -1).T
    else:
        combos = np.array(np.meshgrid(*grids, indexing='ij')).reshape(4, -1).T
    z = z_of(age)
    best_ll = np.full(len(combos), -np.inf)
    for s in range(0, len(combos), chunk):
        c = combos[s:s + chunk]
        if const:
            mu = np.repeat(expit(c[:, 0])[:, None], len(age), axis=1)
            k = (2.0 ** c[:, 1])[:, None]
        else:
            mu = expit(c[:, 0][:, None] + c[:, 1][:, None] * z[None, :]
                       + c[:, 2][:, None] * z[None, :] ** 2)
            k = (2.0 ** c[:, 3])[:, None]
        ll = _bb_ll(np.clip(mu, 1e-9, 1 - 1e-9), k, e[None, :], n[None, :]).sum(axis=1)
        best_ll[s:s + chunk] = ll
    order = np.argsort(-best_ll)[:top]
    return [combos[i] for i in order]


def fit_model(age, e, n, const=False, grids=None, starts=5, report_name=None):
    """§4: coarse grid -> multi-start bounded Nelder-Mead; halt on bound/no-conv."""
    if grids is None:
        grids = (B0_G, LK_G) if const else (B0_G, B1_G, B2_G, LK_G)
    fun = negll_const if const else negll_primary
    bounds = BOUNDS_C if const else BOUNDS
    tops = _grid_top(age, e, n, grids, const=const, top=starts)
    best = None
    for x0 in tops:
        res = minimize(fun, x0, args=(age, e, n), method='Nelder-Mead',
                       bounds=bounds,
                       options={'fatol': 1e-6, 'xatol': 1e-8, 'maxfev': 5000})
        if res.success and (best is None or res.fun < best.fun):
            best = res
    if best is None:
        if report_name:
            halt(f'no Nelder-Mead start converged ({report_name})')
        return None
    for v, (lo, hi) in zip(best.x, bounds):
        if abs(v - lo) < 1e-6 or abs(v - hi) < 1e-6:
            if report_name:
                halt(f'estimate on box bound ({report_name}): {best.x}')
            return None
    return best  # .x params, .fun = -logL


def d_alpha(params):
    """§2 primary estimand."""
    b0, b1, b2 = params[0], params[1], params[2]
    return float(curve_alpha(75, b0, b1, b2) - curve_alpha(25, b0, b1, b2))


# ---------------- §6 CV ----------------

BANDS = [(20, 44), (45, 64), (65, 86)]     # fixed, §6


def cv(age, e, n, repeats=20, folds=5, seed0=20260901, grids=None):
    N = len(age)
    per_part = np.zeros(N)
    deltas = []
    for r in range(1, repeats + 1):
        rng = np.random.default_rng(seed0 + r)
        fold_of = np.full(N, -1)
        for lo, hi in BANDS:
            idx = np.where((age >= lo) & (age <= hi))[0]
            idx = rng.permutation(idx)
            for j, i in enumerate(idx):
                fold_of[i] = j % folds
        d_r = 0.0
        for f in range(folds):
            te = fold_of == f
            tr = ~te
            fa = fit_model(age[tr], e[tr], n[tr], const=False, grids=grids)
            fc = fit_model(age[tr], e[tr], n[tr], const=True)
            if fa is None or fc is None:
                print(f'  CV repeat {r} fold {f}: fit failure (recorded)')
                continue
            mu_a = np.clip(curve_alpha(age[te], *fa.x[:3]), 1e-9, 1 - 1e-9)
            mu_c = np.full(te.sum(), float(expit(fc.x[0])))
            ll_a = _bb_ll(mu_a, 2.0 ** fa.x[3], e[te], n[te])
            ll_c = _bb_ll(mu_c, 2.0 ** fc.x[1], e[te], n[te])
            d_r += float(np.sum(ll_a - ll_c))
            per_part[te] += ll_a - ll_c
        deltas.append(d_r)
        print(f'  CV repeat {r}/{repeats}: delta {d_r:+.2f}')
    per_part /= repeats
    return np.array(deltas), per_part


# ---------------- §8 bootstrap ----------------

def bootstrap(age, e, n, B=1000, seed=20261001):
    rng = np.random.default_rng(seed)
    grids = (B0_B, B1_B, B2_B, LK_B)
    out, curves, fails = [], [], 0
    target, b_done = B, 0
    while b_done < target:
        idx = rng.integers(0, len(age), size=len(age))
        fit = fit_model(age[idx], e[idx], n[idx], const=False,
                        grids=grids, starts=3)
        b_done += 1
        if fit is None:
            fails += 1
            if fails > target - 950 and target < 2000:
                target += 100     # §8 extension rule
            continue
        out.append(d_alpha(fit.x))
        curves.append([float(curve_alpha(a, *fit.x[:3])) for a in (25, 50, 75)])
        if b_done % 100 == 0:
            print(f'  bootstrap {b_done}/{target} (failures {fails})')
    return np.array(out), np.array(curves), fails, b_done


# ---------------- §10 parametric predictive checks ----------------

def ppc(age, e, n, params, sims=1000, seed=20261101):
    b0, b1, b2, lk = params
    k = 2.0 ** lk
    rng = np.random.default_rng(seed)
    mu = np.clip(curve_alpha(age, b0, b1, b2), 1e-9, 1 - 1e-9)
    old = (age >= 73) & (age <= 86)
    young = (age >= 20) & (age <= 37)
    t1s, t2s = [], []
    for _ in range(sims):
        ai = rng.beta(mu * k, (1 - mu) * k)
        es = rng.binomial(n, ai)
        t1s.append(es[old].sum() / n[old].sum())
        t2s.append(int(np.sum(es[young] == 1)))
    t1_obs = e[old].sum() / n[old].sum()
    t2_obs = int(np.sum(e[young] == 1))
    return (t1_obs, np.percentile(t1s, [2.5, 97.5]), np.percentile(t1s, [0.5, 99.5]),
            t2_obs, np.percentile(t2s, [2.5, 97.5]), np.percentile(t2s, [0.5, 99.5]))


# ---------------- S3 shapes ----------------

def negll_knee(params, age, e, n, knee):
    g0, g1, lk = params
    mu = np.clip(expit(g0 + g1 * np.maximum(0, age - knee)), 1e-9, 1 - 1e-9)
    return -float(np.sum(_bb_ll(mu, 2.0 ** lk, e, n)))


def fit_knee(age, e, n, knee):
    G0 = np.arange(-5.0, -0.4 + 1e-9, 0.2)
    G1 = np.arange(-0.05, 0.15 + 1e-9, 0.005)
    combos = np.array(np.meshgrid(G0, G1, LK_G, indexing='ij')).reshape(3, -1).T
    lls = np.array([-negll_knee(c, age, e, n, knee) for c in combos])
    x0 = combos[int(np.argmax(lls))]
    res = minimize(negll_knee, x0, args=(age, e, n, knee), method='Nelder-Mead',
                   options={'fatol': 1e-6, 'maxfev': 4000})
    return -res.fun if res.success else float(lls.max())


# ---------------- reporting helpers (§7.1, §12) ----------------

def curve_report(params):
    b0, b1, b2 = params[0], params[1], params[2]
    a25, a50, a75 = (float(curve_alpha(a, b0, b1, b2)) for a in (25, 50, 75))
    print(f'alpha(25)={a25:.4f} (eps={2 * a25:.4f})  '
          f'alpha(50)={a50:.4f} (eps={2 * a50:.4f})  '
          f'alpha(75)={a75:.4f} (eps={2 * a75:.4f})')
    print('curve (5-year steps):', ' '.join(
        f'{a}:{float(curve_alpha(a, b0, b1, b2)):.3f}' for a in range(20, 87, 5)))
    mono_full = mono_2575 = True
    tp = None
    if abs(b2) > 1e-12:
        zt = -b1 / (2 * b2)
        at = 53 + 10 * zt
        if 20 <= at <= 86:
            tp = at
            mono_full = False
        if 25 <= at <= 75:
            mono_2575 = False
    print(f'turning point: {"none in [20,86]" if tp is None else f"age {tp:.1f}"}; '
          f'monotonic over [20,86]: {mono_full}; over [25,75]: {mono_2575}')
    return mono_2575


# ---------------- synthetic validation (§4.4) ----------------

def synthetic():
    print('=== SYNTHETIC VALIDATION (no real data touched) ===')
    ok = True
    rng = np.random.default_rng(12345)
    N = 264
    age = rng.integers(20, 87, size=N)
    n = np.full(N, 12)
    true = np.array([-2.7, 0.35, 0.05, np.log2(1.5)])
    mu = curve_alpha(age, *true[:3])
    k = 2.0 ** true[3]
    e = rng.binomial(n, rng.beta(mu * k, (1 - mu) * k))
    fit = fit_model(age, e, n, const=False, report_name=None)
    if fit is None:
        print('FAIL: primary fit did not converge on synthetic data')
        return False
    da_t, da_e = d_alpha(true), d_alpha(fit.x)
    print(f'recovery: true dAlpha={da_t:.4f}, est={da_e:.4f}, '
          f'|err|={abs(da_t - da_e):.4f} (tolerance 0.05)')
    ok &= abs(da_t - da_e) < 0.05

    null_e = rng.binomial(n, rng.beta(0.10 * 8, 0.90 * 8, size=N))
    fa = fit_model(age, null_e, n, const=False)
    fc = fit_model(age, null_e, n, const=True)
    daic = (8 + 2 * fa.fun) - (4 + 2 * fc.fun)
    print(f'null data: dAIC(age-const)={daic:+.2f} (should not strongly favor age)')
    ok &= daic > -6

    try:
        fit_model(age, np.zeros(N, dtype=int), n, const=False,
                  report_name='degenerate-test')
        print('FAIL: degenerate all-zero data did not halt')
        ok = False
    except SystemExit:
        print('degenerate all-zero data halts as specified: OK')

    print('CV machinery smoke (2 repeats, bootstrap grids):')
    d, pp = cv(age, e, n, repeats=2, grids=(B0_B, B1_B, B2_B, LK_B))
    print(f'  smoke deltas: {np.round(d, 2)}')
    bs, cur, fails, done = bootstrap(age, e, n, B=20)
    print(f'bootstrap smoke: {len(bs)}/20 successes, {fails} failures')
    ok &= len(bs) >= 15
    r = ppc(age, e, n, fit.x, sims=50)
    print(f'PPC smoke: T1 obs {r[0]:.3f} in 95% {np.round(r[1], 3)}; '
          f'T2 obs {r[3]} in 95% {np.round(r[4], 1)}')

    print('cleaning-logic fixture test:')
    ok &= _cleaning_fixture_test()
    print('SYNTHETIC VALIDATION:', 'PASS' if ok else 'FAIL')
    return ok


def _cleaning_fixture_test():
    """Verify dedupe/exclusion logic on a constructed fixture (no real data)."""
    rows = []
    for pid, iq_ok in (('1', True), ('2', True), ('3', True)):
        for t in range(1, 13):
            rows.append({'Participant': pid, 'Age': '30', 'trial_number': str(t),
                         'CONDITION': 'Listener', 'EgocentricErrors': '0'})
    rows += rows[0:12]                       # exact duplicate block for pid 1
    seen, dedup, dups = set(), [], set()
    for r in rows:
        key = tuple(sorted(r.items()))
        if key in seen:
            dups.add(r['Participant'])
        else:
            seen.add(key)
            dedup.append(r)
    good = (len(rows) - len(dedup) == 12) and dups == {'1'}
    demo = {'1': {'FSIQ4': '100'}, '2': {'FSIQ4': '65'}}   # 3 missing, 2 low-IQ
    ids = {r['Participant'] for r in dedup}
    missing = ids - set(demo)
    low = {p for p in ids & set(demo) if int(demo[p]['FSIQ4']) < 70}
    good &= missing == {'3'} and low == {'2'}
    print('  dedupe + exclusion fixture:', 'OK' if good else 'FAIL')
    return good


# ---------------- §14 the single execution ----------------

def execute():
    import scipy
    print('=== PROTOCOL EXECUTION (single outcome-bearing run; PREREGISTRATION.md) ===')
    print(f'numpy {np.__version__} | scipy {scipy.__version__}')
    if not RAW.exists() or not DEMO.exists():
        halt('data files missing')

    print('\n--- §1 cleaning ---')
    pids, age, e, n, trials = clean()
    print(f'N={len(pids)}; Listener trials={int(n.sum())}; '
          f'pooled ego rate={e.sum() / n.sum():.4f}')

    print('\n--- §4 primary and comparator fits ---')
    fa = fit_model(age, e, n, const=False, report_name='primary')
    fc = fit_model(age, e, n, const=True, report_name='constant')
    ll_a, ll_c = -fa.fun, -fc.fun
    b0, b1, b2, lk = fa.x
    print(f'primary: b0={b0:.4f} b1={b1:.4f} b2={b2:.4f} kappa={2**lk:.3f} '
          f'logL={ll_a:.3f}')
    print(f'constant: alpha0={float(expit(fc.x[0])):.4f} '
          f'(eps={2 * float(expit(fc.x[0])):.4f}) kappa={2**fc.x[1]:.3f} '
          f'logL={ll_c:.3f}')

    print('\n--- §5 AIC ---')
    aic_a, aic_c = 8 - 2 * ll_a, 4 - 2 * ll_c
    daic = aic_a - aic_c
    r1 = daic <= -2
    print(f'AIC primary={aic_a:.2f} constant={aic_c:.2f} dAIC={daic:+.2f} '
          f'-> R1 {"met" if r1 else "NOT met"}')

    print('\n--- §2/§7.1 estimand and curve ---')
    da = d_alpha(fa.x)
    print(f'dAlpha = alpha(75)-alpha(25) = {da:+.4f} ({da / 50:+.5f}/yr)')
    mono_2575 = curve_report(fa.x)

    print('\n--- §6/§7 participant-level CV ---')
    deltas, per_part = cv(age, e, n)
    pos = int(np.sum(deltas > 0))
    r2 = pos >= 17
    print(f'positive repeats: {pos}/20 -> R2 (descriptive stability rule) '
          f'{"met" if r2 else "NOT met"}')
    print(f'delta mean={deltas.mean():+.2f} median={np.median(deltas):+.2f} '
          f'range=[{deltas.min():+.2f}, {deltas.max():+.2f}]')
    print(f'per-participant mean out-of-fold delta: '
          f'{np.mean(per_part):+.4f}; fraction positive '
          f'{np.mean(per_part > 0):.3f} (descriptive only; no p-value — '
          f'repeats are correlated)')
    print('scope: unseen participants on the SAME task and item set only')

    print('\n--- §8 bootstrap (B=1000) ---')
    bs, curves, fails, done = bootstrap(age, e, n)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    print(f'dAlpha 95% percentile CI [{lo:+.4f}, {hi:+.4f}] '
          f'({len(bs)} successes, {fails} failures, {done} draws)')
    for j, a in enumerate((25, 50, 75)):
        clo, chi = np.percentile(curves[:, j], [2.5, 97.5])
        print(f'alpha({a}) 95% CI [{clo:.4f}, {chi:.4f}]')

    print('\n--- §10 parametric predictive checks ---')
    t1o, t1_95, t1_99, t2o, t2_95, t2_99 = ppc(age, e, n, fa.x)
    print(f'T1 (pooled ego rate 73-86): obs {t1o:.4f}; 95% '
          f'[{t1_95[0]:.4f}, {t1_95[1]:.4f}]; 99% [{t1_99[0]:.4f}, {t1_99[1]:.4f}]')
    print(f'T2 (# with exactly 1 error, 20-37): obs {t2o}; 95% '
          f'[{t2_95[0]:.0f}, {t2_95[1]:.0f}]; 99% [{t2_99[0]:.0f}, {t2_99[1]:.0f}]')

    print('\n--- §9 sensitivities ---')
    s1 = fit_model(age, e, n, const=False, grids=(B0_S1, B1_S1, B2_S1, LK_S1))
    print(f'S1 (fine grid): dAlpha={d_alpha(s1.x):+.4f}' if s1 is not None
          else 'S1: fit failure (recorded)')
    for cut, exp_n in ((None, 265), (70, 264), (75, 264), (80, 263)):
        p2, a2, e2, n2, _t = clean(iq_cutoff=(cut if cut else -1), expect=False)
        f2 = fit_model(a2, e2, n2, const=False)
        note = '' if len(p2) == exp_n else f' (expected N={exp_n}!)'
        print(f'S2 cutoff {str(cut):>4}: N={len(p2)}{note} '
              f'dAlpha={d_alpha(f2.x):+.4f}' if f2 is not None else
              f'S2 cutoff {cut}: fit failure')
    print('S3 knee profile (knee 20..86):')
    lls = {kn: fit_knee(age, e, n, kn) for kn in range(20, 87)}
    best_k = max(lls, key=lls.get)
    inside = [kn for kn, v in lls.items() if v >= lls[best_k] - 1.92]
    span = max(inside) - min(inside)
    ident = span < 20
    print(f'  best knee {best_k}, 95% profile [{min(inside)}, {max(inside)}] '
          f'span {span} yr -> {"reported" if ident else "UNIDENTIFIED (span >= 20 yr)"}')
    print('S4 leave-one-participant-out (264 refits):')
    das = []
    for i in range(len(pids)):
        m = np.ones(len(pids), bool)
        m[i] = False
        f_i = fit_model(age[m], e[m], n[m], const=False, starts=1)
        if f_i is not None:
            das.append(d_alpha(f_i.x))
        if (i + 1) % 50 == 0:
            print(f'  ...{i + 1}/264')
    das = np.array(das)
    mx = float(np.max(np.abs(das - da)))
    print(f'  max |change in dAlpha| = {mx:.4f} '
          f'({"FLAG >20% of estimate" if mx > 0.2 * abs(da) else "below 20% flag"})')
    print('S6 per-trial-position Listener ego rates:')
    pos_e = Counter()
    pos_n = Counter()
    for _pid, t, err in trials:
        pos_e[t] += err
        pos_n[t] += 1
    print('  ', {t: f'{pos_e[t] / pos_n[t]:.3f}' for t in sorted(pos_n)})
    das6 = []
    for t_out in sorted(pos_n):
        agg = {}
        for pid, t, err in trials:
            if t != t_out:
                agg.setdefault(pid, [0, 0])
                agg[pid][0] += err
                agg[pid][1] += 1
        a6 = np.array([per_age for per_age in age])
        e6 = np.array([agg[p][0] for p in pids])
        n6 = np.array([agg[p][1] for p in pids])
        f6 = fit_model(a6, e6, n6, const=False, starts=1,
                       grids=(B0_B, B1_B, B2_B, LK_B))
        if f6 is not None:
            das6.append(d_alpha(f6.x))
    mx6 = float(np.max(np.abs(np.array(das6) - da))) if das6 else float('nan')
    print(f'  leave-one-position-out: max |change in dAlpha| = {mx6:.4f} '
          f'(caveat: trial_number may conflate item and position)')

    print('\n--- §7/§12 outcome ---')
    if r1 and r2:
        cat = 'Meets prespecified robustness criteria'
    elif r1 or r2:
        cat = 'Mixed robustness evidence'
    else:
        cat = 'Does not meet prespecified robustness criteria'
    direction = ('increased' if (da > 0 and mono_2575) else
                 'followed the fitted shape')
    print(f'OUTCOME CATEGORY: {cat}')
    print(f'HEADLINE (§12 template): Under P-MIX and its response assumptions, '
          f'the estimated egocentric contribution {direction} with age '
          f'(dAlpha = {da:+.4f}, 95% bootstrap CI [{lo:+.4f}, {hi:+.4f}]; '
          f'eps-dual: {2 * da:+.4f} [{2 * lo:+.4f}, {2 * hi:+.4f}]), and the '
          f'age-dependent model {"met" if (r1 and r2) else ("partially met" if (r1 or r2) else "did not meet")} '
          f'the prespecified robustness criteria against the fitted constant-alpha '
          f'model ({pos}/20 CV repeats).')
    print('\nAll alpha values conditional on the probability-matching response '
          'rule; eps = 2*alpha under argmax+lapse. Scope: this task and item set.')


if __name__ == '__main__':
    if '--synthetic' in sys.argv:
        sys.exit(0 if synthetic() else 1)
    elif '--execute' in sys.argv:
        execute()
    else:
        print('usage: exp4_protocol.py --synthetic | --execute')

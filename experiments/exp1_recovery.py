"""exp1 — parameter recovery for Study 1A (Step 1; STUDY_1A.md).

Question: with the Bradford et al. (2023) dataset's exact structure — ~264
participants, 12 Listener (critical) trials each, ages 20-86 — can the mixture
weight `w` be recovered from choice data at all, and at which levels?

  A. Grand-mean w (pooled).
  B. An age-varying w(age) of the published effect's approximate size
     (plateau to ~age 38, then decline; Bradford et al., 2023), including the
     false-positive rate when no age effect exists.
  C. Individual-level w_i under hierarchical (Beta-Binomial) shrinkage —
     how much do 12 trials actually say about one person?
  D. The response-rule confound: probability matching vs argmax+lapse.

Generative model (synthetic truth): q_i = 1 - w_i is a participant's egocentric
choice probability on critical trials; w_i ~ Beta with mean w(age_i) and
concentration KAPPA (individual heterogeneity); e_i ~ Binomial(12, q_i).
Control/Shared trials carry no information about w under the model and are not
simulated. OtherError outcomes (~1% of real trials) are omitted here — a policy
for them is a real-data-fitting decision recorded in DATASET_NOTES.md.

Fitting is exact-likelihood Beta-Binomial via sufficient statistics; stdlib only;
deterministic per seed. Run:  python experiments/exp1_recovery.py [--fast]
"""
import math
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

FAST = '--fast' in sys.argv

N_PARTICIPANTS = 264
N_TRIALS = 12
AGE_LO, AGE_HI = 20, 86
KNEE = 38                 # plateau/decline knee fixed at the published value
KAPPA_TRUE = 50.0         # individual heterogeneity (unknown in reality; a guess)
REPS = 3 if FAST else 100
SEED = 20260801

# True age curves for w (calibrated to Bradford et al. 2023: ~10% grand egocentric
# rate; plateau 20-37, decline 38+; q(young)~0.07 rising to q(86)~0.20):
W_PLATEAU_TRUE = 0.93
SLOPE_TRUE = 0.13 / (AGE_HI - KNEE)     # ~0.00271 per year
W_FLAT_TRUE = 0.90                       # null-scenario constant w (grand ~10%)


def w_of_age(age, w_plateau, slope):
    return max(0.5, w_plateau - slope * max(0, age - KNEE))


def generate(rng, w_plateau, slope, kappa=KAPPA_TRUE):
    """One synthetic dataset: list of (age, e_i egocentric count)."""
    out = []
    for _ in range(N_PARTICIPANTS):
        age = rng.randint(AGE_LO, AGE_HI)
        mu = w_of_age(age, w_plateau, slope)
        a, b = mu * kappa, (1 - mu) * kappa
        w_i = rng.betavariate(a, b)
        q_i = 1 - w_i
        e_i = sum(1 for _ in range(N_TRIALS) if rng.random() < q_i)
        out.append((age, e_i))
    return out


def betabinom_logpmf(k, n, a, b):
    """log P(k | n, Beta(a,b)) — the choose(n,k) constant is model-independent
    and omitted (cancels in all comparisons)."""
    return (math.lgamma(k + a) + math.lgamma(n - k + b) - math.lgamma(n + a + b)
            - math.lgamma(a) - math.lgamma(b) + math.lgamma(a + b))


def loglik(data_counts, w_plateau, slope, kappa):
    """Exact log-likelihood via sufficient statistics: counts over (age, e)."""
    ll = 0.0
    for (age, e), n in data_counts.items():
        mu_q = 1 - w_of_age(age, w_plateau, slope)   # mean egocentric prob
        a, b = mu_q * kappa, (1 - mu_q) * kappa
        ll += n * betabinom_logpmf(e, N_TRIALS, a, b)
    return ll


KAPPA_GRID = [4, 8, 16, 32, 64, 128, 256, 1024]
W_GRID = [0.60 + 0.005 * i for i in range(79)]              # 0.60 .. 0.99
SLOPE_GRID = [0.0005 * i for i in range(13)]                # 0 .. 0.006


def fit_flat(data):
    counts = Counter(data)
    best = (-1e18, None)
    for w0 in W_GRID:
        for k in KAPPA_GRID:
            ll = loglik(counts, w0, 0.0, k)
            if ll > best[0]:
                best = (ll, (w0, k))
    return best  # (ll, (w0, kappa)); 2 free parameters


def fit_age(data):
    counts = Counter(data)
    best = (-1e18, None)
    for wp in W_GRID:
        for s in SLOPE_GRID:
            for k in KAPPA_GRID:
                ll = loglik(counts, wp, s, k)
                if ll > best[0]:
                    best = (ll, (wp, s, k))
    return best  # 3 free parameters


def aic(ll, k_params):
    return 2 * k_params - 2 * ll


def mean_sd(xs):
    m = sum(xs) / len(xs)
    v = sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1)
    return m, math.sqrt(v)


def engine_validation(rng):
    """Generate one participant-block with the actual engine and confirm the
    analytic shortcut P(ego)=1-w matches the implementation."""
    from cogsim.world import critical_display
    from cogsim.language import scripted_instruction, privileged_competitor
    from cogsim.listener import MixtureListener
    w = 0.85
    listener = MixtureListener(w)
    d = critical_display()
    instr = scripted_instruction(d)
    priv = privileged_competitor(d, instr.frame)
    n = 4000
    ego = sum(1 for _ in range(n)
              if listener.interpret(d, instr.frame).sample(rng) == priv)
    rate, expect = ego / n, 1 - w
    se = math.sqrt(expect * (1 - expect) / n)
    ok = abs(rate - expect) < 4 * se
    print(f'engine check: P(ego) engine={rate:.4f} analytic={expect:.4f} '
          f'(4*SE={4*se:.4f}) -> {"OK" if ok else "MISMATCH"}')
    if not ok:
        raise SystemExit('engine and analytic generative model disagree')


def study_a(rng):
    print('\n=== A. Grand-mean w recovery (flat truth, flat fit) ===')
    for w_true in (0.80, 0.90, 0.95):
        est = []
        for _ in range(REPS):
            data = generate(rng, w_true, 0.0)
            _, (w0, _k) = fit_flat(data)
            est.append(w0)
        m, sd = mean_sd(est)
        print(f'true w={w_true:.2f}: recovered {m:.3f} +/- {sd:.3f} '
              f'(bias {m - w_true:+.3f})  [{REPS} reps]')


def study_b(rng):
    print('\n=== B. Age-effect detection and recovery ===')
    hits = 0
    slopes, kappas = [], []
    for _ in range(REPS):
        data = generate(rng, W_PLATEAU_TRUE, SLOPE_TRUE)
        ll_f, _ = fit_flat(data)
        ll_a, (wp, s, k) = fit_age(data)
        if aic(ll_a, 3) < aic(ll_f, 2) - 2:
            hits += 1
        slopes.append(s)
        kappas.append(k)
    ms, sds = mean_sd(slopes)
    print(f'truth: plateau {W_PLATEAU_TRUE}, slope {SLOPE_TRUE:.5f}/yr, knee {KNEE}')
    print(f'power (age model preferred, dAIC<-2): {hits}/{REPS}')
    print(f'slope recovered: {ms:.5f} +/- {sds:.5f}')
    print(f'kappa estimates (true {KAPPA_TRUE:.0f}): {sorted(Counter(kappas).items())}')

    false_pos = 0
    for _ in range(REPS):
        data = generate(rng, W_FLAT_TRUE, 0.0)
        ll_f, _ = fit_flat(data)
        ll_a, _ = fit_age(data)
        if aic(ll_a, 3) < aic(ll_f, 2) - 2:
            false_pos += 1
    print(f'false-positive rate (flat truth): {false_pos}/{REPS}')


def study_c(rng):
    print('\n=== C. Individual-level w_i under shrinkage (one dataset) ===')
    data = generate(rng, W_PLATEAU_TRUE, SLOPE_TRUE)
    _, (wp, s, k) = fit_age(data)
    post_sds, no_pool = [], []
    for age, e in data:
        mu_q = 1 - w_of_age(age, wp, s)
        a, b = mu_q * k + e, (1 - mu_q) * k + N_TRIALS - e
        post_sds.append(math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1))))
        p = max(e, 0.5) / N_TRIALS
        no_pool.append(math.sqrt(p * (1 - p) / N_TRIALS))
    mp, _ = mean_sd(post_sds)
    mn, _ = mean_sd(no_pool)
    print(f'mean posterior SD of individual q_i (shrunk):   {mp:.3f}')
    print(f'mean no-pooling SE of individual q_i (12 trials): {mn:.3f}')
    print('reading: with 12 trials, individual estimates are prior-dominated -> '
          'individual-difference claims (age, EF) must enter through the '
          'hierarchy, never through per-person point estimates.')


def study_d():
    print('\n=== D. Response-rule confound (exact result, no simulation) ===')
    print('Under probability matching, P(ego)=1-w_i. Under argmax+lapse with '
          'lapse eps_i (uniform over the two candidates), P(ego)=eps_i/2. '
          'The mapping eps=2(1-w) makes the likelihoods IDENTICAL for every '
          'dataset — at the choice level the rules are a relabeling, so all '
          'w conclusions from choice data alone are conditional on the rule. '
          'What breaks the tie: the eye-tracking file (posterior-mass linking '
          'predicts graded competitor consideration; lapse predicts none).')
    rng = random.Random(1)
    data = generate(rng, W_PLATEAU_TRUE, SLOPE_TRUE)
    counts = Counter(data)
    ll_match = loglik(counts, 0.90, 0.001, 32)
    # identical model with q reparameterized as eps/2 — same numbers by def.
    print(f'spot check: logL(matching params) = {ll_match:.3f} '
          '== logL(mapped lapse params) by construction.')


def main():
    print(f'exp1 parameter recovery | N={N_PARTICIPANTS} x {N_TRIALS} critical '
          f'trials | ages {AGE_LO}-{AGE_HI} | kappa_true={KAPPA_TRUE:.0f} | '
          f'reps={REPS} | seed={SEED}{" | FAST" if FAST else ""}')
    rng = random.Random(SEED)
    engine_validation(rng)
    study_a(rng)
    study_b(rng)
    study_c(rng)
    study_d()
    print('\nCaveats: knee fixed at 38 (not estimated); ages uniform (real sample '
          'is not); OtherError category omitted; all conclusions conditional on '
          'the response rule per study D.')


if __name__ == '__main__':
    main()

# Pre-registration — Study 1A confirmatory analysis

**Status: FROZEN upon commit. The freeze is the git commit containing this file;
any later change is a dated addendum in §15, never an in-place edit.**

**Disclosure of prior exploration.** This plan was written *after* exploratory
analyses of the same dataset (exp2, exp3; results in STUDY_1A.md). Its confirmatory
value therefore rests on (a) decisions frozen before the outcome-bearing rerun,
(b) held-out-participant prediction as the primary evidence, and (c) verbatim
reporting of every pre-specified outcome, favorable or not. This is a
preregistration-following-exploration and will be described as such in any writeup.

Data: Bradford, Brunsdon & Ferguson (2023), OSF 2epsu (see DATASET_NOTES.md).
Model family: P-MIX(α), the choice-level projection of Heller et al. (2016) Eq. 2,
with a Beta-Binomial participant hierarchy. All α statements are conditional on the
probability-matching response rule; every reported α has the exact dual reading
ε = 2α under argmax+lapse, and reports state both (§12).

## 1. Sample and cleaning (locked)

1. Remove byte-identical duplicate rows (expected: 48 rows, participants 28225,
   64185).
2. Exclude participants absent from `DirectorTask_Demographics.csv` (expected: id
   30145) and participants with FSIQ4 < 70 (expected: id 24255). Expected N = 264.
3. Model **Listener-condition trials only** (expected 12/participant). Outcome per
   trial: `EgocentricErrors` exactly as coded by the authors. OtherError trials
   count as non-egocentric trials (denominator retained). Shared-condition trials
   are manipulation checks only, never modeled.
4. If any expectation above fails on rerun, the run halts and the discrepancy is
   reported before proceeding (no silent adaptation).

## 2. Primary estimand (locked)

**Δα = α(75) − α(25)** under the primary model: the model-implied change in the
egocentric weight between ages 25 and 75 (probability units). Secondary summary:
Δα / 50 as average per-year change. Ages in years; no rescaling of the estimand.

## 3. Primary model (locked — one model, not a menu)

Logit-quadratic age curve with Beta-Binomial heterogeneity:

- `α(age) = logistic(β0 + β1·z + β2·z²)`, with `z = (age − 53) / 10`
  (decades, centered at the fixed constant 53 — not at any sample statistic).
- Participant weights: `α_i ~ Beta(α(age_i)·κ, (1 − α(age_i))·κ)`;
  `e_i ~ Binomial(n_i, α_i)`, exact Beta-Binomial marginal likelihood (binomial
  coefficient omitted identically in all models — it cancels in every comparison).

Rationale (recorded, since the shape choice follows exploration): the exploratory
PPC showed knee-linear misfit at both age extremes, and the source paper's own
best-fitting accuracy curve was quadratic; the logit link keeps α in (0,1).

**Comparator (locked):** constant-α Beta-Binomial (parameters α0, κ) — described
in all text as "the fitted constant-α model," never "any constant-weight account."

## 4. Estimation (locked)

Maximum likelihood by deterministic two-stage grid:

- Stage 1: β0 ∈ [−5.0, −0.4] step 0.2; β1 ∈ [−0.5, 1.0] step 0.1
  (negative values allowed — the age *decrease* hypothesis stays falsifiable);
  β2 ∈ [−0.5, 0.5] step 0.1; κ ∈ 2^{−1, −0.5, …, 11} (log2 step 0.5, 25 points).
- Stage 2: local refinement around the stage-1 argmax, ±1 stage-1 step per
  parameter at ¼ resolution. No interpolation; the stage-2 argmax is the estimate.
- If any parameter lands on a declared bound, the bound is extended once by the
  same span and the fit repeated; a second boundary hit is reported as such.
- Implementation may use numpy for vectorization; the grids above define the
  estimator regardless of implementation.

## 5. Model comparison, in-sample (locked)

AIC = 2k − 2·logL with k = 4 (primary) and k = 2 (constant); ΔAIC = AIC_primary −
AIC_constant. Pre-specified reading: ΔAIC ≤ −2 favors age dependence.

## 6. Participant-level cross-validation (locked)

- 5 folds × 20 repeats. Folds stratified by fixed age band (20–44 / 45–64 /
  65–86 — fixed constants, not sample quantiles), so every fold spans the age
  range.
- Seeds: 20260901 + r for repeat r ∈ {1..20}.
- Within each training set, both models are fit by §4 in full (no reuse of
  full-sample estimates). **No shape selection occurs anywhere in the primary CV**
  — the primary shape is fixed by §3. (Sensitivity S3 performs shape selection,
  and there it happens inside each training fold by training-AIC, precisely to
  avoid leaking structure from held-out participants.)
- Metric per repeat: summed held-out log-likelihood difference Δ_r (primary −
  constant) over all held-out participants across the 5 folds.

## 7. Decision rule (locked)

The age-dependent model is called **predictively superior** iff Δ_r > 0 in at
least **17 of 20** repeats (one-sided binomial p ≈ .0013 under a fair coin).
Overall confirmation:

- **Confirmed:** ΔAIC ≤ −2 (§5) AND CV rule met (§6–7).
- **Partially supported:** exactly one criterion met.
- **Not confirmed:** neither. All three outcomes are reportable results.

## 8. Uncertainty for the primary estimand (locked)

Nonparametric participant bootstrap, B = 500 resamples (seeded 20261001 + b),
refitting the primary model by §4 per resample; 95% percentile interval for Δα.

## 9. Sensitivity analyses (locked; reported alongside, never promoted)

- **S1 κ:** grid resolution doubled; boundary handling per §4.
- **S2 IQ cutoff:** none / 70 / 75 / 80 (expected N: 265 / 264 / 264 / 263).
- **S3 shape:** knee-linear (knee fixed 38) and estimated-knee alternatives.
  The estimated knee is reported **only if** its 95% profile interval spans
  < 20 years; otherwise declared unidentified on this sample (identifiability
  criterion fixed here, per review).
- **S4 influence:** full leave-one-participant-out (264 refits, stage-1 grids);
  report max |ΔΔα| and flag if it exceeds 20% of the point estimate.
- **S5 response rule:** all α results restated as ε = 2α; no separate fit needed
  (exact relabeling, IDENTIFIABILITY.md).

## 10. Posterior predictive checks (quantities locked now)

Parametric bootstrap from the fitted primary model, 500 simulations (seed 20261101):

- **T1:** pooled egocentric rate among ages 73–86 (fixed band).
- **T2:** number of participants with exactly one egocentric error among ages
  20–37 (fixed band).
- Report observed T1, T2 against 95% and 99% predictive intervals. No exclusion or
  reweighting of the oldest band regardless of outcome; a T1 failure is reported
  as a model limitation (this is the locked treatment of the oldest-decile
  discrepancy).

## 11. Gate to executive-function analysis (locked)

Mediation/moderation analyses proceed as **confirmatory-secondary** only if §7
returns "Confirmed." If either T1 or T2 falls outside its 99% predictive interval,
EF analyses still proceed but are labeled **exploratory** in all reporting.
EF multiplicity: the primary EF variable is a single composite (mean of z-scored
Stroop, O-Span, task-switching, Tower of Hanoi, each oriented so higher = better
EF, orientation fixed before data inspection). The four subscales are secondary,
Holm-corrected. Direction of the primary EF hypothesis: lower EF composite
associates with higher α, over and above age.

## 12. Reporting requirements (locked)

Every reported α carries its ε = 2α dual; the headline claim template is:
"Under P-MIX and its response assumptions, the estimated egocentric contribution
[increased/did not increase] with age (Δα = …, 95% CI …), and the age-dependent
model [was/was not] predictively superior to the fitted constant-α model in
held-out participants (…/20 repeats)." Deviations from this plan: §15 addenda only.

## 13. What this plan does NOT cover

Eye-tracking analyses (D1), any serial-model implementation, education work, and
any analysis of Shared-condition egocentric rows beyond descriptive reporting.

## 14. Execution

`experiments/exp4_confirmatory.py` implements §§1–10 and 12 exactly; it is written
after this freeze and reviewed against this document before running; its first
full execution is the confirmatory run, reported whole.

## 15. Addenda (initially empty)

*(none)*

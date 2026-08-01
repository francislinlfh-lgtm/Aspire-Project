# Frozen Analysis Protocol Following Exploratory Reanalysis — Study 1A

**Status: frozen at commit e09d306 (2026-08-03); amended by Addendum 1 (§15,
2026-08-04) after external review and BEFORE any protocol execution or any
`exp4` code existed.** The public commit history provides a timestamped,
version-controlled record of the frozen protocol; it does not by itself prove the
absence of earlier private analyses — the exploration disclosure below is the
honest account. The original frozen text is preserved verbatim at e09d306.

**Classification (per Addendum 1.1): this is a frozen robustness analysis
following exploration, not an independent confirmation.** Its hypotheses are
*prospectively specified for this execution*; they were formed on this same
dataset. Rerunning frozen code on data whose principal patterns are already known
cannot restore independence. A genuinely confirmatory test requires untouched
outcomes; the recognized candidates are (i) the eye-tracking data of this dataset,
whose outcome variables have never been inspected beyond the file header — eligible
only if a D1 protocol is frozen *before* any outcome inspection — and (ii) external
or newly collected datasets.

**Disclosure of prior exploration.** Exploratory analyses of this dataset (exp2,
exp3; STUDY_1A.md) identified the κ-floor problem, the age trajectory, favorable
model comparison and participant-level CV, the extreme-age misfit, the quadratic
shape choice, and statistics T1/T2. Every threshold below was chosen with
approximate knowledge of what the data will show. The value of this protocol is
that decisions are locked, execution is single-shot, and all outcomes are reported.

Data: Bradford, Brunsdon & Ferguson (2023), OSF 2epsu (DATASET_NOTES.md).
Model family: P-MIX(α), the choice-level projection of Heller et al. (2016)
Eq. 2, with a Beta-Binomial participant hierarchy. All α statements are conditional
on the probability-matching response rule; every reported α carries the exact dual
reading ε = 2α under argmax+lapse (§12).

## 1. Sample and cleaning (locked)

1. Remove byte-identical duplicate rows (expected: 48 rows, participants 28225,
   64185).
2. Exclude participants absent from `DirectorTask_Demographics.csv` (expected: id
   30145) and participants with FSIQ4 < 70 (expected: id 24255). Expected N = 264.
3. Model **Listener-condition trials only** (expected 12/participant). Outcome per
   trial: `EgocentricErrors` exactly as coded by the authors. OtherError trials
   count as non-egocentric trials (denominator retained). Shared-condition trials
   are manipulation checks only, never modeled.
4. If any expectation fails on execution, the run halts and the discrepancy is
   reported before proceeding (no silent adaptation).

## 2. Primary estimand (locked)

**Δα = α(75) − α(25)** under the primary model (probability units); secondary
summary Δα/50 per year. Ages in years; no rescaling.

## 3. Primary model (locked)

Logit-quadratic age curve with Beta-Binomial heterogeneity:

- `α(age) = logistic(β0 + β1·z + β2·z²)`, `z = (age − 53)/10` (fixed constant 53).
- `α_i ~ Beta(α(age_i)·κ, (1 − α(age_i))·κ)`; `e_i ~ Binomial(n_i, α_i)`; exact
  Beta-Binomial marginal likelihood (binomial coefficient omitted identically in
  all compared models — it cancels).

Rationale (recorded; shape chosen after exploration): exploratory parametric
predictive checks indicted knee-linear at both age extremes; the source paper's
accuracy curve was quadratic; the logit link keeps α in (0,1).

**Comparator:** constant-α Beta-Binomial (α0, κ) — described in all reporting as
"the fitted constant-α model," never "any constant-weight account."

### 3.1 Licensing the count likelihood (Addendum 1.5)

`e_i ~ Binomial(n_i, α_i)` is an implication of the trial-level model only under
the following stated assumptions:

- **(a)** Every Listener trial presents exactly one semantically matching
  privileged competitor and one intended mutually-visible referent (the Bradford
  design: one critical instruction per array). Under point-mass domain resolutions
  and probability matching, P(egocentric response) = α_i identically on each such
  trial.
- **(b)** The modeled outcome is binary *egocentric vs not*: OtherError responses
  (~1.2% of trials) are counted as non-egocentric. The likelihood therefore
  estimates egocentric-choice probability; it does not model the other-error
  process. A trinomial/lapse component is out of scope here — and exploratory T2
  already suggests a lapse-like component may be needed; this is a declared
  limitation, not an oversight.
- **(c)** Trials within a participant are treated as exchangeable given α_i;
  item/position effects are not modeled. This assumption is probed by S6
  (item-position diagnostics), and the scope of all conclusions is restricted
  accordingly (§6).
- **(d)** Trial-level information beyond the count (order effects, RT, specific
  competitor identity) is deliberately discarded at this stage.

## 4. Estimation (locked; Addendum 1.8)

1. Deterministic coarse grid (global search): β0 ∈ [−5.0, −0.4] step 0.2;
   β1 ∈ [−0.5, 1.0] step 0.1 (negative allowed — the decrease hypothesis stays
   falsifiable); β2 ∈ [−0.5, 0.5] step 0.1; log2 κ ∈ [−1, 11] step 0.5.
2. Continuous bounded local optimization (scipy Nelder–Mead; scipy 1.17.1 /
   numpy 2.4.4 recorded) started from the **five** best grid points; box bounds
   enforced (β0 [−7, 0], β1 [−1, 1.5], β2 [−1, 1], log2 κ [−1.5, 11.5]);
   convergence tolerance 1e−6 in logL; max 5000 evaluations per start.
3. The best converged optimum is the estimate. Non-convergence of all five starts,
   or an estimate on a box bound, halts with a report.
4. **Code validation is synthetic-only:** `exp4_protocol.py` is verified by
   parameter recovery on synthetic data with known parameters before its single
   full execution on the real dataset, which is reported whole.

## 5. Model comparison, in-sample (locked)

AIC = 2k − 2 logL, k = 4 (primary) vs k = 2 (constant). Prespecified reading:
ΔAIC ≤ −2 favors age dependence.

## 6. Participant-level cross-validation (locked; Addenda 1.2, 1.4)

- 5 folds × 20 repeats; folds stratified by fixed age band (20–44 / 45–64 /
  65–86); seeds 20260901 + r, r ∈ {1..20}; both models refit per training set by
  §4 (grid stage at full resolution). **No shape selection occurs in the primary
  CV** (the shape is fixed by §3); sensitivity S3 selects shape by training-AIC
  *inside each fold* only.
- Metric per repeat: summed held-out logL difference Δ_r (primary − constant).
- Reported: number of positive repeats; mean, median, and range of Δ_r; the
  participant-level aggregate out-of-fold difference (each participant's mean
  held-out contribution across repeats) with the fraction of participants
  positive; no inferential p-value is attached to any CV quantity.
- **Scope (locked language):** participant-level cross-validation assesses
  generalization across participants *within the observed task and item set*; it
  does not assess generalization to unseen items, task variants, populations, or
  laboratories.

## 7. Prespecified robustness criteria (locked; Addenda 1.1, 1.2)

- **R1:** ΔAIC ≤ −2 (§5).
- **R2:** Δ_r > 0 in at least 17 of 20 repeats. *The 17-of-20 threshold is a
  prespecified stability rule, not an inferential test, because repeated
  cross-validation estimates are correlated.*

Outcome categories: **Meets prespecified robustness criteria** (R1 and R2) /
**Mixed robustness evidence** (exactly one) / **Does not meet prespecified
robustness criteria** (neither). All three are reportable results.

### 7.1 Curve-shape reporting (locked; Addendum 1.7)

Report α(25), α(50), α(75) with bootstrap CIs; the fitted curve at 5-year
intervals over 20–86; the turning point age 53 − 5·β1/β2 if it lies in [20, 86];
and whether the fitted curve is monotonic over [20, 86] and over [25, 75].
**Language rule:** "increased across adulthood" may be used only if the fitted
curve is non-decreasing over [25, 75]; otherwise the shape is described as fitted.

## 8. Uncertainty for the primary estimand (locked; Addendum 1.9)

Nonparametric participant bootstrap: one generator, `numpy.random.default_rng(
20261001)`, drawing B = 1000 resamples sequentially; each resample draws 264
participants with replacement at the participant level; duplicated participants
enter as replicated clusters (their (age, e, n) records counted again). Each
resample is refit by §4 with the grid stage at half resolution. Failed or
bound-hitting fits are counted and reported; if successful fits fall below 950,
B is extended until 950 successes or the failure pattern is reported as the
result. Interval: percentile (2.5, 97.5) — chosen over BCa for transparency;
noted as a limitation.

## 9. Sensitivity analyses (locked; reported alongside, never promoted)

- **S1:** grid stage at doubled resolution in all four parameters.
- **S2:** IQ cutoff none / 70 / 75 / 80 (expected N 265 / 264 / 264 / 263).
- **S3:** shape alternatives — knee-linear (knee 38) and estimated-knee; the
  estimated knee is reported only if its 95% profile interval spans < 20 years,
  else declared unidentified on this sample. In CV contexts, shape selection
  happens inside training folds only.
- **S4:** full leave-one-participant-out (264 refits, coarse grid + single-start
  Nelder–Mead); report max |ΔΔα|; flag if > 20% of the point estimate.
- **S5:** response-rule dual statement ε = 2α on every reported α (exact
  relabeling; no refit).
- **S6 (Addendum 1.6):** item-position diagnostics — per-`trial_number` Listener
  error rates (descriptive table) and leave-one-trial-position-out re-estimation
  of Δα (12 refits); report max |ΔΔα|. Caveat, recorded: `trial_number` may
  conflate item identity with presentation position (counterbalanced design);
  if item identities become available from the authors or materials, this
  diagnostic is redone against true items.

## 10. Parametric predictive checks (locked; Addendum 1.3)

Simulation from the maximum-likelihood point estimates of the primary model —
**parametric predictive checks, not posterior predictive checks** (no parameter
posterior is integrated over). 1000 simulated datasets, seed
`numpy.random.default_rng(20261101)`:

- **T1:** pooled egocentric rate, ages 73–86 (fixed band).
- **T2:** number of participants with exactly one egocentric error, ages 20–37.
- Observed T1, T2 reported against 95% and 99% predictive intervals. The oldest
  band is never excluded or reweighted; a T1 failure is reported as a model
  limitation. (Locked treatment of the oldest-band discrepancy.)

## 11. Executive-function analyses: deferred (Addendum 1.10)

**Removed from this protocol.** EF analyses require a separate frozen protocol,
written after the present model assessment and before inspecting any EF
associations. This document predeclares only the gate: that future protocol may
be written and executed regardless of §7's outcome category, but its analyses are
labeled exploratory unless §7 returns "Meets prespecified robustness criteria"
and both T1 and T2 fall within their 99% predictive intervals. No claim of
mediation will be made from cross-sectional association in any case; the causal
estimand, outcome definition, measurement-error handling, transformations,
missing-data rules, and multiplicity structure belong to that future protocol.

## 12. Reporting requirements (locked)

Every reported α carries its ε = 2α dual. Headline template: "Under P-MIX and its
response assumptions, the estimated egocentric contribution [increased / did not
increase / followed the fitted shape] with age (Δα = …, 95% bootstrap CI …), and
the age-dependent model [met / partially met / did not meet] the prespecified
robustness criteria against the fitted constant-α model (…/20 CV repeats)."
Deviations: §15 addenda only.

## 13. Out of scope

Eye-tracking analyses (D1 — note: outcome-untouched, hence the project's one
genuine confirmatory opportunity if its protocol is frozen before inspection);
serial-model implementations; education work; Shared-condition rows beyond
descriptive reporting.

## 14. Execution

`experiments/exp4_protocol.py` implements §§1–10 and 12 exactly; it is validated
against synthetic data only (§4.4), then executed once on the real dataset; the
full output is reported regardless of outcome.

## 15. Addenda

### Addendum 1 — 2026-08-04, following external review; before any exp4 code

Original frozen text preserved at commit e09d306. Amendments, applied to the body
above for usability (the diff is the audit trail):

1. **Reclassified** as a frozen robustness analysis following exploration;
   "Confirmed/Partially supported/Not confirmed" renamed to robustness-criteria
   categories; confirmatory language removed throughout; document retitled
   (filename kept for link continuity).
2. **Binomial p-value on CV repeats removed** — repeats are correlated (same 264
   participants, overlapping training sets); 17/20 is a descriptive stability
   rule; CV reporting expanded (per-repeat and per-participant summaries).
3. **"Posterior predictive" renamed "parametric predictive"** — estimation is ML;
   no posterior is integrated over.
4. **CV scope restricted** to unseen participants on the same task and item set.
5. **§3.1 added:** explicit assumptions licensing the Beta-Binomial count
   likelihood as a projection of trial-level P-MIX, including the OtherError and
   exchangeability caveats.
6. **S6 added:** item-position diagnostics and dominance sensitivity.
7. **§7.1 added:** monotonicity and turning-point reporting locked; endpoint
   contrast may not be described as "increase across adulthood" if the curve is
   non-monotonic over [25, 75].
8. **Estimator upgraded** from lattice-only to coarse grid + multi-start
   continuous Nelder–Mead with bounds, tolerances, and halt conditions;
   synthetic-only validation requirement added.
9. **Bootstrap fully specified** (single RNG, sequential resamples,
   cluster-replication semantics, failure handling, minimum success count) and
   raised to B = 1000.
10. **EF mediation removed** to a separate future frozen protocol; only the gate
    remains here; the term "mediation" deleted from this protocol's claims.

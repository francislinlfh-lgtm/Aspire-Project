# Study 1A — Cognitive model validation

**Claim under test:** an explicit listener model (the domain-mixture account, P-MIX,
adapted from Heller, Parisien & Stevenson, 2016) can reproduce established human
perspective-taking behavior in the director task under a fit-then-predict protocol.

**This study makes no claim about LLMs (that is 1C) and uses no LLM anywhere (the
language layer is scripted frames; 1B validates the parser separately).**

## Hypotheses

- **H-1A.1:** a single fitted weight `α` reproduces the critical/control contrast
  (interference present on critical trials, absent on control — Keysar et al., 2000)
  within pre-registered tolerance.
- **H-1A.2:** the same fitted `α` (not refit) predicts held-out conditions —
  gradedness across manipulations of the display (Heller et al., 2016).
- **H-1A.3 (falsifiable premise):** boundary models P-EGO (α=1) and P-CG (α=0) fail on
  the same data — confirming the fit is doing work.

**Explicit non-claim:** 1A does not and cannot adjudicate serial adjustment vs
simultaneous weighing (IDENTIFIABILITY.md Prop. 1). Any such language in a draft is a
bug.

## Data

Priority order (availability audit is Step 0 — none of these is verified yet):

1. Trial-level data from Heller et al. (2016) — request from authors.
2. Public OSF datasets from perspective-taking studies (Brown-Schmidt / Ryskin labs —
   verify holdings and licenses).
3. Published summary statistics (error rates, condition means) from Keysar et al.
   (2000) and successors — fallback with stated limitations (no item/participant
   variance structure; weaker test).
4. If none suffices for held-out prediction: new choice-only data collection
   (browser-based; preregistered; IRB + ISEF SRC pre-approval; power analysis from
   published effect sizes).

**Step 0 status (2026-07-30): a candidate is verified.** OSF project 2epsu
("Cognitive Mechanisms of Perspective-Taking Across Adulthood: An Eye-Tracking Study
Using the Director Task"; see PubMed 36548095) — **trial-level confirmed by direct
inspection**: `DirectorTask_RawBehaviouralData.csv` has 6,432 rows = one per trial;
266 participants, ages ~20–86; 24 trials each (some 48); columns include CONDITION
(Listener = privileged competitor vs Shared), Object_Clicked (Target / Competitor /
Contrast / Distractor …), per-trial EgocentricErrors, TargetMoveAccuracy, and RT.
A companion 48.5 MB eye-tracking file holds AOI fixation indicators in 20 ms bins
with a "ScalarTime" column (apparently time-locked to the scalar adjective — verify
against the paper), i.e., process-level data relevant to experiment D1.

Adoption checklist — updated 2026-07-31 after obtaining the paper (Bradford,
Brunsdon & Ferguson, 2023, JEP:LMC; AAM via the St Andrews repository; do **not**
commit the PDF to this public repo — APA copyright):
- **Resolved by the paper:** Listener-Only = hidden competitor fits the description
  (perspective required) vs Shared-Perspective = no hidden competitor — maps exactly
  to our critical/control. 12 + 12 critical trials per participant (fillers excluded
  from the CSV, matching its 24 rows/participant). RT is measured **from scalar
  adjective onset** to click — which both confirms that the eye-tracking file's
  ScalarTime is scalar-locked and explains the negative RTs (anticipatory clicks
  before scalar onset). Their RT/eye analyses use lmer with maximal random effects
  (Barr et al., 2013); the participant-level lm is only their age-curve accuracy
  analysis. Bonus: the study includes an executive-function battery (Stroop,
  O-Span, task-switching, Tower of Hanoi — the MediationData.csv), i.e., published
  individual-difference measures that could later moderate fitted `α` — directly
  relevant to effort-based accounts (Epley et al., 2004).
- **Still open:** Object_Clicked codes 'AF', 'F', and numerals (likely filler/slot
  codes — ask or find codebook); why some participants have 48 rows; license
  confirmation; courtesy email. Correspondence per the author note: Elisabeth
  Bradford (Dundee) or Heather Ferguson (Kent). Note honestly: the authors' own
AccuracyAnalysis.Rmd fits participant-level `lm(EgocentricErrors ~ Age)` — our
trial-level hierarchical fitting goes beyond their published analysis, which is the
reanalysis contribution. Lifespan ages also upgrade H-1A.2: fitting `α` by age asks
whether perspective weighting changes across adulthood — a question their design
raises and a mixture-model reanalysis can quantify.

## Procedure

0. **Availability audit** of the datasets above; freeze the choice.
1. **Parameter recovery** on synthetic data: generate from P-MIX(α*), refit, report
   recovery precision vs trial count. If `α` is unrecoverable at realistic N, stop and
   redesign — before touching human data.
2. **Stimulus alignment:** rebuild displays and referring expressions to match the
   chosen dataset item-by-item, including vague-adjective semantics if the stimuli
   require them (MODEL_AUDIT §3.3 — the current superlative simplification is not
   faithful to Keysar's "small").
3. **Model upgrades required by the audit** (MODEL_AUDIT §4): graded within-domain
   distributions; response rule as explicit fitted component (probability matching vs
   softmax(τ) vs argmax+lapse).
4. **Fit** on the designated calibration subset (conditions or participants); freeze.
5. **Predict** held-out conditions; report prediction error, not fit quality
   (Roberts & Pashler, 2000).
6. **Sensitivity analysis** over response rules; conclusions must survive all three or
   be reported as response-rule-dependent.

## Step 1 results (2026-08-01): parameter recovery — PASSED

`experiments/exp1_recovery.py`, 100 replications at the dataset's exact structure
(264 × 12 critical trials, ages 20–86, Beta-Binomial heterogeneity κ=50, seed
20260801), engine-vs-analytic generative check passed:

*(Convention note: this study originally ran under the former `w = 1 − α`
parameterization; the mathematics is mirror-identical and values below are stated
in the α convention adopted 2026-08-01. `exp1_recovery.py` itself now uses α.)*

| Question | Result |
|---|---|
| A. Grand-mean `α` | recovered essentially unbiased: e.g. true 0.10 → 0.099 ± 0.005 |
| B. Age effect (published size: plateau→rise in egocentricity, slope ≈ 0.0027/yr) | **power 100/100** (ΔAIC < −2); slope recovered 0.00270 ± 0.00045; **false-positive rate 2/100** on flat truth |
| B′. Heterogeneity κ | weakly identified (estimates spread 16–1024 around true 50) — the magnitude of individual variation is not well constrained by 12 trials/person |
| C. Individual `α_i` | shrunk posterior SD 0.047 vs no-pooling SE 0.090 — individual estimates are ~half prior; **individual-difference claims (age, EF) must enter through the hierarchy, never per-person point estimates** |
| D. Response rule | exact theorem: matching and argmax+lapse are likelihood-identical under ε = 2α for *every* choice dataset — all `α` conclusions are conditional on the rule; the eye-tracking file (graded competitor consideration vs none) is the discriminating measurement |

Consequences for the fitting plan: proceed — grand `α` and `α(age)` at the
published effect size are comfortably recoverable; report κ with honest intervals;
frame EF-moderation as hierarchical regression; state the rule-conditionality in
the paper, with the ET reanalysis as the resolution path. Caveats carried: knee
fixed at 38; uniform ages (swap in empirical ages when the cleaning pipeline
exists); OtherError category needs a stated policy before real fitting.

## Steps 2–5 results (2026-08-01): exploratory first fit — REAL DATA

`experiments/exp2_bradford_fit.py` (EXPLORATORY — the confirmatory run requires a
pre-registered analysis plan first). Cleaning validation was exact:

- 6,432 → 6,384 rows (the 48 predicted duplicates removed); sample reconstruction
  landed at **N = 264, the paper's exact analysis N** (one id absent from
  demographics + one FSIQ4 < 70), all with exactly 12 Listener trials;
- **mean per-participant egocentric rate: 10.23% — matches the published 10.23%
  to the decimal.** The pipeline reproduces the paper's anchor before fitting.

First fit (P-MIX(α), Beta-Binomial hierarchy, knee fixed at 38):

| Quantity | Result |
|---|---|
| Raw age gradient (pooled ego rate) | 4.51% (20–37) → 8.42% (38–59) → 16.08% (60–86) |
| Model comparison | age model preferred, **ΔAIC = −20.4** vs flat |
| α(age) | α_young = 0.040; slope = 0.0025/yr, profile 95% CI [0.0015, 0.0033]; fitted α: 0.04 at 20–38 → 0.095 at 60 → **0.16 at 86** |
| Held-out (fit odd-position trials, predict even) | age model **+9.85 log-likelihood** (summed over all 1,584 held-out trials, ≈ +0.037/trial; hyperparameters estimated on the training half only; parity rule fixed in code before evaluation, though not formally pre-registered). **Limitation: a within-participant trial split does not license generalization to new participants** — participant-level cross-validation is part of the robustness battery (exp3) |
| Boundary models (H-1A.3) | for 90/264 participants, neither deterministic boundary policy assigns positive probability to the complete observed response pattern — both rejected as implemented policies (a statement about the policies, not about "impossible" psychology) |
| Heterogeneity | κ fit at the grid floor (4): strong individual overdispersion beyond age — extend the κ grid downward in the confirmatory run; EF moderation (MediationData.csv) is the obvious follow-up |

Headline sentence (exploratory; deliberately model-conditional): ***under P-MIX and
its response assumptions, the estimated contribution of the egocentric
interpretation to Bradford et al.'s (2023) trial-level choices increases
approximately threefold across the observed adult range** (extended-κ fit:
α ≈ 0.065 before age 38 to ≈ 0.20 at 86; the initial fourfold figure was partly a
κ-floor artifact — see battery results below), and the age-dependent model improves
held-out likelihood over the fitted constant-α model, including for entirely held-out
participants.* We have not directly measured a psychological
quantity called "egocentric weighting"; we have shown what the fitted parameter
must do, within this model, to account for the behavior. The contribution, stated
precisely: *a previously descriptive age-related error pattern can be expressed as
a quantitatively increasing latent mixture weight within an independently developed
model of perspective-sensitive interpretation, and this age dependence improves
out-of-sample prediction over a constant-weight model.*

**Robustness battery (exp3) — required BEFORE the EF mediation analysis and before
any confirmatory freeze.** The κ-at-floor finding means the hierarchy may be
under-expressing population heterogeneity, which could artificially sharpen the
slope CI; mediation on top of a misspecified hierarchy would partly explain
model error, not psychology. Battery: (i) κ grid extended below 4; (ii) continuous
age (decile table + posterior predictive checks by age band and condition);
(iii) IQ-exclusion sensitivity (none / 70 / 75 / 80); (iv) influential-participant
diagnostics; (v) repeated random trial-splits (was +9.85 split luck?);
(vi) **participant-level repeated cross-validation** (the generalization-to-people
test the parity split cannot provide); (vii) response-rule variant statements
(α vs ε = 2α relabeling made explicit in all reported numbers).

### Battery results (2026-08-01, `exp3_robustness.py`, seed 20260803)

**Verdict: the age effect survives, with three honest revisions and one upgrade.**

1. **The κ floor was binding, as the review predicted.** With the grid extended,
   κ ≈ 1.5 (not at the new edge): population heterogeneity is severe (a strongly
   right-skewed α distribution — most participants near 0, a heavy tail). Freeing
   it: **ΔAIC for the age model weakens from −20.4 to −13.9** (still clearly
   preferred), the slope CI **widens to [0.0015, 0.0040]** (point 0.00275), and
   α_young rises to 0.065. Revised trajectory: **α ≈ 0.065 (20–38) → ≈ 0.20 (86),
   approximately threefold** — the earlier "fourfold" was partly a κ-floor
   artifact. The exploratory table above is superseded by these numbers.
2. **Generalization to people holds — the upgrade.** Participant-level 5-fold CV,
   10 repeats: age model wins **10/10**, mean held-out Δ +5.71 (+0.022 per
   held-out participant). This is the test the parity split could not provide.
3. **The parity split was mildly lucky but not misleading:** 20 random
   within-participant splits give Δ mean +7.05, range [+3.60, +10.15],
   **20/20 positive**.
4. **No influential-participant fragility:** removing any of the 25 targeted
   candidates changes the coarse-grid slope by less than one grid step (0.0005) —
   resolution-limited but reassuring. **IQ-cutoff choice is irrelevant** (slope
   0.0030 at every cutoff from none to 80).
5. **Shape misfit at the extremes (new finding, PPC/deciles):** the knee-linear
   α(age) under-predicts the oldest decile (obs 31.1% vs pred 17.4%, ages 73–82)
   and over-predicts ages 52–63; and in the young band the model expects
   polarized error counts (0 or many) while the data show singletons
   (obs 18 participants with exactly one error vs ~5 predicted). The confirmatory
   plan must pre-register shape flexibility (estimated knee or quadratic, as
   Bradford et al. used). The joint discrepancy **suggests that a single
   age-varying mixture process may not fully account for errors at both ends of
   the age distribution** — a model-failure observation, not an inference about
   mechanisms; it sharpens the response-rule question the eye-tracking reanalysis
   (D1) exists to answer.

## PROTOCOL EXECUTION RESULTS (2026-08-01; exp4 at commit 63943b1; verbatim log in `results/exp4_protocol_output.txt`)

**OUTCOME CATEGORY: Meets prespecified robustness criteria** (R1: ΔAIC = −18.48;
R2: 20/20 CV repeats positive, mean +9.35, range [+7.06, +10.90]).

**Auto-generated §12 headline (the monotonicity rule fired — note the verb):**
*Under P-MIX and its response assumptions, the estimated egocentric contribution
**followed the fitted shape** with age (Δα = +0.1270, 95% bootstrap CI [+0.0621,
+0.1958]; ε-dual +0.2541 [+0.1242, +0.3916]), and the age-dependent model met the
prespecified robustness criteria against the fitted constant-α model (20/20 CV
repeats).*

Key results:

| Quantity | Value |
|---|---|
| Fitted curve | α(25) = 0.078 [0.046, 0.118] · α(50) = 0.076 [0.050, 0.104] · α(75) = 0.205 [0.147, 0.268] |
| Shape | shallow decline 20→38, **turning point at age 38.0**, then accelerating rise to 0.36 at 85 — not monotonic over [25,75], hence "followed the fitted shape," not "increased" |
| CV (unseen participants, same task/items) | 20/20 positive; per-participant mean out-of-fold Δ +0.035; 65.2% of participants positive (descriptive; no p — repeats correlated) |
| Bootstrap | 1000/1000 successes, zero failures |
| **T1 (ego rate 73–86)** | obs 0.290, **inside** 95% predictive interval [0.156, 0.358] — the quadratic resolved the oldest-band misfit that indicted knee-linear |
| **T2 (singleton errors 20–37)** | obs 18, **outside the 99% interval [1, 11] — pre-registered model failure**, now a quantified fact rather than an exploratory hint |
| S1 fine grid | Δα identical (+0.1270) |
| S2 IQ cutoffs | Δα 0.1225–0.1270 across all four — irrelevant |
| S3 estimated knee | best 62, 95% profile span 26 yr ≥ 20 → **declared unidentified per the pre-set criterion** (not reported) |
| S4 full LOO (264) | max |ΔΔα| = 0.0099 (~8% of estimate; below the 20% flag) |
| S6 positions | rates 0.044–0.156 across the 24 positions; leave-one-position-out max |ΔΔα| = 0.0100; caveat: position may conflate item |

Consequences, per the frozen protocol:

1. **The EF gate (§11) is partially closed:** the outcome category is met, but T2
   breaches its 99% interval → the future EF protocol's analyses carry the
   **exploratory** label. The gate did its work.
2. **The T2 failure is the paper's discovered question:** the model cannot produce
   the observed excess of exactly-one-error young adults; a single age-varying
   mixture process does not fully account for errors at both ends of the age
   range. This is the sharpened, pre-registered motivation for the D1
   eye-tracking protocol (whose outcomes remain sealed).
3. Two convergent details worth reporting: the freely-fitted quadratic put its
   turning point at **age 38.0** — the same breakpoint the source paper described
   — without being told; and the estimated-knee criterion correctly declared the
   knee unidentifiable at this N, validating the review's concern in data.

## Analysis

Hierarchical Bayesian fit (participant- and item-level variation where data permit);
model comparison across {P-MIX(α), P-EGO, P-CG} with complexity penalties (PSIS-LOO or
equivalent); posterior of `α` reported with intervals — `α` is the paper's
psychological payload, so its identifiability and stability across subsets is a
result, not a footnote.

## Outcomes

- **Success:** H-1A.1–3 met → the explicit model reproduces the established behavioral
  signatures; proceeds to 1C as the cognitive arm, and licenses D1
  (IDENTIFIABILITY.md §4) as the follow-up.
- **Informative failure:** no `α` fits both signatures → indicts a linking assumption
  (response rule, domain construction) or the point-mass simplification; the failure
  mode is diagnosable from the provenance traces and is itself reportable.
- **Uninformative failure to avoid:** fitting everything with post-hoc flexibility.
  The pre-registered analysis plan is the guardrail.

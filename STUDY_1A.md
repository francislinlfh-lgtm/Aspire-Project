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
in the α convention adopted 2026-08-02. `exp1_recovery.py` itself now uses α.)*

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

## Steps 2–5 results (2026-08-02): exploratory first fit — REAL DATA

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
approximately fourfold across the observed adult range** (fitted α ≈ 0.04 before
age 38 to ≈ 0.16 at 86), and the age-dependent model improves held-out likelihood
over any constant-α account.* We have not directly measured a psychological
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

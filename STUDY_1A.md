# Study 1A — Cognitive model validation

**Claim under test:** an explicit listener model (the domain-mixture account, P-MIX,
adapted from Heller, Parisien & Stevenson, 2016) can reproduce established human
perspective-taking behavior in the director task under a fit-then-predict protocol.

**This study makes no claim about LLMs (that is 1C) and uses no LLM anywhere (the
language layer is scripted frames; 1B validates the parser separately).**

## Hypotheses

- **H-1A.1:** a single fitted weight `w` reproduces the critical/control contrast
  (interference present on critical trials, absent on control — Keysar et al., 2000)
  within pre-registered tolerance.
- **H-1A.2:** the same fitted `w` (not refit) predicts held-out conditions —
  gradedness across manipulations of the display (Heller et al., 2016).
- **H-1A.3 (falsifiable premise):** boundary models P-EGO (w=0) and P-CG (w=1) fail on
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
  individual-difference measures that could later moderate fitted `w` — directly
  relevant to effort-based accounts (Epley et al., 2004).
- **Still open:** Object_Clicked codes 'AF', 'F', and numerals (likely filler/slot
  codes — ask or find codebook); why some participants have 48 rows; license
  confirmation; courtesy email. Correspondence per the author note: Elisabeth
  Bradford (Dundee) or Heather Ferguson (Kent). Note honestly: the authors' own
AccuracyAnalysis.Rmd fits participant-level `lm(EgocentricErrors ~ Age)` — our
trial-level hierarchical fitting goes beyond their published analysis, which is the
reanalysis contribution. Lifespan ages also upgrade H-1A.2: fitting `w` by age asks
whether perspective weighting changes across adulthood — a question their design
raises and a mixture-model reanalysis can quantify.

## Procedure

0. **Availability audit** of the datasets above; freeze the choice.
1. **Parameter recovery** on synthetic data: generate from P-MIX(w*), refit, report
   recovery precision vs trial count. If `w` is unrecoverable at realistic N, stop and
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

## Analysis

Hierarchical Bayesian fit (participant- and item-level variation where data permit);
model comparison across {P-MIX(w), P-EGO, P-CG} with complexity penalties (PSIS-LOO or
equivalent); posterior of `w` reported with intervals — `w` is the paper's
psychological payload, so its identifiability and stability across subsets is a
result, not a footnote.

## Outcomes

- **Success:** H-1A.1–3 met → the explicit model reproduces the established behavioral
  signatures; proceeds to 1C as the cognitive arm, and licenses D1
  (IDENTIFIABILITY.md §4) as the follow-up.
- **Informative failure:** no `w` fits both signatures → indicts a linking assumption
  (response rule, domain construction) or the point-mass simplification; the failure
  mode is diagnosable from the provenance traces and is itself reportable.
- **Uninformative failure to avoid:** fitting everything with post-hoc flexibility.
  The pre-registered analysis plan is the guardrail.

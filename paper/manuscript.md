# [Title — see OUTLINE.md options]

Francis Lin

*Draft v0.1. Sections 2–4 drafted for verification against
`results/exp4_protocol_output.txt`; Sections 1 and 5 to be written from the
scaffolds in OUTLINE.md. Every number below traces to a committed log.*

## Abstract

*[Write last — structure in OUTLINE.md. Must contain: Δα = +0.127 [+0.062,
+0.196]; 20/20 held-out CV; the T2 failure.]*

## 1. Introduction

*(¶1 drafted by FL, supervisor line edits applied — candle display aligned to the
three-candle canonical structure; keysar2000 added to the empirical claim. ¶2–¶6
still to draft per OUTLINE.md.)*

Understanding another person often requires setting aside information that is
obvious from one's own perspective \citep{samuel2025}. The problem is clearest in
reference resolution, where a listener must work out which object a speaker means.
Suppose a speaker and a listener both see two candles, and a third, smaller candle
is visible only to the listener. When the speaker asks for "the small candle," the
candle that is smallest in the listener's view cannot be the intended referent —
the speaker does not know it exists. To interpret the request correctly, the
listener must weigh not only which object best fits the description, but which
objects the speaker can see at all. Yet listeners sometimes look at, and
occasionally reach for, the hidden candle anyway \citep{keysar2000} — the classic
egocentric error.

The processes underlying such errors — documented most extensively in the
"director task" paradigm \citep{keysar2000} — remain disputed.
Egocentric-anchoring accounts propose that listeners initially interpret an
utterance from their own perspective and only later, through an effortful
correction process, adjust toward the speaker's knowledge; errors arise when that
adjustment is incomplete or delayed \citep{keysar2000, epley2004}.
Early-integration accounts instead argue that common-ground information
constrains reference resolution from the earliest moments of processing, such
that listeners do not necessarily begin from a fully egocentric interpretation
\citep{hanna2003}. A third possibility is that listeners represent both
egocentric and common-ground interpretations concurrently, with behavior
reflecting their relative probabilistic weighting rather than a fixed sequence of
anchoring and correction \citep{heller2016}. These accounts can produce similar
final choices even though they imply different underlying computations, making
aggregate error rates insufficient for deciding among them. More fundamentally,
the director task itself has been criticized as potentially confounding
perspective-taking with selective attention and task demands, leaving open
whether an "egocentric error" uniquely identifies a failure to use common ground
at all \citep{rubiofernandez2017}.

Existing computational work has formalized perspective use, but the central
quantity — how much weight the egocentric perspective actually receives — has
never been estimated from interpretive choices. \citet{heller2016} introduced a
probabilistic mixture parameter governing the relative contribution of egocentric
and common-ground information, but used it to generate qualitative predictions
rather than estimating its value from data. \citet{mozuraitis2018} subsequently
examined which ranges of a related parameter reproduced condition-level patterns
in reference production, without trial-level likelihood estimation, participant
heterogeneity, or age dependence. Other neighboring approaches have modeled
common ground as an inferred latent state evaluated against offline judgments
\citep{rubiofernandez2018} or fitted Rational Speech Act parameters in a
different communicative paradigm \citep{hawkins2021}. To our knowledge, no
previous study has estimated a comprehension-side perspective-mixture weight from
director-task choices using a participant-level hierarchy, modeled that weight
across adulthood, and evaluated the resulting age-dependent account through
held-out-participant prediction.

\citet{bradford2023} provide the empirical basis for the present analysis. They
studied a community lifespan sample of adults aged 20–86 (analytic N = 264) using
an eye-tracked, computerized version of the director task, in which each
participant completed 12 critical Listener-Only trials requiring them to ignore a
privileged competitor and interpret the director's intended referent. Their
behavioral analysis found a quadratic relation between age and egocentric error
rates: performance remained broadly stable through approximately age 37, followed
by a substantial increase in egocentric errors from around age 38 onward. The
study also recorded eye movements and made both the data and analysis code openly
available, creating an unusually rich basis for computational reanalysis.
However, their analysis characterized how observed error rates changed across
adulthood; it did not estimate the parameters of a cognitive model intended to
explain those choices.

The present study fitted a choice-level projection of the mixture model of
\citet{heller2016} to the director-task choices of \citet{bradford2023}, using a
Beta–Binomial participant hierarchy and a publicly frozen analysis protocol.
First, the model quantified how the estimated egocentric contribution varied
across adulthood: the contrast between ages 25 and 75 was Δα = +0.127, with a
95% participant-bootstrap interval of [+0.062, +0.196]. Second, the age-dependent
model predicted entirely held-out participants completing the same task and items
better than the fitted constant-α model in all 20 cross-validation repetitions.
Third, a prespecified parametric predictive check revealed a systematic failure
among younger adults, showing that a single age-varying mixture process does not
reproduce the full observed distribution of errors. The analysis therefore yields
not only an estimate of age-related variation in α, but also evidence about where
that quantitative account succeeds and where it breaks.

These results do not adjudicate among the three process accounts introduced
above. At the level of final two-alternative choices, a probability-matching
mixture weight is formally indistinguishable from an argmax-plus-lapse process
under the mapping ε = 2α (Proposition 1), so every estimate is conditional on the
assumed response rule; the Δα above reads equally as a lapse-rate change of
+0.254. Final choices likewise cannot determine whether competing perspectives
were represented simultaneously or arose through an egocentric interpretation
followed by correction. What the present study offers instead is one explicit
account made quantitative, its predictive value measured in held-out
participants, and its empirical failure point located.

**[INTRODUCTION COMPLETE — 2026-08-01. Remaining: Discussion ¶1–¶7 (FL, per
OUTLINE.md scaffold), abstract (last; T2 mandatory), AI-disclosure wording,
verify-flag sweep of references.bib.]**

## 2. Model

### 2.1 A choice-level projection of the domain-mixture account

Heller, Parisien and Stevenson (2016) proposed that listeners resolve definite
reference by weighing two referential domains simultaneously: an egocentric
domain (all objects the listener can see) and a common-ground domain (objects
visible to both interlocutors). Their Equation 2 combines Bayesian reference
resolution under each domain with a weight α on the egocentric domain,

P(obj | RE) = α · P(RE | obj, d=e) P(obj | d=e) + (1 − α) · P(RE | obj, d=c) P(obj | d=c),

where an α near 1 corresponds to egocentric interpretation and α near 0 to full
common-ground restriction. In the original paper, α was varied from 0 to 1 to
generate qualitative predictions; it was not estimated from data.

We fit a deliberately reduced projection of this model to choice data. On a
critical director-task trial, the display admits exactly one best egocentric
referent (a privileged competitor matching the instruction) and one best
common-ground referent (the intended target). With point-mass within-domain
resolution, the model reduces, per trial, to

P(select competitor) = α,  P(select target) = 1 − α,

under a probability-matching response rule. This projection discards three
components of the full account — graded, production-normed referring-expression
likelihoods; a ground-status prior; and incremental (partial-expression)
evaluation — and therefore estimates α only at the level of final choices.

### 2.2 Hierarchy

Participants vary. We model participant i's weight as
α_i ~ Beta(μ(age_i)·κ, (1 − μ(age_i))·κ), with egocentric-choice count
e_i ~ Binomial(n_i, α_i), yielding an exact Beta-Binomial marginal likelihood.
The primary age model is logit-quadratic,
logit μ(age) = β0 + β1 z + β2 z², z = (age − 53)/10;
the comparator is the fitted constant-α model (α0, κ). The primary estimand is
Δα = α(75) − α(25).

### 2.3 Response-rule conditionality (an exact equivalence)

**Proposition.** For two-alternative trials with point-mass domains, the
probability-matching rule with weight α and an argmax-plus-lapse rule with lapse
ε (lapses uniform over the two alternatives) induce identical likelihoods for
every possible dataset under the mapping ε = 2α.

*Proof.* Under matching, P(competitor) = α. Under argmax+lapse with α < .5, the
argmax is the target, so P(competitor) = ε/2. Setting ε = 2α equates the trial
likelihoods, hence all products of them. ∎

Consequently, choice data cannot distinguish "egocentric weighting" from "lapsing"
at this level: every α reported below carries its dual reading ε = 2α, and all
psychological interpretation is explicitly conditional on the response rule.
Process-level data (e.g., graded fixation measures) are required to separate the
readings; we return to this in the Discussion.

## 3. Method

### 3.1 Data

We reanalyze the open dataset of Bradford, Brunsdon and Ferguson (2023;
https://osf.io/2epsu/), an eye-tracked computerized director task with a
community lifespan sample. Participants followed prerecorded instructions to
move objects in a 4×4 grid with occluded slots; on Listener-Only (critical)
trials the occluded object matched the instruction (e.g., the smallest of three
candles, hidden from the director), so correct interpretation required the
director's perspective; on Shared-Perspective (control) trials the occluded
object did not match. Each participant contributed 12 critical and 12 control
trials. We model critical trials; the trial-level outcome is the authors'
EgocentricErrors coding (selection of the hidden competitor); other errors
(~1.2% of trials) count as non-egocentric, so the likelihood estimates
egocentric-choice probability specifically.

### 3.2 Cleaning, with verification against published anchors

Exact byte-duplicate rows were removed (48 rows from two participants whose
sessions were duplicated in the file); one participant absent from the
demographics file and one with FSIQ4 < 70 were excluded, reconstructing the
paper's analysis sample of N = 264 (ages 20–86), each with exactly 12 critical
trials. Two published anchors were reproduced before any model contact: the
analysis N (264) and the mean per-participant egocentric rate (10.23%,
matching Bradford et al.'s reported 10.23%). The cleaning pipeline halts if any
expectation fails.

### 3.3 Protocol history

All analysis decisions were frozen in a public, version-controlled protocol
before the outcome-bearing run (repository commits e09d306, amended a8de96b and
be30e90 after two rounds of external review; implementation 63943b1). The
protocol is explicitly a *frozen analysis following exploration*: earlier
exploratory passes on the same data (committed and public) informed the model
shape and the two predictive-check statistics, and this is disclosed rather than
laundered. One notable exploratory correction is retained in the record: an
initial fit with a bounded heterogeneity grid overstated the age effect
(a κ-floor artifact); freeing κ revised the trajectory downward and widened the
interval. Held-out participant prediction, single-shot execution, and complete
reporting carry the evidential weight.

### 3.4 Estimation and evaluation

Maximum likelihood by a deterministic coarse grid followed by five-start bounded
Nelder–Mead (tolerance 1e−6; bound-hits halt the run; numpy 2.4.4, scipy
1.17.1). Model comparison by AIC. Predictive evaluation by participant-level
5-fold cross-validation, 20 repeats, folds stratified by fixed age bands, fixed
seeds; both models refit within every training set; the prespecified stability
rule (positive held-out difference in ≥ 17/20 repeats) is descriptive, not an
inferential test, because repeated cross-validation estimates are correlated.
Uncertainty for Δα by participant-level cluster bootstrap (B = 1000, fixed
generator, percentile intervals). Parametric predictive checks (from ML point
estimates; not posterior predictive) used two prespecified statistics: T1, the
pooled egocentric rate at ages 73–86; T2, the number of participants aged 20–37
with exactly one egocentric error. Sensitivity analyses: finer grids; IQ-cutoff
variants; knee-shaped alternatives with a prespecified identifiability criterion
for the knee; full leave-one-participant-out; leave-one-trial-position-out.

### 3.5 Scope

Cross-validation here assesses generalization to unseen participants within the
observed task and item set; it does not assess generalization to new items,
task variants, populations, or laboratories.

## 4. Results

### 4.1 Primary fit

The primary model estimated β0 = −2.423, β1 = 0.279, β2 = 0.093, κ = 1.38
(log-likelihood −647.18), against the fitted constant-α model α0 = 0.112
(ε-dual 0.225), κ = 1.24 (log-likelihood −658.41). ΔAIC = −18.48, meeting
criterion R1. The fitted curve gives α(25) = 0.078 [95% CI 0.046, 0.118],
α(50) = 0.076 [0.050, 0.104], α(75) = 0.205 [0.147, 0.268] (ε-duals 0.155,
0.152, 0.409), with **Δα = +0.127 [+0.062, +0.196]** (+0.0025/yr averaged).
The curve is not monotonic over [25, 75]: it declines shallowly to a minimum at
age 38.0 and rises with acceleration thereafter (0.089 at 20; 0.067 at 40;
0.205 at 75; 0.360 at 85). The estimated egocentric contribution therefore
*followed the fitted shape* with age; per the protocol's language rule we do not
describe it as a monotonic increase. Notably, the freely fitted quadratic placed
its turning point at the same age (≈38) that Bradford et al. identified as the
onset of decline, while the knee-shaped sensitivity model's knee parameter was
declared unidentified under the prespecified criterion (95% profile interval
spanning 26 years) — the smooth model recovers the breakpoint description
without being told it, and the data cannot support estimating it as a parameter.

### 4.2 Held-out participant prediction

The age-dependent model produced a positive held-out log-likelihood difference
over the fitted constant-α model in **20 of 20** repeats (mean +9.35, median
+9.56, range [+7.06, +10.90]), meeting the prespecified stability rule R2. The
per-participant mean out-of-fold difference was +0.035, positive for 65.2% of
participants (descriptive summaries; no p-value is attached, as repeats are
correlated). The overall outcome category is **Meets prespecified robustness
criteria**. The bootstrap completed 1000/1000 refits without failures.

### 4.3 A prespecified model failure

T1 passed: the observed pooled egocentric rate at ages 73–86 (0.290) fell
within the model's 95% predictive interval [0.156, 0.358]. **T2 failed beyond
the 99% interval:** 18 participants aged 20–37 made exactly one egocentric
error, against a predictive interval of [1, 11]. The fitted hierarchy, which
accounts for the age trend and for heavy individual heterogeneity (κ ≈ 1.4),
cannot reproduce the observed excess of single-error young adults. We report
this as a result: a single age-varying mixture process, with this response
rule, does not fully account for errors at both ends of the adult age range.

### 4.4 Sensitivities

The estimand was stable in every prespecified probe: fine grids, Δα = +0.1270
(unchanged to four decimals); IQ cutoffs from none to 80, Δα between +0.1225
and +0.1270; full leave-one-participant-out, maximum |ΔΔα| = 0.0099 (≈8% of the
estimate, below the prespecified flag); leave-one-trial-position-out, maximum
|ΔΔα| = 0.0100 (with the recorded caveat that trial position may conflate item
identity in this dataset).

## 5. Discussion

*(Complete — FL draft, 2026-08-01; supervisor edits were citation forms and math
typesetting only. Canonical text lives in manuscript.tex §5; the seven paragraphs:
findings restated in template language → what α is and is not (the ε = 2α dual in
plain terms) → the age-38 convergence and knee unidentifiability → the T2 failure
and two candidate elaborations → five scope limits → the two designed next steps
(sealed ET as prospective test; EF exploratory by gate) → the broader close:
"a transparent quantitative account with an empirical success criterion and a
testable failure mode.")*

## Statements

**Data and code.** All analysis code, the frozen protocol with dated addenda,
and the verbatim execution log are public at
https://github.com/francislinlfh-lgtm/Aspire-Project (key commits: freeze
e09d306; amendments a8de96b, be30e90; implementation 63943b1; results 9764283).
The dataset is Bradford, Brunsdon & Ferguson's (2023) open data at
https://osf.io/2epsu/, cited rather than redistributed.

**AI assistance.** [Disclosure per venue policy — see OUTLINE.md.]

**Acknowledgments.** We thank Bradford, Brunsdon and Ferguson for publishing
their data and code.

## References

*[To assemble — every citation already appears in the repository's documents
with (verify) flags resolved for: Heller et al. 2016; Bradford et al. 2023;
Keysar et al. 2000. Verify page-level details for the remainder before
submission: Hanna et al. 2003; Epley et al. 2004; Epley & Gilovich 2006;
Rubio-Fernández 2017; Barr 2008; Frank & Goodman 2012; Roberts & Pashler 2000.]*

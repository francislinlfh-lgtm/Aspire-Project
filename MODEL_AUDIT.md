# MODEL_AUDIT — provenance of every model, equation, parameter, and function

**Labeling rule (binding, per project constitution):** every equation carries exactly one
label — **[LIT]** literature-derived (with citation; page/equation-level verification
noted where the source is not yet in hand), **[ADAPT]** adapted with stated
justification, **[PROV]** provisional hypothesis / our invention. Every empirical claim
carries a citation. An equation that cannot be traced is marked [PROV] or deleted.

**Summary verdict:**

| Element | Label | Verdict |
|---|---|---|
| P-EGO | reference limit (nobody's theory of adults) | retain as w=0 boundary; never present as a competing account |
| P-CG | reference limit (strong mutual-knowledge reading) | retain as w=1 boundary; already inconsistent with interference data |
| P-MIX(w) | [ADAPT] from Heller et al. (2016) | retain as the primary quantitative account; upgrade requirements listed in §4 |
| P-ANCHOR(p) | [PROV] — our invention wearing Keysar's name | **reclassify**: not a competing model; retain code only as the identifiability exhibit |
| `Interpretation.sample` (response rule) | [PROV] linking assumption | most consequential un-cited choice in the codebase; must be sensitivity-analyzed |
| `best_match` scalar semantics | [PROV] engineering | align to target-study stimuli before any fit |
| displays | paradigm-shaped simplification | rebuild to match the dataset being fit |
| clarification stubs | already labeled open/exploratory | unchanged |
| test suite | software validation only | correct as such; zero scientific validation exists yet |

---

## 1. Model dossiers

### 1.1 P-EGO (`listener.EgocentricListener`)

- **Equation:** `π(r) = 1[r = argbest(ego domain)]` — [PROV] as a theory of adults.
- **Parameters:** none.
- **Provenance:** no published account claims adult listeners are purely egocentric.
  Keysar's own position is *anchoring with adjustment* — egocentric interpretation is
  the starting point, not the endpoint (Keysar, Barr, Balin & Brauner, 2000, *Psych.
  Science*; Epley, Keysar, Van Boven & Gilovich, 2004, *JPSP*). P-EGO exists in cogsim
  as the w=0 limiting case and manipulation check.
- **Already falsified as a complete account:** humans show intermediate, not total,
  egocentric error (Keysar et al., 2000) — which is precisely why it is a reference
  point and nothing more.

### 1.2 P-CG (`listener.CommonGroundListener`)

- **Equation:** `π(r) = 1[r = argbest(CG domain)]` — [PROV] as stated; the *idea* is the
  strong reading of the mutual-knowledge constraint on definite reference (Clark &
  Marshall, 1981).
- **Parameters:** none.
- **Provenance:** even constraint-based theorists do not hold this: Hanna, Tanenhaus &
  Trueswell (2003, *JML*) found early but **partial** integration — privileged
  competitors still attract fixations. P-CG is the w=1 limit.
- **Already falsified as a complete account** by the interference findings above.

### 1.3 P-MIX(w) (`listener.MixtureListener`) — the primary account

- **Equation:** `π(r) = (1−w)·π_ego(r) + w·π_cg(r)` — **[ADAPT]**.
- **Source:** Heller, Parisien & Stevenson (2016, *Cognition*), "Perspective-taking
  behavior as the probabilistic weighing of multiple domains" — interpretation as
  simultaneous probabilistic weighing of egocentric and common-ground domains of
  reference. **Verification pending:** the paper is not yet in hand; the exact
  equation, the treatment of within-domain probabilities (they model graded fixation
  data and, we believe, include salience), and their parameter estimation must be
  confirmed against the text before any claim of implementing "their model."
  Reading list item #2; until verified the label stays [ADAPT], not [LIT].
- **Parameters:** `w ∈ [0,1]` — relative weight of the common-ground domain. The single
  psychologically interpretable free parameter of V1; a fitting target, never
  hand-set in any claim.
- **Our divergences from the source (each a confession, not a feature):**
  1. Within-domain distributions are point masses at the deterministic best match;
     Heller et al. fit graded fixation proportions. Point masses cannot fit fixation
     data and force all gradedness into `w`.
  2. `w` is time-invariant and context-invariant here; their account is about
     *simultaneity*, which our choice-level implementation neither tests nor contradicts.
  3. The response rule (§1.5) is appended by us and is no part of their model.

### 1.4 P-ANCHOR(p) (`listener.AnchorAdjustListener`) — reclassified

- **Equation:** `π = (1−p)·δ(anchor) + p·δ(adjusted)` — **[PROV], our invention.**
- **Purported source:** perspective adjustment (Keysar et al., 2000); anchoring and
  adjustment (Epley et al., 2004). **Neither paper contains this equation.** Their
  claims are *process* claims: the egocentric interpretation is computed fast and
  automatically; correction toward the other's perspective is effortful, slow,
  capacity-limited (time pressure and cognitive load increase egocentric errors —
  Epley et al., 2004; Lin, Keysar & Epley, 2010, *JESP*), and adjustment tends to be
  insufficient (Epley & Gilovich, 2006, *Psych. Science*).
- **The audit finding:** our Bernoulli gloss deletes exactly the content that makes the
  theory distinctive — the temporal asymmetry and effort dependence. What remains is
  algebraically identical to P-MIX (proven in `tests/test_core.py`). As implemented,
  P-ANCHOR is not Keysar's theory; it is P-MIX with a different docstring.
- **Action:** removed from the competing-model set of Study 1A. The class and its
  equivalence test are retained as the standing demonstration of the identifiability
  problem (IDENTIFIABILITY.md §1). A faithful serial implementation requires
  process-level dependent variables and does not exist yet — deliberately.

### 1.5 The response rule (`Interpretation.sample`) — the hidden model

- **Equation:** selection ~ posterior (probability matching) — **[PROV] linking
  assumption**, nowhere cited, and it silently determines how posterior mass maps to
  error rates (e.g., it is why P-EGO's error rate is exactly 1.0 in tests).
- **Alternatives with literature standing:** Luce choice rule / softmax with
  temperature (Luce, 1959); argmax-plus-lapse. The matching-vs-maximizing question is
  itself an old unresolved literature.
- **Action required before any fit (Study 1A):** treat the response rule as an explicit
  model component; fit or sensitivity-analyze across {matching, softmax(τ), argmax+ε}.
  Conclusions that survive only one response rule are conclusions about the response
  rule.

---

## 2. Function-by-function code audit

| Function | Scientific claim encoded | Grounding | Verdict |
|---|---|---|---|
| `world.Obj/Display` | perspective = per-object mutual visibility, binary | paradigm design (physical copresence, Clark & Marshall 1981); ground truth by construction of the director task | retain; note this *sidesteps*, not answers, CG-representation questions (V1.md §6.2) |
| `world.best_match` | scalar adjectives resolve deterministically to extreme within a domain; ties by oid | [PROV] engineering; superlatives are the easy case — vague positives ("the small candle" among three) are graded (Kennedy, 2007, *Ling. & Phil.*) and Keysar's stimuli used "small," not "smallest" — **stimulus-semantics mismatch to fix before fitting** | rewrite when Study 1A stimuli are fixed |
| `world.critical_display/control_display` | minimal 4-object realization of the critical/control contrast | shaped by Keysar et al. (2000) but not matched to it (their displays: 4×4 grid, ~8 objects, multiple occluded slots) | retain for demos; rebuild per target dataset |
| `language.scripted_instruction` | the director refers from the mutual perspective | matches confederate-script design of the paradigm | retain |
| `language.privileged_competitor` | defines "critical trial" | paradigm-derived DV definition | retain |
| `listener._domains` | candidate set = exact category match; no salience, uniform priors | [PROV] simplification; Heller et al. likely weight salience (verify) | upgrade path noted |
| `listener.*Listener` | §1 dossiers | see §1 | see §1 |
| `Interpretation.entropy` | none (math utility feeding exploratory clarification only) | — | retain |
| `clarify.NeverClarify` | assume-by-default baseline | consistent with good-enough processing as a default reading (Ferreira et al.), but chosen for conservatism, not derived | retain, labeled |
| `clarify.ExploratoryEntropyThreshold` | none (marked exploratory; the retracted-threshold lesson is in its docstring) | — | retain as labeled stub |
| `experiment.run_condition` | DV definitions; **`competitor_consideration` = posterior mass ↔ interference** | the ↔ is a linking *hypothesis*; posterior mass is not a fixation proportion, and fixations are process data our models are silent about | retain metric; forbid describing it as "fixations" anywhere |
| `experiment` clarified-trial handling (trial ends without selection) | none | arbitrary; human participants select after clarification | exploratory-only; fix if clarification ever becomes a claim |

**Test suite audit.** All seven tests validate that the implementation matches its
specification — software claims. `test_mix_anchor_choice_equivalence` is the one test
with theoretical content: a valid *analytic* result (an equivalence proof), not an
empirical one. No test validates any claim about humans. That is the correct current
state, and the gap Studies 1A–1C exist to fill. **Missing methodological test** (first
action of Study 1A, analysis code not architecture): parameter recovery — generate
synthetic choice data from P-MIX(w*), refit, and report recovery precision as a
function of trial count. If `w` does not recover from realistic Ns, the fitting plan
is dead before contact with human data.

---

## 3. Register of invented choices (complete)

1. Probability-matching response rule (§1.5) — consequential.
2. Point-mass within-domain distributions (§1.3.1) — consequential for fixation data.
3. Deterministic scalar semantics; superlative reading of vague adjectives — mismatch
   with actual paradigm stimuli ("small").
4. Exact-category candidate generation; no salience weighting; uniform priors.
5. Tie-breaking by object id — harmless (no claim), but present.
6. Display miniaturization (4 objects vs the paradigm's larger displays).
7. Clarified trials terminate without selection — exploratory path only.
8. P-ANCHOR's Bernoulli formalization — see §1.4 (reclassified accordingly).

## 4. Required upgrades before any fit (requirements, not code yet)

1. Graded within-domain distributions (needed for S2 gradedness and any fixation-linked
   fitting; brings implementation closer to the verified Heller et al. formulation).
2. Response rule as an explicit, swappable, fitted component.
3. Stimulus builder matched item-by-item to whichever dataset Study 1A secures.
4. Verification pass on Heller et al. (2016): exact equations, salience treatment,
   fitted parameter values — then relabel §1.3 [ADAPT] → [LIT] where earned.

# IDENTIFIABILITY — which observations can separate which accounts

The central scientific problem of V1 (see MODEL_AUDIT.md for model provenance).

---

## 1. Formal equivalence results

**Proposition 1 (choice equivalence).** For any display and referring frame such that
within-domain resolution is deterministic (a unique best match per domain), P-MIX(w)
and P-ANCHOR(p = w) induce identical choice distributions: both are two-point mixtures
over {egocentric best, common-ground best} with weights (1−w, w).
*Proof:* by construction of both posteriors; verified exhaustively over V1 trial types
in `tests/test_core.py::test_mix_anchor_choice_equivalence`.

**Corollary.** No experiment that records only final object choices on such stimuli can
distinguish a simultaneous-weighing account from a serial anchor-adjust account *at
this level of formalization*. Any paper claiming otherwise from choice data alone is
overreaching — including ours, if we ever do.

**Proposition 2 (nesting).** P-EGO = P-MIX(0) and P-CG = P-MIX(1). The pure models are
boundary points, not alternatives; fitting w tests them automatically.

**Scope note.** Proposition 1 is about our *formalizations*. The underlying theories
(Keysar's effortful adjustment; Heller et al.'s simultaneous weighing) differ in
process content that our choice-level implementations deliberately omit — which is
exactly why the corollary bites: the theories differ, the choice data cannot see it.

## 2. Pairwise divergence map

| Pair | Identical predictions when… | Diverge when… | Choice data sufficient? |
|---|---|---|---|
| P-EGO vs P-MIX(0<w) | control trials (domains coincide) | critical trials | **yes** — and humans' intermediate error rates already reject P-EGO (Keysar et al., 2000) |
| P-CG vs P-MIX(w<1) | control trials | critical trials (P-CG predicts zero interference) | **yes** — fixation interference and nonzero errors already reject P-CG (Keysar et al., 2000; Hanna et al., 2003) |
| **P-MIX vs P-ANCHOR** | **always, on V1 stimuli (Prop. 1)** | only in process observables; possibly in choice under vague modifiers (§3.6) | **no** |

The live identifiability problem is the last row — which is also the live theoretical
dispute in the field (serial adjustment vs simultaneous integration).

## 3. Observables audit

Each candidate observable, tied to literature or marked non-diagnostic. (verify) marks
citations to be confirmed against the source before use in a paper.

### 3.1 Eye-movement time-course — the canonical discriminator
Fixation proportions over time distinguish early-egocentric-then-correct from
constant-proportion integration. This is precisely the battleground of the published
debate: interference fixations (Keysar et al., 2000); early partial integration
(Hanna et al., 2003); anticipation without integration (Barr, 2008, *Cognition*);
simultaneous weighing argued from time-course data (Heller et al., 2016). Diagnostic
**in principle**; requires our models to grow graded domains plus a temporal linking
model (neither exists yet — MODEL_AUDIT §4). The fact that the field has this data and
still disputes the conclusion is the opportunity: the accounts have never been fit
jointly, as formal models with shared linking assumptions, to the same dataset.

### 3.2 Response time / deadline (time pressure)
Serial-effortful accounts predict more egocentric errors under time pressure or load —
and this is empirically documented (Epley et al., 2004; Lin, Keysar & Epley, 2010;
Keysar, Lin & Barr, 2003 (verify details)). A *fixed-w* mixture predicts
deadline-invariant choice once encoding is complete. Diagnostic between the
**parsimonious** versions; see mimicry caveat (§5). Cheapest process-sensitive design
(browser-deliverable; no eye tracker). Response-signal / speed–accuracy-tradeoff
methodology exists in sentence processing (McElree & Griffith, 1995 (verify)).

### 3.3 Attention order / first fixations
A sub-signal of §3.1; same requirements.

### 3.4 Confidence
Not diagnostic here: both formalizations output the *same posterior*, so any naive
confidence linking yields identical predictions. Diagnostic only under added process
assumptions (e.g., conflict-detection confidence signatures) that neither theory
currently specifies. Excluded.

### 3.5 Clarification behavior
Both accounts are silent on clarification (it is our open RQ3, V1.md §6.1). Could
become diagnostic under added assumptions (serial: clarification triggered by detected
anchor/adjustment conflict; simultaneous: by graded ambiguity) — but both the decision
theory and the human baseline are missing. Excluded from V1 claims.

### 3.6 Graded choice probabilities under vague modifiers — [PROV] derivation
V1 stimuli use superlatives ("smallest"), making within-domain resolution
deterministic and triggering Proposition 1. With **vague positives** ("the small
candle" — graded semantics; Kennedy, 2007) and ≥2 common-ground candidates, a serial
account with *insufficient adjustment* (Epley & Gilovich, 2006) predicts final choices
biased toward the anchor within the common-ground domain, while simultaneous weighing
predicts anchor-independent choice among CG candidates. This would be a **choice-level
discriminator** — but the translation of insufficiency to reference resolution is our
derivation, not the literature's. Status: provisional; promising; requires the graded
semantics upgrade first. Notably, Keysar's actual stimuli used vague positives — our
superlative simplification (MODEL_AUDIT §3.3) is hiding potential signal.

### 3.7 Repeated-trial adaptation
Speaker-reliability effects on pragmatic inference exist (Grodner & Sedivy, 2011
(verify); Ryskin & Brown-Schmidt adaptation studies (verify)). Both accounts
accommodate adaptation by letting their parameter drift; weakly diagnostic without
process assumptions. Deferred.

### 3.8 Mouse-tracking
Continuous attraction toward competitors as a cheap time-course proxy (Spivey,
Grosjean & Knoblich, 2005, *PNAS*; Freeman & Ambady, 2010, *Behav. Res. Methods*).
We know of no public director-task mouse-tracking dataset (verify). A candidate
methodology for D1 if deadline designs prove too coarse.

## 4. D1 — the smallest discriminating experiment

**Purpose:** distinguish serial-adjustment from fixed-weight simultaneous integration —
the pair choice data cannot separate (Prop. 1).

- **Design:** response-deadline director task, browser-based. 2 (trial type:
  critical/control) × 2 (deadline: short/long, calibrated in piloting) within-subjects;
  display preview before the utterance so perceptual encoding is not confounded with
  the deadline; deadline anchored to noun offset.
- **IVs:** trial type; deadline. **DVs:** object choice (primary); RT (secondary).
- **Model predictions** (each could be wrong — that is the point):
  - *Serial adjustment* (process version, to be formalized before data collection):
    egocentric-error rate falls from short to long deadline on critical trials —
    a deadline × trial-type interaction. Anchor: time-pressure findings (Epley et
    al., 2004).
  - *Fixed-w mixture:* egocentric-error rate constant across deadlines (given encoding
    control); no interaction.
  - *Both predict:* near-ceiling control accuracy at both deadlines (manipulation
    check).
- **Result favoring serial:** reliable interaction, short ≫ long errors.
- **Result favoring fixed mixture:** flat intermediate error across deadlines.
- **Result falsifying both parsimonious accounts:** no interference at any deadline
  (indicts stimuli against the entire literature), interference *increasing* with
  time, or degraded control accuracy (encoding confound — design failure, not theory
  failure; rerun).
- **Data requirements:** **no suitable public dataset is known to us — stated
  plainly.** Verification queue before collecting anything: (i) Heller et al. (2016)
  data via authors; (ii) OSF holdings of the Brown-Schmidt / Ryskin labs; (iii) any
  deadline-paradigm director-task data. If collection is needed: preregistered; N from
  a power analysis on published critical-trial effect sizes (not guessed here); IRB
  and ISEF SRC pre-approval mandatory (human subjects, minor researcher).
- **Analysis plan:** hierarchical logistic regression (trial type × deadline, random
  intercepts/slopes by participant and item); formal model comparison of the two
  implemented accounts with complexity penalties (PSIS-LOO); **parameter recovery on
  synthetic data before any collection** (MODEL_AUDIT §2, missing-test item).
- **Sequencing:** D1 runs only after Study 1A validates the choice-level machinery.
  It is an extension, not part of the V1 minimal claim.

## 5. The mimicry caveat (disclosed, not buried)

A mixture with time-varying w(t) can mimic any serial account; flexible models mimic
(Roberts & Pashler, 2000, *Psych. Review*; Pitt & Myung, 2002, *TICS*). D1 therefore
adjudicates the *parsimonious* versions of each account; the general claim is bounded
by complexity-penalized comparison, and we say so in any writeup.

## 6. Research-gap statement (narrowest defensible; conditional on verification)

> Egocentric interference in the director task is well documented (Keysar et al.,
> 2000), and probabilistic-weighing models of perspective use have been proposed and
> fit to time-course data (Heller et al., 2016). However, the competing accounts —
> serial egocentric adjustment and simultaneous domain weighing — have each been
> formalized only within their originating papers, under non-identical stimuli,
> dependent variables, and linking assumptions; at the level of final object choice
> they are provably observationally equivalent (Proposition 1). To our knowledge, no
> shared executable framework exists that (i) implements the competing accounts
> against a common task interface, (ii) makes linking assumptions explicit and
> separable, (iii) derives their equivalence classes formally, and (iv) supports
> fit-then-predict comparison on common human datasets — with LLM listeners runnable
> as comparison systems in the same harness.

**Standing caveats:** "to our knowledge" requires the systematic search pass
(RELATED_WORK.md verification debt) — in particular, whether Heller et al. (2016) or
follow-ups already performed formal serial-vs-simultaneous model comparison on their
own data, and whether a companion production-side model exists (Mozuraitis, Stevenson
& Heller (verify)). If either substantially overlaps, the gap narrows to items
(iii)–(iv) and the LLM bridge, and we will say exactly that.

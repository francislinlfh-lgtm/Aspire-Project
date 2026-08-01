# Study 1C — Architecture comparison

**Claim under test:** explicit cognition with an audited language boundary reproduces
human behavioral dynamics in the director task better than an end-to-end LLM listener.

**Stated as a question, not a foregone conclusion — the LLMs may win, and that result
would be published too.**

## Prior art (bounds our claims)

The director task has already been adapted to multimodal LLMs, with reported Level-2
perspective-taking deficits (Visuospatial Perspective Taking in Multimodal Language
Models, 2026, arXiv:2603.23510; see RELATED_WORK.md §8). LLM false-belief evaluations
exist in quantity (and their fragility is documented — Ullman, 2023). Therefore 1C's
contribution is **not** "we evaluated LLMs on the director task." It is:

1. a **DV-matched, same-harness** comparison: identical trials, identical dependent
   variables, cognitive model and LLM listeners run through the same instrument;
2. a **model-based characterization** of LLM behavior: fitting P-MIX to LLM choices to
   ask whether the LLM behaves *as if* it had any stable perspective weight `α` —
   using the cognitive model as a measurement device on the LLM.

## Systems

- **Cognitive arm:** P-MIX with `α` fitted in Study 1A (frozen — no refitting to look
  good here).
- **LLM arms:** (a) text-rendered display + instruction → constrained choice;
  (b) multimodal variant if resourced; (c) prompt battery: minimal instructions vs
  explicit perspective instructions ("the director cannot see objects in covered
  slots") — the difference between (a) and (c) is itself a finding about where the
  behavior lives (weights vs instructions).
- At least two model families; temperature and sampling documented; N samples per
  trial for response distributions.

## Dependent variables (identical across arms)

- Critical-trial egocentric error rate; control accuracy (manipulation check).
- Gradedness: behavior across parametric display manipulations (number/rank of
  competitors).
- **Stability:** repeated identical trials → response distribution consistency;
  cross-prompt variance (an LLM whose "perspective-taking" swings with paraphrase has
  no stable underlying quantity — report this as variance, not as gotcha).
- **Implied-α analysis:** fit P-MIX per arm; report whether a stable `α` exists across
  conditions, with fit quality. The cognitive arm has this by construction; the
  question is whether the LLM arms do.

## Confounds and controls

- **Contamination:** Keysar-style stimuli plausibly appear in training corpora. Use
  novel object categories/configurations isomorphic to the paradigm; report any
  verbatim-paradigm probes separately.
- **Prompt sensitivity:** pre-registered prompt battery; all prompts in the appendix;
  no post-hoc prompt fixing.
- **Format effects:** constrained response format validated on control trials first.

## Comparison criteria (pre-registered)

1. Signature reproduction: presence and gradedness of interference; control cleanliness.
2. Parameter stability/interpretability (`α` posterior width and cross-condition drift).
3. Transparency: Aspire ships a per-trial provenance trace; LLM arms ship completions.
   Reported as a qualitative architectural property, not scored.
4. Data efficiency (trials needed to characterize each system's behavior).

## Possible outcomes, honestly

- LLMs show no interference (over-cooperative or instruction-following) → human-shaped
  misunderstanding requires perspective *limits*, which the explicit model has and the
  LLM lacks.
- LLMs show human-like graded interference with stable implied `α` → the architecture
  claim weakens substantially; report as such. The instrument still contributed the
  measurement method.
- LLMs show interference that is unstable across prompts/paraphrases → the phenomenon
  exists in the LLM but is not a stable disposition; the implied-α analysis quantifies
  this.

# Study 1B — Language-boundary validation

**Claim under test:** an LLM parser can convert natural-language director utterances
into the structured frames the cognitive model consumes **without changing the
cognitive result and without semantic leakage**.

**This is an engineering-validation study. It makes no psychological claim.** Its role
is to protect 1A ("the LLM did the cognition" critique) and 1C ("the parser corrupted
the stimuli" critique) from each other.

## What the parser is and is not allowed to do

Contract (V1.md §2): `parse: utterance text → ReferringFrame(category, scalar)`.
The parser receives **no display information** — it cannot see objects, visibility, or
trial condition. Perspective inference, candidate weighting, and interpretation are
cognition; classification of the utterance into a closed frame space is language.

## Test batteries

1. **Verbatim battery:** the exact scripted instructions used in 1A.
2. **Paraphrase battery:** systematic rewordings ("grab the little candle," "the
   tiniest one — the candle").
3. **Adversarial battery:** indirect requests ("could you get me the small candle?"),
   disfluencies, distractor adjectives, embedded mentions ("not the truck, the small
   candle").
4. **Leakage battery:** identical utterances paired (in separate calls) with varied
   claimed contexts; a compliant parser must produce identical frames — any
   context-sensitivity of frame output is leakage by definition.
5. **Round-trip battery:** template-rendered clarification questions and rendered
   frames re-parsed; require frame fidelity (no added or dropped content). This is
   the audit inherited from V1.md §2.2.

## Metrics

- **Frame accuracy** vs gold frames, per battery.
- **Downstream invariance:** run the identical 1A simulation twice — scripted frames
  vs parsed frames, same seeds. Metric: per-trial choice agreement and distributional
  distance; test paired per-trial disagreements (McNemar). Target: differences within
  simulation sampling noise, pre-registered threshold.
- **Leakage rate:** violations in battery 4 and added-content events in battery 5.
  Target: zero tolerated in accepted runs; every occurrence reported, none silently
  patched.
- **Failure taxonomy:** misparse classes (wrong category, wrong/missing scalar,
  hallucinated modifier), reported by class — the error *structure* matters for
  interpreting any 1C result.

## Design notes

- Multiple parser backends (at least two model families, plus a trivial rule-based
  parser as floor/control): the claim is about the *boundary contract*, not one model.
- Deterministic replay: all parser I/O recorded; the paper's runs are re-executable
  offline from the cache.
- **Report bar:** 1B passes only if downstream invariance holds. Parser accuracy below
  invariance-threshold on adversarial batteries is a *scope statement* for 1C's
  free-language conditions, not a failure of 1A (which uses scripted frames).

# Aspire Project

A small instrument for testing theories of how people understand each other, and how
they fail to.

## The task

Sit across a grid of open shelves from another person. Three candles sit in the slots
between you: a large one, a medium one, a tiny one. The tiny one is in a covered slot
that only you can see into. The person across from you says: "Move the small candle."

From their side of the shelves, the small candle is obviously the medium one. They
don't know the tiny one exists. You know all of this. And still, in study after study,
listeners look at the hidden candle, hesitate over it, and sometimes reach for it
(Keysar, Barr, Balin & Brauner, 2000).

Psycholinguists call this the director task, and they have spent a quarter century
arguing about what it shows. One camp says interpretation starts from your own view of
the world and gets corrected afterward, effortfully, when you remember that the other
person is not you (Keysar et al., 2000; Epley, Keysar, Van Boven & Gilovich, 2004).
Another says there is no correction step: both perspectives are weighed at once,
probabilistically, and the errors fall out of the weighting (Heller, Parisien &
Stevenson, 2016).

Here is the uncomfortable part. If all you record is which candle the listener finally
picks, the two accounts make identical predictions. There is a unit test in this
repository that proves it
(`tests/test_core.py::test_mix_anchor_choice_equivalence`), and working out what
observation could actually separate them is much of what this project is about
([IDENTIFIABILITY.md](IDENTIFIABILITY.md)).

## The rule that defines the project

Aspire contains language models and cognitive models, and they are never allowed to
touch.

An LLM may parse a sentence into structured data ("the small candle" becomes a
category and a size). It may render structured data back into words. It may not
reason, remember, weigh perspectives, update beliefs, or decide anything. All of that
runs in explicit equations you can read, with parameters that mean something. There is
no LLM call anywhere in the core package; every experiment runs offline,
deterministically, from a seed.

The rule exists for a plain reason. If any part of the cognition happens inside a
language model, you can no longer say which theory produced the behavior, and the
whole exercise stops being science.

## Why

Misunderstanding usually gets described as someone's failure: one person explained
badly, or the other listened badly. The psychology of conversation has spent decades
pushing against that picture. "It takes two people working together to play a duet,"
write Clark & Brennan (1991). Understanding is not a signal one person transmits to
another but something two people assemble together, each guessing at what the other
can see.

When it goes wrong, the wreckage has a shape: a gap between what a person intended,
what they actually expressed, and what the other person finally understood. Everyday
life gives you no way to take that gap apart. You live inside your own interpretation
and call it the truth.

The director task is the smallest laboratory version of that gap I know of. One
sentence, one shelf, one hidden candle, and already two people inhabit different
worlds. Aspire models the listener's side of it in pieces small enough to test: what
they saw, how they weighed the other person's view against their own, how unsure they
were, and eventually what they decide to do about being unsure.

## What is actually here

The honest inventory, as of now:

- `cogsim/` — a Python package, standard library only. Displays, structured
  instruction frames, and four listener models: a probabilistic mixture adapted from
  Heller et al. (2016) with a single interpretable parameter `w` (how much weight the
  listener gives the shared view), two boundary models that bracket it, and one model
  kept purely as a cautionary exhibit, because our formalization of it turned out to
  be the mixture model wearing a different name.
- `experiments/exp0_keysar_signature.py` — runs the critical/control contrast and
  prints the classic interference pattern. By construction. The script says so
  itself: it demonstrates the instrument, not a finding.
- `tests/` — seven tests. They check that the code matches its specification,
  including the equivalence proof above. None of them validate anything about humans
  yet.
- The paper trail. Every equation in the project carries one of three labels:
  literature-derived, adapted with justification, or provisional, meaning our own
  unproven guess. [MODEL_AUDIT.md](MODEL_AUDIT.md) traces each model to its source,
  or admits that it can't.

No human data has been fit yet. Instrument built; science not yet begun.

## The plan

Three studies, kept separate so their claims can't blur into one:

1. [Study 1A](STUDY_1A.md) — can the explicit model reproduce the published human
   findings, fitting its parameter on part of the data and predicting the rest? No
   LLM involved anywhere.
2. [Study 1B](STUDY_1B.md) — can an LLM parser feed the same model natural language
   without changing the outcome and without leaking information across the boundary?
   An engineering claim only.
3. [Study 1C](STUDY_1C.md) — put end-to-end LLM listeners on the identical trials and
   compare. Written so that the LLMs are allowed to win; that result would be
   reported too.

## Running it

```
python tests/test_core.py
python experiments/exp0_keysar_signature.py
```

Python 3.10 or newer. No dependencies.

## Reading order

1. [V1.md](V1.md) — the research specification
2. [MODEL_AUDIT.md](MODEL_AUDIT.md) — where every equation comes from
3. [IDENTIFIABILITY.md](IDENTIFIABILITY.md) — which measurements can tell which
   theories apart, and the experiment designed to do it
4. [STUDY_1A.md](STUDY_1A.md) · [STUDY_1B.md](STUDY_1B.md) ·
   [STUDY_1C.md](STUDY_1C.md) — the three claims
5. [RELATED_WORK.md](RELATED_WORK.md) — what already exists, and the narrow gap left
6. [READING_LIST.md](READING_LIST.md) — the ten papers that come before any new code
7. [ARCHITECTURE.md](ARCHITECTURE.md) — an archived early vision, kept as a quarry

## Where this came from

The repository's first life was a canvas game with three LLM-driven characters
(`reference/drift-lab-v3-1.html`). It looked alive and proved nothing: the language
model was inventing the psychology on the fly and grading its own homework. It stays
in the repo as the negative example the rule above exists to prevent.

## License

MIT.

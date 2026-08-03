# Aspire Project

A small instrument for testing theories of how people understand each other, and how
they fail to.

**Paper:** *From Error Curves to an Estimated Weight: A Model-Based Reanalysis of
Perspective Taking Across Adulthood* — [PDF](paper/manuscript.pdf), source and
verified bibliography in [`paper/`](paper/).

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
([IDENTIFIABILITY.md](docs/IDENTIFIABILITY.md)).

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
  Heller et al. (2016) with a single interpretable parameter `α` (how much weight
  the listener gives their own view over the shared one — Heller et al.'s own
  convention), two boundary models that bracket it, and one model
  kept purely as a cautionary exhibit, because our formalization of it turned out to
  be the mixture model wearing a different name.
- `experiments/exp0_keysar_signature.py` — runs the critical/control contrast and
  prints the classic interference pattern. By construction. The script says so
  itself: it demonstrates the instrument, not a finding.
- `tests/` — eight engine tests plus architecture boundary checks. They verify
  that the code matches its specification, including the equivalence proof above.
- `experiments/` and `results/` — the full analysis arc: parameter recovery
  (exp1), an exploratory first fit (exp2), a robustness battery (exp3), and the
  single frozen-protocol execution (exp4), whose verbatim log is committed.
- `paper/` — the manuscript: LaTeX, figure, references.
- The paper trail. Every equation in the project carries one of three labels:
  literature-derived, adapted with justification, or provisional, meaning our own
  unproven guess. [MODEL_AUDIT.md](docs/MODEL_AUDIT.md) traces each model to its source,
  or admits that it can't.

The science has begun, and its first pass is complete: a frozen-protocol
reanalysis of Bradford, Brunsdon & Ferguson's (2023) open lifespan director-task
data, executed once and reported whole ([PREREGISTRATION.md](PREREGISTRATION.md);
results in [docs/STUDY_1A.md](docs/STUDY_1A.md)). The fitted egocentric weight
runs from about 0.08 at age 25 to about 0.20 at 75, predicts entirely held-out
participants in 20 of 20 cross-validation repetitions, and fails one
pre-specified predictive check among younger adults — a boundary the paper
reports as a result, not a footnote. Every value is conditional on the assumed
response rule (ε = 2α; there is a three-line proof of why). The manuscript is
drafted in `paper/`.

## The plan

Three studies, kept separate so their claims can't blur into one:

1. [Study 1A](docs/STUDY_1A.md) — can the explicit model reproduce the published human
   findings, fitting its parameter on part of the data and predicting the rest? No
   LLM involved anywhere. **Complete** — see the results sections in the study file.
2. [Study 1B](docs/STUDY_1B.md) — can an LLM parser feed the same model natural language
   without changing the outcome and without leaking information across the boundary?
   An engineering claim only.
3. [Study 1C](docs/STUDY_1C.md) — put end-to-end LLM listeners on the identical trials and
   compare. Written so that the LLMs are allowed to win; that result would be
   reported too.

## Running it

```
python tests/test_core.py
python experiments/exp0_keysar_signature.py
python experiments/exp4_protocol.py --synthetic
```

Python 3.10 or newer. The core package has no dependencies; the analysis
scripts (exp2 onward) use numpy and scipy.

## Reading order

1. [V1.md](docs/V1.md) — the research specification
2. [MODEL_AUDIT.md](docs/MODEL_AUDIT.md) — where every equation comes from
3. [IDENTIFIABILITY.md](docs/IDENTIFIABILITY.md) — which measurements can tell which
   theories apart, and the experiment designed to do it
4. [STUDY_1A.md](docs/STUDY_1A.md) · [STUDY_1B.md](docs/STUDY_1B.md) ·
   [STUDY_1C.md](docs/STUDY_1C.md) — the three claims
5. [RELATED_WORK.md](docs/RELATED_WORK.md) — what already exists, and the narrow gap left
6. [PREREGISTRATION.md](PREREGISTRATION.md) — the frozen analysis protocol and its addenda
7. [READING_LIST.md](docs/READING_LIST.md) — the ten papers that come before any new code
8. [ARCHITECTURE.md](archive/ARCHITECTURE.md) — an archived early vision, kept as a quarry

## Where this came from

The repository's first life was a canvas game with three LLM-driven characters
(`reference/drift-lab-v3-1.html`). It looked alive and proved nothing: the language
model was inventing the psychology on the fly and grading its own homework. It stays
in the repo as the negative example the rule above exists to prevent.

## License

MIT.

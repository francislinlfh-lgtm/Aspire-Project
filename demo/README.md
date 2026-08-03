# The Common Room, revisited

The little people are back — this time with a validated mind.

Thirty-three simulated people, ages 20 to 84, each carrying an egocentric weight
`α_i` drawn from the **paper's fitted hierarchy** (the exact parameters of the
single protocol execution), face the candle task twelve times. Older people err
more, exactly as the fitted curve predicts — and the curve itself glows under
their feet. Click anyone to open their glass box: their `α`, its ε-dual reading
(shown only where the equivalence proposition licenses it), their trial record,
and the verbatim engine trace behind each choice.

**Architecture rules this demo lives by:**

- **Engine-computed, page-replayed.** Every cognitive event is produced by the
  canonical Python engine (`cogsim.listener.MixtureListener`) in
  `make_room.py`; `room.html` is a pure replay-and-inspection surface with no
  cognition in JavaScript and no LLM anywhere.
- **Honesty travels with the characters.** The page states on its face that α
  is conditional on the response rule, that ε = 2α holds only for α < .5, and
  that the room inherits the model's known failure — it under-produces
  single-slip young adults (predictive check T2). Simulated output, not human
  data.
- One instructive consequence of the fitted κ ≈ 1.4: occasional individuals
  draw extreme weights (an α ≈ .99 elder who errs every time). That is not a
  bug — it is what the fitted heterogeneity actually claims, made visible.

**Run it:** open `demo/room.html` in a browser. Regenerate a new population:

```bash
python demo/make_room.py --seed 42
```

Lineage note: this room is the descendant of `reference/drift-lab-v3-1.html`,
the project's original prompt-driven prototype — retired because its minds were
unfalsifiable. It took one audit, one frozen protocol, and one paper to earn
these thirty-three little people their explicit ones.

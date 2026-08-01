# Related Work and Positioning

**Purpose of this document.** Map the neighboring literature honestly, state what Aspire
does *not* claim, and locate the narrow gap it does claim. Every novelty claim here must
survive a hostile reviewer; when in doubt, the claim is stated weaker.

---

## 1. LLM-centered agent simulacra

**Generative Agents** (Park et al., 2023) put the LLM at the center: a memory stream of
natural-language records, retrieval by recency × importance × relevance, reflection and
planning via prompting. Evaluation is believability rating by human judges. The
architecture demonstrated that LLM agents *look* social; it cannot say *why* any behavior
occurred (the causal story is inside the model weights), and believability is not a
behavioral-fidelity criterion. Aspire inverts the placement of the LLM and replaces
believability with reproduction of published experimental signatures.

## 2. Conceptual frameworks for language agents

**CoALA** (Sumers, Yao, Narasimhan & Griffiths, 2023) organizes LLM agents using
cognitive-architecture vocabulary: working/long-term memory, internal vs. external
actions, a decision cycle. It is a design framework in which the LLM remains the
reasoning substrate. Aspire sits at the pole CoALA's taxonomy points at but does not
occupy: the decision cycle contains **no** LLM calls; the LLM is confined to the
perception/action boundary. We use CoALA's vocabulary where possible, as the field's
lingua franca.

## 3. Explicit-state augmentation of LLMs

**SymbolicToM** (Sclar et al., 2023) maintains explicit multi-level belief graphs outside
the language model to make theory-of-mind reading comprehension robust, showing that
explicit state outperforms implicit LLM state on ToMi. This is the closest spiritual
neighbor on the "externalize psychological state" axis. Differences: SymbolicToM is an
inference aid for answering questions about stories; it is not a process model of a human
participant, is not interactive, and is not evaluated against human behavioral dynamics.

## 4. Cognitive architectures with language — and Lindes & Skiker

The Soar lineage has integrated language with explicit cognition for decades: NL-Soar,
Lucia (Lindes & Laird — comprehension via Embodied Construction Grammar inside Soar),
and Rosie (interactive task learning). Recent work integrates LLMs as knowledge sources
for such agents (Kirk et al., 2023, 2024).

**Lindes & Skiker (2025), *Using Natural Language for Human-Robot Collaboration in the
Real World* ([arXiv:2508.11759](https://arxiv.org/abs/2508.11759))** is our primary
comparison paper. Their system: a **Soar** cognitive agent at the center; a physical
robot (AI2-Thor simulation) for perception/action; accumulated situational knowledge in
Soar's semantic/episodic/procedural memories; and an LLM with **three stated purposes**:
(1) translate language inputs to symbols, (2) **provide general and commonsense
knowledge**, (3) translate symbols to language outputs. The agent orchestrates, reasons,
learns incrementally, and *verifies LLM responses* against its situational knowledge
(and via human confirmation). Three proof-of-concept ChatGPT experiments: grounding
referring expressions given a category list + spatial neighbor graph; commonsense
storage-location retrieval; translating free-form recipes into a controlled-English step
sequence.

| Dimension | Lindes & Skiker | Aspire |
|---|---|---|
| Center | Soar agent (general architecture) | phenomenon-specific psycholinguistic model |
| Goal | capable robot assistant (engineering) | reproduce human behavior *including its errors* (science) |
| LLM roles | parse in, render out, **plus commonsense knowledge source**; in their Exp. 1 the LLM performs full referential resolution incl. spatial reasoning | parse in, render out, **nothing else**; reasoning and knowledge injection forbidden; a closed experimental world removes the need for commonsense |
| LLM verification | consistency-check against situational knowledge; ask the human | round-trip semantic-fidelity audit with a reported leakage metric |
| Evaluation | proof-of-concept accuracy (does the system get the referent right?) | behavioral fidelity (does the model get the referent right *and wrong* the way humans do?) |
| Misunderstanding | an engineering failure to minimize | the object of study to reproduce |

Two further points of contact. First, they describe two options for referential
grounding — the LLM resolves fully, or the LLM emits a formal representation "suitable
for symbolic resolution by the cognitive agent" — and experiment only with the former.
Aspire's parser contract is a commitment to the latter branch, taken not for engineering
reasons but because a sealed boundary is what makes the cognition measurable. Second,
their closing argument — that orchestration is the hardest problem for "agentic LLMs"
and that cognitive-architecture research is where solutions live — is an argument we
inherit and radicalize: we remove the LLM from the decision cycle entirely, which is
only possible because our worlds are closed experimental paradigms rather than kitchens.

**The architectures are siblings; the epistemic goals are orthogonal.**

## 5. Computational theories of dialogue and grounding

Explicit dialogue-state tracking is old, mature engineering, and we claim no novelty in
it: Traum's computational theory of grounding (1994), Poesio & Traum's update semantics,
the Information State approach (Larsson & Traum, 2000), and the clarification-request
literature (Purver; Ginzburg, *The Interactive Stance*; Schlangen) already give explicit
common-ground machinery with grounding acts and CR taxonomies. What that tradition did
not do is evaluate the machinery *as a psychological model* against human behavioral
signatures — systems were evaluated as artifacts (task success, dialogue efficiency).
That evaluation gap, not the machinery, is where Aspire works.

## 6. Computational psycholinguistics

The closest methodological kin, and the literature V1 actually contributes to:

- **Rational Speech Acts** (Frank & Goodman, 2012, and descendants): probabilistic
  pragmatics quantitatively fit to human data — the model for the kind of science we
  want. RSA is predominantly one-shot and offline; multi-turn interactive settings,
  persistent divergence between interlocutors, and clarification decisions are largely
  outside its current practice.
- **Perspective-taking in reference resolution — a live controversy.** Keysar and
  colleagues' egocentric-anchoring account (Keysar, Barr, Balin & Brauner, 2000:
  interference from listener-privileged competitors in the director task) vs.
  early-integration constraint-based accounts (Hanna, Tanenhaus & Trueswell, 2003;
  Brown-Schmidt) vs. **graded probabilistic accounts — Heller, Parisien & Stevenson
  (2016)**, whose Eq. (2) combines Bayesian reference resolution under egocentric and
  common-ground domains with a weight α. **Aspire V1's mixture listener is a
  choice-level projection of Heller et al.'s model** (divergences confessed in
  MODEL_AUDIT §1.3; their α convention adopted project-wide 2026-08-02) — we claim
  the embedding and the fitting, not
  the model. **Verified against their full text (2026-08-01): they varied α from 0
  to 1 and argued from qualitative patterns; α was never fitted to data, no serial
  model was implemented, and no likelihood-based model comparison or held-out
  prediction was performed.** Study 1A's hierarchical trial-level fitting with
  fit-then-predict therefore does what the source paper explicitly did not. Note also that the director task's construct validity is itself contested
  (Rubio-Fernández, 2017: ToM use or selective attention?) — an instrument that can
  implement *both* accounts as competing policies is a contribution to precisely this
  dispute.
- **The weighting parameter's quantitative history (mapped 2026-08-01, systematic
  search).** Three neighbors, none occupying the gap:
  (i) **Mozuraitis, Stevenson & Heller (2016 CogSci; 2018 *Cognitive Science*)** —
  the *production* side: they reformulate Heller's α as a domain probability P(d)
  by marginalization and, in their words, "determine the range of values of P(d)
  that yields a fit to the empirical data" — a range determination against
  condition-level production proportions; no trial-level likelihood estimation, no
  participant hierarchy, no age, no held-out prediction. Verified against their
  CogSci text.
  (ii) **Rubio-Fernández & Jara-Ettinger (2018 CogSci)** — a joint-inference model
  (referent + speaker knowledge + expression preference) for the director task,
  evaluated against *offline human judgments* by model comparison; common ground is
  *inferred*, not weighted; no weight fitting, no age.
  (iii) **Hawkins et al. (2021, Cognitive Science)** — RSA models of perspective
  asymmetries in matcher games, with fitted RSA parameters; different paradigm and
  parameters, no age, not Heller's mixture.
  No computational-model reanalysis of Bradford et al.'s (2023) dataset was found,
  and no fitted perspective-weight model across age in any paradigm.
- **The precise surviving gap (manuscript ¶3 wording):** trial-level
  maximum-likelihood estimation of the *comprehension-side* mixture weight, with a
  participant hierarchy, **as a function of age**, evaluated by held-out
  participant prediction under a frozen public protocol — no prior study found.
  The loose claim "no one has quantified the weight" is false (Mozuraitis) and is
  banned from all drafts.
- **Good-enough processing** (Ferreira et al.): underspecified interpretation as the
  default — background support for treating "assume without clarifying" as the human
  baseline rather than a failure.

## 7. Appraisal architectures

FAtiMA and EMA (Dias & Paiva; Gratch & Marsella) operationalized appraisal theory as
executable mechanisms two decades ago — proof that the "explicit cognition, validated
constructs" tradition exists and works. We defer the affective domain entirely (see
roadmap) and cite this line as precedent, not as competition.

## 8. LLMs as psychological subjects

A growing literature administers psychology experiments to LLMs: false-belief batteries
(Kosinski; Trott et al.; Ullman's fragility critiques), and — directly on our paradigm —
**the director task has already been adapted to multimodal LLMs**
([Visuospatial Perspective Taking in Multimodal Language Models, 2026](https://arxiv.org/html/2603.23510)),
reporting pronounced Level-2 perspective-taking deficits. Therefore Aspire's LLM
benchmark arm is **not** "first to test LLMs on the director task." Our benchmark claim
is narrower and different in kind: a *within-instrument* comparison, on identical trials
and identical dependent variables, between an explicit mechanistic listener and
LLM-centered listeners — evaluating trajectory-level behavioral fidelity, not accuracy.

## 9. The gap Aspire claims — stated narrowly

Each ingredient exists somewhere. We claim the **intersection** is unoccupied:

1. cognition computed entirely outside the LLM (§4's untaken branch, sealed rather than
   porous), **and**
2. an interactive, multi-turn referential-communication setting, **and**
3. evaluation by reproduction of published human behavioral signatures under a
   fit-then-predict protocol, **and**
4. direct behavioral comparison against LLM-centered listeners inside the same
   instrument.

And we explicitly do **not** claim: the first explicit-state language agent (§3, §5),
the first cognition-centered LLM integration (§4), the first probabilistic
perspective-taking model (§6 — Heller et al. got there in 2016), or the first LLM
director-task evaluation (§8). The contribution, if we earn it, is the **instrument**:
psychological theories of perspective use and clarification, operationalized as
swappable executable policies, adjudicated against human data.

*Verification debt: before any submission, this document's "unoccupied intersection"
claim needs a systematic search pass (Semantic Scholar / Google Scholar), not just the
spot-checks done so far.*

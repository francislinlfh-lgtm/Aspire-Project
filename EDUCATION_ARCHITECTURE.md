# Education Edition — Architecture

**Status: design document, rev. 2 (after external review). No production lesson code
exists, deliberately.**

**Governing principle:** *the research platform determines what Aspire can honestly
simulate; the education platform determines how those validated capabilities are
taught.* Never the reverse. A compelling lesson interaction is not a reason to bend
the engine, and the current model is not a doctrine for the product to enshrine.

The Aspire Project splits into two products sharing one engine:

- **Research Edition** — the canonical version: the cognitive engine, experimental
  framework, model implementations, and evaluation pipeline. Everything in V1.md.
- **Education Edition** — an interactive learning platform (initially AP® Psychology,
  later introductory university courses) built *on top of* the engine, never *into* it.

This document specifies how the second product exists without ever touching the first.

---

## 1. The prime directive and its laws

The educational layer is a **client** of the research engine. Not a fork, not a copy,
not a "simplified version." One engine, two products.

Six laws, each enforceable, most enforceable by CI:

- **L1.** Education code imports `cogsim.api` and nothing else from the engine.
  (CI: an import check on `education/`.)
- **L2.** The engine never imports anything from `education/`. (CI: same check,
  reversed.)
- **L3.** An educational need becomes an engine change only if it also serves the
  research instrument. Otherwise education adapts on its side of the boundary.
- **L4.** Pedagogy lives in overlay files that reference engine artifacts by id.
  Engine files contain zero pedagogy — no student-facing names, no lesson hints, no
  difficulty ratings.
- **L5.** Teaching scenarios are instances of the engine's scenario schema. There is
  no separate "education scenario format," ever. The day one exists, duplication has
  begun.
- **L6.** Every student-facing simulation output is labeled as simulated, and model
  provenance labels ([LIT]/[ADAPT]/[PROV]) survive into the classroom. The Education
  Edition inherits the project's honesty rules; it does not get to teach the mixture
  model as settled fact while MODEL_AUDIT.md says otherwise.

Why this matters (restating the requirement as consequences): engine improvements
reach students with zero education-side work; educational deadlines can never push
hacks into research code; and the education edition's content is data — reviewable,
versionable, and rewritable without touching cognition.

## 2. Directory structure

Monorepo for now (one developer, synchronized versions, one CI). The boundary is
enforced by law, not by repo separation; a future repo split becomes cheap precisely
because the boundary is clean.

```
Aspire-Project/
├── cogsim/                      # THE ENGINE — Research Edition core (canonical)
│   ├── api.py                   # planned: the sole client-facing surface (semver)
│   ├── scenarios.py             # planned: declarative scenario schema + loader
│   ├── registry.py              # planned: model descriptors (id, params, provenance)
│   └── world.py · language.py · listener.py · clarify.py · experiment.py  # existing
├── scenarios/                   # engine-format scenario DATA
│   ├── research/                # dataset-matched stimuli (Study 1A requires these)
│   └── teaching/                # educational instances — same schema (L5)
├── experiments/                 # research scripts (unchanged)
├── tests/                       # engine tests + API contract tests
├── education/                   # EDUCATION EDITION — a client, nothing more
│   ├── concepts/                # concept registry (data): stable ids for constructs
│   ├── curricula/
│   │   └── ap-psychology-2024/  # data pack: units → topics → concept ids + status
│   ├── lessons/                 # lesson definitions (data; six-phase schema, §6)
│   ├── overlays/                # presentation metadata keyed by engine ids (L4)
│   ├── player/                  # lesson runtime — imports cogsim.api ONLY (L1)
│   ├── explain/                 # trace → explanation templates
│   ├── assess/                  # prediction capture, quiz schema, scoring
│   ├── ui/                      # web frontend (last; thin; talks only to player)
│   └── tests/                   # education tests (call the real API; no mocks needed)
└── *.md                         # research documents (unchanged)
```

## 3. Module responsibilities

| Module | Owns | Never does |
|---|---|---|
| `cogsim/` (engine) | cognition, scenario semantics, simulation, traces, model registry | pedagogy, presentation, curriculum awareness |
| `cogsim/api.py` | the stable contract: versions, model listing, scenario loading, `run()` | expose internals; change without a version bump |
| `scenarios/` | ground-truth trial definitions in the engine's schema | carry teaching narration or visuals (that's `overlays/`) |
| `education/concepts/` | curriculum-neutral concept registry — the join key of the whole system | reference any curriculum |
| `education/curricula/` | per-curriculum data packs mapping standards → concepts, with coverage status | contain lessons or engine references directly |
| `education/lessons/` | six-phase lesson definitions referencing concepts, scenarios, overlays by id | embed engine logic or inline scenario definitions |
| `education/player/` | lesson state machine, engine calls, prediction/response capture | interpret cognition; modify anything |
| `education/explain/` | translating structured traces into student-readable explanations | generate claims not derivable from the trace |
| `education/assess/` | scoring predictions against simulation outcomes; quizzes | grade anything the player didn't record |
| `education/ui/` | rendering and interaction | contain lesson logic (player owns it) |

## 4. The engine interface

Everything education may touch, in one module:

```python
# cogsim/api.py  (planned — the contract, not yet built)
ENGINE_VERSION: str            # semver; breaking change = major bump
SCENARIO_SCHEMA_VERSION: str
TRACE_SCHEMA_VERSION: str

list_models() -> list[ModelDescriptor]
    # id, human-neutral name, parameters (name, range, meaning),
    # provenance label ([LIT]/[ADAPT]/[PROV]), citations

load_scenario(source: str | dict) -> Scenario     # validated against schema version

run(scenario, model_id, params, seed, n_trials) -> RunResult
    # RunResult is plain-data / JSON-serializable:
    #   per trial: display, instruction frame, posterior, choice, provenance trace
    #   aggregate: the DV set experiment.py already defines
```

Contract properties, decided now:

1. **Semver with a deprecation policy.** Education pins a compatible range
   (`>=0.x,<0.y`); API contract tests live in the *engine's* test suite, so breaking
   the contract breaks research CI, not just the client.
2. **Results are data, not objects.** JSON-serializable end to end, so any frontend
   (CLI, notebook, web, WASM) consumes them without importing engine classes.
3. **Traces are part of the contract.** The provenance trace is already a research
   constitution requirement; education's explanation layer is purely a consumer of
   it. If a lesson can't explain something, the fix is a richer trace schema
   (research-legitimate under L3), never education-side reconstruction of cognition.

## 5. The scenario system

The engine owes itself — for Study 1A, independent of education — a set of **neutral
capabilities**: scenario loading, state initialization, controlled interventions,
simulation execution, trace extraction, result serialization (MODEL_AUDIT §4.3).
Education consumes those primitives. But sharing primitives is not sharing a product:
a research stimulus builder and a classroom scenario-authoring experience are
different tools that happen to emit the same schema. Classroom concepts — difficulty,
hints, misconception tags, prediction prompts, reflection prompts, teacher notes,
curriculum standards — never enter the engine, its schema, or its API. They live in
education-side files that reference engine artifacts by id.

```yaml
# scenarios/teaching/candles-basic.yaml   (engine schema; no pedagogy)
id: teaching/candles-basic
schema_version: 1
display:
  objects:
    - {oid: c1, category: candle, size: 1, mutually_visible: false}
    - {oid: c2, category: candle, size: 2, mutually_visible: true}
    - {oid: c3, category: candle, size: 3, mutually_visible: true}
    - {oid: f1, category: truck,  size: 2, mutually_visible: true}
instruction: {category: candle, scalar: smallest}
conditions: [critical]
```

```yaml
# education/overlays/candles-basic.yaml   (education-owned; references by id)
for: teaching/candles-basic
title: "The Hidden Candle"
narration: "You can see into every slot. Your partner can't..."
art: {candle: candle.svg, truck: truck.svg}
```

Demonstrating a new concept means writing a new scenario file and overlay — data —
plus, at most, a request for an engine feature that research also wants. The engine's
schema validator is the wall: if a scenario needs a field the schema doesn't have,
that's an engine design conversation, not a quiet education-side extension.

## 6. Lesson architecture

A lesson is a declarative sequence of typed phases, executed by a generic player.
The six-phase spine is the pedagogy pattern known as predict–observe–explain, plus
framing on both ends:

```yaml
id: ap-psych/egocentrism-01
version: 1
concept: perspective-taking.egocentric-interference
engine: {compatible: ">=0.1,<0.2"}
phases:
  - type: concept       # what perspective-taking is; content ref, no simulation
  - type: scenario      # present the situation (scenario_ref + overlay_ref)
  - type: prediction    # BEFORE running: "which candle will people reach for,
                        #  and how often?" — captured, not graded yet
  - type: simulation    # model_id: P-MIX; seed fixed; w student-adjustable [0,1]
  - type: explanation   # template over the traces + the gap between the student's
                        #  prediction and the outcome
  - type: reflection    # transfer prompts, quiz_ref, "when did this happen to you?"
```

Design decisions inside this:

- **Phases are a typed, extensible registry.** Adding a phase type (e.g., a
  `compare-models` phase where students run P-EGO vs P-CG vs P-MIX on the same
  scenario) is a player extension, no lesson-format migration.
- **Lessons are organized around psychological questions, not model parameters.**
  The unit of design is a question a student can hold — "what does your partner
  think you can see?" — never "adjust parameter w." Parameter exploration is one
  optional interaction pattern inside individual lessons, and wherever a model
  appears it is labeled as one proposed account. Empirical claims (e.g., that
  neither pure egocentrism nor pure common-ground restriction matches human
  behavior) may be taught from the published literature, with citations; they may
  not be demonstrated *from this engine's output* until Study 1A validates the
  simulation under the relevant conditions.
- **Prediction before simulation is mandatory in the schema** — the player refuses
  to run a simulation phase if no prediction was captured. Commitment before
  evidence is the whole pedagogical (and scientific) point.
- **Determinism is a feature.** Seeds live in the lesson file: every student sees the
  same run, classes can discuss one shared outcome, and re-running is an explicit
  "new sample" act — itself a teachable moment about sampling variability.
- **No LLM anywhere in the lesson path.** Explanations are templates over traces. If
  a conversational tutor is ever added, it inherits the firewall: an LLM may render
  a trace into friendlier words; it may never generate claims about what the model
  did. Same rule as the research edition, same reason.

## 7. Mapping AP® Psychology onto the engine

The 2024 CED: five units (1 Biological Bases, 2 Cognition, 3 Development and
Learning, 4 Social Psychology and Personality, 5 Mental and Physical Health) crossed
with four science practices (1 Concept Application, 2 Research Methods and Design,
3 Data Interpretation, 4 Argumentation).

**The mapping is data, not code, and every entry must carry evidence.** Conceptual
relatedness is not teachability: the director task illustrates a *narrow component*
of broad learning objectives like "cognitive development" or "person perception," and
the registry says exactly which component and what it does not cover. Each entry in
`education/curricula/ap-psychology-2024/coverage.yaml` is required to fill six
fields:

| Field | Content |
|---|---|
| Curriculum objective | the CED topic or science practice, verbatim |
| Psychological phenomenon | the specific, citable effect Aspire can stage |
| Engine capability | what the engine actually runs today (named modules/DVs) |
| Evidence base | the published studies anchoring any truth-claim in a lesson |
| Educational interaction | how a student engages it (predict–observe–explain, etc.) |
| Readiness | see enum below — plus an explicit statement of what is NOT covered |

Readiness levels (an enum, not a mood):

- `instrument-ready` — teachable through the instrument's methodology itself
  (research design, data interpretation, argumentation), independent of any model's
  validity.
- `phenomenon-ready` — the engine can stage the paradigm AND published human data
  anchors the empirical claims; the model appears only as "one proposed account."
- `model-gated` — any claim about the model's *correctness* waits for Study 1A.
- `roadmap-Vn` — requires engine constructs that do not exist yet.
- `out-of-scope` — will not be simulated; the registry says so aloud (Units 1
  and 5), so the product never half-promises neuroscience it will never model.

The research ladder still doubles as the content pipeline — each validated version
flips registry entries forward — but a registry entry is a claim, and claims carry
citations here like everywhere else in this project.

**The strongest current fit is not a topic at all — it's the science practices.**
Practices 2, 3, and 4 (research design, data interpretation, argumentation) are what
the instrument does natively: students formulate a hypothesis, design conditions
(critical vs control), read DV tables, and argue about which model the data support.
A lesson built on one Tier A topic can carry practice-level standards across the
whole course. Where topic coverage is thin, practice coverage is total — lead with
that in any pitch to teachers.

## 8. Adding curricula without rot

- **Concepts are the join key.** The concept registry is the system's interior
  vocabulary; curricula are exterior labelings of it. Adding university cognitive
  psychology = a new data pack mapping that syllabus onto existing concept ids
  (plus requests for new ones). Zero code.
- **Lessons are curriculum-neutral.** A lesson teaches a *concept*; curricula claim
  lessons via the registry. The egocentrism lesson serves AP Psych 3.4, a cognitive
  psych survey week, and a developmental course, unmodified.
- **Lessons are executable, so lessons are tests.** CI runs every lesson's simulation
  phases headlessly and checks their qualitative signatures (interference present on
  critical trials, absent on control). An engine change that would silently break a
  classroom demo breaks the build instead. The education edition becomes a
  regression suite the research edition gets for free — the dependency, made mutual.
- **Versioning discipline:** lessons pin an engine semver range and schema versions;
  ids are never reused; content strings live in locale-keyed files from day one
  (localization is cheap now, a rewrite later).

## 9. Decisions to make now (to avoid refactoring later)

1. **Build `api.py` before any education code exists.** The moment a second client
   imports engine internals, those internals are frozen de facto. Freeze
   deliberately instead, at a surface you chose.
2. **Scenario schema goes in the engine, built when Study 1A needs it** (it does —
   dataset-matched stimuli). This is the single shared investment; do not let
   education build its own.
3. **Settle the name before the facade — but the gate is identity, not imports.**
   Renaming `cogsim` → `aspire` is cheapest now and stays feasible later
   (compatibility aliases, staged deprecation); "now or never" would be
   overstatement. The real question is whether *Aspire* is confirmed as the durable
   technical name — for the package, schemas, CLI, and saved artifacts. Until that
   is decided deliberately, the package stays `cogsim` and `api.py` ships under it.
4. **CI directionality checks from the first education commit** (L1/L2). Trivial to
   add now, culturally impossible to retrofit.
5. **Keep the simulation kernel lightweight; let research take dependencies.** The
   right structure is a split, not an ideology: a browser-compatible simulation
   kernel (currently stdlib-only, and worth keeping dependency-light) that education
   depends on exclusively, plus optional research extras — numerical computation,
   optimization, statistical inference, parameter fitting — that Study 1A will
   likely need and must never be blocked from taking. The kernel/extras boundary
   preserves the WASM/static-site path: the Education Edition can run entirely
   client-side — no servers, no accounts, no student data collected by default.
   For a product aimed at minors in schools, "no data leaves the browser" is the
   privacy architecture (COPPA/FERPA exposure designed out, not complied with).
6. **Concept ids before the first lesson.** Renaming the join key after ten lessons
   reference it is the refactor this document exists to prevent.
7. **Trademark hygiene.** "AP" is a College Board registered trademark. The product
   may describe alignment ("aligned to AP® Psychology topics," with the standard
   non-affiliation disclaimer); it must not carry AP in its name.
8. **Player before UI.** The lesson runtime ships first as a headless library with a
   CLI runner; the web frontend comes last and stays thin. UI is the highest-churn
   layer — keep lesson logic out of it.
9. **License split.** Code stays MIT; decide the lesson-content license (CC BY vs
   CC BY-NC) before any outside contributor writes a lesson.

## 10. Sequencing (the supervisor's paragraph)

The Education Edition costs the research year almost nothing if, and only if, it
stays in this document for now. The only near-term builds it implies — the API
facade and the scenario schema — are things Study 1A requires anyway. Lesson
authoring should gate on Study 1A's fit-then-predict passing, for an honest reason:
lessons will present the mixture model to students, and until 1A runs, the project's
own audit says that model is an unverified adaptation. Teach the phenomenon the day
the data is real; teach the model the day it survives contact with human data. The
registry's `roadmap` statuses make that patience visible instead of vague.

## 11. Authorized scope (current)

Per review, only these pieces exist or may be built now — everything else waits for
Study 1A stability:

1. This document (rev. 2). ✔
2. **API contract draft** — `API_CONTRACT.md`, a specification (not an
   implementation); `api.py` is built later, alongside the scenario schema work
   Study 1A requires.
3. **Coverage registry** — `education/curricula/ap-psychology-2024/coverage.yaml`
   with the six evidence/readiness fields of §7.
4. **One example lesson specification** — `education/lessons/examples/`, running on
   *mocked* simulation output, to test whether the lesson schema is pedagogically
   usable without tying it to an unvalidated model.
5. **CI boundary rules** — `tests/test_boundaries.py` + workflow, enforcing L1/L2
   from the first education commit.
6. **No production lesson code.** No player, no UI, no authored curriculum content.

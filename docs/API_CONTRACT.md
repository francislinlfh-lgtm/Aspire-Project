# Engine API Contract — DRAFT specification

**Status: specification only. `cogsim/api.py` does not exist yet** — it gets built
alongside the declarative scenario schema when Study 1A needs it (EDUCATION_ARCHITECTURE.md
§11.2). This document exists so that when it is built, the surface is one that was
*chosen*, not one that leaked.

Consumers: the future education player, research notebooks, the CLI, any web frontend.
All of them get exactly this and nothing more.

## 1. Stability rules

1. `ENGINE_VERSION` follows semver. Breaking this contract = major bump.
2. Three versioned surfaces, independently: engine (`ENGINE_VERSION`), scenario
   format (`SCENARIO_SCHEMA_VERSION`), trace format (`TRACE_SCHEMA_VERSION`).
3. Deprecations survive at least one minor version with a warning before removal.
4. Contract tests live in the **engine's** test suite (`tests/`): breaking the
   contract breaks research CI, not just the clients.
5. Everything crossing the boundary is plain data (JSON-serializable). No client
   ever imports an engine class other than through `cogsim.api`.

## 2. Operations

```python
# cogsim/api.py — the entire client-facing surface

ENGINE_VERSION: str
SCENARIO_SCHEMA_VERSION: str
TRACE_SCHEMA_VERSION: str

def engine_info() -> dict
    # versions, available schema versions, build metadata

def list_models() -> list[dict]          # ModelDescriptor, §3.1
def describe_model(model_id: str) -> dict

def load_scenario(source: str | dict) -> dict   # validated Scenario, §3.2
def validate_scenario(source: dict) -> list[str]  # [] if valid, else messages

def run(scenario: str | dict,            # scenario id or inline definition
        model_id: str,
        params: dict,                    # validated against the descriptor
        seed: int,
        n_trials: int) -> dict           # RunResult, §3.3
```

## 3. Types (shapes, language-neutral)

### 3.1 ModelDescriptor

```json
{
  "id": "mixture-listener",
  "params": [
    {"name": "alpha", "range": [0.0, 1.0],
     "meaning": "weight of the egocentric domain (Heller et al. 2016 convention)"}
  ],
  "provenance_label": "ADAPT",
  "citations": ["Heller, Parisien & Stevenson (2016), Cognition"]
}
```

Provenance labels ([LIT]/[ADAPT]/[PROV], per MODEL_AUDIT.md) are part of the
contract: clients are *required to be able to know* the epistemic status of what
they are running. Names here are technical ids; student-facing names are a client
concern (overlays), not an API field.

### 3.2 Scenario

The declarative scenario format (EDUCATION_ARCHITECTURE.md §5): id, schema_version,
display (objects with category/size/mutual visibility), instruction frame,
conditions. Owned by the engine; shared verbatim by research stimuli and teaching
scenarios.

### 3.3 RunResult

```json
{
  "engine_version": "…", "trace_schema_version": "…",
  "scenario_id": "…", "model_id": "…", "params": {…},
  "seed": 7, "n_trials": 200,
  "aggregates": {
    "<condition>": {"intended_accuracy": 0.0, "egocentric_error_rate": 0.0,
                     "competitor_consideration": 0.0, "clarify_rate": 0.0}
  },
  "trials": [
    {"condition": "…", "choice": "…", "posterior": {"oid": 0.0},
     "trace": [["step", "detail"], …]}
  ]
}
```

The trace is contractual: it is the raw material for every downstream explanation.
If a client cannot explain something from the trace, the remedy is a richer trace
schema (a legitimate engine change under L3) — never client-side reconstruction of
cognition.

## 4. Errors

Typed, minimal taxonomy: `UnknownModelError`, `InvalidParamsError` (with the
violated descriptor field), `ScenarioValidationError` (with messages),
`SchemaVersionError` (client/engine mismatch). No engine stack internals leak
through error payloads.

## 5. Neutrality clause (what will never be in this API)

Difficulty ratings, hints, prediction prompts, misconception tags, reflection
prompts, teacher notes, curriculum identifiers, student-facing names, presentation
metadata of any kind. Requests to add such fields are, by definition, education-side
overlay work (L4). This clause is the contract's half of the governing principle.

## 6. Open questions (deliberately unresolved)

- Batch/sweep interface (`run_many`) — probably wanted by both research and
  education; design when the first real consumer exists.
- Progress/streaming for long runs — not needed at current engine speeds; revisit
  only with evidence.
- Whether `api.py` exposes the clarification-policy hook — undecided until RQ4
  (V1.md) has any validated content to expose.

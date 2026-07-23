# Education Edition — data only, deliberately

Nothing in this directory is executable, and that is the design, not an accident.
Per [EDUCATION_ARCHITECTURE.md](../EDUCATION_ARCHITECTURE.md) §10–11, production
lesson code (player, UI, authored curriculum) is gated on Study 1A stability.

What exists now:

- `curricula/ap-psychology-2024/coverage.yaml` — the coverage registry: every
  curriculum mapping is a claim with evidence and an honest readiness level.
- `lessons/examples/` — one example lesson specification running on mocked
  simulation output, testing whether the six-phase schema is pedagogically usable
  without depending on an unvalidated model.

Boundary laws L1/L2 (education imports only `cogsim.api`; the engine never imports
education) are enforced by `tests/test_boundaries.py` from this commit forward.

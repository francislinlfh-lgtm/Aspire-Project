"""Trial batteries and dependent variables for the director task. Deterministic.

Dependent variables per condition (critical / control):
  intended_accuracy         P(select the director-intended referent)
  egocentric_error_rate     P(select the privileged competitor)      [critical only]
  competitor_consideration  mean posterior mass on the privileged competitor
                            (linking hypothesis for interference; V1.md §4.3)
  clarify_rate              fraction of trials the policy clarified  [exploratory]
"""
import random
from dataclasses import dataclass

from .world import critical_display, control_display
from .language import scripted_instruction, privileged_competitor
from .clarify import NeverClarify, ASSUME


@dataclass(frozen=True)
class ConditionResult:
    condition: str
    n: int
    intended_accuracy: float
    egocentric_error_rate: float
    competitor_consideration: float
    clarify_rate: float


def run_condition(listener, condition: str, n_trials: int, seed: int,
                  clarification=None) -> ConditionResult:
    clarification = clarification or NeverClarify()
    rng = random.Random(seed)
    make = critical_display if condition == "critical" else control_display

    hits = ego_errors = clarifies = 0
    consideration = 0.0
    for _ in range(n_trials):
        display = make()
        instr = scripted_instruction(display)
        interp = listener.interpret(display, instr.frame)

        priv = privileged_competitor(display, instr.frame)
        if priv is not None:
            consideration += interp.mass_on(priv)

        if clarification.decide(interp) != ASSUME:
            clarifies += 1
            continue  # exploratory runs: a clarified trial ends without a selection

        choice = interp.sample(rng)
        if choice == instr.intended_oid:
            hits += 1
        if priv is not None and choice == priv:
            ego_errors += 1

    answered = n_trials - clarifies
    return ConditionResult(
        condition=condition,
        n=n_trials,
        intended_accuracy=hits / answered if answered else 0.0,
        egocentric_error_rate=ego_errors / answered if answered else 0.0,
        competitor_consideration=consideration / n_trials,
        clarify_rate=clarifies / n_trials,
    )


def run_battery(listener, n_trials: int = 200, seed: int = 7, clarification=None):
    """Both conditions with derived, non-overlapping seeds."""
    return (
        run_condition(listener, "critical", n_trials, seed, clarification),
        run_condition(listener, "control", n_trials, seed + 1, clarification),
    )

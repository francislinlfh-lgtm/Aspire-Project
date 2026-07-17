"""Clarification: an OPEN research question, not an implemented mechanism.

V1.md §6.1 — hypothesis: the listener's decision among {assume, clarify, wait} depends
on interpretation uncertainty, the cost of acting on a misunderstanding, and the cost
of clarifying. No mathematical form is committed until the literature review (V2)
justifies one. This module therefore ships an interface and a null default only.

Anything other than NeverClarify is EXPLORATORY: usable in simulations to probe the
instrument, never citable as a claim of the model.
"""

ASSUME = "assume"
CLARIFY = "clarify"


class NeverClarify:
    """V1 default: always assume. Matches the good-enough-processing baseline reading
    (Ferreira) that unproblematic-seeming interpretation proceeds without repair."""

    def decide(self, interpretation) -> str:
        return ASSUME


class ExploratoryEntropyThreshold:
    """EXPLORATORY STUB — not a claim. A fixed uncertainty threshold is one of three
    candidate formalizations listed in V1.md §6.1; adopting it without literature
    support was the exact mistake retracted in V1.md §2.2."""

    def __init__(self, tau: float):
        self.tau = tau

    def decide(self, interpretation) -> str:
        return CLARIFY if interpretation.entropy() > self.tau else ASSUME

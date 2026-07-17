"""Listener models as swappable policies. Provenance and labels: MODEL_AUDIT.md §1.

Post-audit status: P-MIX is the primary account ([ADAPT] from Heller et al. 2016);
P-EGO and P-CG are reference limits (w=0, w=1), not competing accounts; P-ANCHOR is
retained solely as the identifiability exhibit (MODEL_AUDIT.md §1.4).

Each policy maps (display, frame) -> Interpretation: a posterior over candidate
referents plus a provenance trace. Candidate enumeration and all weighting happen
here, in cognition — never in a language model.

Linking assumptions (V1.md §4.3): selection samples from the posterior (a linking
assumption in itself); posterior mass on the privileged competitor is the model
analogue of interference measures, flagged as a linking hypothesis, not an identity.
"""
import math
from dataclasses import dataclass

from .world import Display, best_match
from .language import ReferringFrame


@dataclass(frozen=True)
class Interpretation:
    posterior: dict          # oid -> probability
    trace: tuple             # ((step, detail), ...) provenance, glass-box requirement

    def map_referent(self) -> str:
        return max(self.posterior.items(), key=lambda kv: (kv[1], kv[0]))[0]

    def mass_on(self, oid) -> float:
        return self.posterior.get(oid, 0.0)

    def entropy(self) -> float:
        return -sum(p * math.log2(p) for p in self.posterior.values() if p > 0)

    def sample(self, rng) -> str:
        r, acc = rng.random(), 0.0
        items = sorted(self.posterior.items())          # deterministic iteration order
        for oid, p in items:
            acc += p
            if r < acc:
                return oid
        return items[-1][0]


def _domains(display: Display, frame: ReferringFrame):
    """Candidate domains: egocentric (all the listener sees) and common-ground
    (mutually visible). Category matching only — graded salience is deferred
    (V1.md §6.4)."""
    ego = [o for o in display.objects if o.category == frame.category]
    cg = [o for o in ego if o.mutually_visible]
    return ego, cg


class EgocentricListener:
    """P-EGO: resolve in the egocentric domain. Baseline, not a serious theory of
    adults — Keysar's own account is anchor-and-adjust, not pure egocentrism."""

    def interpret(self, display, frame) -> Interpretation:
        ego, _ = _domains(display, frame)
        pick = best_match(ego, frame.scalar)
        trace = (("ego_domain", tuple(o.oid for o in ego)), ("ego_best", pick.oid))
        return Interpretation({pick.oid: 1.0}, trace)


class CommonGroundListener:
    """P-CG: full early integration — resolve in the common-ground domain only
    (the strong reading of constraint-based accounts, Hanna et al. 2003)."""

    def interpret(self, display, frame) -> Interpretation:
        _, cg = _domains(display, frame)
        pick = best_match(cg, frame.scalar)
        trace = (("cg_domain", tuple(o.oid for o in cg)), ("cg_best", pick.oid))
        return Interpretation({pick.oid: 1.0}, trace)


class MixtureListener:
    """P-MIX(w): probabilistic weighing of egocentric and common-ground domains.

    This is Heller, Parisien & Stevenson (2016), implemented — not our model.
    w = 0 reduces to P-EGO, w = 1 to P-CG.
    """

    def __init__(self, w: float):
        if not 0.0 <= w <= 1.0:
            raise ValueError("w must be in [0, 1]")
        self.w = w

    def interpret(self, display, frame) -> Interpretation:
        ego, cg = _domains(display, frame)
        ego_best, cg_best = best_match(ego, frame.scalar), best_match(cg, frame.scalar)
        posterior: dict = {}
        posterior[ego_best.oid] = posterior.get(ego_best.oid, 0.0) + (1.0 - self.w)
        posterior[cg_best.oid] = posterior.get(cg_best.oid, 0.0) + self.w
        trace = (("ego_best", ego_best.oid), ("cg_best", cg_best.oid), ("w", self.w))
        return Interpretation(posterior, trace)


class AnchorAdjustListener:
    """P-ANCHOR(p): egocentric anchor with probabilistic adjustment toward common
    ground — a choice-level gloss of Keysar-style anchoring-and-adjustment.

    RECLASSIFIED BY AUDIT (MODEL_AUDIT.md §1.4): this equation appears in no paper —
    it is our [PROV] invention, and it strips the serial theory's distinctive process
    content (effort, time course; Epley et al. 2004). With deterministic within-domain
    resolution it is choice-equivalent to MixtureListener(w=p) — proven in
    tests/test_core.py. It is therefore NOT a competing model in Study 1A; it exists
    as the standing identifiability exhibit (IDENTIFIABILITY.md, Prop. 1).
    """

    def __init__(self, p_adjust: float):
        if not 0.0 <= p_adjust <= 1.0:
            raise ValueError("p_adjust must be in [0, 1]")
        self.p_adjust = p_adjust

    def interpret(self, display, frame) -> Interpretation:
        ego, cg = _domains(display, frame)
        anchor, adjusted = best_match(ego, frame.scalar), best_match(cg, frame.scalar)
        posterior: dict = {}
        posterior[anchor.oid] = posterior.get(anchor.oid, 0.0) + (1.0 - self.p_adjust)
        posterior[adjusted.oid] = posterior.get(adjusted.oid, 0.0) + self.p_adjust
        trace = (("anchor", anchor.oid), ("adjusted", adjusted.oid),
                 ("p_adjust", self.p_adjust))
        return Interpretation(posterior, trace)

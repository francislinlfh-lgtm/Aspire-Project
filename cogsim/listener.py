"""Listener models as swappable policies. Provenance and labels: MODEL_AUDIT.md §1.

Parameter convention (adopted 2026-08-01, matching Heller, Parisien & Stevenson
2016, Eq. 2): **alpha weights the EGOCENTRIC domain** — alpha near 1 means
egocentric interpretation, alpha near 0 means common-ground interpretation.
(The project's former `w` was the complementary weight: w = 1 - alpha.)

Post-audit status: P-MIX is the primary account ([ADAPT] — a choice-level
projection of Heller et al.'s Eq. 2); P-EGO and P-CG are reference limits
(alpha=1, alpha=0), not competing accounts; P-ANCHOR is retained solely as the
identifiability exhibit (MODEL_AUDIT.md §1.4).
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
    """P-EGO: resolve in the egocentric domain — the alpha=1 limit. Baseline, not
    a serious theory of adults; Keysar's own account is anchor-and-adjust."""

    def interpret(self, display, frame) -> Interpretation:
        ego, _ = _domains(display, frame)
        pick = best_match(ego, frame.scalar)
        trace = (("ego_domain", tuple(o.oid for o in ego)), ("ego_best", pick.oid))
        return Interpretation({pick.oid: 1.0}, trace)


class CommonGroundListener:
    """P-CG: full early integration — resolve in the common-ground domain only;
    the alpha=0 limit (the strong reading of constraint-based accounts,
    Hanna et al. 2003)."""

    def interpret(self, display, frame) -> Interpretation:
        _, cg = _domains(display, frame)
        pick = best_match(cg, frame.scalar)
        trace = (("cg_domain", tuple(o.oid for o in cg)), ("cg_best", pick.oid))
        return Interpretation({pick.oid: 1.0}, trace)


class MixtureListener:
    """P-MIX(alpha): probabilistic weighing of egocentric and common-ground domains.

    Choice-level projection of Heller, Parisien & Stevenson (2016), Eq. 2 —
    their model, their alpha convention (alpha weights the egocentric domain);
    our simplifications are confessed in MODEL_AUDIT.md §1.3.
    alpha = 1 reduces to P-EGO, alpha = 0 to P-CG.
    """

    def __init__(self, alpha: float):
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be in [0, 1]")
        self.alpha = alpha

    def interpret(self, display, frame) -> Interpretation:
        ego, cg = _domains(display, frame)
        ego_best, cg_best = best_match(ego, frame.scalar), best_match(cg, frame.scalar)
        posterior: dict = {}
        for oid, mass in ((ego_best.oid, self.alpha), (cg_best.oid, 1.0 - self.alpha)):
            if mass > 0.0:
                posterior[oid] = posterior.get(oid, 0.0) + mass
        trace = (("ego_best", ego_best.oid), ("cg_best", cg_best.oid),
                 ("alpha", self.alpha))
        return Interpretation(posterior, trace)


class AnchorAdjustListener:
    """P-ANCHOR(p): egocentric anchor with probabilistic adjustment toward common
    ground — a choice-level gloss of Keysar-style anchoring-and-adjustment.

    RECLASSIFIED BY AUDIT (MODEL_AUDIT.md §1.4): this equation appears in no paper —
    it is our [PROV] invention, and it strips the serial theory's distinctive process
    content (effort, time course; Epley et al. 2004). With deterministic within-domain
    resolution it is choice-equivalent to MixtureListener(alpha = 1 - p) — proven in
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
        for oid, mass in ((anchor.oid, 1.0 - self.p_adjust),
                          (adjusted.oid, self.p_adjust)):
            if mass > 0.0:
                posterior[oid] = posterior.get(oid, 0.0) + mass
        trace = (("anchor", anchor.oid), ("adjusted", adjusted.oid),
                 ("p_adjust", self.p_adjust))
        return Interpretation(posterior, trace)

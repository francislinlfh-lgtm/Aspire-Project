"""Sanity tests for the V1 instrument. Run: python tests/test_core.py

Includes the identifiability proof of V1.md §4.2: P-MIX(w) and P-ANCHOR(p=w) are
choice-equivalent — the instrument demonstrating that two theories cannot be
separated by V1's dependent variables.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cogsim.world import critical_display, control_display, best_match
from cogsim.language import scripted_instruction, privileged_competitor, ReferringFrame
from cogsim.listener import (EgocentricListener, CommonGroundListener,
                             MixtureListener, AnchorAdjustListener)
from cogsim.experiment import run_battery, run_condition


def test_paradigm_structure():
    d = critical_display()
    instr = scripted_instruction(d)
    assert instr.intended_oid == "c2", "intended = smallest mutually visible"
    assert privileged_competitor(d, instr.frame) == "c1"
    c = control_display()
    instr_c = scripted_instruction(c)
    assert privileged_competitor(c, instr_c.frame) is None


def test_scalar_semantics():
    d = critical_display()
    pool = d.of_category("candle")
    assert best_match(pool, "smallest").oid == "c1"
    assert best_match(pool, "largest").oid == "c3"


def test_pure_policies():
    ego_crit, ego_ctrl = run_battery(EgocentricListener(), n_trials=100, seed=1)
    assert ego_crit.egocentric_error_rate == 1.0
    assert ego_crit.intended_accuracy == 0.0
    assert ego_ctrl.intended_accuracy == 1.0 and ego_ctrl.competitor_consideration == 0.0

    cg_crit, cg_ctrl = run_battery(CommonGroundListener(), n_trials=100, seed=1)
    assert cg_crit.intended_accuracy == 1.0
    assert cg_crit.competitor_consideration == 0.0
    assert cg_ctrl.intended_accuracy == 1.0


def test_mixture_grading_and_consideration():
    prev = 1.1
    for w in (0.0, 0.25, 0.5, 0.75, 1.0):
        crit, _ = run_battery(MixtureListener(w), n_trials=400, seed=3)
        assert abs(crit.competitor_consideration - (1.0 - w)) < 1e-9, \
            "consideration equals egocentric weight exactly (point domains)"
        assert crit.competitor_consideration < prev + 1e-9
        prev = crit.competitor_consideration


def test_mix_anchor_choice_equivalence():
    """The identifiability result: identical posteriors on every trial type."""
    frame_displays = [critical_display(), control_display()]
    for w in (0.0, 0.3, 0.5, 0.8, 1.0):
        mix, anchor = MixtureListener(w), AnchorAdjustListener(w)
        for d in frame_displays:
            f = scripted_instruction(d).frame
            pm, pa = mix.interpret(d, f).posterior, anchor.interpret(d, f).posterior
            assert set(pm) == set(pa)
            assert all(abs(pm[k] - pa[k]) < 1e-12 for k in pm), \
                "P-MIX and P-ANCHOR must be choice-equivalent (V1.md §4.2)"


def test_determinism():
    a = run_condition(MixtureListener(0.4), "critical", 200, seed=11)
    b = run_condition(MixtureListener(0.4), "critical", 200, seed=11)
    assert a == b, "same seed, same result — byte-identical replay"


def test_provenance_trace_present():
    d = critical_display()
    f = scripted_instruction(d).frame
    for listener in (EgocentricListener(), MixtureListener(0.5)):
        interp = listener.interpret(d, f)
        assert interp.trace, "every interpretation must carry a provenance trace"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} tests passed")

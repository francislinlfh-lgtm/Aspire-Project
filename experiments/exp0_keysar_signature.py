"""exp0 — instrument demonstration on the Keysar critical/control contrast.

HONESTY CAVEAT (V1.md §7): at this stage the model reproduces signature S1 *by
construction* — P-EGO errs on critical trials because that is what egocentric
resolution means. This script demonstrates that the instrument runs end-to-end with
the language layer stubbed and produces the paradigm's dependent variables. The
science begins when parameters are fit to human data and tested on held-out
conditions (V1.md §5.2). exp0 is plumbing, not a finding.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cogsim.listener import (EgocentricListener, CommonGroundListener,
                             MixtureListener, AnchorAdjustListener)
from cogsim.experiment import run_battery

POLICIES = [
    ("P-EGO", EgocentricListener()),
    ("P-MIX(w=0.25)", MixtureListener(0.25)),
    ("P-MIX(w=0.50)", MixtureListener(0.50)),
    ("P-MIX(w=0.75)", MixtureListener(0.75)),
    ("P-ANCHOR(p=0.50)", AnchorAdjustListener(0.50)),
    ("P-CG", CommonGroundListener()),
]


def main():
    header = (f"{'policy':<18} {'cond':<9} {'acc(intended)':>13} "
              f"{'egocentric err':>14} {'consideration':>13}")
    print(header)
    print("-" * len(header))
    for name, listener in POLICIES:
        for res in run_battery(listener, n_trials=500, seed=7):
            print(f"{name:<18} {res.condition:<9} {res.intended_accuracy:>13.3f} "
                  f"{res.egocentric_error_rate:>14.3f} "
                  f"{res.competitor_consideration:>13.3f}")
    print("\nNote: signature-by-construction demo; see docstring and V1.md §7.")


if __name__ == "__main__":
    main()

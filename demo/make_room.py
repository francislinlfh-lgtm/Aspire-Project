"""make_room.py — simulate the Common Room population with the FITTED model.

Every cognitive event is computed here, by the canonical engine
(cogsim.listener.MixtureListener), using the paper's fitted parameters
(results/exp4_protocol_output.txt: b0=-2.4230, b1=0.2794, b2=0.0933,
kappa=1.378). The HTML viewer is a pure replay/inspection surface: it
contains no cognition, no model arithmetic beyond drawing, and no LLM.

Run: python demo/make_room.py [--seed N]   -> writes demo/room.html
"""
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cogsim.world import critical_display
from cogsim.language import scripted_instruction, privileged_competitor
from cogsim.listener import MixtureListener

# Fitted primary-model parameters (verbatim from the single protocol execution)
B0, B1, B2, KAPPA = -2.4230, 0.2794, 0.0933, 1.378
N_TRIALS = 12
SEED = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 20260803


def mu(age):
    z = (age - 53.0) / 10.0
    x = B0 + B1 * z + B2 * z * z
    return 1.0 / (1.0 + math.exp(-x))


def main():
    rng = random.Random(SEED)
    display = critical_display()
    instr = scripted_instruction(display)
    priv = privileged_competitor(display, instr.frame)

    people = []
    for age in range(20, 85, 2):                      # 33 little people
        m = mu(age)
        a_i = rng.betavariate(m * KAPPA, (1 - m) * KAPPA)
        listener = MixtureListener(a_i)
        trials = []
        for _t in range(N_TRIALS):
            interp = listener.interpret(display, instr.frame)
            choice = interp.sample(rng)
            trials.append({
                'choice': choice,
                'egocentric': choice == priv,
                'correct': choice == instr.intended_oid,
                'trace': [list(step) for step in interp.trace],
            })
        people.append({'age': age, 'alpha': round(a_i, 4), 'trials': trials})

    bands = {'20-37': [20, 37], '38-59': [38, 59], '60-84': [60, 84]}
    expected = {
        name: round(sum(p['alpha'] * N_TRIALS for p in people
                        if lo <= p['age'] <= hi), 1)
        for name, (lo, hi) in bands.items()
    }
    payload = {
        'meta': {
            'seed': SEED,
            'params': {'b0': B0, 'b1': B1, 'b2': B2, 'kappa': KAPPA},
            'provenance': 'results/exp4_protocol_output.txt @ commit 9764283',
            'intended': instr.intended_oid,
            'privileged': priv,
            'n_trials': N_TRIALS,
            'expected_by_band': expected,
        },
        'curve': [[a, round(mu(a), 4)] for a in range(20, 85)],
        'people': people,
    }

    template = (ROOT / 'demo' / 'room_template.html').read_text(encoding='utf-8')
    html = template.replace('/*__DATA__*/null', json.dumps(payload))
    out = ROOT / 'demo' / 'room.html'
    out.write_text(html, encoding='utf-8')
    total_ego = sum(t['egocentric'] for p in people for t in p['trials'])
    print(f'room generated: {len(people)} people x {N_TRIALS} trials, '
          f'{total_ego} egocentric choices | seed {SEED} -> {out}')


if __name__ == '__main__':
    main()

"""The language boundary.

V1 core validation uses *scripted structured frames* — the analogue of the fixed
confederate scripts human participants received — so the core package needs no LLM at
all ("cognition precedes language" made literal; V1.md §3.3).

Contract for any future LLM adapter (kept OUTSIDE this package):
    parse:  text -> ReferringFrame            (classification into a closed space;
                                               cognition enumerates the candidates)
    render: structured act -> text            (template or LLM; if LLM, subject to the
                                               round-trip audit, V1.md §2.2 item 4)
The LLM may not plan, reason, remember, update beliefs, infer psychology, track
perspective, or decide to clarify. Those functions live in cogsim.* modules only.
"""
from dataclasses import dataclass

from .world import Display, best_match


@dataclass(frozen=True)
class ReferringFrame:
    """Structured content of a referring expression, e.g. 'the smallest candle'."""
    category: str
    scalar: str | None = None


@dataclass(frozen=True)
class Instruction:
    """A scripted director utterance plus its ground-truth intended referent."""
    frame: ReferringFrame
    intended_oid: str


def scripted_instruction(display: Display, category: str = "candle",
                         scalar: str = "smallest") -> Instruction:
    """The scripted director refers from the *mutual* perspective, as in the paradigm:
    the intended referent is the best match among mutually visible objects."""
    frame = ReferringFrame(category, scalar)
    pool = [o for o in display.mutually_visible() if o.category == category]
    intended = best_match(pool, scalar)
    if intended is None:
        raise ValueError("scripted instruction has no resolvable referent")
    return Instruction(frame, intended.oid)


def privileged_competitor(display: Display, frame: ReferringFrame):
    """The oid of the best egocentric match if it is hidden from the director,
    else None. This is the object that makes a trial 'critical'."""
    pool = [o for o in display.objects if o.category == frame.category]
    best = best_match(pool, frame.scalar)
    if best is not None and not best.mutually_visible:
        return best.oid
    return None

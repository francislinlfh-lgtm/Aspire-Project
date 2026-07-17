"""Objects, displays, and scalar semantics for the director task.

The paradigm (Keysar, Barr, Balin & Brauner, 2000): a display of objects, some slots
occluded so the *director* cannot see them. `mutually_visible=False` marks a
listener-privileged object. Perspective is ground-truth computable from the display —
by design of the paradigm, not by theoretical commitment (V1.md §6.2).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Obj:
    oid: str
    category: str
    size: int                # ordinal within the display; 1 = smallest
    mutually_visible: bool   # False = occluded from the director (privileged)


@dataclass(frozen=True)
class Display:
    objects: tuple

    def of_category(self, category: str) -> tuple:
        return tuple(o for o in self.objects if o.category == category)

    def mutually_visible(self) -> tuple:
        return tuple(o for o in self.objects if o.mutually_visible)


def best_match(pool, scalar):
    """Deterministic scalar-adjective semantics within a domain.

    Ties broken by oid so every run is replayable. Returns None on empty pool.
    """
    if not pool:
        return None
    if scalar == "smallest":
        return min(pool, key=lambda o: (o.size, o.oid))
    if scalar == "largest":
        return min(pool, key=lambda o: (-o.size, o.oid))
    if scalar is None:
        # Bare category reference: unique referent expected; ambiguous otherwise.
        return pool[0] if len(pool) == 1 else None
    raise ValueError(f"unknown scalar: {scalar!r}")


def critical_display(category: str = "candle") -> Display:
    """Critical trial: the best *egocentric* match ('smallest candle') is privileged.

    Director-intended referent = smallest mutually visible candle (size 2).
    """
    return Display((
        Obj("c1", category, 1, mutually_visible=False),   # privileged competitor
        Obj("c2", category, 2, mutually_visible=True),    # intended referent
        Obj("c3", category, 3, mutually_visible=True),
        Obj("f1", "truck", 2, mutually_visible=True),     # filler
    ))


def control_display(category: str = "candle") -> Display:
    """Control trial: the occluded slot holds an irrelevant filler; egocentric and
    common-ground readings of 'the smallest candle' coincide."""
    return Display((
        Obj("f0", "block", 1, mutually_visible=False),
        Obj("c2", category, 2, mutually_visible=True),
        Obj("c3", category, 3, mutually_visible=True),
        Obj("f1", "truck", 2, mutually_visible=True),
    ))

"""Architecture boundary checks (EDUCATION_ARCHITECTURE.md, laws L1-L2).

L1: education code may import from the engine only via cogsim.api
    (strictly: `import cogsim.api` or `from cogsim.api import ...`).
L2: engine code may never import from education.

These pass vacuously while education/ contains no Python — the point is that the
rules exist from the first education commit, not after the first violation.

Run: python tests/test_boundaries.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _py_files(folder: str):
    d = ROOT / folder
    return sorted(d.rglob("*.py")) if d.exists() else []


IMPORT_COGSIM = re.compile(
    r"^\s*(?:from\s+cogsim(\.[\w.]+)?\s+import\b|import\s+cogsim(\.[\w.]+)?)",
    re.MULTILINE,
)
IMPORT_EDUCATION = re.compile(r"^\s*(?:from|import)\s+education\b", re.MULTILINE)


def test_L1_education_imports_only_the_api():
    violations = []
    for f in _py_files("education"):
        for m in IMPORT_COGSIM.finditer(f.read_text(encoding="utf-8")):
            submodule = m.group(1) or m.group(2) or ""
            if submodule != ".api":
                violations.append(f"{f.relative_to(ROOT)}: {m.group(0).strip()}")
    assert not violations, (
        "L1 violation — education may import cogsim.api ONLY:\n" + "\n".join(violations)
    )


def test_L2_engine_never_imports_education():
    violations = []
    for f in _py_files("cogsim"):
        for m in IMPORT_EDUCATION.finditer(f.read_text(encoding="utf-8")):
            violations.append(f"{f.relative_to(ROOT)}: {m.group(0).strip()}")
    assert not violations, (
        "L2 violation — the engine must never import education:\n" + "\n".join(violations)
    )


def test_engine_has_no_pedagogy_vocabulary():
    """Cheap tripwire for L4 drift: classroom concepts must not appear in engine code."""
    banned = re.compile(r"\b(lesson|quiz|hint|curriculum|student|teacher)\b", re.IGNORECASE)
    violations = []
    for f in _py_files("cogsim"):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if banned.search(line):
                violations.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()}")
    assert not violations, (
        "L4 drift — pedagogy vocabulary found in engine code:\n" + "\n".join(violations)
    )


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for fn in fns:
        try:
            fn()
            print(f"ok  {fn.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL {fn.__name__}\n{e}")
    print(f"\n{len(fns) - failures}/{len(fns)} boundary checks passed")
    sys.exit(1 if failures else 0)

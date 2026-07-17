"""cogsim — an instrument for operationalizing psychological theories as executable
mechanisms and evaluating them against human behavioral data.

V1 scope: listener-side reference resolution under perspective asymmetry
(the director task). See V1.md for the research specification.

Invariant: no LLM is imported, called, or simulated anywhere in this package.
Language enters as structured frames (cogsim.language); any LLM parser/renderer
lives outside the package and is subject to the round-trip audit (V1.md §2).
"""

__version__ = "0.1.0"

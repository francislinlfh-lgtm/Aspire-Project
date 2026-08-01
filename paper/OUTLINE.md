# Manuscript plan — Study 1A

**Title shortlist (refined 2026-08-01 after the gap mapping; rule-checked — no
"first," no "increases across adulthood," no "U-shaped"):**
1. **RECOMMENDED:** "From error curves to a latent weight: a model-based
   reanalysis of perspective-taking across adulthood" — names the contribution
   (descriptive curves → estimated quantity); venue-agnostic.
2. Findings-forward (journal): "The egocentric weight rises across later
   adulthood — and a single mixture process cannot explain both ends of the adult
   age range" ("rises across later adulthood" is rule-safe: monotone from the
   fitted minimum at 38 onward; carries the T2 failure in the title).
3. Estimand-forward (CogSci-compact): "Weighing perspectives across adulthood:
   estimating the egocentric mixture weight from director-task choices" (quietly
   echoes Heller et al.'s own title — their lineage will notice).

**Venue ladder:** PsyArXiv preprint → CogSci 2027 (6-page, ~Feb deadline) and/or
Psychonomic Bulletin & Review (Brief Report); ISEF/STS project paper draws from the
same manuscript. The paper is written venue-agnostic first.

**Authorship & disclosure plan:** Francis writes Introduction and Discussion first
drafts from the scaffolds below (these are the sections defended at ISEF and in
interviews); AI-assisted drafting of Methods/Results is verified line-by-line by
Francis against `results/exp4_protocol_output.txt` and disclosed in the manuscript's
statement. Every number must trace to a committed log or document.

---

## Argument spine (one sentence per section)

1. **Intro:** Whether listeners interpret reference egocentrically or via common
   ground is a live dispute; Heller et al. (2016) proposed a mixture with weight α
   but never fitted it; Bradford et al. (2023) published lifespan director-task
   data as error curves; fitting α to their trials turns a descriptive age pattern
   into a psychologically interpretable quantity.
2. **Model:** a choice-level projection of Heller's Eq. 2 with a Beta-Binomial
   hierarchy; an exact equivalence result makes all α claims explicitly
   conditional on the response rule (ε = 2α).
3. **Methods:** open data; cleaning that exactly reproduces the published sample
   and error rate; exploration → externally reviewed frozen protocol (commits) →
   single outcome-bearing execution.
4. **Results:** Meets prespecified robustness criteria; Δα = +0.127 [+0.062,
   +0.196]; 20/20 participant-level CV; curve minimum at age 38 (untold);
   T1 passes, **T2 fails at 99%** — the model's own failure, reported as a result.
5. **Discussion:** what a fitted α does and does not mean; the T2 failure as
   evidence that one age-varying mixture process cannot cover both age extremes;
   scope (task/items, choice level, rule-conditional); the sealed eye-tracking
   data as the designed next test.

## Section scaffolds

### Abstract (~150 w; write LAST)
Structure: dispute → mixture model never fitted → reanalysis of N=264 lifespan
dataset → frozen protocol → Δα with CI + CV result → T2 failure → conclusion that
is deliberately model-conditional.

### 1. Introduction — FRANCIS DRAFTS (scaffold)
- ¶1 The phenomenon: director task; egocentric interference (Keysar et al., 2000).
- ¶2 The dispute: egocentric-anchoring (Keysar; Epley et al. 2004) vs early
  integration (Hanna et al., 2003) vs probabilistic weighing (Heller et al., 2016).
  One sentence on construct-validity critique (Rubio-Fernández, 2017).
- ¶3 The gap, stated narrowly and with its neighbors named (RELATED_WORK.md §6,
  searched 2026-08-01): Heller et al. varied α, never fitted it (verified);
  Mozuraitis et al. determined a *range* for the production-side weight against
  condition means — not trial-level estimation, no hierarchy, no age;
  Rubio-Fernández & Jara-Ettinger inferred common ground from offline judgments;
  Hawkins et al. fitted RSA parameters in a different paradigm. **No study has
  estimated the comprehension-side weight from trial-level choices, with a
  participant hierarchy, as a function of age, with held-out prediction.** The
  loose "first to quantify the weight" claim is FALSE and banned.
- ¶4 Aging: Bradford et al. (2023) — lifespan sample, quadratic error curves,
  open data. Their analysis is descriptive of error rates, not model-based.
- ¶5 This paper: fit α(age) at trial level under a frozen protocol; three
  contributions — (i) the estimated quantity + uncertainty, (ii) held-out
  participant prediction, (iii) an honest, pre-registered model failure (T2).
- ¶6 Identifiability honesty up front: response-rule equivalence (forward-ref
  the proposition); serial-vs-simultaneous not adjudicated here.

### 2. Model — DRAFTED (verify)
As in paper/manuscript.md §2 (equations, hierarchy, the equivalence proposition,
what "choice-level projection" omits from Heller's full model).

### 3. Methods — DRAFTED (verify)
As in paper/manuscript.md §3. Every commit hash cited is load-bearing.

### 4. Results — DRAFTED (verify against results/exp4_protocol_output.txt)
As in paper/manuscript.md §4. Includes the exploratory-phase summary in one
clearly-labeled paragraph (κ-floor lesson: fourfold → threefold-ish under freed
heterogeneity) because documenting that correction is credibility, not weakness.

### 5. Discussion — FRANCIS DRAFTS (scaffold)
- ¶1 Restate the finding in the locked template language; the fitted-shape verb.
- ¶2 What α is: a model-defined quantity, not a measured psychological essence;
  the ε = 2α dual reading in plain words.
- ¶3 The turning point at 38 (convergent with the source paper's breakpoint) AND
  the unidentifiable knee — what together they say about smooth vs breakpoint
  descriptions of aging effects.
- ¶4 The T2 failure as the paper's most useful sentence: young-adult singleton
  errors exceed the model's 99% envelope → one age-varying mixture process is
  insufficient; candidate elaborations (lapse component; mixture-of-processes),
  none fitted here, all named as future work.
- ¶5 Scope and limits: same task/item set; choice-level; cross-sectional age;
  reanalysis of one dataset; exploration-informed protocol (not independent
  confirmation).
- ¶6 The designed next step: the untouched eye-tracking outcomes as a genuine
  confirmatory test (protocol to be frozen before inspection); EF analyses
  deferred to a separate protocol with an exploratory label already mandated.
- ¶7 Close: what a small explicit model, an open dataset, and frozen decisions
  bought — a descriptive curve became an estimated quantity with a testable
  failure mode.

### Statements (end matter)
- Data/code availability: all code, protocols, and logs public (repo URL +
  hashes); dataset is Bradford et al.'s OSF 2epsu, cited, not redistributed.
- AI assistance disclosure: drafting/engineering assistance (Claude, Anthropic);
  all analyses specified in the committed protocol; all text verified by the
  author. (Wording to match target venue's policy.)
- Acknowledgments: Bradford, Brunsdon & Ferguson for open data; [external
  reviewer credit as appropriate].

## Claim discipline (binding for every draft pass)
- Verbs from the §12 template only; "followed the fitted shape," never
  "increased across adulthood."
- "The fitted constant-α model," never "any constant-weight account."
- Every α accompanied by ε = 2α at first use and in the key table.
- No "confirmatory" self-description; "frozen protocol following exploration."
- T2 failure appears in the abstract. Non-negotiable.

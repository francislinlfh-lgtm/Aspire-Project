# Dataset codebook — Bradford, Brunsdon & Ferguson (2023), OSF 2epsu

Working notes for the Study 1A candidate dataset. Facts below are extracted from the
author accepted manuscript; page-anchored verification against the published version
happens before any paper submission. **The AAM PDF is APA-copyrighted and must never
be committed to this repository.**

## Identity and permissions

- **Paper:** Bradford, E. E. F., Brunsdon, V. E. A., & Ferguson, H. J. (2023).
  Cognitive mechanisms of perspective-taking across adulthood: An eye-tracking study
  using the director task. *JEP: Learning, Memory, and Cognition*, 49(6), 959–973.
  doi:10.1037/xlm0001190. Funded by ERC Starting Grant CogSoCoAGE (636458).
- **Data:** the paper carries a formal Open Data statement — "Data and analysis code
  can be accessed on the Open Science Framework": https://osf.io/2epsu/. The authors
  even provide a dataset citation in their reference list (Bradford, Brunsdon &
  Ferguson, 2022, *OSF Data and Code…*). **Reanalysis with both citations is the
  intended use of published open data; the license checkbox is effectively
  resolved.** Courtesy email still goes out (recipients confirmed in the author
  note: Elisabeth Bradford, ebradford001@dundee.ac.uk, or Heather Ferguson,
  H.Ferguson@kent.ac.uk).

## Design (as relevant to modeling)

- Eye-tracked computerized director task (Keysar et al., 2000 lineage): 4×4 grid,
  occluded slots, prerecorded audio instructions ("Move the small star one slot
  down"), mouse drag-and-drop responses.
- **Conditions:** Listener-Only — occluded object *semantically matches* the
  description (perspective use required); Shared-Perspective — occluded object does
  **not** match. Note: both conditions have an occluded object; they differ in
  whether it competes. Our `control_display` (non-matching filler in the occluded
  slot) is faithful to this.
- **Trials:** arrays of 3 instructions (2 fillers + 1 critical), 72 instructions
  total; **12 Listener-Only + 12 Shared critical trials** per participant — matching
  the CSV's 24 rows per participant. Filler/critical order counterbalanced.
- **Sample bookkeeping (cleaning rules to replicate):** 268 completed → 4 excluded
  (1 non-native speaker, 1 computer failure, 2 low IQ) → 264 in behavioral analyses
  (abstract says 265 — minor discrepancy to resolve); eye-tracking N = 249 (15 lost
  to calibration). The raw CSV has 266 participant ids → it includes participants
  the paper excluded; **our pipeline must reconstruct their exclusions or justify
  its own.** Their sensitivity analyses also drop participants with ≥90% errors on
  Listener trials (N = 249).
- Procedure context: part of a ~5-hour battery over one or two days, counterbalanced.

## Files and columns

### DirectorTask_RawBehaviouralData.csv (trial-level, verified)

| Column | Meaning | Status |
|---|---|---|
| Participant | id (266 unique — includes later-excluded participants) | confirmed |
| Age | years, 20–86 | confirmed |
| Age2 | appears to be Age − 19 (row 1: Age 20 → 1) | inferred — verify |
| trial_number | 1–24 (critical trials only; fillers absent) | confirmed |
| Trial_section_type | constant "Experimental" | confirmed |
| CONDITION | Listener / Shared (see Design) | confirmed |
| Object_Clicked | Target, Competitor, Contrast, Distractor, plus codes AF, F, 3, 7, 8 | **partially unknown** — AF/F/numerals unexplained; likely filler-object or grid-slot codes; the one remaining email question |
| EgocentricErrors | 1 = selected the hidden competitor | confirmed |
| OtherError | 1 = wrong selection other than the competitor | confirmed (by construction) |
| TargetMoveAccuracy | 1 = correct | confirmed |
| MousePress_RT | ms **from scalar-adjective onset** to click; negative = anticipatory click before scalar onset; paper analyzes correct trials only (~6.56% loss), log-transformed | confirmed |

Open bookkeeping question: a few participants have 48 rows, not 24 — not explained
by the paper (tasks ran over one *or* two days; a repeat administration?). Resolve
before fitting; second email question if the data doesn't answer it.

### DirectorTask_EyeTrackingData.txt (process-level, 48.5 MB)

Columns: Participant, Age, Trial, **ScalarTime** (ms from scalar-adjective onset —
confirmed by the paper's RT convention), Condition, AOI, and binary indicator
columns (Competitor, Contrast, Other, Target) + Trackloss. Paper's treatment: AOIs
around every object; 3000 ms analysis window from scalar onset; 20 ms binary bins
merged to 100 ms; growth curve analysis (Mirman). **This is D1-grade time-course
data** (IDENTIFIABILITY.md §3.1) sitting in public.

### Supporting files

- `MediationData.csv` — executive-function battery: inhibition (Stroop), working
  memory (O-Span), flexibility (task-switching), planning (Tower of Hanoi).
  Individual-difference measures that can moderate fitted `w` — directly relevant
  to effort-based accounts (Epley et al., 2004).
- `DirectorTask_Demographics.csv`, `QuestionnaireData.csv` — participant-level.
- `Code/` — the authors' Rmd analyses (accuracy: participant-level lm over age;
  RT: lmer, maximal random effects; eye: GCA). R 3.5.2.

## Published anchors our pipeline must reproduce before claiming anything new

1. Mean egocentric response rate in Listener-Only: **10.23%** of trials.
2. Quadratic age effect on egocentric errors: plateau ~20–37, decline from ~38.
3. Mean correct RT ≈ 3178 ms from scalar onset; positive linear age effect.
4. Eye data: age-related delay in orienting to target; competitor interference.

If our cleaned data does not reproduce (1)–(3) descriptively, our cleaning is wrong
— fix that before any model fitting. Note for modeling: 10.23% average egocentric
choice, under the current linking assumptions, implies a high fitted `w` — expect
the interesting variance to be *across age and individuals*, not in the grand mean.

## Remaining unknowns (the entire list)

1. Object_Clicked codes AF / F / 3 / 7 / 8.
2. Why some participants have 48 rows.
3. Age2 definition (verify Age − 19).
4. Abstract's N=265 vs results' N=264.
5. Two unexamined files on page 2 of the OSF Code folder — check for a codebook
   before emailing; the codes question may answer itself.

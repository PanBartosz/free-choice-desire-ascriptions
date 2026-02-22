**Paper mapping**
- This folder contains **Study 2** materials and analysis assets for the paper (forthcoming).

**Python environment**
- Use the shared env defined in `paper_analyses/requirements.txt` (setup instructions: `paper_analyses/PYTHON_ENV.md`).

**File inventory**
- Complete per-file mapping (including this study) is in `paper_analyses/docs/FILE_INDEX.md`.

**Overview**
- Truth-value judgment study with strict food preference orders (no modals, no “does not mind” items). Participants judge segmented sentences with `B = TRUE` and `N = FALSE`. Practice gives feedback; the main block does not. Break occurs halfway through the main block.
- Tribes: Urbanites sweets > meat > fruit; Nomads fruits > meat > sweets. The order is strict: wants > accepts > dislikes. For “prefers A to B,” equal categories make the sentence false.
- Run file: `experiment/experiment.html` (loads JSON stimuli from the same folder).

**Stimuli**
- Main set (114 total) in `experiment/stimuli_experimental.json` / root Excel:
  - Single controls (18): 2 tribes × 3 categories (dislike/accept/want) × 3 items. Truth: only “want” is true.
  - Double controls (36): 2 tribes × 3 categories × 2 orders × 3 items. Truth: only want|want disjunctions are true.
  - Prefer different (24): 2 tribes × 2 comparisons (accept vs dislike; want vs accept) × 2 orders × 3 items. Truth depends on order; “prefers A to B” is true when A’s category outranks B’s.
  - Prefer same (12): 2 tribes × 2 comparisons (accept vs accept; want vs want) × 3 items. Truth: false (equal liking).
  - Experimental want disjunctions (24): 2 tribes × 2 subconditions (want|dislike; want|accept) × 2 orders × 3 items. Truth left open (CORRECT = “Y/N”) for analysis; no feedback in main.
- Practice set (32 total) in `experiment/stimuli_practice.json`:
  - Single controls: wants/dislikes only (2 tribes × 2 categories × 2 items) — no “accept” singles.
  - Double controls (wants/dislikes): keep order factor with one item per order (2 × 2 × 2).
  - Prefer different: one exemplar per order (2 × 2 × 2).
  - Prefer same: two exemplars per comparison (2 × 2 × 2).
- Stimuli structure fields (logged): `CONDITION`, `SUBCONDITION`, `STRUCTURE`, `ORDER`, `TRIBE`, `ITEM1/ITEM2`, `ITEM1_TYPE/ITEM2_TYPE`, `RELATION` (gt/lt/eq), `CORRECT`, `LOGICAL_TRUTH`, and prebuilt feedback strings for training items.

**Presentation/Feedback**
- Sentences are segmented: name → predicate → verb → complement. Response prompt shows `B = TRUE` and `N = FALSE`.
- Practice uses explanatory feedback:
  - “always prefers …” when left item outranks right,
  - “never prefers …” when it is worse,
  - “equally likes …” for equal categories,
  - “always wants to eat …” for want controls when the correct answer is true; otherwise “never wants to eat …”.
- Main block has no feedback. Break triggers at the midpoint (`Math.floor(stimuli_experimental.length / 2)`, i.e., after 57 trials).

**Regenerating stimuli**
- From this directory, run `python generate_stimuli.py`.
- Outputs:
  - JSON for jsPsych: `experiment/stimuli_experimental.json`, `experiment/stimuli_practice.json` (as JS variables).
  - Excel (or CSV fallback) for review in both root and `experiment/`: `stimuli_experimental.xlsx`, `stimuli_practice.xlsx`.

**Processing results + report**
- Put the JATOS export (`jatos_results_*.jrzip`) and the Prolific export (`prolific_export_*.csv`) into `results/`.
- Create the tidy dataset:
  - From `results/`: `python process_results.py jatos_results_*.jrzip` (writes `results.csv`).
  - Or from repo root: `python results/process_results.py results/jatos_results_*.jrzip --out results/results.csv`
- Render the Quarto report (from `results/`): `quarto render analysis_preferences_freechoice.qmd` (writes `analysis_preferences_freechoice.html`).

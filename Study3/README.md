**Paper mapping**
- This folder is the copy used for paper prep: **Study 3** in `paper_analyses/Free Choice and Desire Ascriptions_draft.pdf`.
- Source in the original project layout (kept intact there): `Exp5_weak_freechoice_soft_with_reminders/`.

**Python environment**
- Use the shared env defined in `paper_analyses/requirements.txt` (setup instructions: `paper_analyses/PYTHON_ENV.md`).

**Overview**
- Truth-value judgment study (“Magical Island”) targeting free-choice readings under **want**.
- Key manipulation vs Study 2: additional training/anchoring with **does not mind** items, intended to make the “accepted” category salient as *acceptable-but-not-wanted*.
- Keys: `B` = TRUE, `N` = FALSE.
- Run file: `experiment/experiment.html` (jsPsych + JATOS; loads `experiment/stimuli_*.json`).

**Design**
- Practice: 40 trials (feedback after each item).
- Main: 122 trials (no feedback) + a midpoint break (after trial 61).
- Verbs used: `want` (critical) and `does not mind` (training/controls).
- Main-session conditions (counts from the shipped stimuli files):
  - `SINGLE_CONTROL` (42): “X wants to eat …” for each category (wanted/accepted/disliked).
  - `DOUBLE_CONTROL` (30): “X wants to eat … or …” with both items from the same category.
  - `EXPERIMENTAL` (34): disjunctions mixing categories (primarily **want**, plus a small set of **does not mind** disjunctions).
  - `SINGLE_CONTROL_MIND` (8): “X does not mind eating …” (accepted vs disliked).
  - `DOUBLE_CONTROL_MIND` (8): “X does not mind eating … or …” (accepted vs disliked).

**Scenario (preference structure)**
- Two tribes with fixed food preferences:
  - Urbanites: **want** sweets, **accept/do not mind** meat, **dislike** fruit.
  - Nomads: **want** fruit, **accept/do not mind** meat, **dislike** sweets.

**Regenerating stimuli**
- Run `python generate_stimuli.py` from this directory.
- Outputs written at the study root (and/or `experiment/` depending on script version): `stimuli_experimental.json/.xlsx`, `stimuli_practice.json/.xlsx`.

**Processing results + report**
- Put the JATOS export (`jatos_results_*.jrzip`) into `results/`.
- From `results/`, create the tidy dataset:
  - `python process_results.py jatos_results_*.jrzip ../stimuli_experimental.json ../stimuli_practice.json` (writes `results.csv` into `results/`).
- Analysis notebooks/reports live in `results/`:
  - `analiza_soft_with_reminders_tidy.Rmd` (main tidy analysis; renders to HTML).
  - `analiza_soft_with_reminders.Rmd` (older version).

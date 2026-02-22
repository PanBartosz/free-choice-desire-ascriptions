# Commit Policy

This file defines what belongs in GitHub for this project.

## Commit

- Study code:
  - `Study*/generate_stimuli.py`
  - `Study*/experiment/`
  - `Study*/results/process_results.py`
  - analysis source files (`.Rmd`, `.qmd`, `.py`)
- Study materials:
  - `Study*/README.md`
  - stimuli files used by experiments (`.json`, `.xlsx`, `.csv`, `.tsv`, `.md`)
- Data exports in `Study*/results/` including Prolific/JATOS identifiers (kept by direct project instruction).
- Project-level documentation and environment files:
  - `README.md`
  - `requirements.txt`
  - `PYTHON_ENV.md`
  - `docs/`
  - `scripts/`

## Do Not Commit

- Environment artifacts:
  - `.venv/`
  - `__pycache__/`
  - `*.pyc`
- Temporary and runtime files:
  - `tmp/`
  - `nohup.out`
  - `*.log`
- Editor-local files:
  - `.vscode/`
  - `.idea/`
- Auto-generated support directories:
  - `*_files/` (Quarto/R Markdown rendered dependency bundles)
- Backup files:
  - `*.bak`
- Manuscript/article-writing artifacts:
  - `Free Choice and Desire Ascriptions_draft.pdf`
  - `OUTLINE.md`
  - `*_IMRAD.md`
  - `*_results_rewrite.md`
- Rendered analysis outputs:
  - `Study*/results/*.html`

## Pre-Commit Hygiene

Run:

```bash
bash scripts/preflight_repo.sh
```

before pushing to GitHub.

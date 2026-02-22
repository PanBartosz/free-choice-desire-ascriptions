# Free Choice and Desire Ascriptions - Reproducibility Repository

This repository contains code, data, and study materials for three experiments used in the paper project on free choice and desire ascriptions.

The scope is replication-oriented:
- Include data, analysis code, and experimental materials.
- Keep the repository easy to navigate for external users.
- Do not use the repository as a replacement for the full manuscript narrative.

## Repository Structure

```text
paper_analyses/
  Study1/
    experiment/            # jsPsych experiment assets
    results/               # data exports + analysis scripts
    generate_stimuli.py
    README.md
  Study2/
    experiment/
    results/
    generate_stimuli.py
    README.md
  Study3/
    experiment/
    results/
    generate_stimuli.py
    README.md
  docs/
    COMMIT_POLICY.md       # what to commit / what to exclude
    OSF_SETUP.md           # GitHub <-> OSF workflow
  scripts/
    preflight_repo.sh      # repository hygiene checks
  requirements.txt
  PYTHON_ENV.md
```

## Data Policy

- Raw result exports are included in study `results/` folders.
- Per direct project decision, Prolific/JATOS IDs are retained in released files as-is.
- Reuse must remain ethical and compliant with participant-consent and local policy.

## Quick Start

1. Create the Python environment (see `PYTHON_ENV.md`).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run study-specific generation/processing from each study folder as described in:
- `Study1/README.md`
- `Study2/README.md`
- `Study3/README.md`

## What Is Not Tracked

- Local virtual environments and cache files.
- Temporary exports and runtime logs.
- Manuscript draft PDF and other writing artifacts not required for replication.

See `docs/COMMIT_POLICY.md` for the full list.

## Citation

Use `CITATION.cff` when available in citation tooling.

## OSF Linkage

Follow `docs/OSF_SETUP.md` to connect this GitHub repository to an OSF project/component.

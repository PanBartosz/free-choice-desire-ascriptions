# Python environment (shared for all studies)

All Python scripts under `paper_analyses/` are compatible with a single shared virtual environment.

## Create the environment

From the repo root:

```bash
python -m venv paper_analyses/.venv
source paper_analyses/.venv/bin/activate
python -m pip install -U pip
python -m pip install -r paper_analyses/requirements.txt
```

## Quick checks (optional)

```bash
python -m unittest discover -s paper_analyses/Study1/results -p "test_*.py"
python -m py_compile paper_analyses/Study1/generate_stimuli.py
python -m py_compile paper_analyses/Study2/generate_stimuli.py
python -m py_compile paper_analyses/Study3/generate_stimuli.py
```

## Running common scripts

- Regenerate stimuli:
  - `python paper_analyses/Study1/generate_stimuli.py`
  - `python paper_analyses/Study2/generate_stimuli.py`
  - `python paper_analyses/Study3/generate_stimuli.py`
- Process JATOS exports (example):
  - Study 3 (from `paper_analyses/Study3/results/`):
    - `python process_results.py jatos_results_*.jrzip ../stimuli_experimental.json ../stimuli_practice.json`

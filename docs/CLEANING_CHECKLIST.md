# Cleaning Checklist

Use this checklist before a release tag.

## Repository Hygiene

- [ ] `bash scripts/preflight_repo.sh` passes.
- [ ] No temporary execution logs (`nohup.out`, `*.log`) remain.
- [ ] No cache/build artifacts (`__pycache__`, `*.pyc`, `*_files`) remain.
- [ ] No local editor configuration directories (`.vscode`, `.idea`) remain.
- [ ] `tmp/` is absent or empty.

## Data and Materials

- [ ] Raw study exports are in expected `Study*/results/` paths.
- [ ] Study README files match current data processing scripts.
- [ ] Top-level `README.md` structure and quick-start are still correct.

## Metadata

- [ ] `CITATION.cff` repository URL is set.
- [ ] `LICENSE` and `LICENSE-data` reflect intended reuse policy.
- [ ] OSF component and GitHub linkage status documented in `docs/OSF_SETUP.md`.

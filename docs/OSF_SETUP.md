# OSF Setup and GitHub Linkage

This document defines the recommended GitHub -> OSF workflow.

## Target Model

- GitHub is the working source of truth for versioned code/data/materials.
- OSF is the project hub for discoverability and archival snapshots.

## Setup Steps

1. Create a GitHub repository and push this local repository.
2. Create an OSF project.
3. Inside OSF, create components:
   - `Code-and-Data` (public component linked to GitHub)
   - `Restricted-Raw-Data` (private OSF storage, optional)
   - `Supplementary-Materials` (optional)
4. In OSF `Code-and-Data`, add the GitHub add-on and connect the GitHub repository.
5. Set access permissions:
   - public for `Code-and-Data` when ready,
   - restricted/private for any sensitive component.
6. For milestone releases:
   - create a GitHub release tag (for example `v1.0.0`),
   - create an OSF registration/snapshot after tagging.

## Suggested Release Rhythm

- Use semantic-ish tags (`v1.0.0`, `v1.1.0`) for analysis milestones.
- Keep OSF registrations aligned with those tags.

## Metadata To Add In OSF

- Short project description.
- License note for code and data.
- Link to repository `README.md`.
- Contact/citation information.

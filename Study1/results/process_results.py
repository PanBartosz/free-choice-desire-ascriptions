import argparse
import json
import os
import zipfile
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd


def load_stimuli(practice_path: Path, experimental_path: Path) -> tuple[Dict[str, dict], Dict[str, dict]]:
    """Load stimuli files into ITEM -> stimulus lookup tables."""
    def _load(path: Path) -> Dict[str, dict]:
        with open(path, "r") as handle:
            raw = handle.read().strip()
        if raw.startswith("var "):
            _, raw = raw.split("=", 1)
        raw = raw.strip().rstrip(";")
        data = json.loads(raw)
        return {row["ITEM"]: row for row in data}

    return _load(practice_path), _load(experimental_path)


def _participant_id(study_result: dict) -> str | None:
    return study_result.get("urlQueryParameters", {}).get("PROLIFIC_PID")


def _plain_stimulus(stimulus: dict | None, trial: dict) -> str:
    """Return a simple 'Premise: ... / Conclusion: ...' string without HTML."""
    premise = None
    conclusion = None
    if stimulus:
        premise = stimulus.get("PREMISE")
        conclusion = stimulus.get("CONCLUSION")
    premise = premise or trial.get("premise")
    conclusion = conclusion or trial.get("conclusion")
    if premise and conclusion:
        return f"Premise: {premise} / Conclusion: {conclusion}"
    return ""


def _iter_component_trials(zf: zipfile.ZipFile, component_path: str) -> Iterable[dict]:
    data_path = component_path.lstrip("/")
    if not data_path.endswith("data.txt"):
        data_path = os.path.join(data_path, "data.txt")
    with zf.open(data_path) as handle:
        return json.load(handle)


def process_zip(
    zip_path: Path,
    stimuli_practice: Dict[str, dict],
    stimuli_experimental: Dict[str, dict],
    skip_missing_prolific: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Extract participant trials from a JATOS .jrzip archive."""
    participants = []
    skipped_participants = 0
    skipped_rows = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        metadata = json.load(zf.open("metadata.json"))
        for study in metadata.get("data", []):
            for study_result in study.get("studyResults", []):
                pid = _participant_id(study_result)
                participant_frames = []
                for component in study_result.get("componentResults", []):
                    raw_trials = _iter_component_trials(zf, component["path"])
                    parsed = []
                    for trial in raw_trials:
                        if "item" not in trial:
                            continue
                        item_id = trial["item"]
                        session = "PRACTICE" if item_id.startswith("P") else "EXPERIMENTAL"
                        lookup = stimuli_practice if session == "PRACTICE" else stimuli_experimental
                        stimulus = lookup.get(item_id)

                        enriched = dict(trial)
                        enriched["SESSION"] = session
                        enriched["PARTICIPANT"] = pid
                        enriched["stimulus"] = _plain_stimulus(stimulus, trial)
                        if stimulus:
                            enriched["STIMULUS_VALID"] = stimulus.get("VALID")
                            enriched["STIMULUS_DOMAIN"] = stimulus.get("DOMAIN")
                            enriched["STIMULUS_PAIR_TYPE"] = stimulus.get("PAIR_TYPE")
                        parsed.append(enriched)

                    if parsed:
                        participant_frames.append(pd.DataFrame(parsed))

                if not pid and skip_missing_prolific:
                    skipped_participants += 1
                    skipped_rows += sum(len(df_part) for df_part in participant_frames)
                    continue

                if participant_frames:
                    participants.append(pd.concat(participant_frames, ignore_index=True))

    if not participants:
        raise ValueError("No participant data found in the archive.")
    return pd.concat(participants, ignore_index=True), {
        "skipped_participants": skipped_participants,
        "skipped_rows": skipped_rows,
    }


def validate_counts(df: pd.DataFrame, stimuli_practice: Dict[str, dict], stimuli_experimental: Dict[str, dict]) -> None:
    """Ensure each participant saw exactly the intended stimuli."""
    expected = {"PRACTICE": set(stimuli_practice.keys()), "EXPERIMENTAL": set(stimuli_experimental.keys())}
    grouped = df.groupby(["PARTICIPANT", "SESSION"])
    for (pid, session), frame in grouped:
        expected_items = expected[session]
        seen = set(frame["item"])
        missing = expected_items - seen
        extra = seen - expected_items
        if missing or extra:
            raise AssertionError(f"Item mismatch for {pid} / {session}: missing={sorted(missing)}, extra={sorted(extra)}")
        duplicates = frame["item"].duplicated()
        if duplicates.any():
            dup_items = frame.loc[duplicates, "item"].tolist()
            raise AssertionError(f"Duplicate items for {pid} / {session}: {dup_items}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Process JATOS result archive for Experiment 7 (entailment FC).")
    parser.add_argument("zipfile", type=Path, help="Path to jatos_results_*.jrzip file.")
    parser.add_argument("--stimuli-experimental", type=Path, default=None, help="Path to experimental stimuli JSON.")
    parser.add_argument("--stimuli-practice", type=Path, default=None, help="Path to practice stimuli JSON.")
    parser.add_argument("--out", type=Path, default=Path("results.csv"), help="Destination CSV path.")
    parser.add_argument("--skip-validate", action="store_true", help="Skip count validation against stimuli files.")
    parser.add_argument("--keep-missing-prolific", action="store_true",
                        help="Keep participants without PROLIFIC_PID (default: skip them).")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    default_experimental = base_dir.parent / "experiment" / "stimuli_experimental.json"
    default_practice = base_dir.parent / "experiment" / "stimuli_practice.json"
    exp_path = args.stimuli_experimental or default_experimental
    practice_path = args.stimuli_practice or default_practice

    stimuli_practice, stimuli_experimental = load_stimuli(practice_path, exp_path)
    df, skipped = process_zip(
        args.zipfile,
        stimuli_practice,
        stimuli_experimental,
        skip_missing_prolific=not args.keep_missing_prolific,
    )
    if not args.skip_validate:
        validate_counts(df, stimuli_practice, stimuli_experimental)

    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows for {df['PARTICIPANT'].nunique()} participant(s) to {args.out}")
    if skipped["skipped_participants"] or skipped["skipped_rows"]:
        print(f"Skipped {skipped['skipped_participants']} participant(s) without PROLIFIC_PID "
              f"({skipped['skipped_rows']} trial rows).")


if __name__ == "__main__":
    main()

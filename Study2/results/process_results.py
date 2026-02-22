import argparse
import json
import os
import zipfile
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd


def load_stimuli(practice_path: Path, experimental_path: Path) -> tuple[Dict[str, dict], Dict[str, dict]]:
    """Load jsPsych stimuli files into ITEM -> stimulus lookup tables.

    The stimuli files are JS assignments (e.g., `var stimuli_experimental = [...]`).
    """

    def _load(path: Path) -> Dict[str, dict]:
        raw = path.read_text(encoding="utf-8").strip()
        if raw.startswith("var "):
            _, raw = raw.split("=", 1)
        raw = raw.strip().rstrip(";")
        data = json.loads(raw)
        return {row["ITEM"]: row for row in data}

    return _load(practice_path), _load(experimental_path)


def _participant_id(study_result: dict) -> str | None:
    return study_result.get("urlQueryParameters", {}).get("PROLIFIC_PID")


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
    *,
    skip_missing_prolific: bool = True,
    finished_only: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Extract response trials from a JATOS .jrzip archive."""
    participants = []
    skipped_participants = 0
    skipped_rows = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        metadata = json.load(zf.open("metadata.json"))
        for study in metadata.get("data", []):
            for study_result in study.get("studyResults", []):
                if finished_only and study_result.get("studyState") != "FINISHED":
                    continue

                pid = _participant_id(study_result)
                if not pid and skip_missing_prolific:
                    skipped_participants += 1
                    continue

                url_params = study_result.get("urlQueryParameters", {}) or {}
                participant_frames = []

                for component in study_result.get("componentResults", []):
                    parsed = []
                    for trial in _iter_component_trials(zf, component["path"]):
                        if "item" not in trial:
                            continue

                        item_id = trial["item"]
                        if item_id in stimuli_practice:
                            session = "PRACTICE"
                            stimulus = stimuli_practice[item_id]
                        elif item_id in stimuli_experimental:
                            session = "EXPERIMENTAL"
                            stimulus = stimuli_experimental[item_id]
                        else:
                            session = "UNKNOWN"
                            stimulus = None

                        enriched = dict(trial)
                        enriched["SESSION"] = session
                        enriched["PARTICIPANT"] = pid

                        enriched["JATOS_STUDY_RESULT_ID"] = study_result.get("id")
                        enriched["JATOS_STUDY_RESULT_UUID"] = study_result.get("uuid")
                        enriched["JATOS_WORKER_ID"] = study_result.get("workerId")
                        enriched["JATOS_START_DATE"] = study_result.get("startDate")
                        enriched["JATOS_END_DATE"] = study_result.get("endDate")
                        enriched["JATOS_DURATION"] = study_result.get("duration")
                        enriched["JATOS_STUDY_STATE"] = study_result.get("studyState")

                        enriched["PROLIFIC_STUDY_ID"] = url_params.get("STUDY_ID")
                        enriched["PROLIFIC_SESSION_ID"] = url_params.get("SESSION_ID")

                        if stimulus:
                            enriched["STIMULUS_CORRECT"] = stimulus.get("CORRECT")
                            enriched["STIMULUS_LOGICAL_TRUTH"] = stimulus.get("LOGICAL_TRUTH")
                            enriched["STIMULUS_CONDITION"] = stimulus.get("CONDITION")
                            enriched["STIMULUS_SUBCONDITION"] = stimulus.get("SUBCONDITION")
                            enriched["STIMULUS_ORDER"] = stimulus.get("ORDER")

                        parsed.append(enriched)

                    if parsed:
                        participant_frames.append(pd.DataFrame(parsed))

                if participant_frames:
                    participant_df = pd.concat(participant_frames, ignore_index=True)
                    if not pid and not skip_missing_prolific:
                        participant_df["PARTICIPANT"] = ""
                    participants.append(participant_df)
                elif not pid:
                    skipped_participants += 1

    if not participants:
        raise ValueError("No participant data found in the archive.")

    df = pd.concat(participants, ignore_index=True)

    if skip_missing_prolific:
        kept_mask = df["PARTICIPANT"].notna() & (df["PARTICIPANT"].astype(str).str.strip() != "")
        skipped_rows = int((~kept_mask).sum())
        df = df.loc[kept_mask].reset_index(drop=True)

    return df, {"skipped_participants": skipped_participants, "skipped_rows": skipped_rows}


def validate_counts(df: pd.DataFrame, stimuli_practice: Dict[str, dict], stimuli_experimental: Dict[str, dict]) -> None:
    """Ensure each participant saw exactly the intended stimuli once per session."""
    expected = {"PRACTICE": set(stimuli_practice.keys()), "EXPERIMENTAL": set(stimuli_experimental.keys())}
    grouped = df.groupby(["PARTICIPANT", "SESSION"], dropna=False)
    for (pid, session), frame in grouped:
        if session not in expected:
            raise AssertionError(f"Unexpected session label {session!r} for participant {pid!r}.")
        expected_items = expected[session]
        seen = set(frame["item"])
        missing = expected_items - seen
        extra = seen - expected_items
        if missing or extra:
            raise AssertionError(
                f"Item mismatch for participant={pid!r} session={session!r}: "
                f"missing={sorted(missing)} extra={sorted(extra)}"
            )
        duplicates = frame["item"].duplicated()
        if duplicates.any():
            dup_items = frame.loc[duplicates, "item"].tolist()
            raise AssertionError(f"Duplicate items for participant={pid!r} session={session!r}: {dup_items}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process JATOS result archive for Study 2 (preferences free-choice).",
    )
    parser.add_argument("zipfile", type=Path, help="Path to jatos_results_*.jrzip file.")
    parser.add_argument("--stimuli-experimental", type=Path, default=None, help="Path to experimental stimuli JSON.")
    parser.add_argument("--stimuli-practice", type=Path, default=None, help="Path to practice stimuli JSON.")
    parser.add_argument("--out", type=Path, default=Path("results.csv"), help="Destination CSV path.")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validation against stimuli files.")
    parser.add_argument(
        "--keep-missing-prolific",
        action="store_true",
        help="Keep participants without PROLIFIC_PID (default: skip them).",
    )
    parser.add_argument(
        "--keep-nonfinished",
        action="store_true",
        help="Keep study results not marked FINISHED (default: drop them).",
    )
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
        finished_only=not args.keep_nonfinished,
    )
    if not args.skip_validate:
        validate_counts(df, stimuli_practice, stimuli_experimental)

    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows for {df['PARTICIPANT'].nunique()} participant(s) to {args.out}")
    if skipped["skipped_participants"] or skipped["skipped_rows"]:
        print(
            f"Skipped {skipped['skipped_participants']} participant(s) without PROLIFIC_PID "
            f"({skipped['skipped_rows']} trial rows)."
        )


if __name__ == "__main__":
    main()

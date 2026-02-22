import json
import os
import zipfile
import argparse
import pandas as pd


def process_zip(zip_filename, stimuli_practice, stimuli_experimental):
    with zipfile.ZipFile(zip_filename, 'r') as zf:
        # Load metadata.json from the root of the zip archive
        with zf.open('metadata.json') as f:
            metadata = json.load(f)

        participants = []
        count_instructions_conditions = {"hard" : 0, "soft": 0}
        for subject in metadata['data']:
            for results in subject['studyResults']:
                print(f"JATOS ID: {results['id']}")
                prolific_ID = results['urlQueryParameters']['PROLIFIC_PID']
                print(f"PROLIFIC ID: {prolific_ID}")
                for component in results['componentResults']:
                    print(f"PATH: {component['path']}")
                    # Build the file path for data.txt from the component's path.
                    data_txt_path = os.path.join(component['path'], "data.txt")
                    # Remove leading slash if present.
                    if data_txt_path.startswith('/'):
                        data_txt_path = data_txt_path[1:]

                    with zf.open(data_txt_path) as f:
                        data = json.load(f)

                    instructions_count = 0
                    practice_trials = []
                    experimental_trials = []
                    #instructions_condition = "meat"
                    #instructions_condition = None
                    for trial in data:
                        if trial['trial_type'] == "instructions":
                            print("Detected instructions")
                            instructions_count += 1
                        if "condition" in trial:
                            print("Detected trial")
                            # if not instructions_condition:
                            #     instructions_condition = trial["instructions_type"]
                            if instructions_count == 1:
                                trial["ITEM1_TYPE"] = stimuli_practice[trial["item"]]["ITEM1_TYPE"]
                                try:
                                    trial["ITEM2"] = stimuli_practice[trial["item"]]["ITEM2"]
                                    trial["ITEM2_TYPE"] = stimuli_practice[trial["item"]]["ITEM2_TYPE"]
                                except:
                                    pass
                                trial["ITEM1"] = stimuli_practice[trial["item"]]["ITEM1"]
                                practice_trials.append(trial)
                            if instructions_count in (2, 3):
                                trial["ITEM1_TYPE"] = stimuli_experimental[trial["item"]]["ITEM1_TYPE"]
                                try:
                                    trial["ITEM2"] = stimuli_experimental[trial["item"]]["ITEM2"]
                                    trial["ITEM2_TYPE"] = stimuli_experimental[trial["item"]]["ITEM2_TYPE"]
                                except:
                                    pass
                                trial["ITEM1"] = stimuli_experimental[trial["item"]]["ITEM1"]
                                #trial["instructions_type"] = instructions_condition
                                experimental_trials.append(trial)

                    print(f"Number of practice trials: {len(practice_trials)}")
                    print(
                        f"Number of experimental trials: {len(experimental_trials)}")

                    practice_df = pd.DataFrame(practice_trials)
                    experimental_df = pd.DataFrame(experimental_trials)
                    practice_df["SESSION"] = "PRACTICE"
                    experimental_df["SESSION"] = "EXPERIMENTAL"
                    participant_df = pd.concat([practice_df, experimental_df])
                    participant_df["PARTICIPANT"] = prolific_ID
                    participants.append(participant_df)
                    print(f"Processed participant: {prolific_ID}")
                    #print(f"Instructions conditions: {instructions_condition}")
                    #count_instructions_conditions[instructions_condition] += 1

        print(f"Total participants: {len(participants)}")
        participants_df = pd.concat(participants)
        participants_df.to_csv("results.csv", index=False)
        print(f"Instruction conditions: {count_instructions_conditions}")


def main():
    parser = argparse.ArgumentParser(
        description="Process a zip file containing metadata.json and participant data."
    )
    parser.add_argument("zipfile", type=str, help="Path to the zip file")
    parser.add_argument("stimuli_experimental", type=str, help="Path to experimental stimuli file")
    parser.add_argument("stimuli_practice", type=str, help="Path to practice stimuli file")
    args = parser.parse_args()

    with open(args.stimuli_practice, 'r') as f:
        stimuli_practice = json.load(f)
    stimuli_practice_dict = {}
    for stimulus in stimuli_practice:
        stimuli_practice_dict[stimulus["ITEM"]] = stimulus

    print(stimuli_practice_dict)

    with open(args.stimuli_experimental, 'r') as f:
        stimuli_experimental = json.load(f)
    stimuli_experimental_dict = {}
    for stimulus in stimuli_experimental:
        stimuli_experimental_dict[stimulus["ITEM"]] = stimulus


    process_zip(args.zipfile, stimuli_practice_dict, stimuli_experimental_dict)

if __name__ == "__main__":
    main()

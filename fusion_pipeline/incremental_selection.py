import json
import pandas as pd

def load_processing_state(state_path):
    """
    Load the last successfully processed timestamps from the fusion_data state.
    If the state file does not exist, return an empty state.
    """
    if not state_path.exists():
        return {}

    with open(state_path, "r") as file:
        return json.load(file)


def select_new_records(data, source, last_state):
    """
    Select new records that have not yet been processed.
    A record is considered new if its timestamp is later than
    the last successfully processed timestamp for its IDA and source.
    """

    new_records = []

    timestamp_key = f"last_{source}_timestamp"

    for ida, group in data.groupby("IDA"):
        last_timestamp = (last_state.get(str(ida), {}).get(timestamp_key))

        if last_timestamp is None:
            new_records.append(group)
            continue

        last_timestamp = pd.Timestamp(last_timestamp)
        new_group = group[group["timestamp"] > last_timestamp]

        if not new_group.empty:
            new_records.append(new_group)

    if not new_records:
        return data.iloc[0:0].copy()

    return pd.concat(new_records).reset_index(drop=True)


def select_incremental_data(mosaiq_data, myoncare_data, fusion_data_path):
    """
    Select new records from both source datasets.
    """

    state_path = fusion_data_path / "state.json"
    last_state = load_processing_state(state_path)

    # If no previous fusion state, then all imported records are new.
    if not last_state:
        return mosaiq_data.copy(), myoncare_data.copy()

    mosaiq_new = select_new_records(mosaiq_data, "mosaiq", last_state)
    myoncare_new = select_new_records(myoncare_data, "myoncare", last_state)

    return mosaiq_new, myoncare_new
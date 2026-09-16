import json
from pathlib import Path

import pandas as pd


FUSION_COLUMNS = [
    "IDA",
    "source",
    "timestamp",
    "data",
]

def initialize_fusion_data(fusion_data_path):
    """
    Create the fusion data directory structure if it does not exist.
    """

    fusion_data_path.mkdir(parents=True, exist_ok=True)

    records_path = fusion_data_path / "records"
    records_path.mkdir(exist_ok=True)

    fusion_path = fusion_data_path / "fusion.csv"

    if not fusion_path.exists():
        pd.DataFrame(columns=FUSION_COLUMNS).to_csv(fusion_path, index=False)


def write_json_records(prepared_records, fusion_data_path):

    records_path = fusion_data_path / "records"

    for record in prepared_records:
        json_path = records_path / record["filename"]

        with open(json_path, "w") as file:
            json.dump( record["json_record"], file, indent=4)


def append_fusion_rows(prepared_records, fusion_data_path):

    fusion_path = fusion_data_path / "fusion.csv"

    rows = [record["fusion_row"] for record in prepared_records]

    if not rows:
        return

    new_data = pd.DataFrame(rows, columns=FUSION_COLUMNS)
    existing_data = pd.read_csv(fusion_path)

    # Combine old and new records
    fusion_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Sort by IDA, then timestamp
    fusion_data["timestamp"] = pd.to_datetime(fusion_data["timestamp"], format="mixed")
    fusion_data = fusion_data.sort_values( ["IDA", "source", "timestamp"]).reset_index(drop=True)

    fusion_data.to_csv(fusion_path, index=False)


def update_state(prepared_records, fusion_data_path):
    """
    Update state.json with the latest successfully processed timestamp for each IDA and source.
    """
    state_path = fusion_data_path / "state.json"

    if state_path.exists():
        with open(state_path, "r") as file:
            state = json.load(file)
    else:
        state = {}

    for record in prepared_records:

        ida = str(record["fusion_row"]["IDA"])
        source = record["fusion_row"]["source"]
        timestamp = record["fusion_row"]["timestamp"]

        if ida not in state:
            state[ida] = {}

        timestamp_key = f"last_{source}_timestamp"
        current_timestamp = state[ida].get(timestamp_key)

        if (
            current_timestamp is None
            or pd.Timestamp(timestamp) > pd.Timestamp(current_timestamp)
        ):
            state[ida][timestamp_key] = timestamp

    with open(state_path, "w") as file:
        json.dump(state, file, indent=4)


def fuse_records(mosaiq_records, myoncare_records, fusion_data_path):
    """
    Save prepared records into the fusion dataset.
    """

    initialize_fusion_data(fusion_data_path)

    all_records = mosaiq_records + myoncare_records

    # Write source records
    write_json_records(all_records, fusion_data_path)

    # Update fusion index
    append_fusion_rows(all_records, fusion_data_path)

    # Update processing state
    update_state(all_records, fusion_data_path
    )

def write_pending_records(prepared_records, fusion_data_path):
    """
    Save records waiting for approval as JSON files
    """

    pending_path = fusion_data_path / "pending"
    records_path = pending_path / "records"

    pending_path.mkdir(parents=True, exist_ok=True)
    records_path.mkdir(exist_ok=True)

    pending_csv_path = pending_path / "pending.csv"

    #Write JSON records
    for record in prepared_records:
        json_path = records_path / record["filename"]
        with open(json_path, "w") as file:
            json.dump( record["json_record"], file, indent=4)

    # Create pending CSV rows
    rows = []

    for record in prepared_records:
        fusion_row = record["fusion_row"].copy()
        fusion_row["data"] = (f"pending/records/{record['filename']}" )
        rows.append(fusion_row)

    if not rows:
        return

    new_data = pd.DataFrame(rows, columns=FUSION_COLUMNS)

    if pending_csv_path.exists():
        existing_data = pd.read_csv(pending_csv_path)
        pending_data = pd.concat([existing_data, new_data],ignore_index=True)
    else:
        pending_data = new_data

    pending_data["timestamp"] = pd.to_datetime(pending_data["timestamp"],format="mixed")
    pending_data = pending_data.sort_values(
        ["IDA", "timestamp"]).reset_index(drop=True)
    
    pending_data.to_csv(pending_csv_path, index=False)

def load_pending_records(fusion_data_path):
    """
    Load all pending JSON records.
    """
    records_path = (fusion_data_path/ "pending"/ "records")

    if not records_path.exists():
        return []

    pending_records = []

    for file_path in records_path.glob("*.json"):
        with open(file_path, "r") as file:
            json_record  = json.load(file)

        fusion_row = {
            "IDA": json_record["IDA"],
            "source": json_record["source"],
            "timestamp": json_record["timestamp"],
            "data": f"records/{file_path.name}",
        }

        pending_records.append({
            "json_record": json_record,
            "fusion_row": fusion_row,
            "filename": file_path.name,
        })

    return pending_records

def clear_pending_records(fusion_data_path):
    """
    Remove all pending records and pending.csv after successful approval.
    """

    pending_path = fusion_data_path / "pending"
    records_path = pending_path / "records"

    if not pending_path.exists():
        return

    # Remove pending JSON records
    if records_path.exists():
        for file_path in records_path.glob("*.json"):
            file_path.unlink()

    # Remove pending.csv
    pending_csv_path = pending_path / "pending.csv"
    if pending_csv_path.exists():
        pending_csv_path.unlink()

def has_pending_records(fusion_data_path):
    """
    Check whether there are records waiting for approval.
    """
    records_path = (fusion_data_path/ "pending"/ "records")

    if not records_path.exists():
        return False
    
    return any(records_path.glob("*.json"))


def approve_pending_records(fusion_data_path):
    """
    Move approved pending records into the fusion dataset.
    """

    pending_records = load_pending_records(fusion_data_path)

    if not pending_records:
        print("No pending records to approve.")
        return

    initialize_fusion_data(fusion_data_path)

    write_json_records( pending_records, fusion_data_path)
    append_fusion_rows(pending_records, fusion_data_path)
    update_state(pending_records, fusion_data_path)

    # Remove pending records
    clear_pending_records(fusion_data_path)
    print(f"Approved {len(pending_records)} records.")


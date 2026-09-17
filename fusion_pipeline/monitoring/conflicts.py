import json
import pandas as pd

CONFLICT_COLUMNS = [
    "IDA",
    "source",
    "timestamp",
    "existing_data",
    "incoming_data",
    "status",
]

def create_record_key(record):
    """
    Create the unique identifier of a record.
    """
    return (record["IDA"],record["source"],record["timestamp"],)


def load_existing_records(fusion_data_path):
    """
    Load existing fusion records in fusion.csv.
    """

    fusion_path = fusion_data_path / "fusion.csv"

    if not fusion_path.exists():
        return {}

    fusion_data = pd.read_csv(fusion_path)
    existing_records = {}

    for _, row in fusion_data.iterrows():
        record_path = (fusion_data_path/ row["data"])

        if not record_path.exists():
            continue

        with open(record_path, "r") as file:
            record = json.load(file)

        key = create_record_key(record)
        existing_records[key] = {
            "record": record,
            "path": row["data"],
        }

    return existing_records


def detect_conflicts(incoming_records, fusion_data_path):
    """
    Detect incoming records that have the same logical identity as an existing fusion record but different content.

    Returns a list of conflicts.
    """

    existing_records = load_existing_records(fusion_data_path)
    conflicts = []

    for record in incoming_records:
        key = create_record_key(record)

        if key not in existing_records:
            continue

        existing = existing_records[key]
        existing_record = existing["record"]

        if existing_record != record:
            conflicts.append({
                "IDA": record["IDA"],
                "source": record["source"],
                "timestamp": record["timestamp"],
                "existing_record": existing_record,
                "existing_path": existing["path"],
                "incoming_record": record,
            })

    return conflicts


def save_conflicts(conflicts, fusion_data_path):
    """
    Save new conflicts to monitoring/conflicts.csv
    and store incoming conflicting records as JSON.
    """

    if not conflicts:
        return

    monitoring_path = (fusion_data_path / "monitoring")
    records_path = (monitoring_path / "records")
    conflicts_path = (monitoring_path / "conflicts.csv")


    monitoring_path.mkdir(parents=True, exist_ok=True)
    records_path.mkdir(exist_ok=True)

    # Load existing conflicts
    if conflicts_path.exists():
        conflicts_data = pd.read_csv(conflicts_path)
    else:
        conflicts_data = pd.DataFrame(columns=CONFLICT_COLUMNS)

    new_rows = []

    for conflict in conflicts:
        key = create_record_key(conflict)

        # Don't add the same conflict twice
        if not conflicts_data.empty:
            existing_keys = set(
                zip(
                    conflicts_data["IDA"],
                    conflicts_data["source"],
                    conflicts_data["timestamp"],
                )
            )

            if key in existing_keys:
                continue

        filename = (
            f"{conflict['IDA']}_"
            f"{conflict['source']}_"
            f"{conflict['timestamp'].replace(':', '-')}.json"
        )

        incoming_path = (records_path / filename)

        # Save incoming conflicting record
        with open(incoming_path, "w") as file:
            json.dump( conflict["incoming_record"], file, indent=4)

        new_rows.append({
            "IDA": conflict["IDA"],
            "source": conflict["source"],
            "timestamp": conflict["timestamp"],
            "existing_data": conflict["existing_path"],
            "incoming_data": (
                f"monitoring/records/{filename}"
            ),
            "status": "pending",
        })

    if not new_rows:
        return

    new_data = pd.DataFrame( new_rows, columns=CONFLICT_COLUMNS )

    conflicts_data = pd.concat([conflicts_data, new_data] ,ignore_index=True)
    conflicts_data.to_csv(conflicts_path, index=False)


def dataframe_to_records(data, source):

    records = []
    for _, row in data.iterrows():

        timestamp = row["timestamp"].isoformat()

        record_data = {
            column: row[column]
            for column in data.columns
            if column not in ["IDA", "timestamp"]
        }

        records.append({
            "IDA": row["IDA"],
            "source": source,
            "timestamp": timestamp,
            "data": record_data,
        })

    return records
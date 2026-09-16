import json
from pathlib import Path


def serialize_records(data, source):
    """
    Returns list of dictionaries containing:
            - JSON content
            - fusion row metadata
            - intended JSON filename
    """

    prepared_records = []

    for _, row in data.iterrows():

        timestamp = row["timestamp"].isoformat()

        # Create source-specific record data
        record_data = {
            column: row[column] for column in data.columns
            if column not in ["IDA", "timestamp"]
        }

        # JSON record
        json_record = {
            "IDA": row["IDA"],
            "source": source,
            "timestamp": timestamp,
            "data": record_data,
        }

        # Intended JSON filename
        filename = (
            f"{row['IDA']}_{source}_{timestamp.replace(':', '-')}.json"
        )

        # Fusion table row
        fusion_row = {
            "IDA": row["IDA"],
            "source": source,
            "timestamp": timestamp,
            "data": f"records/{filename}",
        }

        prepared_records.append({
            "json_record": json_record,
            "fusion_row": fusion_row,
            "filename": filename,
        })

    return prepared_records
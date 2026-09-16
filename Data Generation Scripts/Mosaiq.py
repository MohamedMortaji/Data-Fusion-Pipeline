from pathlib import Path
from datetime import datetime
import random

import pandas as pd
from mosaiq_config import MOSAIQ_CONFIG

def generate_mosaiq_records(config):

    if config["random_seed"] is not None:
        random.seed(config["random_seed"])

    records = []

    start_timestamp = config["start_date"].timestamp()
    end_timestamp = config["end_date"].timestamp()

    for ida in config["IDAS"]:

        # Random number of records per  patient
        number_of_records = random.randint(
            config["min_records_per_ida"],
            config["max_records_per_ida"])

        # Generate unique timestamps
        timestamps = set()
        while len(timestamps) < number_of_records:
            random_timestamp = random.uniform(start_timestamp, end_timestamp)
            timestamp = datetime.fromtimestamp(random_timestamp)
            timestamps.add(timestamp)

        timestamps = sorted(timestamps)

        # Generate patient-level information once
        diagnosis = random.choice(
            list(config["diagnosis_to_site"].keys())
        )
        treatment_site = config["diagnosis_to_site"][diagnosis]
        machine_id = random.choice(config["machines"])

        for index, timestamp in enumerate(timestamps):
            if index == 0:
                event_type = random.choice(["consultation","treatment planning"])
                treatment_status = "planned"
                dose = 0

            else:
                event_type = random.choice(config["event_types"])
                treatment_status = random.choice(config["treatment_statuses"])
                # Only treatment-related events have a dose
                if event_type in ["treatment","treatment followup"]:
                    dose = round( random.uniform(*config["dose_range_gy"]),1)
                else:
                    dose = 0

            #Append patient record
            record = {
                "IDA": ida,
                "timestamp": timestamp.isoformat(),
                "event_type": event_type,
                "diagnosis": diagnosis,
                "treatment_site": treatment_site,
                "treatment_status": treatment_status,
                "dose": dose,
                "machine_id": machine_id
            }
            records.append(record)

    #Output Final Mosaic Ordered Dataframe
    df = pd.DataFrame(records,columns=config["columns"])
    df = df.sort_values(["IDA", "timestamp"]).reset_index(drop=True)
    return df


def main():
    
    output_path = Path(MOSAIQ_CONFIG["output_file"])

    df = generate_mosaiq_records(MOSAIQ_CONFIG)
    df.to_csv(output_path,index=False)

    print(f"Generated {len(df)} Mosaiq records.")
    print(f"Saved to: {output_path.resolve()}")
    print(df.to_string())


if __name__ == "__main__":
    main()
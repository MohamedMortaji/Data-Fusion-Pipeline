from pathlib import Path
from datetime import datetime
import random

import pandas as pd
from myoncare_config import MYONCARE_CONFIG

def generate_myoncare_records(config):

    if config["random_seed"] is not None:
        random.seed(config["random_seed"])

    records = []

    start_timestamp = config["start_date"].timestamp()
    end_timestamp = config["end_date"].timestamp()

    for ida in config["IDAS"]:

        # Each IDA gets between 2 and 4 records.
        number_of_records = random.randint(
            config["min_records_per_ida"],
            config["max_records_per_ida"]
        )

        # Generate unique timestamps
        timestamps = set()
        while len(timestamps) < number_of_records:
            random_timestamp = random.uniform(start_timestamp, end_timestamp)
            timestamp = datetime.fromtimestamp(random_timestamp)
            timestamps.add(timestamp)
        
        timestamps = sorted(timestamps)

        for timestamp in timestamps:
            record = {
                "IDA": ida,
                "timestamp": timestamp.isoformat(),
                "questionnaire": random.choice(config["questionnaires"]),
                "pain_score": random.randint(*config["score_ranges"]["pain_score"]),
                "fatigue_score": random.randint(*config["score_ranges"]["fatigue_score"]),
                "nausea_score": random.randint(*config["score_ranges"]["nausea_score"]),
                "recovery_score": random.randint(*config["score_ranges"]["recovery_score"]),
            }

            records.append(record)

    #Output Final Myoncare Ordered Dataframe
    df = pd.DataFrame(records,columns=config["columns"])
    df = df.sort_values(["IDA", "timestamp"]).reset_index(drop=True)
    return df


def main():

    output_path = Path(MYONCARE_CONFIG["output_file"])

    df = generate_myoncare_records(MYONCARE_CONFIG)
    df.to_csv(output_path,index=False)

    print(f"Generated {len(df)} Myoncare records.")
    print(f"Saved to: {output_path.resolve()}")
    print(df.to_string())


if __name__ == "__main__":
    main()
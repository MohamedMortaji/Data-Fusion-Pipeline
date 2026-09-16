from datetime import datetime

MYONCARE_CONFIG = {
    "IDAS": [1001, 1002, 1003, 1004,
            1005, 1006, 1007, 1008,
    ],

    "columns": [
        "IDA",
        "timestamp",
        "questionnaire",
        "pain_score",
        "fatigue_score",
        "nausea_score",
        "recovery_score",
    ],

    "min_records_per_ida": 2,
    "max_records_per_ida": 4,

    # Random timestamps will be generated between these dates.
    "start_date": datetime(2026, 1, 1, 0, 0, 0),
    "end_date": datetime(2027, 9, 16, 23, 59, 59),

    "questionnaires": [
        "treatment followup",
        "weekly checkup",
        "monthly checkup"
    ],

    # Score ranges
    "score_ranges": {
        "pain_score": (0, 10),
        "fatigue_score": (0, 10),
        "nausea_score": (0, 10),
        "recovery_score": (0, 10),
    },

    "output_file": "myoncare_sample_new.csv",
    "random_seed": 42,
}

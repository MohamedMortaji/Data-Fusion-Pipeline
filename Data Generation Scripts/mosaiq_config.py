from datetime import datetime

MOSAIQ_CONFIG = {
    "IDAS": [
        1001, 1002, 1003, 1004, 1005,
        1006, 1007, 1008, 1009, 1010,
    ],

    "columns": [
        "IDA",
        "timestamp",
        "event_type",
        "diagnosis",
        "treatment_site",
        "treatment_status",
        "dose",
        "machine_id",
    ],

    "min_records_per_ida": 2,
    "max_records_per_ida": 4,

    # Random timestamps will be generated between these dates.
    "start_date": datetime(2026, 1, 1, 0, 0, 0),
    "end_date": datetime(2027, 9, 16, 23, 59, 59),

    "event_types": [
        "consultation",
        "treatment",
        "treatment followup",
        "imaging",
        "treatment planning",
    ],

    "diagnosis_to_site": {
        "lung cancer": "lung",
        "breast cancer": "breast",
        "prostate cancer": "prostate",
        "head and neck cancer": "head and neck",
        "brain tumor": "brain",
    },

    "treatment_statuses": [
        "planned",
        "active",
        "completed",
        "followup",
    ],

    "machines": [
        "LINAC-01",
        "LINAC-02",
        "LINAC-03",
        "LINAC-04",
    ],

    "dose_range_gy": (20, 70),
    
    "output_file": "mosaiq_sample_new.csv",
    "random_seed": 5,
}

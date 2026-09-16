# Preliminary Preprocessing Steps:
#     Remove completely empty rows
#     Standardize column names
#     Remove whitespace from string values
#     Standardize key fields (IDA & timestamp)
#     Sort Rows chronologically

import pandas as pd

def preprocess_mosaiq(data):
    """
    Apply preliminary preprocessing to Mosaiq data.
    """
    data = data.copy()

    data = data.dropna(how="all")

    data.columns = data.columns.str.strip()

    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].str.strip()

    data["IDA"] = data["IDA"].astype(int)
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    data = data.sort_values(["IDA", "timestamp"]).reset_index(drop=True)

    return data


def preprocess_myoncare(data):
    """
    Apply preliminary preprocessing to Myoncare data.
    """
    data = data.copy()

    data = data.dropna(how="all")

    data.columns = data.columns.str.strip()

    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].str.strip()

    data["IDA"] = data["IDA"].astype(int)
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    data = data.sort_values(["IDA", "timestamp"]).reset_index(drop=True)

    return data


def preprocess_source_data(mosaiq_data, myoncare_data):

    mosaiq_data = preprocess_mosaiq(mosaiq_data)
    myoncare_data = preprocess_myoncare(myoncare_data)
    return mosaiq_data, myoncare_data
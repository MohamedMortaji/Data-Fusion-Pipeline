from pathlib import Path
import pandas as pd


def import_mosaiq(file_path):
    """
    Placeholder Import function for preliminary testing.
    """
    return pd.read_csv(file_path)


def import_myoncare(file_path):
    """
    Placeholder Import function for preliminary testing.
    """
    return pd.read_csv(file_path)


def import_source_data(mosaiq_path, myoncare_path):

    mosaiq_data = import_mosaiq(mosaiq_path)
    myoncare_data = import_myoncare(myoncare_path)
    return mosaiq_data, myoncare_data


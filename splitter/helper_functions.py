"""This module contains helper functions for the splitter module."""
import pandas as pd


def read_csv(file_name: str):
    """Read a csv file and return a pandas dataframe.

    Args:
        file_name: The name of the file to read.
    """
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        df = pd.read_csv(file_name)
    return df

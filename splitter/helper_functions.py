"""This module contains helper functions for the splitter module."""
import pandas as pd
import configparser
from main_helper import timeit


@timeit
def read_csv(file_name: str) -> pd.DataFrame:
    """Read a csv file and return a pandas dataframe.

    Args:
        file_name: The name of the file to read.
    """
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        df = pd.read_csv(file_name)
    return df


def read_config(file_name: str) -> configparser.ConfigParser:
    """Read a config file and return a configparser object."""
    config = configparser.ConfigParser()
    config.read(file_name)
    return config


def collect_columns_names(config) -> list:
    """Collect all columns names from a config file and return a list of column names."""
    columns = []
    for key in config['ColumnNames']:
        columns.append(config['ColumnNames'][key])
    return columns
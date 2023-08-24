"""This module contains helper functions for the splitter module."""
import pandas as pd
import configparser
from main_helper import timeit


@timeit
def read_csv(file_name: str, limit_columns: list[str] = None) -> pd.DataFrame:
    """Read a csv file and return a pandas dataframe.

    Args:
        file_name: The name of the file to read.
        limit_columns: A list of column names to limit the dataframe to. (default: None)
    """
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        if limit_columns is not None:
            df = pd.read_csv(file_name, usecols=limit_columns)
        else:
            df = pd.read_csv(file_name)
    return df


def read_config(file_name: str) -> configparser.ConfigParser:
    """Read a config file and return a configparser object."""
    config = configparser.ConfigParser(interpolation=None)
    config.read(file_name)
    return config


def collect_columns_names(config: configparser.ConfigParser) -> list[str]:
    """Collect all columns names from a config file and return a list of column names."""
    columns = []
    for key in config['ColumnNames']:
        columns.append(config['ColumnNames'][key])
    return columns

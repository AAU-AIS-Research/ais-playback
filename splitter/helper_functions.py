"""This module contains helper functions for the splitter module."""
import pandas as pd
import os
import configparser


def read_csv(file_name: str, config: configparser.ConfigParser) -> pd.DataFrame:
    """Read a csv file and return a pandas dataframe.

    Args:
        file_name: The name of the file to read.
        limit_columns: A list of column names to limit the dataframe to. (default: None)
    """
    seperator = config['DataSource']['separator']
    encoding = config['DataSource']['encoding']

    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        df = pd.read_csv(file_name, sep=seperator, encoding=encoding)
    return df


def read_config(file_name: str) -> configparser.ConfigParser:
    """Read a config file and return a configparser object."""
    config = configparser.ConfigParser(interpolation=None)

    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"Config file not found: {file_name}")

    config.read(file_name)

    return config

# DEAD CODE (previously used with read_csv)
def collect_columns_names(config: configparser.ConfigParser) -> list[str]:
    """Collect all columns names from a config file and return a list of column names."""
    columns = []
    for key in config['ColumnNames']:
        columns.append(config['ColumnNames'][key])
    return columns

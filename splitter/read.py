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
    na_values = ['NaN', 'Unknown', 'nan']

    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        dataframe = pd.read_csv(file_name, sep=seperator, encoding=encoding, na_values=na_values, keep_default_na=False)
    return dataframe


def read_config(file_name: str) -> configparser.ConfigParser:
    """Read a config file and return a configparser object."""
    config = configparser.ConfigParser(interpolation=None)

    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"Config file not found: {file_name}")

    config.read(file_name)

    return config

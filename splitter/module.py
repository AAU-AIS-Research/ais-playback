"""Module for splitting AIS data into files by vessel by day."""

import pandas as pd
import multiprocessing as mp
import os
from splitter.helper_functions import read_csv, read_config, collect_columns_names
from main_helper import collect_files, timeit


def save_to_csv(dataframe, config):
    """Save the dataframe to a csv file.

    Args:
        dataframe: The dataframe to save.
    """



    return None


def sort_by_temporal(dataframe_list, config):
    """Sort dataframe by temporal data.

    Args:
        dataframe_list: The list of dataframes to sort.
        config: A configparser object containing the configuration.
    """
    datetime_format = config['ColumnNames']['datetime-format']
    temporal_column = config['ColumnNames']['timestamp']

    for df in dataframe_list:
        df.sort_values(by=temporal_column, inplace=True)

    return dataframe_list


def split_by_time(dataframe, config):
    """Sort the vessel temporal data.

    Args:
        dataframe: The dataframe to split.
        config: A configparser object containing the configuration.
    """
    df = dataframe


    return df


@timeit
def split_by_vessel(dataframe, config):
    """Split the AIS data by vessel.

    Args:
        dataframe: The dataframe to split.
        config: A configparser object containing the configuration.
    """
    df = dataframe
    vessel_mmsi = config['ColumnNames']['mmsi']
    vessel_mmsi_list = df[vessel_mmsi].unique().tolist()

    df_splits = []
    for group in df.groupby(vessel_mmsi):
        df_splits.append(group[1])

    if len(df_splits) != len(vessel_mmsi_list):
        raise ValueError("The number of splits does not match the number of unique vessels")

    return df_splits


def split(config_file: str):
    """Split the AIS data.

    Args:
        config_file: The name of the config file to use.
    """
    config_path = os.path.abspath("./configs/" + config_file)
    config = read_config(config_path)

    files = collect_files(config)
    columns = collect_columns_names(config)

    for file in files:
        print(f'Splitting file: {file}')
        df = read_csv(file)

        # Drop columns that are not needed
        df.drop(df.columns.difference(columns), axis=1, inplace=True)

        df.dropna(subset=columns, inplace=True)

        df_split = split_by_vessel(df, config)

        df_split = sort_by_temporal(df_split, config)

        df_split = split_by_time(df_split, config)

        for df in df_split:
            save_to_csv(df, config)


    # TODO: After split by vessel, use multiprocessing to sort and split by time

    return None

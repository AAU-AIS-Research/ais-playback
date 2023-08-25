"""Module for splitting AIS data into files by vessel by day."""
import pandas as pd
import os
from splitter.helper_functions import read_csv, read_config
from main_helper import collect_files
import configparser

from datetime import datetime, timedelta
from time import perf_counter


def _split_by_time(dataframe: pd.DataFrame) -> list[pd.DataFrame]:
    """Split the AIS data by time.

    Args:
        dataframe: The dataframe to split.
    """
    date_column = 'date'
    time_column = 'time'
    df = dataframe
    df_lst = []

    df.sort_values(by=[date_column, time_column], inplace=True, ascending=True)
    for group in df.groupby(date_column):
        df_lst.append(group[1])

    return df_lst


def _split_by_vessel(dataframe: pd.DataFrame, config: configparser.ConfigParser) -> list[pd.DataFrame]:
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


def _split_timestamp_column(dataframe: pd.DataFrame, config: configparser.ConfigParser) -> pd.DataFrame:
    """Split the datetime column into date and time columns.

    Args:
        dataframe: The dataframe to split.
        config: A configparser object containing the configuration.
    """
    temporal_column = config['ColumnNames']['timestamp']
    timestamp_format = config['DataSource']['timestamp-format']

    dataframe['date'] = pd.to_datetime(dataframe[temporal_column], format=timestamp_format).dt.date
    dataframe['time'] = pd.to_datetime(dataframe[temporal_column], format=timestamp_format).dt.time

    dataframe.drop(columns=[temporal_column], inplace=True)

    return dataframe


def split(*, config_path: str, source_path: str, target_path: str, prune_to_date: datetime.date = None) -> None:
    """Split the AIS data.

    Args:
        config_path: The path to the config file.
        source_path: The path to the source data. If a folder, all files in the folder will be split.
        target_path: The path to the target folder. Will be created if it does not exist.
        prune_to_date: The date to prune the data to. If None, all data will be split. (default: None)
    """
    total_start_time = perf_counter()
    config_name = os.path.basename(config_path)

    print(f'Splitting AIS data using config: {config_name} at {datetime.now()}')
    print(f'Source path: {source_path}')
    print(f'Target path: {target_path}')

    config = read_config(config_path)
    files = collect_files(source_path, config['DataSource']['filetype'])
    current_file_number = 0
    number_of_files = len(files)

    print(f'Number of files to split: {number_of_files}')

    for file in files:
        start_time_file = perf_counter()
        file_name = os.path.basename(file)

        current_file_number += 1
        print(f'Attempting to split file {current_file_number} of {number_of_files}: {file_name} at {datetime.now()}')

        start_time_read = perf_counter()
        df = read_csv(file, config)

        print(f'File {file_name} read successfully in '
              f'{timedelta(seconds=(perf_counter() - start_time_read))} at {datetime.now()}')

        # Drop rows with missing values
        size_before = df.shape[0]
        df.dropna(subset=[
            config['ColumnNames']['mmsi'],
            config['ColumnNames']['timestamp'],
            config['ColumnNames']['lat'],
            config['ColumnNames']['long'],
        ] ,inplace=True)
        size_after = df.shape[0]
        print(f'Dropped {size_before - size_after} rows with missing values for MMSI, timestamp, lat or long')

        # Split timestamp column into date and time
        _split_timestamp_column(df, config)

        # Rename columns to ensure consistent output
        df.rename(columns={
            config['ColumnNames']['mmsi']: 'MMSI',
            config['ColumnNames']['imo']: 'IMO',
            config['ColumnNames']['status']: 'nav_status',
            config['ColumnNames']['sog']: 'SOG',
            config['ColumnNames']['lat']: 'lat',
            config['ColumnNames']['long']: 'long',
            config['ColumnNames']['cog']: 'COG',
            config['ColumnNames']['heading']: 'heading',
        }, inplace=True)

        # Ensure target path exists, create it if it does not.
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # Split by date then vessel
        vessel_mmsi = config['ColumnNames']['mmsi']
        for dataframe_date in _split_by_time(df):
            date = dataframe_date['date'].iloc[0]

            # If date is before or after prune_to_date, skip
            if prune_to_date is not None and date != prune_to_date:
                break

            print(f'Splitting vessels for date {date} at {datetime.now()}')

            start_time_date = perf_counter()

            # Create date folder if it does not exist
            if not os.path.exists(os.path.join(target_path, str(date))):
                os.makedirs(os.path.join(target_path, str(date)))

            # Split by vessel
            for dataframe_vessel in _split_by_vessel(dataframe_date, config):
                mmsi = dataframe_vessel[vessel_mmsi].iloc[0]

                # Write to file
                dataframe_vessel.to_csv(
                    os.path.join(target_path, str(date), str(mmsi) + '.csv'),
                    index=False,
                    sep='|',
                    encoding='utf-8',
                    header=True)

            print(f'Date {date} split successfully in '
                  f'{timedelta(seconds=(perf_counter() - start_time_date))} at {datetime.now()}')

        print(f'File {file_name} split successfully in '
              f'{timedelta(seconds=(perf_counter() - start_time_file))} at {datetime.now()}')

    print(f'Splitting AIS data using config: {config_name} completed successfully in '
          f'{timedelta(seconds=(perf_counter() - total_start_time))} at {datetime.now()}')

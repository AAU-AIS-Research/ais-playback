"""Module for splitting AIS data into files by vessel by day."""

import pandas as pd
import os
from splitter.helper_functions import read_csv, read_config, collect_columns_names
from main_helper import collect_files, timeit


@timeit
def _split_by_time(dataframe):
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


@timeit
def _split_by_vessel(dataframe, config):
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


@timeit
def _split_datetime(df, config):
    """Split the datetime column into date and time columns.

    Args:
        df: The dataframe to split.
        config: A configparser object containing the configuration.
    """
    temporal_column = config['ColumnNames']['timestamp']
    timestamp_format = config['DataSource']['timestamp-format']

    df['date'] = pd.to_datetime(df[temporal_column], format=timestamp_format).dt.date
    df['time'] = pd.to_datetime(df[temporal_column], format=timestamp_format).dt.time

    df.drop(columns=[temporal_column], inplace=True)

    return df


@timeit
def split(config_file: str):
    """Split the AIS data.

    Args:
        config_file: The name of the config file to use.
    """
    print('Splitting data...')

    config_path = os.path.abspath("./configs/" + config_file)
    config = read_config(config_path)

    files = collect_files(config)
    columns = collect_columns_names(config)

    for file in files:
        print(f'Splitting file: {file}')
        df = read_csv(file, columns)

        df.dropna(inplace=True)

        _split_datetime(df, config)

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

        target_folder = config['DataTarget']['path-split']
        vessel_mmsi = config['ColumnNames']['mmsi']
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        for dataframe_date in _split_by_time(df):
            date = dataframe_date['date'].iloc[0]
            if not os.path.exists(os.path.join(target_folder, str(date))):
                os.makedirs(os.path.join(target_folder, str(date)))
            for dataframe_vessel in _split_by_vessel(dataframe_date, config):
                mmsi = dataframe_vessel[vessel_mmsi].iloc[0]
                dataframe_vessel.to_csv(
                    os.path.join(target_folder, str(date), str(mmsi) + '.csv'),
                    index=False,
                    sep='|',
                    encoding='utf-8',
                    header=True)

        print(f'File {file} split successfully')

    print('Done splitting')

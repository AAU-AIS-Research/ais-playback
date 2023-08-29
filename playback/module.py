"""Module for playing back AIS data from files."""
from main_helper import collect_files
import pandas as pd
import datetime
from time import perf_counter, sleep


def playback(*, source_path: str, speed: int, subset: list[str | int] = None,
             start_time: datetime.time = datetime.time.min, stop_time: datetime.time = datetime.time.max) -> None:
    """Play back AIS data from files.

    Args:
        source_path: The path to the source data. If a folder, all files in the folder will be played back.
        speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
        subset: A list of mmsi numbers or vessel names to play back.
         If None, all vessels will be played back. (default: None)
        start_time: The time to start playback. (default: 00:00:00)
        stop_time: The time to stop playback. (default: 23:59:59)
    """
    print(f'Playing back AIS data at {datetime.datetime.now()}')
    print(f'Source path: {source_path}')
    print('Preprocessing data...')

    prepossessing_start_time = perf_counter()
    files = collect_files(source_path, 'csv')
    dataframe = _concat_files_to_dataframe(files)

    print('Sorting data by timestamp...')

    dataframe = dataframe.sort_values(by=['TIMESTAMP'])

    print(f'Pruning data to be within {start_time} and {stop_time}...')
    dataframe = dataframe[
        (dataframe['TIMESTAMP'].dt.time >= start_time) & (dataframe['TIMESTAMP'].dt.time <= stop_time)]

    print(f'Preprocessing complete in {perf_counter() - prepossessing_start_time} seconds at {datetime.datetime.now()}')
    print(f'Playing back data at {speed}x speed from {start_time} to {stop_time}...')

    for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
        print(f'Printing group: {time_group} at speed {speed}x')

        if not dataframe_group.empty:
            # Reset the index to start at 0, else it will continue from the previous group.
            dataframe_group.reset_index(inplace=True, drop=True)
            print(dataframe_group.to_string())

        sleep(1)


def _concat_files_to_dataframe(files: list[str]) -> pd.DataFrame:
    """Concatenate all files into a single dataframe (sorted by timestamp).

    Args:
        files: A list of file paths to concatenate.
    """
    print(f'Concatenating files at {datetime.datetime.now()}')

    if not files:
        raise ValueError('No files found to concatenate.')

    collect_start_time = perf_counter()
    dataframe_list = []
    number_of_files = len(files)

    print(f'Found {number_of_files} files.')

    for file in files:
        if files.index(file) % 100 == 0:
            percentage_done = round(files.index(file) / number_of_files * 100, 2)
            print(f'\rConcatenating file {files.index(file)} of {number_of_files} ({percentage_done}%)', end='')

        columns_to_read = ['MMSI', 'IMO', 'STATUS', 'SOG', 'LON', 'LAT', 'COG', 'HEADING', 'DATE', 'TIME']
        columns_types = {'MMSI': int, 'IMO': 'Int64', 'STATUS': str, 'SOG': float, 'LON': float, 'LAT': float,
                         'COG': float, 'HEADING': float}
        columns_datetime = ['DATE', 'TIME']
        columns_order = ['MMSI', 'IMO', 'STATUS', 'SOG', 'LON', 'LAT', 'COG', 'HEADING', 'TIMESTAMP']

        dataframe = pd.read_csv(file,
                                encoding='utf-8',
                                sep='|',
                                usecols=columns_to_read,
                                dtype=columns_types,
                                na_values=['Unknown'],
                                parse_dates={'TIMESTAMP': columns_datetime},
                                date_format='%Y-%m-%d %H:%M:%S')[columns_order]

        dataframe_list.append(dataframe)

    dataframe = pd.concat(dataframe_list)
    collect_stop_time = perf_counter()

    print(f'Concatenated files in {collect_stop_time - collect_start_time} seconds at {datetime.datetime.now()}')

    return dataframe

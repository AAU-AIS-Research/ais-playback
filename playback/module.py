"""Module for playing back AIS data from files."""
from main_helper import collect_files
import pandas as pd
from datetime import datetime, timedelta, time
from time import perf_counter, sleep
from playback.processors import Printer
from playback.processors.parent import AbstractPlaybackProcessor
import os


def playback(*,
             source_path: str,
             prepro_path: str = None,
             speed: int,
             subset: list[str | int] = None,  # Not used yet
             start_time: datetime.time = time.min, stop_time: datetime.time = time.max,
             processor: type[AbstractPlaybackProcessor] = Printer,
             ) -> None:
    """Play back AIS data from files.

    Args:
        source_path: The path to the source data. If a folder, all files in the folder will be played back.
        prepro_path: Defines both the path to load preprocessed data from and the path to save preprocessed data to
        if the data has not already been preprocessed. If None, the data will not be saved.
        If a folder, the preprocessed data will be saved to the folder with the same name as the source file or folder.
        (default: None)
        speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
        subset: A list of mmsi numbers or vessel names to play back.
         If None, all vessels will be played back. (default: None)
        start_time: The time to start playback. (default: 00:00:00)
        stop_time: The time to stop playback. (default: 23:59:59)
        processor: The processor class to use for processing the data. (default: Printer)
    """
    print(f'Playing back AIS data at {datetime.now()}')
    print(f'Source path: {source_path}')

    if speed < 1 or speed > 900:
        raise ValueError('Speed must be between 1 and 900.')

    # Logic for loading preprocessed data, or preprocessing the data if it has not already been preprocessed.
    if prepro_path is None:
        print('No preprocessed data path given. Preprocessing data...')
        dataframe = _preprocessing_playback(source_path, start_time, stop_time)
    elif os.path.isdir(prepro_path):
        # If the prepro_path is a folder, the preprocessed data will be saved to the folder with the same name as the
        # source file or folder. Therefore, a check is made to see if the preprocessed data already exists.
        prepro_path = os.path.join(prepro_path, os.path.basename(source_path))
        if os.path.isfile(prepro_path + '.parquet'):
            print(f'Found preprocessed data at {prepro_path}. Loading...')
            dataframe = pd.read_parquet(prepro_path + '.parquet')
        else:
            print(f'No preprocessed data found at {prepro_path}. Preprocessing data...')
            dataframe = _preprocessing_playback(source_path, start_time, stop_time, prepro_path)
    else:
        # Ensure that the prepro_path ends with .parquet
        prepro_path = prepro_path + '.parquet' if prepro_path and not prepro_path.endswith('.parquet') else prepro_path
        if os.path.isfile(prepro_path):
            print(f'Found preprocessed data at {prepro_path}. Loading...')
            dataframe = pd.read_parquet(prepro_path)
        else:
            print(f'No preprocessed data found at {prepro_path}. Preprocessing data...')
            dataframe = _preprocessing_playback(source_path, start_time, stop_time, prepro_path)

    print(f'Playing back data at {speed}x speed from {start_time} to {stop_time}...')

    data_processor = processor()

    data_processor.playback_begun()
    for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
        print(f'Printing group: {time_group} at speed {speed}x')

        if not dataframe_group.empty:
            # Reset the index to start at 0, else it will continue from the previous group.
            dataframe_group.reset_index(inplace=True, drop=True)

            data_processor.process_playback(dataframe_group)

        sleep(1)
    data_processor.playback_ended()


def _preprocessing_playback(
        source_path: str,
        start_time: datetime.time,
        stop_time: datetime.time,
        save_path: str = None
) -> pd.DataFrame:
    """Preprocess the AIS data for playback.

    This includes concatenating files, sorting by timestamp, and pruning to a time interval.

    Args:
        source_path: The path to the source data. If a folder, all files in the folder will be preprocessed.
        start_time: The beginning of the time interval to prune to.
        stop_time: The end of the time interval to prune to.
        save_path: The path to save the preprocessed data to. If None, the data will not be saved. (default: None)
    """
    print('Preprocessing data...')

    prepossessing_start_time = perf_counter()
    files = collect_files(source_path, 'csv')
    dataframe = _concat_files_to_dataframe(files)

    print('Sorting data by timestamp...')

    dataframe = dataframe.sort_values(by=['TIMESTAMP'])

    print(f'Pruning data to be within {start_time} and {stop_time}...')

    dataframe = dataframe[
        (dataframe['TIMESTAMP'].dt.time >= start_time) & (dataframe['TIMESTAMP'].dt.time <= stop_time)]

    print(f'Preprocessing complete in {timedelta(seconds=perf_counter() - prepossessing_start_time)} '
          f'at {datetime.now()}')

    if save_path is not None:
        # Ensure that the save path ends with .parquet
        save_path = save_path + '.parquet' if not save_path.endswith('.parquet') else save_path
        print(f'Saving preprocessed data to {save_path}...')
        dataframe.to_parquet(save_path, index=False)
        print(f'Saved preprocessed data to {save_path} at {datetime.now()}')

    return dataframe


def _concat_files_to_dataframe(files: list[str]) -> pd.DataFrame:
    """Concatenate all files into a single dataframe (sorted by timestamp).

    Args:
        files: A list of file paths to concatenate.
    """
    print(f'Concatenating files at {datetime.now()}')

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

    print(f'Concatenated files in {timedelta(seconds=(perf_counter() - collect_start_time))} at {datetime.now()}')

    return dataframe

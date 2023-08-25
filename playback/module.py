"""Module for playing back AIS data from files."""
import os
from main_helper import collect_files
import pandas as pd
import datetime
import time


# TODO: Find better parameter name than subset
def playback(*, source_path: str, target_path: str, speed: int, subset: list[str | int] = None,
             start_time: datetime.time = datetime.time.min, stop_time: datetime.time = datetime.time.max) -> None:
    """Play back AIS data from files.

    Args:
        source_path: The path to the source data. If a folder, all files in the folder will be played back.
        target_path: The path to the target folder. Will be created if it does not exist.
        speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
        subset: A list of mmsi numbers or vessel names to play back. If None, all vessels will be played back. (default: None)
        start_time: The time to start playback. (default: 00:00:00)
        stop_time: The time to stop playback. (default: 23:59:59)
    """

    print(f'Playing back AIS data at {datetime.datetime.now()}')
    print(f'Source path: {source_path}')
    print(f'Target path: {target_path}')

    total_start_time = time.perf_counter()
    files = collect_files(source_path, 'csv')

    dataframe_list = []
    for file in files:
        file_name = os.path.basename(file)

        # TODO: Fix so it handles date and time correctly
        dataframe = pd.read_csv(file, encoding='utf-8', sep='|')

        # Remove rows outside the time interval
        dataframe = dataframe[(dataframe['time'] >= start_time) & (dataframe['time'] <= stop_time)]

        # Remove rows outside the subset

        # Group by time period based on speed
        dataframe_list = dataframe.groupby(pd.Grouper(key='time', freq=f'{speed}S'))

        # Emit each group
        for group in dataframe_list:
            print('Emitting group')
            print(group)
            print('Sleeping')
            time.sleep(1)

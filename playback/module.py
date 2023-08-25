"""Module for playing back AIS data from files."""
import os
from main_helper import collect_files
import pandas as pd
import datetime
import time


def _adjust_speed(dataframe: pd.DataFrame, speed: int) -> pd.DataFrame:
    """Adjust the speed of the playback, removing rows from the dataframe.

    Args:
        dataframe: The dataframe to adjust.
        speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
    """
    if not 1 <= speed <= 900:
        raise ValueError("Speed must be between 1 and 900")



    return dataframe.iloc[::speed]

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

        dataframe = pd.read_csv(file)

        dataframe = _adjust_speed(dataframe, speed)


        # Keep 1 entry for each second




    # df.to_csv(os.path.join(target_path, file_name), index=False)

    print(f'Playback complete in {time.perf_counter() - total_start_time} seconds at {datetime.datetime.now()}')


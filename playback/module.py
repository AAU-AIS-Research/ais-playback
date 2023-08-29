"""Module for playing back AIS data from files."""
from main_helper import collect_files
import pandas as pd
import datetime


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

    files = collect_files(source_path, 'csv')

    for file in files:
        print(f'Playing back file: {file}')

        cols_to_read = ['MMSI', 'IMO', 'STATUS', 'SOG', 'LON', 'LAT', 'COG', 'HEADING', 'DATE', 'TIME']
        dataframe = pd.read_csv(file, encoding='utf-8', sep='|', usecols=cols_to_read)

        # Create temporary datetime column from date and time columns.
        # This must be done before the groupby operation as Pandas does not support grouping by time.
        dataframe['TIMESTAMP'] = pd.to_datetime(
            dataframe['DATE'].astype(str) + ' ' + dataframe['TIME'].astype(str),
            format='%Y-%m-%d %H:%M:%S')
        dataframe.drop(columns=['DATE', 'TIME'], inplace=True)

        # Remove rows outside the start and stop time.
        dataframe = dataframe[
            (dataframe['TIMESTAMP'].dt.time >= start_time) & (dataframe['TIMESTAMP'].dt.time <= stop_time)]

        for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
            print(f'Printing group: {time_group}')
            if not dataframe_group.empty:
                # Reset the index to start at 0, else it will continue from the previous group.
                dataframe_group.reset_index(inplace=True, drop=True)
                print(dataframe_group.to_string())

"""Module for playing back AIS data from files."""
from helper_functions import collect_files
from datetime import datetime, timedelta, time
from time import perf_counter, sleep
from playback.processors import Printer
from playback.processors.playback_processor import PlaybackProcessor
from playback.constants import METADATA_KEY
import pandas as pd
import os
import pyarrow as pa
import pyarrow.parquet as pq
import json
import logging

class Playback:
    """A class for playing back AIS data from files."""

    def __init__(self,
                 *,
                 source_path: str,
                 prepro_folder: str | None = None,
                 subset: list[str | int] = None,  # Not used yet, but will be used to subset the data.
                 start_time: datetime.time = time.min,
                 stop_time: datetime.time = time.max,
                 player: str = 'simple',
                 processor: PlaybackProcessor = Printer(),
                 verbose: bool = True
                 )-> None:
        """Initialise the playback class.

        Args:
            source_path: The path to the source data. If a folder, all files in the folder will be played back.
            prepro_folder: Defines both the path to load preprocessed data from and the path to save preprocessed data to
            if the data has not already been preprocessed. If None, the preprossed data will not be saved.
            (default: None)
            subset: A list of mmsi numbers or vessel names to play back.
            If None, all vessels will be played back. (default: None)
            start_time: The time to start playback. (default: 00:00:00)
            stop_time: The time to stop playback. (default: 23:59:59)
            processor: The processors class to use for processing the data. (default: Printer)
        """
        # Path related variables
        self.source_path = source_path
        self.prepro_folder = prepro_folder
        self.prepro_base_folder = os.path.join(prepro_folder, os.path.basename(source_path)) \
            if prepro_folder is not None else None
        self.prepro_derived_folder = os.path.join(prepro_folder, 'derived') if prepro_folder is not None else None

        # Filter related variables
        self.subset = subset
        self.start_time = start_time
        self.stop_time = stop_time
        self.player = player

        # Other variables
        self.verbose = verbose
        self.processor = processor

    @property
    def hash_filter_parameters(self):
        """Hashes the parameters which effect the derived data, and returns the hash.

        Used to check if the derived data has already been preprocessed and stored in the preprocessed data folder.
        """
        return hash(tuple([self.subset, self.start_time, self.stop_time, self.player]))

    def play(self, speed: int = 1, no_sleep: bool = False):
        """Play back AIS data from files by emitting groups of data for each time interval.

        Args:
            speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
            no_sleep: If True, the playback will not sleep between emissions. (default: False)
        """
        print(f'Playing back AIS data at {datetime.now()}')
        print(f'Source path: {self.source_path}')

        if speed < 1 or speed > 900:
            raise ValueError('Speed must be between 1 and 900.')

        dataframe = self._preprocess_or_load()

        for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
            print(f'Emitting group: {time_group} at speed {speed}x')

            if not dataframe_group.empty:
                # Reset the index to start at 0, else it will continue from the previous group.
                dataframe_group.reset_index(inplace=True, drop=True)

                self.processor.process(dataframe_group)

            sleep(1) if not no_sleep else None

    def _preprocess_or_load(self) -> pd.DataFrame:
        """Preprocess the data if it has not already been preprocessed, or load the preprocessed data if it has."""
        if self.prepro_folder is None:
            print('No preprocessed data path given. Preprocessing data...')
            dataframe = self._preprocess_playback(save=False)
            return dataframe

        if not os.path.isdir(self.prepro_folder):
            raise ValueError('prepro_folder must be a folder.')

        self._create_preprocessed_folders()

        if not os.path.exists(os.path.join(self.prepro_folder, 'base.parquet')):
            print('Preprocessing base data...')
            self._preprocess_playback_base()

        if os.path.exists(os.path.join(self.prepro_derived_folder, f'{self.hash_filter_parameters}.parquet')):
            print('Loading preprocessed data...')
            dataframe = self._load_playback()
            return dataframe
        else:
            print('Preprocessing altered data...')
            dataframe = self._preprocess_playback()
            return dataframe

    def _load_playback(self, hash: str) -> pd.DataFrame:
        """Load the preprocessed data from the preprocessed data folder."""

        pass

    def _preprocess_playback_base(self) -> pd.DataFrame:
        """Preprocess the source AIS data for further processing as a base for the altered data."""

        pass

    def _preprocess_playback(self, save: bool = True) -> pd.DataFrame:
        """Preprocess the source AIS data for playback.

        This includes concatenating files, sorting by timestamp, and pruning to a time interval.

        Args:
            save: If True, the preprocessed data will be saved to the preprocessed data folder.
        """
        print('Preprocessing data...')

        prepossessing_start_time = perf_counter()
        files = collect_files(self.source_path, 'csv')
        dataframe = self._concat_files_to_dataframe(files)

        return dataframe




    def _create_preprocessed_folders(self) -> None:
        """Creates the folder structure for the preprocessed data."""
        if not os.path.exists(self.prepro_folder):
            os.makedirs(self.prepro_folder)

        if not os.path.exists(self.prepro_derived_folder):
            os.makedirs(self.prepro_derived_folder)


def playback(*,
             source_path: str,
             prepro_path: str | None = None,
             speed: int,
             subset: list[str | int] = None,  # Not used yet, but will be used to subset the data.
             start_time: datetime.time = time.min, stop_time: datetime.time = time.max,
             processor: PlaybackProcessor = Printer(),
             no_sleep: bool = False
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
        processor: The processors class to use for processing the data. (default: Printer)
        no_sleep: If True, the playback will not sleep between emitting groups. (default: False)
    """
    print(f'Playing back AIS data at {datetime.now()}')
    print(f'Source path: {source_path}')

    if speed < 1 or speed > 900:
        raise ValueError('Speed must be between 1 and 900.')

    # Metadata, verifies that parameters which effect the stored data, are the same between playback sessions.
    local_param = locals()
    # Not necessary to check for these parameters as they don't affect the data which is stored.
    no_save_param = ['source_path', 'no_sleep', 'speed', 'processors']
    metadata = {key: str(local_param[key]) for key in local_param.keys() if key not in no_save_param}

    dataframe = _preprocess_or_load(prepro_path, source_path, start_time, stop_time, metadata)

    print(f'Playing back data at {speed}x speed from {start_time} to {stop_time}...')

    playback_processor = processor

    playback_processor.begun()

    for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
        print(f'Emitting group: {time_group} at speed {speed}x')

        if not dataframe_group.empty:
            # Reset the index to start at 0, else it will continue from the previous group.
            dataframe_group.reset_index(inplace=True, drop=True)

            playback_processor.process(dataframe_group)

        sleep(1) if not no_sleep else None

    playback_processor.end()


def _preprocess_or_load(prepro_path: str | None,
                        source_path: str,
                        start_time: datetime.time,
                        stop_time: datetime.time,
                        metadata: dict[str, any]
                        ) -> pd.DataFrame:
    """Preprocess the data if it has not already been preprocessed, or load the preprocessed data if it has.

    Args:
        prepro_path: Defines both the path to load preprocessed data from and the path to save preprocessed data to
        if the data has not already been preprocessed. If None, the data will not be saved.
        If a folder, the preprocessed data will be saved to the folder with the same name as the source file or folder.
        (default: None)
        source_path: The path to the source data. If a folder, all files in the folder will be preprocessed.
        start_time: The beginning of the time interval to prune to (inclusive).
        stop_time: The end of the time interval to prune to (inclusive).
        metadata: A dictionary containing the metadata to save to the preprocessed data.
    """
    if prepro_path is None:
        print('No preprocessed data path given. Preprocessing data...')
        dataframe = _preprocessing_playback(source_path, start_time, stop_time)
        return dataframe

    if not os.path.isdir(prepro_path):
        raise ValueError('prepro_path must be a folder.')

    prepro_folder = prepro_path + os.path.basename(source_path)
    prepro_altered_folder = prepro_folder + '/altered'

    if not os.path.exists(prepro_folder):
        os.makedirs(prepro_folder)





def _preprocessing_playback(
        source_path: str,
        start_time: datetime.time,
        stop_time: datetime.time,
        save_path: str = None,
        metadata: dict[str, any] = None
) -> pd.DataFrame:
    """Preprocess the AIS data for playback.

    This includes concatenating files, sorting by timestamp, and pruning to a time interval.

    Args:
        source_path: The path to the source data. If a folder, all files in the folder will be preprocessed.
        start_time: The beginning of the time interval to prune to (inclusive).
        stop_time: The end of the time interval to prune to (inclusive).
        save_path: The path to save the preprocessed data to. If None, the data will not be saved. (default: None)
    """
    print('Preprocessing data...')

    prepossessing_start_time = perf_counter()
    files = collect_files(source_path, 'csv')
    dataframe = _concat_files_to_dataframe(files)

    print('Sorting data by timestamp...')

    dataframe = dataframe.sort_values(by=['TIMESTAMP'])

    print(f'Pruning data to be within {start_time} and {stop_time}...')
    dataframe = dataframe.set_index('TIMESTAMP')
    dataframe = dataframe.between_time(start_time, stop_time)
    dataframe = dataframe.reset_index()

    print(f'Preprocessing complete in {timedelta(seconds=perf_counter() - prepossessing_start_time)} '
          f'at {datetime.now()}')

    if save_path is not None:
        # Reset the index to start at 0
        dataframe = dataframe.reset_index()

        # Ensure that the save path ends with .parquet
        save_path = save_path + '.parquet' if not save_path.endswith('.parquet') else save_path

        print(f'Saving preprocessed data to {save_path}')

        arrow_table = _dataframe_to_arrow_table_with_metadata(dataframe, metadata)
        pq.write_table(arrow_table, save_path)

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

    print(f'\nConcatenated files in {timedelta(seconds=(perf_counter() - collect_start_time))} at {datetime.now()}')

    return dataframe


def _dataframe_to_arrow_table_with_metadata(dataframe: pd.DataFrame, metadata: dict[str, any]) -> pa.Table:
    """Convert a pandas dataframe to an arrow table with metadata.

    Args:
        dataframe: The pandas dataframe to convert.
        metadata: The metadata to add to the arrow table.
    """
    arrow_table = pa.Table.from_pandas(dataframe)
    metadata_content = json.dumps(metadata)
    existing_metadata = arrow_table.schema.metadata
    combined_metadata = {
        METADATA_KEY.encode(): metadata_content.encode(),
        **existing_metadata
    }
    arrow_table = arrow_table.replace_schema_metadata(combined_metadata)

    return arrow_table

"""Module for playing back AIS data from files."""
from helper_functions import collect_files
from datetime import datetime, timedelta, time
from time import perf_counter, sleep
from playback.processors import Printer
from playback.processors.playback_processor import PlaybackProcessor
import pandas as pd
import os
import hashlib as hl


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
                 processor: PlaybackProcessor = Printer()
                 ) -> None:
        """Initialise the playback class.

        Args:
            source_path: The path to the source data. If a folder, all files in the folder will be played back.
            prepro_folder: Defines both the path to load preprocessed data from and the path to save preprocessed data
            to if the data has not already been preprocessed. If None, the preprocessed data will not be saved.
            (default: None)
            subset: A list of filters to derive a subset of data for playback. Not yet implemented.
            If None, all vessels will be played back. (default: None)
            start_time: The time to start playback. (default: 00:00:00)
            stop_time: The time to stop playback. (default: 23:59:59)
            player: The player to use for playback. Determines how the data is loaded and played back.
            (default: 'simple')
            processor: The processors class to use for processing the data. (default: Printer)
        """
        # Path related variables
        self.source_path = source_path
        self.prepro_base_folder = os.path.join(prepro_folder, os.path.basename(source_path)) \
            if prepro_folder is not None else None
        self.prepro_derived_folder = os.path.join(self.prepro_base_folder, 'Derived Data') \
            if prepro_folder is not None else None

        # Filter related variables
        self.subset = subset
        self.start_time = start_time
        self.stop_time = stop_time
        self.player = player

        # Other variables
        self.verbose = verbose
        self.processor = processor

    @property
    def hash_filter_parameters(self) -> str:
        """Create a hash of the filter parameters.

        Used to check if the derived data has already been preprocessed and stored in the preprocessed data folder.
        """
        filter_parameters = (self.subset, self.start_time, self.stop_time, self.player)
        filter_parameters = str(filter_parameters).encode()
        filter_hash = hl.sha256(filter_parameters).hexdigest()

        return filter_hash

    def play(self, speed: int = 1, no_sleep: bool = False) -> None:
        """Play back AIS data from files by emitting groups of data for each time interval.

        Args:
            speed: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
            no_sleep: If True, the playback will not sleep between emissions. (default: False)
        """
        if speed < 1 or speed > 900:
            raise ValueError('Speed must be between 1 and 900.')

        dataframe = self._preprocess_or_load()

        self.processor.begun()

        for time_group, dataframe_group in dataframe.groupby(pd.Grouper(key='TIMESTAMP', freq=f'{speed}S')):
            print(f'Emitting group: {time_group} at speed {speed}x')

            if not dataframe_group.empty:
                # Reset the index to start at 0, else it will continue from the previous group.
                dataframe_group.reset_index(inplace=True, drop=True)

                self.processor.process(dataframe_group)

            sleep(1) if not no_sleep else None

        self.processor.end()

    def _preprocess_or_load(self) -> pd.DataFrame:
        """Preprocess the data if it has not already been preprocessed, or load the preprocessed data if it has."""
        if self.prepro_base_folder is None:
            print('No preprocessed data path given. Preprocessing data...')
            dataframe = self._create_derived_playback()
            return dataframe

        self._create_preprocessed_folders()

        print('Searching for preprocessed data...')
        if not os.path.exists(os.path.join(self.prepro_base_folder, 'base.parquet')):
            print('No preprocessed base data found.')
            self._preprocess_playback_base()

        if os.path.exists(os.path.join(self.prepro_derived_folder, f'{self.hash_filter_parameters}.parquet')):
            print('Preprocessed derived data found.')
            dataframe = self._load_derived_playback()
            return dataframe
        else:
            print('No preprocessed derived data found.')
            dataframe = self._preprocess_playback_derived()
            return dataframe

    def _create_derived_playback(self) -> pd.DataFrame:
        """Create the derived playback data based on the given parameters and return the derived dataframe."""
        # TODO: Implement this. Collect then apply filters?
        start_time = perf_counter()

        dataframe = self._load_source()

        self._date_and_time_to_timestamp(dataframe)

        # Remove columns that are not needed for playback.
        dataframe = dataframe[self._get_columns()]

        dataframe = self._apply_filters(dataframe)

        print(f'Preprocessed derived data finished at {datetime.now()} '
              f'in {timedelta(seconds=(perf_counter() - start_time))}')

        return dataframe

    def _create_preprocessed_folders(self) -> None:
        """Create the folder structure for the preprocessed data."""
        if not os.path.exists(self.prepro_base_folder):
            print(f'No folder structure for preprocessed data found. '
                  f'Creating folder structure at {self.prepro_base_folder}')
            os.makedirs(self.prepro_base_folder)

        if not os.path.exists(self.prepro_derived_folder):
            os.makedirs(self.prepro_derived_folder)

    def _preprocess_playback_base(self) -> None:
        """Preprocess the source AIS data for further processing as a base for the altered data."""
        start_time = perf_counter()

        print(f'Preprocessing base data at {datetime.now()}')

        dataframe = self._load_source()

        self._date_and_time_to_timestamp(dataframe)

        print('Saving base file for preprocessed data...')

        self._save_parquet(dataframe, os.path.join(self.prepro_base_folder, 'base.parquet'))

        print(f'Preprocessed base data finished at {datetime.now()} '
              f'in {timedelta(seconds=(perf_counter() - start_time))}')

    @staticmethod
    def _date_and_time_to_timestamp(dataframe: pd.DataFrame) -> None:
        """Convert the date and time columns to a timestamp column and drop the date and time columns."""
        dataframe['TIMESTAMP'] = pd.to_datetime(dataframe['DATE'] + ' ' + dataframe['TIME'], format='%Y-%m-%d %H:%M:%S')
        dataframe.drop(columns=['DATE', 'TIME'], inplace=True)
        dataframe.sort_values(by=['TIMESTAMP'], inplace=True)

    def _load_derived_playback(self) -> pd.DataFrame:
        """Load the preprocessed data from the preprocessed data folder."""
        print(f'Loading derived data at {datetime.now()}')

        dataframe = pd.read_parquet(os.path.join(self.prepro_derived_folder, f'{self.hash_filter_parameters}.parquet'))

        return dataframe

    def _get_columns(self) -> list[str]:
        """Return a list of columns.

        Used to limit the columns read from the source data or the preprocessed data.
        """
        if self.player == 'simple':
            return ['MMSI', 'IMO', 'NAV STATUS', 'SOG', 'LONGITUDE', 'LATITUDE', 'COG', 'HEADING', 'TIMESTAMP']

        if self.player == 'extended':
            raise NotImplementedError('Extended player not implemented yet.')

    def _preprocess_playback_derived(self) -> pd.DataFrame:
        """Derive a subset of the preprocessed data based on the given parameters.

        The derived data is saved as a parquet file in the preprocessed data folder and returned as a dataframe.
        """
        start_time = perf_counter()
        print(f'Preprocessing derived data at {datetime.now()}')

        dataframe = self._load_base_playback()

        dataframe = self._apply_filters(dataframe)

        self._save_parquet(dataframe,
                           os.path.join(self.prepro_derived_folder, f'{self.hash_filter_parameters}.parquet'))

        print(f'Preprocessed derived data finished at {datetime.now()} in '
              f'in {timedelta(seconds=(perf_counter() - start_time))}')

        return dataframe

    def _load_base_playback(self) -> pd.DataFrame:
        """Load the base preprocessed data from the preprocessed data folder."""
        print(f'Loading preprocessed base data at {datetime.now()}')

        if self.player == 'extended':
            raise NotImplementedError('Extended player not implemented yet.')

        base_playback_file = os.path.join(self.prepro_base_folder, 'base.parquet')

        dataframe = pd.read_parquet(base_playback_file,
                                    columns=self._get_columns(),
                                    )
        # Changes the order of the columns for consistency.
        dataframe = dataframe[self._get_columns()]

        print('Loading complete')

        return dataframe

    def _apply_filters(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Apply filters to the given dataframe and return the filtered dataframe.

        Args:
            dataframe: The dataframe to apply the filters to.
        """
        dataframe = self._prune_to_time_interval(dataframe)

        return dataframe

    def _prune_to_time_interval(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Prune the given dataframe to the given time interval and return the pruned dataframe.

        Args:
            dataframe: The dataframe to prune.
        """
        dataframe = dataframe.set_index('TIMESTAMP')
        dataframe = dataframe.between_time(self.start_time, self.stop_time)
        dataframe = dataframe.reset_index()

        return dataframe

    @staticmethod
    def _save_parquet(dataframe: pd.DataFrame, path: str) -> None:
        """Save the given dataframe as a parquet file in the preprocessed data folder.

        Args:
            dataframe: The dataframe to save.
            path: The path to save the dataframe to.
        """
        dataframe.to_parquet(path)

    def _load_source(self) -> pd.DataFrame:
        """Load the raw source data from the given files and return a concatenated dataframe."""
        source_files = collect_files(self.source_path, 'csv')
        number_of_files = len(source_files)
        dataframe_list = []
        start_time = perf_counter()

        print(f'Loading source data at {datetime.now()}')

        for file in source_files:
            if source_files.index(file) % 100 == 0:
                percentage_done = round(source_files.index(file) / number_of_files * 100, 2)
                print(f'\rLoading file {source_files.index(file)} of {number_of_files} ({percentage_done}%)', end='')
            dataframe_list.append(pd.read_csv(file, encoding='utf-8', sep='|',
                                              dtype={
                                                  'CALLSIGN': 'string',
                                              }))

        print(f'\nLoaded source data at {datetime.now()} in {timedelta(seconds=(perf_counter() - start_time))}')

        dataframe = pd.concat(dataframe_list, ignore_index=True)

        return dataframe

"""Module for splitting AIS data into files by vessel by day."""
import pandas as pd
import os
from splitter.read import read_csv, read_config
from helper_functions import collect_files
from splitter.readers.source_reader import SourceReader
import configparser

from datetime import datetime, timedelta
from time import perf_counter


class Splitter:

    def __init__(self,
                 *,
                 target_path: str,
                 reader: SourceReader,
                 ) -> None:
        """Initialize the splitter."""
        self.target_path = target_path
        self.reader = reader

    def split(self,
              *,
              source_path: str,
              target_path: str = None,
              prune_to_date: datetime.date = None  # TODO: Don't forget to implement this, i'm looking at you, future me.
              ) -> None:
        """Split the AIS data.

        The AIS data will be split into files by date and by vessel.

        Args:
            source_path: The path to the source data. If a folder, all files in the folder will be split.
            target_path: The path to the target folder. Will be created if it does not exist.
                If None, the target path given in the constructor will be used. (default: None)
            prune_to_date: The date to prune the data to. If None, all data will be split. (default: None)
        """
        target_path = self.target_path if target_path is None else target_path
        start_time = perf_counter()

        print(f'Splitting AIS data from source path: {source_path} -- to -> target path: {target_path}')

        files = collect_files(source_path, '.csv')
        current_file_number = 0
        number_of_files = len(files)

        print(f'Number of files to split: {number_of_files}')

        for file in files:
            current_file_number += 1

            print(f'Attempting to split file {current_file_number} of {number_of_files}: {file} at {datetime.now()}')

            dataframe = self._read_file(file)

            size_before = dataframe.shape[0]

            dataframe.sort_values(by=['DATE', 'TIME'], inplace=True, ascending=True)

            dataframe.dropna(subset=[
                'DATE',
                'TIME',
                'MMSI',
                'LATITUDE',
                'LONGITUDE'
            ], inplace=True)

            size_after = dataframe.shape[0]

            print(f'Dropped {size_before - size_after} rows with missing values for MMSI, timestamp, lat or long')

            # Prune to date
            if prune_to_date is not None:
                dataframe = dataframe[dataframe['DATE'] == prune_to_date]

            for dataframe_day in self._split_by_day(dataframe):
                date = dataframe_day['DATE'].iloc[0]

                if not os.path.exists(os.path.join(target_path, str(date))):
                    os.makedirs(os.path.join(target_path, str(date)))

                for dataframe_vessel in self._split_by_vessel(dataframe_day):
                    mmsi = int(dataframe_vessel['MMSI'].iloc[0])

                    dataframe_vessel.to_csv(
                        os.path.join(target_path, str(date), str(mmsi) + '.csv'),
                        index=False,
                        sep='|',
                        encoding='utf-8',
                        header=True)

            print(f'File {file} split successfully at {datetime.now()} '
                  f'in {timedelta(seconds=(perf_counter() - start_time))}')

    def _read_file(self, file_name: str) -> pd.DataFrame:
        """Read a file and return a pandas dataframe.

        Args:
            file_name: The path to the file to read.
        """
        start_time = perf_counter()

        print(f'Reading file {file_name} at {datetime.now()}')

        dataframe = self.reader.read_file(file_name)

        print(f'File {file_name} read successfully at {datetime.now()} in {timedelta(seconds=(perf_counter() - start_time))}')

        return dataframe

    @staticmethod
    def _split_by_day(dataframe: pd.DataFrame) -> list[pd.DataFrame]:
        """Split a dataframe by day and return a list of dataframes.

        Each dataframe in the list will contain data for a single day.

        Args:
            dataframe: The dataframe to split."""

        dataframe_list = []

        for group in dataframe.groupby('DATE'):
            dataframe_list.append(group[1])

        return dataframe_list

    @staticmethod
    def _split_by_vessel(dataframe: pd.DataFrame) -> list[pd.DataFrame]:
        """Split a dataframe by vessel and return a list of dataframes.

        Each dataframe in the list will contain data for a single vessel (MMSI).

        Args:
            dataframe: The dataframe to split.
        """

        dataframe_list = []

        for group in dataframe.groupby('MMSI'):
            dataframe_list.append(group[1])

        return dataframe_list

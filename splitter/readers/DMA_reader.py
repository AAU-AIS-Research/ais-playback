"""Reader for Danish  files."""
from splitter.readers.source_reader import SourceReader
import pandas as pd


class DMAReader(SourceReader):

    def read_file(self, file_path) -> pd.DataFrame:
        """Read a DMA file and return a pandas dataframe.

        Args:
            file_path: The path to the file to read.
        """
        dataframe = pd.read_csv(file_path, sep=',', na_values=['NaN', 'Unknown', 'nan', '', ' '], keep_default_na=False,
                                parse_dates=['# Timestamp'], date_format='%d/%m/%Y %H:%M:%S',
                                dtype={
                                    'Type of mobile': 'string',
                                    'MMSI': 'Int8',
                                    'Latitude': 'float64',
                                    'Longitude': 'float64',
                                    'Navigational status': 'string',
                                    'ROT': 'float64',
                                    'SOG': 'float64',
                                    'COG': 'float64',
                                    'Heading': 'Int8',
                                    'IMO': 'Int8',
                                    'Callsign': 'string',
                                    'Name': 'string',
                                    'Ship type': 'string',
                                    'Cargo type': 'string',
                                    'Width': 'Int8',
                                    'Length': 'Int8',
                                    'Type of position fixing device': 'string',
                                    'Draught': 'float64',
                                    'Destination': 'string',
                                    'ETA': 'string',
                                    'Data source type': 'string',
                                    'A': 'Int8',
                                    'B': 'Int8',
                                    'C': 'Int8',
                                    'D': 'Int8'
                                })

        dataframe = dataframe.rename(columns={
            '# Timestamp': 'TIMESTAMP',
            'Type of mobile': 'MOBILE TYPE',
            'MMSI': 'MMSI',
            'Latitude': 'LATITUDE',
            'Longitude': 'LONGITUDE',
            'Navigational status': 'NAV STATUS',
            'ROT': 'ROT',
            'SOG': 'SOG',
            'COG': 'COG',
            'Heading': 'HEADING',
            'IMO': 'IMO',
            'Callsign': 'CALLSIGN',
            'Name': 'SHIP NAME',
            'Ship type': 'SHIP TYPE',
            'Cargo type': 'CARGO TYPE',
            'Width': 'WIDTH',
            'Length': 'LENGTH',
            'Type of position fixing device': 'TRANSPONDER TYPE',
            'Draught': 'DRAUGHT',
            'Destination': 'DESTINATION',
            'ETA': 'ETA',
            'Data source type': 'DATA SOURCE TYPE',
            'A': 'A',
            'B': 'B',
            'C': 'C',
            'D': 'D'
        })

        dataframe = self._split_timestamp(dataframe)

        return dataframe

    @staticmethod
    def _split_timestamp(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Split the timestamp column into two columns, date and time.

        Args:
            dataframe: The dataframe to split the timestamp column in.
        """
        # pandas.to_datetime is used to convert the timestamp column to a datetime object, where the accessor functions
        # .dt.date and .dt.time are used to extract the date and time respectively.
        dataframe['DATE'] = pd.to_datetime(dataframe['TIMESTAMP'], format='%d/%m/%Y %H:%M:%S').dt.date
        dataframe['TIME'] = pd.to_datetime(dataframe['TIMESTAMP'], format='%d/%m/%Y %H:%M:%S').dt.time

        # Drop the original timestamp column
        dataframe.drop(columns=['TIMESTAMP'], inplace=True)

        return dataframe

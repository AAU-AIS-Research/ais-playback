"""Abstract superclass for all source readers."""
from abc import ABC, abstractmethod
import pandas as pd


class SourceReader(ABC):
    """Abstract superclass for source readers.

    Used to read AIS files from a particular source of files, ensuring that the type of file, null values, pre/suffixes,
        renaming columns and more are handles before being manipulated by the splitter module.
    """

    @abstractmethod
    def read_file(self, file_path: str) -> pd.DataFrame:
        """Read a file and return a pandas dataframe.

        The dataframe should be in the format:
            - DAY with format YYYY-MM-DD
            - TIME with format HH:MM:SS
            - MMSI as an integer
            - IMO as an integer
            - LATITUDE as a float
            - LONGITUDE as a float
            - SOG as a float
            - COG as a float
            - ROT as a float
            - HEADING as an integer
            - NAV_STATUS as an integer
            - TYPE as an integer
            - DRAUGHT as a float
            - A integer
            - B integer
            - C integer
            - D integer
            - CALLSIGN as a string
            - DESTINATION as a string
            - ETA as a string
            - NAME as a string

        Additional columns should be included with proper types and upper case names.
        Please take care of removing all null values from the dataframe before returning it.

        Args:
            file_path: The path to the file to read.
        """

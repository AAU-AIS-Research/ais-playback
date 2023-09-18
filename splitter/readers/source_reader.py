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

        If you are going to implement a new reader, please ensure that the dataframe returned by this method follows
            the documentation for the splitter module. TODO: Create documentation and then add link.
        See DMAReader for an example of how to implement this method.

        Args:
            file_path: The path to the file to read.
        """

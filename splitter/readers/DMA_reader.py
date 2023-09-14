"""Reader for Danish  files."""
from splitter.readers.source_reader import SourceReader
import pandas as pd


class DMAReader(SourceReader):

    def read_file(self, file_path) -> pd.DataFrame:
        """Read a DMA file and return a pandas dataframe.

        Args:
            file_path: The path to the file to read.
        """
        dataframe = pd.read_csv(file_path, sep=';', encoding='', na_values=['NaN', 'Unknown', 'nan'])

        return dataframe

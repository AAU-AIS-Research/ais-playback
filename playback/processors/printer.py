"""A  """
from playback.processors.parent import AbstractPlaybackProcessor
import pandas as pd


class Printer(AbstractPlaybackProcessor):
    """Processor responsible for printing each dataframe as they are processed."""

    def process_playback(self, dataframe: pd.DataFrame) -> None:
        """Prints the dataframe"""
        print(dataframe.to_string())

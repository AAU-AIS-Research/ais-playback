"""Module responsible for printing each dataframe as they are processed during playback."""
from playback.processors.parent import AbstractPlaybackProcessor
import pandas as pd


class Printer(AbstractPlaybackProcessor):
    """Processor responsible for printing each dataframe as they are processed during playback."""

    def process_playback(self, dataframe: pd.DataFrame) -> None:
        """Print the dataframe."""
        print(dataframe.to_string())

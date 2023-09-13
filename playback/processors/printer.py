"""Module responsible for printing each dataframe as they are processed during playback."""
from playback.processors.playback_processor import PlaybackProcessor
import pandas as pd


class Printer(PlaybackProcessor):
    """Processor responsible for printing each dataframe as they are processed during playback."""

    def begun(self) -> None:
        """Print a message to indicate that the playback has begun."""
        print('Playback begun.')

    def process(self, dataframe: pd.DataFrame) -> None:
        """Print contents of the dataframe."""
        print(dataframe.to_string())

    def end(self) -> None:
        """Print a message to indicate that the playback has ended."""
        print('Playback ended.')

"""Abstract superclass for all playback processors."""""
import pandas as pd
from abc import ABC, abstractmethod


class PlaybackProcessor(ABC):
    """Abstract superclass for all playback processors.

    Used to process data as it is played back in real time for the playback module.
    """

    @abstractmethod
    def begun(self) -> None:
        """Execute once when playback begins."""

    @abstractmethod
    def process(self, data: pd.DataFrame) -> None:
        """Execute each time a new dataframe is emitted during playback."""

    @abstractmethod
    def end(self) -> None:
        """Execute once when playback ends."""

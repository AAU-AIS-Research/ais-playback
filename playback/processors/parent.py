"""Base class for all processors. Used to process data as it is played back in real time for the playback module."""
import pandas as pd
from abc import ABC, abstractmethod


class AbstractPlaybackProcessor(ABC):
    """"""

    def __init__(self):
        """Initialise the processor."""

    def process_begun(self) -> None:
        """Run when the processing begins.
        For example, this could be used to initialise a plot.
        """
        pass

    @abstractmethod
    def process_playback(self, data: pd.DataFrame) -> None:
        """Run each time a new dataframe is processed during playback.
        For example, this could be used to update a plot.
        """
        raise NotImplementedError('process_data not implemented.')

    def process_ended(self) -> None:
        """Run when the processing ends.
        For example, this could be used to save a plot.
        """
        pass
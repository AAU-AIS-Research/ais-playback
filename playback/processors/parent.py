"""Base class for all processors. Used to process data as it is played back in real time for the playback module."""
import pandas as pd
from abc import ABC, abstractmethod


class AbstractPlaybackProcessor(ABC):
    """Abstract superclass for all playback processors."""

    def __init__(self) -> None:
        """Initialise the processor."""

    def begun(self) -> None:
        """Run when the playback begins.

        For example, this could be used to record the time the playback began.
        """
        pass

    @abstractmethod
    def process(self, data: pd.DataFrame) -> None:
        """Run each time a new dataframe is processed during playback.

        For example, this could be used to update a plot.
        """
        raise NotImplementedError('playback_process_dataframe not implemented.')

    def end(self) -> None:
        """Run when the playback ends.

        For example, this could be used to save a plot.
        """
        pass

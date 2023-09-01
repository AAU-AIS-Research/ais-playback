"""Base class for all processors. Used to process data as it is played back in real time for the playback module."""
import pandas as pd
from abc import ABC, abstractmethod


class AbstractPlaybackProcessor(ABC):
    """Abstract parent class for all playback processors."""

    def __init__(self) -> None:
        """Initialise the processor."""

    def playback_begun(self) -> None:
        """Run when the playback begins.

        For example, this could be used to initialise a plot.
        """
        pass

    @abstractmethod
    def playback_process_dataframe(self, data: pd.DataFrame) -> None:
        """Run each time a new dataframe is processed during playback.

        For example, this could be used to update a plot.
        """
        raise NotImplementedError('process_data not implemented.')

    def playback_ended(self) -> None:
        """Run when the playback ends.

        For example, this could be used to save a plot.
        """
        pass

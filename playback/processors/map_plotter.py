from playback.processors.parent import AbstractPlaybackProcessor
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from typing import Any

class MapPlotter(AbstractPlaybackProcessor):
    """Processor responsible for printing each dataframe as they are processed during playback."""

    def __init__(self, *, base_map: Any, target_path: str) -> None:
        """Initialise the processor."""
        super().__init__()
        self.base_map = base_map
        self.save_path = target_path

    def playback_begun(self) -> None:
        """Initialise the plot."""
        pass

    def playback_process_dataframe(self, data: pd.DataFrame) -> None:
        """Update the plot with the new data, and save the plot."""

        pass

    def playback_ended(self) -> None:
        """Collect all the plots and save them as a gif."""
        plt.savefig(self.save_path + '/map.png')
        pass


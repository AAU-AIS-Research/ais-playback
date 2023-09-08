"""Playback processor that creates a map of the vessel's movements, then combines the images into a mp4 video."""
from playback.processors.parent import AbstractPlaybackProcessor
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import os
from moviepy.editor import ImageSequenceClip


class MapPlotter(AbstractPlaybackProcessor):
    """Processor responsible for printing each dataframe as they are processed during playback."""

    def __init__(self,
                 *,
                 extent: tuple[int] = (5, 16, 52.8, 60),  # Default extent is Danish waters
                 target_folder: str) -> None:

        if os.path.isfile(target_folder):
            raise ValueError('target_folder must be a folder, not a file.')

        super().__init__()
        self.save_path = target_folder
        self.loop_count = 0

        # Initialise the plot
        self.projection = ccrs.PlateCarree()
        self.map = plt.axes(projection=self.projection)
        self.map.set_extent(extent, crs=self.projection)
        self.map.add_image(cimgt.GoogleTiles(), 7)

    def begun(self) -> None:
        """Reset the plot, so that it can be reused for the next playback.

        Also creates the save folder if it doesn't exist.
        """
        self.__init__(target_folder=self.save_path)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def process(self, dataframe: pd.DataFrame) -> None:
        """Update the plot with the new data, and save the plot."""
        self.loop_count += 1

        self.scatter = plt.scatter(dataframe.LON, dataframe.LAT, transform=self.projection, s=1, c='red')
        plt.savefig(f'{self.save_path}/frame_{self.loop_count}.png', dpi=300)
        self.scatter.remove()

    def end(self) -> None:
        """Collect all the plots and save them as a mp4."""
        print('Creating video...')
        image_folder = self.save_path
        video_name = f'{self.save_path}/video.mp4'
        png_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]
        png_files.sort(key=os.path.getmtime)
        video = ImageSequenceClip(png_files, fps=5)
        video.write_videofile(video_name, codec='mpeg4', verbose=False, logger=None)
        print('Video created.')

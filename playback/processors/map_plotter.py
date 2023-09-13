"""Playback processors that creates a map of the vessel's movements, then combines the images into a mp4 video."""
from playback.processors.playback_processor import PlaybackProcessor
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import os
from moviepy.editor import ImageSequenceClip


class MapPlotter(PlaybackProcessor):
    """Processor capable of creating maps of the vessel's movements then combining the images into a video.

    The map is created using Cartopy saved as a png, then the pngs are combined into a mp4 using MoviePy.
    """

    def __init__(self,
                 *,
                 extent: tuple[int] = (5, 16, 52.8, 60),  # Default extent is Danish waters
                 target_folder: str) -> None:
        """Initialise the processor.

        Args:
            extent: The extent of the map to plot. (default: (5, 16, 52.8, 60))
            target_folder: The folder to save the map and video in.
        """
        if os.path.isfile(target_folder):
            raise ValueError('target_folder must be a folder, not a file.')

        self.save_path = target_folder
        self.loop_count = 0

        # Initialise the plot
        self.projection = ccrs.PlateCarree()
        self.scatter = None
        self.map = plt.axes(projection=self.projection)
        self.map.set_extent(extent, crs=self.projection)
        self.map.add_image(cimgt.GoogleTiles(), 7)

    def begun(self) -> None:
        """Reinitialise the processor so that the plot is empty and the loop count is 0.

        Also creates the save folder if it doesn't exist.
        """
        self.__init__(target_folder=self.save_path)  # FIXME: This is a hacky way to reinitialise the processor

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

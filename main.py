"""Main file for the AIS playback project."""
import datetime
from playback import playback
from splitter import split
from playback.processors import MapPlotter
from mpl_toolkits.basemap import Basemap

def split_dma_folder() -> None:
    """Split the AIS data from the Danish Maritime Authority."""
    split(
        config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
        source_path='C:/Project Data/AIS/DMA 2023-08-01 to 2023-08-07',
        target_path='C:/Project Data/AIS/Split/DMA 1 Week (New Header)'
    )


def split_ma_folder() -> None:
    """Split the AIS data from the Marine Cadastre."""
    split(
        config_path='C:/Projects/ais-playback/config_examples/marine_cadastre.ini',
        source_path='C:/Project Data/AIS/MA/AIS_2023_01_01.csv',
        target_path='C:/Project Data/AIS/Split/MA'
    )


playback_folder = 'C:/Project Data/AIS/Preprocessed Playback Data'


def playback_single_file() -> None:
    """Playback of a single file."""
    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02/219004616.csv',
        speed=600,  # 10 minutes per second
        start_time=datetime.time(hour=11, minute=40, second=0),
        stop_time=datetime.time(hour=12, minute=0, second=0),
        prepro_path=playback_folder
    )


def playback_multiple_files() -> None:
    """Playback of multiple files."""
    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02',
        speed=1,  # 1 second per second
        start_time=datetime.time(hour=11, minute=59, second=56),
        stop_time=datetime.time(hour=12, minute=0, second=0),
        prepro_path=playback_folder
    )


def playback_with_map_plotter() -> None:
    """Playback of multiple files with a map plotter."""
    map_of_denmark = Basemap(projection='merc',  # Mercator's projection.
                             urcrnrlat=60,  # Upper border.
                             llcrnrlat=52.8,  # Lower border.
                             llcrnrlon=5.8,  # Left  border.
                             urcrnrlon=16,  # Right border.
                             resolution='h'
                             )
    map_of_denmark.drawmapboundary(fill_color='aqua')
    map_of_denmark.fillcontinents(color='coral', lake_color='aqua')
    map_of_denmark.drawcoastlines()
    map_target = 'C:/Project Data/AIS/Maps'

    MP = MapPlotter(
        base_map=map_of_denmark,
        target_path=map_target)

    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02',
        speed=1,  # 1 second per second
        start_time=datetime.time(hour=11, minute=59, second=56),
        stop_time=datetime.time(hour=12, minute=0, second=0),
        prepro_path=playback_folder,
        processor=MP
    )


if __name__ == '__main__':

    map_of_denmark = Basemap(projection='merc',  # Mercator's projection.
                             urcrnrlat=60,  # Upper border.
                             llcrnrlat=52.8,  # Lower border.
                             llcrnrlon=5.8,  # Left  border.
                             urcrnrlon=16,  # Right border.
                             resolution='i'
                             )
    map_of_denmark.drawmapboundary(fill_color='aqua')
    map_of_denmark.fillcontinents(color='coral', lake_color='aqua')
    map_of_denmark.drawcoastlines()
    map_target = 'C:/Project Data/AIS/Maps'

    MP = MapPlotter(
        base_map=map_of_denmark,
        target_path=map_target)

    MP.playback_begun()
    MP.playback_ended()

    #split_dma_folder()
    #split_ma_folder()

    #playback_single_file()
    #playback_multiple_files()
    #playback_with_map_plotter()

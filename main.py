"""Main file for the AIS playback project."""
import datetime
from playback import playback
from splitter import split
from playback.processors import MapPlotter


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
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02/219023785.csv',
        speed=60,  # 1 minutes per second
        start_time=datetime.time(hour=11, minute=50, second=0),
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


def playback_with_map_plotter_single() -> None:
    """Playback of multiple files with a map plotter."""
    map_target = "C:/Project Data/AIS/Maps/Vessel 219023785 - 2023-08-02"

    MP = MapPlotter(
        target_path=map_target)

    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02/219023785.csv',
        speed=900,
        processor=MP,
        no_sleep=True
    )


def playback_with_map_plotter_multiple() -> None:
    """Playback of multiple files with a map plotter."""
    map_target = "C:/Project Data/AIS/Maps/Day 2023-08-02"

    MP = MapPlotter(
        target_path=map_target)

    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02',
        speed=900,
        processor=MP,
        no_sleep=True,
        prepro_path="C:/Project Data/AIS/Preprocessed Playback Data"
    )


if __name__ == '__main__':

    split_dma_folder()
    split_ma_folder()

    playback_single_file()
    playback_multiple_files()

    playback_with_map_plotter_single()
    playback_with_map_plotter_multiple()

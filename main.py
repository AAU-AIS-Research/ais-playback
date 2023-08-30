"""Main file for the AIS playback project."""
import datetime
from playback import playback
from splitter import split


def split_dma_folder() -> None:
    """Split the AIS data from the Danish Maritime Authority."""
    split(
        config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
        source_path='C:/Project Data/AIS/DMA 2023-08-01 to 2023-08-07',
        target_path='C:/Project Data/AIS/Split/DMA 1 Week (New Header)')


def split_ma_folder() -> None:
    """Split the AIS data from the Marine Cadastre."""
    split(
        config_path='C:/Projects/ais-playback/config_examples/marine_cadastre.ini',
        source_path='C:/Project Data/AIS/MA/AIS_2023_01_01.csv',
        target_path='C:/Project Data/AIS/Split/MA')


def playback_single_file() -> None:
    """Playback of a single file."""
    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02/219004616.csv',
        speed=600,  # 10 minutes per second
        start_time=datetime.time(hour=11, minute=0, second=0),
        stop_time=datetime.time(hour=12, minute=0, second=0)
        )


def playback_multiple_files() -> None:
    """Playback of multiple files."""
    playback(
        source_path='C:/Project Data/AIS/Split/DMA 1 Week/2023-08-02',
        speed=1,  # 1 second per second
        start_time=datetime.time(hour=11, minute=59, second=50),
        stop_time=datetime.time(hour=12, minute=0, second=0)
        )


if __name__ == '__main__':

    split_dma_folder()
    #split_ma_folder()

    playback_single_file()
    playback_multiple_files()

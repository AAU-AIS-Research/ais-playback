"""Main file for the AIS playback project."""
import datetime

from splitter.module import split
from playback.module import playback


def split_dma_folder():
    """Split the AIS data from the Danish Maritime Authority"""
    split(
        config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
        source_path='C:/Project Data/AIS/DMA 2023-08-12 to 2023-08-14',
        target_path='C:/Project Data/AIS/Split/DMA')


def split_ma_folder():
    """Split the AIS data from the Marine Cadastre."""
    split(
        config_path='C:/Projects/ais-playback/config_examples/marine_cadastre.ini',
        source_path='C:/Project Data/AIS/MA/AIS_2023_01_01.csv',
        target_path='C:/Project Data/AIS/Split/MA')


def playback_single_file():
    """Playback of a single file"""
    playback(
        source_path='C:/Project Data/AIS/Split/MA/2023-01-01/368396216.csv',
        speed=600, # 10 minutes per second
        start_time=datetime.time(hour=0, minute=0, second=0),
        stop_time=datetime.time(hour=12, minute=0, second=0)
        )


if __name__ == '__main__':

    #split_dma_folder()
    split_ma_folder()

    playback_single_file()
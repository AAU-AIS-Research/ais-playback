"""Main file for the AIS playback project."""
from splitter.module import split
from playback.module import playback


def split_dma():
    # Split the AIS data from the Danish Maritime Authority
    split(
        config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
        source_path='C:/Project Data/AIS/DMA 2023-08-12 to 2023-08-14',
        target_path='C:/Project Data/AIS/Split/DMA')


def split_ma():
    # Split the AIS data from the Marine Cadastre.
    split(
        config_path='C:/Projects/ais-playback/config_examples/marine_cadastre.ini',
        source_path='C:/Project Data/AIS/MA/AIS_2023_01_01.csv',
        target_path='C:/Project Data/AIS/Split/MA')


def playback_single_file():
    # Playback a single file
    playback(
        source_path='C:/Project Data/AIS/Split/DMA/2023-08-13/311001262.csv',
        target_path='C:/Project Data/AIS/Playback',
        speed=4)


if __name__ == '__main__':

    split_dma()
    split_ma()

    #playback_single_file()
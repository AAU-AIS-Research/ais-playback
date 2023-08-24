"""Main file for the AIS playback project."""
from splitter.module import split

if __name__ == '__main__':

    # Split the AIS data from the Danish Maritime Authority
    split(
        config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
        source_path='C:/Project Data/AIS/DMA 2023-08-12 to 2023-08-14',
        target_path='C:/Project Data/AIS/Split/DMA')

    # Split the AIS data from the Marine Cadastre.
    split(
        config_path='C:/Projects/ais-playback/config_examples/marine_cadastre.ini',
        source_path='C:/Project Data/AIS/MA/AIS_2023_01_01.csv',
        target_path='C:/Project Data/AIS/Split/MA')

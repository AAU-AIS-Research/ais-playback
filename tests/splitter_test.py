from splitter.helper_functions import read_csv, read_config
from splitter.module import split
import pandas as pd
import configparser
import os

test_folder_path = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(test_folder_path, 'data')
test_config_path = os.path.join(test_folder_path, 'data/split_config.ini')


def get_file_names(path: str) -> list[str]:
    """Return a list of file names in a given path."""
    return [file for file in os.listdir(path)]


def test_read_config():
    """Test the read_config function."""
    config = read_config(test_config_path)
    assert type(config) is configparser.ConfigParser


def test_read_csv():
    """Test the read_csv function."""
    df = read_csv(os.path.join(test_data_path, 'ferry.csv'), read_config(test_config_path))
    assert type(df) is pd.DataFrame



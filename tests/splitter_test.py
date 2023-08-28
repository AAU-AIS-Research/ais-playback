from splitter.helper_functions import read_csv, read_config
from splitter.module import split
import datetime
import pandas as pd
import configparser
import os

test_folder = os.path.dirname(os.path.abspath(__file__))
test_data = os.path.join(test_folder, 'data')
test_temp = os.path.join(test_folder, 'data/temp')
test_config = os.path.join(test_folder, 'data/split_config.ini')


def clear_temp_folder():
    """Clear the temp folder."""
    if os.path.basename(test_temp) == 'temp':
        for dir in os.listdir(test_temp):
            dir_path = os.path.join(test_temp, dir)
            if os.path.isdir(dir_path):
                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    os.remove(file_path)
                os.rmdir(dir_path)
            else:
                os.remove(dir_path)


def number_of_files_in_folder(folder_path: str) -> int:
    """Return the number of files in a folder."""
    return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])


def number_of_folders_in_folder(folder_path: str) -> int:
    """Return the number of folders in a folder."""
    return len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])


def file_exists(file_path: str) -> bool:
    """Return True if the file exists."""
    return os.path.isfile(file_path)


def test_read_config():
    """Test the read_config function."""
    config = read_config(test_config)
    assert type(config) is configparser.ConfigParser


def test_read_csv():
    """Test the read_csv function."""
    df = read_csv(os.path.join(test_data, 'ferry.csv'), read_config(test_config))
    assert type(df) is pd.DataFrame


def test_split():
    """Test the split function."""
    clear_temp_folder()
    split(
        config_path=test_config,
        source_path=os.path.join(test_data, 'ferry_2day_2vessel.csv'),
        target_path=test_temp
    )
    assert number_of_folders_in_folder(test_temp) == 2
    assert number_of_files_in_folder(os.path.join(test_temp, '2022-10-15')) == 1
    assert number_of_files_in_folder(os.path.join(test_temp, '2022-10-16')) == 2
    assert file_exists(os.path.join(test_temp, '2022-10-15', '219000734.csv')) is True
    assert file_exists(os.path.join(test_temp, '2022-10-16', '219000734.csv')) is True
    assert file_exists(os.path.join(test_temp, '2022-10-16', '219000743.csv')) is True


def test_split_with_pruning():
    """Test the split function with pruning."""
    clear_temp_folder()
    split(
        config_path=test_config,
        source_path=os.path.join(test_data, 'ferry_2day_2vessel.csv'),
        target_path=test_temp,
        prune_to_date=datetime.date(2022, 10, 16)
    )
    assert number_of_folders_in_folder(test_temp) == 1
    assert number_of_files_in_folder(os.path.join(test_temp, '2022-10-16')) == 2
    assert file_exists(os.path.join(test_temp, '2022-10-16', '219000734.csv')) is True
    assert file_exists(os.path.join(test_temp, '2022-10-16', '219000743.csv')) is True

    clear_temp_folder()
    split(
        config_path=test_config,
        source_path=os.path.join(test_data, 'ferry_2day_2vessel.csv'),
        target_path=test_temp,
        prune_to_date=datetime.date(2022, 10, 15)
    )
    assert number_of_folders_in_folder(test_temp) == 1
    assert number_of_files_in_folder(os.path.join(test_temp, '2022-10-15')) == 1
    assert file_exists(os.path.join(test_temp, '2022-10-15', '219000734.csv')) is True

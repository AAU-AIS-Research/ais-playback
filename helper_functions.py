"""Helper functions for the project as a whole."""
import configparser


def read_csv_header(file_name):
    """Read the header of a csv file and return a list of column names in order of appearance."""
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        with open(file_name, 'r') as f:
            header = f.readline().strip().split(',')
        return header


def read_config(file_name):
    """Read a config file and return a configparser object."""
    config = configparser.ConfigParser()
    config.read(file_name)
    return config

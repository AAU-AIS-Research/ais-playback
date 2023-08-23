"""Helper functions for the project as a whole."""
from datetime import datetime, timedelta
from time import perf_counter
import os


def timeit(func, name: str = None):
    """Execute a given function and prints the time it took the function to execute.

    Args:
        func: The function to execute and time.
        name: Identifier for the function execution, if None, the function name will be used. (default: None)
    """
    if name is None:
        name = func.__name__

    def wrap(*args, **kwargs):
        print(f"{name} started at {datetime.now()}")
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{name} finished at {datetime.now()}")
        print(f"{name} took {timedelta(seconds=(end - start))}")
        return result

    return wrap


def read_csv_header(file_name):
    """Read the header of a csv file and return a list of column names in order of appearance."""
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        with open(file_name, 'r') as f:
            header = f.readline().strip().split(',')
        return header


def collect_files(config):
    """Collect all files in a given path and return a list of file paths.

    Args:
        path: The path to collect files from.
        config: A configparser object containing the configuration.
    """
    path = config['DataSource']['path']
    filetype = config['DataSource']['filetype']

    if os.path.isdir(path):
        return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(filetype)]
    elif os.path.isfile(path):
        return [path if path.endswith(filetype) else None]
    else:
        return []

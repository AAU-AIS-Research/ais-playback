"""Helper functions for the project as a whole."""
from datetime import datetime, timedelta
from time import perf_counter
import os
import warnings


# FIXME (Low Priority, Large):
#  Annotate this function with proper type hints.
def timeit(func, name: str = None):  # noqa: ANN001,ANN201
    """Execute a given function and prints the time it took the function to execute.

    Args:
        func: The function to execute and time.
        name: Identifier for the function execution, if None, the function name will be used. (default: None)
    """
    if name is None:
        name = func.__name__

    def wrap(*args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        print(f"{name} started at {datetime.now()}")
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{name} finished at {datetime.now()}")
        print(f"{name} took {timedelta(seconds=(end - start))}")
        return result

    return wrap


def read_csv_header(file_name: str) -> list[str]:
    """Read the header of a csv file and return a list of column names in order of appearance."""
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        with open(file_name, 'r') as f:
            header = f.readline().strip().split(',')
        return header


def collect_files(path: str, filetype: str) -> list[str]:
    """Collect all files in a given path and return a list of file paths.

    Args:
        path: The path to collect files from.
        filetype: The filetype to collect. Must be a string, e.g. 'csv' or 'txt'.
    """
    if os.path.isdir(path):
        return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(filetype)]
    elif os.path.isfile(path):
        return [path if path.endswith(filetype) else None]
    else:
        # TODO (Low priority, Medium):
        #  Reevaluate. Raise exception instead of warning?
        warnings.warn(f'Path {path} is not a file or a directory', UserWarning, stacklevel=2)
        return []


def print_lines(file_name: str, number_of_lines: int = 5) -> None:
    """Print the first n lines of a file.

    Args:
        file_name: The name of the file to print.
        number_of_lines: The number of lines to print. (default: 5)
    """
    with open(file_name, 'r') as f:
        for i in range(number_of_lines):
            print(f.readline().strip())

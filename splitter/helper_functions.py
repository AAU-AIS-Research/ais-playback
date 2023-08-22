import pandas as pd


def read_csv(file_name):
    """ Read a csv file and return a pandas dataframe
    file_name: str
        The name of the file to read
    """

    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        df = pd.read_csv(file_name)
    return df


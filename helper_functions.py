import configparser

def read_csv_header(file_name):
    if not file_name.endswith('.csv'):
        raise ValueError("File must be a csv file")
    else:
        with open(file_name, 'r') as f:
            header = f.readline().strip().split(',')
        return header

def read_config(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    return config
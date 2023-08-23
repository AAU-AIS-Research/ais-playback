from splitter.helper_functions import read_csv

def test_read_csv():
    """Test the read_csv function."""
    df = read_csv("C:/Project Data/AIS/aisdk-2023-08-12.csv")
    assert df is not None
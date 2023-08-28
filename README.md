# Setup
* Install requirements with `pip install -r requirements.txt`
* Setup the config file (see below)
* Import the modules (see below)
* Run the modules (see below)

## Setting up a config file
The config file is used to provides information about the source of the AIS data and the columns names of the data. 
The columns names are split into 2 sections, `SimpleColumns` and `ExtendedColumns`.

The config file is a `.ini` file that should be created from a copy of the `template.ini` file found in the `config_examples` folder. 
The config file contains the following sections:

### DataSource: 
This section must contains the information about the source of the AIS data
* `filetype`: The type of the source, currently only `csv` is supported
* `seperator`: The delimiter used in the file, such as `,` or `|`
* `timestamp-format`: The format of the timestamp in the file, such as `%d/%m/%Y %H:%M:%S`
* `encoding`: The encoding of the file, such as `utf-8`
* `nullvalue`: The value used to indicate a null value in the file, such as `` or `NULL`
### SimpleColumns: 
This section must contain the information about the columns in the AIS data file that are used during simple playback. 
The fields are mandatory and must be filled in.

* `mmsi`: The column name of the MMSI
* `imo`: The column name of the IMO number
* `status`: The column name of the navigational status
* `sog`: The column name of the speed over ground
* `lat`: The column name of the latitude
* `lon`: The column name of the longitude
* `cog`: The column name of the course over ground
* `heading`: The column name of the heading
* `timestamp`: The column name of the timestamp
### ExtendedColumns: 
This section must contain the information about the columns in the AIS data file that are used during extended playback. 
The fields are not mandatory and can be left empty.
  * NOT YET IMPLEMENTED, LEAVE EMPTY 

## Importing the modules
To use the modules, you need to import them into your python script. 
```python
from splitter.module import split
from playback.module import playback
from datetime import datetime # Optional, only needed for certain playback parameters 
```
The `main.py` file contains an example of how to use the modules.

## Running the modules
To run the modules, you need to call the appropriate function. 

### Splitter
The splitter module can be run by calling the `split` function.

It has 3 parameters:
* `config_path`: The path to the config file
* `source_path`: The path to the source folder or file
* `target_path`: The path to the target folder

Example:
```python
from splitter.module import split

# Split the AIS data from the Danish Maritime Authority
split(
    config_path='C:/Projects/ais-playback/config_examples/danish_marine_authority.ini',
    source_path='C:/Project Data/AIS/DMA 2023-08-12 to 2023-08-14',
    target_path='C:/Project Data/AIS/Split/DMA')
```

### Playback
The playback module can be run by calling the `playback` function.

NOTE: The playback module is still rough and does not yet conform to the MarineTime format. 

It has 4 parameters:
* `source_path`: The path to the source file to playback
* `speed`: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
* `start_time`: The time to start playback. Must be a `datetime.time` object.
* `stop_time`: The time to stop playback. Must be a `datetime.time` object.

Example:
```python
from playback.module import playback
from datetime import datetime

# Playback a split file (1 day, 1 vessel) from the Danish Maritime Authority
playback(
    source_path='C:/Project Data/AIS/Split/DMA/2023-08-13/368396216.csv',
    speed=600, # 10 minutes per second
    start_time=datetime.time(hour=0, minute=0, second=0), # Optional, defaults to 00:00:00
    stop_time=datetime.time(hour=12, minute=0, second=0)  # Optional, defaults to 23:59:59
    )
```

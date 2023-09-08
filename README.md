# Setup
* Install requirements with `pip install -r requirements.txt`
* Setup the config file (see below)
* Import the modules (see below)
* Run the modules (see below)

## Setting up a config file
The config file is used to provides information about a source of the AIS data and the columns names for that data. 
The columns names are split into 2 sections, `SimpleColumns` and `ExtendedColumns`.

The config file is a `.ini` file that should be created by copying the `template.ini` file found in the `config` folder, changing the variables in the copy to match the structure of your AIS data.

An example of a fully filled out config file can be seen in the `danish_marine_authority.ini` file in the `config` folder.
This config defines the AIS data from the [Danish Maritime Authority](https://dma.dk/safety-at-sea/navigational-information/ais-data).

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

* `mmsi`: Maritime Mobile Service Identity Number (MMSI) number
* `imo`: International Maritime Organisation (IMO) number
* `status`: Navigational status 
* `sog`: Speed over ground
* `lat`: Latitude
* `lon`: Longitude
* `cog`: Course over ground
* `heading`: Heading
* `timestamp`: Timestamp
### ExtendedColumns: 
This section must contain the information about the columns in the AIS data file that are used during extended playback. 
The fields are currently mandatory and must be filled in, but they are not yet used.

* `ship-name`: Name of the vessel
* `callsign`: Call sign
* `mobile-type`: Type of transponder (e.g. Class A, Class B, etc.) 
* `ship-type`: Type of vessel (e.g. cargo, tanker, etc.)
* `cargo-type`: Type of cargo 
* `device-type`: Type of position system (e.g. GPS, DGPS, etc.)
* `width`: Width of the vessel
* `length`: Length of the vessel
* `draught`: Draught (or draft)
* `destination`: Destination
* `data-source`: Data source type
* `eta`: Estimated time of arrival
* `a`: Dimension to bow
* `b`: Dimension to stern
* `c`: Dimension to port
* `d`: Dimension to starboard

## Importing the modules
To use the modules, you need to import them: 
```python
from splitter.module import split
from playback.module import playback
from datetime import datetime # Optional, only needed for certain playback parameters 
```

## Running the modules
To run the modules, you need to call the appropriate function. 

### Splitter
The splitter module can be run by calling the `split` function.

It has 4 parameters:
* `config_path`: The path to the config file
* `source_path`: The path to the source folder or file
* `target_path`: The path to the target folder
* `prune_to_date`: The date to prune the data to. Must be a `datetime.date` object. Optional, defaults to `None`

Example:

```python
from splitter import split

# Split the AIS data from the Danish Maritime Authority
split(
    config_path='/config/danish_marine_authority.ini',
    source_path='C:/Project Data/AIS/DMA 2023-08-12 to 2023-08-14',
    target_path='C:/Project Data/AIS/Split/DMA')
```

### Playback
The playback module can be run by calling the `playback` function.

NOTE: The playback module is still rough and does not yet conform to the MarineTime format. 

It has 6 parameters:
* `source_path`: The path to the source file to playback
* `prepro_path`: The path to store and load the preprocessed data, making future runs faster. Optional, defaults to `None` 
* `speed`: The speed to play back the data. 1 is real time, 2 is twice as fast, etc. Must be between 1 and 900.
* `start_time`: The time to start playback. Must be a `datetime.time` object. Optional, defaults to 00:00:00
* `stop_time`: The time to stop playback. Must be a `datetime.time` object. Optional, defaults to 23:59:59
* `processor`: The playback processor to use. Optional, defaults to `Printer` which prints the data emission to the console. 

Example:
```python
from playback import playback
from datetime import datetime

# Playback a split file (1 day, 1 vessel) from the Danish Maritime Authority
playback(
    source_path='C:/Project Data/AIS/Split/DMA/2023-08-13/368396216.csv',
    prepro_path='C:/Project Data/AIS/Preprocessed',
    speed=600, # 10 minutes per second
    start_time=datetime.time(hour=0, minute=0, second=0),
    stop_time=datetime.time(hour=12, minute=0, second=0) 
    )
```
## Playback Processors
The playback module supports different playback processors which are classes that process the data emission from the playback module.

It's up to the processor to decide what to do with the data emissions from the playback module.

The following processors are currently available:
* `Printer`: Prints the data emission to the console (default for the playback module).
* `MapPlotter`: Plots the data emission on a map which is stored in a folder as png files. 
When all emission are processed, a video is created from the png files and stores the video in the same folder.

Further processors can be created by inheriting from the `AbstractPlaybackProcessor` class and implementing the `process` method and optionally the `begun` and `end` method.

The `process` method is called for each data emission, where each data emission is passed as a `DataFrame` from the pandas library.

The `begun` method is called when the playback begins and the `end` method is called when the playback ends. 
This can be used for initialization, cleaning up resources or store results collected during the playback. 
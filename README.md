# Setup
* Install requirements with `pip install -r requirements.txt`
* Import and run each of the modules (see below)

## Splitter module
First the splitter class needs to be initialized with the following parameters:

* `target_path`: Path to the folder where the split files should be stored
* `reader`: Which reader object to use for reading the source files. 

Readers are classes that read the source files and return a `DataFrame` from the pandas library.

Further documentation on readers will be added later, as their requirements are still being defined.

Example:

```python
from splitter import Splitter
from splitter.readers import DMAReader # Reader for the Danish Maritime Authority

dma_splitter = Splitter(
    target_path='C:/Project Data/Split/DMA',
    reader=DMAReader())
```

To split a file, call the `split` method on the splitter object with the following parameters:
* `source_path`: Path to the source file to split, must be a csv file or folder containing csv files.
* `target_path`: Path to the folder where the split files should be stored. Optional, defaults to the target_path specified when initializing the splitter object.
* `prune_to_data`: Whether to prune the split files to a single defined date. Optional, defaults to `None`, which means no pruning. 

Example:

```python
import datetime

dma_splitter.split(
    source_path='C:/Project Data/AIS/DMA/2023-08-13.csv',
    prune_to_date=datetime.date(year=2023, month=8, day=1)) 
```

## Playback
First the playback class needs to be initialized with the following parameters:
* `source_path`: Path to a split file or folder containing the split files.
* `prepro_folder`: Path to the folder for storing preprocessed files. Optional, defaults to the `None`, which means no preprocessing.
* `subset`: Which subset of the data to playback. Not implemented yet.
* `processor`: Which processor object to use for processing the data emissions. Optional, defaults to the `Printer` processor.
* `start_time`: The start time of the playback. Optional, defaults to minimum time (00:00:00)
* `stop_time`: The stop time of the playback. Optional, defaults to maximum time (23:59:59)
* `player`: Defines which columns to use for the playback. Optional, defaults to `simple` which uses `['MMSI', 'IMO', 'NAV STATUS', 'SOG', 'LONGITUDE', 'LATITUDE', 'COG', 'HEADING', 'TIMESTAMP']` as columns. 

Preprocessing is a process where the data is read from the split files and stored in a more efficient format for faster playback on subsequent runs.

To perform the playback, call the `play` method on the playback object with the following parameters:
* `speed`: The speed of the playback, where 1 is real time and 2 is twice as fast. Optional, defaults to 1 and highest allowed value is 900 (15 min per emission).
* `no_sleep`: Whether to skip sleeping between each emission. Optional, defaults to `False`, which means sleeping between each emission.

example:

```python
from playback import Playback
from playback.processors import MapPlotter # Processor for plotting on a map
import datetime

dma_playback = Playback(
    source_path='C:/Project Data/Split/DMA',
    prepro_folder='C:/Project Data/Preprocessed/DMA',
    processor=MapPlotter(target_folder='C:/Project Data/Map/DMA'),
    start_time=datetime.time(hour=8, minute=0, second=0),
    stop_time=datetime.time(hour=16, minute=0, second=0))
    
dma_playback.play(speed=1) # Play at real time
```

## Playback Processors
The playback module supports different playback processors which are classes that process the data emission from the playback module.

It's up to the processor to decide what to do with the data emissions from the playback module.

The following processors are currently available:
* `Printer`: Prints the data emission to the console (default for the playback module).
* `MapPlotter`: Plots the data emission on a map which is stored in a folder as png files. 
When all emission are processed, a video is created from the png files and stores the video in the same folder.

Further processors can be created by inheriting from the `PlaybackProcessor` class and implementet the following methods:
* `process`: Called for each data emission, where each data emission is passed as a `DataFrame` from the pandas library.
* `begun`: Called when the playback begins. Can be used for initialization.
* `end`: Called when the playback ends. Can be used for cleaning up resources or store results collected during the playback.

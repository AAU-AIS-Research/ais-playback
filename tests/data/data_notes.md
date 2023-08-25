# CSV files
## ferry.csv
Single day of data for 1 vessel (ferry), sailing between 2 ports.
Used as a source for other data files.

## ferry_2day_2vessel.csv
Modified version of `ferry.csv`, so that it portrays 2 days of data for 2 vessels (switches from one to the other).

* Reduced to 60 entries
* First 20 entries are for vessel 1, day 1
* Next 30 entries are for vessel 1, day 2
* Next 10 entries are for vessel 2, day 2

 ### Expected outcome after split:
2 folders, 1 folder for day 1 containing 2 vessels and 1 folder for day 2 containing 1 vessel.

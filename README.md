# Summary

This repository consists of preprocessing and postprocessing scripts in both python and r for running WEPP and analysis of results.

```converttotwo....py``` files convert the WEPP input files from one OFE to two OFE

```edit_run_file_year.py``` files edit the year value in the run file. This is usefully when making changes to the run configuration for the WEPP watershed in bulk.

```water_balance_aggregate.py``` will summarize waterbalance and directly output it as a word file.

```summarize_waterbal.py``` will summarize water balance for each hillslope. 

```Report_result_final.ipynb``` file processes all the WEPP watershed runs, computes and summarize water balance and erosion... Map them to different WEPPID and TopazID using Geopandas.. And provide a clean dataframe for analysis in R and Python for producing graphs and conducting further analysis.

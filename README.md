# Summary

This repository consists of preprocessing and postprocessing scripts in both python and r for running WEPP and analysis of results.

```converttotwo....py``` files convert the WEPP input files from one OFE to two OFE

```edit_run_file_year.py``` files edit the year value in the run file. This is usefully when making changes to the run configuration for the WEPP watershed in bulk.

```water_balance_aggregate.py``` will summarize waterbalance and directly output it as a word file.

```summarize_waterbal.py``` will summarize water balance for each hillslope. 

```yearly_erosion_single_hillslope.py``` will summarize yearly erosion for each hillslope for each OFE.. This function is mainly used for post processing in large watershed with high number of hillslopes.

```final_erosion_analysis.rmd``` will conduct further data analysis to identify trends in different rotation, periods, tillage types and produce graphs using ggplot..

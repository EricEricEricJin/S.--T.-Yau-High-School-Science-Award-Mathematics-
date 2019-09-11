# Results from simulation experiments
This folder contains experiment results obtained from the experiment of the fast approach.
## CSV files
The CSV files are outputed by report.py module. They show the following: 
- data source 
- arguments(threshold, minium points number, run times) 
- time used by CSI method 
- time used by the new approach 
- mean errors 
- max errors 
- number of linear and curve parts found

## PNG files
### PNG files named by xx_0.png
These files plot the curve fiited by the new approach and scatters original data. 
The red parts are parts found linear, and green parts are parts found curve. 
The blue points show the original data.

### PNG files named by xx.png
These files scatter the time complexity against number of linear parts founded. 
Green points are from the new approach, red points are from CSI. 

CS6601 AI Fall 2013
Project 2, Shelly Bagchi & Laura Strickland
A Non-Invasive Supplement to Continuous Glucose Monitoring for Type 1 Diabetes

(1) trimCSV.py
usage:  trimCSV.py FILENAME, e.g. 'trimCSV.py MYFILE101'
This script takes an input CSV file from the folder 'diabetesFilesNoHeaders' and
trims out rows of invalid data: where sensors read 'inf' or where the CGM reading
is 0 or -1.  Additionally, the data is tagged by 30-minute intervals (60 data
points each) by if the overall CGM trend is rising, falling, or stable (change
within +/- 10).  The trimmed CSV file is saved in the folder 'trimmedDataFiles'.

(2) simplecgmstplot.py
This program uses matplotlib to plot the raw skin temperature and CGM blood glucose
reading obtained from the trimmed CSV file specified in the top of the main code.
The plot image is saved in the folder 'plotsRawData'.

(3) plotBGST.py
This program uses matplotlib to plot the raw skin temperature and CGM blood glucose
reading obtained from the trimmed CSV file specified in the top of the main code.
The CGM data is color-coded by the slope of each interval: green = stable, 
red = rising, and blue = falling.  The plot image is saved in the folder
 'plotsRawData'.
 
(4) trainTestHMM.py
This program uses scikit-learn and matplotlib to plot the results of training an
HMM on 80% of data obtained from the trimmed CSV file specified in the top of
the main code.  The HMM is tested on the remaining 20% and that data is 
color-coded by the assigned hidden state and plotted.  The plot image is saved 
in the folder 'plotshmm'.
Additionally, the CGM data, original labels, and assigned states are printed
to a CSV file in the folder 'resultsEvaluation' for analysis.
 
(5) trainTestSVM.py
This program uses scikit-learn and matplotlib to plot the results of training 
an SVM on 80% of data obtained from the trimmed CSV file specified in the top
of the main code.  The SVM is tested on the remaining 20% and that data is 
color-coded by the assigned group and plotted.  The plot image is saved in the 
folder 'plotssvm'.
Additionally, the CGM data, original labels, and assigned groups are printed
to a CSV file in the folder 'resultsEvaluation' for analysis.

(6) folder 'referenceCode'
Contains the original viztool code provided by Aditya Tirodkar and Subrai Pai.

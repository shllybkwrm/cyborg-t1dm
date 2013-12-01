#! /usr/bin/env python
# Data read-in adapted from http://software-carpentry.org/blog/2012/05/an-exercise-with-matplotlib-and-numpy.html
# GaussianHMM info from http://scikit-learn.org/stable/auto_examples/applications/plot_hmm_stock_analysis.html

from __future__ import print_function
import numpy as np
import datetime
from datetime import datetime
import pylab as pl
import os
import matplotlib.pyplot as pyplot
from sklearn.hmm import GaussianHMM
#from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
#from sklearn.hmm import GaussianHMM

def dateconv(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    #print(date)
    return date

def t1dmread(file_name):
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm', 'numlabel'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int, np.int]})
    data = np.loadtxt(file_name, delimiter=';', skiprows=1,converters = { 0 : dateconv },usecols=(0,7,10,13,17,18,19,20,21,22,23,24,25,26,27,28), dtype=dtypes)
    return data


def stuffPlot(timestamps,func,title,ylabel):
    fig = pyplot.figure()
    pyplot.title(title)
    pyplot.ylabel(ylabel)
    pyplot.xlabel('Time')
    pyplot.plot(timestamps,func,marker='o')
    pyplot.show()
    
    return fig

#--------------------------------------------------

# If no plots folder exists, make a folder to store all of the plots
if not os.path.exists('plots'):
    os.mkdir('plots')

data = t1dmread('trimmedDataFiles/MYFILE101.no_gaps_MINIMAL_labeled.csv')
timeStamps = np.array(data['timestamp'])
skinTemp = np.array(data['skin temp'])
airTemp = np.array(data['air temp'])
steps = np.array(data['steps'])
hr = np.array(data['hr'])
cgm = np.array(data['cgm'])
numlabels = np.array(data['numlabel'])
#labels = np.array(data['label'])
normskintemp = skinTemp - airTemp

training = np.column_stack([normskintemp[0:299],numlabels[0:299]])
test = np.column_stack([normskintemp[300:360],numlabels[300:360]])

#fit1 = np.column_stack([normskintemp,numlabels])

n_components = 3
model = GaussianHMM(n_components,covariance_type='diag',n_iter=1000)
model.fit([training])
hidden_states_training = model.predict(training)

print("Transition Matrix:\n")
print(model.transmat_)
for i in range(n_components):
    print("%dth hidden state:" % i)
    print("Mean = ",model.means_[i])
    print("Variance = ",np.diag(model.covars_[i]))
    print()

hidden_states_test = model.predict(test)
print("Test Set Hidden States")
print(hidden_states_test)                         # Please note that hidden state 2 may not correspond to label 2! 

#! /usr/bin/env python
# Data read-in adapted from http://software-carpentry.org/blog/2012/05/an-exercise-with-matplotlib-and-numpy.html
# GaussianHMM info from http://scikit-learn.org/stable/auto_examples/applications/plot_hmm_stock_analysis.html

import numpy as np
from datetime import datetime
import pylab as pl
import os
import matplotlib.pyplot as pyplot
from sklearn.hmm import GaussianHMM
#from sklearn.hmm import GaussianHMM

def dateconv(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    #print(date)
    return date

def t1dmread(file_name):
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int] })
    data = np.loadtxt(file_name, delimiter=',', skiprows=1,converters = { 0 : dateconv },usecols=(0,7,10,13,17,18,19,20,21,22,23,24,25,26,27), dtype=dtypes)
    return data


def basichmm(datacol1,datacol2): #This may need more arguments if we discover correlation with multiple factors.
    cols = np.column_stack([datacol1,datacol2])
    
    components = 7 # 7 components = 7 stages?
    model = GaussianHMM(components, covariance_type="diag", n_iter=1000)
    model.fit([cols])
    hidden_states = model.predict(cols)
    print("Hidden States:")
    for i in range(components):
        print("Hidden state %d" % i)
        print("mean = ", model.means_[i])
        print("variance = %d", np.diag(model.covars_[i]))
        print()
        
    return 


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
#if not os.path.exists('~/cyborg-t1dm/cyborg-t1dm/plots'):
if not os.path.exists('plots'):
    os.mkdir('plots')



data = t1dmread('trimmedDataFiles/MYFILE101.no_gaps_trimmed.csv')
timestamps101 = np.array(data['timestamp'])
skinTemp101 = np.array(data['skin temp'])
airTemp101 = np.array(data['air temp'])
steps101 = np.array(data['steps'])
hr101 = np.array(data['hr'])
cgm101 = np.array(data['cgm'])
normskintemp101 = skinTemp101 - airTemp101


pyplot.ion()

fig = stuffPlot(timestamps101,(normskintemp101),'Skin Temp - Near Temp, Subject 101','Skin Temp - Near Temp')

fig.savefig('plots/skinneartemp101')

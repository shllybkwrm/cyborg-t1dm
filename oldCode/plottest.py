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
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int] })
    data = np.loadtxt(file_name, delimiter=',', skiprows=1,converters = { 0 : dateconv },usecols=(0,7,10,13,17,18,19,20,21,22,23,24,25,26,27), dtype=dtypes)
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



data = t1dmread('trimmedDataFiles/MYFILE101.no_gaps_trimmed.csv')
timeStamps101 = np.array(data['timestamp'])
skinTemp101 = np.array(data['skin temp'])
airTemp101 = np.array(data['air temp'])
steps101 = np.array(data['steps'])
hr101 = np.array(data['hr'])
cgm101 = np.array(data['cgm'])
normskintemp101 = skinTemp101 - airTemp101

toFit = np.column_stack([cgm101,normskintemp101])
print("Fitting to HMM")
n_components = 4
model = GaussianHMM(n_components,covariance_type='diag',n_iter=1000)
model.fit([toFit])

hidden_states = model.predict(toFit)

print("done\n")

print("Transition Matrix for Normed Skin Temperature")
print(model.transmat_)
print("\nMeans and variances of each hidden state: \n")

for i in range(n_components):
    print("%dth hidden state:" % i)
    print("Mean = ",model.means_[i])
    print("Variance = ",np.diag(model.covars_[i]))
    print()

fig = pl.figure()
skinTemp = fig.add_subplot(211)
pl.ylabel('Norm of Skin Temp')
cgmFig = fig.add_subplot(212)
pl.ylabel('CGM BG Estimate')
pl.xlabel('Time')
#hrFig = fig.add_subplot(313)
#stepsFig = fig.add_subplot(414)
for i in range(n_components):
    idx = (hidden_states == i)
    skinTemp.plot_date(timeStamps101[idx],normskintemp101[idx],'o',label="Hidden State %d" % i)
    cgmFig.plot_date(timeStamps101[idx],cgm101[idx],'o',label="Hidden State %d" % i)
#    hrFig.plot_date(timeStamps101[idx],hr101[idx],'o',label="Hidden State %d" % i)
#    stepsFig.plot_date(timeStamps101[idx],steps101[idx],'o',label="Hidden State %d" % i)
cgmFig.legend()
skinTemp.legend()
#hrFig.legend()
#stepsFig.legend()

pl.show()

pyplot.ion()

#fig = stuffPlot(timestamps101,(normskintemp101),'Skin Temp - Near Temp, Subject 101','Skin Temp - Near Temp')

fig.savefig('plots/skinneartemp101')

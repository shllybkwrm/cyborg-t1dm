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

def dateconv(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    #print(date)
    return date

def t1dmread(file_name):
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm', 'numlabel'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int, np.int]})
    data = np.loadtxt(file_name, delimiter=',', skiprows=1,converters = { 0 : dateconv },usecols=(0,7,10,13,17,18,19,20,21,22,23,24,25,26,27,28), dtype=dtypes)
    return data

#--------------------------------------------------

data = t1dmread('trimmedDataFiles/MYFILE103_trimmed.csv')
figOutputFilename = 'plotshmm/hmmskincgm103'
csvOutputFilename = 'resultComparison/skincgm-hmm103.csv'

timeStamps = np.array(data['timestamp'])
skinTemp = np.array(data['skin temp'])
airTemp = np.array(data['air temp'])
steps = np.array(data['steps'])
hr = np.array(data['hr'])
cgm = np.array(data['cgm'])
numlabels = np.array(data['numlabel'])
normskintemp = skinTemp - airTemp

lenData = len(timeStamps)
lenTrain = np.ceil(0.8*lenData)

training = np.column_stack([normskintemp[0:lenTrain],numlabels[0:lenTrain]])
test = np.column_stack([normskintemp[(lenTrain+1):lenData],numlabels[(lenTrain+1):lenData]])
test_timeStamps = timeStamps[lenTrain+1:lenData]

test_st = normskintemp[int(lenTrain)+1:lenData]
test_cgm = cgm[int(lenTrain)+1:lenData]
# "Official" labels for test set data
test_labels = numlabels[int(lenTrain)+1:lenData]

n_components = 3    # Rising, falling, and stable blood sugar
model = GaussianHMM(n_components,covariance_type='diag',n_iter=1000)
model.fit([training])
hidden_states_training = model.predict(training)



print("Transition Matrix:\n")
print(model.transmat_)
for i in range(n_components):
    print("Hidden state %d:" % i)
    print("Mean = ",model.means_[i])
    print("Variance = ",np.diag(model.covars_[i]))
    print()

hidden_states_test = model.predict(test)
print("Test Set Hidden States")

test_results = np.empty_like(hidden_states_test,dtype="S10")
state_contents = np.empty_like(hidden_states_test)
for idx,item in np.ndenumerate(hidden_states_test):
    if item == 2:
        np.put(test_results,idx,'falling',mode='clip')
        np.put(state_contents,idx,item,mode='clip')
    elif item == 1:
        np.put(test_results,idx,'rising',mode='clip')
        np.put(state_contents,idx,item,mode='clip')
    else: 
        np.put(test_results,idx,'stable',mode='clip')
        np.put(state_contents,idx,item,mode='clip')

results = np.column_stack((test_timeStamps,state_contents,test_results))
print("Results:\n")
print(results)

# If no plots folder exists, make a folder to store all of the plots
if not os.path.exists('plotshmm'):
    os.mkdir('plotshmm')


'''
fig = pl.figure()
skinTemp = fig.add_subplot(211)
pl.ylabel('Skin Temp - Ambient Temp')
cgmFig = fig.add_subplot(212)
pl.ylabel('CGM BG')
pl.xlabel('Time')
fig.autofmt_xdate()
for i in range(n_components):
    idx = (hidden_states_test == i)
<<<<<<< HEAD
    skinTemp.plot_date(timeStamps[idx],normskintemp[idx],'.',label="Hidden State %d" % i)
    cgmFig.plot_date(timeStamps[idx],cgm[idx],'.',label="Hidden State %d" % i)
cgmFig.legend()

r = pl.Rectangle((0, 0), 1, 1, fc="r")
g = pl.Rectangle((0, 0), 1, 1, fc="g")
b = pl.Rectangle((0, 0), 1, 1, fc="b")
cgmFig.legend( [g,r,b], ['Stable','Rising','Falling'] )
=======
    skinTemp.plot_date(test_timeStamps[idx],test_st[idx],'.',label="Hidden State %d" % i)
    cgmFig.plot_date(test_timeStamps[idx],test_cgm[idx],'.',label="Hidden State %d" % i)
skinTemp.legend()
'''
fig = pl.figure()
skinTemp = fig.add_subplot(211)
pl.ylabel('Skin Temp - Ambient Temp')
cgmFig = fig.add_subplot(212)
pl.ylabel('CGM BG')

for i in range(0,len(state_contents)):
#    start = i*60
#    stop = (i+1)*60
    if state_contents[i]==0:
        color = 'g.'
        Label = 'Hidden State 0'
    elif state_contents[i]==1:
        color = 'r.'
        Label = 'Hidden State 1'
    elif state_contents[i]==2:
        color = 'b.'
        Label = 'Hidden State 2'
    skinTemp.plot_date(test_timeStamps[i],test_st[i],color,label=Label)
    cgmFig.plot_date(test_timeStamps[i],test_cgm[i],color,label=Label)
pl.xlabel('Time')
fig.autofmt_xdate()

#handles, labels = skinTemp.get_legend_handles_labels()
r = pl.Rectangle((0, 0), 1, 1, fc="r")
g = pl.Rectangle((0, 0), 1, 1, fc="g")
b = pl.Rectangle((0, 0), 1, 1, fc="b")
cgmFig.legend( [g,r,b], ['Hidden State 0','Hidden State 1','Hidden State 2'] )


# Prints the HMM's label result for each time segment
for index, item in enumerate(test_results):
    if np.mod(index,60) == 0:
        print(item)

pl.show()
fig.savefig(figOutputFilename)


testDataOut = np.column_stack( [ test_cgm, test_labels, state_contents ] )
np.savetxt(csvOutputFilename, testDataOut, '%d', delimiter=",")


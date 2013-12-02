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
from sklearn import svm

def dateconv(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    #print(date)
    return date

def t1dmread(file_name):
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm', 'numlabel'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int, np.int]})
    data = np.loadtxt(file_name, delimiter=',', skiprows=1,converters = { 0 : dateconv },usecols=(0,7,10,13,17,18,19,20,21,22,23,24,25,26,27,28), dtype=dtypes)
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
timeStamps = np.array(data['timestamp'])
skinTemp = np.array(data['skin temp'])
airTemp = np.array(data['air temp'])
steps = np.array(data['steps'])
hr = np.array(data['hr'])
cgm = np.array(data['cgm'])
numlabels = np.array(data['numlabel'])
#labels = np.array(data['label'])
normskintemp = skinTemp - airTemp

#lenData = len(timeStamps)/60
samples = len(timeStamps)/60
lenTrain = np.ceil(0.8*samples)
trainSamples = np.empty((samples,2))
trainLabels = np.empty((samples,1))
timeStart = np.empty((samples,1),dtype=datetime)

# for each index and element in normskintemp
# if index % 60 == 59
# put that as second feature for the current row
# if index % 60 == 0,
# put that as first feature for the current row
# 
next = 0
for index,item in np.ndenumerate(normskintemp):
#    import pdb; pdb.set_trace()
    idxmod = np.mod(index,60)
    if idxmod == 59:
        np.put(trainSamples,(next,2),item,mode='clip')
    elif idxmod == 0:
        np.put(trainSamples,(next,1),item,mode='clip')
        np.put(trainLabels,next,numlabels[index],mode='clip')
        np.put(timeStart,next,timeStamps[index],mode='clip')

training = np.column_stack([trainSamples[0:lenTrain],trainLabels[0:lenTrain]])
test = np.column_stack([trainSamples[(lenTrain+1):samples],trainLabels[(lenTrain+1):samples]])
test_timeStamps = timeStart[lenTrain+1:samples]

############ What goes into Fit:
# For fit() for an svm, you put in 3 array arguments:
# an array X of size [n_samples, n_features] holding the training samples, and an array Y of integer values, size [n_samples], holding the class labels for the training samples

# Idea: Get array that is same length of number of samples. In it, put timestamp at beginning of interval, first skintemp value in interval, last skintemp value in interval, slope calculated from those two, and HMM label (1, 0, -1). The slope becomes 

n_components = 3    # Rising, falling, and stable blood sugar
model = svm.SVC()
model.fit(trainSamples[0:lenTrain],trainLabels[0:lenTrain])
groups_training = model.predict(trainSamples[0:lenTrain])

group_test = model.predict(trainSamples[(lenTrain+1):samples])
print("Test Set Groups")

test_results = np.empty_like(group_test,dtype="S10")
state_contents = np.empty_like(group_test)
for idx,item in np.ndenumerate(group_test):
    if item == -1:
        np.put(test_results,idx,'falling',mode='clip')
        np.put(state_contents,idx,item,mode='clip')
    elif item == 1:
        np.put(test_results,idx,'rising',mode='clip')
        np.put(state_contents,idx,item,mode='clip')
    else: 
        np.put(test_results,idx,'stable',mode='clip')
        np.put(state_contents,idx,item,mode='clip')
#    print(item)
#    print(test_results[idx])
#    import pdb; pdb.set_trace()
#print(test_timeStamps)
#print(test_results)



results = np.column_stack((test_timeStamps,state_contents,test_results))
print(results)


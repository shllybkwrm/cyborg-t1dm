#! /usr/bin/env python
# Data read-in adapted from http://software-carpentry.org/blog/2012/05/an-exercise-with-matplotlib-and-numpy.html

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

data = t1dmread('trimmedDataFiles/MYFILE117_trimmed.csv')
timeStamps = np.array(data['timestamp'])
skinTemp = np.array(data['skin temp'])
airTemp = np.array(data['air temp'])
steps = np.array(data['steps'])
hr = np.array(data['hr'])
cgm = np.array(data['cgm'])
numlabels = np.array(data['numlabel'])
normskintemp = skinTemp - airTemp

samples = len(timeStamps)/60
lenTrain = np.ceil(0.8*samples)
lenTrainFull = 0.8*len(timeStamps)
trainSamplesBegin = []
trainSamplesEnd = []
trainLabels = []
trainTestLabels = []
timeStart = []
testLabels = []

for index,item in np.ndenumerate(normskintemp):
    idxmod = np.mod(index,60)
    if idxmod == 59:
        trainSamplesEnd.append(item)
    elif idxmod == 0:
        trainSamplesBegin.append(item)
        trainTestLabels.append(numlabels[index])
        timeStart.append(timeStamps[index])

# Arrays containing just the first and last readings of each time segment (and corresponding data)
training = np.column_stack([trainSamplesBegin[0:int(lenTrain)],trainSamplesEnd[0:int(lenTrain)]])
trainLabels = trainTestLabels[0:int(lenTrain)]
test = np.column_stack([trainSamplesBegin[(int(lenTrain)+1):samples],trainSamplesEnd[(int(lenTrain)+1):samples]])

# "Official" labels for test set data
testLabels = trainTestLabels[(int(lenTrain)+1):samples]
test_timeStamps = timeStart[int(lenTrain)+1:samples]

# Arrays with all data
longTestSt = normskintemp[(int(lenTrainFull) + 1):len(normskintemp)]
longTestTime = timeStamps[(int(lenTrainFull) + 1):len(timeStamps)]
longTestCGM = cgm[(int(lenTrainFull) + 1):len(cgm)]

# For training SVM: first skintemp value in interval, last skintemp value in interval, and label (1, 0, -1).

model = svm.SVC()
model.fit(training,trainLabels)
group_training = model.predict(training)

group_test = model.predict(test)
print("Test Set Groups")

test_results = np.empty_like(group_test,dtype="S10")
state_contents = np.empty_like(group_test,dtype=np.int)
for idx,item in np.ndenumerate(group_test):
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
if not os.path.exists('plotssvm'):
    os.mkdir('plotssvm')

fig = pl.figure()
skinTemp = fig.add_subplot(211)
pl.ylabel('Skin Temp - Ambient Temp')
cgmFig = fig.add_subplot(212)
pl.ylabel('CGM BG')
'''
for i in range(3):
    idx = (group_test == i)
    skinTemp.plot_date(timeStamps[idx],normskintemp[idx],'.',label="Class %d" % i)
    cgmFig.plot_date(timeStamps[idx],cgm[idx],'.',label="Class %d" % i)
'''

#test_st = normskintemp[int(lenTrain)+1:samples]
#test_cgm = cgm[int(lenTrain)+1:samples]

for i in range(0,len(group_test)):
    start = i*60
    stop = (i+1)*60
    if group_test[i]==0:
        color = 'c.'
        Label = 'Group 0'
    elif group_test[i]==1:
        color = 'm.'
        Label = 'Group 1'
    elif group_test[i]==2:
        color = 'k.'
        Label = 'Group 2'
    skinTemp.plot_date(longTestTime[start:stop],longTestSt[start:stop],color,label=Label)
    cgmFig.plot_date(longTestTime[start:stop],longTestCGM[start:stop],color,label=Label)
pl.xlabel('Time')
fig.autofmt_xdate()

#handles, labels = skinTemp.get_legend_handles_labels()
c = pl.Rectangle((0, 0), 1, 1, fc="c")
m = pl.Rectangle((0, 0), 1, 1, fc="m")
k = pl.Rectangle((0, 0), 1, 1, fc="k")
cgmFig.legend( [c,m,k], ['Group 0','Group 1','Group 2'] )

pl.show()

fig.savefig('plotssvm/svmskincgm117')

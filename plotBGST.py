#! /usr/bin/env python

import numpy as np
import datetime
from datetime import datetime
import pylab as pl
import os
import matplotlib.pyplot as pyplot

def dateconv(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    #print(date)
    return date

def t1dmread(file_name):
    dtypes = np.dtype({ 'names' : ('timestamp', 'skin temp', 'air temp', 'steps', 'lying down', 'sleep', 'physical activity', 'energy', 'sedentary', 'moderate', 'vigorous', 'very vigorous', 'mets', 'hr', 'cgm', 'cgm dir'),
                        'formats' : [datetime, np.float, np.float, np.int, np.int, np.float, np.int, np.float, np.int, np.int, np.int, np.int, np.float, np.int, np.int, np.int] })
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

#--------------------------

# If no plots folder exists, make a folder to store all of the plots
if not os.path.exists('plotsRawData'):
    os.mkdir('plotsRawData')

data = t1dmread('trimmedDataFiles/MYFILE108_trimmed.csv')
timeStamps = np.array(data['timestamp'])
skinTemp = np.array(data['skin temp'])
airTemp = np.array(data['air temp'])
steps = np.array(data['steps'])
hr = np.array(data['hr'])
cgm = np.array(data['cgm'])
cgmDir = np.array(data['cgm dir'])
normskintemp = skinTemp - airTemp


fig = pl.figure()

skinTemp = fig.add_subplot(211)
pl.ylabel('Skin Temp - Ambient Temp')

cgmFig = fig.add_subplot(212)
pl.ylabel('CGM BG')
for i in range(0,len(cgm)):
    if cgmDir[i]==0:
        cgmFig.plot(timeStamps[i],cgm[i],'g.')
    elif cgmDir[i]==1:
        cgmFig.plot(timeStamps[i],cgm[i],'r.')
    elif cgmDir[i]==2:
        cgmFig.plot(timeStamps[i],cgm[i],'b.')
fig.autofmt_xdate()

#skinTemp = fig.add_subplot(212)
#pl.ylabel('Normalized Skin Temp')
'''
for i in range(0,len(cgm)):
    if cgmDir[i]==0:
        skinTemp.plot(timeStamps[i],normskintemp[i],'go')
    elif cgmDir[i]==1:
        skinTemp.plot(timeStamps[i],normskintemp[i],'ro')
    elif cgmDir[i]==-1:
        skinTemp.plot(timeStamps[i],normskintemp[i],'bo')
'''
skinTemp.plot(timeStamps,normskintemp,'m.')
fig.autofmt_xdate()
pl.xlabel('Time')

pl.show()
fig.savefig('plotsRawData/bgstsubplot108')


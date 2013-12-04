'''
trimCSV.py
Shelly Bagchi
-----
This program takes an input CSV file of diabetes sensor data and trims it.
Rows of data that contain inf values or CGM = 0, -1 values are removed.
Groups of CGM data are tagged as rising, falling, or stable.
'''

import csv, sys

#with open('DataFile103.csv', 'rb') as csvfile:
#    csvReader = csv.reader(csvfile, dialect='excel')

assert len(sys.argv) == 2, "Please provide a filename, e.g. 'trimCSV.py MYFILE101'."
filename = str(sys.argv[1])
#filename = 'MYFILE101.no_gaps'
print "----- Trimming file", filename, "-----"

f = open('untrimmedDataFiles/'+filename+'.no_gaps.csv', 'rb')
csvReader = csv.reader(f, dialect='excel')

g = open('trimmedDataFiles/'+filename+'_trimmed.csv', 'wb')
csvWriter = csv.writer(g, dialect='excel')

#i = 0 
csvData = []
for row in csvReader:
    #print ', '.join(row)
    #if i>1:
    #    break
    #else:
    #    i += 1
    csvData.append(row)

#print csvData[0]
#print csvData[1]

print len(csvData), "rows in csvData"

i = 0
j = 0
csvData_trimmed = []
#csvData_trimmed.append([Time (GMT-07:00),Transverse accel - peaks,Forward accel - peaks,Longitudinal accel - peaks,Forward accel - point,Transverse accel - point,Longitudinal accel - point,Skin temp - average,Transverse accel - average,Longitudinal accel - average,Near-body temp - average,Transverse accel - MAD,Longitudinal accel - MAD,Step Counter,Forward accel - average,Forward accel - MAD,GSR - average,Lying down,Sleep,Physical Activity,Energy expenditure,Sedentary,Moderate,Vigorous,Very Vigorous,METs,Heart Rate,CGM])
csvData_trimmed.append(['Time (GMT-07:00)', 'Transverse accel - peaks', 'Forward accel - peaks', 'Longitudinal accel - peaks', 'Forward accel - point', 'Transverse accel - point', 'Longitudinal accel - point', 'Skin temp - average', 'Transverse accel - average', 'Longitudinal accel - average', 'Near-body temp - average', 'Transverse accel - MAD', 'Longitudinal accel - MAD', 'Step Counter', 'Forward accel - average', 'Forward accel - MAD', 'GSR - average', 'Lying down', 'Sleep', 'Physical Activity', 'Energy expenditure', 'Sedentary', 'Moderate', 'Vigorous', 'Very Vigorous', 'METs', 'Heart Rate', 'CGM', 'CGM direction'])
print len(csvData_trimmed[0]), "data labels"
print len(csvData[0]), "columns in csv data"

for k in range(1,len(csvData)):
    if len(csvData_trimmed[0]) >= len(csvData[0]):
        row = csvData[k]
    else:
        row = csvData[k][:-1]
    #row = csvData[k]
    if 'inf' in row:
        i += 1
        #print row
        #csvData.remove(row)
        #csvData.pop( csvData.index(row) )
    elif (row[27] == '-1') or (row[27] == '0'):
    #elif (row[-2] == '-1') or (row[-2] == '0'):
        j += 1
        #print row
        #csvData.remove(row)
        #csvData.pop( csvData.index(row) )
    else:
        csvData_trimmed.append(row)

print "Removed", i, "inf rows"
print "Removed", j, "CGM = -1 rows"
print "Now", len(csvData_trimmed), "rows in csvData_trimmed"

#print csvData[0][0]
#print csvData_trimmed[2]

cgmData = []

for row in csvData_trimmed:
    if csvData_trimmed.index(row)==0:
        pass
    else:
        cgmData.append(int(row[-2]))
#print cgmData[:100]

cgmInterval = 2*30  # at 2 measurements/minute
intervals = int(len(csvData_trimmed)/cgmInterval)
cgmDir = []

print "Finding CGM directions over", intervals, "intervals of", cgmInterval
for i in range(0,intervals):
    start = i*cgmInterval
    stop = (i+1)*cgmInterval    
    cgmSlice = cgmData[start:stop]
    #print "Finding CGM deltas from", start, "to", stop
    
    diff = [(y-x) for (x,y) in zip(cgmSlice[:-1], cgmSlice[1:])]
    #print diff
    #avg = sum(delta)/(len(delta)*1.0)
    delta = sum(diff)
    #print "Interval delta is", sum(delta), "with an average of", avg
    #print "Interval delta is", delta
    if delta<=10 and delta>=-10:
        cgmDir.append(0)
    elif delta<0:
        cgmDir.append(2)
    else:
        cgmDir.append(1)        
#print cgmDir

for i in range(1, len(csvData_trimmed)):
    row = csvData_trimmed[i]
    interval = i/cgmInterval
    if interval>=len(cgmDir):
        interval = len(cgmDir)-1
    
    row[-1] = cgmDir[interval]
#print csvData_trimmed[1]
#print csvData_trimmed[60]
#print csvData_trimmed[120]
#print csvData_trimmed[-1]

for row in csvData_trimmed:
    #print row
    csvWriter.writerow(row)


f.close()
g.close()
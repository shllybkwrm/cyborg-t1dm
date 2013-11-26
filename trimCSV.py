'''
trimCSV.py
Shelly Bagchi
-----
This program takes an input CSV file of diabetes sensor data and trims it.
Rows of data that contain inf values or CGM = 0, -1 values are removed.
'''

import csv

#with open('DataFile103.csv', 'rb') as csvfile:
#    csvReader = csv.reader(csvfile, dialect='excel')

filename = 'MYFILE101.no_gaps'
print "----- Trimming file", filename, "-----"

f = open('untrimmedDataFiles/'+filename+'.csv', 'rb')
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
csvData_trimmed.append(['Time (GMT-07:00)', 'Transverse accel - peaks', 'Forward accel - peaks', 'Longitudinal accel - peaks', 'Forward accel - point', 'Transverse accel - point', 'Longitudinal accel - point', 'Skin temp - average', 'Transverse accel - average', 'Longitudinal accel - average', 'Near-body temp - average', 'Transverse accel - MAD', 'Longitudinal accel - MAD', 'Step Counter', 'Forward accel - average', 'Forward accel - MAD', 'GSR - average', 'Lying down', 'Sleep', 'Physical Activity', 'Energy expenditure', 'Sedentary', 'Moderate', 'Vigorous', 'Very Vigorous', 'METs', 'Heart Rate', 'CGM'])
for k in range(1,len(csvData)):
    row = csvData[k]
    if 'inf' in row:
        i += 1
        #print row
        #csvData.remove(row)
        #csvData.pop( csvData.index(row) )
    elif (row[len(row) - 3] == '-1') or (row[len(row) - 1] == '0'):
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

for row in csvData_trimmed:
    #print row
    csvWriter.writerow(row)


f.close()
g.close()
import csv

#with open('DataFile103.csv', 'rb') as csvfile:
#    csvReader = csv.reader(csvfile, dialect='excel')

f = open('DataFile103.csv', 'rb')
csvReader = csv.reader(f, dialect='excel')

g = open('DataFile103_trimmed.csv', "wb")
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
for k in range(len(csvData)):
    row = csvData[k]
    if 'inf' in row:
        i += 1
        #print row
        #csvData.remove(row)
        #csvData.pop( csvData.index(row) )
    elif (row[len(row) - 1] == '-1') or (row[len(row) - 1] == '0'):
        j += 1
        #print row
        #csvData.remove(row)
        #csvData.pop( csvData.index(row) )
    else:
        csvData_trimmed.append(row)

print "Removed", i, "inf rows"
print "Removed", j, "CGM = -1 rows"
print "Now", len(csvData_trimmed), "rows in csvData_trimmed"

#print csvData[2]
#print csvData_trimmed[2]

for row in csvData_trimmed:
    #print row
    csvWriter.writerow(row)


f.close()
g.close()
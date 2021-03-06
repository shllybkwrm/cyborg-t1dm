import csv
#import scipy.stats.pearsonr
import numpy as np
import datetime as DT
import matplotlib.pyplot as plt
from pylab import *
from scipy.stats import *

def make_date(datestr):
		return DT.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')

class plotallcol(object):
	
	def reader(self,file):		
		arr = np.genfromtxt(file, delimiter=',',
						converters={'Date': make_date}, names =  ('Date', '2TAPeaks', '3FAPeaks', '4LAPeaks', '5FAPoint', '6TAPoint', '7LAPoint', '8SkinTempAve', '9TAAve', '10LAAve', '11NBTempAve', 
		'12TAMAD', '13LAMAD', '14StepC', '15FAAve', '16FAMAD', '17GSRAve', '18LyingD', '19Sleep', '20PhysAc', '21EnExp', '22Sedent', '23Moderate', '24Vigorous', '25VVig', '26METs','27HRMValue','28SensorValue','29SensorDate','30HRMDate','31Extra'),
						dtype = None)
						
		index={1:'Date', 2:'2TAPeaks', 3:'3FAPeaks', 4:'4LAPeaks', 5:'5FAPoint', 6:'6TAPoint', 7:'7LAPoint', 8:'8SkinTempAve', 9:'9TAAve', 10:'10LAAve', 11:'11NBTempAve', 
		12:'12TAMAD', 13:'13LAMAD', 14:'14StepC', 15:'15FAAve', 16:'16FAMAD', 17:'17GSRAve', 18:'18LyingD', 19:'19Sleep', 20:'20PhysAc', 21:'21EnExp', 22:'22Sedent', 23:'23Moderate', 24:'24Vigorous', 25:'25VVig', 26:'26METs', 27:'27HRMValue', 28:'28SensorValue', 29:'29SensorDate', 30:'30HRMDate'}
		
		return arr,index
	
	def bestspace(self,arr,index,thecolumn,interval):
		
						
		# Find the first instance of a CGM value in MYFILE
		p=1 # P is the CGM start point
		con=True
		while con:
			if(arr['28SensorValue'][p]==-1):
				p+=1
			else:	
				con=False
		if(p<interval):
			p=interval
			
		maxcount=0
		bestspace=0
		for space in range(0,121):
			count=0
			thisp=p+space
			for x in range(thisp,len(arr)-interval):
				m=(pearsonr( arr['28SensorValue'][x:x+interval],arr[index[thecolumn]][x-interval-space:x-space])[0])
				if(m*m)>0.85:
					count+=1
			if count>maxcount:
				maxcount=count
				bestspace=space

		return bestspace,p+space,(maxcount+0.0)/((len(arr)-1)+0.0)		
	
	def first(self,arr,index,thecolumn,interval):
		# Find the first instance of a CGM value in MYFILE
		p=1 # P is the CGM start point
		con=True
		while con:
			if(arr['28SensorValue'][p]==-1):
				p+=1
			else:	
				con=False
		if(p<interval):
			p=interval
		count=0	
		space=0
		for x in range(p,len(arr)-interval):
			m=(pearsonr( arr['28SensorValue'][x:x+interval],arr[index[thecolumn]][x-interval-space:x-space])[0])
			if(m*m)>0.85:
				count+=1
		return 0,p, (count+0.0)/((len(arr)-1)+0.0)		

	
	def plotter(self,savefile,histogramsave,arr,index,thecolumn,space,p,interval):
		colindex=[] 
		correlation=[]
		
		
		for x in range(p,len(arr)-interval):
			colindex.append(x)
			m=(pearsonr( arr['28SensorValue'][x:x+interval],arr[index[thecolumn]][x-interval-space:x-space])[0])
			if(isnan(m)): m=0
			correlation.append(  m*m ) # 60 rows down from the current index p for CGM and 60 rows behind from that for the other column
			
		histogramsave+="+StandardDev_"+str(np.std(correlation))+"_Average_"+str(np.average(correlation))+".pdf"
		
		plt.clf()
		plt.cla()
		plt.scatter(colindex,correlation,s=0.1)
		plt.plot(colindex,correlation,linewidth=0.25, color='g')
		plt.xlabel('Sensor Value')
		plt.ylabel(index[thecolumn])
		plt.axhline(y=.85, color='r')
		savefig(savefile,format='pdf')
		
		plt.clf()
		plt.cla()
		plt.xlim(0,1)
		plt.axvline(x=.85, color='r',linewidth=0.1)
		plt.hist(correlation,2000,(0.0,1.0))
		plt.xlabel(index[thecolumn]+' histogram')
		plt.ylabel('Sensor Value')
		
		savefig(histogramsave,format='pdf')
		
		
ninterval=[90]		
for i in ninterval:	
	fname=[112]
	for x in fname:	
		print x," ",ninterval
		sl=plotallcol()
		arr,index=sl.reader("/home/strickland/cyborg-t1dm/viztool/MYFILE104.no_gaps.csv")
		interval=(i*2)+1
		cols=[8]
		for y in cols:
			
			space,startpoint,maxcount=sl.bestspace(arr,index,y,interval)
			#space,startpoint,maxcount=sl.first(arr,index,y,interval)
			
			histogramsave="/home/strickland/cyborg-t1dm/viztool/Histogram"+index[y]+"_individual_"+str(x)+"_"+str(space)+"_Totalcount_"+str(maxcount)
			correlationsave="/home/strickland/cyborg-t1dm/viztool/Spaced_CorrelationPlot_"+index[y]+"_individual_"+str(x)+"_"+str(space)+"_Totalcount_"+str(maxcount)+".pdf"
			sl.plotter(correlationsave,histogramsave,arr,index,y,space,startpoint,interval)		
		print space
#histogramsave="E:\Dropbox\DMITRI_Data_GT\CorrelationPlot_"+str(interval)+"_rows\Histogram"+index[y]+"_individual_"+str(x)+"_"+str(space)+"_Totalcount_"+str(maxcount)

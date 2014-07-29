#  precisionRecallPlot.py  
#  This script needs to be called with two inputs:
#  1) the filename of a .csv file  that was generated with Analysis/randomForestAnalysis.py
#  2) a filename to output the plot to.
#
#  The script will read the data, pull out the actual results and predicted probability
#  and compute Precision and Recall at thresholds from 0 to 1
#



from __future__ import division
import pandas as pd
import numpy as np
import argparse


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('infname', help='Name of Random Forests Output File (.csv file)')
parser.add_argument('outfname', help='Name of Output Figure File (.png file)')
args = parser.parse_args()
infname = args.infname
outfname = args.outfname




df=pd.read_csv(infname)

predic_prob=np.array(df['predic_prob10'])
actual=np.array(df['actual0'])

P=np.empty([101])
R=np.empty([101])
		
for i in range(0,101):
	T=i*0.01
	ppred=predic_prob<T
#	TP=sum(labels[test]*1+ppred==2)
#	FP=sum(labels[test]*1-ppred==-1)
#	FN=sum(ppred*1-labels[test]*1==-1)
	TP=sum(actual*1+ppred==2)
	FP=sum(actual*1-ppred==-1)
	FN=sum(ppred*1-actual*1==-1)
	P[i]=TP/(TP+FP)
	R[i]=TP/(TP+FN)
	#print 'P=' + str(P) + ' and R=' + str(R)
	del ppred
	print str(T)
	
import matplotlib.pyplot as plt
plt.scatter(R,P)
plt.xlim(0,1),plt.ylim(0,1)
plt.plot([0,1],[1,0])
plt.xlabel('Recall')
plt.ylabel('Precision')

svplt=1
if svplt==1:
	print 'Saving plot as', outfname
	plt.savefig(outfname)


plt.show()
		

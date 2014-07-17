# Hey guys,
# A primitive attempt to read in a bunch of data, move it around a bit, then run a machine learning algorithm on the data.
# Not much accomplished from a grand perspective, but good from my standpoint to be working with Python. 
# I'll be back tomorrow to keep cleaning it up and to really dig into the machine learning component. 
# 
#This attempt was done on a subset of the data that I used, but it should work on the larger data set.  Not tested yet.

import pandas as pd
import datetime as dt
import numpy as np
import scipy as sp

#%reset clear variables ?

fname='berkeley_ping_data_1000.csv'
raw_dat=pd.read_csv(fname,skipinitialspace=True)
#raw_dat["Make"]=raw_dat.map(str.strip)

#raw_dat.dtypes
#raw_dat['ping_id']=raw_dat['ping_id'].astype('int')  #'float' etc...

#Convert to datetime
raw_dat['last_impression_date'][raw_dat['last_impression_date']=='None']=np.NaN
raw_dat['last_impression_time'][raw_dat['last_impression_time']=='None']=np.NaN
raw_dat['last_seen_online_date'][raw_dat['last_seen_online_date']=='None']=np.NaN
raw_dat['last_seen_online_time'][raw_dat['last_seen_online_time']=='None']=np.NaN
raw_dat['date_clicked'][raw_dat['date_clicked']=='None']=np.NaN
raw_dat['time_clicked'][raw_dat['time_clicked']=='None']=np.NaN
raw_dat['date_sent_success'][raw_dat['date_sent_success']=='None']=np.NaN
raw_dat['time_sent_success'][raw_dat['time_sent_success']=='None']=np.NaN


raw_dat['li_datetime']=pd.to_datetime(raw_dat['last_impression_date'] + ' ' + raw_dat['last_impression_time'])
raw_dat['lso_datetime']=pd.to_datetime(raw_dat['last_seen_online_date'] + ' ' + raw_dat['last_seen_online_time'])
raw_dat['tu_clicked_datetime']=pd.to_datetime(raw_dat['time_clicked'] + ' ' + raw_dat['date_clicked']) #backwards due to label errors
raw_dat['ping_sent_datetime']=pd.to_datetime(raw_dat['date_sent_success'] + ' ' + raw_dat['time_sent_success']) 


#These define the Tutors who Responded within 60 seconds...
#NOT the response time for the student...which would have to be calculated using the earliest 
#Ping_sent
raw_dat['response_time']=raw_dat['tu_clicked_datetime']-raw_dat['ping_sent_datetime']
raw_dat['response_time']=raw_dat['response_time'].astype('timedelta64[s]')

raw_dat['li_dt']=raw_dat['ping_sent_datetime']-raw_dat['li_datetime']
raw_dat['li_dt']=raw_dat['li_dt'].astype('timedelta64[s]')

raw_dat['lso_dt']=raw_dat['ping_sent_datetime']-raw_dat['lso_datetime']
raw_dat['lso_dt']=raw_dat['lso_dt'].astype('timedelta64[s]')

raw_dat['success']=raw_dat['response_time']<60


raw_dat.drop('last_impression_date',axis=1,inplace=True)
raw_dat.drop('last_impression_time',axis=1,inplace=True)
raw_dat.drop('last_seen_online_date',axis=1,inplace=True)
raw_dat.drop('last_seen_online_time',axis=1,inplace=True)
raw_dat.drop('date_clicked',axis=1,inplace=True)
raw_dat.drop('time_clicked',axis=1,inplace=True)
raw_dat.drop('date_sent_success',axis=1,inplace=True)
raw_dat.drop('time_sent_success',axis=1,inplace=True)
raw_dat.drop(['time_clicked_score','timezone','lesson_subject','ping_id'],axis=1,inplace=True)
raw_dat.drop(['li_datetime','lso_datetime','tu_clicked_datetime','ping_sent_datetime','response_time'],axis=1,inplace=True)

unique_lesson_ids=raw_dat['lesson_id'].unique()
train_id=unique_lesson_ids[0::2]
test_id=unique_lesson_ids[1::2]


#Create the Training Data
#Get First Lesson to Create the Data Frame
loar=raw_dat['lesson_id']==train_id[0]
train_dat=pd.DataFrame.as_matrix(raw_dat[loar])
del loar

#Remove the First Id then iterate through the rest
train_id=train_id[1::1]
for d in train_id:
	loar=raw_dat['lesson_id']==d  #loar= Logical Array
	tmpdat=pd.DataFrame.as_matrix(raw_dat[loar])
	train_dat=np.append(train_dat,tmpdat,axis=0)
	del loar
	del tmpdat
	
#Create the Testing Data
#Get First Lesson to Create the Data Frame
loar=raw_dat['lesson_id']==test_id[0]
test_dat=pd.DataFrame.as_matrix(raw_dat[loar])
del loar

#Remove the First Id then iterate through the rest
test_id=test_id[1::1]
for d in test_id:
	loar=raw_dat['lesson_id']==d  #loar= Logical Array
	tmpdat=pd.DataFrame.as_matrix(raw_dat[loar])
	test_dat=np.append(test_dat,tmpdat,axis=0)
	del loar
	del tmpdat

#Convert boolean to numerical
test_dat=test_dat*1
train_dat=train_dat*1

#print train_dat[:,7]
	
from sklearn.ensemble import RandomForestClassifier
	
print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_dat[0::,0:6], train_dat[:,7] )

print 'Predicting...'
output = forest.predict(test_dat[0::,0:6])

#Compare output and test_dat[0::,7]
num_records=output.size


corr=test_dat[:,7]-output
overall_pctcorr=sum(corr==0)/num_records

tutors_show=test_dat[:,7]==1  # A logical Array to map to the output
tutor_pctcorr=sum(output[tutors_show])/sum(tutors_show)

#print 'Overall Number Correct = ' + overall_pctcorr
#print ''
#print 'Correctly Prediced When Tutors Did Repond within One Minute  = ' + tutor_pctcorr



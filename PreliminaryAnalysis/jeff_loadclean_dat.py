# Hey guys,
# A primitive attempt to read in a bunch of data, move it around a bit, then run a machine learning algorithm on the data.
# Not much accomplished from a grand perspective, but good from my standpoint to be working with Python. 
# I'll be back tomorrow to keep cleaning it up and to really dig into the machine learning component. 
# 
from __future__ import division
import pandas as pd
import datetime as dt
import numpy as np
import scipy as sp
import time
import pickle 


#%reset clear variables ?

fname='berkeley_ping_data.csv'
raw_dat=pd.read_csv(fname,skipinitialspace=True,na_values='None')
#raw_dat.dtypes

#Convert to datetime
#Takes about 50 seconds per calculation...why so long?
raw_dat['li_datetime']=pd.to_datetime(raw_dat['last_impression_date'] + ' ' + raw_dat['last_impression_time'])
raw_dat['lso_datetime']=pd.to_datetime(raw_dat['last_seen_online_date'] + ' ' + raw_dat['last_seen_online_time'])
raw_dat['tu_clicked_datetime']=pd.to_datetime(raw_dat['time_clicked'] + ' ' + raw_dat['date_clicked']) #backwards due to label errors
raw_dat['ping_sent_datetime']=pd.to_datetime(raw_dat['date_sent_success'] + ' ' + raw_dat['time_sent_success']) 


#These define the Tutors who Responded within 60 seconds...
#This is NOT the response time for the student...which would have to be calculated using the earliest 
#Ping_sent

raw_dat['response_time']=(raw_dat['tu_clicked_datetime']-raw_dat['ping_sent_datetime']).astype('timedelta64[s]')
raw_dat['li_dt']=(raw_dat['ping_sent_datetime']-raw_dat['li_datetime']).astype('timedelta64[s]')
raw_dat['lso_dt']=(raw_dat['ping_sent_datetime']-raw_dat['lso_datetime']).astype('timedelta64[s]')
raw_dat['success']=raw_dat['response_time']<60


raw_dat.drop(['last_impression_date','last_impression_time'],axis=1,inplace=True)
raw_dat.drop(['last_seen_online_date','last_seen_online_time'],axis=1,inplace=True)
raw_dat.drop(['date_clicked','time_clicked'],axis=1,inplace=True)
raw_dat.drop(['date_sent_success','time_sent_success'],axis=1,inplace=True)
raw_dat.drop(['time_clicked_score','timezone','lesson_subject','ping_id'],axis=1,inplace=True)
raw_dat.drop(['li_datetime','lso_datetime','tu_clicked_datetime','ping_sent_datetime','response_time'],axis=1,inplace=True)

#Identify the Trianing and Testing Data, keeping lessons together
unique_lesson_ids=raw_dat['lesson_id'].unique()
train_id=unique_lesson_ids[0::2]
test_id=unique_lesson_ids[1::2]


train_df=raw_dat[raw_dat['lesson_id'].isin(train_id)]
test_df=raw_dat[raw_dat['lesson_id'].isin(test_id)]

# Convert boolean to numerical
test_df=test_df*1
train_df=train_df*1


test_df=test_df.dropna(axis=0)
train_df=train_df.dropna(axis=0)

train_df.to_pickle('jd_trainingdata_df.pkl')
test_df.to_pickle('jd_testingdata_df.pkl')


# mergeTutorPingDataFrames.py
# Add the tutor data to the cleanPingDataFrame data to create cleanPingTutorDataFrame:
#   fraction of pings responded to (add in for given statuses/times)
#   n_pings = number of times pinged
#   n_clicks = number of times tutor connected
#   n_clicks_under_30 = number of times tutor connected within 30 seconds
#   hourly_response[hour] = in local timezone, what fraction of pings do tutors respond to within 30 seconds
#   hourly_response_n_clicked[hour] = gives total number clicked within 30 seconds for each hour
#   hourly_response_n_not_clicked[hour] = gives number not clicked within 30 seconds for each hour
#   hourly_average_sec_response[hour] = gives average tutor response rate when they do connect

import pandas as pd
import numpy as np
import sys
sys.path.append('./Analysis')
from loadData import load_pickle
import cPickle


#Load the Tutor and Ping Data
tutor_fname='Data/tutorDataFrame.pickle'
tdata=load_pickle(tutor_fname)
ping_fname='Data/cleanPingDataFrame.pickle'
pdata=load_pickle(ping_fname)

#Copy the dataframe and add new columns
pt_df=pdata
pt_df['hourly_avg_sec_response']=np.nan
pt_df['hourly_response']=np.nan
pt_df['hourly_response_n_clicked']=np.nan
pt_df['hourly_response_n_not_clicked']=np.nan
pt_df['n_clicks']=np.nan
pt_df['n_clicks_under_30']=np.nan
pt_df['n_pings']=np.nan

# Round to the lower hour to avoid 24 which will not work as an index to the dataframe
hour=np.floor(pt_df['time_sent_success_local'])
	
# Loop through the rows 
for i in pt_df.index:
	if i%10000==0: print "Pings evaluated:", i, "/", len(pt_df.index)
	tutor=pt_df.iloc[i]['tutor_id']
	tutor_local_time=int(hour[i])
	pt_df['hourly_avg_sec_response'][i]=tdata[tutor].hourly_average_sec_response[tutor_local_time]
	pt_df['hourly_response'][i]=tdata[tutor].hourly_response[tutor_local_time]
	pt_df['hourly_response_n_clicked'][i]=tdata[tutor].hourly_response_n_clicked[tutor_local_time]
	pt_df['hourly_response_n_not_clicked'][i]=tdata[tutor].hourly_response_n_not_clicked[tutor_local_time]
	pt_df['n_clicks'][i]=tdata[tutor].n_clicks
	pt_df['n_clicks_under_30'][i]=tdata[tutor].n_clicks_under_30
	pt_df['n_pings'][i]=tdata[tutor].n_pings

print "Saving Ping/Tutor dataframe..."
with open(r"Data/cleanPingTutorDataFrame.pickle", "wb") as output_file:
    cPickle.dump(pt_df, output_file)		

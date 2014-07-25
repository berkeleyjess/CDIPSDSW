# Create dataframe indexed by tutor_id with attributes:
#   fraction of pings responded to (add in for given statuses/times)
#   n_pings = number of times pinged
#   n_clicks = number of times tutor connected
#   n_clicks_under_30 = number of times tutor connected within 30 seconds
#   hourly_response[hour] = in local timezone, what fraction of pings do tutors respond to within 30 seconds
#   hourly_response_n_clicked[hour] = gives total number clicked within 30 seconds for each hour
#   hourly_response_n_not_clicked[hour] = gives number not clicked within 30 seconds for each hour
#   hourly_average_sec_response[hour] = gives average tutor response rate when they do connect
#   subjects = list of subjects taught by tutor

import pandas as pd
import numpy as np
import cPickle
from pytz import timezone

def readTutorData(pings_df):

    total_pings = len(pings_df['tutor_id'])

    # Get list of all unique tutor IDs
    tutor_ids=pings_df['tutor_id'].unique()

    # Produce dataframe indexed by tutor_id with attributes above
    print "Getting tutor info..."
    df_dict = {}
    series_dicts = {}
    for tid in tutor_ids:
        series_dicts[tid] = {}

    for x in xrange(total_pings):
        if x%10000==0: print "Pings evaluated:", x, "/", total_pings

        entry = pings_df.iloc[x, :]
        tid = entry['tutor_id']

        # Add number of pings variable, and if first instance, initialize all other variables
        if 'n_pings' in series_dicts[tid]: series_dicts[tid]['n_pings']+=1
        else:
            series_dicts[tid]['n_pings']=1
            series_dicts[tid]['n_clicks']=0
            series_dicts[tid]['n_clicks_under_30']=0
            series_dicts[tid]['hourly_response_n_clicked']=[0]*24
            series_dicts[tid]['hourly_response_n_not_clicked']=[0]*24
            series_dicts[tid]['hourly_average_sec_response']=[0]*24
            series_dicts[tid]['subjects']=[]

        # Add number of clicks variables
        if entry['time_clicked'] != None:
            series_dicts[tid]['n_clicks']+=1
            series_dicts[tid]['hourly_average_sec_response'][int(entry['time_sent_success_local'])]+=entry['sec_response']
        if entry['time_clicked'] != None and entry['sec_response']<30:
            series_dicts[tid]['n_clicks_under_30']+=1
            series_dicts[tid]['hourly_response_n_clicked'][int(entry['time_sent_success_local'])]+=1
        else: series_dicts[tid]['hourly_response_n_not_clicked'][int(entry['time_sent_success_local'])]+=1

        # Add list of subjects taught
        series_dicts[tid]['subjects'].append(entry['lesson_subject'])


    print "Building tutor dataframe..."

    for tid in series_dicts.keys():
        # Keep only unique subjects
        series_dicts[tid]['subjects'] = list(set(series_dicts[tid]['subjects']))

        # Compute hourly response
        series_dicts[tid]['hourly_response'] = []
        for x in xrange(24):
            total_this_hour = series_dicts[tid]['hourly_response_n_clicked'][x] + series_dicts[tid]['hourly_response_n_not_clicked'][x]
            if total_this_hour == 0: series_dicts[tid]['hourly_response'].append(-1)
            else: series_dicts[tid]['hourly_response'].append(series_dicts[tid]['hourly_response_n_clicked'][x] / float(total_this_hour))

            # Compute average response time
            if series_dicts[tid]['hourly_response_n_clicked'][x]!=0:
                series_dicts[tid]['hourly_average_sec_response'][x] /= float(series_dicts[tid]['hourly_response_n_clicked'][x])
            else: series_dicts[tid]['hourly_average_sec_response'][x] = -1

        # Form series to go into dataframe
        s = pd.Series(series_dicts[tid])
        df_dict[tid] = s

    # Make final dataframe
    tutor_df = pd.DataFrame(df_dict)

    return tutor_df

if __name__ == '__main__':
    # Import data file
    print "Loading in ping data..."
    with open(r"Data/cleanPingDataFrame.pickle", "rb") as input_file:
        pings_df = cPickle.load(input_file)

    tutor_df = readTutorData(pings_df)

    print "Saving tutor dataframe..."
    with open(r"Data/tutorDataFrame.pickle", "wb") as output_file:
        cPickle.dump(tutor_df, output_file)



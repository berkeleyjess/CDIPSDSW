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
import sys
sys.path.append('./Analysis')
from processTools import add_weighted_hourly_response

def readTutorData(pings_df, weight=10.0):
    """
    The weight option is for the weighted_hourly_response
    column - see add_weighted_hourly_response in
    processTools.py.
    """

    total_pings = len(pings_df['tutor_id'])

    # Get list of all unique tutor IDs
    tutor_ids=pings_df['tutor_id'].unique()

    # Produce dataframe indexed by tutor_id with attributes above
    print "Getting tutor info..."
    df_dict = {}
    series_dicts = {}
    for tid in tutor_ids:
        series_dicts[tid] = {}

    from time import time
    t0 = time()
    
    # Loop over pings grouped by tutor_id
    for i, (tid, tutor_pings) in enumerate(pings_df.groupby(
            'tutor_id', sort=False)):
        if i%1000 == 0:
            print '    Tutors evaluated:', i, '/', len(tutor_ids)

        series_dicts[tid]['n_pings'] = len(tutor_pings)
        series_dicts[tid]['n_clicks'] = len(
            tutor_pings[~pd.isnull(tutor_pings.time_clicked)])
        series_dicts[tid]['n_clicks_under_30'] = len(
            tutor_pings[tutor_pings.sec_response < 30.])
        series_dicts[tid]['subjects'] = list(set(
            tutor_pings.lesson_subject))

        # Loop over pings grouped by tutor's local hour
        series_dicts[tid]['hourly_response_n_clicked'] = np.zeros(24)
        series_dicts[tid]['hourly_response_n_not_clicked'] = np.zeros(24)
        series_dicts[tid]['hourly_average_sec_response'] = np.zeros(24)
        for h, g in tutor_pings.groupby(
                tutor_pings.time_sent_success_local.apply(
                lambda x: int(x))):
            series_dicts[tid]['hourly_response_n_not_clicked'][h] = \
                len(g.sec_response[~(g.sec_response < 30.)])
            series_dicts[tid]['hourly_response_n_clicked'][h] = \
                len(g.sec_response) - \
                series_dicts[tid]['hourly_response_n_not_clicked'][h]
            total_sec_response = g.sec_response.sum()
            series_dicts[tid]['hourly_average_sec_response'][h] = \
                0 if pd.isnull(total_sec_response) else total_sec_response

    print "Building tutor dataframe..."

    for tid in series_dicts.keys():
        # Keep only unique subjects
        #series_dicts[tid]['subjects'] = list(set(series_dicts[tid]['subjects']))

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

    # Add a 'weighted_hourly_response' column
    tutor_df = add_weighted_hourly_response(tutor_df, 
                                            weight=weight)
    
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



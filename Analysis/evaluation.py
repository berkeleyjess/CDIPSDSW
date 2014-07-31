# This file should read in the output csv's from Analysis files and comparatively assess them. Much of this will probably be moved into plotting scripts once we're dealing with continuous variables.


"""
Given test data from a ping DataFrame with added data on tutors
and a model fit to training data:

- select lessons (tutoring requests) by their lesson IDs,

- rank all tutors within a lesson using the model predictions
  (randomize order before sorting to deal with tutors with 
  equal predicted probability),

- compute and compare statistics on tutor responses to pings from  
  both the model-based rankings and the actual outcomes.
"""

import numpy as np
import pandas as pd
import datetime

# load ping data
print 'Loading ping data...'
from loadData import load_pickle
ping_df = load_pickle('Data/cleanPingDataFrame.pickle')

# load model results
print 'Loading model results...'
pred_csv = 'Analysis/Data/RF.csv'
ping_id_headers = ['ping_id' + str(i) for i in range(3)]
actual_headers = ['actual' + str(i) for i in range(3)]
prob_headers = ['predicted_probability' + str(i) for i in range(3)]
pred_df = pd.read_csv(pred_csv)

n_for_fast_response_actual = []
n_for_fast_response_pred = []
n_fast_in_first_5_actual = []
n_fast_in_first_5_pred = []
wait_time_actual = []
wait_time_pred = []

print 'Simulating pings and computing statistics...'
for ping_id, actual, prob in zip(ping_id_headers, actual_headers, prob_headers):
    # get useful columns from ping DataFrame
    test_ping_df = ping_df[ping_df.id.isin(pred_df[ping_id].values)]
    for col in ['lesson_id', 'id', 'time_sent_success', 'time_clicked', 'sec_response', 'sec_since_online']:
        new_col = test_ping_df[col]
        new_col.index = pred_df[ping_id].index
        pred_df[col] = new_col
    # compute new actual values
    #pred_df[actual] = (pred_df.sec_response < 30.)
    # group by lesson_id
    # **** REMOVE HEAD(50) ****
    for lesson, lesson_df in pred_df.head(1000).groupby('lesson_id', sort=False):
        # only include lessons with a complete set of predictions and at least one fast response
        if (len(lesson_df) == len(ping_df[ping_df.lesson_id == lesson])) and \
                lesson_df[actual].values.any():
            
            # shuffle indices to randomize pings with equal assigned probabilities
            ind = np.array(range(len(lesson_df)))
            np.random.shuffle(ind)
            sim_ping_order = ind[(-lesson_df[prob].values[ind]).argsort()]
            #print sim_ping_order
            
            #print np.vstack((lesson_df[actual], lesson_df[prob], lesson_df.sec_response < 30.))
            if not (lesson_df[actual] == (lesson_df.sec_response < 30.)).all():
                print lesson, np.vstack((lesson_df[ping_id], lesson_df.id, lesson_df[actual], lesson_df.sec_response < 30.))
            
            # indices of pings with < 30 sec response time
            fast_responses_actual = np.where(lesson_df[actual])[0]
            fast_responses_pred = np.where(lesson_df[actual].values[sim_ping_order])[0]
            
            # number of pings required to get < 30 sec response
            n_for_fast_response_actual.append(fast_responses_actual.min() + 1)
            n_for_fast_response_pred.append(fast_responses_pred.min() + 1)
            
            # number of pings in first 5 with < 30 sec responses
            if len(lesson_df) >= 5:
                n_fast_in_first_5_actual.append(float(len(np.where(fast_responses_actual < 5)[0])))
                n_fast_in_first_5_pred.append(float(len(np.where(fast_responses_pred < 5)[0])))
                
            # wait time from first ping sent to first response
            def timedelta_with_nan(dt):
                if np.isnan(dt):
                    return datetime.timedelta(days=365) # replace NaNs with 1-year response times
                else:
                    return datetime.timedelta(seconds=dt)
            sim_time_clicked = np.array([t + timedelta_with_nan(dt) \
                                         for (t, dt) in zip(lesson_df.time_sent_success.values,
                                                            lesson_df.sec_response.values[sim_ping_order])])
            min_time_clicked = lesson_df.time_clicked.dropna().min()
            if 'float' in str(type(min_time_clicked)):
                print lesson, lesson_df.time_clicked.values, lesson_df[actual].values, lesson_df.sec_since_online.values
            else:
                wait_time_actual.append((lesson_df.time_clicked.dropna().min() - lesson_df.time_sent_success.min()).seconds)
                wait_time_pred.append((sim_time_clicked.min() - lesson_df.time_sent_success.min()).seconds)
            

for x in [n_for_fast_response_actual, n_for_fast_response_pred, 
          n_fast_in_first_5_actual, n_fast_in_first_5_pred,
          wait_time_actual, wait_time_pred]:
    print np.mean(x)



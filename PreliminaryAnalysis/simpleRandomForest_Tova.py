import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier
import cPickle
from pytz import timezone

#execfile('jess_scripts/time_zones.py')

# Import data files
with open(r"Data/trainDataFrame.pickle", "rb") as input_file:
    train_df = cPickle.load(input_file)
with open(r"Data/testDataFrame.pickle", "rb") as input_file:
    test_df = cPickle.load(input_file)

with open(r"Data/tutorDataFrame.pickle", "rb") as input_file:
    tutor_df = cPickle.load(input_file)
with open(r"Data/subjectDataFrame.pickle", "rb") as input_file:
    subject_df = cPickle.load(input_file)

print tutor_df[79223]
print subject_df['Game Theory']

'''
# Full list of variables: 'available', 'available_now', 'client', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'

for df in [train_df, test_df]:

    # Store variables relative to when ping was sent
    f = lambda x: 0 if x==None else x / np.timedelta64(1, 'h')
    j = lambda x: 0 if np.isnan(x) or np.isinf(x) else x

    df['online_for'] = df['time_sent_success'] - df['last_seen_online_time']
    df['online_for']=df['online_for'].map(f)
    df['online_for']=df['online_for'].map(j)

    df['last_impression'] = df['time_sent_success'] - df['last_impression_time']
    df['last_impression']=df['last_impression'].map(f)
    df['last_impression']=df['last_impression'].map(j)

    # Get time in local timezone
    f = lambda x: 0 if x==None or np.isnan(x) or np.isinf(x) else x

    df['local_time'] = df['time_sent_success']
    for x in xrange(len(df['timezone'])):
        tz = timezone(COMMON_TIMEZONES_STR[df['timezone'][x]])
        df['local_time'][x] = df['time_sent_success'][x].astimezone(tz).hour + df['time_sent_success'][x].astimezone(tz).minute/60.
    df['local_time'] = df['local_time'].map(f)

    # Add my success variable to the training sample
    f = lambda x: False if x==None else True
    df['clicked'] = df['time_clicked'].map(f)

# Store IDs and true answer for output
ids = test_df['id'].values
real_click = test_df['clicked'].values
fit_data = train_df['clicked'].values

# Remove everything I don't care about
train_df = train_df.drop(['clicked', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'], axis=1)

test_df = test_df.drop(['clicked', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'], axis=1)

# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_df.values
test_data = test_df.values

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data, fit_data )

print 'Predicting...'
output = forest.predict(test_data)

predictions_file = open("output_guesses.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["id","will_click", "did_click"])
open_file_object.writerows(zip(ids, output, real_click))
predictions_file.close()
print 'Done.'
'''

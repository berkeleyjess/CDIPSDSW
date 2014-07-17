import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier
import cPickle

# Import data files
with open(r"Data/trainDataFrame.pickle", "rb") as input_file:
    train_df = cPickle.load(input_file)
with open(r"Data/testDataFrame.pickle", "rb") as input_file:
    test_df = cPickle.load(input_file)

# Full list of variables: 'available', 'available_now', 'client', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'

# Add my success variable to the training sample
f = lambda x: False if x==None else True
train_df['clicked'] = train_df['time_clicked'].map(f)
test_df['clicked'] = test_df['time_clicked'].map(f)

# Store IDs and true answer for output
ids = test_df['id'].values
real_click = test_df['clicked'].values

# Remove everything I don't care about
train_df = train_df.drop(['client', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'], axis=1)

test_df = test_df.drop(['clicked', 'client', 'id', 'last_impression_time', 'last_seen_online_time', 'lesson_id', 'lesson_subject', 'time_clicked', 'time_clicked_score', 'time_sent_success', 'timezone', 'tutor_id'], axis=1)

# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_df.values
test_data = test_df.values

# Note that I need to add the 'clicked' field last
(nrows, ncols) = train_data.shape

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,0::ncols-1], train_data[0::,ncols-1] )

print 'Predicting...'
output = forest.predict(test_data)

predictions_file = open("output_guesses.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["id","will_click", "did_click"])
open_file_object.writerows(zip(ids, output, real_click))
predictions_file.close()
print 'Done.'


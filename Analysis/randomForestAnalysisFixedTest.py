"""
Train random forest classifier based on whether tutor response is 
above or below a specified time threshold.

Outputs:

- csv file with 3*k columns where k is the 
  number of cross-validation k-folds:
  test0, actual0, prediction0, ..., testk, actualk, predictionk,
  containing the indices of the test data,
  the actual result, and the predicted result 
  for each cross-validation run.

- txt file contains the number of estimators, 
  features used, feature importance,
  precision, and recall for each of the three runs. 
"""

output_prefix = 'Analysis/Data/RF_with_tutor'

import sys
sys.path.append('./Classes')
from readTutorData import readTutorData
sys.path.append('./Analysis')
from loadData import load_pickle
import processTools
import numpy as np
from sklearn import cross_validation, metrics, ensemble, svm
import pandas as pd
import matplotlib.pyplot as plt



# which columns to include as features
selected_features = ['available',
                     'available_now',
                     'client',
                     'sec_since_online',
                     'sec_since_pageload',
                     'time_sent_success_local',
                     #'hourly_response',
                     'weighted_hourly_response']

# time threshold for successful response (in seconds)                     
success_time = 30.

# number of k-folds for cross-validation
n_cv = 3

# weight of average tutor response rate vs. individual rate
# for weighted_hourly_response
# (irrelevant if that feature is not selected)
hr_weight = 10.0

# choose classifier and its settings
cl_settings = {'n_estimators': 20}
classifier = ensemble.RandomForestClassifier(**cl_settings)
    

print 'Loading ping data...'
df = load_pickle('Data/cleanPingDataFrame.pickle')

# replace Facebook client with Gtalk
df = processTools.change_facebook_client(df)

# drop rows before available_now was first used
df = processTools.drop_pings_before_available_now(df)

# drop rows with NaN entries in sec_since_online
df = df.dropna(subset=['sec_since_online'])

# compute labels for true classes (0/1 for slow/fast response)
labels = (df['sec_response'] < success_time).values

ping_ids = df['id'].values

# set up cross-validation
kfold = cross_validation.StratifiedKFold(labels, n_folds=n_cv)
# find minimum test data length
min_len_test = len(df)
for (train, test) in kfold:
    if len(test) < min_len_test:
        min_len_test = len(test)

# csv file for index, actual result, and prediction for each CV iteration
csv_filename = output_prefix + '.csv'
# txt file for selected features and other relevant info
txt_filename = output_prefix + '.txt'

txt_file = open(txt_filename, 'wb')
txt_file.write('Random forest with {0:d} estimators\n\nFeatures:\n'. \
               format(cl_settings['n_estimators']))
for feature in selected_features:
    txt_file.write(feature + '\n')
txt_file.write('\nThreshold for successful response: {0:f} s\n'.format(
                success_time))

# DataFrame for csv output
out_df = pd.DataFrame()

# loop over cross-validation k-folds
for i, (train, test) in enumerate(kfold):
    output = '\n\nk-fold {0:d}:\n---------\n'.format(i+1)
    print output
    txt_file.write(output)

    # standardize test data lengths
    test = test[:min_len_test]
    
    train_df = df.loc[df.index[train], :]
    test_df = df.loc[df.index[test], :]
    
    # add tutor hourly response data
    if 'hourly_response' in selected_features or \
        'weighted_hourly_response' in selected_features:
        # only read tutor data from the training data
        tutor_df = readTutorData(train_df, weight=hr_weight)
        # add hourly_response columns based on training data
        # to both training and test DataFrames
        train_df = processTools.add_ping_hourly_response(
            train_df, tutor_df)
        test_df = processTools.add_ping_hourly_response(
            test_df, tutor_df)
            
    train_features = train_df[selected_features].values
    test_features = test_df[selected_features].values
    
    # fit model to training data and compute predictions for test data
    model = classifier.fit(train_features, labels[train])
    prediction = classifier.predict(test_features)
    pred_prob = classifier.predict_proba(test_features)
    output = '\nPrecision: ' + \
        str(round(metrics.precision_score(labels[test], prediction), 4)) \
        + '\nRecall = ' + str(round(metrics.recall_score(
            labels[test], prediction), 4)) + \
        '\nFeature importances: ' + ' '.join(
            [str(fi) for fi in classifier.feature_importances_]) + '\n'
    print output
    txt_file.write(output)

    # write results to csv file
    headers = [s + str(i) for s in \
        ['ping_id', 'actual', 'prediction', 'predicted_probability']]
    for h, col in zip(headers,
            [ping_ids[test], labels[test], prediction, pred_prob[:,1]]):
        out_df[h] = col
    
out_df.to_csv(csv_filename, index=False)
txt_file.close()

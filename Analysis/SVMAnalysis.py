"""
Train SVM classifier based on whether tutor response is 
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

import sys
sys.path.append('./Classes')
from readTutorData import readTutorData
sys.path.append('./Analysis')
from loadData import load_pickle
import processTools
import numpy as np
from sklearn import cross_validation, metrics, \
    ensemble, svm
import pandas as pd
import matplotlib.pyplot as plt


# time threshold for successful response (in seconds)                     
success_time = 30.

# which columns to include as features
selected_features = {'available': {},
                     'available_now': {},
                     'client': {},
                     'sec_since_online': {'transform': \
                                          lambda x: np.log(1.+x)},
                     'sec_since_pageload': {'transform': \
                                            lambda x: np.log(1.+x)},
                     'time_sent_success_local': {'range': (0, 24)}}
                     #'hourly_response': {'range': (-1, 1)},
                     #'weighted_hourly_response': {'range': (0, 1)}}

# number of feature classes below which to split into binary features
max_classes = 10

# number of k-folds for cross-validation
n_cv = 3

# weight of average tutor response rate vs. individual rate
# for weighted_hourly_response
# (irrelevant if that feature is not selected)
hr_weight = 10.0

# choose classifier and its settings
cl_settings = {'C': 1.0, 'class_weight': {0:1, 1:2.5}, 'verbose': 1}
classifier = svm.LinearSVC(**cl_settings)
    

print 'Loading ping data...'
df=load_pickle('Data/cleanPingDataFrame.pickle')

# drop rows with NaN entries in sec_since_online
df = df.dropna(subset=['sec_since_online'])

# compute labels for true classes (0/1 for slow/fast response)
labels = (df['sec_response'] < success_time).values

# set up cross-validation
kfold = cross_validation.StratifiedKFold(labels, n_folds=n_cv)
# find minimum test data length
min_len_test = len(df)
for (train, test) in kfold:
    if len(test) < min_len_test:
        min_len_test = len(test)

# rescale features
# (move this to a function in processTools.py?)
print 'Rescaling features...'
new_features = []
dropped_features = []
for f in selected_features:
    # skip hourly_response features since they haven't been added yet
    # (also they don't really need to be rescaled)
    if f not in ['hourly_response', 'weighted_hourly_response']:
        feature_type = str(type(df[f].dropna()[0]))
        # map boolean values to -1/1
        if 'bool' in feature_type:
            df[f] = df[f].apply(lambda x: 1 if x else -1)
        else:
            # map classes to multiple binary features
            classes = set(df[f].dropna())
            if len(classes) < max_classes:
                if len(classes) <= 2:
                    df[f] = df[f].apply(lambda x: 1 if x == classes[0] \
                                                  else -1)
                else:
                    for c in classes:
                        s = pd.Series(np.where(df[f] == c, 1, -1), 
                                      index=df.index)
                        df[f + str(c)] = s
                        new_features.append(f + str(c))
                    df.drop(f, axis=1)
                    dropped_features.append(f)
            else:
                # transform variables
                if 'transform' in selected_features[f]:
                    df[f] = df[f].apply(selected_features[f]['transform'])
                # rescale to (-1, 1) using given range
                if 'range' in selected_features[f]:
                    f_min = selected_features[f]['range'][0]
                    f_ext = selected_features[f]['range'][1] - f_min
                    df[f] = df[f].apply(lambda x: 2.*(x-f_min)/f_ext - 1.)
                # if range not given, center on mean and scale to unit var.
                else:
                    mean, std = (df[f].mean(), df[f].std())
                    df[f] = df[f].apply(lambda x: (x - mean)/std)

for f in new_features:
    selected_features[f] = {}
for f in dropped_features:
    dropped = selected_features.pop(f)


output_prefix = 'Analysis/Data/LinearSVC'
# csv file for index, actual result, and prediction for each CV iteration
csv_filename = output_prefix + '.csv'
# txt file for selected features and other relevant info
txt_filename = output_prefix + '.txt'

txt_file = open(txt_filename, 'wb')
txt_file.write('SVC\n\nFeatures:\n')
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
    
    train_df = df.iloc[train]
    test_df = df.iloc[test]
    
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
            
    train_features = train_df[selected_features.keys()].values
    test_features = test_df[selected_features.keys()].values
    
    # fit model to training data and compute predictions for test data
    model = classifier.fit(train_features, labels[train])
    prediction = classifier.predict(test_features)
    pred_conf = classifier.decision_function(test_features)
    output = '\nPrecision: ' + \
        str(round(metrics.precision_score(labels[test], prediction), 4)) \
        + '\nRecall = ' + str(round(metrics.recall_score(
            labels[test], prediction), 4)) + '\n'
    print output
    txt_file.write(output)

    # write results to csv file
    headers = [s + str(i) for s in \
        ['test', 'actual', 'prediction', 'confidence_score']]
    for h, col in zip(headers,
            [test, labels[test], prediction, pred_conf]):
        out_df[h] = col
    
out_df.to_csv(csv_filename, index=False)
txt_file.close()

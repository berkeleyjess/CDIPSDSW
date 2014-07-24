# Chooses the functions from processTools.py it would like to use
# Applies the RandomForest algorithm and stores the output.
#   For now, all analysis scripts should output a csv with columns 'ping_id', 'data', 'model'

import sys
sys.path.append('./Analysis')
from loadData import load_pickle
import numpy as np

pingtutor_fname='Data/cleanPingTutorDataFrame.pickle'
df=load_pickle(pingtutor_fname)

#  Define your successful response time and create a boolean column of successful responses
success_time=30
df['success']=df['sec_response']<success_time

# which columns to include as features
selected_features = ['available','available_now',
                    'client','sec_since_online',
                    'time_sent_success_local',
                    'sec_since_pageload',
                    'success']
                         
rf_df=df[selected_features]

from processTools import drop_nan_row
rf_df=drop_nan_row(rf_df)

'''
# choose classifier and its settings
    cl_settings = {'n_estimators': 10}
    classifier = ensemble.RandomForestClassifier(**cl_settings)
    
    # number of k-folds for cross-validation
    n_cv = 3
     
    # select features from the data
    features = data[selected_features].values
    print '\nfeatures:', selected_features
    
    # define the true answers for the training set
    labels = data.sec_response.apply(
        fast_response, args=(max_time_sec,)).values

    # set up cross-validation
    kfold = cross_validation.StratifiedKFold(
        labels, n_folds=n_cv, shuffle=True)
    
    # fit the classifier and compute metrics on the test sample
    for i, (train, test) in enumerate(kfold):
        print '\nk-fold {0:d}:'.format(i+1)
        classifier.fit(features[train], labels[train])
        print 'feature importances:', \
            classifier.feature_importances_
        prediction = classifier.predict(features[test])
        print 'precision:', \
            metrics.precision_score(labels[test], prediction)
        print 'recall:', \
            metrics.recall_score(labels[test], prediction)
            '''
"""
Fit a classifier to a training subset of the ping data and 
predict whether pings in a test subset will get a response
within a certain amount of time.
"""

from pandas import isnull

def fast_response(response_time, max_time):
    """
    For a given response time, return 1 if < max_time (a fast response)
    and 0 otherwise (including NaN values).
    """
    return 0 if (isnull(response_time) or 
                 response_time > max_time) else 1
    

if __name__ == '__main__':
    from pandas.io.pytables import HDFStore
    # scikit-learn version 0.15.0
    from sklearn import cross_validation, metrics, ensemble

    # load DataFrame saved by clean_ping_data.py
    store = HDFStore('../Data/ping_data_cleaned.h5')
    data = store['data']
    store.close()

    # threshold time for successful response
    max_time_sec = 30.
    # choose classifier and its settings
    cl_settings = {'n_estimators': 10}
    classifier = ensemble.RandomForestClassifier(**cl_settings)
    # which columns to include as features
    selected_features = ['availability',
                         'client',
                         'time_sent_success_local',
                         'sec_since_online',
                         'sec_since_pageload',
                         'timezone']
    # number of k-folds for cross-validation
    n_cv = 3
                         
    # remove rows with null values
    # - e.g., for < 1% of tutors, the time when they last
    #   appeared online is unknown so sec_since_online
    #   has null values
    data = data.dropna(subset=selected_features)
    
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

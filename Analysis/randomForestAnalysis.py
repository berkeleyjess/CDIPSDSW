# Chooses the functions from processTools.py it would like to use
# Applies the RandomForest algorithm and stores the output.
#   For now, all analysis scripts should output a csv with columns 'ping_id', 'data', 'model'
#
#  The script outputs a .csv file with nine columns test0,actual0,prediction0,
#  test1,actual1,prediction1,test2,actual2,prediction2.
#  The columns contain the index of the actual data in the cleanPingTutorDataFrame.pickle,
#  the actual result, and the predicted result for the three cross-validation runs (0,1,2)
#
#  The .txt file contains the number of estimators, features used, and feature importance,
#  precision, and recall for each of the three runs. 


import sys
sys.path.append('./Analysis')
from loadData import load_pickle
import processTools
import numpy as np
from sklearn import cross_validation, metrics, ensemble
import pandas as pd
import matplotlib.pyplot as plt


#User Defined Output File, Change before running file
outfname = 'run10'

#Load the Ping and Tutor Data Frame
print 'Loading ping/tutor DataFrame...'
pingtutor_fname='Data/cleanPingTutorDataFrame.pickle'
df=load_pickle(pingtutor_fname)

#Calculate a couple extra values from the Tutor Data
df['n_clicks_under_30_pct']=df['n_clicks_under_30']/df['n_pings']
df['n_clicks_pct']=df['n_clicks']/df['n_pings']

#  Define your successful response time and create a boolean column of successful responses
success_time=30
df['success']=df['sec_response']<success_time

# which columns to include as features
# (plus 'success' for true answers for the training set)
selected_features = [#'available',
                     #'available_now',
                     #'client',
                     'sec_since_online',
                     'sec_since_pageload',
                     'time_sent_success_local',
                     #'hourly_avg_sec_response',
                     'hourly_response',
                     #'weighted_hourly_response',
                     #'hourly_response_n_clicked',
                     #'hourly_response_n_not_clicked',
                     #'n_clicks_under_30_pct',
                     #'n_clicks_pct',
                     'success']    

# add weighted_hourly_response column
if 'weighted_hourly_response' in selected_features:
    weight = 10.0
    tutor_df = load_pickle('Data/tutorDataFrame.pickle').transpose()
    tutor_df = processTools.add_weighted_hourly_response(
        tutor_df, weight)
    whr = tutor_df.weighted_hourly_response[df.tutor_id]
    df['weighted_hourly_response'] = pd.Series(np.choose(
        np.floor(df.time_sent_success_local).astype(int).values,
        np.transpose(np.array(list(whr.values)))),
        index=df.index)
    
#rf_data is the data that will go into Random Forest
rf_data=df[selected_features]

#Drop the NaN's
from processTools import drop_nan_row
rf_data=drop_nan_row(rf_data)

# choose classifier and its settings
nest=9
cl_settings = {'n_estimators': nest}
classifier = ensemble.RandomForestClassifier(**cl_settings)
    
# number of k-folds for cross-validation
n_cv = 3
     
# select features from the data
# define the true answers for the training set
labels = rf_data['success'].values

#Drop success (the answer) from the features data
rf_data.drop(['success'],axis=1,inplace=True)
features = rf_data.values
print '\nfeatures:', selected_features
    
# set up cross-validation
kfold = cross_validation.StratifiedKFold(labels,n_folds=n_cv)
# find minimum test length
min_len_test = len(rf_data)
for (train, test) in kfold:
    if len(test) < min_len_test:
        min_len_test = len(test)

#Define the Name of the output file names
#The .txt file will hold info on which features are most important
#The .csv file will hold the predicted, actual, and index of actual results
output_filestr='Analysis/Data/pingTutorData_nest_equal_' + \
    str(nest)
csvfilename=output_filestr + '.csv'
txtfilename=output_filestr + '.txt'

#Open the .txt file
tfid=open(txtfilename,'wb')
tfid.write('Random Forests, n_estimators = ' + str(nest) + '\n')
for item in selected_features:
	tfid.write(item + '\t')

outdf=pd.DataFrame()	
# fit the classifier and compute metrics on the test sample
for i, (train, test) in enumerate(kfold):
	print('\nk-fold {0:d}:'.format(i+1))
	output=classifier.fit(features[train], labels[train])
	print ('feature importances:', \
	classifier.feature_importances_)
	#Write Variables to Text File
	tfid.write('\n')
	for item in classifier.feature_importances_:
		tfid.write(str(round(item,4)) + '\t')
	prediction = classifier.predict(features[test])
	predic_prob= classifier.predict_proba(features[test])
	print 'precision:', \
	metrics.precision_score(labels[test], prediction)
	tfid.write('\n' + 'Precision = ' + str(round(metrics.precision_score(labels[test], prediction),4)))
	print 'recall:', \
	metrics.recall_score(labels[test], prediction)
	tfid.write('\n' + 'Recall = ' + str(round(metrics.recall_score(labels[test], prediction),4)) + '\n')
	h1='test' + str(i)
	h2='actual' + str(i)
	h3='prediction' + str(i)
	h4='predic_prob1' + str(i)
	h5='predic_prob2' + str(i)
	outdf[h1]=test
	outdf[h2]=labels[test]
	outdf[h3]=prediction
	outdf[h4]=predic_prob[:,0]
	outdf[h5]=predic_prob[:,1]
	#=pd.DataFrame({h1:test,h2:labels[test],h3:prediction})
	
outdf.to_csv(csvfilename,index=False)
tfid.close()


		
		
	
		
	
	
=======

>>>>>>> 2c21a13c92c4120a13b0902f0627efe34e97b660




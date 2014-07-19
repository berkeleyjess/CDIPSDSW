#jeff_randomforest.py
#	Loads up data processed by jeff_loadclean_dat.py and rund RandomForest on it.
from __future__ import division
import pandas as pd

train_df=pd.read_pickle('jd_trainingdata_df.pkl')
test_df=pd.read_pickle('jd_testingdata_df.pkl')

# Convert DataFrames to numpy matricies
test_dat=pd.DataFrame.as_matrix(test_df)
train_dat=pd.DataFrame.as_matrix(train_df)

from sklearn.ensemble import RandomForestClassifier	


print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_dat[0::,0:6], train_dat[:,7] )



print 'Predicting...'
output = forest.predict(test_dat[0::,0:6])


#Compare output and test_dat[0::,7]
num_records=output.size

corr=test_dat[:,7]-output
overall_pctcorr=(sum(corr==0)/num_records)*100

#Look at the number of times the model predicted a tutor would respond, and did
tutors_show=test_dat[:,7]==1  # A logical Array to map to the output
tutor_pctcorr=sum(output[tutors_show])/sum(tutors_show)*100

#look at the number of times the model predicted a tutor would respond, but didn't
predict_tutor_show=output==1

tutor_pctincorr=(sum(predict_tutor_show)-sum(test_dat[:,7][predict_tutor_show]))/sum(predict_tutor_show)*100

print ''
print 'Percentage of Predictions that were Correct = ', overall_pctcorr
print 'Percentage of Time Correctly Prediting When Tutors Would Respond within One Minute  = ', tutor_pctcorr
print 'Percentage of Time Incorrectly Prediting When Tutors Would Respond within One Minute  = ', tutor_pctincorr

import pandas as pd
import numpy as np
import cPickle

# Data cleanup
# TRAIN DATA
read_in_file = 'Classes/berkeley_read_in_data.py'
execfile(read_in_file)

# Divide pings into train and test
length = len(pings)
train_set = pings[0:length/2]
test_set = pings[length/2:length]

# Get list of Ping attributes
bad_attributes = dir(Ping)
attributes = dir(pings[0])
for ba in bad_attributes: attributes.remove(ba)
print "Attributes to be stored:", attributes

# Put training Ping objects into a dataframe
df_dict = {}
for a in attributes:
    i = 0
    series_dict = {}
    for ping in train_set:
        series_dict[i] = eval('ping.'+a)
        i+=1
    s = pd.Series(series_dict)
    df_dict[a] = s
train_df = pd.DataFrame(df_dict)

print "Created training set."
print train_df['available'][0]

# Put testing Ping objects into a dataframe
df_dict = {}
for a in attributes:
    i = 0
    series_dict = {}
    for ping in test_set:
        series_dict[i] = eval('ping.'+a)
        i+=1
    s = pd.Series(series_dict)
    df_dict[a] = s
test_df = pd.DataFrame(df_dict)

print "Created test set."

with open(r"Data/trainDataFrame.pickle", "wb") as output_file:
    cPickle.dump(train_df, output_file)
with open(r"Data/testDataFrame.pickle", "wb") as output_file:
    cPickle.dump(test_df, output_file)


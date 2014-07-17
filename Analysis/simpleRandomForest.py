import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

# Data cleanup
# TRAIN DATA
read_in_file = 'Classes/berkeley_read_in_data.py'
execfile(read_in_file)

# Divide pings into train and test
length = len(pings)
train_set = pings[0:length/2]
test_set = pings[length/2+1:length]

# Get list of Ping attributes
bad_attributes = dir(Ping)
bad_attributes += ['id']
attributes = dir(pings[0])
for ba in bad_attributes: attributes.remove(ba)
print attributes

# Put training Ping objects into a dataframe
df_dict = {}

for ping in train_set:
    series_dict = {}
    for a in attributes:
        series_dict[a] = eval('ping.'+a)
    s = pd.Series(series_dict, attributes)
    df_dict[ping.id] = s

train_df = pd.DataFrame(df_dict)

print train_df['available'][0]



'''

input_attributes = {}

input_attributes['available'] = []
for ping in pings:
    input_attributes['available'] += ping.available

print input_attributes






train_npy = np.load('Data/train.csv')
train_df =
train_df = pd.read_csv('Data/train.csv', header=0)        # Load the train file into a dataframe

# I need to convert all strings to integer classifiers.
# I need to fill in the missing values of the data and make it complete.

# female = 0, Male = 1
train_df['Gender'] = train_df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

# Embarked from 'C', 'Q', 'S'
# Note this is not ideal: in translating categories to numbers, Port "2" is not 2 times greater than Port "1", etc.

# All missing Embarked -> just make them embark from most common place
if len(train_df.Embarked[ train_df.Embarked.isnull() ]) > 0:
    train_df.Embarked[ train_df.Embarked.isnull() ] = train_df.Embarked.dropna().mode().values

Ports = list(enumerate(np.unique(train_df['Embarked'])))    # determine all values of Embarked,
Ports_dict = { name : i for i, name in Ports }              # set up a dictionary in the form  Ports : index
train_df.Embarked = train_df.Embarked.map( lambda x: Ports_dict[x]).astype(int)     # Convert all Embark strings to int

# All the ages with no data -> make the median of all Ages
median_age = train_df['Age'].dropna().median()
if len(train_df.Age[ train_df.Age.isnull() ]) > 0:
    train_df.loc[ (train_df.Age.isnull()), 'Age'] = median_age

# Add a value for whether or not has spouse on titanic
# Unmarried = 0, Married but spouse not on ship = 1, Married spouse on ship = 2, Unknown = 3

mrs= train_df['Name'].map(lambda x: x.find('Mrs')!=-1)
miss= train_df['Name'].map(lambda x: x.find('Miss')!=-1)
master= train_df['Name'].map(lambda x: x.find('Master')!=-1)

# Married: 1, Unmarried: 2, Unknown: 0
train_df['Married'] = master.map({True:2, False:0}).astype(int)
train_df['Married'] += miss.map({True:2, False:0}).astype(int)
train_df['Married'] += mrs.map({True:1, False:0}).astype(int)

train_df['SpouseAboard'] = master.map({True:False, False:False})

for name in train_df['Name']:
    if name.find('Mrs.')!=-1:
        last = name.split(', Mrs. ')[0]
        first = name.split(', Mrs. ')[1].split(' (')[0]
        if last+', Mr. '+first in train_df['Name']:
            train_df['SpouseAboard'][index(train_df['Name'], last+', Mr. '+first)] = True
            train_df['SpouseAboard'][index(train_df['Name'], last+', Mrs. '+first)] = True

# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
train_df = train_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1)


# TEST DATA
test_df = pd.read_csv('Data/test.csv', header=0)        # Load the test file into a dataframe

# I need to do the same with the test data now, so that the columns are the same as the training data
# I need to convert all strings to integer classifiers:
# female = 0, Male = 1
test_df['Gender'] = test_df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

# Embarked from 'C', 'Q', 'S'
# All missing Embarked -> just make them embark from most common place
if len(test_df.Embarked[ test_df.Embarked.isnull() ]) > 0:
    test_df.Embarked[ test_df.Embarked.isnull() ] = test_df.Embarked.dropna().mode().values
# Again convert all Embarked strings to int
test_df.Embarked = test_df.Embarked.map( lambda x: Ports_dict[x]).astype(int)


# All the ages with no data -> make the median of all Ages
median_age = test_df['Age'].dropna().median()
if len(test_df.Age[ test_df.Age.isnull() ]) > 0:
    test_df.loc[ (test_df.Age.isnull()), 'Age'] = median_age

# All the missing Fares -> assume median of their respective class
if len(test_df.Fare[ test_df.Fare.isnull() ]) > 0:
    median_fare = np.zeros(3)
    for f in range(0,3):                                              # loop 0 to 2
        median_fare[f] = test_df[ test_df.Pclass == f+1 ]['Fare'].dropna().median()
    for f in range(0,3):                                              # loop 0 to 2
        test_df.loc[ (test_df.Fare.isnull()) & (test_df.Pclass == f+1 ), 'Fare'] = median_fare[f]

# Collect the test data's PassengerIds before dropping it
ids = test_df['PassengerId'].values

# Add a value for whether or not has spouse on titanic
# Unmarried = 0, Married but spouse not on ship = 1, Married spouse on ship = 2, Unknown = 3

mrs= test_df['Name'].map(lambda x: x.find('Mrs')!=-1)
miss= test_df['Name'].map(lambda x: x.find('Miss')!=-1)
master= test_df['Name'].map(lambda x: x.find('Master')!=-1)

# Married: 1, Unmarried: 2, Unknown: 0
test_df['Married'] = master.map({True:2, False:0}).astype(int)
test_df['Married'] += miss.map({True:2, False:0}).astype(int)
test_df['Married'] += mrs.map({True:1, False:0}).astype(int)

test_df['SpouseAboard'] = master.map({True:False, False:False})

for name in test_df['Name']:
    if name.find('Mrs.')!=-1:
        last = name.split(', Mrs. ')[0]
        first = name.split(', Mrs. ')[1].split(' (')[0]
        if last+', Mr. '+first in test_df['Name']:
            test_df['SpouseAboard'][index(test_df['Name'], last+', Mr. '+first)] = True
            test_df['SpouseAboard'][index(test_df['Name'], last+', Mrs. '+first)] = True

# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
test_df = test_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1)


# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_df.values
test_data = test_df.values


print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,0] )

print 'Predicting...'
output = forest.predict(test_data).astype(int)


predictions_file = open("myfirstforest.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'

'''

# Create dataframe indexed by subject with features:
#   List of tutors for subject
#   List of lessons for subject
#   Number of pings for subject

import pandas as pd
import numpy as np
import cPickle
from pytz import timezone

# Import data file
print "Loading in ping data..."
with open(r"Data/cleanPingDataFrame.pickle", "rb") as input_file:
    pings_df = cPickle.load(input_file)
total_pings = len(pings_df['tutor_id'])

# Get list of all unique subjects
subjects=pings_df['lesson_subject'].unique()

# Produce dataframe indexed by tutor_id with attributes above
print "Getting subject info..."
df_dict = {}
series_dicts = {}
for sub in subjects:
    series_dicts[sub] = {}

for x in xrange(total_pings):
    if x%10000==0: print "Pings evaluated:", x, "/", total_pings

    entry = pings_df.iloc[x, :]
    sub = entry['lesson_subject']

    # Add number of pings variable, and if first instance, initialize all other variables
    if 'n_pings' in series_dicts[sub]: series_dicts[sub]['n_pings']+=1
    else:
        series_dicts[sub]['n_pings']=1
        series_dicts[sub]['lesson_ids']=[]
        series_dicts[sub]['tutor_ids']=[]

    series_dicts[sub]['lesson_ids'].append(entry['lesson_id'])
    series_dicts[sub]['tutor_ids'].append(entry['tutor_id'])

print "Building subject dataframe..."

for sub in series_dicts.keys():
    # Keep only unique entries
    series_dicts[sub]['lesson_ids'] = list(set(series_dicts[sub]['lesson_ids']))
    series_dicts[sub]['tutor_ids'] = list(set(series_dicts[sub]['tutor_ids']))

    # Form series to go into dataframe
    s = pd.Series(series_dicts[sub])
    df_dict[sub] = s

# Make final dataframe
subject_df = pd.DataFrame(df_dict)

print "Saving tutor dataframe..."
with open(r"Data/subjectDataFrame.pickle", "wb") as output_file:
    cPickle.dump(subject_df, output_file)



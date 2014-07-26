"""
Count the number of unique tutor IDs in each data set and 
the number shared between each pair of data sets.
"""

import pandas as pd
import sys
import os.path

def tutor_id_set(csv_file):
    tutor_id_series = pd.read_csv(csv_file, skipinitialspace=True, usecols=['tutor_id'])
    return set(tutor_id_series['tutor_id'])

for f in ['Data/berkeley_tutor_data.csv',
          'Data/berkeley_ping_data.csv',
          'Data/berkeley_message_data.csv',
          'Data/berkeley_old_message_data.csv']:
    if not os.path.isfile(f):
        sys.exit('Missing CSV file: ' + f)
    
all_tutors = tutor_id_set('Data/berkeley_tutor_data.csv')
ping_tutors = tutor_id_set('Data/berkeley_ping_data.csv')
message_tutors = tutor_id_set('Data/berkeley_message_data.csv')
old_message_tutors = tutor_id_set('Data/berkeley_old_message_data.csv')

print
print 'Number of unique tutor IDs in each data set or data set pair'
print '------------------------------------------------------------'

tutor_ids = [all_tutors, ping_tutors, old_message_tutors, message_tutors]
labels = ['tutor', 'ping', 'old_message', 'message']
for i in range(4):
    print labels[i] + ': ' + str(len(tutor_ids[i]))
    for j in range(i+1,4):
        print '    intersection(' + labels[i] + ', ' + \
            labels[j] + '): ' + \
            str(len(tutor_ids[i] & tutor_ids[j]))

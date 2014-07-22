"""
Add new columns to the ping DataFrame:
  
- Time differences in seconds:
  'sec_response', 'sec_since_online', and 'sec_since_pageload'.
  
- Local time of day in hours past midnight:
  'time_sent_success_local' and 'time_clicked_local'.

- Two new time zone columns, 'timezone_str' which 
  gives the time zone location as a string, and 'hours_from_utc'
  which gives the time zone offset from UTC in hours.
"""

import numpy as np
import pandas as pd
import cPickle
import pytz
import datetime
import sys
sys.path.append('.')
import time_zones

def local_time(column):
    """
    Return a function that operates on a DataFrame row,
    converting the datetime object in the specified column 
    to the time zone corresponding to the index in 
    the 'timezone' column (from pytz.common_timezones) and
    computing the local time of day (in hours).
    """
    def return_function(row):
        utc_datetime = row[column]
        if pd.isnull(utc_datetime):
            return np.nan
        else:
            tz = pytz.timezone(
                time_zones.COMMON_TIMEZONES_STR[row['timezone']])
            local_datetime = utc_datetime.astimezone(tz)
            return local_datetime.hour + \
                local_datetime.minute/60. + \
                local_datetime.second/3600.
    return return_function
    
def hours_from_utc(row):
    """
    Given a DataFrame row containing a time zone string and 
    a date (here, the date of the ping is used), return the
    offset from UTC for that time zone in hours.
    """
    timezone = row['timezone_str']
    dt = row['time_sent_success']
    try:
        hours = pytz.timezone(timezone).utcoffset(
            datetime.datetime(dt.year, dt.month, dt.day)). \
            total_seconds()/3600.
    except pytz.exceptions.NonExistentTimeError:
        hours = pytz.timezone(timezone).utcoffset(
            datetime.datetime(dt.year, dt.month, dt.day), 
            is_dst=True).total_seconds()/3600.
    return hours
    

print 'Reading raw data...'
with open(r"Data/pingDataFrame.pickle", "rb") as input_file:
    data = cPickle.load(input_file)

# add columns for time differences (in seconds)
print 'Adding time difference columns...'
delta = data.time_clicked - data.time_sent_success
data['sec_response'] = delta.astype('timedelta64[s]')
delta = data.time_sent_success - data.last_seen_online_time
data['sec_since_online'] = delta.astype('timedelta64[s]')
delta = data.time_sent_success - data.last_impression_time
data['sec_since_pageload'] = delta.astype('timedelta64[s]')

# add columns for the local time_sent_success and time_clicked
print 'Adding local time columns...'
data['time_sent_success_local'] = \
    data.apply(local_time('time_sent_success'), axis=1)
data['time_clicked_local'] = \
    data.apply(local_time('time_clicked'), axis=1)
    
# add more time zone columns
print 'Adding time zone columns...'
data['timezone_str'] = data.timezone.apply(
    lambda tz: time_zones.COMMON_TIMEZONES_STR[tz])
data['hours_from_utc'] = data.apply(hours_from_utc, axis=1)

# save new DataFrame to pickle file
with open(r"Data/cleanPingDataFrame.pickle", "wb") as output_file:
    cPickle.dump(data, output_file)

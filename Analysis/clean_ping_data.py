"""
Read ping data from the CSV file into a pandas DataFrame,
clean the data and add new columns, and save the resulting
DataFrame in HDF5 format.

The main changes to the columns are:

- Each pair of date and time columns is combined into a single
  column as a pandas Timestamp (UTC).

- The 'available' and 'available_now' columns are replaced by 
  a single integer-valued 'availability' column.
  
- Three new columns give time differences in seconds:
  'sec_response', 'sec_since_online', and 'sec_since_pageload'.
  
- Two new columns give the local time of day in hours past midnight:
  'time_sent_success_local' and 'time_clicked_local'.

If you get an error when reading to the end of the ping data,
try deleting the last row of the CSV file (which is incomplete 
and seems to cause problems for the read_csv function).
"""

import numpy as np
import pandas as pd
import sys
sys.path.append('../.')
import time_zones

def parse_date_and_time(date_or_time, time_or_date):
    """
    Convert date and time strings (can be given in either order)
    into a datetime object. Time zone is assumed to be UTC.
    If either value is missing, returns NaN.
    """
    datetime_column = []
    for dt, td in zip(date_or_time, time_or_date):
        if dt == 'None' or td == 'None':
            datetime_column.append(np.nan)
        else:
            datetime_column.append(
                pd.to_datetime(' '.join([dt, td]), utc=True))
    return datetime_column

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
            tz = time_zones.COMMON_TIMEZONES_STR[row['timezone']]
            local_datetime = utc_datetime.tz_convert(tz). \
                to_pydatetime()
            return local_datetime.hour + \
                local_datetime.minute/60. + \
                local_datetime.second/3600.
    return return_function

    
if __name__ == '__main__':
    import argparse
    
    # optional arguments (mainly for testing purposes)
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n_pings', type=int, default=None,
                        help='number of rows to read')
    parser.add_argument('-fp', '--first_ping', type=int, default=1,
                        help='first ping to read (starting from 1)')
    args = parser.parse_args()

    csv_file = '../Data/berkeley_ping_data.csv'
    
    # date/time pairs
    # order is unimportant, so misordering of date_clicked and 
    # time_clicked columns doesn't matter
    date_time_columns = {'datetime_last_impression' : [7, 8],
                         'datetime_last_seen_online' : [9, 10],
                         'datetime_clicked' : [12, 13],
                         'datetime_sent_success' : [14, 15]}

    data = pd.read_csv(
        csv_file, 
        skipinitialspace=True, # remove extra spaces in column names
        skiprows=range(1, args.first_ping),
        nrows=args.n_pings,
        parse_dates=date_time_columns, # combine dates and times
        date_parser=parse_date_and_time,
        true_values=['True'],
        false_values=['False'])

    # replace available and available_now with single integer
    #     0: not available
    #     1: available (and not available now)
    #     2: available now
    data['availability'] = data.available.astype(int) + \
        data.available_now.astype(int)
    data = data.drop(['available', 'available_now'], axis=1)
        
    # add columns for time differences (in seconds)
    delta = data.datetime_clicked - data.datetime_sent_success
    data['sec_response'] = delta.astype('timedelta64[s]')
    delta = data.datetime_sent_success - \
        data.datetime_last_seen_online
    data['sec_since_online'] = delta.astype('timedelta64[s]')
    delta = data.datetime_sent_success - \
        data.datetime_last_impression
    data['sec_since_pageload'] = delta.astype('timedelta64[s]')
    
    # add columns for the local time_sent_success and time_clicked
    data['time_sent_success_local'] = \
        data.apply(local_time('datetime_sent_success'), axis=1)
    data['time_clicked_local'] = \
        data.apply(local_time('datetime_clicked'), axis=1)

    # save the new DataFrame using HDF5
    store = pd.io.pytables.HDFStore('../Data/ping_data_cleaned.h5')
    store['data'] = data
    store.close()

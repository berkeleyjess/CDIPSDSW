# Here we add functions that can be applied to the dataframe that comes from cleanData.py. Make sure that each function doesn't expect additional features to already exist

# INFO ON NEW FEATURES:
# FEATURE NAME                  FUNCTION THAT ADDS IT           DESCRIPTION

import numpy as np
import pandas as pd

def nan_to_zeros(df):
    """
    Given a DataFrame, all NaN's are replaced with zeros.
    """
    
    header_list=data.columns.values.tolist()
    j = lambda x: 0 if np.isnan(x) or np.isinf(x) else x
    #df=df.map
    return df
    
def drop_nan_row(df):
    """
    Given a DataFrame, all rows containing NaN's are 
    removed from the DataFrame.
    """
    print df.shape
    orig_rws=df.shape[0]
    df=df.dropna(axis=0)
    remain_rws=df.shape[0]
    print "Removed ", orig_rws-remain_rws ," rows of data."
    return df

def add_ping_availability_int(ping_df):
    """
    Sum boolean 'available' and 'available_now' columns
    of ping DataFrame to get integer 'availability' column.
    """
    ping_df['availability'] = ping_df.available.astype(int) + \
                              ping_df.available_now.astype(int)
    return ping_df

def change_facebook_client(ping_df, method='gtalk'):
    """
    Change or drop pings with client==2 (Facebook).
    """
    if method == 'gtalk':
        # replace all Facebook entries with Gtalk
        ping_df['client'] = ping_df.client.apply(
            lambda x: 1 if x == 2 else x)
    elif method == 'drop':
        # drop all rows with Facebook
        ping_df = ping_df[ping_df.client != 2]
    return ping_df

def drop_pings_before_available_now(ping_df):
    """
    Drop all pings before the first instance of available_now==True.
    """
    first_now = ping_df[ping_df.available_now].index[0]
    return ping_df.ix[first_now:]

def add_weighted_hourly_response(tutor_df, weight=10.0):
    """
    Add a column to the tutor DataFrame that combines the
    hourly response for each individual tutor with the 
    overall hourly response for all tutors.
    
    - If the number of pings for a tutor in an hour is zero, 
      this is equal to the overall hourly response.
      
    - If the number of pings for a tutor in an hour is 
      much larger than the specified weight, then this is
      approximately equal to the hourly response for that
      individual tutor.
    """
    tutor_df = tutor_df.transpose()
    
    # total pings per local hour for each tutor
    tutor_df['hourly_n_pings'] = \
        tutor_df['hourly_response_n_clicked'].apply(
            lambda x: np.array(x)) + \
        tutor_df['hourly_response_n_not_clicked'].apply(
            lambda x: np.array(x))

    # hourly response for all tutors
    total_hourly_response = \
        tutor_df['hourly_response_n_clicked'].apply(
            lambda x: np.array(x)).sum() / \
        tutor_df['hourly_n_pings'].sum().astype(float)
    tutor_df['total_hourly_response'] = pd.Series(
        len(tutor_df)*[total_hourly_response])
        
    # weighted hourly response
    tutor_df['weighted_hourly_response'] = \
        (pd.Series(len(tutor_df)*[weight*total_hourly_response],
                   index=tutor_df.index) + \
            tutor_df['hourly_response_n_clicked'].apply(
                lambda x: np.array(x))) / \
        (pd.Series(len(tutor_df)*[weight], index=tutor_df.index) + \
            tutor_df['hourly_n_pings'])
        
    return tutor_df.transpose()
    
def add_ping_hourly_response(ping_df, tutor_df):
    """
    Given a ping DataFrame and tutor DataFrame, add hourly_response
    and weighted_hourly_response columns to the ping data that 
    take a single value from the corresponding length-24 arrays
    in the tutor data, selected based on the local time at which
    the ping was sent.

    For tutors in the ping DataFrame not found in the tutor DataFrame,
    the hourly_response is set to -1 and the weighted_hourly_response
    is set to the average (from total_hourly_response).
    """
    tutor_ids = ping_df.tutor_id
    # change tutor IDs not found in the tutor DataFrame to 0
    tutor_ids = np.where(np.in1d(tutor_ids, tutor_df.columns), 
                         tutor_ids, 0)

    # add a column to the tutor DataFrame with tutor_id = 0
    #  where hourly_response is an array with all values -1
    #  and weighted_hourly_response is total_hourly_response
    tutor_df[0] = pd.Series(index=tutor_df.index)
    # placeholder values to be replaced using fill_hr_cols
    tutor_df[0].ix['hourly_response'] = 0
    tutor_df[0].ix['weighted_hourly_response'] = 1
    # total_hourly_response is the same for all columns,
    #  so just take it from the first column
    thr = tutor_df[tutor_df.columns[0]].ix['total_hourly_response']

    def fill_hr_cols(x, thr):
        if x == 0:
            return np.zeros(24) - 1
        elif x == 1:
            return thr
        else:
            return np.nan

    tutor_df[0] = tutor_df[0].apply(lambda x: fill_hr_cols(x, thr))

    for label in ['hourly_response', 'weighted_hourly_response']:
        hr = tutor_df.ix[label][tutor_ids]
        ping_df[label] = pd.Series(np.choose(
            np.floor(ping_df.time_sent_success_local).astype(int).values,
            np.transpose(np.array(list(hr.values)))),
            index=ping_df.index)
    return ping_df

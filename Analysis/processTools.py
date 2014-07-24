# Here we add functions that can be applied to the dataframe that comes from cleanData.py. Make sure that each function doesn't expect additional features to already exist

# INFO ON NEW FEATURES:
# FEATURE NAME                  FUNCTION THAT ADDS IT           DESCRIPTION



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

def add_ping_availability_int(df):
    """
    Sum boolean 'available' and 'available_now' columns
    of ping DataFrame to get integer 'availability' column.
    """
    df['availability'] = df.available.astype(int) + \
                         df.available_now.astype(int)
    return df

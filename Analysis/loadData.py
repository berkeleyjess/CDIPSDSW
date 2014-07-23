"""
Functions for loading data from different storage formats.
"""

def load_pickle(file_name):
    """
    Load data stored by pickle.
    """
    import cPickle
    with open(file_name, 'rb') as input_file:
        s = input_file.read()
        return cPickle.loads(s)
        # this seems to be much slower:
        #return cPickle.load(input_file)

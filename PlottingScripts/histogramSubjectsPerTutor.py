"""
Histograms of the number of pings sent and clicked
vs. the tutor's local time.
"""

import pandas as pd
required_data = ['Data/tutorDataFrame.pickle']

def plot(tutor_data):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)

    n_subjects = {}
    for tid in tutor_data:
        n_subjects[tid] = len(tutor_data[tid].subjects)
    n_subjects_series = pd.Series(n_subjects)

    n_subjects_series.hist(bins=range(100), ax=ax, color='r')

    ax.set_xlim(0, 100)
    #ax.set_xticks(range(0, 27, 3))

    ax.set_xlabel('Number of Subjects per Tutor')
    ax.set_ylabel('Number of Tutors')

    return fig

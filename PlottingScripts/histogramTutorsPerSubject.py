"""
Histograms of the number of pings sent and clicked
vs. the tutor's local time.
"""

import pandas as pd
required_data = ['Data/subjectDataFrame.pickle']

def plot(subject_data):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)

    n_tutors = {}
    for subj in subject_data:
        n_tutors[subj] = len(subject_data[subj].tutor_ids)
    n_tutors_series = pd.Series(n_tutors)
    binwidth = 10
    n_tutors_series.hist(bins=range(0, 500+binwidth, binwidth), ax=ax, color='r')

    ax.set_xlim(0, 500)
    #ax.set_xticks(range(0, 27, 3))

    ax.set_xlabel('Number of Tutors per Subject')
    ax.set_ylabel('Number of Subjects')

    return fig

"""
Histograms of the number of pings sent and clicked 
vs. the tutor's local time.
"""

required_data = ['Data/cleanPingDataFrame.pickle']

def plot(ping_data):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    hours = range(25) # bin edges, so we need 0 through 24
    ping_data.time_sent_success_local.hist(bins=hours, ax=ax, color='r')
    ping_data.time_clicked_local.hist(bins=hours, ax=ax, color='b')
    
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 27, 3))
    
    ax.set_xlabel('Local time (hours since midnight)')
    ax.set_ylabel('Number of pings')
    
    ax.text(1.5, 21500, 'Time sent', color='r')
    ax.text(1.5, 19500, 'Time clicked', color='b')
    
    return fig
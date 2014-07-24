"""
Scatter plots of ping response time vs. various features 
with median response times in bins.
"""

import numpy as np

required_data = ['Data/cleanPingDataFrame.pickle']

def scatter_with_binned_median(ax, x, y, x_bins, 
                               scale='linear', join=False):
    x_bin_centers = []
    medians = []
    for i in range(len(x_bins)-1):
        if scale == 'linear':
            x_bin_centers.append(0.5*(x_bins[i]+x_bins[i+1]))
        elif scale == 'log':
            x_bin_centers.append(
                np.exp(0.5*np.log(x_bins[i]*x_bins[i+1])))
        medians.append(y[(x_bins[i] < x) & 
                         (x < x_bins[i+1])].median())
    ax.plot(x, y, linestyle='None', marker='.', markersize=2,
            color=(0.7,0.7,0.7))
    ls = '-' if join else 'None'
    ax.plot(x_bin_centers, medians, linestyle=ls, marker='o',
            markersize=10, color='k')
            

def plot(ping_data):
    import matplotlib.pyplot as plt
    import sys
    sys.path.append('./Analysis')
    from processTools import add_ping_availability_int
    
    plt.rcParams.update({'figure.figsize': (12.0, 8.0)})
    fig = plt.figure()
    
    n_row = 2
    n_col = 2
    
    y = ping_data.sec_response
    
    ping_data = add_ping_availability_int(ping_data)

    subplots = {1: {'x': ping_data.sec_since_online,
                    'range': (0.5, 1e7),
                    'bins': np.logspace(-1, 8, num=20),
                    'scale': 'log',
                    'join': True,
                    'xlabel': 'Time online (s)'},
                2: {'x': ping_data.sec_since_pageload,
                    'range': (0.5, 1e7),
                    'bins': np.logspace(-1, 8, num=20),
                    'scale': 'log',
                    'join': True,
                    'xlabel': 'Time since page load (s)'},
                3: {'x': ping_data.time_sent_success_local,
                    'range': (0, 24),
                    'bins': np.linspace(0, 24, num=25),
                    'scale': 'linear',
                    'join': True,
                    'xlabel': 'Time of ping at tutor\'s location (h)'},
                4: {'x': ping_data.availability + \
                        0.8*(np.random.rand(len(ping_data))-0.5),
                    'range': (-1, 3),
                    'bins': [-0.5, 0.5, 1.5, 2.5],
                    'scale': 'linear',
                    'join': False,
                    'xlabel': 'Availability'}}
    
    for p in subplots:
        ax = fig.add_subplot(n_row, n_col, p)
        scatter_with_binned_median(ax, subplots[p]['x'], y, 
            subplots[p]['bins'], join=subplots[p]['join'])
        ax.set_xlim(subplots[p]['range'])
        ax.set_xscale(subplots[p]['scale'])
        ax.set_ylim((0., 300.))
        ax.set_xlabel(subplots[p]['xlabel'])
        ax.set_ylabel('Ping response time (s)')
    
    ax = fig.add_subplot(223)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xticklabels(['midnight', '3am', '6am', '9am', 'noon',
                        '3pm', '6pm', '9pm'])
    
    ax = fig.add_subplot(224)
    ax.text(-0.31, 275, 'Unavailable', fontsize=10)
    ax.text(0.75, 275, 'Available', fontsize=10)
    ax.text(1.61, 275, 'Available now', fontsize=10)
    
    return fig
    
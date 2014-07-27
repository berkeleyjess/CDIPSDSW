"""
Ping timeline for a single lesson ID. Plot the cumulative number
of pings sent (all pings, pings that got a response, and pings
with a response within 30 seconds) vs. time in seconds.
"""

import numpy as np

required_data = ['Data/cleanPingDataFrame.pickle']

def plot(ping_data):
    import matplotlib.pyplot as plt
    
    # get all unique lesson IDs from the ping data
    all_lessons = ping_data.lesson_id.unique()

    # choose a lesson at random
    lesson = all_lessons[np.random.randint(0, len(all_lessons))]
    lesson_pings = ping_data[ping_data.lesson_id == lesson]
    print 'Lesson ID: ' + str(lesson)

    # compute times relative to the earliest ping
    # and response time for each click
    lesson_start = lesson_pings.time_sent_success.iloc[0]
    t_sent = lesson_pings.time_sent_success - lesson_start
    t_clicked = lesson_pings.time_clicked - lesson_start
    dt_clicked = lesson_pings.time_clicked - lesson_pings.time_sent_success

    # create time grid
    total_sec = np.ceil((t_sent.iloc[-1] + np.timedelta64(5, 's')) / \
        np.timedelta64(1, 's')).astype(int)
    t = np.array([np.timedelta64(s, 's') for s in range(total_sec + 1)])
    
    # compute cumulative ping counts on the time grid
    nc_pings = [np.sum(t_sent < t_sec) for t_sec in t]
    nc_pings_clicked = [np.sum((t_sent < t_sec) & (t_clicked > 0)) \
        for t_sec in t]
    nc_pings_clicked_lt30sec = [np.sum((t_sent < t_sec) & \
        (dt_clicked < np.timedelta64(30, 's'))) for t_sec in t]
        
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    
    ax.plot(t, nc_pings, 'k-', label='all pings')
    ax.plot(t, nc_pings_clicked, 'r-', label='clicked')
    ax.plot(t, nc_pings_clicked_lt30sec, 'b-', label='clicked < 30 sec')
    
    ax.set_xlim(0, total_sec)
    ax.set_ylim(0, 1.2*nc_pings[-1])
    
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Cumulative number of pings')
    plt.legend(loc='upper left', frameon=False)
    
    return fig
    
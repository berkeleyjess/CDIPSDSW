"""
Ping timeline for a single lesson ID. Plot the cumulative number
of pings sent (all pings, pings that got a response, and pings
with a response within 30 seconds) vs. time in seconds.

By default, one lesson ID is plotted at random. Specific and/or 
multiple lesson IDs can be selected with the following options:

- N > 1 random lessons can be displayed using the command line
  arguments 'random N' with makePlot.py, e.g.
      python makePlot.py lessonPingsVsTime.py random 4

- Lessons with specific IDs can be plotted using 'id ID1 ID2 ...', e.g.
      python makePlot.py lessonPingsVsTime.py id 134153 89699
      
- Lessons can also be selected by their indices (starting from 0), e.g.
      python makePlot.py lessonPingsVsTime.py index 0 1 2
"""

import numpy as np

required_data = ['Data/cleanPingDataFrame.pickle']

def plot(ping_data, args=None):
    import matplotlib.pyplot as plt
    
    # get all unique lesson IDs from the ping data
    all_lessons = ping_data.lesson_id.unique()

    # choose a single lesson at random by default
    lessons = [all_lessons[np.random.randint(0, len(all_lessons))]]
    
    # check for lessons specified by optional arguments
    if args is not None:
        if len(args) > 1:
            if args[0] == 'random':
                lessons = []
                for i in range(int(args[1])):
                    lesson_index = np.random.randint(0, len(all_lessons))
                    lessons.append(all_lessons[lesson_index])
            elif args[0] == 'id':
                lessons = [int(a) for a in args[1:]]
            elif args[0] == 'index':
                lessons = [all_lessons[int(a)] for a in args[1:]]
            else:
                print 'Option "' + args[0] + '" is unknown. ',
                print 'Using default (one random lesson ID).'
        else:
            print '2 or more arguments required. ',
            print 'Using default (one random lesson ID).'
    
    # set up subplot grid
    n_sub_x = int(np.ceil(np.sqrt(len(lessons))))
    n_sub_y = int(np.ceil(len(lessons) / float(n_sub_x)))
    plt.rcParams.update({'figure.figsize': (6.*n_sub_x, 4.*n_sub_y)})
    fig = plt.figure()
    
    for i, lesson in enumerate(lessons):
    
        lesson_pings = ping_data[ping_data.lesson_id == lesson]
        print 'Lesson ID: ' + str(lesson)

        # compute times relative to the earliest ping
        # and response time for each click
        lesson_start = lesson_pings.time_sent_success.iloc[0]
        t_sent = lesson_pings.time_sent_success - lesson_start
        t_clicked = lesson_pings.time_clicked - lesson_start
        t_clicked_min = (t_clicked.min().values / np.timedelta64(1, 's'))[0]
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
        
        
        ax = fig.add_subplot(n_sub_y, n_sub_x, i+1)
        
        ax.plot(t, nc_pings, 'k-', label='all pings')
        ax.plot(t, nc_pings_clicked, 'r-', label='clicked')
        ax.plot(t, nc_pings_clicked_lt30sec, 'b-', label='clicked < 30 sec')
        ax.plot((t_clicked_min, t_clicked_min), (0, 1.2*nc_pings[-1]), 
            'r:', label='first click')
        
        ax.set_xlim(0, total_sec)
        ax.set_ylim(0, 1.2*nc_pings[-1])
        
        ax.set_xlabel('Time (sec)')
        ax.set_ylabel('Cumulative number of pings')
        plt.legend(loc='upper left', frameon=False)
    
    return fig
    
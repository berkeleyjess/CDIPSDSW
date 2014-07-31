"""
Scatter plots of ping response time vs. various features 
with median response times in bins.
"""

import numpy as np

required_data = ['Analysis/Data/RF_all_features_w_10_eval.pickle']

def plot(eval_df):
    import matplotlib.pyplot as plt
    
    plt.rcParams.update({'figure.figsize': (8.0, 10.0)})
    fig = plt.figure()
    
    ax = fig.add_subplot(311)
    bins_l = np.array(np.arange(0.001, 20.001, 0.5))
    bins_r = bins_l + 0.498
    mean_actual = np.round(eval_df.n_for_fast_response_actual.mean(), 1)
    mean_pred = np.round(eval_df.n_for_fast_response_pred.mean(), 1)
    eval_df.n_for_fast_response_actual.hist(bins=bins_l, ax=ax,
        color=(0,.3,.9), grid=False, 
        label='Actual rankings (avg.=' + str(mean_actual) + ')')
    eval_df.n_for_fast_response_pred.hist(bins=bins_r, ax=ax, 
        color=(.9,.8,.2), grid=False, 
        label='Model rankings (avg.=' + str(mean_pred) + ')')
    ax.set_xlabel(
        'Number of pings needed to get one under-30-second response')
    plt.legend(frameon=False)    
    
    ax = fig.add_subplot(312)
    bins_l = np.array(np.arange(-0.249, 5.251, 0.25))
    bins_r = bins_l + 0.248
    mean_actual = np.round(eval_df.n_fast_in_first_5_actual.mean(), 2)
    mean_pred = np.round(eval_df.n_fast_in_first_5_pred.mean(), 2)
    eval_df.n_fast_in_first_5_actual.hist(bins=bins_l, ax=ax,
        color=(0,.3,.9), grid=False, 
        label='Actual rankings (avg.=' + str(mean_actual) + ')')
    eval_df.n_fast_in_first_5_pred.hist(bins=bins_r, ax=ax, 
        color=(.9,.8,.2), grid=False, 
        label='Model rankings (avg.=' + str(mean_pred) + ')')
    ax.set_xlabel('Number of under-30-second responses from first 5 pings')
    ax.set_xlim(-0.5, 5.5)
    plt.legend(frameon=False)

    ax = fig.add_subplot(313)
    bin_width = 5.
    bar_width = 1./3.
    bins_l = np.array(np.arange(0.001 - bar_width, 
        12. + bar_width + 0.001, bar_width))
    bins_r = bins_l + bar_width - 0.002
    mean_actual = int(np.round(eval_df.wait_time_actual.mean()))
    mean_pred = int(np.round(eval_df.wait_time_pred.mean()))
    (eval_df.wait_time_actual.dropna()/bin_width).astype(int).hist(
        bins=bins_l, ax=ax, color=(0,.3,.9), grid=False, 
        label='Actual rankings (avg.=' + str(mean_actual) + ' sec.)')
    (eval_df.wait_time_pred.dropna()/bin_width).astype(int).hist(
        bins=bins_r, ax=ax, color=(.9,.8,.2), grid=False, 
        label='Model rankings (avg.=' + str(mean_pred) + ' sec.)')
    ax.set_xlabel('Total time until first response (seconds)')
    ax.set_xlim(-1, 13)
    plt.legend(frameon=False)
    plt.draw()
    xticklabels = ax.get_xticklabels()
    ax.set_xticklabels([(lambda s: str(int(bin_width*int(s.get_text()))) if len(s.get_text())>0 else '')(t) for t in xticklabels])

    return fig
    
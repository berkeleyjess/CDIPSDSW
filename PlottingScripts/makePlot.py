"""
General script to set up default plot settings,
make a plot using the commands in a plotting script 
given as a command line argument, and display the plot.
With the -s option, the plot can also be saved to a png file.

Example - creating a plot using
PlottingScripts/histogramLocalTime.py (run from the base directory):
    python PlottingScripts/makePlot.py histogramLocalTime

Each plotting script should define:

- required_data: a list of the files containing
  the DataFrames needed for the plot
  
- plot: a function that takes one or more DataFrames
  (in the same order as in required_data) and returns
  a matplotlib figure

A future revision of this script could include an 
interactive mode that allows several plots to be created
sequentially without needing to reload data each time.
"""

import sys
sys.path.extend(['./PlottingScripts', './Analysis'])
import os.path
import argparse
import cPickle
from importlib import import_module
import loadData

def set_interactive_backend(i=0):
    """
    Look for a matplotlib backend that will allow
    the plot to be displayed.
    """
    backends = matplotlib.rcsetup.interactive_bk
    try:
        plt.switch_backend(backends[i])
    except ImportError:
        if i+1 < len(backends):
            set_interactive_backend(i+1)
        else:
            sys.exit('No interactive backend found.')

import matplotlib
import matplotlib.pyplot as plt
set_interactive_backend()
import defaultSettings

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', help='name of plotting script')
parser.add_argument('-s', '--save_file', help='name of output file')
parser.add_argument('plot_args', nargs=argparse.REMAINDER, 
    help='extra arguments specific to the plotting script')
args = parser.parse_args()
# strip .py extension from script file if it's there
if args.file.endswith('.py'):
    args.file = args.file[:-3]
# check that the script file exists
if not os.path.isfile(os.path.join('PlottingScripts', 
                                   args.file + '.py')):
    sys.exit(args.file + '.py not found')
# import the plotting script
plot_module = import_module(args.file)
if not hasattr(plot_module, 'required_data'):
    sys.exit('Missing required_data in ' + args.file)
if 'plot' not in dir(plot_module):
    sys.exit('Missing plot function in ' + args.file)

# load data
print 'Reading data...'
data = []
for d in plot_module.required_data:
    data.append(loadData.load_pickle(d))

# import the plotting script and run its plot function
print 'Plotting...'
if args.plot_args:
    fig = plot_module.plot(*data, args=args.plot_args);
else:
    fig = plot_module.plot(*data)
plt.tight_layout()

if args.save_file:
    print 'Saving plot as', args.save_file
    fig.savefig(args.save_file)
else:
    plt.show()

    

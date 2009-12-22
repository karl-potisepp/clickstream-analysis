#here we should set some default configuration. support threshold, exclude patterns

session_timeout = 1800

#if float, then relative is considered
#if int, then absolute
support = 0.02

filename = [
    "math-access_log",
    "math-access_log.1",
    "math-access_log.2",
    "math-access_log.3",
    "math-access_log.4",
    "math-access_log.5",
    "math-access_log.6",
    "math-access_log.7",
    "math-access_log.8",
    "math-access_log.9"]    
    
filename.reverse()
#filename = filename[:1]
DATA = "../../data/all/"
OUTPUT = "../../output/"
paths = [DATA+f for f in filename]

range_min = 1
range_max = 100

filter_fn = lambda x: len(x) > 1



import numpy
fig_width_pt = 400  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'pdf',
          'axes.labelsize': 12,
          'text.fontsize': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'figure.figsize': fig_size}
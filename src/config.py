#here we should set some default configuration. support threshold, exclude patterns
import os, sys
from logs import apachelogs
session_timeout = 1800

#if float, then relative is considered, if int, then absolute
support = 0.06


path = "../sample_data/someother/"
log_line_reader = lambda x:  apachelogs.SomeOtherLogLine(x)

#or uncomment

#path = "../sample_data/clf/"
#log_line_reader = lambda x:  apachelogs.ApacheLogLine(x)



if os.path.isdir(path) :
    filename = map(lambda x: os.path.join(path, x), os.listdir(path))
    filename = filter(lambda x: os.path.isfile(x), filename)
else:
  print "invalid path, terminating"
  sys.exit(2)



OUTPUT = "results.html"





#applied onlu on simple session ie [page1, page2]
#can be used to filter session length or contents
session_filter_fn = lambda x: len(x) > 1





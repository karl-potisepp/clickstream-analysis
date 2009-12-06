#here we should set some default configuration. support threshold, exclude patterns

session_timeout = 1800

#if float, then relative is considered
#if int, then absolute
support = 0.1

filename = [
    "math-access_log",
    "math-access_log.1",
    "math-access_log.2",
    "math-access_log.3",
    "math-access_log.4"]
    
filename.reverse()
#filename = filename[:1]
DATA = "../../data/"
OUTPUT = "../../output/"
paths = [DATA+f for f in filename]

range_min = 1
range_max = 100
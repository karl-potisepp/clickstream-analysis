#here we should set some default configuration. support threshold, exclude patterns

session_timeout = 1800

#if float, then relative is considered
#if int, then absolute
support = 0.05

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

"""
filename = [

    "math-access_log",
    "math-access_log.1"]    
print "December"
"""        
filename.reverse()


DATA = "../../data/all/"
OUTPUT = "../../output/"
paths = [DATA+f for f in filename]

range_min = 1
range_max = 100

filter_fn = lambda x: len(x) > 1


def has_keywords(x):
  
  for line in x:
    if line == "inimesed_Instituudid":
      return True
  return False


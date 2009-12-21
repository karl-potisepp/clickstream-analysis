'''
Created on 22.12.2009

@author: Riivo

a pretty naive approach
'''


def deocarate_timings(patterns, log):
  """ return a list of average times spent on each page, based on transaction"""
  transactions = log.get_sessions()
  timings = {}
  for trans in transactions.values():
    i = 0
    for pattern in patterns:
      pos = contains(trans, pattern)
      if pos !=-1:
        timings.setdefault(i, Timing(pattern)).sum(pos, trans)
      i+=1
        
  pass
  
  


def contains(session, pattern):
  """checks where pattern is present in transactions"""
  i = 0
  j = 0
  s = [x.url for x in session]
  for req in s:
    print req
    if req.url == pattern[i]:
      i = i + 1
    else:
      i = 0
    
    if len(pattern) == i:
      
      print j, s, pattern
      return j
     
    j+=1  

  
  return -1

def is_substring(candidate, maximal_forwards):
  s_mf = ",".join(maximal_forwards)
  s_candidate = ",".join(candidate)
  return s_mf.find(s_candidate) != -1
  
class Timing:
  
  def __init__(self, pattern):
    self.pattern = pattern
    self.times = []
    for pat in self.pattern:
      self.times.append(0)
    
  def sum(self, pos, transaction):
    pass  
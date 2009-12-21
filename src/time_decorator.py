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
  if len(pattern) == 0: return -1
  """checks where pattern is present in transactions"""
  i = 0
  j = 0
  print session
  s = [x.url for x in session]
  for req in s:
    if req == pattern[i]:
      i = i + 1
    else:
      i = 0
    if len(pattern) == i: return j
    j+=1  

  
  return -1


class Timing:
  
  def __init__(self, pattern):
    self.pattern = pattern
    self.times = []
    for pat in self.pattern:
      self.times.append(0)
    
  def sum(self, pos, transaction):
    pass
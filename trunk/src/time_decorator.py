'''
Created on 22.12.2009

@author: Riivo

a pretty naive approach
'''
import numpy
import config

def deocarate_timings(patterns, log):
  """ return a list of average times spent on each page, based on transaction"""
  transactions = log.get_sessions()
  timings = {}
  for trans in transactions.values():
    if not config.filter_fn(trans): continue
    i = 0
    for pattern in patterns:
      pos = contains(trans, pattern)
      if pos !=-1:
        timings.setdefault(i, Timing(pattern)).sum(pos, trans)
      i+=1
  
  for k, v in timings.items():
    v.output()
  return timings
  


def contains(session, pattern):
  """checks where pattern is present in transactions"""
  if len(pattern) == 0: return -1
  i = 0
  j = 0

  s = [x.url for x in session]
  for req in s:
    if req == pattern[i]:
      i = i + 1
    else:
      i = 0
    if len(pattern) == i:
      return (j-i)+1
    j+=1  

  
  return -1


class Timing:
  
  def __init__(self, pattern):
    self.pattern = pattern
    self.times = []
    for _ in self.pattern:
      self.times.append([])
    
  def sum(self, pos, transaction):
    for i in range(0, len(self.times)):
      if pos+i+1 >= len(transaction): return
      delta = transaction[pos+i+1].date - transaction[pos+i].date
      self.times[i].append(delta.seconds)

      
  def output(self):
    s = [numpy.around(numpy.average(x),2) for x in self.times]
    m = [numpy.around(numpy.median(x),2) for x in self.times]
    print self.pattern
    print s
    print m
    print "="*20
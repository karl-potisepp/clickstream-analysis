'''
Created on 02.12.2009

@author: Riivo

Implemented ideas are from:

Efficient Data Mining for Path Traversal Patterns
Chen, Ming S. and Park, Jong S. and Yu, Philip S.
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.2212
Knowledge and Data Engineering, 1998
'''


def mf(data):
    maximal_forward_refernces  = set([])
    for session in data:
        mf = [] # current forward refernce
        f  = 1 # direction
        for page in session:
            can_add = -1
            for r in range(len(mf)):
                if mf[r]==page:
                    can_add=r
                    break
                    
            if can_add != -1:
                if f == 1:
                    maximal_forward_refernces.add(tuple([p for p in mf])) # copy
                mf = mf[:r+1]
                f = 0
            else:
                mf.append(page)
                f = 1
            
    return map(lambda x: list(x), maximal_forward_refernces)
    

def mr(data, mf):
    pass
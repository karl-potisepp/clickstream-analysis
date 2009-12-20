'''
Created on 09.12.2009

@author: Riivo
'''

import pickle
import config
import os
    
def encode(rows):
    new_rows = []
    counter = 0
    dict = {}
    for row in rows:
        new_row = []
        for item in row:
            if item not in dict:
                counter = counter + 1
                dict.setdefault(item, counter)
            
            new_row.append(dict[item])
        new_rows.append(new_row)
    return new_rows, dict
                
def fpm(trans, file="woot.txt"):
    transactions, dict = encode(trans)
    sessions_file = open('../../fsm/'+file, 'w')
    for session in transactions:
        line = ",".join(map(str, session)) + '\n'
        sessions_file.write(line)
    sessions_file.close()
    
    codebook = open('../../fsm/'+file+".pickle", 'w')
    
    
    pickle.dump(dict, codebook)
    
    import subprocess
    fp = open('../../fsm/valjund.txt', 'w')
    p = subprocess.Popen(['../../fsm/fsm.exe','apriori', '../../fsm/woot.txt',  '100','../../fsm/output.txt'],
                          stdout=fp,stderr=fp)
    p.wait()
    
    
    print p.returncode
    return decode(open('../../fsm/output.txt'), dict)

        

def decode(rows, codebook):
    new_rows = []
    for row in rows:
        new_row = []
        for item in row.split(" ")[:-1]:
            print item
            new_row.append(resolve_item(int(item), codebook))
        new_rows.append(new_row)
        
    return new_rows
    
    
             
def resolve_item(item, codebook):
    for key, value in codebook.items():
        if value == item:
            return key
    raise NotImplementedError
 




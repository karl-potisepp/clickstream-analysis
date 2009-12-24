'''
Created on 09.12.2009

@author: Riivo
Wrapper for fsm.exe. Provides way to use fsm.exe from python as subprocess

'''

import subprocess
    
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
                
def fpm(trans, support=100, file="woot.txt"):
  
    transactions, dict = encode(trans)
  
    sessions_file = open('../../fsm/'+file, 'w')
    for session in transactions:
        line = ",".join(map(str, session)) + '\n'
        sessions_file.write(line)
    sessions_file.close()
    
    
    
    fp = open('../../fsm/valjund.txt', 'w')
    p = subprocess.Popen(['../../fsm/fsm.exe',
                          'apriori',
                          '../../fsm/woot.txt',
                          str(support),
                          '../../fsm/output.txt'],
                          stdout=fp,stderr=fp)
    p.wait()
    fp.close()

    return decode(open('../../fsm/output.txt'), dict)

        
def decode(rows, codebook):
    tts = 0
    new_rows = []
    first = True
    for row in rows:
        if first:
          tts = int(row.split(" ").pop().replace("(","").replace(")", "").strip()) *1.0
          first = False
          continue
        new_row = []
        split = row.split(" ")
        support = split.pop().replace("(","").replace(")", "").strip()
        support = int(support) * 1.0 / tts
        for item in split:
            new_row.append(resolve_item(int(item), codebook))
        new_rows.append((new_row, support))
        
    return new_rows
    
             
def resolve_item(item, codebook):
    for key, value in codebook.items():
        if value == item:
            return key
    raise NotImplementedError
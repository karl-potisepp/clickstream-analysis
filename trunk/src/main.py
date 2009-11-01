#!/usr/bin/env python
# -*- coding: utf_8 -*-

import apachelogs, logparser
import apriori, statistics



if __name__ == "__main__":

    #log file names
    filename = [
        "math-access_log",
        "math-access_log.1",
        "math-access_log.2",
        "math-access_log.3",
        "math-access_log.4"]
    
    filename.reverse()
        
    print filename 
    paths = ["../../data/"+f for f in filename]


    #read log files
    log = apachelogs.ApacheLogFile(*paths)

    parser = logparser.LogParser(log, [])
    parser.parse()
    stats = statistics.LogFileStatistics(parser)
    
    stats.output_some_statistics()
    ##stats.print_five_number_summary()
    
    #with math.ut.ee data set, big difference if support is 5%, 6%, 7%
    
    min_support = int(parser.get_session_count() * 0.06)

    transactions = parser.get_simple_sessions()


    
    rules = apriori.extract_itemsets(transactions, min_support)
    
    items = apriori.calculate_supports(rules, transactions)
    
    for n, itemset in items:
        print n, itemset
        
    
    import numpy
    import pylab
    lens = sorted([len(session) for session in transactions])
    lens = numpy.array(lens)
    pylab.hist(lens, bins=25, range=(0,100))
    pylab.show()





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
    
    min_support = int(parser.get_session_count() * 0.05)
    print min_support
    range_min = 1
    range_max = 100
    transactions = [session for session in parser.get_simple_sessions() if len(session) > range_min and len(session) < range_max ]


    
    print "="*80
    rules = apriori.extract_itemsets(transactions, min_support)
    
    items = apriori.calculate_supports(rules, transactions)
    
    for n, itemset in items:
        print n, itemset
    
    print "="*80
	
	
    from fpgrowth import find_frequent_itemsets
    items = find_frequent_itemsets(transactions, min_support)
    for itemset in items:
        print itemset
    
    
    import pylab
    lens = sorted([len(session) for session in transactions])
    pylab.hist(lens,bins=(range_max-range_min), range=(range_min,range_max))
    pylab.show()
    




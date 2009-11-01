#!/usr/bin/env python
# -*- coding: utf_8 -*-

import config
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
        
       
    paths = ["../../data/"+f for f in filename]


    #read log files
    log = apachelogs.ApacheLogFile(*paths)

    parser = logparser.LogParser(log, [])
    parser.parse()
    stats = statistics.LogFileStatistics(parser)
    
    stats.output_some_statistics()
    ##stats.print_five_number_summary()
    
    #with math.ut.ee data set, big difference if support is 5%, 6%, 7%
    
    min_support = parser.get_session_count() * 0.06

    
    rules = apriori.print_rules(parser.get_simple_sessions(), min_support)
    






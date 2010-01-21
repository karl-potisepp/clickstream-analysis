# -*- coding: utf_8 -*-
from sqlite3.test import transactions

import config
from algorithms import apriori, sequences, time_decorator
from fsm import fsm_wrapper
from util import statistics, output
from logs import  logparser, apachelogs


def analyse_clickstream(paths, support):

    log = apachelogs.ApacheLogFile(*paths)
    parser = logparser.LogParser(log, [])
    parser.parse()
    
    out = output.Ouput()
    # output simple statistics about data set
    stats = statistics.LogFileStatistics(parser)
    stats.output_some_statistics(out)

    
    # sessions from the parser    
    
    transactions = [session for session in parser.get_simple_sessions() if config.session_filter_fn(session)]
    db_size = len(transactions)
    out.p("db size after reduction: {0}".format(db_size))

    if type(support) is float:
        min_support = int(len(transactions) * support)+1
    else:
        min_support = support
    
    out.p("Support {0}".format(support))



    out.h1("Closed itemset: ")
    out.tbl()
    out.tr(["support", "itemsets"])
    import operator
    data = apriori.extract_itemsets(transactions, min_support)
    data = sorted(data, key=operator.itemgetter(1), reverse=True)
    for itemset, support in data:
        s = 1.0*support / db_size
        out.tr([str(round(s,2)), ", ".join(itemset)] )
    out.e_tbl()
    out.hr()

    
    results = fsm_wrapper.fpm(transactions, min_support)
    out.h1("Sequential patterns: ")
    out.tbl()
    out.tr(["support", "itemsets"])
    for r in  results:
        seq, support = r
        out.tr([str(round(support,2)), " -> ".join(seq)])
    out.e_tbl()
    time_decorator.output_readable(time_decorator.deocarate_timings(results, parser, len(transactions)), out)
    out.hr()
    
    
    
    lrs, mfs = sequences.large_reference_sequences(transactions, min_support)
    out.h1("Large reference sequences: ")
    out.tbl()
    for r in  lrs:
        out.tr([" -> ".join(r)])
    out.e_tbl()
    out.hr()
    
    out.to_file()
    print "done!"

    
  
   
if __name__ == "__main__":
    #some commandline support
    #import util.opts
    #files, suppoert = util.opts.read_opts(argv)
    print "running..."
    analyse_clickstream(config.filename, config.support)
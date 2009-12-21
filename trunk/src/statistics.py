#some simple descriptive statistics
import numpy as np

class LogFileStatistics:
    
    def __init__(self, log_parser):
        self.log_parser = log_parser
        
    #crude function for five number summary
    def __five_num_summary(self, nr_list):
        nr_list.sort()
        l = len(nr_list)
        return (nr_list[0], 
            nr_list[ (l-int(3*(l/4)))-1 ], 
            nr_list[ (l-int(2*(l/4)))-1 ], 
            nr_list[ (l-int(l/4))-1 ],
            nr_list[ l-1 ])
    
    def mean_time_on_url(self, url):
        return np.around(np.median(self.log_parser.urls_times[url]), 1)
    
    def output_some_statistics(self):
        print "Sessions: ", self.log_parser.get_session_count()
        print "Matching lines: ", self.log_parser.get_line_count()
        print "Number of different urls: ", len(self.log_parser.urls)
    
    def print_five_number_summary(self):
        #calculate five number summaries for all urls to find out how 
        #long people stayed on one page
        for url, secs in self.log_parser.urls_times.iteritems():
            print url, self.__five_num_summary(secs), secs
            
    def session_len_graph(self, transactions):
      import pylab
      lens = sorted([len(session) for session in transactions])
      pylab.hist(lens,bins=(range_max-range_min), range=(range_min,range_max))
      pylab.show()

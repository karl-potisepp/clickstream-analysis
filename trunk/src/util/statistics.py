#some simple descriptive statistics

import config
class LogFileStatistics:
    
    def __init__(self, log_parser):
        self.log_parser = log_parser

    def output_some_statistics(self, out):
        out.h1("Some stats")
        out.p("Sessions: {0}".format(self.log_parser.get_session_count()))
        out.p("Matching lines: {0}".format(self.log_parser.get_line_count()))
        out.p("Number of different urls: {0}".format(len(self.log_parser.urls)))    

    def session_len_graph(self, transactions):
      import pylab
      import numpy
      lens = sorted([len(session) for session in transactions])
      min = numpy.min(numpy.array(lens))
      max = 100
      ax = pylab.axes()
      pylab.hist(lens,bins=(max-min), range=(min,max))
      ax.set_xlabel("Session length")
      ax.set_ylabel("Number of sessions")
      pylab.savefig(config.OUTPUT+"session_len.pdf")

    def page_freq_graph(self, transactions):
        import config
        import numpy
        freq_item_list = {}
        for trans in transactions:
            for item in trans:
                if item in freq_item_list:
                    freq_item_list[item]+=1
                else:
                    freq_item_list[item]=1      
        
        from operator import itemgetter
        pages = []
        counts = []
        pos = []
        i = 1.0
        for p, c in sorted(freq_item_list.items(), key=itemgetter(1)):
          pages.append(p)
          counts.append(c)
          pos.append(i)
          i = i + 2.0

        import pylab
        pylab.cla()
        pylab.clf()
        pylab.figure(1)
        pylab.barh(numpy.array(pos), numpy.array(counts), align='center')

        #pylab.yticks(numpy.array(pos), tuple(pages))
        pylab.xlabel("Page count")
        #pylab.grid(True)
        pylab.savefig(config.OUTPUT+"page_distribution.pdf")
        
        

        
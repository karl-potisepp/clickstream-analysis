"""apachelogs.py: Based heavily on apachelogs.py, authored by Kevin Scott (kevin.scott@gmail.com)"""

import re
import fileinput
import config
import time

_lineRegex = re.compile(r'([^ ]*) ([^ ]*) ([^ ]*) \[([^\]]*)\] "([^"]*)" (\d+) ([^ ]*)')
class ApacheLogLine:
    """A Python class whose attributes are the fields of Apache log line.
    CLF format only
    127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
    would have the following field values as an ApacheLogLine:

    ip = '127.0.0.1'
    ident = '-'
    http_user = 'frank'
    time = '10/Oct/2000:13:55:36 -0700'
    request_line = 'GET /apache_pb.gif HTTP/1.0'
    http_response_code = '200'
    http_response_size = 2326
    http_method = 'GET'
    url = '/apache_pb.gif'
    http_vers = 'HTTP/1.0'
    """
    
    def __init__(self, line):
        m = _lineRegex.match(line.strip())
 
        self.ip, self.ident, \
        self.http_user, self.time, \
        self.request_line, self.http_response_code, \
        self.http_response_size = m.groups()
        
        self.http_method, self.url, self.http_vers = self.request_line.split()
        
    def __str__(self):
        """Return a simple string representation of an ApacheLogLine."""
        return ' '.join([self.ip, self.ident, self.time, self.request_line,
                self.http_response_code, self.http_response_size])


class SomeOtherLogLine:

    def __init__(self, line):

        groups = line.strip().split(";")
        #['1', '1257170750', '2.11.2009 16:05:50', '42', '1', '42', 'browser', 'page1', '42']
        #weekday  unix_time  usual_time  client_id  host_ip  site_id  agent  request_url  referer_url

        self.weekday, self.unix_time, self.time, \
        self.client_id, self.ip, self.site_id, \
        self.agent, self.url, self.refere_url = groups
        
        self.http_response_code=200
        self.http_method = "GET"
        self.time= time.strftime("%d/%b/%Y:%H:%M:%S", time.localtime(float(self.unix_time)))
        
        
    def __str__(self):
        """Return a simple string representation of an ApacheLogLine."""
        return ' '.join([self.ip, self.ident, self.time, self.request_line,
                self.http_response_code, self.http_response_size])    





class ApacheLogFile:
    """An abstraction for reading and parsing Apache log files."""
    def __init__(self, *filename):
        
        """Instantiating an ApacheLogFile opens a log file.    
        Client is responsible for closing the opened log file by calling close()"""
        self.f = fileinput.input(filename)

    def close(self):
        """Closes the Apache log file."""
        self.f.close()

    def __iter__(self):
        """Returns a log line object for each iteration. """
        
        for line in self.f:
            log_line = config.log_line_reader(line)
            yield log_line

                    

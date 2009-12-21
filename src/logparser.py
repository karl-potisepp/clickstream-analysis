# -*- coding: utf_8 -*-

import uuid
from datetime import datetime
import re

import config

class LogParser:
    
    #dictionary for storing sessions
    #key - session id
    #value - 
    sessions = {}

    #list of IPs deemed non-useful (automated pollers, search robots)
    ip_blacklist = []
    
    # set for urls
    urls = set([])

    count = 0
    
    
    def __init__(self, apache_log_file, ip_blacklist = []):
        self.apache_log_file = apache_log_file
        self.ip_blacklist = ip_blacklist

    def __format_url(self, line):
        
        #format URLs so that equivalent URLs would always be same
        
        #strip parts starting with ? from urls
        qmark_index = line.url.find("?")
        if qmark_index != -1:
            line.url = line.url[0:qmark_index]
        #strip slash from end of url
        
        if len(line.url) > 0 and line.url[len(line.url) - 1] == "/":
            line.url = line.url[0:len(line.url) - 1]
        
        if len(line.url) > 0 and line.url[0] == "/":
            line.url = line.url[1:]
        
        line.url = line.url.replace("/", "_")
        if len(line.url) == 0:
            line.url = "avaleht"
        
        line.url = re.sub(r'[^\w]', '', line.url)

    
    def parse(self):

        #dictionary for storing the last url for every session
        #key - session id
        #value - last url for that session
        last_session_url = {}

        #dictionary containing tuples (time, unique id) for IPs
        #key - IP
        #value - (time of last request, unique id)
        last_ip = {}

        #dictionary for storing the last http_response_code for every session
        #key - session id
        #value - last http_response_code for that session
        last_session_http_code = {}
    
        for line in self.apache_log_file:
            
            #whether or not the requested file is robots.txt
            #if it is, we add the ip to the blacklist
            if line.url.find("robots.txt") != -1:
                self.ip_blacklist.append(line.ip)
    
            #whether the line should be discarded or not
            if self.filter(line):
                continue
        
            self.__format_url(line)
    
            #add URL to list of URLs
            self.urls.add(line.url)
    
            line.time = line.time.split()[0]
            line.date = datetime.strptime(line.time, '%d/%b/%Y:%H:%M:%S')
    
            #here we add a tuple of (date of request, unique id)
            #to correspond to an IP address in the last_ip dictionary
            last_ip.setdefault(line.ip, (line.date, uuid.uuid4().hex))
            (last_time_for_ip, last_session_for_ip) = last_ip[line.ip]
            
            delta =  line.date - last_time_for_ip
            if delta.seconds  > config.session_timeout:
                sess_key =  uuid.uuid4().hex
            else:
                sess_key =  last_session_for_ip

            #if last request in this session was met with http code 302, then
            #this line is probably a redirect and should be discarded
            code = last_session_http_code.get(sess_key, 0)
            if int(code) == 302 and  int(line.http_response_code) == 200 and delta.seconds < 5:
                continue        

            last_session_url.setdefault(sess_key, line.url)
            last_ip[line.ip] = (line.date, sess_key)
            # add last session http code
            last_session_http_code.setdefault(sess_key, line.http_response_code)
    
            #add line to sessions dictionary
            #if session doesn't exist in sessions, then initialize it
            self.sessions.setdefault(sess_key, []).append(line)
    
            self.count +=1

    
    def get_sessions(self):
        return self.sessions
    
    def get_line_count(self):
        return self.count
    
    def get_session_count(self):
        return len(self.sessions)
    
    #function to evaluate whether a log file line is useful or not
    #XXX make configurable
    def filter(self, line):
        
        result = False
        #if ip is in blacklist
        if self.ip_blacklist.count(line.ip) > 0:
            return False
        #no images, CSS or JS files
        result = result or line.url.find(".png") != -1
        result = result or line.url.find(".gif") != -1
        result = result or line.url.find(".jpg") != -1
        result = result or line.url.find(".pjpeg") != -1
        result = result or line.url.find(".png") != -1
        result = result or line.url.find(".x-png") != -1
        result = result or line.url.find(".js") != -1
        result = result or line.url.find(".css") != -1
        result = result or line.url.find(".ico") != -1
    
        #no error pages
        result = result or line.url.find("/errorleht") != -1
        #result = result or line.http_response_code == 302
    
        #no HTTP OPTIONS
        result = result or line.http_method.find("OPTIONS") != -1
    
        #no home directories
        result = result or line.url.find("/~") != -1
    
        return result


            
    def get_simple_sessions(self):
        simple_sessions = []
        for s in self.sessions.values():
            session = []
            for line in s:
                session.append(line.url)
            simple_sessions.append(session)
        
        return simple_sessions
        
class Session:
  def __init__(self, session):
    self.pages = [x.url for x in session]
    self.times = [x.time for x in session]
  
  
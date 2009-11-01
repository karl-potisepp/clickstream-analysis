# -*- coding: utf_8 -*-

import uuid
import config
from datetime import datetime

class LogParser:
    
    #dictionary for storing sessions
    #key - session id
    #value - 
    sessions = {}
    


    #list of IPs deemed non-useful (automated pollers, search robots)
    ip_blacklist = []
    
    # set for urls
    urls = set([])

    #dictionary for storing the interval in seconds between request for an url and last request in that session
    #key - url
    #value - list of intervals
    urls_times = {}

    count = 0
    
    
    def __init__(self, apache_log_file, ip_blacklist = []):
        self.apache_log_file = apache_log_file
        self.ip_blacklist = ip_blacklist
    
    def parse(self):

        #dictionary for storing the last url for every session
        #key - session id
        #value - last url for that session
        last_session_url = {}   
    
        #dictionary containing tuples (time, unique id) for IPs
        #key - IP
        #value - (time of last request, unique id)
        last_ip = {}    
    
        
    
        for line in self.apache_log_file:
            
            #checks whether line is useful or not
    
            #whether or not the requested file is robots.txt
            #if it is, we add the ip to the blacklist
            if line.url.find("robots.txt") != -1:
                self.ip_blacklist.append(line.ip)
    
            #whether the line should be discarded or not
            if self.filter(line):
                continue
    
            #END checks whether line is useful or not
    
    
            #format URLs so that equivalent URLs would always be same        
    
            
            #strip parts starting with ? from urls
            qmark_index = line.url.find("?")
            if qmark_index != -1:
                line.url = line.url[0:qmark_index]
            
            #strip slash from end of url
            if len(line.url) > 0 and line.url[len(line.url)-1] == "/": 
                line.url = line.url[0:len(line.url)-1]
            
            if len(line.url) == 0:
                line.url = "___"
            #END format URLs
    
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
    
            #to calculate the time spent viewing the url in hand, we must know 
            #the time of the next click within this session
            #so we must have a variable for each session storing the url of it's last request
    
            #if the last url for the current session is known
            #then delta.seconds is the amount of seconds spent viewing that url
            if sess_key in last_session_url:            
                if line.url in self.urls_times:
                    self.urls_times[line.url].append(delta.seconds)
                else:
                    self.urls_times[line.url] = [delta.seconds]            
                
    
            last_session_url.setdefault(sess_key, line.url)
        
            last_ip[line.ip] = (line.date, sess_key)
    
            #add line to sessions dictionary
            #if session doesn't exist in sessions, then initialize it
            self.sessions.setdefault(sess_key, []).append(line)
    
            self.count +=1

    
    def get_session(self):
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
        
#!/usr/bin/env python
# -*- coding: utf_8 -*-

import apachelogs
from datetime import datetime, date, time
import uuid
import numpy as np

#function to evaluate whether a log file line is useful or not
def filter(line, ip_blacklist):
	result = False
	#if ip is in blacklist
	if ip_blacklist.count(line.ip) > 0:
		return False
	#no images, CSS or JS files
	result = result or line.url.find(".png") != -1
	result = result or line.url.find(".gif") != -1
	result = result or line.url.find(".jpg") != -1
	result = result or line.url.find(".png") != -1
	result = result or line.url.find(".js") != -1
	result = result or line.url.find(".css") != -1
	result = result or line.url.find(".ico") != -1

	#no HTTP OPTIONS
	result = result or line.http_method.find("OPTIONS") != -1

	#no home directories
	result = result or line.http_method.find("/~") != -1

	return result

if __name__ == "__main__":


	filename = ["data/math-access_log","data/math-access_log.1","data/math-access_log.2","data/math-access_log.3","data/math-access_log.4"]
	log = apachelogs.ApacheLogFile(*filename)

	sessions = {}

	last_ip = {}

	#list of IPs deemed non-useful (automated pollers, search robots)
	ip_blacklist = []
	
	urls = set([])
	count = 0

	for line in log:

		#whether or not the requested file is robots.txt
		#if it is, we add the ip to the blacklist
		if line.url.find("robots.txt") != -1:
			ip_blacklist.append(line.ip)

		if filter(line, ip_blacklist):
			continue

		#TODO: strip parts containing ?var=id&var2=id2 from the end of URLs 

		urls.add(line.url)
		line.time = line.time.split()[0]
		line.date = datetime.strptime(line.time, '%d/%b/%Y:%H:%M:%S')

		last_ip.setdefault(line.ip, (line.date, uuid.uuid4().hex))
		
		(last_time_for_ip, last_session_for_ip) = last_ip[line.ip]
		
		delta =  line.date - last_time_for_ip
		#1800 session time out session
		if delta.seconds  > 1800:
			sess_key =  uuid.uuid4().hex
		else:
			sess_key =  last_session_for_ip
	
		last_ip[line.ip] = (line.date, sess_key)
		sessions.setdefault(sess_key, []).append(line)

		count +=1


    #sessions dict contains all sessions

	#TODO: output a list of sessions
    

	print "Matching lines: ", count
	print "No events", len(urls)


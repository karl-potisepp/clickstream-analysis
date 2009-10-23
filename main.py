#!/usr/bin/env python
# -*- coding: utf_8 -*-

import apachelogs
from datetime import datetime
import uuid
import apriori

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

	#no error pages
	result = result or line.url.find("/errorleht") != -1

	#no HTTP OPTIONS
	result = result or line.http_method.find("OPTIONS") != -1

	#no home directories
	result = result or line.http_method.find("/~") != -1

	return result

if __name__ == "__main__":

	#log file names
	filename = [
		"math-access_log",
		"math-access_log.1",
		"math-access_log.2",
		"math-access_log.3",
		"math-access_log.4"]
	
	paths = ["../data/"+f for f in filename]

	#read log files
	log = apachelogs.ApacheLogFile(*paths)

	#dictionary for storing sessions
	#key - session id
	#value - 
	sessions = {}

	#dictionary containing tuples (time, unique id) for IPs
	#key - IP
	#value - (time of last request, unique id)
	last_ip = {}

	#list of IPs deemed non-useful (automated pollers, search robots)
	ip_blacklist = []
	
	# set for urls
	urls = set([])

	#dictionary for storing the interval in seconds between request for an url and last request in that session
	#key - url
	#value - list of intervals
	urls_times = {}
	#dictionary for storing the last url for every session
	#key - session id
	#value - last url for that session
	last_session_url = {}


	count = 0

	for line in log:
		
		#checks whether line is useful or not

		#whether or not the requested file is robots.txt
		#if it is, we add the ip to the blacklist
		if line.url.find("robots.txt") != -1:
			ip_blacklist.append(line.ip)

		#whether the line should be discarded or not
		if filter(line, ip_blacklist):
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

		#END format URLs

		#TODO: to calculate the time spent viewing the url in hand, we must know 
		#the time of the next click within this session
		#so we must have a variable for each session storing the it's last request

		#add URL to list of URLs
		urls.add(line.url)
		line.time = line.time.split()[0]
		line.date = datetime.strptime(line.time, '%d/%b/%Y:%H:%M:%S')

		#here we add a tuple of (date of request, unique id)
		#to correspond to an IP address in the last_ip dictionary
		last_ip.setdefault(line.ip, (line.date, uuid.uuid4().hex))
		
		(last_time_for_ip, last_session_for_ip) = last_ip[line.ip]
		
		delta =  line.date - last_time_for_ip

		#1800 seconds session time out
		if delta.seconds  > 1800:
			sess_key =  uuid.uuid4().hex
		else:
			sess_key =  last_session_for_ip
	
		last_ip[line.ip] = (line.date, sess_key)

		#add line to sessions dictionary
		#if session doesn't exist in sessions, then initialize it
		sessions.setdefault(sess_key, []).append(line)

		count +=1

	min_support = 1000

	simple_sessions = []
	for s in sessions.values():
		session = []
		for line in s:
			session.append(line.url)
		simple_sessions.append(session)
	
	
	
	apriori.print_rules(simple_sessions, min_support)
	

	print "session", len(sessions)
	print "Matching lines: ", count
	print "No events", len(urls)


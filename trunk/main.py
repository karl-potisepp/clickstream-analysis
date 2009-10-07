import apachelogs
from datetime import datetime, date, time
import uuid
import numpy as np

def filter(line):
	result = False
	result = result or line.url.find(".png") != -1
	result = result or line.url.find(".gif") != -1
	result = result or line.url.find(".jpg") != -1
	result = result or line.url.find(".png") != -1
	result = result or line.url.find(".js") != -1
	result = result or line.url.find(".css") != -1
	return result

if __name__ == "__main__":


	filename = ["data/math-access_log","data/math-access_log.1","data/math-access_log.2","data/math-access_log.3","data/math-access_log.4"]
	log = apachelogs.ApacheLogFile(*filename)

	sessions = {}

	last_ip = {}
	
	urls = set([])
	count = 0

	for line in log:
		if filter(line):
			continue
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
    

	print "Matching lines: ", count
	print "No events", len(urls)


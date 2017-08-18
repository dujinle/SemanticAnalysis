#!/usr/bin/python
# -*- coding:utf-8 -*-

import time, datetime

def GetTimeStamp(t_time):
	try:
		tupletime = list(t_time);
		if tupletime[0] == 'null': return 0;
		if tupletime[1] == 'null': tupletime[1] = 0;
		if tupletime[2] == 'null': tupletime[2] = 0;
		if tupletime[3] == 'null': tupletime[3] = 0;
		if tupletime[4] == 'null': tupletime[4] = 0;
		if tupletime[5] == 'null': tupletime[5] = 0;
		if tupletime[6] == 'null': tupletime[6] = 0;
		if tupletime[7] == 'null': tupletime[7] = 0;
		if tupletime[8] == 'null': tupletime[8] = 0;
		while len(tupletime) < 9:
			tupletime.append(0);
		return time.mktime(tupletime);
	except Exception as e:
		raise e

def GetTimeFromStamp(stamp):
	time_tuple = time.localtime(stamp);
	return time_tuple;


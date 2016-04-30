#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,re
#reload(sys);
#sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../../commons'));
#============================================
import config
month = [31,31,28,31,30,31,30,31,31,30,31,30,31];
leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];
tmenu = {
	'sec':config.tm_sec,
	'min':config.tm_min,
	'hour':config.tm_hour,
	'day':config.tm_day,
	'month':config.tm_mon,
	'year':config.tm_year
};


def _make_sure_time(mytime,idx):
	if mytime[0] == 'null': return False;
	if idx >= config.tm_sec:
		if mytime[config.tm_sec] < 0:
			mytime[config.tm_min] -= (mytime[config.tm_sec] // 60 + 1);
			mytime[config.tm_sec] = 60 - mytime[config.tm_sec] % 60;
		if mytime[config.tm_sec] >= 60:
			mytime[config.tm_min] += mytime[config.tm_sec] // 60;
			mytime[config.tm_sec] = mytime[config.tm_sec] % 60;

	if idx >= config.tm_min:
		if mytime[config.tm_min] < 0:
			mytime[config.tm_hour] -= (mytime[config.tm_min] // 60 + 1);
			mytime[config.tm_min] = 60 - mytime[config.tm_min] % 60;
		if mytime[config.tm_min] >= 60:
			mytime[config.tm_hour] += mytime[config.tm_min] // 60;
			mytime[config.tm_min] = mytime[config.tm_min] % 60;

	if idx >= config.tm_hour:
		if mytime[config.tm_hour] < 0:
			mytime[config.tm_day] -= (mytime[config.tm_hour] // 24 + 1);
			mytime[config.tm_hour] = 24 - mytime[config.tm_hour] % 24;
		if mytime[config.tm_hour] > 24:
			mytime[config.tm_day] += (mytime[config.tm_hour] // 24);
			mytime[config.tm_hour] = mytime[config.tm_hour] % 24;

	if _is_leap_year(mytime[config.tm_year]) and idx >= config.tm_day:
		mymon = mytime[config.tm_mon] % 12;
		while mytime[config.tm_day] <= 0:
			mytime[config.tm_day] = mytime[config.tm_day] + leap_mon[mymon - 1];
			mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
			if mymon == 0: mymon = 12;
			else: mymon = mymon - 1;

		mymon = mytime[config.tm_mon] % 12;
		while mytime[config.tm_day] > leap_mon[mymon]:
			mytime[config.tm_day] = mytime[config.tm_day] - leap_mon[mymon];
			mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
			mymon = mymon + 1;
	elif idx >= config.tm_day:
		mymon = mytime[config.tm_mon] % 12;
		while mytime[config.tm_day] <= 0:
			mytime[config.tm_day] = mytime[config.tm_day] + month[mymon - 1];
			mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
			if mymon == 0: mymon = 12;
			else: mymon = mymon - 1;
		while mytime[config.tm_day] > month[mymon]:
			mytime[config.tm_day] = mytime[config.tm_day] - month[mymon];
			mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
	if idx >= config.tm_mon:
		while mytime[config.tm_mon] <= 0:
			mytime[config.tm_mon] = mytime[config.tm_mon] + 12;
			mytime[config.tm_year] = mytime[config.tm_year] - 1;
		while mytime[config.tm_mon] > 12:
			mytime[config.tm_mon] = mytime[config.tm_mon] - 12;
			mytime[config.tm_year] = mytime[config.tm_year] + 1;

def _is_leap_year(myyear):
	if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
		return True;
	return False;

def _creat_empty_interval():
	my_interval = dict();
	my_interval['str'] = '';
	my_interval['start'] = ['null','null','null','null','null','null','null','null','null'];
	my_interval['end'] = ['null','null','null','null','null','null','null','null','null'];
	return my_interval;

def _creat_next_interval(struct):
	my_interval = dict();
	my_interval['str'] = '';
	my_interval['start'] = ['null','null','null','null','null','null','null','null','null'];
	my_interval['end'] = ['null','null','null','null','null','null','null','null','null'];
	struct['intervals'].append(my_interval);
	struct['my_inter_id'] = struct['my_inter_id'] + 1;
	return my_interval;

def _list_copy(l1,l2,idb):
	for idx,value in enumerate(l1):
		l2[idx] = value;
		if idb == idx: break;
	return l2;

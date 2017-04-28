#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,re,time
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
month = [31,31,28,31,30,31,30,31,31,30,31,30,31];
leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];

#time['year','month','day','hour','min','sec','week','day in year','week_idx']

tmenu = {
	'week_idx':8,
	'week':6,
	'sec':5,
	'min':4,
	'hour':3,
	'day':2,
	'month':1,
	'year':0
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
	tlist = list()
	tlist.extend(l2);
	for idx,value in enumerate(l1):
		if tlist[idx] <> 'null' and value <> 'null':
			tlist[idx] = tlist[idx] + value;

		if value <> 'null': tlist[idx] = value;
		if idb == idx: break;
	return tlist;

def _create_null_time():
	return ['null','null','null','null','null','null','null','null','null'];

def _is_merge_able(st,et):
	if not st.has_key('stime'): return None;
	if not et.has_key('stime'): return None;
	if st['scope'] == et['scope']: return None;

	stime = _list_copy(st['stime'],et['stime'],8);
	etime = _list_copy(st['stime'],et['etime'],8);
	return [stime,etime];

def _get_time_stamp(t_time):
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
	while len(tupletime) < 9: tupletime.append(0);
	return time.mktime(tupletime);

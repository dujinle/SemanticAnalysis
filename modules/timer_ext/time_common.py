#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,time

month = [31,31,28,31,30,31,30,31,31,30,31,30,31];
leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];

#time['year','month','day','hour','min','sec','week','week_idx','is-enable']

tmenu = {
	'enable':8,
	'week_idx':7,
	'week':6,
	'sec':5,
	'min':4,
	'hour':3,
	'day':2,
	'month':1,
	'year':0
};
def _list_copy(l1,l2,idb,flg = False):
	tlist = list()
	tlist.extend(l1);
	for idx,value in enumerate(l2):
		if tlist[idx] <> 'null' and value <> 'null' and flg == False:
			tlist[idx] = tlist[idx] + value;
		elif tlist[idx] <> 'null' and value <> 'null':
			tlist[idx] = value;
		if value <> 'null': tlist[idx] = value;
		if idb <= idx: break;
	return tlist;

def _list_empty_copy(l1,l2,idb,flg = False):
	tlist = list()
	tlist.extend(l1);
	for idx,value in enumerate(l2):
		if idb <= idx: break;
		if tlist[idx] <> 'null':
			continue;
		else:
			tlist[idx] = value;
	return tlist;

def _create_null_time():
	return ['null','null','null','null','null','null','null','null','null'];

def _is_merge_able(st,et,fal = False):
	if not st.has_key('stime'): return None;
	if not et.has_key('stime'): return None;
	if fal == False and st['scope'] == et['scope']: return None;

	stime = _list_copy(st['stime'],et['stime'],8,fal);
	etime = _list_copy(st['stime'],et['etime'],8,fal);
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

def time_from_stamp(stamp):
	time_tuple = time.localtime(stamp);
	return time_tuple;

def _make_sure_time(mytime,sidx):
	if mytime[0] == 'null': return False;
	tidx = tmenu['sec'];
	idx = tmenu[sidx];
	if idx >= tidx:
		if mytime[tidx] < 0:
			mytime[tidx - 1] -= (mytime[tidx] // 60 + 1);
			mytime[tidx] = 60 - mytime[tidx] % 60;
		if mytime[tidx] >= 60:
			mytime[tidx - 1] += mytime[tidx] // 60;
			mytime[tidx] = mytime[tidx] % 60;

	tidx = tmenu['min'];
	if idx >= tidx:
		if mytime[tidx] < 0:
			mytime[tidx - 1] -= (mytime[tidx] // 60 + 1);
			mytime[tidx] = 60 - mytime[tidx] % 60;
		if mytime[tidx] >= 60:
			mytime[tidx] += mytime[tidx] // 60;
			mytime[tidx] = mytime[tidx] % 60;

	tidx = tmenu['hour'];
	if idx >= tidx:
		if mytime[tidx] < 0:
			mytime[tidx - 1] = (mytime[tidx] // 24 + 1);
			mytime[tidx] = 24 - mytime[tidx] % 24;
		if mytime[tidx] > 24:
			mytime[tidx - 1] += (mytime[tidx] // 24);
			mytime[tidx] = mytime[tidx] % 24;

	tidx = tmenu['day'];
	if _is_leap_year(mytime[tmenu['year']]) and idx >= tidx:
		mymon = mytime[tidx - 1] % 12;
		while mytime[tidx] <= 0:
			mytime[tidx] = mytime[tidx] + leap_mon[mymon - 1];
			mytime[tidx - 1] = mytime[tidx - 1] - 1;
			if mymon == 0: mymon = 12;
			else: mymon = mymon - 1;

		mymon = mytime[tidx - 1] % 12;
		while mytime[tidx] > leap_mon[mymon]:
			mytime[tidx] = mytime[tidx] - leap_mon[mymon];
			mytime[tidx - 1] = mytime[tidx - 1] + 1;
			mymon = mymon + 1;
	elif idx >= tidx:
		mymon = mytime[tidx - 1] % 12;
		while mytime[tidx] <= 0:
			mytime[tidx] = mytime[tidx] + month[mymon - 1];
			mytime[tidx - 1] = mytime[tidx - 1] - 1;
			if mymon == 0: mymon = 12;
			else: mymon = mymon - 1;
		while mytime[tidx] > month[mymon]:
			mytime[tidx] = mytime[tidx] - month[mymon];
			mytime[tidx - 1] = mytime[tidx - 1] + 1;

	tidx = tmenu['month'];
	if idx >= tidx:
		while mytime[tidx] <= 0:
			mytime[tidx] = mytime[tidx] + 12;
			mytime[tidx - 1] = mytime[tidx - 1] - 1;
		while mytime[tidx] > 12:
			mytime[tidx] = mytime[tidx] - 12;
			mytime[tidx - 1] = mytime[tidx - 1] + 1;

def _is_leap_year(myyear):
	if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
		return True;
	return False;


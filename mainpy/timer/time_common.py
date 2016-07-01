#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,re
#reload(sys);
#sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import config
from myexception import MyException

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

def _if_has_key(intext,keys):
	rlist = dict();
	strs = intext;
	for key in keys:
		while True:
			if strs.find(key) <> -1:
				idx = strs.find(key);
				rlist[idx] = key;
				strs = strs.replace(key,'X'*len(key),1);
			else: break;
	tlist = sorted(rlist.items(),key = lambda d: d[0]);
	res_list = list();
	for t in tlist: res_list.append(t[1]);
	return res_list;

def _make_only_one(matchs):
	best_id = 0x2000;
	best_end = 0;
	mykey = None;
	for key in matchs.keys():
		match = matchs[key];
		if match.start() < best_id:
			best_id = match.start();
			best_end = match.end();
			mykey = key;
		elif match.start() == best_id:
			if match.end() > best_end:
				best_id = match.start();
				best_end = match.end();
				mykey = key;
	return mykey;

def _make_sure_time(mytime,idx):
	if mytime[0] == 'null': return False;
	if mytime[config.tm_sec] > 60:
		mytime[config.tm_sec] = mytime[config.tm_sec] - 60;
		mytime[config.tm_min] = mytime[config.tm_min] + 1;
		return True;
	elif mytime[config.tm_sec] < 0:
		mytime[config.tm_sec] = mytime[config.tm_sec] + 60;
		mytime[config.tm_min] = mytime[config.tm_min] - 1;
		return True;

	if mytime[config.tm_min] > 60:
		mytime[config.tm_min] = mytime[config.tm_min] - 60;
		mytime[config.tm_hour] = mytime[config.tm_hour] + 1;
		return True;
	elif mytime[config.tm_min] < 0:
		mytime[config.tm_min] = mytime[config.tm_min] + 60;
		mytime[config.tm_hour] = mytime[config.tm_hour] - 1;
		return True;

	if mytime[config.tm_hour] > 24:
		mytime[config.tm_hour] = mytime[config.tm_hour] - 24;
		mytime[config.tm_day] = mytime[config.tm_day] + 1;
		return True;
	elif mytime[config.tm_hour] < 0:
		mytime[config.tm_hour] = mytime[config.tm_hour] + 24;
		mytime[config.tm_day] = mytime[config.tm_day] - 1;
		return True;

	if _is_leap_year(mytime[config.tm_year]):
		mymon = mytime[config.tm_mon] % 12;
		if mytime[config.tm_day] > leap_mon[mymon] and idx >= config.tm_day:
			mytime[config.tm_day] = mytime[config.tm_day] - leap_mon[mymon];
			mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
			return True;
		elif mytime[config.tm_day] <= 0 and idx >= config.tm_day:
			mytime[config.tm_day] = mytime[config.tm_day] + leap_mon[mymon - 1];
			mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
			return True;
	else:
		mymon = mytime[config.tm_mon] % 12;
		if mytime[config.tm_day] > month[mymon] and idx >= config.tm_day:
			mytime[config.tm_day] = mytime[config.tm_day] - month[mymon];
			mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
			return True;
		elif mytime[config.tm_day] <= 0 and idx >= config.tm_day:
			mytime[config.tm_day] = mytime[config.tm_day] + month[mymon - 1];
			mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
			return True;

	if mytime[config.tm_mon] > 12 and idx >= config.tm_mon:
		mytime[config.tm_mon] = mytime[config.tm_mon] - 12;
		mytime[config.tm_year] = mytime[config.tm_year] + 1;

def _is_leap_year(myyear):
	if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
		return True;
	return False;

def _find_idx(text,match,extend):
	idx = text.find(match);
	prev_str = text[:idx];
	num = len(re.findall('UT',prev_str));
	num += len(re.findall('NT',prev_str));
	num += len(re.findall('WT',prev_str));
	num += len(re.findall('QT',prev_str));
	num += len(re.findall(extend,prev_str));
	return num;

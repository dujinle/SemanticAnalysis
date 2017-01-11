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

def _find_idx(text,match,extend):
	idx = text.find(match);
	prev_str = text[:idx];
	num = len(re.findall('AA',prev_str));
	num += len(re.findall(extend,prev_str));
	return num;

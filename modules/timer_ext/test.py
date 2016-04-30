#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#============================================
import common
from time_mager import TimeMager

tmager = TimeMager();
tmager.init();
for lstr in sys.stdin.readlines():
	struct = dict();
	larry = lstr.strip('\n').split('\t');
	struct['text'] = larry[0].decode('utf8');
	tmager.encode(struct);
	if len(larry) == 1:
		common.print_dic(struct);
		continue;
	ans = larry[1].decode('utf8');
	for key in struct['time_stcs'].keys():
		item = struct['time_stcs'][key];
		lstr = item['str'];
		stime = [str(i) for i in item['stime'] if i <> 'null'];
		etime = [str(i) for i in item['etime'] if i <> 'null'];
		tstr = '-'.join(stime);
		estr = '-'.join(etime);
		ans_arry = ans.split(',');
		if tstr <> ans_arry[0] or estr <> ans_arry[1]:
			print lstr,tstr,estr,ans,'failed';
		else:
			print lstr,'success';
#	common.print_dic(struct);

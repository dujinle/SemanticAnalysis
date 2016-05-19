#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../../commons'));
sys.path.append(os.path.join(base_path,'../../'));
sys.path.append(os.path.join(base_path,'../'));
#============================================
import common,config
from time_normal import TNormal,TBucket
from time_week import TWeek
from time_festival import TFestival,TEFestival
from time_solarterm import TSolarTerm
from time_decade import TDecade
from time_front import TFront
from time_tail import TTail
from time_replace import TReplace

def load_test_hour(hfile):
	dp = open(hfile,'r');
	return dp.readlines();

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Usage: %s file' %sys.argv[0];
		sys.exit(-1);

	ut = TNormal();
	nt = TBucket();
	wt = TWeek();
	tf = TFestival();
	tef = TEFestival();
	ts = TSolarTerm();
	td = TDecade();
	tof = TFront();
	tt = TTail();
	tre = TReplace();
	ut.load_data('../tdata/TNormal.txt');
	nt.load_data('../tdata/TBucket.txt');
	wt.load_data('../tdata/TWeek.txt');
	tf.load_data('../tdata/TFestival.txt');
	tef.load_data('../tdata/TEFestival.txt');
	ts.load_data('../tdata/TSolarterm.txt');
	td.load_data('../tdata/TDecade.txt');
	tof.load_data('../tdata/TFront.txt');
	tre.load_data('../tdata/TReplace.txt');

	test_data = load_test_hour(sys.argv[1]);
	for data in test_data:
		if data[0] == '#': continue;
		dstr = data.strip('\r\n').split('\t');
		ddate = dstr[0].decode('utf-8');
		dndate = dstr[1].split(',');

		struct = dict();
		struct['text'] = ddate;
		struct['intervals'] = list();
		struct['my_inter_id'] = 0;
		struct['step_id'] = 0;
		idx = 0;
		while True:
			if struct['step_id'] >= len(struct['text']):
				tt.encode(struct);
				break;
			tre.encode(struct);
			ret = tof.encode(struct);
			ret += ut.encode(struct);
			ret += nt.encode(struct);
			ret += wt.encode(struct);
			ret += tf.encode(struct);
			ret += tef.encode(struct);
			ret += ts.encode(struct);
			ret += td.encode(struct);
			if ret == -8:
				tt.encode(struct);
				struct['step_id'] = struct['step_id'] + 1;
		myinterval = struct['intervals'][0];
		start = myinterval['start'];
		end = myinterval['end'];
		for idx,sl in enumerate(dndate[0].split('-')):
			if start[idx] == 'null' and sl == 'null':
				break;
			if start[idx] <> int(sl):
				common.print_dic(struct);
				sys.exit(-1);
		for idx,sl in enumerate(dndate[1].split('-')):
			if end[idx] == 'null' and sl == 'null':
				break;
			if end[idx] <> int(sl):
				common.print_dic(struct);
				sys.exit(-1);
		print '%s hour[%s-%s] success' %(ddate,dndate[0],dndate[1]);

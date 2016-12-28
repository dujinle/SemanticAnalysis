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
#============================================
import common,config

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: %s infile testfile' %sys.argv[0];
		sys.exit(-1);

regdata = common.read_json(sys.argv[1]);
testdata = common.read_json(sys.argv[2]);
if regdata.has_key('template'):
	for mm in regdata['template']:
		tkey = mm['func'];
		com = re.compile(mm['reg']);
		if testdata.has_key(tkey):
			for it in testdata[tkey]:
				match = com.search(it);
				if match is None:
					print it,'faile',
				else:
					print match.group(0),it,'succ'

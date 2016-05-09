#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../'));
sys.path.append(os.path.join(base_path,'../commons'));
#==============================================================
import common
from myexception import MyException
common.debug = False;
from mager import Mager

def analysis_result(struct,ans):
	clocks = struct['mcks'];
	for item in ans:
		for ck in clocks.keys():
			if item == ck:
				clock = clocks[ck];
				if clock.has_key('status'):
					if clock['status']['type'] <> 'delay': return False;
	return True;

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Usage: %s tfile' %sys.argv[0];
		sys.exit(-1);

	try:
		mg = Mager();
		mg.init();
		clocks = mg.modules['Alarm'].fdata;
		dfile = sys.argv[1];
		data = common.read_json(dfile);
		for item in data:
			clocks.clocks.clear();
			clocks.myclock = None;
			for ck in item['init']:
				if clocks.myclock is None: clocks.myclock = ck;
				clocks.clocks[ck['key']] = ck;

			struct = mg.encode(item['test'],'Alarm');
			if item.has_key('print') and item['print'] == 'true':
				res = common.get_dicstr(struct);
				sys.stderr.write(res + '\n');
			if analysis_result(struct,item['ans']) == True:
				sys.stderr.write(item['test'] + ' succ\n')
			else:
				sys.stderr.write(item['test'] + ' failed\n')
				res = common.get_dicstr(struct);
				sys.stderr.write(res + '\n');
				sys.exit(-1)
	except Exception as e:
		raise MyException(sys.exc_info());

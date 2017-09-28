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

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Usage: %s tfile' %sys.argv[0];
		sys.exit(-1);

	try:
		mg = Mager();
		mg.init();

		dfile = sys.argv[1];
		dp = open(dfile,'r');
		for line in dp.readlines():
			line = line.strip('\n').strip('\r').decode('utf8');
			if len(line) == 0 or line[0] == '#':
				continue;
			lline = line.split('\t');
			struct = mg.encode(lline[0],lline[1]);
			common.print_dic(struct);
	except Exception as e:
		raise MyException(sys.exc_info());

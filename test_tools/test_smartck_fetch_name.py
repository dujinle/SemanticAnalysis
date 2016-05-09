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
			debug_type = '';
			for istr in struct['stseg']:
				if struct['stc'].has_key(istr):
					item = struct['stc'][istr];
					debug_type = debug_type + item['stype'];
			if struct.has_key('ck_name'):
				sys.stderr.write(lline[0] + ' ' + struct['ck_name'] + '\n');
			elif struct.has_key('ck_tag'):
				sys.stderr.write(lline[0] + ' ' + struct['ck_tag']['name'] + '\n');
			else:
				sys.stderr.write(lline[0] + '\n');
	except Exception as e:
		raise MyException(sys.exc_info());

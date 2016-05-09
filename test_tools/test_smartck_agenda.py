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
		data = common.read_json(dfile);
		for item in data:
			struct = mg.encode(item['case'],'Alarm');
			if struct.has_key('mcks'):
				ans = item['ans'];
				if struct['mcks'].has_key(ans['key']):
					clock = struct['mcks'][ans['key']];
					if clock['time'] == ans['time'] and int(clock['able']['able']) == int(ans['able']):
						sys.stderr.write(item['case'] + 'succ\n');
						continue;
			sys.stderr.write(item['case'] + 'failed\n');
	except Exception as e:
		raise MyException(sys.exc_info());

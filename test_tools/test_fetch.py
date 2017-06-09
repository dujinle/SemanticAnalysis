#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,codecs
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

	dfile = sys.argv[1];
	try:
		mg = Mager();
		mg.init();
		fp = codecs.open(dfile,'r','utf-8');
		while True:
			line = fp.readline();
			if not line: break;
			if line[0] == '#': continue;
			line = line.strip('\n');
			larr = line.split('\t');
			struct = mg.encode(larr[0],None);
			fetch_type = list();
			for st in struct['stseg']:
				if struct['stc'].has_key(st):
					item = struct['stc'][st];
					fetch_type.append(item['type']);
				else:
					fetch_type.append(st);
			sys.stderr.write(' '.join(struct['stseg']) + '\t' + ' '.join(fetch_type) + '\n');
		fp.close();
	except Exception as e:
		raise MyException(sys.exc_info());

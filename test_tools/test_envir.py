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

def analy(struct,tdir,value):
	if not struct.has_key('result'): return False;
	if struct['result'].has_key('temp'):
		temp = struct['result']['temp'];
		if temp['dir'] == tdir and temp['value'] == value:
			return True;
	elif struct['result'].has_key('volume'):
		temp = struct['result']['volume'];
		if temp['dir'] == tdir and temp['value'] == value:
			return True;
	return False;

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
			line = line.strip('\n').strip('\r');
			larr = line.split('\t');
			struct = mg.encode(larr[0],'Envir');
			if analy(struct,larr[1],larr[2]) == True:
				sys.stderr.write(line + ' succ......\n');
			else:
				sys.stderr.write(line + ' failed......\n');
		fp.close();
	except Exception as e:
		raise MyException(sys.exc_info());

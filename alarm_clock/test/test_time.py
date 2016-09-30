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
sys.path.append(os.path.join(base_path,'../../modules/timer'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
sys.path.append(os.path.join(base_path,'../../modules/mytag'));
sys.path.append(os.path.join(base_path,'../pystr'));
#============================================
import common,config
from time_mager import TimeMager
from tag_mager import MytagMager
from wordseg import WordSeg
from scene_engin import SEngin

def analysis_result(struct,ans):
	if type(ans) == dict:
		key = ans['key'];
		clock = struct['mcks'][key];
		if ans.has_key('time'):
			if ans['time'] == clock['time']:
				return True;
			else:
				return False;
		elif ans.has_key('info'):
			if ans['info'] == clock['info']:
				return True;
			else:
				return False;
		elif ans.has_key('able'):
			if ans['able'] == clock['able']['able']:
				return True;
			else:
				return False;
	elif type(ans) == list:
		for item in ans:
			key = item['key'];
			clock = struct['mcks'][key];
			if item.has_key('time'):
				if item['time'] == clock['time']:
					return True;
				else:
					return False;
			elif item.has_key('info'):
				if item['info'] == clock['info']:
					return True;
				else:
					return False;
			elif item.has_key('able'):
				if item['able'] == clock['able']['able']:
					return True;
				else:
					return False;
	return False;

def del_param(argv):
	ifile = tfile = tmode = '';
	if argv[1] == '-i':
		ifile = argv[2];
	else:
		print 'Usage:%s -i [init] -t [test] -m [mtime|....]' %argv[0];
		sys.exit(-1);
	if argv[3] == '-t':
		tfile = argv[4];
	else:
		print 'Usage:%s -i [init] -t [test] -m [mtime|....]' %argv[0];
		sys.exit(-1);
	if argv[5] == '-m':
		tmode = argv[6];
	else:
		print 'Usage:%s -i [init] -t [test] -m [mtime|....]' %argv[0];
		sys.exit(-1);
	return (ifile,tfile,tmode);

if len(sys.argv) <= 1:
	print 'Usage:%s -i [init] -t [test] -m [mtime|....]' %sys.argv[0];
	sys.exit(-1);

wd = WordSeg();
timer = TimeMager(wd);
tag = MytagMager(wd);
se = SEngin(wd);

se.init('../tdata/');
timer.init('Timer');
tag.init('Mytag');

struct = dict();
struct['result'] = dict();
#params read
ifile,tfile,tmode = del_param(sys.argv);
#init data
ck_list = common.read_json(ifile);
for ck in ck_list:
	se.clocks[ck['key']] = ck;
se.myclock = ck_list[0];
#read test file
tests = common.read_json(tfile);
#start tests
for test in tests:
	struct['text'] = test['test'];
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	if analysis_result(struct,test['ans']) == True:
		print test['test'],'succ';
		if test.has_key('print') and test['print'] == 'true': common.print_dic(struct);
	else:
		print test['test'],'faile';
		common.print_dic(struct);

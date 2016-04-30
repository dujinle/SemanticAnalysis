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
sys.path.append(os.path.join(base_path,'../../modules/prev_deal'));
sys.path.append(os.path.join(base_path,'../pystr'));
#============================================
import common,config
from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from wordseg import WordSeg
from scene_engin import SEngin

def analysis_result(struct,ans):
	if isinstance(ans,dict):
		key = ans['key'];
		clock = struct['mcks'][key];
		if ans.has_key('time'):
			if ans['time'] <> clock['time']:
				return False;
		elif ans.has_key('info'):
			if ans['info'] <> clock['info']:
				return False;
		elif ans.has_key('able'):
			if int(ans['able']) <> int(clock['able']['able']):
				return False;
	elif isinstance(ans,list):
		for item in ans:
			key = item['key'];
			clock = struct['mcks'][key];
			if item.has_key('time'):
				if item['time'] <> clock['time']:
					return False;
			elif item.has_key('info'):
				if item['info'] <> clock['info']:
					return False;
			elif item.has_key('able'):
				if int(item['able']) <> int(clock['able']['able']):
					return False;
	return True;


wd = WordSeg();
timer = TimeMager();
tag = MytagMager();
pdeal = PDealMager();
se = SEngin();

se.init('../tdata/');
timer.init('Timer');
tag.init('Mytag');
pdeal.init('PDeal');

struct = dict();
struct['result'] = dict();
#read test file
tests = common.read_json('./mtime.json');
#start tests
for test in tests:
	se.clocks.clear();
	se.myclock = None;
	for ck in test['init']:
		if se.myclock is None: se.myclock = ck;
		se.clocks[ck['key']] = ck;
	struct['text'] = test['test'];
	struct['inlist'] = wd.tokens(struct['text']);
	pdeal.encode(struct);
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	if analysis_result(struct,test['ans']) == True:
		print test['test'],'succ';
		if test.has_key('print') and test['print'] == 'true': common.print_dic(struct);
	else:
		print test['test'],'faile';
		common.print_dic(struct);
		sys.exit(-1)

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
from time_mager import TimeMager
from tag_mager import MytagMager
from pdeal_mager import PDealMager
from wordseg import WordSeg
from scene_engin import SEngin

def analysis_result(struct,ans):
	if not struct['result'].has_key('clocks'): return False;
	clocks = struct['result']['clocks'];
	for key in ans:
		tag = False
		for ck in clocks:
			if ck['key'] == key:
				tag = True;
				break;
		if tag == False:
			return False;
	return True;

wd = WordSeg();
timer = TimeMager(wd);
tag = MytagMager(wd);
pdeal = PDealMager(wd);
se = SEngin();

se.init('../tdata/');
pdeal.init('PDeal');
timer.init('Timer');
tag.init('Mytag');

struct = dict();
struct['result'] = dict();

tests = common.read_json('./msearch.json');
for test in tests:
	#start tests
	se.clocks.clear();
	se.myclock = None;
	for ck in test['init']:
		if se.myclock is None: se.myclock = ck;
		se.clocks[ck['key']] = ck;
	struct['text'] = test['test'];
	struct['inlist'] = wd.tokens(struct['text']);
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	if analysis_result(struct,test['ans']) == True:
		print test['test'],'succ';
		if test.has_key('print') and test['print'] == 'true':
			common.print_dic(struct);
	else:
		print test['test'],'faile';
		common.print_dic(struct);
		sys.exit(-1);

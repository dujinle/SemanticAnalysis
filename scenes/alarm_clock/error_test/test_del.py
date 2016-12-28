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


wd = WordSeg();
timer = TimeMager(wd);
tag = MytagMager(wd);
pdeal = PDealMager(wd);
se = SEngin(wd);

se.init('../tdata/');
pdeal.init('PDeal');
timer.init('Timer');
tag.init('Mytag');

struct = dict();
struct['result'] = dict();
ck_list = common.read_json('./test.init');
se.clocks.clear();
for ck in ck_list:
	if se.myclock is None: se.myclock = ck_list[ck];
	se.clocks[ck] = ck_list[ck];
while True:
	mstr = raw_input('Enter your input: ');
	if mstr == 'q': break;
	struct['text'] = mstr.decode('utf-8');
	pdeal.encode(struct);
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	common.print_dic(struct);


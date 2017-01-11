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
#============================================
import common,config
from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from wordseg import WordSeg
from scene_engin import SEngin

wd = WordSeg();
timer = TimeMager();
tag = MytagMager();
pdeal = PDealMager();
se = SEngin();

tag.init('Mytag');
pdeal.init('PDeal');
timer.init('Timer');

se.init('../tdata/');
struct = dict();
struct['result'] = dict();
#'''
while True:
	mstr = raw_input('Enter your input: ');
	if mstr == 'q': break;
	struct['text'] = mstr.decode('utf-8');
	struct['inlist'] = wd.tokens(struct['text']);
	pdeal.encode(struct);
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	common.print_dic(struct);
#'''

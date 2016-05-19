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
sys.path.append(os.path.join(base_path,'../'));
sys.path.append(os.path.join(base_path,'../timer'));
sys.path.append(os.path.join(base_path,'../music'));
sys.path.append(os.path.join(base_path,'../wordsegs'));
#============================================
import common,config
from alarm_engin import AEngin
from time_mager import TimeMager
from music_mager import MusicMager
from wordseg import WordSeg
ae = AEngin();
wd = WordSeg();
timer = TimeMager(wd);
music = MusicMager(wd);
timer.init('Timer');
music.init('Music');

ae.init('./tdata');
struct = dict();
struct['result'] = dict();
'''
tstr = u'设一个每周3的闹钟';
struct.update(timer.encode(tstr));
struct.update(music.encode(tstr));
ae.encode(struct);
common.print_dic(struct);
'''
while True:
	mstr = raw_input('Enter your input: ');
	if mstr == 'q': break;
	struct.update(timer.encode(mstr.decode('utf-8')));
	struct.update(music.encode(struct['text']));
	ae.encode(struct);
	common.print_dic(struct);
#'''

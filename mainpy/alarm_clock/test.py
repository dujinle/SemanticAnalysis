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
from alarm_fname import ACname
from time_mager import TimeMager
from music_mager import MusicMager
from wordseg import WordSeg
ae = AEngin();
aname = ACname();
wd = WordSeg();
timer = TimeMager(wd);
timer.init('Timer');
music = MusicMager(wd);
music.init('Music');
aname.load_data('./tdata/ck_name.txt');
ae.init();
while True:
	mstr = raw_input('Enter your input: ');
	if mstr == 'q': break;
	struct = timer.encode(mstr.decode('utf-8'));
	#struct.update(music.encode(mstr));
	ae.encode(struct);
	aname.encode(struct);
	common.print_dic(struct);

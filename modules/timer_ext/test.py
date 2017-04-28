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
#============================================
import common
from time_mager import TimeMager

tmager = TimeMager();
tmager.init();
for lstr in sys.stdin.readlines():
	struct = dict();
	larry = lstr.strip('\n').split('\t');
	struct['text'] = larry[0].decode('utf8');
	tmager.encode(struct);
	common.print_dic(struct);

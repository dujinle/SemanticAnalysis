#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../../modules/timer'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
sys.path.append(os.path.join(base_path,'../../modules/mytag'));
sys.path.append(os.path.join(base_path,'../../modules/prev_deal'));
#==============================================================

import common,config
from common import logging
from scene_engin import SEngin
from scene_replace import SceneReplace
from time_mager import TimeMager
from tag_mager import MytagMager
from pdeal_mager import PDealMager
from wordseg import WordSeg
from myexception import MyException

class SceneMager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager(self.wordseg);
		self.mytag = MytagMager(self.wordseg);
		self.pdeal = PDealMager(self.wordseg);
		self.engine = SEngin(self.wordseg);
		self.struct = collections.OrderedDict();

	def init(self,dtype):
		try:
			fdir = config.dfiles[dtype];
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.pdeal.init('PDeal');
			self.engine.init(fdir);
		except MyException as e: raise e;

	def encode(self,inlist):
		self.struct['text'] = inlist;
		self.struct['result'] = dict();
		try:
			self.pdeal.encode(self.struct);
			self.timer.encode(self.struct);
			self.mytag.encode(self.struct);
			self.engine.encode(self.struct);
			return self.struct;
		except Exception as e:
			logging.error(sys.exc_info()[0]);
			logging.error(sys.exc_info()[1]);
			print sys.exc_info()[0],sys.exc_info()[1];

'''
try:
	mg = SceneMager();
	mg.init('Alarm');
	common.print_dic(mg.encode(u'设置一个闹钟'));
except MyException as e:
	print e.value;
'''

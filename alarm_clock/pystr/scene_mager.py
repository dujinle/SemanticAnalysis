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
#==============================================================

import common,config
from scene_engin import SEngin
from time_mager import TimeMager
from tag_mager import MytagMager
from wordseg import WordSeg

from myexception import MyException

class SceneMager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager(self.wordseg);
		self.mytag = MytagMager(self.wordseg);
		self.engine = SEngin(self.wordseg);
		self.struct = collections.OrderedDict();

	def init(self,dtype):
		try:
			fdir = config.dfiles[dtype];
			print fdir
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.engine.init(fdir);
		except MyException as e: raise e;

	def encode(self,inlist):
		self.struct['text'] = inlist;
		self.struct['result'] = dict();
		try:
			self.timer.encode(self.struct);
			self.mytag.encode(self.struct);
			self.engine.encode(self.struct);
			return self.struct;
		except MyException as e:
			res = common.get_dicstr(self.struct);
			res = e.value + '\n' +res;
			raise MyException(res);

'''
try:
	mg = SceneMager();
	mg.init('Alarm');
	common.print_dic(mg.encode(u'设置一个闹钟'));
except MyException as e:
	print e.value;
'''

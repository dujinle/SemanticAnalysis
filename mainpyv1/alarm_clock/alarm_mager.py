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
sys.path.append(os.path.join(base_path,'../'));
sys.path.append(os.path.join(base_path,'../timer'));
sys.path.append(os.path.join(base_path,'../music'));
#==============================================================

import common,config
from alarm_engin import AEngin
from time_mager import TimeMager
from music_mager import MusicMager

from myexception import MyException

class AlarmMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.timer = TimeMager(wordseg);
		self.music = MusicMager(wordseg);
		self.engine = AEngin();

	def init(self,dtype):
		try:
			fdir = config.dfiles[dtype];
			self.timer.init('Timer');
			self.music.init('Music');
			self.engine.init(fdir);
		except MyException as e: raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		struct['result'] = dict();
		try:
			struct.update(self.timer.encode(struct['text']));
			struct.update(self.music.encode(struct['text']));
			self.engine.encode(struct);
			return struct;
		except MyException as e:
			res = common.get_dicstr(struct);
			res = e.value + '\n' +res;
			raise MyException(res);

'''
try:
	sys.path.append('../wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = AlarmMager(wordseg);
	mg.init('Alarm');
	common.print_dic(mg.encode(u'设置一个闹钟'));
except MyException as e:
	print e.value;
'''

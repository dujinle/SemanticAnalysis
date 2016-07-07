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
#==============================================================

import common,config
from alarm_action import AA
from alarm_engin import AE
from time_mager import TimeMager


#from calc_time import CalcTimeInterval
from myexception import MyException

class AlarmMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.clocks = dict();
		self.timer = TimeMager(wordseg);

		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(AA());
		self.tag_objs.append(AE());

	def init(self,dtype):
		try:
			step = 1;
			self.timer.init('Timer');
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except MyException as e: raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		try:
			struct.update(self.timer.encode(inlist));
			if not struct.has_key('inlist'):
				struct['inlist'] = self.wordseg.tokens(inlist);
			for obj in self.tag_objs:
				obj.init();
				obj.encode(struct);
			return struct;
		except MyException as e:
			res = common.get_dicstr(struct);
			res = e.value + '\n' +res;
			raise MyException(res);

	def deal_data(self,fname,action,data):
		try:
			for obj in self.tag_objs:
				ret = obj.deal_data(fname,action,data);
				if ret == common.PASS:
					continue;
				elif not ret is None:
					return ret;
		except MyException as e:
			raise e;

	def write_file(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.write_file(dfiles[str(step)]);
				step = step + 1;
		except MyException as e:
			raise e;
#'''
try:
	sys.path.append('../wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = AlarmMager(wordseg);
	mg.init('Alarm');
	common.print_dic(mg.encode(u'增加一个5点40分的闹钟,调晚一点'));
except MyException as e:
	print e.value;
#'''

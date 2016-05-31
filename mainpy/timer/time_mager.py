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
#==============================================================

import common,config
from time_interval import NT
from time_interval import UT
from time_interval import CT
from time_interval import TF
from time_week import TW
from time_week import TWE

from time_mood import TM
from time_mood import TS
from time_mood import AS

from calc_time import CalcTimeInterval
from myexception import MyException

class TimeMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(UT());
		self.tag_objs.append(NT());
		self.tag_objs.append(CT());
		self.tag_objs.append(TW());
		self.tag_objs.append(TWE());

		self.tag_objs.append(TF());
		self.tag_objs.append(CalcTimeInterval());
		#self.tag_objs.append(TimeMood());
		#self.tag_objs.append(TimeStatus());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except MyException as e: raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		try:
			struct['inlist'] = self.wordseg.tokens(inlist);
			struct['taglist'] = list();
			struct['taglist'].extend(struct['inlist']);
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
'''
try:
	sys.path.append('../wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = TimeMager(wordseg);
	mg.init('Timer');
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	wordseg.deal_word('del',{'value':u'天上'});
	wordseg.deal_word('del',{'value':u'午前'});
	#common.print_dic(mg.encode(u'3月4号上午前'));
	#common.print_dic(mg.encode(u'明天'));
	common.print_dic(mg.encode(u'周3'));
except MyException as e:
	print e.value;
'''

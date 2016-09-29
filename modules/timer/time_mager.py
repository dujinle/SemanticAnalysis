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

import common,config,time_common
from time_normal import TNormal,TBucket
from time_week import TWeek
from time_festival import TFestival,TEFestival
from time_solarterm import TSolarTerm
from time_decade import TDecade
from time_front import TFront
from time_tail import TTail
from time_replace import TReplace
from time_mood import TMood
from myexception import MyException


class TimeMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();
		self.tail = TTail();

		# mark tag objs #
		self.tag_objs.append(TReplace());
		self.tag_objs.append(TFront());
		self.tag_objs.append(TNormal());
		self.tag_objs.append(TBucket());
		self.tag_objs.append(TWeek());

		self.tag_objs.append(TFestival());
		self.tag_objs.append(TEFestival());
		self.tag_objs.append(TSolarTerm());
		self.tag_objs.append(TDecade());
		self.tag_objs.append(TMood());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except MyException as e: raise e;

	def encode(self,struct):
		struct['intervals'] = list();
		struct['mood'] = list();
		struct['my_inter_id'] = 0;
		struct['step_id'] = 0;
		try:
			cur_status = False;
			while True:
				if struct['step_id'] >= len(struct['text']):
					if cur_status == True: self.tail.encode(struct);
					break;
				ret = 0;
				for obj in self.tag_objs:
					obj.init();
					ret += obj.encode(struct);
					if struct['step_id'] >= len(struct['text']): break;
				if ret == -9:
					if cur_status == True:
						cur_status = False;
						self.tail.encode(struct);
						struct['my_inter_id'] = struct['my_inter_id'] + 1;
					struct['step_id'] = struct['step_id'] + 1;
				else: cur_status = True;
			if struct.has_key('step_id'): del struct['step_id'];
			if struct.has_key('my_inter_id'): del struct['my_inter_id'];
			if struct.has_key('scope'): del struct['scope'];
			if struct.has_key('prev_func'): del struct['prev_func'];
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
	#common.print_dic(mg.encode(u'14点15分30秒'));
	#common.print_dic(mg.encode(u'凌晨'));
	common.print_dic(mg.encode(u'7点一刻'));
	#common.print_dic(mg.encode(u'今年中秋节'));
	#common.print_dic(mg.encode(u'下午2点30分'));
	#common.print_dic(mg.encode(u'上周末'));
except MyException as e:
	print e.value;
'''

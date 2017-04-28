#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common,config,time_common
from time_normal import TNormal,TBucket
from time_week import TWeek
from time_festival import TFestival,TEFestival
from time_solarterm import TSolarTerm
from time_decade import TDecade
from time_front import TFront
from time_tail import TTail
from time_replace import TReplace
from myexception import MyException


class TimeMager:
	def __init__(self):
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

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except Exception as e:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		struct['intervals'] = list();
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
				if ret == -8:
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
		except Exception as e:
			raise MyException(sys.exc_info());

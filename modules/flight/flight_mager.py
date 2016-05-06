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
sys.path.append(os.path.join(base_path,'../location'));
sys.path.append(os.path.join(base_path,'../timer'));
#==============================================================

import common,config
from flight import Flight
from airline import AIR
from time_mager import TimeMager
from local_mager import LocalMager

from myexception import MyException

class FlightMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.timer = TimeMager(wordseg);
		self.local = LocalMager(wordseg);
		self.flight = Flight();
		self.airline = AIR();

	def init(self,dtype):
		self.timer.init('Timer');
		self.local.init('Local');
		dfiles = config.dfiles[dtype];
		self.flight.init(dfiles['1']);
		self.airline.init(dfiles['2']);

	def encode(self,inlist):
		try:
			struct = self.timer.encode(inlist);
			if not struct is None:
				ret = self.local.encode(struct['text']);
				if not ret is None: struct.update(ret);
				self.flight.encode(struct);
				self.airline.encode(struct);

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
	mg = FlightMager(wordseg);
	mg.init('Flight');
	#mg.write_file();
	#wordseg.deal_word('add',{'value':u'翠微路'});
	common.print_dic(mg.encode(u'明天去上海的国际航空航班GS2034最早的'));
except MyException as e:
	print e.value;
'''

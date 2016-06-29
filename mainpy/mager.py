#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);

sys.path.append(os.path.join(base_path,'./voice'));
sys.path.append(os.path.join(base_path,'./temperature'));
sys.path.append(os.path.join(base_path,'./timer'));
sys.path.append(os.path.join(base_path,'./location'));
sys.path.append(os.path.join(base_path,'./flight'));
sys.path.append(os.path.join(base_path,'./catering'));
sys.path.append(os.path.join(base_path,'./music'));
sys.path.append(os.path.join(base_path,'./wordsegs'));
sys.path.append(os.path.join(base_path,'../commons'));
#==============================================================

from wordseg import WordSeg
import common,config
from myexception import MyException
from voice_mager import VoiceMager
from temp_mager import TempMager
from time_mager import TimeMager
from local_mager import LocalMager
from music_mager import MusicMager
from catering_mager import CateringMager
from flight_mager import FlightMager

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.modules = dict();
		self.modules['Voice'] = VoiceMager(self.wordseg);
		self.modules['Temp'] = TempMager(self.wordseg);
		self.modules['Timer'] = TimeMager(self.wordseg);
		self.modules['Local'] = LocalMager(self.wordseg);
		self.modules['Music'] = MusicMager(self.wordseg);
		self.modules['Catering'] = CateringMager(self.wordseg);
		self.modules['Flight'] = FlightMager(self.wordseg);

	def init(self):
		try:
			for key in self.modules:
				self.modules[key].init(key);
		except MyException as e:
			raise e;

	def encode(self,inlist,mdl):

		struct = collections.OrderedDict();
		module = config.dtype;
		if not mdl is None: module = mdl;

		try:
			mobj = self.modules[module];
			return mobj.encode(inlist);
		except MyException as e:
			raise e;

	def deal_data(self,mdl,fname,action,data):
		module = config.dtype;
		if not mdl is None: module = mdl;

		try:
			mobj = self.modules[module];
			res = mobj.deal_data(fname,action,data);
			return res;
		except MyException as e:
			raise e;

	def sp_deal(self,action,word):
		if self.wordseg is None:
			raise MyException('the word seg obj is none');
		try:
			self.wordseg.deal_word(action,word);
		except MyException as e:
			raise e;

	def write_file(self,mdl):

		module = config.dtype;
		if not mdl is None: module = mdl;
		try:
			mobj = self.modules[module];
			mobj.write_file(module);
			self.wordseg.write_file();
		except MyException as e:
			raise e;
'''
try:
	mg = Mager();
	mg.init();
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	#mg.sp_deal('del',{'value':u'大点'});
	common.print_dic(mg.encode(u'明天上午到上地七街的机票','Flight'));
	#mg.sp_deal('del',{'value':u'静音'});
	#mg.deal_data('M','add',{'value':u'音'});
	#common.print_dic(mg.encode(u'静音'));
	#mg.sp_deal('del',{'value':u'最大声'});
	#common.print_dic(mg.encode(u'大点声'));
except MyException as e:
	print e.value;
'''

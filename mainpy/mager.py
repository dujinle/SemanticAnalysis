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
sys.path.append(os.path.join(base_path,'./wordsegs'));
sys.path.append(os.path.join(base_path,'../commons'));
#==============================================================

from wordseg import WordSeg
import common,config
from myexception import MyException
from voice_mager import VoiceMager

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.modules = dict();
		self.modules['Voice'] = VoiceMager(self.wordseg);

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
	common.print_dic(mg.encode(u'把声音调到最大','Voice'));
	#mg.sp_deal('del',{'value':u'静音'});
	#mg.deal_data('M','add',{'value':u'音'});
	#common.print_dic(mg.encode(u'静音'));
	#mg.sp_deal('del',{'value':u'最大声'});
	#common.print_dic(mg.encode(u'大点声'));
except MyException as e:
	print e.value;
'''

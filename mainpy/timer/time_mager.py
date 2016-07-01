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
from time_ut import UT
from time_ut import UTE
from time_ut import CUTE
from time_nt import NT
from time_nt import NTE
from time_nt import CNTE
from time_wt import WT
from time_wt import WTE
from time_wt import CWTE
from time_qt import QT
from time_qt import CQT
from time_allt import ALLT
from time_allt import CALLT
from time_mood import TM
from time_mood import TS
from time_mood import AS


#from calc_time import CalcTimeInterval
from myexception import MyException

class TimeMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(UT());
		self.tag_objs.append(NT());
		self.tag_objs.append(WT());
		self.tag_objs.append(QT());

		self.tag_objs.append(UTE());
		self.tag_objs.append(NTE());
		self.tag_objs.append(WTE());
		self.tag_objs.append(ALLT());

		self.tag_objs.append(CUTE());
		self.tag_objs.append(CNTE());
		self.tag_objs.append(CWTE());
		self.tag_objs.append(CQT());
		self.tag_objs.append(CALLT());
		self.tag_objs.append(TM());
		self.tag_objs.append(TS());
		self.tag_objs.append(AS());

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
	mg = TimeMager(wordseg);
	mg.init('Timer');
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	#wordseg.deal_word('del',{'value':u'天上'});
	#wordseg.deal_word('del',{'value':u'午前'});
	#common.print_dic(mg.encode(u'14点15分30秒'));
	#common.print_dic(mg.encode(u'凌晨'));
	#common.print_dic(mg.encode(u'下周3上午'));
	#common.print_dic(mg.encode(u'下周3上午'));
	common.print_dic(mg.encode(u'3小时前'));
	#common.print_dic(mg.encode(u'下午2点30分'));
	#common.print_dic(mg.encode(u'上周末'));
except MyException as e:
	print e.value;
#'''

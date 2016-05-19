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
#==============================================================

import common,config
from myexception import MyException
from marktag import M,C,F,X
from extendtag import X1,M1,F1,Z
from checktag import PM
from calctag import Calc

class TimeMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(M());
		self.tag_objs.append(C());
		self.tag_objs.append(F());
		self.tag_objs.append(X());
		# extend tag objs #
		self.tag_objs.append(X1());
		self.tag_objs.append(M1());
		self.tag_objs.append(F1());
		self.tag_objs.append(Z());
		# calc tag obj #
		self.tag_objs.append(PM());
		self.tag_objs.append(Calc());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except MyException as e:
			raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		struct['taglist'] = list();
		try:
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
'''
try:
	sys.path.append('../wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = VoiceMager(wordseg);
	mg.init('Voice');
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	#mg.sp_deal('del',{'value':u'大点'});
	common.print_dic(mg.encode(u'声音太吵了'));
	#mg.sp_deal('del',{'value':u'静音'});
	#mg.deal_data('M','add',{'value':u'音'});
	#common.print_dic(mg.encode(u'静音'));
	#mg.sp_deal('del',{'value':u'最大声'});
	#common.print_dic(mg.encode(u'大点声'));
	#common.print_dic(mg.encode(u'再整点'));
except MyException as e:
	print e.value;
'''

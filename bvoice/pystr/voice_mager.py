#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common,config
from myexception import MyException
from marktag import M,C,F,X
from extendtag import X1,M1,F1,Z
from checktag import PM
from calctag import Calc

class VoiceMager:
	def __init__(self):
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
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			struct['taglist'] = list();
			for obj in self.tag_objs:
				obj.init();
				obj.encode(struct);
			del struct['taglist'];
			if struct.has_key('F1'): del struct['F1'];
			if struct.has_key('reg'): del struct['reg'];
		except Exception as e:
			raise e;

	def deal_data(self,fname,action,data):
		try:
			for obj in self.tag_objs:
				ret = obj.deal_data(fname,action,data);
				if ret == common.PASS:
					continue;
				elif not ret is None:
					return ret;
		except Exception as e:
			raise e;

	def write_file(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.write_file(dfiles[str(step)]);
				step = step + 1;
		except Exception as e:
			raise e;
'''
try:
	sys.path.append('../modules/wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = VoiceMager(wordseg);
	mg.init('Voice');
	struct = dict();
	struct['text'] = u'连一点声音都没有';
	struct['inlist'] = wordseg.tokens(struct['text']);
	struct['taglist'] = list();
	mg.encode(struct);
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	common.print_dic(struct);
	#mg.deal_data('M','add',{'value':u'音'});
	#common.print_dic(mg.encode(u'静音'));
	#mg.sp_deal('del',{'value':u'最大声'});
	#common.print_dic(mg.encode(u'大点声'));
	#common.print_dic(mg.encode(u'再整点'));
except Exception as e:
	raise e;
'''

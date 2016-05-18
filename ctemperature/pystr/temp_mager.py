#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common,config
from myexception import MyException
from marktag import M,C,F,X
from numtag import Nt
from extendtag import X1,M1,F1,Z
from checktag import PM
from calctag import Calc

class TempMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(M());
		self.tag_objs.append(C());
		self.tag_objs.append(F());
		self.tag_objs.append(X());
		self.tag_objs.append(Nt());
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

	def encode(self,struct):
		try:
			struct['taglist'] = list();
			for obj in self.tag_objs:
				obj.init();
				obj.encode(struct);
			del struct['taglist'];
			if struct.has_key('F1'): del struct['F1'];
			if struct.has_key('reg'): del struct['reg'];
		except Exception as e: raise e;

	def deal_data(self,fname,action,data):
		try:
			print fname,action,data;
			for obj in self.tag_objs:
				ret = obj.deal_data(fname,action,data);
				if ret == common.PASS:
					continue;
				elif not ret is None: return ret;
		except Exception as e: raise e;

	def write_file(self,mdl):
		try:
			step = 1;
			dfiles = config.dfiles[mdl];
			for obj in self.tag_objs:
				obj.write_file(dfiles[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

'''
try:
	sys.path.append('../../modules/wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();

	mg = TempMager(wordseg);
	mg.init('Temp');
	struct = dict();
	struct['text'] = u'空调调到25度';
	struct['taglist'] = list();
	struct['inlist'] = wordseg.tokens(struct['text']);
	mg.encode(struct);
	common.print_dic(struct);
except Exception as e:
	raise e;
'''

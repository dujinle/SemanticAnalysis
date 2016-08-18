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
from CTR import CTR
from CAT import CAT

from myexception import MyException

class CateringMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(CTR());
		self.tag_objs.append(CAT());

	def init(self,dtype):
		try:
			step = 1;
			fdirs = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.init(fdirs[str(step)]);
				step = step + 1;
		except MyException as e: raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		try:
			struct['inlist'] = self.wordseg.tokens(inlist);
			struct['catering'] = struct['inlist'][:];
			for obj in self.tag_objs:
				obj.encode(struct);
			return struct;
		except MyException as e:
			res = common.get_dicstr(struct);
			res = e.value + '\n' +res;
			raise MyException(res);

	def deal_data(self,fname,action,data):
		try:
			ret = obj = None;
			obj = self.tag_objs[0];

			if action == 'add':
				ret = obj._add(data);
			elif action == 'del':
				ret = obj._del(data);
			elif action == 'get':
				ret = obj._get(None);
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
	mg = CateringMager(wordseg);
	mg.init('Catering');
	#mg.write_file();
	wordseg.deal_word('add',{'value':u'四川菜'})
	#common.print_dic(mg.encode(u'来一首王菲的歌'));
	common.print_dic(mg.encode(u'四川菜'));
except MyException as e:
	print e.value;
'''

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
sys.path.append(os.path.join(base_path,'./'));
#==============================================================

import common,config
from pdeal_replace import PDealReplace
from myexception import MyException

class PDealMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(PDealReplace());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs: obj.encode(struct);
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
	mg = PDealMager(wordseg);
	mg.init('PDeal');
	struct = dict();
	struct['text'] = u'8点提醒我回忆';
	common.print_dic(mg.encode(struct));
except MyException as e:
	print e.value;
'''

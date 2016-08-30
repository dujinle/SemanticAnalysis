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
from mytag_encode import MyTagEncode

from myexception import MyException

class MytagMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MyTagEncode());

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
			for obj in self.tag_objs:
				obj.encode(struct);
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
	mg = MytagMager(wordseg);
	mg.init('Mytag');
	#mg.write_file();
	common.print_dic(mg.encode(u'来一首笨小孩'));
	#common.print_dic(mg.encode(u'来一首纯音乐'));
except MyException as e:
	print e.value;
'''

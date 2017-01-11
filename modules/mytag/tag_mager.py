#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
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
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
			return struct;
		except Exception as e:
			raise e;

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

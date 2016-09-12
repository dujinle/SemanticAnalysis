#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#==============================================================

import common,config,hanzi2num
from common import MyException

class PrevMager:

	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.regs = u'[一二三四五六七八九十零]{1,}';

	def init(self,dtype): pass;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		mats = re.findall(self.regs,struct['text']);
		for mstr in mats:
			numstr = str(hanzi2num.cn2dig(mstr));
			struct['text'] = struct['text'].replace(mstr,numstr,1);
		return struct;
'''
try:
	sys.path.append('../wordsegs');
	from wordseg import WordSeg
	wordseg = WordSeg();
	mg = PrevMager(wordseg);
	mg.init(None);
	#mg.write_file();
	common.print_dic(mg.encode(u'八点四十分'));
except MyException as e:
	print e.value;
'''

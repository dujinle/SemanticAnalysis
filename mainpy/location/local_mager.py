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
from AD import AD
from CM import CM
from CR import CR
from CELL import CELL


from myexception import MyException

class LocalMager:
	def __init__(self,wordseg):
		self.wordseg = wordseg;
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(AD());
		self.tag_objs.append(CM());
		self.tag_objs.append(CR());
		self.tag_objs.append(CELL());

	def init(self,dtype):
		try:
			step = 1;
			fdirs = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.init(fdirs[str(step)]);
		except MyException as e: raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		try:
			struct['inlist'] = self.wordseg.tokens(inlist);
			struct['locals'] = struct['inlist'][:];
			for obj in self.tag_objs:
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
	mg = LocalMager(wordseg);
	mg.init('Local');
	#mg.write_file();
	wordseg.deal_word('add',{'value':u'翠微路'});
	wordseg.deal_word('add',{'value':u'交叉路口'});
	wordseg.deal_word('add',{'value':u'家属楼'});
	wordseg.deal_word('del',{'value':u'路与'});
	common.print_dic(mg.encode(u'海淀西二旗七贤村家属楼'));
except MyException as e:
	print e.value;
'''

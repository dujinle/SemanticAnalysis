#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
abspath = os.path.abspath(__file__);
base_path = os.path.split(abspath)[0];

sys.path.append(base_path + '/tagpy');
sys.path.append(base_path + '/wordsegs');
sys.path.append(base_path + '/../commons');
#==============================================================

from wordseg import WordSeg
import common
import config
from myexception import MyException
from marktag import M
from marktag import C
from marktag import F
from marktag import X
from extendtag import X1
from extendtag import M1
from extendtag import F1
from extendtag import Z
from checktag import PM
from calctag import Calc

#@common.singleton
class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
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

	def sp_deal(self,action,word):
		if self.wordseg is None:
			raise MyException('the word seg obj is none');
		try:
			self.wordseg.deal_word(action,word);
		except MyException as e:
			raise e;

	def write_file(self):
		try:
			step = 1;
			dfiles = config.dfiles[config.dtype];
			for obj in self.tag_objs:
				obj.write_file(dfiles[str(step)]);
				step = step + 1;
			self.wordseg.write_file();
		except MyException as e:
			raise e;
'''
try:
	mg = Mager();
	mg.init('Voice');
	#mg.write_file();
	#common.print_dic(mg.encode(u'把声音调大点'));
	#mg.sp_deal('del',{'value':u'大点'});
	common.print_dic(mg.encode(u'把声音调到最大'));
except MyException as e:
	print e.value;
'''

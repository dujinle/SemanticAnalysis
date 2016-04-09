#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding('utf-8');
import collections
import config

sys.path.append('./pstr');
sys.path.append('./wordsegs');
from wordseg import WordSeg
import common
from M import M
from C import C
from F import F
from X import X
from PM import PM
from T import T
from calc import Calc
from toolbox import ToolBox
class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.objs = list();
		self.objs.append(M());
		self.objs.append(C());
		self.objs.append(F());
		self.objs.append(X());
		self.objs.append(T());
		self.objs.append(PM());
		self.objs.append(Calc());
		self.objs.append(ToolBox());

	def init(self):
		try:
			step = 1;
			for obj in self.objs:
				obj.load_data(config.dfiles[str(step)]);
				step = step + 1;
		except Exception as e:
			raise e;

	def encode(self,inlist):
		struct = collections.OrderedDict();
		struct['text'] = inlist;
		try:
			struct['inlist'] = self.wordseg.tokens(inlist);
			for obj in self.objs:
				obj.encode(struct);
			common.print_dic(struct);
		except Exception as e:
			raise e;
mg = Mager();
mg.init();
mg.encode(u'声音太大了');

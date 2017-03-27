#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'./commons'));

#==============================================================

import common,config
from myexception import MyException
from modules import *
from scenes import *

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager();
		self.mytag = TagMager();
		self.pdeal = PDealMager();
		self.concpt = ConMager();
		self.dist = DistMager();
		self.wsvd = WsvdMager();

		self.struct = collections.OrderedDict();
		self.modules = dict();
		self.modules['News'] = NewsMager();
		self.modules['Guide'] = GuideMager();

	def set_step(self,step): self.struct['step'] = step;
	def set_scene(self,scene):
		common.print_dic(self.struct);
		self.struct['scene'] = scene;

	def init(self):
		try:
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.pdeal.init('PDeal');
			self.concpt.init('Concept');
			self.dist.init('Dist');
			for key in self.modules:
				self.modules[key].init();
		except Exception as e:
			raise MyException(sys.exc_info());

	def _clear_struct(self,struct):
		idx = 0;
		while True:
			if idx >= len(struct.keys()): break;
			key = struct.keys()[idx];
			if key == 'step' or key == 'scene':
				idx = idx + 1;
				continue;
			else:
				del struct[key];
				continue;

	def encode(self,text,mdl = None):
		self._clear_struct(self.struct);
		self.struct['text'] = text;
		self.pdeal.encode(self.struct);
		self.struct['inlist'] = self.wordseg.tokens(self.struct['text']);
		self.struct['otext'] = self.struct['text'];
		self.struct['result'] = dict();

		self.timer.encode(self.struct);
		self.mytag.encode(self.struct);
		self.concpt.encode(self.struct);
		self.wsvd.encode(self.struct);
		if not mdl is None:
			self.struct['scene'] = mdl;
		elif not self.struct.has_key('scene'):
			self.dist.encode(self.struct);
		if self.struct.has_key('scene'):
			mdl = self.struct['scene'];
			print 'get scene:',self.struct['scene'];
#		'''
#		self.struct['step'] = 'which';
		if self.modules.has_key(mdl):
			self.struct['text'] = self.struct['otext'];
			mobj = self.modules[mdl];
			mobj.encode(self.struct);
		if self.struct.has_key('step') and self.struct['step'] == 'end':
			del self.struct['scene'];
			del self.struct['step'];
#		'''
		return self.struct;

#'''
try:
	mg = Mager();
	mg.init();
	while True:
		istr = raw_input("raw_input: ");
		if istr == 'q' or istr == 'bye': break;
		print istr;
		sarr = istr.decode('utf8').split(' ');
		if len(sarr) == 2:
			common.print_dic(mg.encode(sarr[0],sarr[1]));
		else:
			common.print_dic(mg.encode(sarr[0],None));
except Exception as e:
	raise e;
#'''

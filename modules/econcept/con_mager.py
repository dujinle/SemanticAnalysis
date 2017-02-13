#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from mark_num import MarkNum
from mark_objs import MarkObjs
from mark_pronoun import MarkPronoun
from mark_tmood import MarkTmood

import struct_utils as Sutil

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data,'SomeObjs'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeAdj'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeVerb'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeAux'));		#标记助词
		self.tag_objs.append(MarkObjs(self.net_data,'SomeUnits'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeOther'));
		self.tag_objs.append(MarkNum(self.net_data,'SomeNums'));
		self.tag_objs.append(MarkTmood(self.net_data,'SomeTmood'));
		self.tag_objs.append(MarkPronoun(self.net_data,'SomePronoun'));	#标记代词
		self.tag_objs.append(MarkPronoun(self.net_data,'SomeSpace'));	#标记方位词
		self.tag_objs.append(MarkPronoun(self.net_data,'SomeAdverb'));	#标记副词

	def init(self,dtype):
		try:
			self.net_data.load_data();
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			struct['merg'] = list();
			self._fetch_time(struct);
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;

	def _fetch_time(self,struct):
		if not struct.has_key('intervals'): return None;
		struct['Times'] = list();
		for inter in struct['intervals']:
			istr = inter['str'].replace('_','');
			Sutil._merge_some_words(struct,istr,0);
			inter['stype'] = 'TIME';
			inter['type'] = 'TIME';
			inter['str'] = istr;
			struct['Times'].append(inter);
			struct['text'] = struct['text'].replace(istr,'',1);

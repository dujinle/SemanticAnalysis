#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from mark_objs import MarkObjs

import struct_utils as Sutil

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data,'SomeNouns'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeAuxs'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeVerbs'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeMoods'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeProns'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeTenses'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeLogics'));

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
			#struct['text'] = struct['text'].replace(istr,'',1);
		del struct['intervals'];

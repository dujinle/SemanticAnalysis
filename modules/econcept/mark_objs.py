#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
from myexception import MyException
import struct_utils as Sutil
#标记对象名词以及链接的网络
class MarkObjs():
	def __init__(self,net_data):
		self.net_data = net_data;

	def encode(self,struct):
		try:
			if not struct.has_key('Objs'): struct['Objs'] = list();
			if not struct.has_key('Verbs'): struct['Verbs'] = list();
			self._mark_objs(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs(self,struct):
		noun = self.net_data.get_noun_net();
		vbs = self.net_data.get_verb_net();
		idx = 0;
		while True:
			if idx >= len(struct['text']): break;
			strs = struct['text'][idx:];
			wd = '';
			for word in list(strs):
				wd = wd + word;
				if noun.has_key(wd):
					wc = noun[wd];
					struct['Objs'].append(wc);
					idx = idx + len(wd) - 1;
					wd = '';
					break;
				elif vbs.has_key(wd):
					wc = vbs[wd];
					struct['Verbs'].append(wc);
					idx = idx + len(wd) - 1;
					wd = '';
					break;
			idx = idx + 1;

		#把连续的动词合并为一个词,这里是因为分词的不理想导致动词的分开
		Sutil._merge_cont_tag(struct,'Verbs');
		tid = 0;
		for verb in struct['Verbs']:
			if verb['str'] in struct['inlist']:
				continue;
			tid = Sutil._merge_some_words(verb['str'],tid);

#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

#标记介词
class MarkPrep():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			self._mark_prep(struct);
			Sutil._link_split_words(struct,self.key);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_prep(self,struct):
		data = self.net_data.get_data_key(self.key);
		if data is None: return None;

		for key in data.keys():
			item = data[key];
			for it in item:
				comp = re.compile(it['reg']);
				match = comp.search(struct['text']);
				if not match is None:
					tdic = dict();
					tdic['str'] = match.group(0);
					tdic['type'] = it['type'];
					if it.has_key('stype'):
						tdic['stype'] = it['stype'];
					else:
						tdic['stype'] = key;
					struct[self.key].append(tdic);


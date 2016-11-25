#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
import struct_utils as Sutil
#标记对象名词以及链接的网络
class MarkObjs():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			self._mark_objs(struct);
			Sutil._link_split_words(struct,self.key);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs(self,struct):
		data = self.net_data.get_data_key(self.key);
		if data is None: return None;
		idx = 0;
		while True:
			if idx >= len(struct['text']): break;
			strs = struct['text'][idx:];
			wd = '';
			for word in list(strs):
				wd = wd + word;
				if data.has_key(wd):
					tdic = data[wd];
					idx = idx + len(wd) - 1;
					struct[self.key].append(tdic);
					wd = '';
					break;
			idx = idx + 1;

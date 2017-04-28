#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
#标记对象以及链接的网络
class MarkObjs():

	def load_data(self,dfile): pass;

	def encode(self,struct,key,data):
		try:
			if not struct.has_key(key): struct[key] = list();
			self._mark_objs_text(struct,key,data);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs_text(self,struct,key,data):
		try:
			mdata = data.get_data_key(key);
			if mdata is None: return None;

			for item in mdata:
				comp = re.compile(item['reg']);
				match = comp.search(struct['text']);
				if match is None: continue;
				tdic = dict(item);
				tdic['str'] = match.group();
				struct[key].append(tdic);
		except Exception as e:
			raise MyException(sys.exc_info());

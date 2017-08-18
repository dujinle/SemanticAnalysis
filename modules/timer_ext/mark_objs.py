#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
#标记对象以及链接的网络
class MarkObjs():

	def __init__(self): self.text = None;

	def init(self): self.text = None;

	def load_data(self,dfile): pass;

	def encode(self,struct,key,data):
		try:
			if self.text is None: self.text = struct['text'];
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

				amatch = re.findall(item['reg'],self.text);
				for tstr in amatch:
					if len(tstr) == 0: continue;
					tdic = dict(item);
					tdic['str'] = tstr;
					struct[key].append(tdic);
					self.text = self.text.replace(tstr,'TIME');
		except Exception as e:
			raise MyException(sys.exc_info());

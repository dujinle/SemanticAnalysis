#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

class FetchBelongs():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self._fetch_belong(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_belong(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				it['key'] = key;
				self._merge_objs(struct,it);

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['start']): return None;
		if not struct.has_key(item['end']): return None;

		pid = tid = 0;
		while True:
			if pid >= len(struct[item['start']]): break;
			pit = struct[item['start']][pid];
			tid = 0;
			while True:
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				pstr = pit['str'] + item['desc'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					vit[item['key']] = pit;
					del struct[item['start']][pid];
					pid = pid - 1;
				tid = tid + 1;
			pid = pid + 1;

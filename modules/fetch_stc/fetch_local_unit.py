#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#方位词和单位词组组合
class FetchLocalUnit():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			if not struct.has_key('Lunit'): struct['Lunit'] = list();
			self._fetch_lunit(struct);
			Sutil._link_split_words(struct,'Lunit');
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_lunit(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			item['key'] = key;
			self._fetch_local_unit(struct,item);

	def _fetch_local_unit(self,struct,item):
		pid = tid = 0;
		while True:
			if pid >= len(struct[item['start']]): break;
			pit = struct[item['start']][pid];
			tid = 0;
			while True:
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				pstr = pit['str'] + vit['str'];
				if struct['text'].find(pstr) <> -1:
					tdic = dict();
					tdic['str'] = pstr;
					tdic['stype'] = pit['stype'] + vit['stype'];
					tdic['type'] = item['key'];
					tdic['stc'] = [pit,vit];
					struct['Lunit'].append(tdic);
					del struct[item['end']][tid];
					del struct[item['start']][pid];
					pid = pid - 1;
					break;
				tid = tid + 1;
			pid = pid + 1;


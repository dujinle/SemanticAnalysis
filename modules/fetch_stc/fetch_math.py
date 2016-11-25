#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
import struct_utils as Sutil

#标记数学计算数据
class FetchMath():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			if not struct.has_key('Math'): struct['Math'] = list();
			self._mark_objs(struct);
			self._fetch_math(struct);
			Sutil._link_split_words(struct,'Math');
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs(self,struct):
		Math = self.data;
		idx = 0;
		while True:
			if idx >= len(struct['text']): break;
			strs = struct['text'][idx:];
			wd = '';
			for word in list(strs):
				wd = wd + word;
				tdic = self._get_words_type(wd,Math);
				if not tdic is None:
					struct['Math'].append(tdic);
					idx = idx + len(wd) - 1;
					wd = '';
					break;
			idx = idx + 1;

	def _get_words_type(self,words,data):
		if data.has_key(words):
			tdic = dict(data[words]);
			tdic['type'] = 'Math';
			return tdic;
		return None;

	def _fetch_math(self,struct):
		for math in struct['Math']:
			pstr = math['reg'];
			nlist = list();
			rlist = list();
			tid = pid = 0;
			while True:
				tid = pid;
				if tid >= len(struct['Nums']): break;
				while True:
					if pstr.find('NUM') == -1: break;
					if tid >= len(struct['Nums']): break;
					it = struct['Nums'][tid];
					nlist.append(it);
					rlist.append(it);
					pstr = pstr.replace('NUM',it['str'],1);
					del struct['Nums'][tid];
				if struct['text'].find(pstr) <> -1:
					math['nums'] = nlist;
					del math['reg'];
					nlist = list();
					break;
				else:
					rlist.extend(struct['Nums']);
					struct['Nums'] = rlist;
					rlist = list();
					pid = pid + 1;
					nlist = list();

#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#抓取动词与特殊词之间的关系 并标注
class FetchVerbStc():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self._fetch_verbs(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_verbs(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				self._fetch_true(struct,it['reg'],'Verbs',it['pos'],key);

	def _fetch_true(self,struct,reg,objs_key,pos,key):
		for it in struct[objs_key]:
			idx = struct[objs_key].index(it);
			pp = reg + it['str'];
			#在 玩 完了
			if pos == 'after': pp = it['str'] + reg;
			comp = re.compile(pp);
			match = comp.search(struct['text']);
			if match is None: continue;
			tdic = dict();
			tdic['type'] = key + it['type'];
			tdic['stype'] = key + it['stype'];
			tdic['str'] = match.group(0);
			tdic['verb'] = it;
			if pos == 'after':
				tdic['type'] = it['type'] + key;
				tdic['stype'] = it['stype'] + key;
			struct[objs_key][idx] = tdic;

#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第一层的解析 合并一些 符合条件的 词组 比如 数字单位组个
class Fetch1Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self._fetch_1L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_1L(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			if key == 'MERGE':
				for it in item:
					self._merge_objs(struct,it);
			elif key == 'USELESS':
				for it in item:
					self._fetch_useless(struct,it);

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['start']): return None;
		if not struct.has_key(item['end']): return None;
		if not struct.has_key(item['key']): struct[item['key']] = list();
		pid = tid = 0;
		while True:
			if pid >= len(struct[item['start']]): break;
			pit = struct[item['start']][pid];
			tid = 0;
			while True:
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				pstr = pit['str'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					tdic = dict();
					tdic['str'] = pstr;
					if item['force'] == 'tail':
						tdic['type'] = vit['type'];
						tdic['stype'] = vit['stype'];
					elif item['force'] == 'prev':
						tdic['type'] = pit['type'];
						tdic['stype'] = pit['stype'];
					tdic['stc'] = [pit,vit];
					struct[item['key']].append(tdic);
					struct['remove'].append(pit['str']);
					struct['remove'].append(vit['str']);
					del struct[item['start']][pid];
					del struct[item['end']][tid];
					tid = tid - 1;
					pid = pid - 1;
					Sutil._merge_some_words(struct,pstr,0);
				tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['end']]) == 0: del struct[item['end']];
		if len(struct[item['start']]) == 0: del struct[item['start']];

	def _fetch_useless(self,struct,key):
		if not struct.has_key(key): return None;
		tid = 0;
		while True:
			if tid >= len(struct[key]): break;
			vit = struct[key][tid];
			struct['text'] = struct['text'].replace(vit['str'],'',1);
			tid = tid + 1;

#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第三层的解析 合并一些 符合条件的 结构
class Fetch3Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self._fetch_3L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_3L(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				self._merge_objs(struct,it);

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['start']): return None;
		if not struct.has_key(item['end']): return None;

		pid = tid = 0;
		while True:
			if pid >= len(struct[item['start']]): break;

			pit = struct[item['start']][pid];
			if pit['type'] <> item['st'] and item['st'] <> '*':
				pid = pid + 1;
				continue;

			tid = 0;
			while True:
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				if vit['type'] <> item['et'] and item['et'] <> '*':
					tid = tid + 1;
					continue;

				pstr = pit['str'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					if item['force'] == 'tail':
						vit[item['type']] = pit;
						struct['text'] = struct['text'].replace(pstr,vit['str'],1);
						struct['remove'].append(pit['str']);
						del struct[item['start']][pid];
						pid = pid - 1;
					elif item['force'] == 'prev':
						pit[item['type']] = vit;
						struct['text'] = struct['text'].replace(pstr,pit['str'],1);
						struct['remove'].append(vit['str']);
						del struct[item['end']][tid];
						tid = tid - 1;
				tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['end']]) == 0: del struct[item['end']];
		if len(struct[item['start']]) == 0: del struct[item['start']];
